# ManagedObject, NativeObject & IObject

This page covers the core object types you interact with in REFramework.NET: `ManagedObject` for GC-managed engine objects, `NativeObject` for native engine objects, and the `IObject` interface for reflection-style access.

## ManagedObject

`ManagedObject` represents a garbage-collected object inside the RE Engine's managed runtime. Most game objects you interact with — enemies, save managers, UI elements — are managed objects.

### Creating from a raw address

In hooks, you receive raw `ulong` addresses. Convert them to `ManagedObject` instances:

```csharp
var mo = ManagedObject.ToManagedObject(address);
if (mo == null) {
    // address was 0 or invalid
    return;
}
```

This is the primary way to get a `ManagedObject` in pre-hooks, where `args[1]` is the `this` pointer and `args[2+]` are parameters:

```csharp
[MethodHook(typeof(app.SaveManager), nameof(app.SaveManager.save), MethodHookType.Pre)]
static PreHookResult OnSavePre(Span<ulong> args) {
    var self = ManagedObject.ToManagedObject(args[1])?.As<app.SaveManager>();
    if (self == null) return PreHookResult.Continue;

    API.LogInfo($"Save triggered, slot count: {self._MaxUseSaveSlotCount}");
    return PreHookResult.Continue;
}
```

### Casting to typed proxies with `.As<T>()`

Typed proxies give you compile-time access to fields, properties, and methods. Cast with `.As<T>()`:

```csharp
var mo = ManagedObject.ToManagedObject(address);
var typed = mo.As<app.SaveServiceManager>();

// Now you get autocomplete, type checking, and direct field access:
bool ready = typed.IsInitialized;
typed._MaxUseSaveSlotCount = 117;
typed.reloadSaveSlotInfo();
```

The type parameter `T` must be a generated proxy interface from the TDB reference assemblies (namespaces like `app`, `via`, `ace`, `_System`). Every generated type has a static `REFType` field that returns its `TypeDefinition`:

```csharp
TypeDefinition td = app.SaveServiceManager.REFType;
```

### Getting the raw address

Use `.GetAddress()` to retrieve the raw `ulong` address. This is required when modifying a post-hook's return value:

```csharp
[MethodHook(typeof(app.SomeFactory), nameof(app.SomeFactory.create), MethodHookType.Post)]
static void OnCreatePost(ref ulong retval) {
    var original = ManagedObject.ToManagedObject(retval);
    // ... modify or replace ...
    retval = replacement.GetAddress();
}
```

### Reading fields by name

`.GetField(string name)` reads a field reflectively. It returns `object` — a `ManagedObject` for reference types, or a boxed value for value types (`int`, `float`, `bool`, enums):

```csharp
var mo = ManagedObject.ToManagedObject(address);
string name = (string)mo.GetField("_Name");
int count = (int)mo.GetField("_Count");
var child = (ManagedObject)mo.GetField("_ChildRef");
```

Prefer typed proxies (`.As<T>()`) over `GetField` when the type is available. `GetField` is useful for types without generated proxies or when working generically.

### Getting the type at runtime

`.GetTypeDefinition()` returns the `TypeDefinition` for the object's actual runtime type:

```csharp
var mo = ManagedObject.ToManagedObject(address);
TypeDefinition td = mo.GetTypeDefinition();
API.LogInfo($"Object type: {td.GetFullName()}");
```

## IObject Interface

`IObject` is the common interface for reflection-style access. Both `ManagedObject` and typed proxy interfaces implement it. Use it when typed proxies are unavailable or when you need dynamic dispatch.

### Calling methods by name

```csharp
var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();

// Reflection-style call via IObject:
object result = (saveMgr as IObject).Call("reloadSaveSlotInfo");
```

Pass arguments positionally:

```csharp
object result = (obj as IObject).Call("setValue", 42, true);
```

### Disambiguating overloaded methods

When a type has overloaded methods, include the parameter signature in the method name string:

```csharp
object result = (obj as IObject).Call("getValue(app.SaveSlotSegmentType)", segmentValue);
```

### Reading fields via IObject

```csharp
object val = (obj as IObject).GetField("_Name");
```

### When to use IObject over typed proxies

