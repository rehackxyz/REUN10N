Solved by: @OS1R1S

### Question:
We made a game.

### Solution:
1. Use [GDRETools](https://github.com/GDRETools/gdsdecomp) to decompile Godot 
2. Flag is found at `script/player.gd`

```gdscript 
@onready var cam = $Camera3D
@onready var footstep = $footsteps
var flag = "KashiCTF{N07_1N_7H3_G4M3}"  # Get the footstep audio

var gravity = 20.0

func _ready():
    print(flag)
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
```

**Flag:** `KashiCTF{N07_1N_7H3_G4M3}`

