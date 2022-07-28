Type descriptor for objects in the RE Engine. 

Returned from things like `REManagedObject:get_type_definition()` or `sdk.find_type_definition(name)`

## Methods
### `self:get_full_name()`
Returns the full name of the class.

Equivalent to concatenating `self:get_namespace()` and `self:get_name()`.

### `self:get_name()`
Returns the type name. Does not contain namespace.

### `self:get_namespace()`
Returns the namespace this type is contained in.

### `self:get_method(name)`
Returns an `REMethodDefinition`. To be used in things like `sdk.hook`.

The full function prototype can be supplied to get an overloaded function.

Example: `foo:get_method("Bar(System.Int32, System.Single)")`

### `self:get_methods()`
Returns a list of `REMethodDefinition`

Filters out methods that are potentially just stubs or null.

### `self:get_field(name)`
Returns an `REField`.

### `self:get_fields()`
Returns a list of `REField`

### `self:get_parent_type()`
Returns the `RETypeDefinition` this type inherits from.

### `self:get_runtime_type()`
Returns a `System.Type`. Useful for methods that require this. Equivalent to `typeof` in C#.

### `self:get_size()`
Returns the full size of the object. e.g. 0x14 for `System.Int32`.

### `self:get_valuetype_size()`
Returns the value type size. e.g. 4 for `System.Int32`. 

### `self:get_generic_argument_types()`

### `self:get_generic_type_definition()`

### `self:is_a(typename or RETypeDefinition)`
Returns whether `self` or its parents are a `typename` or the `RETypeDefinition` passed.

### `self:is_value_type()`
Returns whether the type is a [ValueType](https://docs.microsoft.com/en-us/dotnet/api/system.valuetype?view=net-5.0).

Does not necessarily need to inherit from `System.ValueType` for this to be true. An example would be `via.vec3`.

### `self:is_by_ref()`

### `self:is_pointer()`

### `self:is_primitive()`

### `self:is_generic_type()`

### `self:is_generic_type_definition()`

### `self:create_instance()`
Returns an `REManagedObject`.
