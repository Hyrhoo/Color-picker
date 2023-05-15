import pygame
from rgb_slider import RGB_Slider

class Color_Picker:

    def __init__(
            self,
            width: int,
            height: int,
            center: tuple[int, int]
        ) -> None:
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=center)
        
        self.color_change = True
    

    def draw(self, surface):
        pass
    
    def handle_event(self, event, sub_surface_pos):
        pass
    
    def get_color(self):
        self.color_change = False
        return None


if __name__ == "__main__":
    pygame.init()
    screen_size = (1800, 800)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    color_picker = Color_Picker(1700, 150, tuple(i//2 for i in screen_size))

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

        color_picker.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if color_picker.color_change:
            print(color_picker.get_color())
