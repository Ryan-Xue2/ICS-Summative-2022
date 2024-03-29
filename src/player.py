import os
import time
import settings

from pgzero.builtins import images, Rect
from constants import HURT, LEFT, RIGHT, IDLE, WALKING, ATTACKING, JUMPING, FALLING


class Player:
    def __init__(self, screen_width, screen_height, level_map, solid_rects, liquid_rects, enemies, boss=None):
        # The width and height of the game screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Player's hitpoints and attack damage variables
        self.hitpoints = settings.player_hitpoints
        self.attack_dmg = settings.player_attack_dmg
        self.health_multiplier = 1
        self.attack_multiplier = 1

        # Player's horizontal move speed, jumping ability, and the amount of gravity applied onto them
        self.speed = settings.player_speed
        self.speed_multiplier = 1
        self.jump_power = settings.player_jump_power
        self.gravity = settings.player_gravity
        
        # The player's y movement velocity
        self.y_velocity = 0

        # Player's movement flags
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

        # Collision flags
        self.collided_bottom = False
        self.collided_left = False
        self.collided_right = False

        # An attribute to keep track of which direction the player is facing, 
        # -1 for left, and 1 for right
        self.direction_facing = RIGHT
        # Float x and y values to keep track of the location of the playerdw
        # since rects can only store integer values
        self.x = 0.0
        self.y = 0.0
        
        # Player's hitbox represented as a rect
        self.rect = images.kirby.idle.idle_right.get_rect()

        # Images of the player standing still
        self.idle_imgs = [
            'kirby/idle/idle_left',
            'kirby/idle/idle_right'
        ]
        
        # Images for the player moving left
        self.moving_left_imgs = []
        for filename in os.listdir('images/kirby/left_walk'):
            filename = filename.split('.')[0]
            # I am using .format instead of fstring to meet requirement of using string methods
            self.moving_left_imgs.append('kirby/left_walk/{}'.format(filename))
        
        # Images for the player moving right
        self.moving_right_imgs = []
        for filename in os.listdir('images/kirby/right_walk'):
            filename = filename.split('.')[0]
            self.moving_right_imgs.append(f'kirby/right_walk/{filename}')
        
        self.hurt_images = []
        for filename in os.listdir('images/kirby/hurt'):
            filename = filename.split('.')[0]
            self.hurt_images.append(f'kirby/hurt/{filename}')
        self.hurt_images.extend(self.hurt_images[:])  # Make the hurt images repeat so the animation is longer
        
        # Images of the player attacking to the left
        self.attack_left_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_left'):
            filename = filename.split('.')[0]
            self.attack_left_imgs.append(f'kirby/basic_attack_left/{filename}')
        
        # Images of the player attacking to the right
        self.attack_right_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_right'):
            filename = filename.split('.')[0]
            self.attack_right_imgs.append(f'kirby/basic_attack_right/{filename}')
        
        # Images of the player jumping to the right
        self.right_jump_imgs = []
        for filename in os.listdir('images/kirby/right_jump'):
            filename = filename.split('.')[0]
            self.right_jump_imgs.append(f'kirby/right_jump/{filename}')
        
        # Images of the player jumping to the left
        self.left_jump_imgs = []
        for filename in os.listdir('images/kirby/left_jump'):
            filename = filename.split('.')[0]
            self.left_jump_imgs.append(f'kirby/left_jump/{filename}')

        # Player's state (eg. idle, walking, jumping, etc.) and the frame of the animation
        self._state = IDLE
        self._frame = 0

        # List of rects of the solid and liquid blocks respectively in the level map
        # Will use these rects to detect and deal with collisions
        self.solid_rects = solid_rects
        self.liquid_rects = liquid_rects

        # Whether the player is in a liquid
        self.in_liquid = False

        # The map of the current level
        self.level_map = level_map

        # List of the guards
        self.enemies = enemies

        # The boss instance
        self.boss = boss

    def handle_collisions(self):
        """Deal with any collisions the player faces with """
        self.collided_bottom = False
        self.collided_right = False
        self.collided_left = False

        # TODO: To improve the collision, dont check sides that are in between two solid blocks

        for rect in self.solid_rects:
            if not self.rect.colliderect(rect):
                continue
            
            # Find the absolute distances of the player's sides to the rect's sides 
            dist_left = abs(rect.right - self.rect.left)
            dist_right = abs(rect.left - self.rect.right)
            dist_top = abs(rect.bottom - self.rect.top)
            dist_bottom = abs(rect.top - self.rect.bottom)


            # Player's left or right side hit block
            if min(dist_left, dist_right) < min(dist_top, dist_bottom):
                # Player's left side hit block
                if dist_left < dist_right:
                    self.collided_left = True
                    self.x = rect.right + 1
                    
                # Player's right side hit block
                else:
                    self.collided_right = True
                    self.x = rect.left - 1 - self.rect.width
            
            # Player's head or feet hit block
            else:
                # Player's feet hit block
                if dist_bottom < dist_top:
                    # Add 1 so that the player continues to collide and so that self.collided_bottom is 
                    # always True when it appears the player is standing
                    self.y = rect.top - self.rect.height + 1   
                    
                    self.collided_bottom = True
                    self.y_velocity = 0
                    
                # Player's head hit block
                else:
                    self.y = rect.bottom + 1
                    self.y_velocity = 0

            # Update the player's rect position
            self.rect.x = self.x
            self.rect.y = self.y
        
        # Check if kirby is in liquid and if they are then set self.in_liquid to True
        if self.rect.collidelist(self.liquid_rects) != -1:
            self.in_liquid = True
        else:
            self.in_liquid = False
    
    def update(self):
        """Move the character based on the movement flags and also handle any collisions with objects"""
        # Update the player's x and y position
        # Jump if the jump key is pressed and player is on a platform
        if self.jumping and self.collided_bottom:
            self._frame = 0  # Reset the animation frame to the first one
            # Jump but reduce jump power by 30% if the player is in a liquid
            self.y_velocity -= self.jump_power * (0.7 if self.in_liquid else 1)
        
        # Apply gravity to the y velocity if the player is in the air
        if not self.collided_bottom:
            self.y_velocity += self.gravity

        # Add y velocity value to the player's y value
        self.y += self.y_velocity

        # Move the player left or right based on the movement flags
        if self.moving_right ^ self.moving_left:
            # Calculate speed by multiplying by the multiplier and reducing speed by 50% if 
            # the player is in a liquid
            speed = self.speed * self.speed_multiplier * (0.5 if self.in_liquid else 1)

            if self.moving_left:
                self.x -= speed
            elif self.moving_right:
                self.x += speed

        # Don't let the player go thru the left or right of the screen
        # by pushing them back if they try
        if self.x < 0:
            self.x = 0
        elif self.x + self.rect.width > self.screen_width:
            self.x = self.screen_width - self.rect.width

        # Update the rect x and y position
        self.rect.x = self.x
        self.rect.y = self.y

        # Deal with any collisions with blocks
        self.handle_collisions()

        # Update the player's state
        # Don't change the state if the player is attacking, to not 
        # interrupt the attack animation
        if self._state not in [ATTACKING, HURT]:
            # Player is midair
            if not self.collided_bottom:
                if self.y_velocity > 0:
                    self._state = FALLING
                else:
                    self._state = JUMPING
            # Player is moving left xor moving right
            elif self.moving_left ^ self.moving_right:
                self._state = WALKING
            # Player isn't moving
            else:
                self._state = IDLE

    def basic_attack(self):
        """Punch and deal damage to any enemies in range of the attack"""
        # Set the player's state to attacking
        # and also reset the animation frame back to 0
        self._state = ATTACKING
        self._frame = 0

        attack_range = 10

        # Player is facing left
        if self.direction_facing == LEFT:
            attack_rect = Rect(
                self.x, self.y, 
                attack_range, self.rect.height)
        # Player is facing right
        else:
            attack_rect = Rect(
                self.x+self.rect.width, self.y, 
                attack_range, self.rect.height)

        # Deal damage to any enemies in the player's attack box
        to_remove = []
        for enemy in self.enemies:
            if enemy.rect.colliderect(attack_rect):
                enemy.hurt = True
                enemy.hitpoints -= self.attack_dmg * self.attack_multiplier
                if enemy.hitpoints <= 0:
                    to_remove.append(enemy)

        # Remove enemies who have lost all their hitpoints from the list
        for enemy in to_remove:
            self.enemies.remove(enemy)
        
        # Deal damage to boss if they are in attack rect
        if self.boss is not None:
            if self.boss.rect.colliderect(attack_rect):
                self.boss.hitpoints -= self.attack_dmg * self.attack_multiplier

    def hurt(self, damage):
        """Set kirby's state to hurt, and deal damage to kirby"""
        self._state = HURT
        self._frame = 0
        self.hitpoints -= damage
    
    def load_level(self, spawn_x, spawn_y, level_map):
        """
        Resets the player's hitpoints and sets the player's position to 
        the specified position. Also updates the level map. Doesn't
        need to update the solid and liquid rects because those are changed
        in the load_level function in main.py.
        """
        self.hitpoints = settings.player_hitpoints * self.health_multiplier
        self.x = spawn_x
        self.y = spawn_y
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.level_map = level_map

    def blit(self, screen):
        """Draw the player to the screen, with the correct animations"""
        image = None

        # The player is attacking
        if self._state == ATTACKING:
            if self.direction_facing == LEFT:
                image = self.attack_left_imgs[self._frame]
            else:
                image = self.attack_right_imgs[self._frame]

            # If the frame is the last one in the attack animation, then
            # stop the animation and set the player's state to the correct state
            if self._frame == len(self.attack_left_imgs) - 1:
                if self.collided_bottom:
                    self._state = WALKING if self.moving_left ^ self.moving_right else IDLE
                elif self.y_velocity > 0:
                    self._state = FALLING
                else:
                    self._state = JUMPING
                self._frame = 0

        # The player is idle
        elif self._state == IDLE:
            if self.direction_facing == LEFT:
                image = self.idle_imgs[0]
            else:
                image = self.idle_imgs[1]

        # The player is moving
        elif self._state == WALKING:
            sz = len(self.moving_left_imgs)
            if self.direction_facing == LEFT:
                image = self.moving_left_imgs[self._frame % sz]
            elif self.direction_facing == RIGHT:
                image = self.moving_right_imgs[self._frame % sz]

        # The player is jumping in the air (midair and y velocity is negative)
        elif self._state == JUMPING:
            if self._frame > 2:
                if self.direction_facing == LEFT:
                    image = self.left_jump_imgs[2]
                else:
                    image = self.right_jump_imgs[2]
            elif self.direction_facing == LEFT:
                image = self.left_jump_imgs[self._frame]
            else:
                image = self.right_jump_imgs[self._frame]
        
        # The player is midair and y velocity > 0
        elif self._state == FALLING:
            if self.direction_facing == LEFT:
                image = self.left_jump_imgs[-1]
            else:
                image = self.right_jump_imgs[-1]

        # The player is hurt
        elif self._state == HURT:
            image = self.hurt_images[self._frame]
            
            # If the frame is the last one in the animation images
            if self._frame == len(self.hurt_images) - 1:
                # Calculate what state kirby should be in next
                if self.collided_bottom:
                    self._state = WALKING if self.moving_left ^ self.moving_right else IDLE
                elif self.y_velocity > 0:
                    self._state = FALLING
                else:
                    self._state = JUMPING
                # Reset the animation frame back to 0
                self._frame = 0

        self._frame += 1  # Go to the next animation frame
        screen.blit(image, self.rect)