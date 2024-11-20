## `sdk.hook` method arguments
`ByRef` parameters are not correctly supported by REFramework. `ByRef` parameters are essentially `T**` instead of `T*` type pointers. They are usually used for out parameters.

These will need to be manually dereferenced using a trick by instantiating a `System.UInt64` and reading the `mValue` field to dereference it.

```lua
local function deref_ptr(ptr)
    local fake_int64 = sdk.to_valuetype(ptr, "System.UInt64")
    local deref = fake_int64:get_field("mValue")

    return deref
end

sdk.hook(sdk.find_type_definition("foo"):get_method("bar"),
    function(args)
        local deref = deref_ptr(args[6])
        local arg = sdk.to_managed_object(deref):add_ref()
    end,
    function(retval)
        return retval
    end
)
```

For `out` ref parameter, this can only be done inside the post hook.

```lua
sdk.hook(sdk.find_type_definition("foo"):get_method("bar"),
    function(args)
        local storage = thread.get_hook_storage()
        storage["ref_arg"] = args[3]
    end,
    function(retval)
        local ref_arg = thread.get_hook_storage()["ref_arg"]
        local deref = deref_ptr(ref_arg)
        local arg = sdk.to_managed_object(deref):add_ref()

        return retval
    end
)
```
