Methods to be used on `re.on_frame` or `re.on_draw_ui`.

If you need more rendering functionality, check out the REFramework plugin [reframework-d2d](https://github.com/cursey/reframework-d2d)

## Methods
### `draw.world_to_screen(world_pos)`
Returns an optional `Vector2f` corresponding to the 2D screen position. Returns `nil` if `world_pos` is not visible.
### `draw.world_text(text, 3d_pos, color)`
### `draw.text(text, x, y, color)`
### `draw.filled_rect(x, y, w, h, color)`
### `draw.outline_rect(x, y, w, h, color)`
### `draw.line(x1, y1, x2, y2, color)`