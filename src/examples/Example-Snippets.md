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
known_elements = {}

re.on_pre_gui_draw_element(function(element, context)
    known_elements[element:call("get_GameObject")] = os.clock()
end)

local draw_control = nil
local draw_children = nil
local draw_next = nil

draw_control = function(control, prefix, seen)
    prefix = prefix or ""
    if control == nil then return end

    seen = seen or {}
    if seen[control] then return end
    seen[control] = true

    local name = control:call("get_Name")
    if imgui.tree_node(prefix .. name) then
        draw_children(control, prefix, seen)
        object_explorer:handle_address(control)
        imgui.tree_pop()
    end

    draw_next(control, prefix, seen)
end

draw_next = function(control, prefix, seen)
    prefix = prefix or ""
    if control == nil then return end

    local ok, next = pcall(control.call, control, "get_Next")

    if ok then
        draw_control(next, prefix, seen)
    end

    --draw_next(control, prefix)
    --draw_children(control, prefix .. " ")
end

draw_children = function(control, prefix)
    prefix = prefix or ""
    if control == nil then return end

    local child = control:call("get_Child")
    draw_control(child, prefix .. " ", seen)
end

local should_draw_offsets = {
    re4 = 0x11,
    re2 = 0x13,
    re7 = 0x13,
}

local should_draw_offset = should_draw_offsets[reframework:get_game_name()]

if should_draw_offset == nil then
    should_draw_offset = 0x11
end

re.on_draw_ui(function()
    local sorted_elements = {}

    for k, v in pairs(known_elements) do
        local succeed, result = pcall(k.call, k, "get_Name")

        if not succeed or result == nil or k:get_reference_count() == 1 or (os.clock() - v > 1) then
            known_elements[k] = nil
        else
            table.insert(sorted_elements, k)
        end
    end

    table.sort(sorted_elements, function(a, b)
        return a:call("get_Name") < b:call("get_Name")
    end)

    for i, element in ipairs(sorted_elements) do
        imgui.push_id(tostring(element:get_address()))

        local changed, value = imgui.checkbox("", element:read_byte(should_draw_offset) == 1)

        if changed then
            element:write_byte(should_draw_offset, value and 1 or 0)
        end
        

        imgui.same_line()

        local gui = element:call("getComponent(System.Type)", sdk.typeof("via.gui.GUI"))

        if gui ~= nil then
            local view = gui:call("get_View")

            if view ~= nil then
                --if (imgui.button("test")) then
                    view:call("set_ResAdjustScale(via.gui.ResolutionAdjustScale)", 2)
                    view:call("set_ResAdjustAnchor(via.gui.ResolutionAdjustAnchor)", 4)
                    view:call("set_ResolutionAdjust(System.Boolean)", true)
                --end
            end
        end

        if imgui.tree_node(element:call("get_Name") .. " " .. string.format("%x", element:get_address())) then
            local transform = element:call("get_Transform")
            local joints = transform:call("get_Joints")

            if joints then
                imgui.text("Joints: " .. tostring(joints:get_size()))
            end

            if gui ~= nil then
                local ok, world_pos_attach = pcall(element, call, "getComponent(System.Type)", sdk.typeof("app.UIWorldPosAttach"))

                if ok and world_pos_attach ~= nil then
                    local now_target_pos = world_pos_attach:get_field("_NowTargetPos")
                    local screen_pos = draw.world_to_screen(now_target_pos)

                    if screen_pos then
                        local name = element:call("get_Name")

                        draw.text(name, screen_pos.x, screen_pos.y, 0xFFFFFFFF)
                    end
                end

                local view = gui:call("get_View")

                if view ~= nil then
                    draw_control(view)
                end
            end

            object_explorer:handle_address(element)
            imgui.tree_pop()
        end

        imgui.pop_id()
    end
end)
```



<video width="1280" height="720" controls>
<source src="https://user-images.githubusercontent.com/2909949/176351319-c070b216-fe71-4eb9-84f2-46c665892b11.mp4" type="video/mp4">
</video>



### 3D Gizmo test script
```
local gn = reframework:get_game_name()

local function get_localplayer()
    if gn == "re2" or gn == "re3" then
        local player_manager = sdk.get_managed_singleton(sdk.game_namespace("PlayerManager"))
        if player_manager == nil then return nil end
    
        return player_manager:call("get_CurrentPlayer")
    elseif gn == "dmc5" then
        local player_manager = sdk.get_managed_singleton(sdk.game_namespace("PlayerManager"))
        if player_manager == nil then return nil end
    
        local player_comp = player_manager:call("get_manualPlayer")
        if player_comp == nil then return nil end

        return player_comp:call("get_GameObject")
    elseif gn == "mhrise" then
        local player_manager = sdk.get_managed_singleton(sdk.game_namespace("player.PlayerManager"))
        if player_manager == nil then return nil end
    
        local player_comp = player_manager:call("findMasterPlayer")
        if player_comp == nil then return nil end

        return player_comp:call("get_GameObject")
    end

    return nil
