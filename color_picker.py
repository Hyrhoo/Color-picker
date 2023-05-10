import pygame
from rgb_slider import RGB_Slider

if __name__ == "__main__":
    screen_size = (1800, 800)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    rgb_slider = RGB_Slider(1700, 150, tuple(i//2 for i in screen_size))

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
            rgb_slider.handle_event(event)
        
        rgb_slider.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if rgb_slider.color_change:
            print(rgb_slider.get_color())
        


