# EasySetup_for_renpy — Easy Ren'Py Setup

[中文版](README.md)

A convenient tool to make Ren'Py easier for beginners, providing simple custom statements and automatic character registration.

## Features

- Custom statements: shake, move, show_at, combo statements with natural-language-like syntax
- Automatic sprite registration: filename keyword matching via expression_map, falls back to default when no matching file found
- Automatic side image registration: just place images in the correct directory
- Fully adjustable parameters: shake duration, amplitude, move time, xy coordinates, etc.
- Modular: statements organized by type in separate files; core dependencies can be extracted independently
- Built-in weather effects with zero external assets: implemented purely with Ren'Py built-in features
- Simplified main menu customization: just replace the corresponding files

## Quick Start

1. Download `renpy` and `vscode`

2. Install the official Ren'Py plugin, then drag this project into `vscode`

3. Read through `README.md` for quick configuration, `understand the licenses of this project and its dependencies`

4. Edit `script.rpy`:

```renpy
label start:
    show_at ch to_center  # Show new character ch at center
    ch "Hello!"            # ch says hello
    ch h "Happy"           # ch speaks with h(appy) expression
    shake_x ch             # Shake along X axis
    move ch to_right       # Move ch to the right, default 0.5s
    return                 # Return to main menu
```

5. Open `renpy` and run

## Character Registration

### Asset Directory Structure
- Suppose your character asset folder is named `characters`, character name `ch1`

```
characters/ch1/
├── ch1.png              ← Default sprite
├── ch1_happy.png        ← Expression variant
├── ch1_angry.png
├── ...
└── side/
    ├── ch1.png          ← Default side image
    ├── ch1_happy.png
    ├── ch1_angry.png
    └── ...
```

### Configure Expression Mapping

```renpy
# 0_config.rpy
expression_map = {
    "normal": "n",
    "angry": "a",
    "happy": "h",
    "shy": "s",
    "frown": "f",
    "frown_mouth": "fm",
    "sad": "sd",
    "surprise": "sp",
    "cry": "c",
    "upset": "ut",
}
```
- You can modify the presets in `0_config.rpy`

### Register a Character

```renpy
# Write in character_definition.rpy

# Helper config to handle height issues, ignoring sprite size inconsistencies and hat height offsets
# Note: format is "image_tag": {"cm": xxx, "hat": xxx}
python early:
    character_zoom.update({
        "ch11111": {"cm": 160, "hat": 200}, 
    })

# Register character
# See 0_config.rpy for detailed parameters
define ch = new({
    "name": "Character 1",       # Display name
    "image_tag": "ch11111",      # Image tag for this character
    "file": "../characters/ch1/",# Asset path
    "side": True,                # Has side image
})
```

## Custom Statements

- Expressions are optional — defaults to the last used expression
- Remember to use the character's `define` name (e.g., `ch` above), not the image_tag

### Shake

```renpy
shake_x character [expression] [duration] [amplitude]       Hides dialogue window
shake_y character [expression] [duration] [amplitude]
say_shake_x character [expression] "text" [duration] [amplitude]  Normal dialogue window
say_shake_y character [expression] "text" [duration] [amplitude]
```

### Move

```renpy
move character [expression] to_xxx [duration]
move character [expression] x y [duration]
say_move character [expression] "text" to_xxx [duration]
say_move character [expression] "text" x y [duration]
show_at character [expression] to_xxx [dissolve duration]
show_at character [expression] x y [dissolve duration]
```

### Combo

```renpy
shake_move character [expression] [x|y] to_xxx    Shake then move
move_shake character [expression] [x|y] to_xxx    Move then shake
say_shake_move character [expression] "text" [x|y] to_xxx
say_move_shake character [expression] "text" [x|y] to_xxx
```

## Adjustable Parameters

Defined in the `python early:` block of `0_config.rpy`:

| Variable             | Default     | Description                          |
| -------------------- | ----------- | ------------------------------------ |
| `shake_total`        | 0.48        | Total shake duration (seconds)       |
| `shake_offset`       | 12          | Shake amplitude (pixels)             |
| `move_dur`           | 0.5         | Move duration (seconds)              |
| `start_pos`          | (0.5, -1.0) | Initial character position           |
| `dissolve_dur`       | 0.3         | Show_at fade-in duration (seconds)   |
| `combo_move_dur`     | 0.5         | Combo move duration (seconds)        |
| `combo_shake_total`  | 0.48        | Combo shake total duration (seconds) |
| `combo_shake_offset` | 12          | Combo shake amplitude (pixels)       |
| `side_size`          | 273         | Side image size (pixels)            |
| `ppm`                | 7.5         | Pixels per centimeter                |
| `base_room`          | 0.6         | Sprite scaling fallback ratio        |
| `base_align`         | (0.5, 1.0)  | Default anchor point                 |

## File Structure

```
game/
├── 0_config.rpy                Global parameters
├── character_definition.rpy    Character definitions
├── function/
│   ├── anims.rpy               Animation classes
│   ├── register_api.rpy        Registration API
│   ├── shake/                  Shake statements
│   ├── move/                   Move/position statements
│   ├── combo/                  Combo statements
│   └── weather.rpy             Weather effects
├── script.rpy                  Main script
└── ...
characters/ch1/
├── ch1.png
└── side/
    └── ch1.png
```

## License

### Framework

Apache 2.0

### Font

Source Han Sans SC (思源黑体)
© 2014-2025 Adobe. Source is a trademark of Adobe in the United States and/or other countries.
[SIL Open Font License 1.1](https://github.com/adobe-fonts/source-han-sans)
Full license text available at `game/fonts/OFL.txt`

### Engine

Built on [Ren'Py](https://www.renpy.org/)
Ren'Py Visual Novel Engine © 2004-2024 Tom Rothamel
MIT License · Full license terms:
https://www.renpy.org/doc/html/license.html