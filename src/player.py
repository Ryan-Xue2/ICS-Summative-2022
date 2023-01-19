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

        # An attribute to keep track of which direction the player is facing, 
        # -1 for left, and 1 for right
        self.direction_facing = 1
        
        # Float x and y values to keep track of the location of the player
        # since rects can only store integer values
        self.x = 0.0
        self.y = 0.0
        
        # Player's image as well as the rect representing their hitbox
        self.image = images.player.convert_alpha()
        self.rect = self.image.get_rect()

        # List of rects of the solid and liquid blocks respectively in the level map
        # Will use these rects to detect and deal with collisions
        self.solid_rects = solid_rects
        self.liquid_rects = liquid_rects

        self.enemies = enemies

    def handle_collisions(self):
        """Deal with any collisions the player faces with """
        pass
    
    def update_position(self):
        """Move the character based on the movement flags and also handle any collisions with objects"""
        # Jump if the jump key is pressed and TODO: the player is on the ground
        if self.jumping and self.y + self.rect.height == self.screen_height:
            self.y_velocity -= self.jump_power
        
        if self.y - self.rect.height < self.screen_height:
            self.y_velocity += self.gravity

        # Add y_velocity to the player's y value
        # self.y += self.y_velocity

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
        if self.direction_facing == -1:
            attack_rect = Rect(
                self.x-50, self.y, 
                self.rect.width, self.rect.height)
        else:
            attack_rect = Rect(
                self.x+50, self.y, 
                self.rect.width, self.rect.height)

        for enemy in self.enemies:
            continue
            # TODO: check whether the enemy is in the attack rect of the player
            # if they are, then deal damage to them, and remove them from the list if 
    
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
