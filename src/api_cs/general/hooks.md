# Method Hooks

## Overview

Method hooks let you intercept any game method before and/or after it executes. You can inspect arguments, modify them, skip the original method entirely, or change its return value.

Unlike Lua hooks, C# hooks are **non-blocking** and may **run on multiple threads simultaneously**. The runtime does not serialize hook invocations — if the game calls a hooked method from two threads at once, your hook body runs concurrently on both. This has direct implications for shared state (see [Thread Safety](#thread-safety)).

Hooks are declared with the `[MethodHook]` attribute:

```csharp
[MethodHook(typeof(TargetType), nameof(TargetType.targetMethod), MethodHookType.Pre)]
static PreHookResult MyPreHook(Span<ulong> args) { ... }

[MethodHook(typeof(TargetType), nameof(TargetType.targetMethod), MethodHookType.Post)]
static void MyPostHook(ref ulong retval) { ... }
```

There are three required parameters and one optional:

| Parameter | Meaning |
|-----------|---------|
| `typeof(T)` | The type that declares the method |
| `nameof(T.method)` | The method name to hook |
| `MethodHookType.Pre` or `.Post` | Whether to run before or after the original |
| `bool skipJmp` *(optional)* | When `true`, skips the initial `jmp` instruction at the function entry. Use when hooking functions that have been patched with a trampoline. Defaults to `false`. |

## Pre-Hooks

A pre-hook runs **before** the original method body. Its signature is:

```csharp
static PreHookResult OnPre(Span<ulong> args)
```

### Argument layout

The `args` span contains the raw call arguments as `ulong` values:

| Index | Contents |
|-------|----------|
| `args[0]` | Thread context pointer (rarely needed — used for internal runtime calls) |
| `args[1]` | `this` pointer for **instance methods** |
| `args[2]`, `args[3]`, ... | Method parameters, in declaration order |

For **static methods** there is no `this` pointer — parameters start at `args[1]`:

| Index | Contents |
|-------|----------|
| `args[0]` | Thread context |
| `args[1]` | First parameter |
| `args[2]` | Second parameter, etc. |

### Converting arguments

Reference-type arguments (objects, strings, arrays) are raw addresses. Convert them with `ManagedObject.ToManagedObject`, then cast to a typed proxy:

```csharp
[MethodHook(typeof(app.SaveDataService), nameof(app.SaveDataService.writeSaveData), MethodHookType.Pre)]
static PreHookResult OnWriteSave(Span<ulong> args) {
    var self = ManagedObject.ToManagedObject(args[1])?.As<app.SaveDataService>();
    int slotIndex = (int)args[2]; // value-type param: cast directly

    API.LogInfo($"writeSaveData called on slot {slotIndex}");
    return PreHookResult.Continue;
}
```

Value-type parameters (`int`, `float`, `bool`, enums) are stored directly in the `ulong` — cast them to the appropriate type.

### Return value

| Return | Effect |
|--------|--------|
| `PreHookResult.Continue` | Proceed to the original method (and any post-hooks) |
| `PreHookResult.Skip` | Skip the original method entirely. Post-hooks still run. |

### Modifying arguments

Because `args` is a `Span<ulong>`, writes are visible to the original method:

```csharp
[MethodHook(typeof(app.EnemyDamageParam), nameof(app.EnemyDamageParam.calcDamage), MethodHookType.Pre)]
static PreHookResult OnCalcDamage(Span<ulong> args) {
    // Double the damage value (third parameter)
    args[3] = args[3] * 2;
    return PreHookResult.Continue;
}
```

## Post-Hooks

A post-hook runs **after** the original method returns. There are two valid signatures:

```csharp
// Use this when you need to read or modify the return value
static void OnPost(ref ulong retval)

// Use this when you only need a notification that the method ran
static void OnPost()
```

### Working with the return value

The meaning of `retval` depends on the method's return type:

| Return type | What `retval` contains |
|-------------|----------------------|
| Reference type (object, string, array) | Object address — convert with `ManagedObject.ToManagedObject(retval)` |
| Value type (`int`, `float`, `bool`, enum) | The raw value — cast directly |
| `void` | Undefined — do not read |

Reading a reference-type return:

```csharp
[MethodHook(typeof(app.SaveServiceManager), nameof(app.SaveServiceManager.getSaveSlotInfo), MethodHookType.Post)]
static void OnGetSlotInfo(ref ulong retval) {
    var info = ManagedObject.ToManagedObject(retval)?.As<app.SaveSlotInfo>();
    if (info != null) {
        API.LogInfo($"Slot info returned: chapter {info._ChapterNo}");
    }
}
```

