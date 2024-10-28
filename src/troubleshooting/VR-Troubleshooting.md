Here you'll find various solutions and FAQ to various problems you may encounter with the VR mod.

[Getting Started Guide](https://beastsaber.notion.site/beastsaber/Praydog-s-Resident-Evil-2-3-VR-mod-3db8bd110ebf4a38870e1a5114b16998)

Newer builds can be found [here](https://github.com/praydog/REFramework-nightly/releases/) (master branch only)

The old pre-RT beta builds of RE2/RE3/RE7 may be more stable with the mod on some computers. You can switch to the beta in Steam under the game's properties. Once this is done, the old version of the mod will need to be downloaded, these are the zip files in the release with "TDB" in them.

## Builds with better performance and fixed TAA

(This only applies to RT builds of RE2/3/7, RE8 and newer games)

In REFramework's **pd-upscaler builds**, TAA is completely fixed, and performance is greatly improved with a new renderer. Optionally, DLSS, FSR2, XeSS can be used.

This will eventually make its way into the stable builds, but you can find the **pd-upscaler** builds here, with a GitHub account: [https://github.com/praydog/REFramework/actions](https://github.com/praydog/REFramework/actions)

![upscalerbuilds](https://github.com/user-attachments/assets/f981abb3-a5d4-4e64-86fd-c97e89b8dec6)

## Reporting a bug
Report it on the [Issues](https://github.com/praydog/REFramework/issues) page.

If you are crashing, or are having a technical problem then upload these files from your game folder:
* `re2_framework_log.txt`
* `reframework_crash.dmp` if you are crashing

If you do not have an `reframework_crash.dmp` and are crashing, download a newer build, links at the top of the page.

## Trying newer/beta builds (pd-upscaler)
GitHub account required: [https://github.com/praydog/REFramework/actions/](https://github.com/praydog/REFramework/actions/)

## Opening the in-game menu with motion controllers (OpenVR only right now)
Aim at the palm of your left hand with your head and your right hand. Do not press anything, and an overlay menu should show up.

If that doesn't work, you can use the desktop version of the menu using the Insert key. This method won't work in the headset.

If that still doesn't work, options can be changed in the `re2_fw_config.txt` in your game directory.


## For those with motion sickness
Enable "Decoupled Camera Pitch" under "VR" in the REFramework menu. This will stop the camera from moving vertically in any way. Do note that while this may not necessarily break anything, it may make it less clear of what to do in certain parts of the game when the camera is supposed to shift vertically, or what the camera is intending to look at in a cutscene.

## Common fixes
* Restarting SteamVR
* Disabling overlay software
* Disabling SteamVR theater
* Disabling "Hardware-accelerated GPU scheduling"
   * This **MUST** be disabled if you are getting extremely low frames
* Swapping between DX11 and DX12
* Taking the headset off and putting it back on
* If your game appears "rainbow" colored, or you are stuck in the SteamVR void
    * You have an HDR monitor and HDR must be disabled in some way
    * Unplugging the monitor temporarily has been a reported fix
    * Also setting the game to windowed mode can fix this, HDR sometimes gets forced on in fullscreen
* If your screen looks squished with black bars turn off Borderless window mode
* Make sure no graphical settings are being forced globally (e.g. from Nvidia Control Panel)
    * The exception to this is disabling HDR which is required or else the game will not display within the headset

### In RE2
There is a known issue of a softlock sometimes occurring in the Birkin fight if it goes on too long. It can be fixed simply by disabling FirstPerson until he spawns again.

## Switching to OpenXR
By default, REFramework uses OpenVR for the VR functionality. In some cases, switching to OpenXR can increase performance anywhere from slightly, to a significant amount. The most significant gains have been observed to come when running the games in DX12, but your mileage may vary.

To switch to OpenXR, simply delete the `openvr_api.dll` that came with the zip file. Make sure the `openxr_loader.dll` that came with the mod is present in the game folder.

Not all headsets may have an OpenXR runtime. Headsets like the Index which run natively through SteamVR may not see a performance increase.

If you are using an Oculus headset or a headset that has its own dedicated OpenXR runtime, it is recommended to switch to the runtime provided by your headset manufacturer, e.g. the Oculus OpenXR runtime for Oculus headsets. Using SteamVR as the runtime is only recommended if your headset does not have a dedicated runtime, or are using something like Virtual Desktop.

## OpenXR Pitfalls
* There is no wrist overlay for modifying VR settings yet
* Modifying controller bindings is not as expressive as OpenVR
* Personally only tested on Oculus Quest 2 and CV1, reports that it works on Reverb G2

## What about the others like DMC5 and MHRise?
They are both fully 6DOF but with the least support.

~~They have the same issue of audio positioning being incorrect~~ **only in MHRise now**.

~~DMC5 has some issues with some incorrect UI elements.~~ Fixed in a recent update.

## Gameplay
### All games
#### Switching Weapons
On supported controllers, bound to left trigger + joystick by default. Otherwise, "weapondial" will need to be bound to something, or the d-pad bindings will need to be bound.

### RE2 and RE3
### General
* Motion controller support
* Head-based movement
* Smooth locomotion
* Smooth turning
* Mostly right-handed

Playing with a gamepad is supported. IK gets disabled when using one.

### Gestures
#### Opening the map
Can be done by pressing the inventory button while holding your controller behind your head/over your shoulder.

### Additional options
#### Disabling the crosshair
The option to disable it is under "Script Generated UI" in the REFramework menu. The corresponding script can also be removed from the `reframework/autorun` folder.

---

### RE7 and RE8
#### General
* Motion controller support
* Head-based movement
* Smooth locomotion
* Smooth turning
* Mostly right-handed

Playing with a gamepad is supported.

### Controls not working?
1. Unplug or disconnect your gamepad. The gamepad conflicts with the VR controls.
2. Not all controllers may have proper default bindings, and will need to be manually bound

### Body is annoying or getting in the way?
Body parts can be selectively disabled under "RE8VR" in the REFramework menu

### Want to play without facegun or motion controls, or any additional features, only VR?
Just delete `re8_vr.lua` from the `reframework` directory.

### Broken graphical settings
(RE7) Ambient occlusion must be set to SSAO or Off. The max setting is broken/buggy.

### Gestures
#### Opening the map
Can be done by pressing the inventory button while holding your controller behind your head/over your shoulder.

#### Blocking
Hold your hands in front of your face.

#### Healing
Reach behind your head with your right hand, hold down the grip, and a medicine bottle will appear in your hand. Press right trigger to initiate a heal.

A softlock can occur in the first fight with Mia if you pull out the bottle.

### Additional options
#### Disabling the crosshair
The option to disable it is under "Script Generated UI" in the REFramework menu.

## Bindings
Bindings can be changed in SteamVR's controller bindings section.

Known working default bindings:
* Oculus Touch
* Valve Index Knuckles

Needs additional testing:
* Vive Wands

If a set of controllers don't work as expected, they can be set up in the SteamVR controller bindings.

In OpenXR, the bindings can be changed under "VR".

## Performance
One of the most taxing parts of these mods is the **resolution** you have set. The in-game resolution has no effect, it must be changed in SteamVR.

To modify the resolution in your headset:
* Open the SteamVR overlay
* Click on the cogwheel on the bottom right
* Click on "Video"
* Change "Render Resolution" to "Custom" and then lower the resolution until it is playable

You can also use [openvr_fsr](https://github.com/fholger/openvr_fsr) with this mod.

There are other demanding in-game quality settings (ranked by approximate performance impact):
* Ray Tracing (RE8 only at the moment, will need a very powerful GPU to run this at a good framerate)
* Image Quality (set this to 100% if you're not sure, lower it if it improves performance)
* Shadow Quality
* Screen Space Reflections
* Ambient Occlusion
* Subsurface Scattering

Some other ones:
* Mesh Quality

You may want to start on all low or use the "Performance Priority" preset and work your way up to acceptable settings.

The Lua scripts can have a minor impact on performance. If you don't mind playing without physical knifing and physical grenade throwing, you can remove their respective scripts from the `autorun` folder in your game directory.

Enabling AFR/AER can be done under the "VR" section of the menu.

## What graphical settings are broken?
Volumetric Lighting, Lens Flares, TAA, and Motion Blur. Will need the help of someone more experienced with shaders to fix these.

TAA has a partial fix in the latest nightly builds.

**Important Note** (This only applies to RT builds of RE2/3/7, RE8 and newer games): TAA is completely fixed in the **pd-upscaler** builds of REFramework, and performance is greatly improved with a new renderer.

This will eventually make its way into the stable builds, but you can find the **pd-upscaler** builds here, with a GitHub account: [https://github.com/praydog/REFramework/actions](https://github.com/praydog/REFramework/actions)

![upscalerbuilds](https://github.com/user-attachments/assets/f981abb3-a5d4-4e64-86fd-c97e89b8dec6)


## What graphical settings are forced?
These are forced, but the forcing can be toggled off in REFramework's menu, under VR.

* FPS, gets forced to "Variable" (uncapped)
* Antialiasing, gets forced to "None" if using any TAA variant
* Motion Blur, gets forced to "Off"
* VSync, gets forced to "Off"
* Lens Distortion, gets forced to "Off"
* Lens Flares, gets forced to "Off"
* Volumetric Lighting, gets forced to "Off"

These forced changes are not visual in the options menu, but will take effect.
