import pygame
from rgb_slider import RGB_Slider
from rgb_square import RGB_Square
from color_viewer import Color_Viewer

class Color_Picker:

    def __init__(
            self,
            width: int,
            height: int,
            background_color: tuple[int, int, int, int] | str  = "#00000000",
            **position: tuple[int, int]
        ) -> None:
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.rect = self.image.get_rect(**position)

        square_size = min(round(height/1.1), round(width*0.9))
        slider_height = height - square_size
        color_viewer_size = (width-square_size, height-slider_height)

        self.rgb_slider = RGB_Slider(width, slider_height, 1.0, "#FFFFFF42", bottomleft=(0, height))
        self.rgb_square = RGB_Square(square_size, square_size, self.rgb_slider.get_color(), "#FFFFFF42", topright=(width, 0))
        self.color_viewer = Color_Viewer(*color_viewer_size, self.rgb_square.get_color(), topleft=(0, 0))
        
        print(self.rgb_slider.get_color(), self.rgb_square.get_color())
        self.selected_color = self.rgb_square.get_color()
        self.color_change = True

        self.background_color = background_color
    

    def draw(self, surface):
        self.image.fill(self.background_color)
        self.color_viewer.draw(self.image)
        self.rgb_slider.draw(self.image)
        self.rgb_square.draw(self.image)
        surface.blit(self.image, self.rect)
    
    def handle_event(self, event, primary_surface_pos):
        pos = (primary_surface_pos[0] + self.rect.x, primary_surface_pos[1] + self.rect.y)
        self.rgb_slider.handle_event(event, pos)
        self.rgb_square.handle_event(event, pos)
    
    def update(self):
        if self.rgb_slider.color_change:
            self.rgb_square.change_base_color(self.rgb_slider.get_color())
        if self.rgb_square.color_change:
            self.color_change = True
            self.color_viewer.change_color(self.rgb_square.get_color())
            self.selected_color = self.rgb_square.get_color()

    def get_color(self):
        self.color_change = False
        return self.selected_color


if __name__ == "__main__":
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
