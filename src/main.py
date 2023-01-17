import json
import pgzrun

from player import Player
from settings import screen_width, screen_height

with open('levels.json') as levels_file:
    levels = json.load(levels_file)

WIDTH = screen_width
HEIGHT = screen_height

player = Player(WIDTH, HEIGHT)
bg_img = Actor('background')


def draw():
    """Draw the background image, the level, and the player to the screen"""
    bg_img.draw()
    player.blit(screen)


def update():
    """Update the positions and hitpoints of the player and the enemies"""
    player.update_position()


def on_key_down(key):
    """Handle keydown events"""
    if key == keys.RIGHT or key == keys.D:
        player.moving_right = True
    elif key == keys.LEFT or key == keys.A:
        player.moving_left = True
    elif key == keys.UP or key == keys.W:
        player.jumping = True

def on_key_up(key):
    """Handle keyup events"""
    if key == keys.RIGHT or key == keys.D:
        player.moving_right = False
    elif key == keys.LEFT or key == keys.A:
        player.moving_left = False
    elif key == keys.UP or key == keys.W:
        player.jumping = False


def draw_level(level):
    pass


def load_next_level():
    pass



pgzrun.go()
