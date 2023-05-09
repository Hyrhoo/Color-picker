import pygame
from rgb_slider import RGB_Slider

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1900, 500))
    clock = pygame.time.Clock()
    rgb_slider = RGB_Slider(1700, 30)

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        rgb_slider.draw(screen, (950, 250))
        pygame.display.flip()
        clock.tick(60)
        


