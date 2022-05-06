Here you'll find various solutions and FAQ to various problems you may encounter with the VR mod.

[Getting Started Guide](https://beastsaber.notion.site/beastsaber/Praydog-s-Resident-Evil-2-3-VR-mod-3db8bd110ebf4a38870e1a5114b16998)

Newer builds can be found [here](https://github.com/praydog/REFramework-nightly/releases/)

## Reporting a bug
Report it on the [Issues](https://github.com/praydog/REFramework/issues) page.

If you are crashing, or are having a technical problem then upload these files from your game folder:
* `re2_framework_log.txt`
* `reframework_crash.dmp` if you are crashing

If you do not have an `reframework_crash.dmp` and are crashing, download a newer build, links at the top of the page.

## Opening the in-game menu with motion controllers (OpenVR only right now)
Aim at the palm of your left hand with your head and your right hand. Do not press anything, and an overlay menu should show up.

If that doesn't work, you can use the desktop version of the menu using the Insert key. This method won't work in the headset.

If that still doesn't work, options can be changed in the `re2_fw_config.txt` in your game directory.

## Switching to OpenXR
By default, REFramework uses OpenVR for the VR functionality. In some cases, switching to OpenXR can increase performance anywhere from slightly, to a significant amount.

To switch to OpenXR, simply delete the `openvr_api.dll` that came with the zip file. Make sure the `openxr_loader.dll` that came with the mod is present in the game folder.

## OpenXR Pitfalls
* There is no wrist overlay for modifying VR settings yet
* Modifying controller bindings is not as expressive as OpenVR
* Personally only tested on Oculus Quest 2 and CV1, reports that it works on Reverb G2

## Common fixes
* Restarting SteamVR
* Disabling overlay software
* Disabling SteamVR theater
* Disabling "Hardware-accelerated GPU scheduling"
   * This **MUST** be disabled if you are getting extremely low frames
* Swapping between DX11 and DX12
* Taking the headset off and putting it back on
* If you are using an HDR monitor, unplugging the monitor temporarily has been a reported fix
* If your screen looks squished with black bars turn off Borderless window mode
* Make sure no graphical settings are being forced globally (e.g. from Nvidia Control Panel)
    * The exception to this is disabling HDR which is required or else the game will not display within the headset

### In RE2
There is a known issue of a softlock sometimes occurring in the Birkin fight if it goes on too long. It can be fixed simply by disabling FirstPerson until he spawns again.

## What is the status of RE7 and RE8?
RE7 and RE8 are fully 6DOF and playable with a gamepad, but with a few caveats:
* RE7 has no motion controls at the moment
* RE8's motion controls are in an experimental and incomplete state
* There is no full body IK yet like RE2/RE3
* ~~The audio positioning will not match up with your HMD rotation~~ **fixed in a recent update**
* You cannot aim with your head yet

You've been warned!

## What about the others like DMC5 and MHRise?
They are both fully 6DOF but with the least support.

~~They have the same issue of audio positioning being incorrect~~ **only in MHRise now**.

~~DMC5 has some issues with some incorrect UI elements.~~ Fixed in a recent update.

## Gameplay
RE2 and RE3:
* Motion controller support
* Head-based movement
* Smooth locomotion
* Smooth turning
* Mostly right-handed

Playing with a gamepad is supported. IK gets disabled when using one.

## Bindings
Bindings can be changed in SteamVR's controller bindings section.

Known working default bindings:
* Oculus Touch
* Valve Index Knuckles

Needs additional testing:
* Vive Wands

If a set of controllers don't work as expected, they can be set up in the SteamVR controller bindings.

## Performance
One of the most taxing parts of these mods is the **resolution** you have set. The in-game resolution has no effect, it must be changed in SteamVR.

To modify the resolution in your headset:
* Open the SteamVR overlay
* Click on the cogwheel on the bottom right
* Click on "Video"
* Change "Render Resolution" to "Custom" and then lower the resolution until it is playable

You can also use [openvr_fsr](https://github.com/fholger/openvr_fsr) with this mod.

There are other demanding in-game quality settings (ranked by approximate performance impact):
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
