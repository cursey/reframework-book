# thread

The `thread` API is for storing thread-specific data and querying information about the current thread.

Added in `8e9375ce5433c5b4ce38e8398c168c3ab036415c`.

## `thread.get_id()`

Returns the ID of the current thread.

## `thread.get_hash()`

Returns the hash of the ID of the current thread.

## `thread.get_hook_storage()`

Returns the ephemeral hook storage meant to be used within `sdk.hook`.

This is preferred over storing variables you need in a global variable in the `pre` hook when you need the data in the `post` hook.

The hook storage is popped/destroyed at the end of the `post` hook. Safe to be used within a recursive context.

This API is preferred because there are no longer any guarantees that the entire hook will be locked during pre/post hooks, due to deadlocking issues seen.

### Example

```lua
local pawn_t = sdk.find_type_definition("app.Pawn")

sdk.hook(
    pawn_t:get_method("updateMove"),
    function(args)
        local storage = thread.get_hook_storage()
        storage["this"] = sdk.to_managed_object(args[2])
    end,
    function(retval)
        local this = thread.get_hook_storage()["this"]
        print("this: " .. tostring(this:get_type_definition():get_full_name()))
        return retval
    end
)
```