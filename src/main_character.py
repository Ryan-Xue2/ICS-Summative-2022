from pgzero.builtins import images


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
        
        self.image = images.main_character.convert_alpha()
        self.rect = self.image.get_rect()

    def handle_collisions(self):
        # collision with screen
        pass
    
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

        if self.y + self.rect.height >= self.screen_height:
            self.y = self.screen_height - self.rect.height
            self.y_velocity = 0

        self.rect.x = self.x
        self.rect.y = self.y
        # check if x is colliding with anything
        # and put it back

    
    def _is_midair(self):
        if self.y + self.rect.height >= self.screen_height:
            return False
        return True

    def blit(self, screen):
        screen.blit(self.image, self.rect)
