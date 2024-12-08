Main starting point for most things.

## Methods
### `sdk.get_tdb_version()`
Returns the version of the type database. A good approximation of the version of the RE Engine the game is running on.

### `sdk.game_namespace(name)`
Returns `game_namespace.name`.

DMC5: `name` would get converted to `app.name`

RE3: `name` would get converted to `offline.name`

### `sdk.get_thread_context()`

### `sdk.get_native_singleton(name)`
Returns a `void*`. Can be used with [sdk.call_native_func](#sdkcall_native_funcobject-type_definition-method_name-args)

Possible singletons can be found in the Native Singletons view in the Object Explorer.
### `sdk.get_managed_singleton(name)`
Returns an [REManagedObject*](types/REManagedObject.md).

Possible singletons can be found in the Singletons view in the Object Explorer.
### `sdk.find_type_definition(name)`
Returns an [RETypeDefinition*](types/RETypeDefinition.md).

### `sdk.typeof(name)`
Returns a `System.Type`. 

Equivalent to calling `sdk.find_type_definition(name):get_runtime_type()`.

Equivalent to `typeof` in C#.

### `sdk.create_instance(typename, simplify)`
Returns an [REManagedObject](types/REManagedObject.md).

Equivalent to calling `sdk.find_type_definition(typename):create_instance()`

`simplify` - defaults to `false`. Set this to `true` if this function is returning `nil`.

### `sdk.create_managed_string(str)`
Creates and returns a new `System.String` from `str`.

### `sdk.create_managed_array(type, length)`
Creates and returns a new [SystemArray](types/SystemArray.md) of the given `type`, with `length` elements.

`type` can be any of the following:

* A `System.Type` returned from [sdk.typeof](#sdktypeofname)
* An [RETypeDefinition](types/RETypeDefinition.md) returned from [sdk.find_type_definition](#sdkfind_type_definitionname)
* A Lua `string` representing the type name.

Any other type will throw a Lua error.

If `type` cannot resolve to a valid `System.Type`, a Lua error will be thrown.

### `sdk.create_sbyte(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.SByte` given the `value`.

### `sdk.create_byte(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Byte` given the `value`.

### `sdk.create_int16(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Int16` given the `value`.

### `sdk.create_uint16(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.UInt16` given the `value`.

### `sdk.create_int32(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Int32` given the `value`.

### `sdk.create_uint32(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.UInt32` given the `value`.

### `sdk.create_int64(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Int64` given the `value`.

### `sdk.create_uint64(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.UInt64` given the `value`.

### `sdk.create_single(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Single` given the `value`.

### `sdk.create_double(value)`
Returns a fully constructed [REManagedObject](types/REManagedObject.md) of type `System.Double` given the `value`.

### `sdk.create_resource(typename, resource_path)`
Returns an `REResource`.

If the typename does not correctly correspond to the resource file or is not a resource type, `nil` will be returned.

### `sdk.create_userdata(typename, userdata_path)`
Returns an [REManagedObject](types/REManagedObject.md) which is a `via.UserData`. `typename` can be `"via.UserData"` unless you know the full typename.

### `sdk.deserialize(data)`
Returns a list of [REManagedObject](types/REManagedObject.md) generated from `data`. 

`data` is the raw RSZ data contained for example in a `.scn` file, starting at the `RSZ` magic in the header.

`data` must in `table` format as an array of bytes.

Example usage:
```
local rsz_data = json.load_file("Foobar.json")
local objects = sdk.deserialize(rsz_data)

for i, v in ipairs(objects) do
    local obj_type = v:get_type_definition()
    log.info(obj_type:get_full_name())
end
```

### `sdk.call_native_func(object, type_definition, method_name, args...)`
Return value is dependent on what the method returns.

Full function prototype can be passed as `method_name` if there are multiple functions with the same name but different parameters.

Should only be used with native types, not [REManagedObject](types/REManagedObject.md) (though, it can be if wanted).

Example:
```lua
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
Returns a [REManagedObject*](types/REManagedObject.md). Returns the current camera being used by the engine.

### `sdk.hook(method_definition, pre_function, post_function, ignore_jmp)`
Creates a hook for [method_definition](types/REMethodDefinition.md), intercepting all incoming calls the game makes to it.

`ignore_jmp` - Skips trying to follow the first jmp in the function. Defaults to `false`.

Using `pre_function` and `post_function`, the behavior of these functions can be modified.

NOTE: Some native methods may not be able to be hooked with this, e.g. if they are just a  wrapper over the native function. Some additional work will need to be done from our end to make those work.

pre_function and post_function looks like so:
```lua
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

    -- if the argument is a ValueType, you need to do this to access its fields:
    -- local type = sdk.find_type_definition("via.Position")
    -- local x = sdk.get_native_field(arg[3], type, "x")

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
```lua
local function on_pre_get_timescale(args)
end

local function on_post_get_timescale(retval)
    -- Make the game run 5 times as fast instead
    -- TODO: Make it so casting return values like this is not necessary
    return sdk.float_to_ptr(5.0)
end

sdk.hook(sdk.find_type_definition("via.Scene"):get_method("get_TimeScale"), on_pre_get_timescale, on_post_get_timescale)
```

### `sdk.hook_vtable(obj, method, pre, post)`
Similar to `sdk.hook` but hooks on a **per-object** basis instead, instead of hooking the function globally for all objects.

Only works if the target method is a **virtual method**.

### `sdk.is_managed_object(value)`
Returns true if `value` is a valid [REManagedObject](types/REManagedObject.md).

Use only if necessary. Does a bunch of checks and calls [IsBadReadPtr](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-isbadreadptr) a lot.
### `sdk.to_managed_object(value)`
Attempts to convert `value` to an [REManagedObject*](types/REManagedObject.md).

`value` can be any of the following types:

* An [REManagedObject*](types/REManagedObject.md), in which case it is returned as-is
* A lua number convertible to `uintptr_t`, representing the object's address
* A `void*`

Any other type will return `nil`.

A `value` that is not a valid [REManagedObject*](types/REManagedObject.md) will return `nil`, equivalent to calling [sdk.is_managed_object](#sdkis_managed_objectvalue) on it.

### `sdk.to_double(value)`
Attempts to convert `value` to a `double`.

`value` can be any of the following types:

* A `void*`

### `sdk.to_float(value)`
Attempts to convert `value` to a `float`.

`value` can be any of the following types:
* A `void*`

### `sdk.to_int64(value)`
Attempts to convert `value` to a `int64`.

`value` can be any of the following types:
* A `void*`

If you need a smaller datatype, you can do:
* `(sdk.to_int64(value) & 1) == 1` for a boolean
* `(sdk.to_int64(value) & 0xFF)` for an unsigned byte
* `(sdk.to_int64(value) & 0xFFFF)` for an unsigned short (2 bytes)
* `(sdk.to_int64(value) & 0xFFFFFFFF)` for an unsigned int (4 bytes)

### `sdk.to_ptr(value)`
Attempts to convert `value` to a `void*`.

`value` can be any of the following types:

* An [REManagedObject*](types/REManagedObject.md)
* A lua number convertible to `int64_t`
* A lua number convertible to `double`
* A lua boolean
* A `void*`, in which case it is returned as-is

Any other type will return `nil`.

### `sdk.to_valuetype(obj, t)`
Attempts to convert `obj` to `t`

`obj` can be a:

* Number
* void*

`t` can be a:

* [RETypeDefinition](types/RETypeDefinition.md)
* string

### `sdk.float_to_ptr(number)`
Converts `number` to a `void*`.

## Enums
### `sdk.PreHookResult`
* `sdk.PreHookResult.CALL_ORIGINAL`
* `sdk.PreHookResult.SKIP_ORIGINAL`
