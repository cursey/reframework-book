## Methods
### `self:add_ref()`
Adds a reference to `self`. `REResource` types are not automatically reference counted like `REManagedObject`.

### `self:release()`
Releases a reference to `self`. `REResource` types are not automatically reference counted like `REManagedObject`.

### `self:get_address()`
Returns the address of `self`.

### `self:create_holder(typename)`
Returns a `via.ResourceHolder` variant which holds `self`. Automatically adds a reference to `self`.

```lua
local res = sdk.create_resource("via.motion.MotionFsm2Resource", "_Chainsaw/AppSystem/Character/ch0Common/Motion/Fsm/ch0Common.motfsm2"):add_ref()
local holder = res:create_holder("via.motion.MotionFsm2ResourceHolder"):add_ref()
```