### Replacing the return value

Write to `retval` to change what the caller receives:

```csharp
[MethodHook(typeof(app.SaveServiceManager), nameof(app.SaveServiceManager.getMaxSaveSlotCount), MethodHookType.Post)]
static void OnGetMaxSlots(ref ulong retval) {
    // Override the max slot count
    retval = 117;
}
```

For reference types, set `retval` to the address of a different object:

```csharp
retval = replacementObject.GetAddress();
```

## Combined Pre and Post Hooks

A common pattern hooks the same method with both a pre-hook and a post-hook. The pre-hook captures context (typically `this`), and the post-hook uses it to make modifications after the method has run.

Store captured state in a static field — but see [Thread Safety](#thread-safety) for caveats.

```csharp
static app.GuiSaveLoadController.Unit pendingUnit;

[MethodHook(typeof(app.GuiSaveLoadController.Unit), nameof(app.GuiSaveLoadController.Unit.onSetup), MethodHookType.Pre)]
static PreHookResult OnSetupPre(Span<ulong> args) {
    pendingUnit = ManagedObject.ToManagedObject(args[1])?.As<app.GuiSaveLoadController.Unit>();
    return PreHookResult.Continue;
}

[MethodHook(typeof(app.GuiSaveLoadController.Unit), nameof(app.GuiSaveLoadController.Unit.onSetup), MethodHookType.Post)]
static void OnSetupPost(ref ulong retval) {
    if (pendingUnit != null) {
        pendingUnit._SaveItemNum = 90;
        pendingUnit = null;
    }
}
```

Why not do everything in the pre-hook? Because `onSetup` may initialize fields that you want to override — if you write them before the original runs, the original will overwrite your values.

## Thread Safety

C# hooks are **not serialized**. If the game calls a hooked method from multiple threads, your hook body executes concurrently on all of them.

This means:

- **Read-only hooks** (logging, inspection) are safe without synchronization.
- **Hooks that write to shared state** (static fields, collections) must use locks or other synchronization primitives.

```csharp
static readonly object _lock = new object();
static int totalDamageDealt;

[MethodHook(typeof(app.EnemyDamageParam), nameof(app.EnemyDamageParam.applyDamage), MethodHookType.Pre)]
static PreHookResult OnApplyDamage(Span<ulong> args) {
    int damage = (int)args[2];
    lock (_lock) {
        totalDamageDealt += damage;
    }
    return PreHookResult.Continue;
}
```

The combined pre+post pattern shown above (storing `this` in a static field) is a **race condition** if the hooked method can be called from multiple threads. In practice, many game methods only run on the main thread — but if you are unsure, use `[ThreadStatic]` or a `ConcurrentDictionary` keyed by thread ID:

```csharp
[ThreadStatic]
static app.GuiSaveLoadController.Unit pendingUnit;
```

For more detail, see [Threading](threading.md).

## Hooking Gotchas

### Inlined property accessors

The IL2CPP runtime may inline `get_` and `set_` property accessor methods. When this happens, hooking `get_PropertyName` can trigger on **unrelated call sites** that were inlined to the same native code.

Always verify the object type inside your hook body:

```csharp
[MethodHook(typeof(app.SaveSlotInfo), nameof(app.SaveSlotInfo.get_SlotNo), MethodHookType.Pre)]
static PreHookResult OnGetSlotNo(Span<ulong> args) {
    var self = ManagedObject.ToManagedObject(args[1]);
    if (self == null) return PreHookResult.Continue;

    // Verify the object is actually the type we expect
    var td = self.GetTypeDefinition();
    if (td == null || td.GetFullName() != "app.SaveSlotInfo") {
        return PreHookResult.Continue;
    }

    // Safe to proceed
    var info = self.As<app.SaveSlotInfo>();
    API.LogInfo($"SlotNo accessed: {info.SlotNo}");
    return PreHookResult.Continue;
}
```

### Hooking constructors and virtual methods

- Constructor hooks (`.ctor`) work, but the object may be partially initialized in a pre-hook.
- Virtual method hooks apply to **all overrides** — the hook fires regardless of which subclass implementation is called. Check the concrete type if you need to filter.

### Avoid heavy work in hooks

Hooks run inline with the game's execution. Long-running operations (file I/O, network calls) will stall the game thread. Offload heavy work to a background task if needed.
