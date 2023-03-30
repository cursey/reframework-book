REManagedObjects are the basic building blocks of most types in the engine (unless they're native types).

They are returned from methods like:
* `sdk.call_native_func`
* `sdk.call_object_func`
* `sdk.get_managed_singleton`
* `REManagedObject:call`

Example usage:
```lua
local scene_manager = sdk.get_native_singleton("via.SceneManager")
local scene_manager_type = sdk.find_type_definition("via.SceneManager")
local scene = sdk.call_native_func(scene_manager, scene_manager_type, "get_CurrentScene")

-- Scene is an REManagedObject
if scene ~= nil then
    local current_timescale = scene:call("get_TimeScale")
    log.info("Current timescale: " .. tostring(current_timescale))

    scene:call("set_TimeScale", 5.0)
end
```

## Custom indexers
### `self.foo`
If `foo` is a field or method of the object, returns either the field or `REMethodDefinition` if it exists.

### `self:foo(bar, baz)`
If `foo` is a method of the object, calls `foo` with the supplied arguments.

If the method is an overloaded function, you must instead use `self:call(name, args...)` with the correct function prototype, as this does not deduce the correct function based on the passed arguments.

### `self.foo = bar`
If `foo` is a field of the object, assigns the value `bar` to the field.

This automatically handles the reference counting for the old and new field. Do not use `:force_release()` and `:add_ref_permanent()` in this case to handle the references.

### `self[i]`
Checks if the object has a `get_Item` method and calls it with `i`.

### `self[i] = foo`
Checks if the object has a `set_Item` method and calls it with `i` and `foo` as the respective parameters.

## Methods
### `self:call(method_name, args...)`
Return value is dependent on the method's return type. Wrapper over `sdk.call_object_func`.

Full function prototype can be passed as `method_name` if there are multiple functions with the same name but different parameters.

e.g. `self:call("foo(System.String, System.Single, System.UInt32, System.Object)", a, b, c, d)`

Valid method names can be found in the Object Explorer. Find the type you're looking for, and valid methods will be found under `TDB Methods`.
### `self:get_type_definition()`
Returns an `RETypeDefinition*`.
### `self:get_field(name)`
Return type is dependent on the field type.
### `self:set_field(name, value)`
### `self:get_address()`
### `self:get_reference_count()`

### `self:deserialize_native(data, objects)`
Experimental API to deserialize `data` into `self`.

`data` is RSZ data, in `table` format as an array of bytes.

Will only work on native `via` types.

## Dangerous Methods
Only use these if necessary!

### `self:add_ref()`
Increments the object's internal reference count.

### `self:add_ref_permanent()`
Increments the object's internal reference count without REFramework managing it. Any objects created with REFramework and also using this method will not be deleted after the Lua state is destroyed.

### `self:release()`
Decrements the object's internal reference count. Destroys the object if it reaches 0. Can only be used on objects managed by Lua.

### `self:force_release()`
Decrements the object's internal reference count. Destroys the object if it reaches 0. Can be used on any REManagedObject. Can crash the game or cause undefined behavior.

When a new Lua reference is created to an `REManagedObject`, REFramework automatically increments its reference count internally with `self:add_ref()`. This will keep the object alive until you are no longer referencing the object in Lua. `self:release()` is automatically called when Lua is no longer referencing the object anywhere.

The only time you will need to manually call `self:add_ref()` and `self:release()` is when a newly created object is returned by the engine, e.g. an array, or something from `sdk.create_instance()`.

A more in-depth explanation can be found in the "FrameGC Algorithm" section of this GDC presentation by Capcom:

https://github.com/kasicass/blog/blob/master/3d-reengine/2021_03_10_achieve_rapid_iteration_re_engine_design.md#framegc-algorithm-17

### `self:read_byte(offset)`
### `self:read_short(offset)`
### `self:read_dword(offset)`
### `self:read_qword(offset)`
### `self:read_float(offset)`
### `self:read_double(offset)`
### `self:write_byte(offset, value)`
### `self:write_short(offset, value)`
### `self:write_dword(offset, value)`
### `self:write_qword(offset, value)`
### `self:write_float(offset, value)`
### `self:write_double(offset, value)`
