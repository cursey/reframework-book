Bindings to access VR from lua.

## Methods
### `vrmod:get_controllers()`
Returns a list of device indices for the active controllers.

### `vrmod:get_position(index)`
Returns the position for a given device index.

### `vrmod:get_rotation(index)`
Returns the rotation for a given device index.

### `vrmod:get_transform(index)`
Returns the full transformation matrix for a given device index.

### `vrmod:get_velocity(index)`
Returns the velocity for a given device index.

### `vrmod:get_angular_velocity(index)`
Returns the angular velocity for a given device index.

### `vrmod:get_left_stick_axis()`
Returns a `Vector2f`.

### `vrmod:get_right_stick_axis()`
Returns a `Vector2f`.

### `vrmod:get_current_eye_transform(flip)`
### `vrmod:get_current_projection_matrix(flip)`
### `vrmod:get_standing_origin()`
### `vrmod:set_standing_origin(pos)`
`pos` is a Vector4f.

### `vrmod:get_rotation_offset()`
### `vrmod:set_rotation_offset(quat)`
### `vrmod:recenter_view()`
### `vrmod:recenter_gui(from)`
`from` is a `Quaternion`.

### `vrmod:get_action_set()`
### `vrmod:get_active_action_set()`
### `vrmod:get_action_trigger()`
### `vrmod:get_action_grip()`
### `vrmod:get_action_joystick()`
### `vrmod:get_action_joystick_click()`
### `vrmod:get_action_a_button()`
### `vrmod:get_action_b_button()`
### `vrmod:get_action_weapon_dial()`
### `vrmod:get_action_minimap()`
### `vrmod:get_action_block()`
### `vrmod:get_action_dpad_up`
### `vrmod:get_action_dpad_down`
### `vrmod:get_action_dpad_left`
### `vrmod:get_action_dpad_right`
### `vrmod:get_action_heal`
### `vrmod:get_left_joystick()`
Returns a `vr::VRInputValueHandle_t`. To be used in `vrmod:is_action_active` as the `source`.

### `vrmod:get_right_joystick()`
Returns a `vr::VRInputValueHandle_t`. To be used in `vrmod:is_action_active` as the `source`.

### `vrmod:get_right_joystick()`
### `vrmod:is_using_controllers()`
Returns `true` if the user has issued any inputs to the controllers within the last 10 seconds.

### `vrmod:is_openvr_loaded()`
Returns `true` if OpenVR is loaded.

### `vrmod:is_openxr_loaded()`
Returns `true` if OpenXR is loaded.

### `vrmod:is_hmd_active()`
Returns `true` if the user currently has their VR headset on.
### `vrmod:is_action_active(action, source)`
Returns `true` if the `action` belonging to `source` is active. 

Active meaning that the user is e.g. holding the A button down if the A button was the `action`.
### `vrmod:is_using_hmd_oriented_audio()`
### `vrmod:toggle_hmd_oriented_audio()`
### `vrmod:apply_hmd_transform(rotation, position)`
Applies the headset's transform to the given rotation and position. Both parameters are in and out parameters.

### `vrmod:apply_haptic_vibration(seconds_from_now, duration, frequency, amplitude, source)`
### `vrmod:get_last_render_matrix()`
