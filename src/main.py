import pgzrun
from main_character import MainCharacter


WIDTH = 800
HEIGHT = 500

main_char = MainCharacter(WIDTH, HEIGHT)
bg_img = Actor('background')

def draw():
    screen.clear()
    bg_img.draw()
    main_char.blit(screen)


def update():
    main_char.update_position()


def on_key_down(key):
    if key == keys.RIGHT or key == keys.D:
        main_char.moving_right = True
    elif key == keys.LEFT or key == keys.A:
        main_char.moving_left = True
    elif key == keys.UP or key == keys.W:
        main_char.jumping = True

def on_key_up(key):
    if key == keys.RIGHT or key == keys.D:
        main_char.moving_right = False
    elif key == keys.LEFT or key == keys.A:
        main_char.moving_left = False
    elif key == keys.UP or key == keys.W:
        main_char.jumping = False


pgzrun.go()
