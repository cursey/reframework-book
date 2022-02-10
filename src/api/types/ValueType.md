Container for unknown ValueTypes.

## Methods
### `ValueType.new(typename)`

### `self:call(name, args...)`
### `self:get_field(name)`
### `self:set_field(name, value)`
Note that this does not change anything in-game. `ValueType` is just a local copy.

You'll need to pass the `ValueType` somewhere that would make use of the changed data.

### `self:address()`
### `self:get_type_definition()`

### `self.type`
### `self.data`
`std::vector<uint8_t>`

## Dangerous Methods
Only use these if necessary!
### `self:read_byte(offset)`
### `self:read_short(offset)`
### `self:read_dword(offset)`
### `self:read_qword(offset)`
### `self:read_float(offset)`
### `self:read_double(offset)`
### `self:write_byte(offset, value)`
### `self:write_short(offset, value)`
### `self:write_dword(offset, value)`
### `self:write_qword(offset, value)`
### `self:write_float(offset, value)`
### `self:write_double(offset, value)`