Method descriptor.

## Methods
### `self:get_name()`

### `self:get_return_type()`
Returns an `RETypeDefinition*`.

### `self:get_function()`
Returns a `void*`. Pointer to the actual function in memory.

### `self:get_declaring_type()`
Returns an `RETypeDefinition*` corresponding to the class/type that declared this method.

### `self:get_num_params()`
Returns the number of parameters required to call the function.

### `self:get_param_types()`
Returns a list of `RETypeDefinition`

### `self:get_param_names()`
Returns a list of strings for the parameter names

### `self:is_static()`
Returns whether this method is static or not.

### `self:call(obj, args...)`
Equivalent to calling `obj:call(args...)`

Can also use `self(obj, args...)`
