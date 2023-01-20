import os
import settings

from pgzero.builtins import images, Rect


class Player:
    def __init__(self, screen_width, screen_height, solid_rects, liquid_rects, enemies):
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
        self.direction_facing = 1
        
        # Float x and y values to keep track of the location of the player
        # since rects can only store integer values
        self.x = 0.0
        self.y = 0.0
        
        # Player's images as well as the rect representing their hitbox
        self.image = images.kirby.idle.idle_left
        self.rect = self.image.get_rect()

        self.idle_imgs = [
            'images/idle/idle_left',
            'images/idle/idle_right'
        ]
        
        self.moving_left_imgs = []
        for filename in os.listdir('images/kirby/left_walk'):
            filename = filename.split('.')[0]
            self.moving_left_imgs.append(f'images/kirby/left_walk/{filename}')
        
        self.moving_right_imgs = []
        for filename in os.listdir('images/kirby/right_walk'):
            filename = filename.split('.')[0]
            self.moving_right_imgs.append(f'images/kirby/right_walk/{filename}')
        
        self.special_attack_imgs = []
        for filename in os.listdir('images/kirby/special_attack'):
            filename = filename.split('.')[0]
            self.moving_right_imgs.append(f'images/kirby/special_attack/{filename}')
        
        self.attack_left_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_left'):
            filename = filename.split('.')[0]
            self.attack_left_imgs.append(f'images/kirby/basic_attack_left/{filename}')
        
        self.attack_right_imgs = []
        for filename in os.listdir('images/kirby/basic_attack_right'):
            filename = filename.split('.')[0]
            self.attack_right_imgs.append(f'images/kirby/basic_attack_right/{filename}')

        # List of rects of the solid and liquid blocks respectively in the level map
        # Will use these rects to detect and deal with collisions
        self.solid_rects = solid_rects
        self.liquid_rects = liquid_rects

        self.enemies = enemies

    def handle_collisions(self):
        """Deal with any collisions the player faces with """
        self.collided_bottom = False
        self.collided_right = False
        self.collided_left = False

        for rect in self.solid_rects:
            if self.rect.colliderect(rect):
                # Figure out whether the player is closing to the horizontal part of the block 
                # or the vertical part and do the player translation to the one closer
                dist_left = abs(rect.right - self.rect.left)
                dist_right = abs(rect.left - self.rect.right)
                dist_top = abs(rect.bottom - self.rect.top)
                dist_bottom = abs(rect.top - self.rect.bottom)

                # Collision with right or left side is closer than the collision to the top or bottom
                if min(dist_left, dist_right) < min(dist_top, dist_bottom):
                    # Player's left side hit wall
                    if dist_left < dist_right:
                        self.collided_left = True
                        self.x = rect.right + 1
                        
                    # Player's right side hit wall
                    else:
                        self.collided_right = True
                        self.x = rect.left - 1 - self.rect.width
                
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

                # Update the player's position
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
            if self.moving_left:
                self.x -= self.speed
            elif self.moving_right:
                self.x += self.speed

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
        # Player is facing left
        if self.direction_facing == -1:
            attack_rect = Rect(
                self.x-10, self.y, 
                self.rect.width, self.rect.height)
        # Player is facing right
        else:
            attack_rect = Rect(
                self.x+self.rect.width+10, self.y, 
                self.rect.width, self.rect.height)

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
        screen.blit(self.image, self.rect)
