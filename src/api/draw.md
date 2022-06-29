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

### `draw.gizmo(unique_id, matrix, operation, mode)`
* `unique_id`, an int64 that must be unique for every gizmo. Usually an address of an object will work. The same ID will control multiple gizmos with the same ID.
* `matrix`, the Matrix4x4f the gizmo is modifying.
* `operation`, defaults to UNIVERSAL. Use `imgui.ImGuizmoOperation` enum.
* `mode`, defaults to WORLD. WORLD or LOCAL. Use `imgui.ImGuizmoMode` enum.

Returns a tuple of `changed`, `mat`. Mat is the modified `matrix` that was passed.

```
    imgui.new_enum("ImGuizmoOperation", 
                    "TRANSLATE", ImGuizmo::OPERATION::TRANSLATE, 
                    "ROTATE", ImGuizmo::OPERATION::ROTATE,
                    "SCALE", ImGuizmo::OPERATION::SCALE,
                    "SCALEU", ImGuizmo::OPERATION::SCALEU,
                    "UNIVERSAL", ImGuizmo::OPERATION::UNIVERSAL);
    imgui.new_enum("ImGuizmoMode", 
                    "WORLD", ImGuizmo::MODE::WORLD,
                    "LOCAL", ImGuizmo::MODE::LOCAL);
```

Example video

<video width="640" height="480" controls>
<source src="https://user-images.githubusercontent.com/2909949/176351319-c070b216-fe71-4eb9-84f2-46c665892b11.mp4" type="video/mp4">
</video>

### `draw.cube(matrix)`

### `draw.grid(matrix, size)`
