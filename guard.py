import settings


class Guard:
    def __init__(self):
        self.health = settings.guard_hitpoints
        self.attack = settings.guard_attack_dmg
        self.speed = settings.guard_speed
        self.img = None
        self.x = 0.0
        self.y = 0.0
        self.rect = [0, 0, 10, 10]