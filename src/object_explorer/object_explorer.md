# Object Explorer

The object explorer will be your go-to reference when actively working on a script or a plugin. It will provide you with tools for examining and modifying objects.

Found under `DeveloperTools` in the REFramework menu.

## Finding game functions to call, and fields to grab
Poke around the singletons until you find something you're interested in. 

Objects under `Singletons` can be obtained with `sdk.get_managed_singleton("name")`

Objects under `Native Singletons` can be obtained with `sdk.get_native_singleton("name")`

Do note that the `Singletons` (AKA Managed Singletons) are the usually the most exposed. They were originally written in C#.

`Native Singletons` have fields and methods exposed, but they are usually hand picked. These ones were written in C++, and have the least amount of data exposed about them.

Anything under `TDB Methods` or `TDB Fields` of something within the `ObjectExplorer` can be called or grabbed using the various call and field getter/setter methods found here in the wiki. 

You **CANNOT** use the `Reflection Methods` or `Reflection Properties` yet without direct memory reading/writing, only the TDB versions are fully supported.

## Singletons
Are generally global managers dedicated to certain parts of the game, e.g. `app.EnemyManager` for enemies, `app.InteractManager` for interactions, etc...
