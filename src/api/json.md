## Methods

### `json.load_string(json_str)`
Takes a JSON string and turns it into a Lua table. Returns `nil` on error.

### `json.dump_string(value, [indent])`
Takes a Lua value (usually a table) and turns it into a JSON string. Returns an empty string on error. Optionally, it takes an `indent` parameter that specifies how the JSON string should be formatted.

### `json.load_file(filepath)`
Loads a JSON file identified by `filepath` relative to the `reframework/data` subdirectory and returns it as a Lua table. Returns `nil` if the file does not exist.

### `json.dump_file(filepath, value, [indent])`
Takes a Lua value (usually a table), and turns it into a JSON file identified as `filepath` relative to the `reframework/data` subdirectory.  Returns `true` if the dump was successful, `false` otherwise. Optionally, it takes an `indent` parameter that specifies how the JSON file should be formatted.