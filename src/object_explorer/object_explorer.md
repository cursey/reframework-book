# Object Explorer

The object explorer will be your go-to reference when actively working on a script or a plugin. It will provide you with tools for examining and modifying objects.

Found under `DeveloperTools` in the REFramework menu.


<video width="640" height="480" controls>
<source src="https://user-images.githubusercontent.com/2909949/176354040-b118473d-2def-4439-bdb9-c8899497aae4.mp4" type="video/mp4">
</video>


## Definitions
### TDB
**T**ype **D**ata**b**ase. Contains all of the metadata for classes, fields, methods, events, etc...

Comparable to IL2CPP metadata in Unity.

## Finding game functions to call, and fields to grab
Poke around the singletons until you find something you're interested in. 

Objects under `Singletons` can be obtained with `sdk.get_managed_singleton("name")`

Objects under `Native Singletons` can be obtained with `sdk.get_native_singleton("name")`

Do note that the `Singletons` (AKA Managed Singletons) are the usually the most exposed. They were originally written in C#.

`Native Singletons` have fields and methods exposed, but they are usually hand picked. These ones were written in C++, and have the least amount of data exposed about them.

Anything under `TDB Methods` or `TDB Fields` of something within the `ObjectExplorer` can be called or grabbed using the various call and field getter/setter methods found here in the wiki. 

You **CANNOT** use the `Reflection Methods` or `Reflection Properties` yet without direct memory reading/writing, only the TDB versions are fully supported.

## Dump SDK
This button will create a few things.

1. A `il2cpp_dump.json` in your game folder
2. An `sdk` folder with C++ headers and sources generated from the TDB data

The `il2cpp_dump.json` is usually the most relevant. It can be used as an offline reference for looking up fields and methods. It can be parsed to your liking with Python or your go-to programming or scripting language.

