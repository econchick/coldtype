# Changelog

Starting at 0.5.0, all notable changes to Coldtype will be described here (briefly). Edit: looks like I forgot this existed, so we're starting again at 0.5.16

## [0.5.0] - 2021-06-02
### Added
- `coldtype.fx.skia`
- `SkiaImage` (subclass of `DATImage`, which has been moved to `coldtype.img` module)
### Removed
- `.phototype`/`.color_phototype` methods on `DATPen` — these are now "chainable" methods in the _coldtype.fx.skia_ module, and can be applied by importing ala `from coldtype.fx.skia import phototype` and then chaining to a pen, `.ch(phototype(...))`

## [0.5.16] - 2021-08-03
### Added
- Minor improvements to the self-rasterizing/drawbot-renderer, to support transparent backgrounds
### Removed
- `@drawbot_script` and `@drawbot_animation` from the global import; now reside and can be imported from `coldtype.drawbot` module

## [0.5.17] - 2021-08-06
### Fixed
- Quoting paths in `blend_frame`
### Removed
- `unicodedata2` from primary installation requirements, in order to make blender installation smoother (i.e. not require Include header-copying from python source tarball) — thanks @colinmford!

## [0.6.0] - 2021-08-30
### Added
- New features for managing meshes in BlenderPen
- embedded profiles, so `-p b3d` should now work globally
### Removed
- `duration` keyword for `@animation`, since it’s redundant to `timeline=<int>` shortcut

## [0.6.1] - 2021-08-31
### Added
- Support for `kp` and `tu` in `Glyphwise`

## [0.6.2] - 2021-09-01
### Added
- Support for single-char `Glyphwise`
- `Glyphwise` now returns `DATPens`, not `DraftingPens`

## [0.6.3] - 2021-09-07
### Added
- Support for multi-return styler fn for `Glyphwise`
- Coldtype panel for `@b3d_sequencer`

## [0.6.6] - 2021-09-10
### Added
- Better MIDI primitives
- `coldtype midi` midi viewer

## [0.6.8] - 2021-09-16
### Added
- Better axidraw primitives in new `coldtype.axidraw` namespace, demonstrated in `test/visuals/test_axidraw.png`
- New `numpad` special variable that can handle up to 9 special actions, triggerable from the numpad with the viewer enabled
### Removed
- Dependency on `PyOpenGL-accelerate` in the `[viewer]` extra — not really sure why that was there to begin with.

## [0.6.9] - 2021-09-20
### Added
- Restored some audio capabilities, via `audio=` keywords and the new `ConfigOption.EnableAudio`/`KeyboardShortcut.EnableAudio`

## [0.7.0] - 2021-09-26
### Fixed
- General tidying, particularly for use in `[notebook]`
### Removed
- Dependency on `noise` in `[viewer]`

## [0.7.1] - 2021-09-28
### Added
- Support for configurable `BLENDER_APP_PATH`
- Better support for Windows-Blender workflow

## [0.7.2] - 2021-09-29
### Added
- Support for gif export in `@notebook_animation.show`

## [0.7.3] - 2021-10-07
### Added
- `strip=` kwarg on StSt (defaulting to `True`) so incoming text is automatically stripped (but can be overriden as in the `Glyphwise` use of `StSt`)
- `coldtype.blender.fluent` experimental chainable interface for direct manipulation of blender objects

## [0.7.4] - 2021-10-21
### Added
- Support for lineTo's in `distribute_on_path`
- More `coldtype.blender.fluent` interface
- Ability to exit from renderer with -1 in `prenormalize_filepath`

## [0.7.5] - 2021-10-25
### Added
- `@ui` decorator idea, to be used/tested in Goodhertz plugin-builder