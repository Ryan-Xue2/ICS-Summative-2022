from pgzero.builtins import Actor, animate, images

import settings


class Boss:
    def __init__(self, player):
        self.player = player
        self.actor = Actor('idi_left')
        self.attack_img = images.idi_attack_lg
        self.idi_img_left = images.idi_left
        self.idi_img_right = images.idi_right

        self.hitpoints = settings.boss_hitpoints
        self.attack_dmg = settings.boss_attack_dmg
        self.speed = settings.boss_speed

        self.animation = None
    
    def attack(self):
        """Perform a dash attack"""
        target = self.player.x, self.player.y
        self.animation = animate(self.actor, duration=1, tween='accelerate', pos=target)

        # TODO: use player's hurt method later maybe
        if self.actor.colliderect(self.player):
            self.player.hurt(self.attack_dmg)
    
    def spawn(self, x, y):
        """Spawn in the boss into the level"""
        self.actor.left = x
        self.actor.top = y
    
    def blit(self, screen):
        # Actor facing left
        if ((self.actor.angle >= 0 and self.actor.angle <= 90) 
            or (self.actor.angle < 0 and self.actor.angle >= -90)):
            screen.blit(self.idi_img_left, (self.actor.left, self.actor.top))
        else:
            screen.blit(self.idi_img_right, (self.actor.left, self.actor.top))
