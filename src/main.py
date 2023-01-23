import sys 
import json
import time
import pgzrun

from guard import Guard
from player import Player
from random import randint
from constants import HURT, LEFT, RIGHT
from pgzero.builtins import images
from settings import screen_width, screen_height, player_hitpoints


# Load the level maps, and the ids and their corresponding block
# Addtionally, load in what the rewards/buffs the player
# receives at the end of the level are  
with open('levels.json') as levels_file:
    levels = json.load(levels_file)
    blocks = levels['block_ids']
    blocks = {int(key): value for key, value in blocks.items()}
    level_buffs = levels['level_buffs']
    level_maps = levels['level_maps']

# Rects that will store the rects of the solids and the liquids that the
# player might collide with
solid_rects = []
liquid_rects = []
bullets = []
# List that will store all enemy instances
enemies = []

# Global variable cur_level keeping track which level we are currently on
cur_level = 0

# The dimensions of the game screen
WIDTH = screen_width
HEIGHT = screen_height

# Player class and the background image
player = Player(WIDTH, HEIGHT, level_maps[0], solid_rects, liquid_rects, enemies)
bg_img = images.background

# Load all the images into memory
# Block images
dirt = images.blocks.dirt
grass = images.blocks.grass
stone = images.blocks.stone
water = images.blocks.water
stone_bricks = images.blocks.stone_bricks
portal = Actor('blocks/portal')

# Health image
heart = images.heart
empty_heart = images.empty_heart


def draw():
    """Draw the background image, the level, and the player to the screen"""
    screen.blit(bg_img, (0, 0))
    draw_level(level_maps[cur_level])
    player.blit(screen)

    # Draw enemies to the screen
    for enemy in enemies:
        enemy.blit(screen)

    # Draw bullets to the screen
    for bullet in bullets:
        bullet.draw()

    # Draw hearts representing player's health
    for i in range(player.hitpoints):
        screen.blit(heart, (i*heart.get_width()+1, 0))

    # Draw empty hearts to the screen representing the hitpoints
    # that the player has lost
    for j in range(player.hitpoints, player_hitpoints * player.health_multiplier):
        screen.blit(empty_heart, (j*heart.get_width()+1, 0))
        
    # time.sleep(0.1)


def update():
    """Update the positions and hitpoints of the player and the enemies"""
    global cur_level

    player.update()  # Update the player's position, state, etc

    # Update the enemies
    for enemy in enemies:
        enemy.update()

    to_remove = []
    for bullet in bullets:
        bullet.update()
        # Bullet flew out the left or right
        if bullet.actor.right < 0 or bullet.actor.x > WIDTH:
            to_remove.append(bullet)
        # Bullet flew out the top or bottom
        elif bullet.actor.y > HEIGHT or bullet.actor.right < 0:
            to_remove.append(bullet)
        # The bullet hit a block
        elif bullet.actor.collidelist(solid_rects) != -1:
            to_remove.append(bullet)
        # The bullet hit the player
        elif bullet.actor.colliderect(player.rect):
            # Remove health from the player
            player.hitpoints -= 1
            player._state = HURT
            player._frame = 0
            if player.hitpoints <= 0:
                print('dead')
            to_remove.append(bullet)

    for bullet in to_remove:
        bullets.remove(bullet)
    
    if len(enemies) == 0:
        if portal.colliderect(player.rect):
            buff = level_buffs[cur_level]
            if buff is not None:
                if buff == 'strength':
                    player.attack_multiplier = 3
                elif buff == 'health':
                    player.health_multiplier = 3
                elif buff == 'speed':
                    player.speed_multiplier = 1.3

            cur_level += 1
            if cur_level == len(level_maps):
                print('No more levels')
                print(cur_level)
                sys.exit()
            level_map = level_maps[cur_level]
            load_level(level_map)
            
    

def on_key_down(key):
    """Handle keydown events"""
    if key == keys.RIGHT or key == keys.D:
        player.moving_right = True
        player.direction_facing = RIGHT
    elif key == keys.LEFT or key == keys.A:
        player.moving_left = True
        player.direction_facing = LEFT
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
    """Attack when the player clicks the left or right mouse button"""
    player.basic_attack()


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
                # screen.blit(portal, (x, y))
                portal.left = x 
                portal.top = y
                portal.draw()


def load_level(level_map):
    """Load a level into memory, loading the collision rects, etc."""
    # Clear the lists holding the solid and liquid rects, as well as the enemies
    # and the bullets
    # This will clear all the references to these lists as well, so the lists in the 
    # player instance will not need to be changed, since those are the same object
    solid_rects.clear()
    liquid_rects.clear()
    bullets.clear()
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
                # Create a guard, set its x y position to the block
                # and make it shoot every 2-4 seconds
                guard = Guard(player, bullets)
                guard.set_pos(x, y)
                clock.schedule_interval(guard.shoot, 2 + randint(0, 2))
                # clock.schedule_interval(guard.shoot, 0.5)
                enemies.append(guard)
            elif name == 'player':
                player.load_level(j*50, i*50, level_map)

                
# Load the first level into memory
load_level(level_maps[0])


# Run the game
pgzrun.go()
