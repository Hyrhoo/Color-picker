import pygame

class Color_Viewer:
    def __init__(
            self,
            width: int,
            height: int,
            color: tuple[int, int, int] | str,
            **potsition: tuple[int, int]
        ) -> None:
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(**potsition)

        self.color = color
        self.image.fill(color)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def change_color(self, new_color):
        self.color = new_color
        self.image.fill(self.color)