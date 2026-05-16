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
PLAYER_SPEED_UP = 250      # px/s — rising against gravity
PLAYER_SPEED_H = 375       # px/s — horizontal left and right
PLAYER_SPEED_DOWN = 500    # px/s — falling with gravity
ANIM_INTERVAL = 0.15       # seconds per animation frame (~7 Hz)

# Display size for sprites (15% smaller than source PNG)
DISPLAY_SPRITE_SIZE = int(SPRITE_SIZE * 0.85)  # 108px

# Effective boundary clamp positions (derived from display sprite size)
# Ground: sprite bottom stops when 75% into ground zone (GROUND_Y to SCREEN_H)
GROUND_STOP_Y = GROUND_Y + int((SCREEN_H - GROUND_Y) * 0.75) - DISPLAY_SPRITE_SIZE
# Ceiling: sprite top stops when 75% into ceiling zone (0 to CEILING_H)
CEILING_STOP_Y = int(CEILING_H * 0.25)
