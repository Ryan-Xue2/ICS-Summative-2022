import pgzrun
from main_character import MainCharacter

main_char = MainCharacter()

def draw():
    screen.clear()
    main_char.blit()

def update():
    main_char.actor.x += 1

pgzrun.go()
