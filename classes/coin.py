import pygame
import random

# Clase Coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Color amarillo para la moneda
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800 - self.rect.width)
        self.rect.y = random.randint(0, 600 - self.rect.height)
