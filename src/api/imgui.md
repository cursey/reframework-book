Bindings for ImGui. Can be used in the `re.on_draw_ui` callback.

Some methods can be used in `re.on_frame` if `begin_window`/`end_window` is used.

Example:
```
local thing = 1
local things = { "hi", "hello", "howdy", "hola", "aloha" }

re.on_draw_ui(function()
    if imgui.button("Whats up") then 
        thing = 1
    end

    local changed, new_thing = imgui.combo("Greeting", thing, things) 
    if changed then thing = new_thing end
end)
```

## Methods
### `imgui.begin_window(name, open, flags)`
Creates a new window with the title of `name`.

`open` is a bool. Can be `nil`. If not `nil`, a close button will be shown in the top right of the window.

`flags` - ImGuiWindowFlags.

`begin_window` must have a corresponding `end_window` call.

This function may only be called in `on_frame`, not `on_draw_ui`.

Returns a bool. Returns `false` if the user wants to close the window.

### `imgui.end_window()`
Ends the last `begin_window` call. Required.

### `imgui.begin_child_window(size, border, flags)`
`size` - Vector2f

`border` - bool

`flags` - ImGuiWindowFlags

### `imgui.end_child_window()`
### `imgui.begin_group()`
### `imgui.end_group()`

### `imgui.begin_rect()`
### `imgui.end_rect(additional_size, rounding)`
These two methods draw a rectangle around the elements between `begin_rect` and `end_rect`

### `imgui.button(label)`
Draws a button with `label` text.

Returns `true` when the user presses the button.

### `imgui.text(text)`
Draws text.

### `imgui.checkbox(label, value)`
Returns a tuple of `changed`, `value`

### `imgui.drag_float(label, value, speed, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.drag_float2(label, value (Vector2f), speed, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.drag_float3(label, value (Vector3f), speed, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.drag_float4(label, value (Vector4f), speed, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.drag_int(label, value, speed, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.slider_float(label, value, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.slider_int(label, value, min, max, display_format (optional))`
Returns a tuple of `changed`, `value`

### `imgui.input_text(label, value, flags (optional))`
Returns a tuple of `changed`, `value`

### `imgui.combo(label, selection, values)`
Returns a tuple of `changed, value`. 

`changed` = true when selection changes. 

`value` is the selection index within `values` (a table)

### `imgui.color_picker(label, color, flags)`

Returns a tuple of `changed`, `value`. `color` is an integer color in the form ABGR which `imgui` and `draw` APIs expect.

### `imgui.color_picker_argb(label, color, flags)`

Returns a tuple of `changed`, `value`. `color` is an integer color in the form ARGB.

### `imgui.color_picker3(label, color (Vector3f), flags)`

Returns a tuple of `changed`, `value`

### `imgui.color_picker4(label, color (Vector4f), flags)`

Returns a tuple of `changed`, `value`

### `imgui.color_edit(label, color, flags)`

Returns a tuple of `changed`, `value`. `color` is an integer color in the form ABGR which `imgui` and `draw` APIs expect.

### `imgui.color_edit_argb(label, color, flags)`

Returns a tuple of `changed`, `value`. `color` is an integer color in the form ARGB.

### `imgui.color_edit3(label, color (Vector3f), flags)`

Returns a tuple of `changed`, `value`

### `imgui.color_edit4(label, color (Vector4f), flags)`

Returns a tuple of `changed`, `value`

`flags` for `color_picker/edit` APIs: `ImGuiColorEditFlags`

### `imgui.tree_node(label)`
### `imgui.tree_node_ptr_id(id, label)`
### `imgui.tree_node_str_id(id, label)`
### `imgui.tree_pop()`
All of the above `tree` functions must have a corresponding `tree_pop`!

### `imgui.same_line()`
### `imgui.spacing()`
### `imgui.new_line()`
### `imgui.is_item_hovered()`

### `imgui.collapsing_header(name)`

### `imgui.load_font(filepath, size, [ranges])`
Loads a font file from the `reframework/fonts` subdirectory at the specified `size` with optional Unicode `ranges` (an array of start, end pairs ending with 0). Returns a handle for use with `imgui.push_font()`. If `filepath` is nil, it will load the default font at the specified size.

### `imgui.push_font(font)`
Sets the font to be used for the next set of ImGui widgets/draw commands until `imgui.pop_font` is called.

### `imgui.pop_font()`
Unsets the previously pushed font.

### `imgui.get_default_font_size()`
Returns size of the default font for REFramework's UI.

### `imgui.set_next_window_pos(pos (Vector2f or table), condition, pivot (Vector2f or table))`
`condition` is the `ImGuiCond` enum.

```
enum ImGuiCond_
{
    ImGuiCond_None          = 0,        // No condition (always set the variable), same as _Always
    ImGuiCond_Always        = 1 << 0,   // No condition (always set the variable)
    ImGuiCond_Once          = 1 << 1,   // Set the variable once per runtime session (only the first call will succeed)
    ImGuiCond_FirstUseEver  = 1 << 2,   // Set the variable if the object/window has no persistently saved data (no entry in .ini file)
    ImGuiCond_Appearing     = 1 << 3    // Set the variable if the object/window is appearing after being hidden/inactive (or the first time)
};
```

### `imgui.set_next_window_size(size (Vector2f or table), condition)`
`condition` is the `ImGuiCond` enum.

### `imgui.push_id(id)`
`id` can be an `int`, `const char*`, or `void*`.

### `imgui.pop_id()`