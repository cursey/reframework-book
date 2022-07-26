This is the filesystem API. ~~REFramework purposefully restricts scripts from the usual Lua `io` API so that scripts do not have unrestricted access to a users system.~~ Instead, this API focuses specifically on the `reframework/data` subdirectory.

In newer builds of REFramework, the `io` API is fully supported, but it can only access the `reframework/data` directory and the stdout/in/err streams. `io.popen` is also removed.

The `io` APIs have access to the `natives` directory via the `$natives` token passed at the start of the filepath string for any of the functions.

## Methods

### `fs.glob(filter)`
Returns a table of file paths that match the `filter`. `filter` should be a regex string for the files you wish to match.

#### Example

```lua
-- Get my mods JSON files.
local json_files = fs.glob([[my-cool-mod\\.*json]])

-- Iterate over them.
for k, v in ipairs(json_files) do
    -- v will be something like `my-cool-mod\config-file-1.json` 
end
```

### `fs.read(filename)`
Reads `filename` and returns the data as a string.

### `fs.write(filename, data)`
Writes `data` to `filename`. `data` is a string.