This dump can take a few minutes to run, so expect your game to freeze. The dump will be quite large, and seem to get larger with each new game that comes to the RE Engine (MHRise's is almost 1GB). Keep this in mind when choosing a text editor to view the file.

Python scripts that make use of the il2cpp dump can be found [Here](https://github.com/praydog/REFramework/tree/master/reversing/scripts) and [Here](https://github.com/praydog/REFramework/tree/master/reversing/rsz)

<details>
<summary>Example piece of il2cpp_dump.json output in RE8</summary>
<pre><code lang=json>
"app.PropsManager": {
    "address": "14814d4f0",
    "crc": "c3e89da7",
    "deserializer_chain": [
        {
            "address": "0x14602b540",
            "name": "via.Object"
        },
        {
            "address": "0x14602a530",
            "name": "System.Object"
        },
        {
            "address": "0x14602a850",
            "name": "via.Component"
        },
        {
            "address": "0x14602a9d0",
            "name": "via.Behavior"
        }
    ],
    "fields": {
        "&lt;Camera>k__BackingField": {
            "flags": "Private",
            "id": 110417,
            "init_data_index": 0,
            "offset_from_base": "0x60",
            "offset_from_fieldptr": "0x10",
            "type": "via.Camera"
        },
        "&lt;Player>k__BackingField": {
            "flags": "Private",
            "id": 110416,
            "init_data_index": 0,
            "offset_from_base": "0x58",
            "offset_from_fieldptr": "0x8",
            "type": "via.GameObject"
        },
        "FlotageProcess": {
            "flags": "FamANDAssem | Family",
            "id": 110418,
            "init_data_index": 0,
            "offset_from_base": "0x68",
            "offset_from_fieldptr": "0x18",
            "type": "app.FlotageProcess"
        },
        "SwingRopeProcess": {
            "flags": "FamANDAssem | Family",
            "id": 110419,
            "init_data_index": 0,
            "offset_from_base": "0x70",
            "offset_from_fieldptr": "0x20",
            "type": "app.SwingRopeProcess"
        }
    },
    "flags": "Public | BeforeFieldInit | NativeCtor | ManagedVTable",
    "fqn": "cdbfb0f2",
    "id": 75313,
    "methods": {
        ".ctor550755": {
            "flags": "FamANDAssem | Family | HideBySig | SpecialName | RTSpecialName",
            "function": "1400522b0",
            "id": 550755,
            "impl_flags": "EmptyCtor | HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            }
        },
        "doAwake550751": {
            "flags": "Family | Virtual | HideBySig",
            "function": "1417678a0",
            "id": 550751,
            "impl_flags": "HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            },
            "vtable_index": 16
        },
        "doLateUpdate550754": {
            "flags": "Family | Virtual | HideBySig",
            "function": "1400b52d0",
            "id": 550754,
            "impl_flags": "HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            },
            "vtable_index": 19
        },
        "doOnDestroy550750": {
            "flags": "Family | Virtual | HideBySig",
            "function": "1400b1410",
            "id": 550750,
            "impl_flags": "HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            },
            "vtable_index": 20
        },
        "doStart550752": {
            "flags": "Family | Virtual | HideBySig",
            "function": "1400b3780",
            "id": 550752,
            "impl_flags": "HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            },
            "vtable_index": 17
        },
        "doUpdate550753": {
            "flags": "Family | Virtual | HideBySig",
            "function": "14176e430",
            "id": 550753,
            "impl_flags": "HasThis",
            "invoke_id": 3,
            "returns": {
                "name": "",
                "type": "System.Void"
            },
            "vtable_index": 18
        },
        "get_Camera550748": {
            "flags": "FamANDAssem | Family | HideBySig | SpecialName",
            "function": "140061200",
            "id": 550748,
            "impl_flags": "HasRetVal | HasThis",
            "invoke_id": 4,
            "returns": {
                "name": "",
                "type": "via.Camera"
            }
        },
        "get_Player550746": {
            "flags": "FamANDAssem | Family | HideBySig | SpecialName",
            "function": "14005a350",
            "id": 550746,
            "impl_flags": "HasRetVal | HasThis",
            "invoke_id": 4,
            "returns": {
                "name": "",
                "type": "via.GameObject"
            }
        },
        "set_Camera550749": {
            "flags": "FamANDAssem | Family | HideBySig | SpecialName",
            "function": "140062dc0",
            "id": 550749,
            "impl_flags": "HasThis",
            "invoke_id": 17,
            "params": [
                {
                    "name": "value",
                    "type": "via.Camera"
                }
            ],
            "returns": {
                "name": "",
                "type": "System.Void"
            }
        },
        "set_Player550747": {
            "flags": "FamANDAssem | Family | HideBySig | SpecialName",
            "function": "14005b6b0",
            "id": 550747,
            "impl_flags": "HasThis",
            "invoke_id": 17,
            "params": [
                {
                    "name": "value",
                    "type": "via.GameObject"
                }
            ],
            "returns": {
                "name": "",
                "type": "System.Void"
            }
        }
    },
    "parent": "app.SingletonBehavior`1<app.PropsManager>",
    "properties": {
        "Camera": {
            "getter": "get_Camera",
            "id": 126015,
            "setter": "set_Camera"
        },
        "Player": {
            "getter": "get_Player",
            "id": 126014,
            "setter": "set_Player"
        }
    },
    "size": "78"
}
</code></pre>
</details>

## Singletons
Are generally global managers dedicated to certain parts of the game, e.g. `app.EnemyManager` for enemies, `app.InteractManager` for interactions, etc...

## Native Singletons
Are also global managers, but they were created in C++ instead of C#. This means they may not have as much data exposed about them, if any at all.

These singletons are usually much more related to engine behavior than the usual `Singletons`.
    
## TDB Fields
Lists all of the fields for a given type visible within the TDB.

## TDB Methods
Lists all of the methods for a given type visible within the TDB. Can right click on any method to open a context menu.

### Context Menu
#### Copy Address
#### Copy Name
#### Hook
Hooks the method and opens a separate window, adds onto it if it already exists. The window contains each method you've hooked from the Object Explorer. 

Each method contains
* Skip function call
* Call count
    
Useful for debugging if you need to know if a method gets called or not. You can also choose to skip calling the original method.
