# Typed Proxies

## What Are Typed Proxies?

When REFramework.NET loads, it reads the game's **type database (TDB)** and generates C# reference assemblies that mirror every type in the engine. These assemblies contain interfaces with properties for fields and methods matching the original game types.

The generated assemblies live in:

```
reframework/plugins/managed/generated/
```

Add them as references in your project to get full IntelliSense, autocomplete, and compile-time type checking against game types. You never write these files — REFramework produces them automatically from the running game.

Each generated interface corresponds to a game type. When you cast a `ManagedObject` to one of these interfaces, property accesses and method calls are forwarded to the underlying game object through REFramework's interop layer.

## Namespace Mapping

Game type names map directly to C# namespaces and interface names. The namespace separator `.` in the TDB becomes a C# namespace boundary:

| Game TDB type | C# interface |
|---|---|
| `app.PlayerManager` | `app.PlayerManager` |
| `via.Transform` | `via.Transform` |
| `ace.WeatherManager` | `ace.WeatherManager` |
| `System.Array` | `_System.Array` |
| `System.String` | `_System.String` |

The `System` namespace is prefixed with an underscore (`_System`) to avoid conflicts with the real `System` namespace in .NET. All other namespaces map one-to-one.

## `REFType` Static Field

Every generated interface has a static field:

```csharp
static TypeDefinition REFType
```

This gives you the `TypeDefinition` for that game type without string-based lookup.

**Before (reflection):**

```csharp
var typeDef = API.GetTDB().FindType("app.GuiSaveDataInfo");
```

**After (typed proxy):**

```csharp
var typeDef = app.GuiSaveDataInfo.REFType;
```

From a `TypeDefinition` you can:

```csharp
// Look up methods
var method = app.GuiSaveDataInfo.REFType.GetMethod("someMethod");

// Create a new instance of the type
var instance = app.GuiSaveDataInfo.REFType.CreateInstance();

// Create a managed array of the type
var array = app.GuiSaveDataInfo.REFType.CreateManagedArray(100);
array.Globalize(); // prevent GC collection if you need to keep it
```

## `.As<T>()` Casting

Cast any `ManagedObject` to a typed proxy interface with `.As<T>()`:

```csharp
var managedObj = ManagedObject.ToManagedObject(address);
var typed = managedObj.As<app.SaveSlotPartition>();
```

The underlying object is unchanged — `.As<T>()` returns a typed wrapper that gives you property and method access. It returns `null` if the cast is not valid.

```csharp
var obj = ManagedObject.ToManagedObject(args[1]);
var player = obj?.As<app.PlayerManager>();
if (player != null) {
    // Use typed access
}
```

## Property Access (Fields)

Generated interfaces expose game object fields as C# get/set properties. Field names are preserved from the TDB, including the underscore prefix convention common in RE Engine types.

**Before (reflection):**

```csharp
int count = (int)managedObj.GetField("_SlotCount");
managedObj.SetField("_SlotCount", 90);
```

**After (typed proxy):**

```csharp
var partition = managedObj.As<app.SaveSlotPartition>();
int count = partition._SlotCount;   // read
partition._SlotCount = 90;          // write
```

Typed property access is cleaner, caught at compile time, and visible in IntelliSense.

## Method Calls

Generated interfaces expose game methods directly as C# methods. Property getters/setters in the TDB appear as C# properties.

**Before (reflection):**

```csharp
(saveMgr as IObject).Call("reloadSaveSlotInfo");
bool ready = (bool)(saveMgr as IObject).Call("get_IsInitialized");
```

**After (typed proxy):**

```csharp
var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();
saveMgr.reloadSaveSlotInfo();
bool ready = saveMgr.IsInitialized;
```

Method arguments and return types are also typed when the signature is representable in C#.

## Enum Types

Game enums from the TDB are generated as real C# enums. Use them instead of magic integers.

**Before (magic constants):**

```csharp
if ((int)part.GetField("_Usage") == 3) { ... }
```

**After (typed enum):**

```csharp
var part = managedObj.As<app.SaveSlotPartition>();
if (part._Usage == app.SaveSlotCategory.Game) { ... }
```

Enums work in `switch` statements, comparisons, and flags operations as expected:

```csharp
switch (part._Usage) {
    case app.SaveSlotCategory.Game:
        // handle game save
        break;
    case app.SaveSlotCategory.System:
        // handle system save
        break;
}
```

## Getting Typed Singletons

Use `API.GetManagedSingletonT<T>()` to retrieve a game singleton already cast to its typed proxy:

**Before:**

```csharp
var mo = API.GetManagedSingleton("app.SaveServiceManager");
var saveMgr = mo.As<app.SaveServiceManager>();
```

**After:**

```csharp
var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();
saveMgr.reloadSaveSlotInfo();
saveMgr._MaxUseSaveSlotCount = 117;
```

One call, fully typed from the start.

## When Typed Proxies Don't Work

Typed proxies cover the vast majority of game types, but there are cases where you must fall back to reflection-style access through `IObject` / `ManagedObject`:

- **Generic types** — Types like `CatalogSetDictionary<K,V>` or `List<T>` specializations do not have generated typed proxies. Use `IObject.Call()` and `ManagedObject.GetField()` instead.
- **Complex method signatures** — Some methods with unusual parameter types (pointers, `ref` structs, nested generics) may not appear on the generated interface.
- **Dynamically discovered types** — If you resolve a type at runtime by name, you already have a `ManagedObject` and may not know the concrete interface at compile time.

