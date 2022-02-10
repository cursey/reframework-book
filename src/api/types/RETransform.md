`RETransform` is the basic building block of all GameObjects, they always contain one. 

Inherits from `REComponent`.

## Methods
### `self:calculate_base_transform(joint)`
Returns a `Matrix4x4f`. Returns the reference pose (T-pose) for a specific joint relative to the transform's origin (in local transform space).