end

local joint_work = {}

re.on_pre_application_entry("LockScene", function()
    for k, v in pairs(joint_work) do
        v.func(v.mat)
    end

    joint_work = {}
end)

re.on_frame(function()
    local player = get_localplayer()
    if player == nil then return end

    local transform = player:call("get_Transform")
    if transform == nil then return end

    local mat = transform:call("get_WorldMatrix")
    local changed = false

    changed,mat = draw.gizmo(transform:get_address(), mat)

    if changed then
        transform:set_rotation(mat:to_quat())
        transform:set_position(mat[3])
    end

    local joints = transform:call("get_Joints")
    local mouse = imgui.get_mouse()

    for i, joint in ipairs(joints:get_elements()) do
        mat = joint:call("get_WorldMatrix")

        local mat_screen = draw.world_to_screen(mat[3])
        local mat_screen_top = draw.world_to_screen(mat[3] + Vector3f.new(0, 0.1, 0))

        if mat_screen and mat_screen_top then
            local delta = (mat_screen - mat_screen_top):length()
            local mouse_delta = (mat_screen - mouse):length()
            if mouse_delta <= delta then

                changed, mat = draw.gizmo(joint:get_address(), mat)

                if changed then
                    table.insert(joint_work, { ["mat"] = mat, ["func"] = function(mat)
                        joint:call("set_Rotation", mat:to_quat())
                        joint:call("set_Position", mat[3])
                    end
                })
                end
            end
        end
    end
end)
```

### RE2/RE3 material toggler with keybinding system
```lua
local game_name = reframework:get_game_name()
if game_name ~= "re2" and name ~= "re3" then
    re.msg("This script is only for RE2 or RE3")
    return
end

local display_children = nil
local display_siblings = nil

local waiting_for_input_map = {}
local key_bindings = {}
local prev_key_states = {}

local function was_key_down(i)
    local down = reframework:is_key_down(i)
    local prev = prev_key_states[i]
    prev_key_states[i] = down

    return down and not prev
end

local function display_mesh(transform)
    local gameobj = transform:get_GameObject()
    if gameobj == nil then return end

    imgui.set_next_item_open(true, 2)
    imgui.push_id(gameobj:get_address())

    -- Look for via.render.Mesh components within the game object.
    -- It will have the materials we can toggle.
    if imgui.tree_node(gameobj:get_Name()) then
        -- Object explorer display for debugging.
        if imgui.tree_node("Object explorer") then
            object_explorer:handle_address(gameobj:get_address())
            imgui.tree_pop()
        end

        local mesh = gameobj:call("getComponent(System.Type)", sdk.typeof("via.render.Mesh"))

        -- Now display the materials in the mesh.
        if mesh ~= nil then
            imgui.text("Materials: " .. tostring(mesh:get_MaterialNum()))
            for i=0, mesh:get_MaterialNum()-1 do
                imgui.push_id(i)

                local name = mesh:getMaterialName(i)
                local enabled = mesh:getMaterialsEnable(i)

                local bound_key = key_bindings[name]
                local is_key_down = bound_key ~= nil and was_key_down(bound_key)

                if imgui.checkbox(name, enabled) or is_key_down then
                    mesh:setMaterialsEnable(i, not enabled)
                end

                imgui.same_line()
                if not waiting_for_input_map[name] then
                    if imgui.button("bind key") then
                        waiting_for_input_map[name] = true
                    end

                    if key_bindings[name] ~= nil then
                        imgui.same_line()
                        if imgui.button("clear") then
                            key_bindings[name] = nil
                        end

                        imgui.same_line()
                        imgui.text_colored("key: " .. tostring(key_bindings[name]), 0xFF00FF00)
                    end
                else
                    imgui.text_colored("Press a key to bind", 0xFF00FFFF)

                    local key = reframework:get_first_key_down()
                    if key ~= nil then
                        key_bindings[name] = key
                        waiting_for_input_map[name] = false
                    end
                end

                imgui.pop_id()
            end
        else
            imgui.text("No via.render.Mesh component found")
        end

        imgui.tree_pop()
    end

    imgui.pop_id()
end

display_children = function(transform)
    local child = transform:get_Child()

    if child ~= nil then
        display_mesh(child)
        display_children(child)
        display_siblings(child)
    end
end

