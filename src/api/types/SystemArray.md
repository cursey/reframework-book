Easy-to-use wrapper over `System.Array`. Functions calls that return arrays or objects will automatically get converted to `SystemArray` types if eligible.

Inherits from `REManagedObject`.

## Notes
Do not use `ipairs` on `SystemArray` types. Use `pairs` instead, unless you return the elements in a lua array via `get_elements()`. Using `ipairs` will skip the first element and go past the end of the array.

## Methods
### `self:get_elements()`
Returns the array's elements as a lua table. 

Keep in mind these objects will all be full `REManagedObject` types, not the ValueTypes they represent, if any, like `System.Int32`
### `self:get_element(index)`
Returns the object at `index` in the array.
### `self:get_size()`
Returns the size of the array.

## Meta-methods
### `SystemArray[]`
Wrapper for `self:get_element(index)`
