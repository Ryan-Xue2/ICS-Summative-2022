from pgzero.builtins import Actor, animate, images

import settings


class Boss:
    def __init__(self, player):
        self.player = player
        self.attack_img = images.idi_attack
        self.idi_img_left = images.idi_left
        self.idi_img_right = images.idi_right

        self.hitpoints = settings.boss_hitpoints
        self.attack_dmg = settings.boss_attack_dmg
        self.speed = settings.boss_speed

        self.dashing = False

        self.x = 0
        self.y = 0
        self.rect = self.idi_img_left.get_rect()
        self.x_velocity = 0
        self.y_velocity = 0

        self.target = None
        self.just_attacked = False
        self.frames_count = 15
    
    def dash_attack(self):
        """Perform a dash attack"""
        self.dashing = True

        self.target = (self.player.x, self.player.y, self.player.rect.width, self.player.rect.height)
        x_diff = self.player.x - self.x
        y_diff = self.player.y - self.y

        self.x_velocity = x_diff / abs(x_diff) * self.speed
        self.y_velocity = y_diff / abs(x_diff) * self.speed
        print(self.x_velocity, self.y_velocity)


    def set_pos(self, x, y):
        """Set the position of the boss to the specified x and y position"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def update(self):
        """Update the boss position"""
        # If the boss is not dashing, then just exit the method
        if not self.dashing:
            return
        
        # Update the x and y values
        self.x += self.x_velocity
        self.y += self.y_velocity
        
        self.rect.x = self.x
        self.rect.y = self.y

        # Check if the boss hit the original target it was aiming for
        if self.rect.colliderect(self.target):
            self.dashing = False
            self.target = None
            self.x_velocity = 0
            self.y_velocity = 0
            self.just_attacked = True

            # Check if the boss hit the player
            if self.rect.colliderect(self.player.rect):
                self.player.hurt(self.attack_dmg)
        
    
    def blit(self, screen):
        """Draw the boss to the screen"""
        if self.x_velocity < 0:
            screen.blit(self.idi_img_left, self.rect)
        else:
            screen.blit(self.idi_img_right, self.rect)

        if self.just_attacked:
            self.frames_count -= 1
            # Frames left
            if self.frames_count == 0:
                self.just_attacked = False
                self.frames_count = 15

            x = self.x - (self.attack_img.get_width() - self.idi_img_left.get_width()) / 2
            y = self.y - (self.attack_img.get_height() - self.idi_img_left.get_height()) / 2

            screen.blit(self.attack_img, (x, y))