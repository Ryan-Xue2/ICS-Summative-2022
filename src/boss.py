from pgzero.builtins import Actor, animate

import settings


class Boss:
    def __init__(self, player):
        self.player = player
        self.actor = Actor('idi_left')
        self.hitpoints = settings.boss_hitpoints
        self.attack_dmg = settings.boss_attack_dmg
        self.speed = settings.boss_speed
        self.animation = None
    
    def attack(self):
        """Perform a dash attack"""
        target = self.player.x, self.player.y
        self.animation = animate(self.actor, tween='bounce_end', pos=target)

        # TODO: use player's hurt method later maybe
        if self.actor.colliderect(self.player):
            self.player.hitpoints -= 3

    def big_boom(self):
        pass
    
    def spawn(self, x, y):
        """Spawn in the boss into the level"""
        self.actor.left = x
        self.actor.top = y