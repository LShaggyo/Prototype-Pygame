import pygame

# Clase Platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))  # Color azul para la plataforma
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
