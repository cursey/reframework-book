## RE Engine
### Grabbing components from a game object
```lua
-- Find a component contained in a game object by its type name
local function get_component(game_object, type_name)
    local t = sdk.typeof(type_name)

    if t == nil then 
        return nil
    end

    return game_object:call("getComponent(System.Type)", t)
end

-- Get all components of a game object as a table
local function get_components(game_object)
    local transform = game_object:call("get_Transform")

    if not transform then
        return {}
    end

    return game_object:call("get_Components"):get_elements()
end
```

### Getting the current elapsed time in seconds
In newer builds, `os.clock` is available.

```lua
local app_type = sdk.find_type_definition("via.Application")
local get_elapsed_second = app_type:get_method("get_UpTimeSecond")

local function get_time()
    return get_elapsed_second:call(nil)
end
```

### Generating enums/static fields
```lua
local function generate_enum(typename)
    local t = sdk.find_type_definition(typename)
    if not t then return {} end

    local fields = t:get_fields()
    local enum = {}

    for i, field in ipairs(fields) do
        if field:is_static() then
            local name = field:get_name()
            local raw_value = field:get_data(nil)

            log.info(name .. " = " .. tostring(raw_value))

            enum[name] = raw_value
        end
    end

    return enum
end

via.hid.GamePadButton = generate_enum("via.hid.GamePadButton")
app.HIDInputMode = generate_enum("app.HIDInputMode")
```

### GUI Debugger
```lua
local known_elements = {}

re.on_pre_gui_draw_element(function(element, context)
    known_elements[element:call("get_GameObject")] = true
end)

re.on_draw_ui(function()
    local sorted_elements = {}

    for k, v in pairs(known_elements) do
        if not pcall(k.call, k, "get_Name") then
            known_elements[k] = nil
        else
            table.insert(sorted_elements, k)
        end
    end

    table.sort(sorted_elements, function(a, b)
        return a:call("get_Name") < b:call("get_Name")
    end)

    for element, _ in pairs(known_elements) do
        if imgui.tree_node(element:call("get_Name") .. " " .. string.format("%x", element:get_address())) then
            object_explorer:handle_address(element)
            imgui.tree_pop()
        end
    end
end)
```

### Dumping fields of an REManagedObject or type (very verbose)
Use `object:get_type_definition():get_fields()` for an easier way to do this. The below snippet should rarely be used.

```lua
-- type is the "typeof" variant, not the type definition
local function dump_fields_by_type(type)
    log.info("Dumping fields...")

    local binding_flags = 32 | 16 | 4 | 8
    local fields = type:call("GetFields(System.Reflection.BindingFlags)", binding_flags)

    if fields then
        fields = fields:get_elements()

        for i, field in ipairs(fields) do
            log.info("Field: " .. field:call("ToString"))
        end
    end
end

local function dump_fields(object)
    local object_type = object:call("GetType")

    dump_fields_by_type(object_type)
end
```

## Monster Hunter Rise
### Getting the local player
```lua
local function get_localplayer()
    local playman = sdk.get_managed_singleton("snow.player.PlayerManager")

    if not playman then 
         return 
    end

    return playman:call("findMasterPlayer")
end
```

## Devil May Cry 5
### Getting the local player
```lua
local function get_localplayer()
    local playman = sdk.get_managed_singleton(sdk.game_namespace("PlayerManager"))

    if not playman then
        return nil
    end

    return playman:call("get_manualPlayer")
end
```

## Resident Evil 2/3
### Getting the local player
```lua
local function get_localplayer()
    local playman = sdk.get_managed_singleton(sdk.game_namespace("PlayerManager"))

    if not playman then
        return nil
    end

    return playman:call("get_CurrentPlayer")
end
```

## Resident Evil 8
### Getting the local player
```lua
local function get_localplayer()
    if not propsman then
        propsman = sdk.get_managed_singleton(sdk.game_namespace("PropsManager"))
    end

    return propsman:call("get_Player")
end
```