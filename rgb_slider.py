import pygame

class RGB_Slider:
    def __init__(
            self,
            width: int,
            height: int,
            center: tuple[int, int],
        ) -> None:
        self.surface = pygame.Surface((1531, 1))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, (width, height))
        self.rect = self.surface.get_rect(center=center)

        self.select = False
        self.color_change = True

        cursor_height = max(3, height + height // 5)
        cursor_width = max(3, cursor_height // 5)
        self.cursor_surface = pygame.Surface((cursor_width, cursor_height)).convert_alpha()
        self.cursor_rect = self.cursor_surface.get_rect()
        self.move_cursor(self.rect.left)

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
        surface.blit(self.surface, self.rect)
        surface.blit(self.cursor_surface, self.cursor_rect)

    def move_cursor(self, new_pos):
        self.color_change = True
        self.cursor = new_pos-self.rect.left
        self.cursor = min(max(self.cursor, 0), self.rect.width-1)
        self.cursor_color = self.surface.get_at((self.cursor, 0))
        self.cursor_rect.center = (self.rect.left + self.cursor, self.rect.top + self.rect.height/2)

        self.cursor_surface.fill((0, 0, 0, 0))
        rect_coordon = (0, 0, self.cursor_rect.width, self.cursor_rect.height)
        pygame.draw.rect(self.cursor_surface, self.cursor_color, rect_coordon, border_radius=9999)
        pygame.draw.rect(self.cursor_surface, "#000000", rect_coordon, 1, 9999)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_colliding = self.rect.collidepoint(*event.pos) or self.cursor_rect.collidepoint(*event.pos)
            if is_colliding:
                self.select = True
                self.move_cursor(event.pos[0])
        if event.type == pygame.MOUSEBUTTONUP:
            self.select = False
        if event.type == pygame.MOUSEMOTION:
            if self.select:
                self.move_cursor(event.pos[0])

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
            rgb_slider.handle_event(event)

        rgb_slider.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if rgb_slider.color_change:
            print(rgb_slider.get_color())