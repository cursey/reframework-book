This page refers to functions like:
* `sdk.call_native_func`
* `sdk.call_object_func`
* `sdk.get_native_field`
* `REManagedObject:call`
* `REManagedObject:get_field`

These functions have auto conversions for some types:
* `System.String`
    * Gets converted to a normal lua string
* `System.Int`, `System.UInt`, `System.Boolean`, `System.Single` types
    * Gets converted to native lua equivalents
* `via.vec2`, `via.vec3`, `via.vec4`
    * Gets converted to Vector2f, Vector3f, Vector4f
* `via.mat4`
    * Gets converted to Matrix4x4f
