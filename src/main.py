import json
import pgzrun

from pgzero.builtins import images

from player import Player
from settings import screen_width, screen_height


# Load the level maps, and the ids and their corresponding block
# Addtionally, load in what the rewards/buffs the player
# receives at the end of the level are  
with open('levels.json') as levels_file:
    levels = json.load(levels_file)
    blocks = levels['block_ids']
    blocks = {int(key): value for key, value in blocks.items()}
    level_maps = levels['level_maps']

# Rects that will store the rects of the solids and the liquids that the
# player might collide with
solid_rects = []
liquid_rects = []

# Global variable cur_level keeping track which level we are currently on
cur_level = 0

# Load the first level into memory
# load_level()

# The dimensions of the game screen
WIDTH = screen_width
HEIGHT = screen_height

# Player class and the actor for the background
player = Player(WIDTH, HEIGHT)
bg_img = Actor('background')


def draw():
    """Draw the background image, the level, and the player to the screen"""
    bg_img.draw()
    draw_level(level_maps[cur_level])
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
    """Draw the blocks in a level to the screen"""
    dirt = images.dirt
    grass = images.grass
    stone = images.stone
    water = images.water
    stone_bricks = images.stone_bricks

    block_width, block_height = 50, 50
    for i, row in enumerate(level_map):
        for j, block in enumerate(row):
            x, y = j*block_width, i*block_height
            block_name = blocks[block]['name']
            if block_name == 'dirt':
                screen.blit(dirt, (x, y))
            elif block_name == 'water':
                screen.blit(water, (x, y))
            elif block_name == 'stone':
                screen.blit(stone, (x, y))
            elif block_name == 'grass':
                screen.blit(grass, (x, y))
            elif block_name == 'stone_bricks':
                screen.blit(stone_bricks, (x, y))
            

def load_level():
    """Load a level into memory, loading the collision rects, etc."""
    pass



pgzrun.go()
