There are 3 `VectorXf` types:
* `Vector2f`
* `Vector3f`
* `Vector4f`

## Creation
### `Vector2f.new(x, y)`

### `Vector3f.new(x, y, z)`

### `Vector4f.new(x, y, z, w)`

## Fields

### `x: number`
The X component of the `VectorXf`

### `y: number`
The Y component of the `VectorXf`

### `z: number`
The Z component of the `VectorXf`. Only `Vector3f` and `Vector4f` have this field.

### `w: number`
The W component of the `VectorXf`. Only `Vector4f` has this field.

## Methods

### `self:dot(other)`
Returns the dot product between `self` and `other`.

### `self:cross(other)`
Returns the cross product between `self` and `other`.

### `self:length()`
Returns the length of `self`.

### `self:normalize()`
Normalizes `self`. Nothing is returned.

### `self:normalized()`
Returns the normalization of `self`.

### `self:reflect(normal)`
Returns the reflection of `self` over `normal`.

### `self:refract(normal, eta)`
Returns the refraction of `self` over `normal` with the given `eta`.

### `self:lerp(other, t)`
Returns the linear interpolation between `self` and `other` with the given `t`.

### `self:to_vec2()`
Converts `self` to a `Vector2f`. Not available if `self` is already a `Vector2f`.

### `self:to_vec3()`
Converts `self` to a `Vector3f`. Not available if `self` is already a `Vector3f`.

### `self:to_vec4()`
Converts `self` to a `Vector4f`. Not available if `self` is already a `Vector4f`.

### `self:to_mat()`
Converts `self` to a `Matrix4x4f`. Treats `self` as the forward vector.

### `self:to_quat()`
Converts `self` to a `Quaternion`. Treats `self` as the forward vector.

Equivalent to `self:to_mat():to_quat()`.

## Meta-methods

### `VectorXf + VectorXf`
`VectorXf` addition.

### `VectorXf - VectorXf`
`VectorXf` subtraction.

### `VectorXf * scalar`
`VectorXf` `scalar` multiplication.