display_siblings = function(transform)
    local next = transform:get_Next()

    if next ~= nil then
        display_mesh(next)
        display_children(next)
        display_siblings(next)
    end
end

re.on_draw_ui(function()
    -- Obtain the FigureManager singleton.
    local figure_manager = sdk.get_managed_singleton(sdk.game_namespace("FigureManager"))

    if figure_manager == nil then
        imgui.text("FigureManager not found")
        return
    end

    if imgui.tree_node("Material toggler") then
        -- Get the current figure/model being displayed.
        local figure = figure_manager:get_CurrentFigureObj()

        if figure ~= nil then
            local figure_name = figure:get_Name()
            imgui.text("Current figure: " .. figure_name)

            local transform = figure:get_Transform()

            -- Go through all of the children transforms and look for mesh components.
            -- The mesh components will have the materials we can toggle.
            display_children(transform)
        else
            imgui.text("No figure found")
        end

        imgui.tree_pop()
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

## General
### Spinner and progress bar in ImGui
```lua
local progress = 0.0

re.on_frame(function()
    progress = progress + 0.001
    if progress > 1.0 then 
        progress = 0.0
    end
end)

local function lerp(x0, x1, t)
    return (1.0 - t) * x0 + t * x1
end

local function interval(t0, t1, tween_func)
    return function(t)
        --return t < t0 and 0.0 or t > t1 and 1.0 or tween_func((t - t0) / (t1 - t0))
        if t < t0 then
            return 0.0
        elseif t > t1 then
            return 1.0
        end
        
        return tween_func((t - t0) / (t1 - t0))
    end
end

local function sawtooth(x, t)
    return math.fmod(x * t, 1.0)
end

local function cubic_bezier(t, p0, p1, p2, p3)
    local u = 1.0 - t
    return p0 * u*u*u + p1 * 3.0 * u*u*t + p2 * 3.0 * u*t*t + p3 * t*t*t
end

local function stroke_head_tween(d, t)
    t = sawtooth(d, t)
    return interval(0.0, 0.5, function(x) return cubic_bezier(x, 0.2, 0.0, 0.4, 1.0) end)(t)
end

local function stroke_tail_tween(d, t)
    t = sawtooth(d, t)
    return interval(0.5, 1.0, function(x) return cubic_bezier(x, 0.2, 0.0, 0.4, 1.0) end)(t)
end

local function step_tween(x, t)
    return math.floor(lerp(0.0, x, t))
end

-- https://github.com/ocornut/imgui/issues/1901
local function draw_spinner(center, radius, color, thickness)
    local rect = {
        imgui.get_cursor_pos(),
        imgui.get_cursor_pos() + Vector2f.new(radius * 2, radius * 2) -- todo: frame padding
    }

    imgui.item_size(rect[1], rect[2])
    if not imgui.item_add(rect[1], rect[2], "circle") then
        --print("oh no")
        --return
    end

    local period = 5.0
    local t = math.fmod(os.clock(), period) / period

    imgui.draw_list_path_clear()

    local num_segments = 24

    local num_detents = 5
    local skip_detents = 3

    local head_value = stroke_head_tween(num_detents, t);
    local tail_value = stroke_tail_tween(num_detents, t);
    local step_value = step_tween(num_detents, t);
    local rotation_value = sawtooth(num_detents, t);

    local min_arc =  30.0 / 360.0 * 2.0 * math.pi
    local max_arc = 270.0 / 360.0 * 2.0 * math.pi
    local step_offset = skip_detents * 2.0 * math.pi / num_detents
    local rotation_compensation = math.fmod(4.0*math.pi - step_offset - max_arc, 2.0 * math.pi);

    local start_angle = -math.pi * 2.0
    local a_min = start_angle + tail_value * max_arc + rotation_value * rotation_compensation - step_value * step_offset;
    local a_max = a_min + (head_value - tail_value) * max_arc + min_arc;

    for i = 0, num_segments - 1 do
        local a = a_min + (i / num_segments) * (a_max - a_min)
        local x = center.x + math.cos(a) * radius
        local y = center.y + math.sin(a) * radius
        imgui.draw_list_path_line_to(Vector2f.new(x, y))
    end

    imgui.draw_list_path_stroke(color, false, thickness)
end

re.on_draw_ui(function()
    local center = imgui.get_cursor_pos() + imgui.get_window_pos()
    local radius = 10
    local color = 0x5050BFFF
    local thickness = 2

    draw_spinner(Vector2f.new(center.x + radius, center.y + radius), radius, color, thickness)

    imgui.same_line()
    imgui.progress_bar(progress, Vector2f.new(200, 20), string.format("Progress: %.1f%%", progress * 100))
end)
```
