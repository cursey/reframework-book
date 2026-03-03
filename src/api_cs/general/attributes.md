# Attributes

REFramework.NET uses attributes from `REFrameworkNET.Attributes` and `REFrameworkNET.Callbacks` to declaratively wire your plugin into the engine. This page covers all four.

## `[PluginEntryPoint]`

Marks the plugin entry point. The decorated method **must** be `public static void` with no parameters. It is called exactly once when the plugin loads.

**Namespace:** `REFrameworkNET.Attributes`

```csharp
using REFrameworkNET;
using REFrameworkNET.Attributes;

public class MyPlugin
{
    [PluginEntryPoint]
    public static void Main()
    {
        API.LogInfo("MyPlugin loaded");
    }
}
```

Only one method per assembly should carry this attribute.

## `[PluginExitPoint]`

Marks a cleanup method called when the plugin unloads — either during a hot-reload cycle or when the game exits. Use it to:

- Null out static references to game objects
- Cancel background threads or timers
- Reset any global state your plugin modified

**Namespace:** `REFrameworkNET.Attributes`

**Signature:** `public static void`, no parameters.

```csharp
[PluginExitPoint]
public static void OnUnload()
{
    _cachedManager = null;
    _cts?.Cancel();
    API.LogInfo("MyPlugin unloaded");
}
```

If you skip this and your plugin is hot-reloaded, stale references to old managed objects will cause crashes.

## `[MethodHook]`

Hooks a game method so your code runs before (pre) or after (post) the original.

**Namespace:** `REFrameworkNET.Attributes`

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `Type` | The type containing the method, e.g. `typeof(app.SomeType)` |
| `methodName` | `string` | Method name. Use `nameof(app.SomeType.someMethod)` with typed proxies. |
| `hookType` | `MethodHookType` | `MethodHookType.Pre` or `MethodHookType.Post` |
| `skipJmp` | `bool` *(optional)* | When `true`, the hook skips the initial `jmp` instruction at the function entry point. Set this to `true` when hooking functions that have been patched with a trampoline by another mod or by the game itself. Defaults to `false`. |

### Pre-hook

**Signature:** `static PreHookResult Method(Span<ulong> args)`

The `args` span contains raw pointers:

| Index | Value |
|-------|-------|
| `args[0]` | Thread context (internal, rarely needed) |
| `args[1]` | `this` pointer of the instance the method was called on |
| `args[2+]` | Method parameters in declaration order |

Return `PreHookResult.Continue` to let the original method execute, or `PreHookResult.Skip` to suppress it entirely (the post-hook still fires).

```csharp
[MethodHook(typeof(app.SaveServiceManager), nameof(app.SaveServiceManager.reloadSaveSlotInfo), MethodHookType.Pre)]
static PreHookResult OnPreReload(Span<ulong> args)
{
    var self = ManagedObject.ToManagedObject(args[1])?.As<app.SaveServiceManager>();
    if (self == null)
        return PreHookResult.Continue;

    API.LogInfo($"reloadSaveSlotInfo called, max slots = {self._MaxUseSaveSlotCount}");
    return PreHookResult.Continue;
}
```

For **static methods**, there is no `this` pointer — parameters start at `args[1]` instead of `args[2]`:

```csharp
[MethodHook(typeof(app.WeaponDef), nameof(app.WeaponDef.Attack), MethodHookType.Pre)]
static PreHookResult OnPreAttack(Span<ulong> args)
{
    // Static method: args[0] = thread context, args[1] = first param, args[2] = second param
    int wpType = (int)args[1];
    int wpId = (int)args[2];
    return PreHookResult.Continue;
}
```

The optional `skipJmp` parameter is unrelated to static methods — it controls hook installation behavior:

```csharp
// Hook a function that has a jmp trampoline at its entry point
[MethodHook(typeof(app.SomeType), nameof(app.SomeType.patchedMethod), MethodHookType.Pre, true)]
static PreHookResult OnPre(Span<ulong> args) => PreHookResult.Continue;
```

