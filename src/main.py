import json
import pgzrun

from pgzero.builtins import images

from player import Player
from settings import screen_width, screen_height


with open('levels.json') as levels_file:
    levels = json.load(levels_file)
    block_ids = levels['block_ids']
    levels = levels['level_maps']

print(block_ids)

WIDTH = screen_width
HEIGHT = screen_height

player = Player(WIDTH, HEIGHT)
bg_img = Actor('background')


def draw():
    """Draw the background image, the level, and the player to the screen"""
    bg_img.draw()
    draw_level(levels[0])
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

def draw_level(level_map):
    dirt = images.dirt
    grass = images.grass
    stone = images.stone
    stone_bricks = images.stone_bricks
    water = images.water
    print(dir(dirt))

    for i, row in enumerate(level_map):
        for j, block in enumerate(row):
            if block_ids[str(block)]['name'] == 'dirt':
                screen.blit(dirt, (j*50, i*50))
            elif block_ids[str(block)]['name'] == 'water':
                screen.blit(water, (j*50, i*50))
            elif block_ids[str(block)]['name'] == 'stone':
                screen.blit(stone, (j*50, i*50))
            elif block_ids[str(block)]['name'] == 'grass':
                screen.blit(grass, (j*50, i*50))

def load_next_level():
    pass



pgzrun.go()
