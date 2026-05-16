import pygame
from enum import Enum, auto
from settings import (
    SCREEN_W, SCREEN_H, SPRITE_SIZE, DISPLAY_SPRITE_SIZE,
    CEILING_STOP_Y, GROUND_STOP_Y,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_IDLE,
    PLAYER_SPEED_UP, PLAYER_SPEED_H, PLAYER_SPEED_DOWN, ANIM_INTERVAL,
)


class CharState(Enum):
    ALIVE = auto()
    CRASHING = auto()
    DEAD = auto()
    POSING = auto()
    RESPAWNING = auto()


class Player:
    """One playable character: Superman or Goblin.

    Parameterised by ``character`` ("superman" or "goblin").  All sprite keys,
    key bindings, and starting positions are driven by class-level tables so
    both characters share a single code path.

    Usage (from game.py)::

        players = [Player("superman", assets), Player("goblin", assets)]
        # each frame:
        keys = pygame.key.get_pressed()
        for p in players:
            p.update(dt, keys)
            p.draw(screen)

    Phase 3 beam collision MUST use:
        if beam.direction in (DIR_LEFT, DIR_RIGHT):
    NEVER write:
        beam.direction == DIR_LEFT or DIR_RIGHT  # VB6 Or-bug — always True for truthy DIR_RIGHT
    """

    # ------------------------------------------------------------------ #
    # Class-level sprite / control tables                                 #
    # ------------------------------------------------------------------ #

    _CONTROLS: dict = {
        "superman": {
            DIR_UP:    pygame.K_UP,
            DIR_DOWN:  pygame.K_DOWN,
            DIR_LEFT:  pygame.K_LEFT,
            DIR_RIGHT: pygame.K_RIGHT,
        },
        "goblin": {
            DIR_UP:    pygame.K_w,
            DIR_DOWN:  pygame.K_s,
            DIR_LEFT:  pygame.K_a,
            DIR_RIGHT: pygame.K_d,
        },
    }

    _AIR_SPRITES: dict = {
        "superman": {
            DIR_UP:    ("sup1",    "sup2"),
            DIR_DOWN:  ("sdown1",  "sdown2"),
            DIR_LEFT:  ("sleft1",  "sleft2"),
            DIR_RIGHT: ("sright1", "sright2"),
            DIR_IDLE:  ("superman", "superman"),
        },
        "goblin": {
            DIR_UP:    ("gup1",   "gup2"),
            DIR_DOWN:  ("gdown1", "gdown2"),
            DIR_LEFT:  ("gleft1", "gleft2"),
            DIR_RIGHT: ("gright1","gright2"),
            DIR_IDLE:  ("gevil",  "gevil"),
        },
    }

    # 4-step walk cycle: index into _GROUND_WALK_SPRITES list.
    # Produces 1->2->1->3 (0-indexed: 0->1->0->2) as per D-10.
    _GROUND_WALK_CYCLE: list = [0, 1, 0, 2]

    _GROUND_WALK_SPRITES: dict = {
        "superman": ["ckent1", "ckent2", "ckent3"],
        "goblin":   ["gevil1", "gevil2", "gevil3"],
    }

    _GROUND_IDLE_SPRITE: dict = {
        "superman": "ckent",
        "goblin":   "gevil",
    }

    # ------------------------------------------------------------------ #
    # Lifecycle                                                            #
    # ------------------------------------------------------------------ #

    def __init__(self, character: str, assets) -> None:
        self.character = character
        self.assets = assets
        self.state = CharState.ALIVE

        # Starting positions — characters face each other at game start.
        # self.facing: last non-idle direction — used by Phase 3 beam firing.
        # Phase 3 collision check MUST use: if beam.direction in (LEFT, RIGHT):
        # NEVER write: beam.direction == LEFT or RIGHT  (VB6 Or-bug — always True for truthy RIGHT)
        if character == "superman":
            self.x = float(SCREEN_W * 0.75)
            self.facing = DIR_LEFT
        else:
            self.x = float(SCREEN_W * 0.25)
            self.facing = DIR_RIGHT

        self.y = float(SCREEN_H // 2)

        # Animation state
        self._anim_timer: float = 0.0
        self._anim_frame: int = 0
        self._ground_walk_step: int = 0

        # Cached draw state (updated each update() call)
        self._direction: int = DIR_IDLE
        self._on_ground: bool = False
        self._moving_h: bool = False

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def rect(self) -> pygame.Rect:
        """Axis-aligned bounding rect — used by Phase 3 beam collision."""
        return pygame.Rect(int(self.x), int(self.y), DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE)

    # ------------------------------------------------------------------ #
    # Update                                                               #
    # ------------------------------------------------------------------ #

    def update(self, dt: float, keys) -> None:
        """Advance player by *dt* seconds given current keyboard state *keys*.

        *keys* is the return value of ``pygame.key.get_pressed()`` supplied by
        the caller (game.py) — player.py never calls get_pressed() itself (MOV-03).
        """
        if self.state != CharState.ALIVE:
            return

        # Step 1 — determine on_ground before movement
        on_ground = self.y >= GROUND_STOP_Y

        # Step 2 — compute dx, dy, direction
        dx = 0.0
        dy = 0.0
        direction = DIR_IDLE
        ctrl = self._CONTROLS[self.character]

        # Horizontal (elif — only one direction per frame)
        if keys[ctrl[DIR_LEFT]]:
            dx = -PLAYER_SPEED_H * dt
            direction = DIR_LEFT
            self.facing = DIR_LEFT
        elif keys[ctrl[DIR_RIGHT]]:
            dx = PLAYER_SPEED_H * dt
            direction = DIR_RIGHT
            self.facing = DIR_RIGHT

        # Vertical (only sets direction/facing if no horizontal key held)
        if keys[ctrl[DIR_UP]]:
            dy = -PLAYER_SPEED_UP * dt
            if direction == DIR_IDLE:
                direction = DIR_UP
                self.facing = DIR_UP
        elif keys[ctrl[DIR_DOWN]] and not on_ground:
            # D-11: down key suppressed on ground — visual floor only, not a state change
            dy = PLAYER_SPEED_DOWN * dt
            if direction == DIR_IDLE:
                direction = DIR_DOWN
                self.facing = DIR_DOWN

        # Step 3 — apply movement
        self.x += dx
        self.y += dy

        # Step 4 — horizontal wrap (MOV-04)
        if self.x < -DISPLAY_SPRITE_SIZE:
            self.x = SCREEN_W
        elif self.x > SCREEN_W:
            self.x = -DISPLAY_SPRITE_SIZE

        # Step 5 — vertical clamp
        if self.y < CEILING_STOP_Y:   # MOV-06: ceiling (top 75% into cloud zone)
            self.y = CEILING_STOP_Y
        if self.y > GROUND_STOP_Y:    # MOV-05: ground (bottom 75% into ground zone)
            self.y = GROUND_STOP_Y

        # Step 6 — re-compute on_ground after clamp
        on_ground = self.y >= GROUND_STOP_Y

        # Step 7 — animation timer
        self._anim_timer += dt
        if self._anim_timer >= ANIM_INTERVAL:
            self._anim_timer -= ANIM_INTERVAL        # preserve sub-interval remainder
            self._anim_frame = 1 - self._anim_frame  # toggle 0 <-> 1
            if on_ground and dx != 0:
                self._ground_walk_step = (self._ground_walk_step + 1) % 4

        # Step 8 — cache draw state
        self._direction = direction
        self._on_ground = on_ground
        self._moving_h = (dx != 0)

    # ------------------------------------------------------------------ #
    # Draw                                                                 #
    # ------------------------------------------------------------------ #

    def draw(self, screen: pygame.Surface) -> None:
        """Blit the current animation frame onto *screen*."""
        key = self._get_sprite_key()
        surf = pygame.transform.scale(self.assets.sprites[key], (DISPLAY_SPRITE_SIZE, DISPLAY_SPRITE_SIZE))
        screen.blit(surf, (int(self.x), int(self.y)))

    def _get_sprite_key(self) -> str:
        """Return the correct sprite key for the current movement/ground state."""
        if self._on_ground:
            if self._moving_h:
                idx = self._GROUND_WALK_CYCLE[self._ground_walk_step]
                return self._GROUND_WALK_SPRITES[self.character][idx]
            else:
                return self._GROUND_IDLE_SPRITE[self.character]
        else:
            frames = self._AIR_SPRITES[self.character][self._direction]
            return frames[self._anim_frame]
