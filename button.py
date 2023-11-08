import pygame

class Button:

    def __init__(
            self,
            width,
            height,
            title,
            title_size,
            action,
            background_color,
            **position
        ) -> None:
        self.draw_surface = pygame.Surface((width, height)).convert_alpha()
        self.draw_rect = self.draw_surface.get_rect(**position)

        self.font = pygame.Font(None, title_size)
        self.title = title
        self.title_surface = self.font.render(self.title, True, "#FFFFFF")
        self.title_rect = self.title_surface.get_rect(center=(width/2, height/2))
        self.background_color = background_color

        # self.surface = pygame.Surface((width, height)).convert_alpha()
        # self.surface.fill("#00000000")
        # pygame.draw.rect(self.surface, background_color, (0, 0, width, height), 0, 999999)
        # pygame.draw.rect(self.surface, "#FFFFFF", (0, 0, width, height), 3, 999999)
        self.border_color = "#FFFFFF"

        self.action = action
        self.is_select = False

    def draw(self, surface):
        self.draw_surface.fill("#00000000")
        # self.draw_surface.blit(self.surface, (0, 0))
        pygame.draw.rect(self.draw_surface, self.background_color, (0, 0, self.draw_rect.width, self.draw_rect.height), 0, 999999)
        pygame.draw.rect(self.draw_surface, self.border_color, (0, 0, self.draw_rect.width, self.draw_rect.height), 3, 999999)
        self.draw_surface.blit(self.title_surface, self.title_rect)
        surface.blit(self.draw_surface, self.draw_rect)

    def change_title(self, new_title):
        self.title = new_title
        self.title_surface = self.font.render(self.title, True, "#FFFFFF")
        self.title_rect = self.title_surface.get_rect(center=(self.draw_rect.width/2, self.draw_rect.height/2))
    
    def handle_event(self, event: pygame.event.Event, primary_surface_pos):
        mouse_pos = pygame.mouse.get_pos()
        pos = (mouse_pos[0] - primary_surface_pos[0], mouse_pos[1] - primary_surface_pos[1])
        is_colliding = self.draw_rect.collidepoint(pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_colliding:
                self.action()
        if event.type == pygame.MOUSEMOTION:
            if is_colliding:
                self.is_select = True
                self.border_color = "#999999"
            else:
                self.is_select = False
                self.border_color = "#FFFFFF"


if __name__ == "__main__":
    pygame.init()
    screen_size = (1800, 800)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    button = Button(200, 50, "salut !", 40, lambda: print("bouton cliquer"), "#FF4242", center=tuple(i//2 for i in screen_size))

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
            button.handle_event(event, (0, 0))

        button.draw(screen)
        pygame.display.flip()
        clock.tick(60)