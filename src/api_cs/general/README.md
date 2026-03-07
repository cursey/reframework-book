# REFramework.NET

REFramework.NET is a C# scripting API that lets you build mods and plugins for RE Engine games. It provides direct access to the engine's type system, managed objects, and native functions through a generated typed proxy layer, with performance 3-7x faster than Lua (single-threaded) and up to 80x faster in multi-threaded scenarios.

## Features

* **Runtime compilation** — Place a `.cs` file in `reframework/plugins/source/` and it compiles automatically. Edit, save, and the plugin hot-reloads without restarting the game.
* **Typed proxy generation** — Reference assemblies are auto-generated from the game's type database (TDB). Every game type becomes a C# interface with properties, methods, and enums. Full IDE autocomplete.
* **Method hooking** — Intercept any game method before or after execution. Inspect/modify arguments, skip the original, or replace return values. Non-blocking: hooks run on multiple threads simultaneously.
* **Engine callbacks** — Register for per-frame updates, draw events, and other engine lifecycle points.
* **Pre-compiled assembly support** — Ship `.dll` plugins for production, use `.cs` source files for development.

## Getting Started

### Prerequisites

* [.NET 10.0 runtime](https://dotnet.microsoft.com/en-us/download/dotnet/10.0) installed on your system
* [REFramework nightly build](https://github.com/praydog/REFramework-nightly/releases) with .NET support
* `csharp-api.zip` from the [same releases page](https://github.com/praydog/REFramework-nightly/releases), extracted into your game's root directory.

### Source Plugins (recommended for development)

Write a single `.cs` file and place it in `reframework/plugins/source/`. REFramework compiles and loads it automatically:

```csharp
using REFrameworkNET;
using REFrameworkNET.Attributes;

public class MyPlugin {
    [PluginEntryPoint]
    public static void Main() {
        API.LogInfo("Hello from C#!");
    }
}
```

Source plugins always compile against the latest generated reference assemblies, so they have the highest compatibility with future API versions.

For IDE autocomplete, create a class library project referencing:
* `reframework/plugins/REFramework.NET.dll`
* `reframework/plugins/managed/dependencies/*.dll` (generated reference assemblies)

Then symlink or copy your `.cs` file to the `source/` folder when ready to test.

### Pre-compiled Plugins

For distribution, compile to a `.dll` targeting `x64` and place it in `reframework/plugins/managed/`. The plugin manager loads it automatically.

Copy any additional dependencies to `reframework/plugins/managed/dependencies/`.

## Plugin Lifecycle

1. REFramework loads the .NET runtime
2. Reference assemblies are generated from the game's TDB → `reframework/plugins/managed/generated/`
3. Dependencies loaded from `reframework/plugins/managed/dependencies/`
4. Source files compiled from `reframework/plugins/source/`
5. Pre-compiled assemblies loaded from `reframework/plugins/managed/`
6. `[PluginEntryPoint]` methods called on each plugin
7. On hot-reload or exit: `[PluginExitPoint]` methods called, then cycle restarts

## API Overview

| Component | Purpose |
|-----------|---------|
| [Attributes](attributes.md) | `[PluginEntryPoint]`, `[PluginExitPoint]`, `[MethodHook]`, `[Callback]` |
| [Method Hooks](hooks.md) | Intercept game methods, inspect/modify args and return values |
| [Typed Proxies](typed-proxies.md) | Generated interfaces for game types: property access, method calls, enums |
| [ManagedObject & IObject](managed-objects.md) | Low-level object access, reflection fallback, lifetime management |
| [Arrays](arrays.md) | `_System.Array`, creating/resizing managed arrays |
| [Threading](Notes-On-Threading.md) | Multi-threading in hooks, explicit threads, `LocalFrameGC()` |
| [Benchmarks](benchmarks.md) | Performance comparisons vs Lua |

## Key Types

| Type | Namespace | Purpose |
|------|-----------|---------|
| `API` | `REFrameworkNET` | Main entry point: logging, singletons, TDB access |
| `ManagedObject` | `REFrameworkNET` | Represents a GC-managed engine object |
| `NativeObject` | `REFrameworkNET` | Represents a native engine object |
| `TypeDefinition` | `REFrameworkNET` | Type metadata: methods, fields, create instances |
| `IObject` | `REFrameworkNET` | Common interface for reflection-style field/method access |
| `PreHookResult` | `REFrameworkNET` | Hook return value: `Continue` or `Skip` |

## Example

See [Walkthrough: RE9 Additional Save Slots](../examples/additional-save-slots.md) for a complete real-world plugin demonstrating hooks, typed proxies, callbacks, arrays, and more.
