import settings

from pgzero.builtins import images


class Guard:
    def __init__(self):
        self.hitpoints = settings.guard_hitpoints
        self.attack = settings.guard_attack_dmg
        self.speed = settings.guard_speed

        self.img = images.guard
        self.rect = self.img.get_rect()

        self.x = 0.0
        self.y = 0.0
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def update_position():
        pass

    def blit(self, screen):
        screen.blit(self.img, self.rect)