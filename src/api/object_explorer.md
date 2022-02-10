Gives access to some of the Object Explorer's UI display. Must be called within `re.on_draw_ui`.

## Methods
### `object_explorer:handle_address(addr)`
Same as typing in the address in the Object Explorer. 

`addr` must point to an REManagedObject for the display to work. 

Verification is not necessary, Object Explorer automatically handles it.