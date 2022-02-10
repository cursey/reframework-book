## Creation
### `Matrix4x4f.new()`

## Methods

### `self:to_quat()` 
Returns a `Quaternion` built from `self`.

### `self:inverse()`
Returns a `Matrix4x4f` that is the inverse of `self`.

### `self:invert()`
Inverts `self`. Returns nothing.

## Meta-methods

### `Matrix4x4f * Matrix4x4f`
`Matrix4x4f` multiplication.

### `Matrix4x4f * Vector4f`
`Matrix4x4f` `Vector4f` multiplication

### `Matrix4x4f[]`
`Matrix4x4f` element indexing. Valid range is `[0, 3)`.

Returns a `Vector4f`.