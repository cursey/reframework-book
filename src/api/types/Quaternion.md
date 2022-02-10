## Constructor
### `Quaternion.new(w, x, y, z)`

## Fields
### `x: number`
The X component of the `Quaternion`.

### `y: number`
The Y component of the `Quaternion`.

### `z: number`
The Z component of the `Quaternion`.

### `w: number`
The W component of the `Quaternion`.

## Methods

### `self:to_mat4()`
Returns a `Matrix4x4f` built from `self`.

### `self:inverse()`
Returns a `Quaternion` that is the inverse of `self`.

### `self:invert()`
Inverts `self`. Returns nothing.

### `self:normalize()`
Normalizes `self`. Returns nothing.

### `self:normalized()`
Returns a `Quaternion` that is the normalization of `self`.

## Meta-methods

### `Quaternion * Quaternion`
`Quaternion` multiplication.

### `Quaternion * Vector3f`
`Quaternion` `Vector3f` multiplication.

### `Quaternion * Vector4f`
`Quaternion` `Vector4f` multiplication.

### `Quaternion[]`
`Quaternion` element indexing. Valid range is `[0, 4)`.