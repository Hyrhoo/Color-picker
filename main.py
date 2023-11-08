import pygame
from fonctions import *
from color_picker import Color_Picker
from button import Button

button_select_color = Button
button_copy_rgb = Button
button_copy_hex = Button

pygame.init()
screen_size = (1800, 800)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
color_picker = Color_Picker(1000, 400, "#FFFFFF42", center=tuple(i//2 for i in screen_size))

while True:
    screen.fill("#424242")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        color_picker.handle_event(event, (0, 0))

    color_picker.update()

    color_picker.draw(screen)
    pygame.display.flip()
    clock.tick(60)

    if color_picker.color_change:
        print(color_picker.get_color())
