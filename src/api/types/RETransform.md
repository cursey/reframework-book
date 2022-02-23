`RETransform` is the basic building block of all GameObjects, they always contain one. 

Inherits from `REComponent`.

## Methods
### `self:calculate_base_transform(joint)`
Returns a `Matrix4x4f`. Returns the reference pose (T-pose) for a specific joint relative to the transform's origin (in local transform space).

### `self:set_position(position, no_dirty)`
Sets the world position (`Vector4f`) of the transform.

When `no_dirty` is `true`, the transform and its parents will not be marked as dirty. This seems to be necessary when the scene is locked, because parent transforms will end up getting stuck.

### `self:set_rotation(rotation)`
Sets the world rotation (`Quaternion`) of the transform.

### `self:get_position()`
Gets the world position (`Vector4f`) of the transform.

### `self:get_rotation()`
Gets the world rotation (`Quaternion`) of the transform.