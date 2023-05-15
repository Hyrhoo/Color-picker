import pygame

class RGB_Slider:
    def __init__(
            self,
            width: int,
            height: int,
            center: tuple[int, int],
            cursor_proportion: float = 0.25,
            background_color: tuple[int, int, int, int] | str = "#FFFFFF42"
        ) -> None:
        self.draw_surface = pygame.Surface((width, height)).convert_alpha()
        self.draw_rect = self.draw_surface.get_rect(center=center)

        cursor_height = height
        cursor_width = cursor_height * cursor_proportion
        surf_size = (width - cursor_width, height * 0.85)

        self.surface = pygame.Surface((1531, 1))
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
        self.move_cursor(self.surface_rect.x)

        self.background_color = background_color


    def create_color(self, step):
        color = [255, 0, 0]
        if step:
            value = min(255, step)
            color[1] += value
            step -= value
        if step:
            value = min(255, step)
            color[0] -= value
            step -= value
        if step:
            value = min(255, step)
            color[2] += value
            step -= value
        if step:
            value = min(255, step)
            color[1] -= value
            step -= value
        if step:
            value = min(255, step)
            color[0] += value
            step -= value
        if step:
            value = min(255, step)
            color[2] -= value
            step -= value
        if step:
            raise ValueError(f"the given value is too big {step}")
        return tuple(color)

    def __color_surface(self):
        for x in range(1531):
            color = self.create_color(x)
            self.surface.set_at((x, 0), color)

    def draw(self, surface):
        self.draw_surface.fill(self.background_color)
        self.draw_surface.blit(self.surface, self.surface_rect)
        self.draw_surface.blit(self.cursor_surface, self.cursor_rect)
        surface.blit(self.draw_surface, self.draw_rect)

    def move_cursor(self, new_pos):
        self.color_change = True
        self.cursor = new_pos - self.surface_rect.x
        self.cursor = min(max(self.cursor, 0), self.surface_rect.width - 1)
        self.cursor_color = self.surface.get_at((self.cursor, 0))
        self.cursor_rect.topleft = (1 + self.cursor + self.surface_rect.x - self.cursor_rect.width/2, 0)

        self.cursor_surface.fill((0, 0, 0, 0))
        rect_coordon = (0, 0, self.cursor_rect.width, self.cursor_rect.height)
        pygame.draw.rect(self.cursor_surface, self.cursor_color, rect_coordon, border_radius=9999)
        pygame.draw.rect(self.cursor_surface, "#FFFFFF", rect_coordon, self.cursor_border_thickness, 9999)

    def handle_event(self, event: pygame.event.Event, sub_surface_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - sub_surface_pos[0] - self.draw_rect.x, event.pos[1] - sub_surface_pos[1] - self.draw_rect.y)
            is_colliding = self.surface_rect.collidepoint(pos) or self.cursor_rect.collidepoint(pos)
            if is_colliding:
                self.select = True
                self.move_cursor(pos[0])
        if event.type == pygame.MOUSEBUTTONUP:
            self.select = False
        if event.type == pygame.MOUSEMOTION:
            if self.select:
                pos = event.pos[0] - sub_surface_pos[0] - self.draw_rect.x
                self.move_cursor(pos)

    def get_color(self):
        self.color_change = False
        return self.cursor_color

if __name__ == "__main__":
    pygame.init()
    screen_size = (1800, 800)
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
            rgb_slider.handle_event(event, (0, 0))

        rgb_slider.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if rgb_slider.color_change:
            print(rgb_slider.get_color())