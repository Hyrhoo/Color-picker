import pygame
from fonctions import rgb_to_hsv, hsv_to_rgb
class RGB_Square:
    
    def __init__(
            self,
            width: int,
            height: int,
            base_color: tuple[int, int, int],
            background_color: tuple[int, int, int, int] | str = "#00000000",
            **position: tuple[int, int]
        ) -> None:
        self.draw_surface = pygame.Surface((width, height)).convert_alpha()
        self.draw_rect = self.draw_surface.get_rect(**position)

        self.hue = rgb_to_hsv(*base_color)[0]

        cursor_width = round(width / 10)
        cursor_height = round(height / 10)
        surf_size = (width - cursor_width, height - cursor_height)
        self.x_multi = 1 / surf_size[0]
        self.y_multi = 1 / surf_size[1]

        self.surface = pygame.Surface((256, 256))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, surf_size)

        self.x_offset = round((self.draw_surface.get_width() - self.surface.get_width()) / 2)
        self.y_offset = round((self.draw_surface.get_height() - self.surface.get_height()) / 2)
        self.surface_rect = self.surface.get_rect(topleft=(self.x_offset, self.y_offset))

        self.select = False
        self.color_change = True

        self.cursor_surface = pygame.Surface((cursor_width, cursor_height)).convert_alpha()
        self.cursor_rect = self.cursor_surface.get_rect()
        self.cursor_border_thickness = int(min(max(cursor_height//10, 1), max(cursor_width//10, 1)))
        self.move_cursor(self.surface_rect.right, self.surface_rect.top)

        self.background_color = background_color
    
    def __color_surface(self):
        multi = 1/255
        for x in range(256):
            x_mult = x*multi
            for y in range(256):
                y2 = 255 - y
                color = hsv_to_rgb(self.hue, x_mult, y2*multi)
                self.surface.set_at((x, y), color)
    
    def draw(self, surface):
        self.draw_surface.fill(self.background_color)
        self.draw_surface.blit(self.surface, self.surface_rect)
        self.draw_surface.blit(self.cursor_surface, self.cursor_rect)
        surface.blit(self.draw_surface, self.draw_rect)
    
    def move_cursor(self, x, y):
        self.color_change = True
        x = x - self.surface_rect.x
        y = y - self.surface_rect.y
        self.cursor = (min(max(x, 0), self.surface_rect.width - 1), min(max(y, 0), self.surface_rect.height - 1))
        
        cursor_saturation = self.cursor[0]*self.x_multi
        cursor_value = (self.surface_rect.height - self.cursor[1])*self.y_multi
        self.cursor_color = hsv_to_rgb(self.hue, cursor_saturation, cursor_value)
        self.cursor_rect.center = (1 + self.cursor[0] + self.x_offset, 1 + self.cursor[1] + self.y_offset)

        self.cursor_surface.fill((0, 0, 0, 0))
        rect_coordon = (0, 0, self.cursor_rect.width, self.cursor_rect.height)
        pygame.draw.rect(self.cursor_surface, self.cursor_color, rect_coordon, border_radius=9999)
        pygame.draw.rect(self.cursor_surface, "#FFFFFF", rect_coordon, self.cursor_border_thickness, 9999)
    
    def handle_event(self, event: pygame.event.Event, primary_surface_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - primary_surface_pos[0] - self.draw_rect.x, event.pos[1] - primary_surface_pos[1] - self.draw_rect.y)
            is_colliding = self.surface_rect.collidepoint(pos) or self.cursor_rect.collidepoint(pos)
            if is_colliding:
                self.select = True
                self.move_cursor(*pos)
        if event.type == pygame.MOUSEBUTTONUP:
            self.select = False
        if event.type == pygame.MOUSEMOTION:
            if self.select:
                pos = (event.pos[0] - primary_surface_pos[0] - self.draw_rect.x, event.pos[1] - primary_surface_pos[1] - self.draw_rect.y)
                self.move_cursor(*pos)

    def get_color(self):
        self.color_change = False
        return self.cursor_color
    
    def change_base_color(self, new_color):
        self.hue = rgb_to_hsv(*new_color)[0]

        surf_size = self.surface_rect.size

        self.surface = pygame.Surface((256, 256))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, surf_size)

        # self.surface_rect = self.surface.get_rect(topleft=(self.x_offset, self.y_offset))
        self.color_change = True
        cursor_pos = (self.cursor[0] + self.x_offset, self.cursor[1] + self.y_offset)
        self.move_cursor(*cursor_pos)

    def set_value(self, value):
        cursor_y = self.surface_rect.height - value/self.y_multi
        self.move_cursor(self.cursor[0], self.surface_rect.y + cursor_y)

    def set_saturation(self, saturation):
        cursor_x = saturation/self.x_multi
        self.move_cursor(self.surface_rect.x + cursor_x, self.cursor[1])


if __name__ == "__main__":
    import random
    pygame.init()
    screen_size = (1800, 800)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    rgb_square = RGB_Square(500, 500, (255, 0, 0), "#FFFFFF42", center=tuple(i//2 for i in screen_size))

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
            rgb_square.handle_event(event, (0, 0))

        rgb_square.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if rgb_square.color_change:
            print(rgb_square.get_color())