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
### `draw.outline_circle(x, y, radius, color, num_segments)`
### `draw.filled_circle(x, y, radius, color, num_segments)`
### `draw.outline_quad(x1, y1, x2, y2, x3, y3, x4, y4, color)`
### `draw.filled_quad(x1, y1, x2, y2, x3, y3, x4, y4, color)`
### `draw.sphere(world_pos, radius, color, outline)`
Draws a 3D sphere with a 2D approximation in world space.

### `draw.capsule(world_start_pos, world_end_pos, radius, color, outline)`
Draws a 3D capsule with a 2D approximation in world space.
