# API, TDB & VM — Core Static Classes

These three static classes are the primary entry points for REFramework.NET plugins. They provide logging, singleton access, type database queries, and managed string allocation.

## API (`REFrameworkNET.API`)

All members are static. This is your main interface to the REFramework runtime.

### Logging

```csharp
API.LogInfo("Player spawned");
API.LogWarning("Config file missing, using defaults");
API.LogError("Failed to resolve singleton");
```

| Method | Description |
|---|---|
| `LogInfo(string message)` | Log at Info level |
| `LogWarning(string message)` | Log at Warning level |
| `LogError(string message)` | Log at Error level |

Two static properties control log behavior:

| Property | Type | Default | Description |
|---|---|---|---|
| `LogLevel` | `LogLevel` enum (`Info`, `Warning`, `Error`) | `Info` | Minimum severity that gets emitted. Set to `Warning` to suppress info-level noise. |
| `LogToConsole` | `bool` | `true` | When `true`, log messages are also printed to the REFramework console window. |

```csharp
// Suppress info logs during a hot loop
API.LogLevel = LogLevel.Warning;

// Disable console mirroring
API.LogToConsole = false;
```

### Singleton access

Singletons are how you reach into the running game. Most game managers (`app.PlayerManager`, `app.EnemyManager`, etc.) are managed singletons; engine subsystems (`via.SceneManager`, `via.Application`) are native singletons.

#### Untyped access

```csharp
ManagedObject playerMgr = API.GetManagedSingleton("app.PlayerManager");
NativeObject sceneMgr = API.GetNativeSingleton("via.SceneManager");
```

| Method | Returns | Description |
|---|---|---|
| `GetManagedSingleton(string name)` | `ManagedObject` | Retrieve a managed singleton by its full type name. Returns `null` if not found. |
| `GetNativeSingleton(string name)` | `NativeObject` | Retrieve a native singleton by its full type name. Returns `null` if not found. |

#### Generic typed access

The generic variants call `GetManagedSingleton` / `GetNativeSingleton` under the hood and then cast to a typed proxy via `.As<T>()`. This is the preferred approach when you have generated proxy types:

```csharp
var playerMgr = API.GetManagedSingletonT<app.PlayerManager>();
var sceneMgr = API.GetNativeSingletonT<via.SceneManager>();

// playerMgr is already typed — direct field/method access:
var player = playerMgr.get_CurrentPlayer();
```

| Method | Returns | Constraint |
|---|---|---|
| `GetManagedSingletonT<T>()` | `T` | `T : ref class` (proxy type) |
| `GetNativeSingletonT<T>()` | `T` | `T : ref class` (proxy type) |

Both return `null` (default of `T`) if the singleton is not found.

> **Caveat:** `NativeSingleton` does **not** carry a `TypeDefinition` — only a `TypeInfo` handle. This means `GetNativeSingleton(name)` returns a `NativeObject` that lacks the typed proxy path. Use `GetNativeSingletonT<T>()` when you need typed access to native singletons.

#### Enumerating all singletons

```csharp
List<ManagedSingleton> managed = API.GetManagedSingletons();
List<NativeSingleton> native = API.GetNativeSingletons();

foreach (var s in managed) {
    API.LogInfo($"Managed: {s.Name} @ 0x{s.Instance.GetAddress():X}");
}
```

| Method | Returns |
|---|---|
| `GetManagedSingletons()` | `List<ManagedSingleton>` — all currently registered managed singletons |
| `GetNativeSingletons()` | `List<NativeSingleton>` — all currently registered native singletons |

### GC — `LocalFrameGC()`

```csharp
API.LocalFrameGC();
```

Flushes the RE Engine VM's local reference frame. Call this on **custom threads** (not the main game thread) after performing bulk managed allocations or method invocations. Without it, local references accumulate and can crash the managed heap.

On the main thread, the engine handles this automatically each frame. You only need to call it manually in background workers or long-running loops.

### UI — `IsDrawingUI()`

```csharp
if (API.IsDrawingUI()) {
    ImGui.Text("Overlay is visible");
}
```

Returns `true` while REFramework's ImGui overlay is actively rendering. Use this to conditionally draw ImGui elements inside your render callbacks — avoids drawing when the overlay is hidden.

### Plugin directory — `GetPluginDirectory(Assembly)`

```csharp
string dir = API.GetPluginDirectory(typeof(MyPlugin).Assembly);
string configPath = Path.Combine(dir, "config.json");
```

Returns the directory containing the calling plugin's `.cs` source file or `.dll`. Useful for loading configuration files, assets, or data relative to your plugin without hardcoding paths.

