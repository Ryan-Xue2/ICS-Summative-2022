import sys 
import json
import pgzrun
import settings

from boss import Boss
from guard import Guard
from player import Player
from random import randint
from constants import LEFT, RIGHT
from pgzero.builtins import images


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

# List that will store all enemy instances as well as the bullets
enemies = []
bullets = []

# Global variable cur_level keeping track which level we are currently on
cur_level = 0

# The dimensions of the game screen
WIDTH = settings.screen_width
HEIGHT = settings.screen_height

# The player instance as well as the boss
player = Player(WIDTH, HEIGHT, level_maps[cur_level], solid_rects, liquid_rects, enemies)
boss = None

# The background images
bg_img = images.background
bg_img2 = images.castle_background

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
    """
    Draw the background image, the level, the player, 
    the health bars of both the player and the boss, 
    and also the enemies and bullets to the screen
    """

    # Draw the background 
    # If its the first or last level, then draw an outside background
    # otherwise draw a background of a castle
    if cur_level == 0 or cur_level == 4:
        screen.blit(bg_img, (0, 0))
    else:
        screen.blit(bg_img2, (0, 0))
    
    # Draw the blocks in the level to the screen
    draw_level(level_maps[cur_level])

    # Draw the player to the screen
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
    max_player_hp = settings.player_hitpoints * player.health_multiplier
    for j in range(player.hitpoints, max_player_hp):
        screen.blit(empty_heart, (j*heart.get_width()+1, 0))

    # Draw the boss if they exist
    if boss is not None:
        boss.blit(screen)

        # Draw the boss bar 5 pixels down from the player's health bar
        max_boss_hp = settings.boss_hitpoints
        boss_hp = boss.hitpoints
        percent_hp = boss_hp / max_boss_hp
        bar_len = 600
        bar_width = 30

        # Draw the portion of the bar representing the remaining health in red, and the health gone in gray
        y = heart.get_height() + 5
        screen.draw.filled_rect(Rect(0, y, 
                                     bar_len*percent_hp, bar_width), (255, 0, 0)) 
        screen.draw.filled_rect(Rect(bar_len*percent_hp, y, 
                                     bar_len * (1-percent_hp), bar_width), (50, 50, 50))



def update():
    """Update the positions and hitpoints of the player and the enemies"""
    global boss
    global attacked
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
            player.hurt(settings.guard_attack_dmg)
            if player.hitpoints <= 0:
                # If player died, then restart the level
                load_level(level_maps[cur_level])
                to_remove = []
                break  # break out of the loop to avoid getting an error trying to remove things that are already removed
            to_remove.append(bullet)
    
    # Remove all the bullets that have 
    for bullet in to_remove:
        bullets.remove(bullet)
    
    # Killed all the enemies so portal opens
    if len(enemies) == 0 and boss is None:
        if portal.colliderect(player.rect):
            # Apply any buffs that are given for the completing the level
            buff = level_buffs[cur_level]
            if buff is not None:
                if buff == 'strength':
                    player.attack_multiplier = 3
                elif buff == 'health':
                    player.health_multiplier = 3
                elif buff == 'speed':
                    player.speed_multiplier = 1.3

            # Load the next level. If its the last level, then quit
            cur_level += 1
            if cur_level == len(level_maps):
                sys.exit()
            level_map = level_maps[cur_level]
            load_level(level_map)
    
    # Update the boss
    if boss is not None:
        # Attack as long as the boss is not in the middle of an attack
        # and is also not in the attack animation at the end
        if not boss.dashing and not boss.just_attacked:
            boss.dash_attack()
        else:
            # Boss is dashing, so update their x y position
            boss.update()
    
    # If player lost all their hitpoints (from boss attack), then reload the level
    if player.hitpoints <= 0:
        load_level(level_maps[cur_level])
    

def on_key_down(key):
    """Handle keydown events"""
    # Move right if d or right arrow key pressed
    if key == keys.RIGHT or key == keys.D:
        player.moving_right = True
        player.direction_facing = RIGHT
    # Move left if a or left arrow key pressed
    elif key == keys.LEFT or key == keys.A:
        player.moving_left = True
        player.direction_facing = LEFT
    # Jump if up arrow key or w key pressed
    elif key == keys.UP or key == keys.W:
        player.jumping = True


def on_key_up(key):
    """Handle keyup events"""
    # Stop moving right if right arrow key or d key lifted up
    if key == keys.RIGHT or key == keys.D:
        player.moving_right = False
    # Stop moving left if left arrow key or a key lifted up
    elif key == keys.LEFT or key == keys.A:
        player.moving_left = False
    # Stop jumping if up arrow key or w key lifted up
    elif key == keys.UP or key == keys.W:
        player.jumping = False


def on_mouse_down():
    """Attack when the player clicks the left or right mouse button"""
    global boss
    # Make player punch
    player.basic_attack()
    # If player's attack made boss' health go lower than 1, then "kill" the boss
    if boss is not None and boss.hitpoints <= 0:
        boss = None


def draw_level(level_map):
    """Draw the blocks in a level to the screen"""
    block_width, block_height = 50, 50
    for i, row in enumerate(level_map):
        for j, block in enumerate(row):
            # Calculate the x and y position of the block
            x, y = j*block_width, i*block_height

            # Get the name of the block
            block_name = blocks[block]['name']
        
            # Draw the block to the screen
            if block_name == 'dirt':
                screen.blit(dirt, (x, y))
            elif block_name == 'water':
                screen.blit(water, (x, y))
            elif block_name == 'stone':
                screen.blit(stone, (x, y))
            elif block_name == 'grass':
                screen.blit(grass, (x, y))
            elif block_name == 'stone_brick':
                screen.blit(stone_bricks, (x, y))
            # Portal is an actor, not just an image surface because we 
            # need to detect when the player enters the portal
            elif block_name == 'portal':
                portal.left = x 
                portal.top = y
                portal.draw()


def load_level(level_map):
    global boss

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
            # Get the block type and block anme
            block_type, name = blocks[block]['type'], blocks[block]['name']

            # Calculate the x y position of the block
            block_width, block_height = 50, 50
            x, y = j*block_width, i*block_height

            # Calculate rect if the block is solid and add to solid rects list
            if block_type == 'solid':
                solid_rects.append(Rect(x, y, block_width, block_height))

            # Caluclate rect if the block is liquid and add to liquid rects list
            elif block_type == 'liquid':
                liquid_rects.append(Rect(x, y, block_width, block_height))

            elif name == 'guard':
                # Create a guard, set its x y position to the block
                # and make it shoot every 2-4 seconds
                guard = Guard(player, bullets)
                guard.set_pos(x, y)
                clock.schedule_interval(guard.shoot, 2 + randint(0, 2))
                # clock.schedule_interval(guard.shoot, 0.5)
                enemies.append(guard)
            
            # Spawn the player in the correct position and reset their hp
            elif name == 'player':
                player.load_level(j*block_width, i*block_height, level_map)
            
            # Spawn the boss if there is one in the level
            elif name == 'boss':
                boss = Boss(player)
                # Make sure to add boss to the player instance so that it knows where 
                player.boss = boss  
                boss.set_pos(j*block_width, i*block_height)

                
# Load the first level into memory
load_level(level_maps[0])


# Run the game
pgzrun.go()
