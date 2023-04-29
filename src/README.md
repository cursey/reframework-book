This is the REFramework wiki. It will mostly serve as documentation for the scripting and plugin system.

[VR Troubleshooting](troubleshooting/VR-Troubleshooting.md)

[Contributing to documentation](https://github.com/cursey/reframework-book)

[Nightly builds](https://github.com/praydog/REFramework-nightly/releases)

## Reporting a bug
Report it on the [Issues](https://github.com/praydog/REFramework/issues) page.

If you are crashing, or are having a technical problem then upload these files from your game folder:
* `re2_framework_log.txt` - The WHOLE LOG, not snippets of it.
* `reframework_crash.dmp` if you are crashing

## Help! My pirated copy does not work

Contrary to some belief, **this mod does not contain any anti-piracy checks of any kind**. Pirated copies just do not receive support. If it works then, it works. If not, additional support is not going to be added.

## Lua Scripting

REFramework comes with a scripting system using Lua. 

Leveraging the RE Engine's IL2CPP implementation, REFramework gives developers powerful control over the game engine.

If you are interested in native plugins: [read the plugin section](#plugins)

## Loading a script

### Manual Loading
Click on `ScriptRunner` from the main REFramework menu. From there, press `Run Script` and locate the corresponding `*.lua` file you wish to load.

### Automatic Loading
Create an `reframework/autorun` folder in your game directory. This is automatically created when REFramework loads. REFramework will automatically load whatever `*.lua` scripts are in here during initialization.

## Handling Lua errors

### During script startup
When a Lua error occurs here, a MessageBox will pop up explaining what the error is.

### During callback execution
When a Lua error occurs here, the reason will be written to a debug log. ~~[DebugView](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview) is required to view these.~~ In newer nightly builds, the errors can be viewed directly within the ScriptRunner window.

We don't pop a MessageBox here so the user doesn't lock their game.

## Finding game functions to call, and fields to grab
Use the `ObjectExplorer`. It can be found under `DeveloperTools` in the REFramework menu.

Poke around the singletons until you find something you're interested in. 

Objects under `Singletons` can be obtained with `sdk.get_managed_singleton("name")`

Objects under `Native Singletons` can be obtained with `sdk.get_native_singleton("name")`

Do note that the `Singletons` (AKA Managed Singletons) are the usually the most exposed. They were originally written in C#.

`Native Singletons` have fields and methods exposed, but they are usually hand picked. These ones were written in C++, and have the least amount of data exposed about them.

Anything under `TDB Methods` or `TDB Fields` of something within the `ObjectExplorer` can be called or grabbed using the various call and field getter/setter methods found here in the wiki. 

You **CANNOT** use the `Reflection Methods` or `Reflection Properties` yet without direct memory reading/writing, only the TDB versions are fully supported.

Good APIs to start on: [sdk](https://github.com/praydog/REFramework/wiki/sdk) and [re](https://github.com/praydog/REFramework/wiki/re)

[Example Scripts](examples/Example-Scripts.md)

[Further Object Explorer Documentation](object_explorer/object_explorer.md)

---

## Plugins
REFramework has the ability to run native DLL plugins. This can also just be used as a loose DLL loader, with no awareness of REF.

The plugins can perform much of what Lua can, with much more freedom. They have access to much of the important SDK functionality of REFramework, as well as useful callbacks for rendering/input/game code.

### Loading a plugin
Drop the `.dll` file into the `reframework/plugins` directory.

### Using the plugin API
Include the `include` directory from the root REFramework project directory in your plugin. Include `API.hpp` if you are using C++ and want a more C++ approach to using the SDK.

From there, you have the option to export these functions:

```cpp
// OPTIONAL
// Enforces plugin versioning
// If REF's major version does not match the plugin's required version, the plugin will not load
// If REF's minor version is less than the plugin's required version, the plugin will not load
// If REF's patch version does not match, the plugin will load but a warning will be displayed in the plugin menu
extern "C" __declspec(dllexport) void reframework_plugin_required_version(REFrameworkPluginVersion* version) {
    version->major = REFRAMEWORK_PLUGIN_VERSION_MAJOR;
    version->minor = REFRAMEWORK_PLUGIN_VERSION_MINOR;
    version->patch = REFRAMEWORK_PLUGIN_VERSION_PATCH;

    // Optionally, specify a specific game name that this plugin is compatible with.
    //version->game_name = "MHRISE";
}
```

```cpp
using namespace reframework; // For API class

// OPTIONAL
// Used for initializing the REFramework SDK and additional functions
extern "C" __declspec(dllexport) bool reframework_plugin_initialize(const REFrameworkPluginInitializeParam* param) {
    API::initialize(param);

    // Example usage of param functions
    const auto functions = param->functions;
    functions->on_lua_state_created(on_lua_state_created);
    functions->on_lua_state_destroyed(on_lua_state_destroyed);
    functions->on_frame(on_frame);
    functions->on_pre_application_entry("BeginRendering", on_pre_begin_rendering); // Look at via.ModuleEntry or the wiki for valid names here
    functions->on_post_application_entry("EndRendering", on_post_end_rendering);
    functions->on_device_reset(on_device_reset);
    functions->on_message((REFOnMessageCb)on_message);
    functions->log_error("%s %s", "Hello", "error");
    functions->log_warn("%s %s", "Hello", "warning");
    functions->log_info("%s %s", "Hello", "info");
    API::get()->log_error("%s %s", "Hello", "error");
    API::get()->log_warn("%s %s", "Hello", "warning");
    API::get()->log_info("%s %s", "Hello", "info");

    return true;
}
```

Optionally, you can specify a DllMain if for example your plugin absolutely needs to load immediately, or do not want the additional functionality of REFramework's plugin API.

### Example of using native SDK functionality
```cpp
// Grabbing the game window size with a C++ call and invoke
auto& api = API::get();
const auto tdb = api->tdb();

auto vm_context = api->get_vm_context();

const auto scene_manager = api->get_native_singleton("via.SceneManager");
const auto scene_manager_type = tdb->find_type("via.SceneManager");

const auto scene_manager_full_name = scene_manager_type->get_full_name();

OutputDebugString((std::stringstream{} << scene_manager_full_name << " Size: " << scene_manager_full_name.size()).str().c_str());

const auto get_main_view = scene_manager_type->find_method("get_MainView");
const auto main_view = get_main_view->call<API::ManagedObject*>(vm_context, scene_manager);

if (main_view == nullptr) {
    return;
}

// Method 1: Call
float size[3]{};
main_view->call("get_Size", &size, vm_context, main_view);

// Method 2: Invoke
auto get_size_invoke_result = main_view->invoke("get_Size", {});
float* size_invoke = (float*)&get_size_invoke_result;
```

### Example plugins
[REFramework Example Plugin](https://github.com/praydog/REFramework/tree/master/examples)

[REFramework Direct2D Plugin](https://github.com/cursey/reframework-d2d)

### Plugin headers
[REFramework Plugin API Headers](https://github.com/praydog/REFramework/tree/master/include/reframework)

## Side notes
Everything is subject to change and maybe refactored over time.

Lua uses a shared state across all scripts. Use `local` variables so as to not cause conflicts with other scripts.

If there's something you find you can't do without native code, Lua can `require` native DLLs. Native plugins are also an option.

RE Engine's IL2CPP implementation is not the same as Unity's. While RE Engine and Unity have many similarities, they are not the same, and no existing tooling for Unity or IL2CPP will work on the RE Engine.

C# scripting maybe a possibility in the future for more natural interaction with the engine, but is not currently being looked at. REFramework is open source, so any developer wishing to do that can try.

While REFramework's scripting API can do all sorts of things, [RE_RSZ](https://github.com/alphazolam/RE_RSZ) is another powerful tool that may be more suitable in some scenarios. 
For example:
* Inserting/cloning more game objects into a specific scene
* Edits that don't require runtime awareness of the game's state
* Time-sensitive edits to files (like something REFramework can't capture during startup)
* Using it for base edits with an REFramework script on top for additional functionality
* Changes that are impossible with REFramework's scripting system

## Thanks
[cursey](https://github.com/cursey/) for helping build the scripting system.

[The Hitchhiker](https://github.com/youwereeatenbyalid/) for testing/writing scripts/finding bugs/helpful suggestions.

[alphaZomega](https://github.com/alphazolam) for testing/writing scripts/finding bugs/helpful suggestions.

## Discords
[Modding Haven](https://discord.gg/9Vr2SJ3) (General RE Engine modding)

[Infernal Warks](https://discord.com/invite/nX5EzVU) (DMC5 modding)

[Monster Hunter Modding Discord](https://discord.gg/gJwMdhK)

[Flatscreen to VR Modding Discord](http://flat2vr.com)
