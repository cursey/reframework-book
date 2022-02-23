## Constructors
### `Matrix4x4f.new()`

### `Matrix4x4f.new(x1, y1, z1, w1, x2, y2, z2, w2 x3, y3, z3, w3, x4, y4, z4, w4)`

### Static methods
### `Matrix4x4f.identity()`
Returns the identity matrix.

## Methods

### `self:to_quat()` 
Returns a `Quaternion` built from `self`.

### `self:inverse()`
Returns a `Matrix4x4f` that is the inverse of `self`.

### `self:invert()`
Inverts `self`. Returns nothing.

### `self:interpolate(other, t)`
Returns the linear interpolation between `self` and `other` with the given `t`.

### `self:matrix_rotation()`
Extracts the rotation matrix from `self`.

## Meta-methods

### `Matrix4x4f * Matrix4x4f`
`Matrix4x4f` multiplication.

### `Matrix4x4f * Vector4f`
`Matrix4x4f` `Vector4f` multiplication

### `Matrix4x4f[]`
`Matrix4x4f` element indexing. Valid range is `[0, 3)`.

Returns a `Vector4f`.