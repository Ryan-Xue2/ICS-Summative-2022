import settings

from constants import LEFT, RIGHT
from pgzero.builtins import images, Actor, clock
from bullet import Bullet


class Guard:
    def __init__(self, player, bullets):
        # Guard stats
        self.hitpoints = settings.guard_hitpoints
        self.attack = settings.guard_attack_dmg
        self.speed = settings.guard_speed
        self.range = settings.guard_range

        # Load all the images of the guards
        self.img = images.guard
        self.img_hurt = images.guard_hurt
        self.img_left = images.guard_left
        self.img_hurt_left = images.guard_hurt_left

        # Guard's hitbox
        self.rect = self.img.get_rect()

        # 
        self.direction_facing = LEFT
        self.hurt = False

        self.bullets = bullets

        # Player instance os the guard knows where to go and where to shoot
        self.player = player

        # Guard's float x y positions (because rects dont store int values)
        self.x = 0.0
        self.y = 0.0
    
    def set_pos(self, x, y):
        """Set the guard's x y position to the specifed x and y values"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        """Update the guard's direction facing"""
        if abs(self.x - self.player.x) <= self.range:
            if self.x < self.player.x:
                self.direction_facing = RIGHT
            else:
                self.direction_facing = LEFT
    
    def shoot(self):
        """Shoot a bullet in the direction of the player"""
        # Don't shoot if the player is not in range
        if (self.player.x - self.x) > self.range:
            return
            
        bullet = Bullet()

        # Make the bullet seem like it started from the guard's gun
        if self.direction_facing == LEFT:
            bullet.actor.left, bullet.actor.top = self.rect.midleft
        else:
            bullet.actor.left, bullet.actor.top = self.rect.midright

        # Angle the bullet towards the player
        angle = bullet.actor.angle_to(self.player.rect.center)
        bullet.actor.angle = angle
        self.bullets.append(bullet)

    def blit(self, screen):
        """Draw the guard image to the screen"""
        image = None
        if self.hurt:
            if self.direction_facing == LEFT:
                image = self.img_hurt_left
            else:
                image = self.img_hurt
            self.hurt = False

        elif self.direction_facing == LEFT:
            image = self.img_left
        else:
            image = self.img

        screen.blit(image, self.rect)