## Methods
### `reframework:is_drawing_ui()`
Returns `true` if the REFramework menu is open.

### `reframework:get_game_name()`
Returns the name of the game this REFramework was compiled for.

e.g. "dmc5" or "re2"

### `reframework:is_key_down(key)`
`key` is a Windows virtual key code.

### `reframework:get_commit_count()`
Returns the total number of commits on the current branch of the REFramework build.

### `reframework:get_branch()`
Returns the branch name of the REFramework build.

ex: "master"

### `reframework:get_commit_hash()`
Returns the commit hash of the REFramework build.

### `reframework:get_tag()`
Returns the last tag of the REFramework build on its current branch.

ex: "v1.5.4"

### `reframework:get_tag_long()`

### `reframework:get_commits_past_tag()`
Returns the number of commits past the last tag.

### `reframework:get_build_date()`
Returns the date that REFramework was built (mm/dd/yyyy).

### `reframework:get_build_time()`
Returns the time that REFramework was built.