- **Generic code** — operating on objects whose type isn't known at compile time
- **Dynamic dispatch** — calling methods determined at runtime
- **Types without proxies** — some generic or internal types may not have generated interfaces
- **Quick prototyping** — when you don't want to look up the exact proxy type

## NativeObject

`NativeObject` represents a native (non-GC) engine object. These are C++ objects managed by the engine itself, not by the managed GC. You encounter them less often in typical plugin code.

Common native singletons include `via.Application`, `via.SceneManager`, and other low-level engine services:

```csharp
// Access a native singleton
var app = API.GetNativeSingletonT<via.Application>();
```

`NativeObject` supports the same `IObject` interface for reflection-style access:

```csharp
var sceneMgr = API.GetNativeSingletonT<via.SceneManager>();
object result = (sceneMgr as IObject).Call("get_CurrentScene");
```

The key difference from `ManagedObject`: native objects are not garbage-collected, so `Globalize()` is not relevant for them. Their lifetime is managed by the engine's native memory systems.

## HandleInvokeMember_Internal

For edge cases where the normal `Call` path doesn't work — null `this` invocations, unusual argument marshaling, or internal method dispatch — use `HandleInvokeMember_Internal` on a `MethodDefinition`:

```csharp
// Get the method definition
var methodDef = app.SomeType.REFType.FindMethod("processData");

// Invoke with explicit control
object result = null;
methodDef.HandleInvokeMember_Internal(instance, new object[] { arg1, arg2 }, ref result);
```

This is a low-level escape hatch. Typical use cases:

- **Null `this` calls** — some static-like methods are declared as instance methods but never read `this`. Pass `null` as the instance:
  ```csharp
  object result = null;
  methodDef.HandleInvokeMember_Internal(null, new object[] { data }, ref result);
  ```
- **Controlled argument marshaling** — when automatic marshaling through `Call` produces incorrect results
- **Debugging invocation issues** — when `Call` throws and you need to isolate why

Prefer `Call` or typed proxy method calls in all normal circumstances.

## Lifetime Management

The RE Engine has its own garbage collector. If you hold a reference to a `ManagedObject` in C# but the engine's GC doesn't know about it, the engine may collect the underlying object. This causes crashes or silent corruption.

### When to call `.Globalize()`

**Globalize any `ManagedObject` that persists across frames.** This tells the engine's GC to keep the object alive.

```csharp
// REQUIRED: storing in a static field
static ManagedObject _cachedManager;

[PluginEntryPoint]
public static void Main() {
    _cachedManager = API.GetManagedSingleton("app.SaveServiceManager");
    _cachedManager.Globalize();  // prevent engine GC from collecting
}
```

```csharp
// REQUIRED: storing in a collection
static List<ManagedObject> _trackedObjects = new();

void TrackObject(ManagedObject obj) {
    obj.Globalize();
    _trackedObjects.Add(obj);
}
```

```csharp
// REQUIRED: arrays you create
var newArray = app.SomeType.REFType.CreateManagedArray(100);
newArray.Globalize();
```

### When Globalize is NOT needed

**Temporary references within a single hook or callback execution do not need Globalize.** The engine's GC will not run mid-callback:

```csharp
[MethodHook(typeof(app.SaveManager), nameof(app.SaveManager.save), MethodHookType.Pre)]
static PreHookResult OnSavePre(Span<ulong> args) {
    // No Globalize needed — these are temporary, used and discarded within this call
    var self = ManagedObject.ToManagedObject(args[1])?.As<app.SaveManager>();
    var slotInfo = self._CurrentSlotInfo;
    API.LogInfo($"Saving slot: {slotInfo._SlotNo}");
    return PreHookResult.Continue;
}
```

**Objects returned by the engine through hooks** are already managed by the engine — you don't need to globalize them unless you store the reference for later.

### Summary

| Scenario | Globalize? |
|---|---|
| Static field / class member | **Yes** |
| Collection (List, Dictionary, array) | **Yes** |
| Newly created managed array | **Yes** |
| Local variable in a hook/callback | No |
| Temporary cast via `.As<T>()` | No |
| Return value you're inspecting but not storing | No |
