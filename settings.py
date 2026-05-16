# Display
SCREEN_W = 1280
SCREEN_H = 800
FPS = 60

# Sprites — 4x upscale from 32x32 ICO source
SPRITE_SIZE = 128

# Background zones (derived from VB6 frmSuperman.frm proportional translation)
CEILING_H = 50     # white band: y=0 to y=50
GROUND_Y = 750     # green band starts here: y=750 to y=800 (50px tall)

# Colors
# SKY_COLOR: VB6 BackColor &H00FFFF00& — OLE stores BGR, so &H00FFFF00& = R=0, G=255, B=255 = cyan
SKY_COLOR = (0, 255, 255)
CEILING_COLOR = (255, 255, 255)  # vbWhite
GROUND_COLOR = (0, 128, 0)       # vbGreen = 0x008000

# Gameplay
WIN_SCORE = 50
BEAM_SPEED = 400              # pixels per second — tunable in Phase 3
GOBLIN_BEAM_COLOR = (0, 200, 0)    # green per CMB-04
SUPERMAN_BEAM_COLOR = (200, 0, 0)  # red per CMB-04

# Direction constants (Phase 2+)
DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4
DIR_POSE = 5
DIR_IDLE = 6

# Player Movement (Phase 2)
PLAYER_SPEED_UP = 200      # px/s — rising against gravity (D-01)
PLAYER_SPEED_H = 300       # px/s — horizontal left and right (D-01)
PLAYER_SPEED_DOWN = 400    # px/s — falling with gravity (D-01)
ANIM_INTERVAL = 0.15       # seconds per animation frame (~7 Hz) (D-03)
