# Walkthrough: RE9 Additional Save Slots

> **Full source:** [praydog/RE9AdditionalSaveSlots](https://github.com/praydog/RE9AdditionalSaveSlots) (~250 lines)

This page walks through a real-world REFramework C# plugin that expands RE9's save slot limit from 12 to 90. It exercises nearly every major API surface: entry/exit points, frame callbacks, typed proxies, enums, pre+post method hooks, array manipulation, reflection fallback for generics, and managed object lifetime control.

---

## 1. Introduction

Resident Evil 9 ships with 12 Game save slots. The **Additional Save Slots** plugin raises that to 90 by patching the in-memory save partition data at runtime.

It is a good learning example because it demonstrates:

| Feature | Where it appears |
|---|---|
| `[PluginEntryPoint]` / `[PluginExitPoint]` | Plugin lifecycle |
| `[Callback(typeof(UpdateBehavior))]` | Deferred initialization via frame polling |
| `API.GetManagedSingletonT<T>()` | Accessing game singletons with typed proxies |
| Typed proxy field/property/method access | Reading and writing `_SlotCount`, `_MaxUseSaveSlotCount`, calling `reloadSaveSlotInfo()` |
| Enum comparison via typed proxies | `part._Usage == app.SaveSlotCategory.Game` |
| `IObject.GetField` / `IObject.Call` | Reflection fallback for generic types |
| `[MethodHook]` pre + post pairs | Capturing `this` in pre-hook, patching state in post-hook |
| `_System.Array` + `CreateManagedArray` | Reading, creating, and replacing arrays in post-hooks |
| `ManagedObject.Globalize()` | Preventing GC of plugin-created objects |

---

## 2. Plugin Skeleton

Every REFramework C# plugin is a class with static entry and exit points decorated with attributes:

```csharp
using System;
using REFrameworkNET;
using REFrameworkNET.Attributes;
using REFrameworkNET.Callbacks;

public class AdditionalSavesPlugin {
    const int MAX_GAME_SAVES = 90;

    static bool initialized;
    static app.GuiSaveLoadController.Unit pendingUnit;

    [PluginEntryPoint]
    public static void Main() {
        API.LogInfo("[AdditionalSaves] C# plugin loaded. Waiting for SaveServiceManager...");
    }

    [PluginExitPoint]
    public static void OnUnload() {
        initialized = false;
        pendingUnit = null;
        API.LogInfo("[AdditionalSaves] C# plugin unloaded.");
    }
}
```

Key points:

- **`[PluginEntryPoint]`** marks the method REFramework calls when the plugin DLL is loaded. Game singletons are typically *not* available yet at this point -- do not attempt game logic here.
- **`[PluginExitPoint]`** is called on unload (hot-reload or shutdown). Clean up static state so a re-load starts fresh.
- Static fields hold cross-hook state. `pendingUnit` bridges a pre-hook and its matching post-hook (see [Section 7](#7-prehook--posthook-pattern-onsetup)).

---

## 3. Polling With Callbacks

Game singletons like `SaveServiceManager` are not yet created when your plugin loads. The standard pattern is to register a per-frame callback that polls until the singleton is ready:

```csharp
[Callback(typeof(UpdateBehavior), CallbackType.Pre)]
public static void OnUpdateBehavior() {
    if (initialized) return;

    var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();
    if (saveMgr == null) return;

    if (!saveMgr.IsInitialized) return;

    if (ExpandGamePartition(saveMgr)) {
        initialized = true;
        API.LogInfo($"[AdditionalSaves] Initialization complete. MAX_GAME_SAVES = {MAX_GAME_SAVES}");
    }
}
```

The `[Callback(typeof(UpdateBehavior), CallbackType.Pre)]` attribute registers this method to run every frame, *before* the engine's own update tick. Once `initialized` is set, the early return makes the per-frame cost negligible.

This is the idiomatic way to defer initialization. Do **not** spin-wait or sleep in `Main()` -- the game is single-threaded and you will deadlock.

---

## 4. Reading Typed Singletons

```csharp
var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();
```

`API.GetManagedSingletonT<T>()` returns a **typed proxy** -- an interface generated from the game's type database (TDB). Through it you get compile-time access to fields, properties, and methods:

```csharp
if (!saveMgr.IsInitialized) return;       // property read
saveMgr._MaxUseSaveSlotCount = newMax;     // field write
saveMgr.reloadSaveSlotInfo();              // method call
```

No reflection strings, no casts. If you misspell a member name the C# compiler catches it.

---

## 5. Navigating the Object Graph (Generic Type Fallback)

Not all game types have typed proxies. Generic types like `CatalogSetDictionary<K, V>` are not represented in the TDB as distinct closed types, so you must fall back to `IObject` reflection:

```csharp
static ManagedObject GetDefaultSegmentItemSet(app.SaveServiceManager saveMgr) {
    // _SaveSlotPartitions is a generic CatalogSetDictionary -- no typed proxy
    var partitionsDict = (saveMgr as IObject).GetField("_SaveSlotPartitions") as ManagedObject;
    if (partitionsDict == null) return null;

    // Try getValue(Default_0) -> _Source
    ManagedObject valueColl = null;
    try {
        valueColl = (partitionsDict as IObject)?.Call(
            "getValue(app.SaveSlotSegmentType)",
            (int)app.SaveSlotSegmentType.Default_0) as ManagedObject;
    } catch { }

    if (valueColl != null) {
        var itemSet = valueColl.GetField("_Source") as ManagedObject;
        if (itemSet != null) return itemSet;
    }

    // Fallback: _Dict -> FindValue
    var dict = partitionsDict.GetField("_Dict") as ManagedObject;
    if (dict == null) return null;

    return (dict as IObject)?.Call(
        "FindValue(app.SaveSlotSegmentType)",
        (int)app.SaveSlotSegmentType.Default_0) as ManagedObject;
}
```

The pattern:

1. Cast a typed proxy to `IObject` to access fields/methods by string name.
2. Use `GetField("name")` for field reads -- returns `object` (box or `ManagedObject`).
3. Use `Call("methodName(paramTypes)", args...)` for method calls. The method signature string disambiguates overloads.
4. Enum arguments are passed as `(int)` casts.
5. Build in a **fallback path**. Game updates may change internal dictionary implementations. This plugin tries `getValue()` first, then falls back to navigating `_Dict.FindValue()`.

---

## 6. Using Typed Proxies and Enums

Once you have the partitions array, typed proxies and enums make iteration clean:

```csharp
var partitionsArr = partitionsArrMo.As<_System.Array>();
int arrSize = partitionsArr.Length;

app.SaveSlotPartition gamePartition = null;

for (int i = 0; i < arrSize; i++) {
    var partMo = partitionsArr.GetValue(i) as ManagedObject;
    if (partMo == null) continue;

    var part = partMo.As<app.SaveSlotPartition>();
    if (part == null) continue;

    if (part._Usage == app.SaveSlotCategory.Game) {
        gamePartition = part;
    }
}

// Patch the partition
gamePartition._SlotCount = MAX_GAME_SAVES;
```

Key details:

- **`_System.Array`** is the typed proxy for `System.Array`. Use `.GetValue(i)` and `.SetValue(elem, i)` for element access.
- **`.As<T>()`** on `ManagedObject` casts to any typed proxy interface. It does not copy -- it wraps the same underlying managed object.
- **Enum comparison** works directly: `part._Usage == app.SaveSlotCategory.Game`. The generated enum type mirrors the game's TDB enum values.
- **Field writes** like `._SlotCount = MAX_GAME_SAVES` go through the typed proxy's property setter, which writes directly to the managed object's memory.

---

## 7. Pre+Post Hook Pattern (`onSetup`)

Some patches require context from *before* a method runs to make decisions *after* it returns. The pre+post hook pair solves this:

```csharp
static app.GuiSaveLoadController.Unit pendingUnit;

[MethodHook(typeof(app.GuiSaveLoadController.Unit),
            nameof(app.GuiSaveLoadController.Unit.onSetup),
            MethodHookType.Pre)]
public static PreHookResult OnSetupPre(Span<ulong> args) {
    pendingUnit = ManagedObject.ToManagedObject(args[1])
        ?.As<app.GuiSaveLoadController.Unit>();
    return PreHookResult.Continue;
}

[MethodHook(typeof(app.GuiSaveLoadController.Unit),
            nameof(app.GuiSaveLoadController.Unit.onSetup),
            MethodHookType.Post)]
public static void OnSetupPost(ref ulong retval) {
    if (!initialized || pendingUnit == null) return;

    try {
        int current = pendingUnit._SaveItemNum;
        if (current < MAX_GAME_SAVES) {
            pendingUnit._SaveItemNum = MAX_GAME_SAVES;
        }
    } catch (Exception e) {
        API.LogWarning($"[AdditionalSaves] onSetup patch failed: {e.Message}");
    }

    pendingUnit = null;  // always clear
}
```

How it works:

1. **Pre-hook** receives `Span<ulong> args`. `args[0]` is the thread context, `args[1]` is `this`, `args[2+]` are the method parameters. Convert `args[1]` to a typed proxy and stash it in a static field.
2. Return `PreHookResult.Continue` to let the original method execute (or `PreHookResult.Skip` to suppress it).
3. **Post-hook** receives `ref ulong retval`. It reads the stashed reference, patches the object, then **nulls the reference** to avoid holding a stale pointer.

Always null your stashed references in the post-hook. The managed object could be collected between frames if you hold onto it.

---

## 8. Array Manipulation in a Post-Hook (`makeSaveDataList`)

The most complex hook replaces the return value of `makeSaveDataList` with a larger array:

```csharp
[MethodHook(typeof(app.GuiSaveLoadModel),
            nameof(app.GuiSaveLoadModel.makeSaveDataList),
            MethodHookType.Post)]
public static void OnMakeSaveDataListPost(ref ulong retval) {
    if (!initialized) return;

    var arr = ManagedObject.ToManagedObject(retval)?.As<_System.Array>();
    if (arr == null || arr.Length >= MAX_GAME_SAVES) return;

    int len = arr.Length;

    // Create expanded array from the element's TypeDefinition
    var newArrMo = app.GuiSaveDataInfo.REFType.CreateManagedArray((uint)MAX_GAME_SAVES);
    newArrMo.Globalize();  // prevent GC -- we are returning this
    var newArr = newArrMo.As<_System.Array>();

    // Copy existing elements
    for (int i = 0; i < len; i++) {
        var elem = arr.GetValue(i);
        if (elem != null) newArr.SetValue(elem, i);
    }

    // Fill new slots
    // ... (calls makeSaveData for each new index)

    retval = newArrMo.GetAddress();  // replace return value
}
```

Critical details:

- **`TypeDefinition.CreateManagedArray(count)`** allocates a new managed array of that element type. Access the `TypeDefinition` via the static `REFType` field on any generated type (e.g., `app.GuiSaveDataInfo.REFType`).
- **`Globalize()`** is mandatory for any `ManagedObject` your plugin creates and passes back to the game. Without it, the .NET GC may collect the object while the game still references it.
- **`retval = newArrMo.GetAddress()`** replaces what the caller sees. `GetAddress()` returns the raw native pointer as `ulong`, which is what `retval` expects.
- Copy elements from the old array before replacing. The game already populated those slots -- you are extending, not replacing.

---

## 9. Key Takeaways

1. **Prefer typed proxies.** They give compile-time safety and read like normal C#. Use `API.GetManagedSingletonT<T>()` and `.As<T>()`.

2. **Fall back to `IObject` for generics.** When a type has no generated proxy (generics, internal framework types), cast to `IObject` and use `GetField`/`Call` with string names.

3. **`Globalize()` arrays and objects you create.** Any `ManagedObject` your plugin allocates and hands off to the game must be globalized, or it will be collected.

4. **Use callbacks for deferred init.** Game singletons are not ready at plugin load time. Poll in an `UpdateBehavior` callback and gate on a flag.

5. **Combine pre+post hooks for context.** Capture `this` or arguments in the pre-hook, act on them in the post-hook, then null the reference.

6. **Enums work natively.** Generated enum types like `app.SaveSlotCategory` compare directly with `==`. Pass them to `IObject.Call` as `(int)` casts.

7. **Replace return values carefully.** In a post-hook, set `retval` to `GetAddress()` of the replacement object. The original return value is gone -- make sure the replacement is valid.

8. **Build fallback paths.** Game updates change internals. Where possible, try the primary access path and fall back to an alternative (as seen in `GetDefaultSegmentItemSet`).