### TDB shortcut — `GetTDB()`

```csharp
TDB tdb = API.GetTDB();
```

Equivalent to `TDB.Get()`. Convenience accessor when you already have `API` in scope.

---

## TDB (`REFrameworkNET.TDB`)

The **Type Database** — REFramework's reflection system over the RE Engine's type metadata. Access it via `TDB.Get()` or `API.GetTDB()`.

### Type lookup

| Method | Returns | Description |
|---|---|---|
| `FindType(string name)` | `TypeDefinition` | Look up a type by full name (e.g. `"app.PlayerManager"`). **Not cached** — avoid in hot paths. |
| `GetType(uint index)` | `TypeDefinition` | Look up by numeric TDB index. |
| `GetType(string name)` | `TypeDefinition` | Alias for `FindType`. |
| `FindTypeByFqn(uint fqn)` | `TypeDefinition` | Look up by FQN hash. |
| `GetTypeT<T>()` | `TypeDefinition` | **Cached** lookup using the proxy type's compile-time metadata. **Prefer this on hot paths.** |

```csharp
var tdb = TDB.Get();

// One-off lookup (fine in init code):
TypeDefinition td = tdb.FindType("app.PlayerManager");

// Hot-path lookup (cached, no string allocation):
TypeDefinition td2 = tdb.GetTypeT<app.PlayerManager>();
```

### Method and field lookup

```csharp
Method m = tdb.FindMethod("app.PlayerManager", "get_CurrentPlayer");
Field f = tdb.FindField("app.EnemyContext", "_ConditionDamageList");
```

| Method | Returns | Description |
|---|---|---|
| `FindMethod(string typeName, string methodName)` | `Method` | Find a method by type name and method name. |
| `FindField(string typeName, string fieldName)` | `Field` | Find a field by type name and field name. |

### Metadata counts

```csharp
var tdb = TDB.Get();
API.LogInfo($"Types: {tdb.GetNumTypes()}, Methods: {tdb.GetNumMethods()}, " +
            $"Fields: {tdb.GetNumFields()}, Properties: {tdb.GetNumProperties()}");
```

| Method | Returns |
|---|---|
| `GetNumTypes()` | `uint` — total type count in the TDB |
| `GetNumMethods()` | `uint` — total method count |
| `GetNumFields()` | `uint` — total field count |
| `GetNumProperties()` | `uint` — total property count |

### Iterating all types

The `Types` property returns an iterable collection of every `TypeDefinition` in the database:

```csharp
foreach (var td in TDB.Get().Types) {
    if (td.GetFullName().Contains("Enemy")) {
        API.LogInfo($"Found: {td.GetFullName()} (index {td.GetIndex()})");
    }
}
```

> **Performance note:** This iterates the entire TDB. Use `FindType` or `GetTypeT<T>` for targeted lookups.

---

## VM (`REFrameworkNET.VM`)

Low-level access to the RE Engine's managed virtual machine.

### `CreateString(string)` → `SystemString`

Allocates a `System.String` on the RE Engine's managed GC heap. Use this when you need to pass a string argument to a game method via reflection:

```csharp
var greeting = VM.CreateString("Hello, Hunter!");
method.Invoke(obj, new object[] { greeting });
```

The returned `SystemString` is a `ManagedObject`. It is subject to the engine's garbage collector — if you need to store it beyond the current frame, call `Globalize()` to prevent collection:

```csharp
var persistent = VM.CreateString("Cached label");
persistent.Globalize();
// Safe to store in a static field now
```

> **When do you need this?** Whenever you call a game method that expects a managed `System.String` parameter. Passing a raw C# `string` will not work — the engine expects its own heap-allocated string object.

`SystemString` extends `ManagedObject` and overrides `ToString()`, so you can read engine strings back to C#:

```csharp
// Reading a string field from a game object
var nameField = someObj.GetField("_Name");
string name = nameField?.ToString(); // calls SystemString.ToString()
```

---

## Quick reference

```csharp
// Logging
API.LogInfo("message");
API.LogLevel = LogLevel.Warning;

// Singletons (typed)
var mgr = API.GetManagedSingletonT<app.PlayerManager>();

// Type database
var td = TDB.Get().FindType("app.EnemyManager");
var m  = TDB.Get().FindMethod("app.EnemyManager", "getEnemyCount");

// String allocation
var s = VM.CreateString("text");

// Plugin-relative paths
var dir = API.GetPluginDirectory(typeof(MyPlugin).Assembly);

// GC on custom threads
API.LocalFrameGC();
```
