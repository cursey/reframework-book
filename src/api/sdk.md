Main starting point for most things.

## Methods
### `sdk.game_namespace(name)`
Returns `game_namespace.name`.

DMC5: `name` would get converted to `app.name`

RE3: `name` would get converted to `offline.name`

### `sdk.get_thread_context()`

### `sdk.get_native_singleton(name)`
Returns a `void*`. Can be used with `sdk.call_native_func`

Possible singletons can be found in the Native Singletons view in the Object Explorer.
### `sdk.get_managed_singleton(name)`
Returns an `REManagedObject*`.

Possible singletons can be found in the Singletons view in the Object Explorer.
### `sdk.find_type_definition(name)`
Returns an `RETypeDefinition*`.

### `sdk.typeof(name)`
Returns a `System.Type`. 

Equivalent to calling `sdk.find_type_definition(name):get_runtime_type()`.

Equivalent to `typeof` in C#.

### `sdk.create_instance(typename, simplify)`
Returns an `REManagedObject`. Equivalent to calling `sdk.find_type_definition(typename):create_instance()`

`simplify` - defaults to `false`. Set this to `true` if this function is returning `nil`.

### `sdk.create_resource(typename, resource_path)`
Returns an `REResource`.

### `sdk.call_native_func(object, type_definition, method_name, args...)`
Return value is dependent on what the method returns.

Full function prototype can be passed as `method_name` if there are multiple functions with the same name but different parameters.

Should only be used with native types, not `REManagedObject` (though, it can be if wanted).

Example:
```
local scene_manager = sdk.get_native_singleton("via.SceneManager")
local scene_manager_type = sdk.find_type_definition("via.SceneManager")
local scene = sdk.call_native_func(scene_manager, scene_manager_type, "get_CurrentScene")

if scene ~= nil then
    -- We can use call like this because scene is a managed object, not a native one.
    scene:call("set_TimeScale", 5.0)
end
```
### `sdk.call_object_func(managed_object, method_name, args...)`
Return value is dependent on what the method returns.

Full function prototype can be passed as `method_name` if there are multiple functions with the same name but different parameters.

Alternative calling method:
`managed_object:call(method_name, args...)`

### `sdk.get_native_field(object, type_definition, field_name)`
### `sdk.set_native_field(object, type_definition, field_name, value)`

### `sdk.get_primary_camera()`
Returns a `REManagedObject*`. Returns the current camera being used by the engine.

### `sdk.hook(method_definition, pre_function, post_function, ignore_jmp)`
Creates a hook for `method_definition`, intercepting all incoming calls the game makes to it.

`ignore_jmp` - Skips trying to follow the first jmp in the function. Defaults to `false`.

Using `pre_function` and `post_function`, the behavior of these functions can be modified.

NOTE: Some native methods may not be able to be hooked with this, e.g. if they are just a  wrapper over the native function. Some additional work will need to be done from our end to make those work.

pre_function and post_function looks like so:
```
local function pre_function(args)
    -- args are modifiable
    -- args[1] = thread_context
    -- args[2] = "this"/object pointer
    -- rest of args are the actual parameters
    -- actual parameters start at args[2] in a static function
    -- Some native functions will have the object start at args[1] and rest at args[2]
    -- All args are void* and not auto-converted to their respective types.
    -- You will need to do things like sdk.to_managed_object(args[2])
    -- or sdk.to_int64(args[3]) to get arguments to better interact with or read.
    -- Hooks cannot grab stack arguments yet (past r9), so 4 arguments max are supported.

    -- OPTIONAL: Specify an sdk.PreHookResult
    -- e.g.
    -- return sdk.PreHookResult.SKIP_ORIGINAL -- prevents the original function from being called
    -- return sdk.PreHookResult.CALL_ORIGINAL -- calls the original function, same as not returning anything
end

local function post_function(retval)
    -- return something else if you don't want the original return value
    -- NOTE: the post_function will still be called if SKIP_ORIGINAL is returned from the pre_function
    -- So, if your function expects something valid in return, keep that in mind, as retval will not be valid.
    -- Make sure to convert custom retvals to sdk.to_ptr(retval)
    return retval
end
```

Example hook:
```
local function on_pre_get_timescale(args)
end

local function on_post_get_timescale(retval)
    -- Make the game run 5 times as fast instead
    -- TODO: Make it so casting return values like this is not necessary
    return sdk.float_to_ptr(5.0)
end

sdk.hook(sdk.find_type_definition("via.Scene"):get_method("get_TimeScale"), on_pre_get_timescale, on_post_get_timescale)
```

### `sdk.is_managed_object(value)`
Returns true if `value` is a valid `REManagedObject`.

Use only if necessary. Does a bunch of checks and calls [IsBadReadPtr](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-isbadreadptr) a lot.
### `sdk.to_managed_object(value)`
### `sdk.to_double(value)`
### `sdk.to_float(value)`
### `sdk.to_int64(value)`
### `sdk.to_ptr(value)`
### `sdk.float_to_ptr(number)`


## Enums
### `sdk.PreHookResult`
* `sdk.PreHookResult.CALL_ORIGINAL`
* `sdk.PreHookResult.SKIP_ORIGINAL`