Fallback example for a generic type:

```csharp
var dict = managedObj.As<app.SomeGenericContainer>(); // null — no proxy exists
// Fall back to reflection
var mo = managedObj as IObject;
var count = (int)mo.Call("get_Count");
var value = mo.Call("get_Item", key);
```

You can freely mix typed proxies and reflection on the same object. Use typed access where available and drop to reflection only where necessary.


## Proxy Factory Classes

Under the hood, `.As<T>()` creates a `DispatchProxy` that forwards calls to the underlying `IObject`. Three factory classes are available for advanced scenarios where you need to create proxies manually:

| Class | Underlying type | Use case |
|---|---|---|
| `ManagedProxy<T>` | `ManagedObject` | Most game objects (GC-managed) |
| `NativeProxy<T>` | `NativeObject` | Native engine objects (not GC-managed) |
| `AnyProxy<T>` | `IObject` | When you don't know the object kind |

Each has a static `Create(object target)` method:

```csharp
// Create proxy manually from a ManagedObject
var mo = API.GetManagedSingleton("app.SaveServiceManager");
var saveMgr = ManagedProxy<app.SaveServiceManager>.Create(mo);
```

`ManagedProxy<T>` and `NativeProxy<T>` also have a convenience method:

```csharp
// Create directly from a singleton name
var saveMgr = ManagedProxy<app.SaveServiceManager>.CreateFromSingleton("app.SaveServiceManager");
```

In practice, prefer `.As<T>()` and `API.GetManagedSingletonT<T>()` — they handle the proxy creation for you. Use the factory classes only when you have a specific need to control the proxy kind.

## Iterating Game Collections

### Typed Proxies (recommended)

Typed proxies implement `REFrameworkNET.Collections.IDictionary<K,V>`, `IList<T>`, `ICollection<T>`, etc. These interfaces provide idiomatic C# iteration that **works correctly**:

```csharp
var saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();

// Dictionary — iterate keys, values, or use indexer
var handlers = saveMgr._GameSlotSaveHandlers;  // IDictionary<string, GameSlotSaveHandler>
API.LogInfo($"Count: {handlers.Count}");        // 37

foreach (var key in handlers.Keys) {
    API.LogInfo($"Key: {key}");                  // "AchievementManager", "CharacterManager", ...
}

foreach (var val in handlers.Values) {
    // val is a real GameSlotSaveHandler proxy — not null
}

var handler = handlers["CharacterManager"];      // indexer works

// List — direct foreach
var requests = saveMgr._ProcessRequests;          // IList<Process>
foreach (var req in requests) {
    // each req is a real Process proxy
}
```

Tested live against RE9 with 37 dictionary entries — keys return real `System.String` values, values return real `GameSlotSaveHandler` proxy objects, indexer works.

> **Important:** Do NOT cast proxies to `System.Collections.IEnumerable`. Proxies implement `REFrameworkNET.Collections.IList<T>` / `IDictionary<K,V>` — these are different interfaces with their own `GetEnumerator()` that dispatches correctly through the proxy system.

### ManagedObject (fallback)

`ManagedObject` implements `System.Collections.IEnumerable` via `ObjectEnumerator`, which calls `get_Count`/`get_Length` + `get_Item(int)`. This **only works for arrays**:

| Type | Works via ManagedObject? | Why |
|------|------------------------|-----|
| `T[]` (arrays) | **Yes** | Has `get_Length` + `get_Item(int)` |
| `List<T>` | Untested with data | Has `get_Count` + `get_Item(int)` — should work |
| `Dictionary<K,V>` | **No — silent nulls** | `get_Item` takes a key, not int; yields N nulls |
| `CatalogSetDictionary` | **No — silent nulls** | No `get_Item` at all |
| `Queue<T>`, `HashSet<T>` | **No** | No `get_Item(int)` |

```csharp
// WORKS: T[] arrays via ManagedObject
var arr = someObj.GetField("_SomeArray") as ManagedObject;
foreach (var item in (IEnumerable)arr) {
    var typed = ((ManagedObject)item).As<app.SomeType>();
}

// BROKEN: Dictionary via ManagedObject — silently yields all null
var dict = someObj.GetField("_SomeDict") as ManagedObject;
foreach (var item in (IEnumerable)dict) {
    // item is ALWAYS null, no error thrown
}
```

> **Rule of thumb:** Use typed proxies for collection iteration. Only fall back to `ManagedObject` for arrays or when proxy types aren't available.

## ValueType and Stack-Allocated Structs

Some game types are value types (structs), not reference types. Use `ValueType.New<T>()` to create a stack-allocated boxed value:

```csharp
var vec3 = ValueType.New<via.vec3>();
// Set fields on the value type
(vec3 as IObject).Call("set_x", 1.0f);
(vec3 as IObject).Call("set_y", 2.0f);
(vec3 as IObject).Call("set_z", 3.0f);

// Pass to a method that expects a value type
transform.Call("set_Position", vec3);
```

You can also create value types from a `TypeDefinition`:

```csharp
var typeDef = API.GetTDB().FindType("via.Quaternion");
var quat = typeDef.CreateValueType();
```

`ValueType` wraps a managed byte array sized to the type's `ValueTypeSize`. It implements `IObject`, so you can call methods and access fields on it.