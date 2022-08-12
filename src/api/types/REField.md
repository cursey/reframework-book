## Methods
### `self:get_name()`
### `self:get_type()`
Returns an `RETypeDefinition*`.
### `self:get_offset_from_base()`
### `self:get_offset_from_fieldptr()`
### `self:get_declaring_type()`
### `self:get_flags()`
### `self:is_static()`
### `self:is_literal()`
### `self:get_data(obj)`
Returns the data contained in the field for `obj`. 

`obj` can be any of the following type:
  - `nil`, if the field is static
  - `REManagedObject*`
  - `void*` pointing to a `REManagedObject` or `ValueType`
