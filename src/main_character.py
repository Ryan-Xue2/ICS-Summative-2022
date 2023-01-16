from pgzero.builtins import Actor, Rect


class MainCharacter:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.speed = 5
        self.jump_force = 10
        self.gravity = 1

        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        
        self.x = 0
        self.y = 0

        self.y_velocity = 0

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
    
    def update_position(self):
        if self.jumping and not self._is_midair():
            self.y_velocity -= self.jump_force
        
        if self._is_midair():
            self.y_velocity += self.gravity

        self.y += self.y_velocity

        if self.moving_right ^ self.moving_left:
            if self.moving_left:
                self.x -= self.speed
            elif self.moving_right:
                self.x += self.speed

        if self.y + 100 >= self.screen_height:
            self.y = self.screen_height - 100
            self.y_velocity = 0

        self.actor.x = self.x
        self.actor.y = self.y
        print(self.x, self.y)
        # check if x is colliding with anything
        # and put it back

    
    def _is_midair(self):
        if self.y + 100 >= self.screen_height:
            return False
        return True

    def blit(self):
        self.actor.draw()
        self.sword_actor.draw()
