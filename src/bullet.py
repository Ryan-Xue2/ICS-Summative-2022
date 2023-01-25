from pgzero.builtins import Actor 

import math
import settings


class Bullet:
    def __init__(self):
        self.actor = Actor('bullet')
        self.speed = settings.bullet_speed
    
    def update(self):
        """Figure out where the bullet is angled towards and fly in that direction"""
        direction = -math.radians(self.actor.angle)
        self.actor.x += math.cos(direction) * self.speed  # cos is adj/hyp, adj is the length
        self.actor.y += math.sin(direction) * self.speed  # sin is opp/hyp, opp is the height
    
    def draw(self):
        """Draw the bullet to the screen"""
        self.actor.draw()