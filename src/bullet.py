from pgzero.builtins import Actor 

import settings
import math


class Bullet:
    def __init__(self):
        self.actor = Actor('bullet')
        # Must keep x and y float values because actor.x and actor.y are only integer values
        self.x = 0.0
        self.y = 0.0
        self.solid_rects = None
        self.speed = settings.bullet_speed
    
    def update(self):
        direction = -math.radians(self.actor.angle)  # THE ANGLE HAS TO BE REVERSED BECAUSE GOD KNOWS WHY?????????
        self.actor.x += math.cos(direction) * self.speed  # cos is adj/hyp, adj is the length
        self.actor.y += math.sin(direction) * self.speed  # sin is opp/hyp, opp is the height
        # self.actor.x = self.x
        # self.actor.y = self.y
    
    def draw(self):
        self.actor.draw()