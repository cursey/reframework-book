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

### `imgui.small_button(label)`

### `imgui.invisible_button(id, size, flags)`
`size` is a Vector2f or a size 2 array.

### `imgui.arrow_button(id, dir)`
`dir` is an `ImguiDir`

### `imgui.text(text)`
Draws text.

### `imgui.text_colored(text, color)`
Draws text with color.

`color` is an integer color in the form ARGB.

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
Returns a tuple of `changed`, `value`, `selection_start`, `selection_end`

### `imgui.input_text_multiline(label, value, size, flags (optional))`
Returns a tuple of `changed`, `value`, `selection_start`, `selection_end`

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
### `imgui.is_item_hovered(flags)`
### `imgui.is_item_active()`
### `imgui.is_item_focused()`

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

```cpp
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

### `imgui.get_id()`

### `imgui.get_mouse()`
Returns a `Vector2f` corresponding to the user's mouse position in window space.

## Methods, to be documented
### `imgui.get_key_index(...)`

### `imgui.is_key_down(...)`

### `imgui.is_key_pressed(...)`

### `imgui.is_key_released(...)`

### `imgui.is_mouse_down(...)`

### `imgui.is_mouse_clicked(...)`

### `imgui.is_mouse_released(...)`

### `imgui.is_mouse_double_clicked(...)`

### `imgui.indent(...)`

### `imgui.unindent(...)`

### `imgui.begin_tooltip(...)`

### `imgui.end_tooltip(...)`

### `imgui.set_tooltip(...)`

### `imgui.open_popup(...)`

### `imgui.begin_popup(...)`

### `imgui.begin_popup_context_item(...)`

### `imgui.end_popup(...)`

### `imgui.close_current_popup(...)`

### `imgui.is_popup_open(...)`

### `imgui.calc_text_size(...)`

### `imgui.get_window_size(...)`

### `imgui.get_window_pos(...)`

### `imgui.set_next_item_open(...)`

### `imgui.begin_list_box(...)`

### `imgui.end_list_box(...)`

### `imgui.begin_menu_bar(...)`

### `imgui.end_menu_bar(...)`

### `imgui.begin_main_menu_bar(...)`

### `imgui.end_main_menu_bar(...)`

### `imgui.begin_menu(...)`

### `imgui.end_menu(...)`

### `imgui.menu_item(...)`

### `imgui.get_display_size(...)`

### `imgui.push_item_width(...)`

### `imgui.pop_item_width(...)`

### `imgui.set_next_item_width(...)`

### `imgui.calc_item_width(...)`

### `imgui.push_style_color(...)`

### `imgui.pop_style_color(...)`

### `imgui.push_style_var(...)`

### `imgui.pop_style_var(...)`

### `imgui.get_cursor_pos(...)`

### `imgui.set_cursor_pos(...)`

### `imgui.get_cursor_start_pos(...)`

### `imgui.get_cursor_screen_pos(...)`

### `imgui.set_cursor_screen_pos(...)`

### `imgui.set_item_default_focus(...)`

## Table API
### `imgui.begin_table(...)`

### `imgui.end_table(...)`

### `imgui.table_next_row(...)`

### `imgui.table_next_column(...)`

### `imgui.table_set_column_index(...)`

### `imgui.table_setup_column(...)`

### `imgui.table_setup_scroll_freeze(...)`

### `imgui.table_headers_row(...)`

### `imgui.table_header(...)`

### `imgui.table_get_sort_specs(...)`

### `imgui.table_get_column_count(...)`

### `imgui.table_get_column_index(...)`

### `imgui.table_get_row_index(...)`

### `imgui.table_get_column_name(...)`

### `imgui.table_get_column_flags(...)`

### `imgui.table_set_bg_color(...)`
