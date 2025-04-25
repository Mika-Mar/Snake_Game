import pygame
import globals

class Fruit(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("fruit.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (globals.snake_box,globals.snake_box))
        self.rect = self.image.get_rect(center=pos)
    def get_pos(self):
        return self.rect.center
