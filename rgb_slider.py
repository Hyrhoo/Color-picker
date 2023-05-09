import pygame

class RGB_Slider:
    def __init__(
            self,
            wigth: int,
            height: int,
            angle: int = 0,
            border_color: tuple[int, int, int] = (0, 0, 0)
        ) -> None:
        self.surface = pygame.Surface((1530, 1))
        self.__color_surface()
        self.surface = pygame.transform.scale(self.surface, (wigth, height))
        self.surface = pygame.transform.rotate(self.surface, angle)
        pygame.draw.rect(self.surface, border_color, (0, 0, wigth, height), 1)
    
    def creat_color(self, step):
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
        return tuple(color)

    def __color_surface(self):
        for x in range(1530):
            color = self.creat_color(x)
            self.surface.set_at((x, 0), color)
    
    def draw(self, surface, center):
        rect = self.surface.get_rect(center=center)
        surface.blit(self.surface, rect)
