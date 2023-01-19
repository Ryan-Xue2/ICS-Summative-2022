import settings

from pgzero.builtins import images


class Player:
    def __init__(self, screen_width, screen_height):
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
        self.collided_left = False
        self.collided_right = False
        self.collided_bottom = False
        
        # Float x and y values to keep track of the location of the player
        # since rects can only store integer values
        self.x = 0.0
        self.y = 0.0
        
        # Player's image as well as the rect representing their hitbox
        self.image = images.player.convert_alpha()
        self.rect = self.image.get_rect()

        # Level solid rects

    def handle_collisions(self):
        """Deal with any collisions the player faces with """
        # Collision with screen
        # Collision with blocks
        pass
    
    def update_position(self):
        """Move the character based on the movement flags and also handle any collisions with objects"""
        # Jump if the jump key is pressed and TODO: the player is on the ground
        if self.jumping and self.y + self.rect.height == self.screen_height:
            self.y_velocity -= self.jump_power
        
        # TODO:
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
        # TODO: calculate the attack rect
        attack_rect = Rect(0, 0, 0, 0)
    
    def load_level(self, level):
        """Load a new level"""
        # maybe can do the setting x y position somewhere else, like in the load new level function in main
        pass

    def blit(self, screen):
        """Draw the player to the screen"""
        screen.blit(self.image, self.rect)
