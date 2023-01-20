import json
import pgzrun

from pgzero.builtins import images

from player import Player
from guard import Guard
from settings import screen_width, screen_height


def load_level(level_map):
    """Load a level into memory, loading the collision rects, etc."""
    # Clear the lists holding the solid and liquid rects, as well as the enemies
    # This will clear all the references to these lists as well, so the lists in the 
    # player instance will not need to be changed, since those are the same object
    solid_rects.clear()
    liquid_rects.clear()
    enemies.clear()

    for i, row in enumerate(level_map):
        for j, block in enumerate(row):
            block_type, name = blocks[block]['type'], blocks[block]['name']
            block_width, block_height = 50, 50
            x, y = j*block_width, i*block_height

            if block_type == 'solid':
                solid_rects.append(Rect(x, y, block_width, block_height))
            elif block_type == 'liquid':
                liquid_rects.append(Rect(x, y, block_width, block_height))
            elif name in ['guard', 'boss']:
                guard = Guard()
                guard.set_pos(x, y)
                enemies.append(guard)
            elif name == 'player':
                player.load_level(j*50, i*50)

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

# List that will store all enemy instances
enemies = []

# Global variable cur_level keeping track which level we are currently on
cur_level = 0

# The dimensions of the game screen
WIDTH = screen_width
HEIGHT = screen_height

# Player class and the actor for the background
player = Player(WIDTH, HEIGHT, solid_rects, liquid_rects, enemies)
bg_img = images.background

# Load the first level into memory
load_level(level_maps[0])

# Load all the images into memory
dirt = images.blocks.dirt
grass = images.blocks.grass
stone = images.blocks.stone
water = images.blocks.water
stone_bricks = images.blocks.stone_bricks
portal = images.blocks.portal

# rects

def draw():
    """Draw the background image, the level, and the player to the screen"""
    screen.blit(bg_img, (0, 0))
    draw_level(level_maps[cur_level])
    player.blit(screen)
    for enemy in enemies:
        enemy.blit(screen)


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


def on_mouse_down():
    player.attack()


def draw_level(level_map):
    """Draw the blocks in a level to the screen"""

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
            elif block_name == 'portal':
                screen.blit(portal, (x, y))

pgzrun.go()
