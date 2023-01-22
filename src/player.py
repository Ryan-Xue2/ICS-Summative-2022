import os
import settings

from constants import LEFT, RIGHT, IDLE, WALKING, ATTACKING
from pgzero.builtins import images, Rect


class Player:
    def __init__(self, screen_width, screen_height, level_map, solid_rects, liquid_rects, enemies):
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
        self.jump_power = settings.player_jump_power
        self.gravity = settings.player_gravity
        
        # The player's y movement velocity
        self.y_velocity = 0

        # Player's movement flags
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.collided_bottom = False
        self.collided_left = False
        self.collided_right = False

        # An attribute to keep track of which direction the player is facing, 
        # -1 for left, and 1 for right
        self.direction_facing = RIGHT
        
        # Float x and y values to keep track of the location of the player
        # since rects can only store integer values
        self.x = 0.0
        self.y = 0.0
        
        # Player's images as well as the rect representing their hitbox
        self.image = images.kirby.idle.idle_left
        self.rect = self.image.get_rect()

        self.idle_imgs = [
            'kirby/idle/idle_left',
            'kirby/idle/idle_right'
        ]
        
        self.moving_left_imgs = []
        for filename in os.listdir('images/kirby/left_walk'):
            print(filename)
            filename = filename.split('.')[0]
            self.moving_left_imgs.append(f'kirby/left_walk/{filename}')
            print(filename)
        
        self.moving_right_imgs = []
        for filename in os.listdir('images/kirby/right_walk'):
            filename = filename.split('.')[0]
            self.moving_right_imgs.append(f'kirby/right_walk/{filename}')
        
        self.special_attack_imgs = []
        for filename in os.listdir('images/kirby/special_attack'):
            filename = filename.split('.')[0]
            self.moving_right_imgs.append(f'kirby/special_attack/{filename}')
        
        self.attack_left_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_left'):
            filename = filename.split('.')[0]
            self.attack_left_imgs.append(f'kirby/basic_attack_left/{filename}')
        
        self.attack_right_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_right'):
            filename = filename.split('.')[0]
            self.attack_right_imgs.append(f'kirby/basic_attack_right/{filename}')

        # Player's state (eg. idle, walking, jumping, etc.) and the frame of the animation
        self._state = IDLE
        self._frame = 0

        # List of rects of the solid and liquid blocks respectively in the level map
        # Will use these rects to detect and deal with collisions
        self.solid_rects = solid_rects
        self.liquid_rects = liquid_rects
        self.level_map = level_map

        self.enemies = enemies

    def handle_collisions(self):
        """Deal with any collisions the player faces with """
        self.collided_bottom = False
        self.collided_right = False
        self.collided_left = False

        # TODO: to improve the collision, dont check sides that are in between two solids
        # also becaues i need the code to be less similar

        for rect in self.solid_rects:
            if not self.rect.colliderect(rect):
                continue

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

            self.rect.x = self.x
            self.rect.y = self.y
    
    def update_position(self):
        """Move the character based on the movement flags and also handle any collisions with objects"""

        # Jump if the jump key is pressed and TODO: the player is on the ground
        if self.jumping and self.collided_bottom:
            self.y_velocity -= self.jump_power
        
        if self.y - self.rect.height < self.screen_height:
            self.y_velocity += self.gravity

        # Add y_velocity to the player's y value
        self.y += self.y_velocity

        # Move the player left or right based on the movement flags
        if self.moving_right ^ self.moving_left:
            self._state = WALKING

            if self.moving_left:
                self.x -= self.speed
            elif self.moving_right:
                self.x += self.speed
        
        else:
            self._state = IDLE

        # Stop y velocity and put y value in right place if clipping through floor 
        if self.y + self.rect.height >= self.screen_height:
            self.y = self.screen_height - self.rect.height
            self.y_velocity = 0

        self.rect.x = self.x
        self.rect.y = self.y

        # check if the player is colliding with anything
        self.handle_collisions()

    def attack(self):
        """Do an attack animation and damage any enemies in range"""
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

        to_remove = []
        for enemy in self.enemies:
            if enemy.rect.colliderect(attack_rect):
                enemy.hitpoints -= self.attack_dmg * self.attack_multiplier
                if enemy.hitpoints <= 0:
                    to_remove.append(enemy)

        for enemy in to_remove:
            self.enemies.remove(enemy)
    
    def load_level(self, spawn_x, spawn_y):
        # reset health, and place player back at spawn point
        self.hitpoints = settings.player_hitpoints
        self.x = spawn_x
        self.y = spawn_y
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def blit(self, screen):
        """Draw the player to the screen"""
        image = None

        # The player is attacking
        if self._state == ATTACKING:
            if self.direction_facing == LEFT:
                image = self.attack_left_imgs[self._frame]
            else:
                image = self.attack_right_imgs[self._frame]

            # If the frame is the last one in the attack animation, then
            # stop the animation
            if self._frame == len(self.attack_left_imgs) - 1:
                self._state = WALKING if self.moving_left ^ self.moving_right else IDLE
                self._frame = 0

        # The player is idle
        elif self._state == IDLE:
            if self.direction_facing == LEFT:
                image = self.idle_imgs[0]
            else:
                image = self.idle_imgs[1]

        elif self._state == WALKING:
            sz = len(self.moving_left_imgs)
            if self.direction_facing == LEFT:
                image = self.moving_left_imgs[self._frame % sz]
            elif self.direction_facing == RIGHT:
                image = self.moving_right_imgs[self._frame % sz]


        elif self._state == JUMPING:
            pass

        elif self._state == FALLING:
            pass

        elif self._state == SPECIAL:
            pass

        self._frame += 1
        print(image)
        screen.blit(image, self.rect)