### Post-hook

**Signature:** `static void Method(ref ulong retval)`

`retval` holds the return value as a raw address (for reference types) or a value (for value types). You can read it, or replace it to change what the caller receives.

```csharp
[MethodHook(typeof(app.SaveServiceManager), nameof(app.SaveServiceManager.getMaxSaveSlotNum), MethodHookType.Post)]
static void OnPostGetMax(ref ulong retval)
{
    // Override the return value to increase max save slots
    retval = 117;
}
```

To replace a reference-type return value:

```csharp
[MethodHook(typeof(app.SomeType), nameof(app.SomeType.getName), MethodHookType.Post)]
static void OnPostGetName(ref ulong retval)
{
    var original = ManagedObject.ToManagedObject(retval);
    // ... build replacement ...
    retval = replacement.GetAddress();
}
```

## `[Callback]`

Registers a method to run on an engine callback — most commonly the per-frame update tick.

**Namespace:** `REFrameworkNET.Callbacks`

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `Type` | Callback source type, e.g. `typeof(UpdateBehavior)` |
| `callbackType` | `CallbackType` | `CallbackType.Pre` or `CallbackType.Post` |

**Signature:** `public static void Method()` — no parameters.

```csharp
using REFrameworkNET.Callbacks;

[Callback(typeof(UpdateBehavior), CallbackType.Pre)]
public static void OnUpdate()
{
    // Runs every frame before the engine update
}
```

`CallbackType.Pre` fires before the engine processes the callback; `CallbackType.Post` fires after.

### Common callback types

All callback classes live in `REFrameworkNET.Callbacks`. There are hundreds corresponding to engine lifecycle stages. The most commonly used:

| Callback | When it fires |
|----------|--------------|
| `UpdateBehavior` | Per-frame game logic update (most common) |
| `LateUpdateBehavior` | After per-frame update |
| `UpdateMotion` | Animation/motion update |
| `UpdateGUI` | GUI update |
| `PreupdateGUI` | Before GUI update |
| `UpdatePhysics` | Physics tick |
| `BeginRendering` | Start of rendering frame |
| `EndRendering` | End of rendering frame |
| `ImGuiRender` | ImGui overlay rendering |
| `ImGuiDrawUI` | ImGui UI rendering |
| `Initialize` | Engine initialization (runs once) |
| `Setup` | Post-initialization setup (runs once) |
| `Start` | After setup completes (runs once) |

For a complete list, see the `GENERATE_POCKET_CLASS` macros in `Callbacks.hpp` in the REFramework source.
## Complete Example

A minimal plugin using all four attributes:

```csharp
using REFrameworkNET;
using REFrameworkNET.Attributes;
using REFrameworkNET.Callbacks;

public class ExamplePlugin
{
    private static app.SaveServiceManager _saveMgr;

    [PluginEntryPoint]
    public static void Main()
    {
        API.LogInfo("ExamplePlugin loaded");
    }

    [PluginExitPoint]
    public static void OnUnload()
    {
        _saveMgr = null;
        API.LogInfo("ExamplePlugin unloaded");
    }

    [Callback(typeof(UpdateBehavior), CallbackType.Pre)]
    public static void OnUpdate()
    {
        if (_saveMgr == null)
            _saveMgr = API.GetManagedSingletonT<app.SaveServiceManager>();
    }

    [MethodHook(typeof(app.SaveServiceManager),
                nameof(app.SaveServiceManager.getMaxSaveSlotNum),
                MethodHookType.Pre)]
    static PreHookResult OnPreGetMax(Span<ulong> args)
    {
        API.LogInfo("getMaxSaveSlotNum called");
        return PreHookResult.Continue;
    }

    [MethodHook(typeof(app.SaveServiceManager),
                nameof(app.SaveServiceManager.getMaxSaveSlotNum),
                MethodHookType.Post)]
    static void OnPostGetMax(ref ulong retval)
    {
        retval = 117;
    }
}
```
