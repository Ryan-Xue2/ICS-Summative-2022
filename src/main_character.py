from pgzero.builtins import Actor, Rect

class MainCharacter:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sword_x = 0
        self.sword_y = 0
        self.actor = Actor('main_character')
        self.sword_actor = Actor('mythicalsword')
        print(dir(Actor))
        print(Actor.image)
        print(self.actor.pos)
        self.rect = Rect(self.actor.x+50, self.actor.y, 10, 10)


    def collided(self, rect):
        if rect.colliderect(self.rect):
            return True
        return False

    def blit(self):
        self.actor.draw()
        self.sword_actor.draw()
