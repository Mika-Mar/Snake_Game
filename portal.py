import pygame

import globals


class Portal(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = (pygame.image.load("Portal.png"), pygame.image.load("Portal2.png"))
        self.images = (pygame.transform.scale(self.images[0], (globals.snake_box, globals.snake_box))),pygame.transform.scale(self.images[1], (globals.snake_box, globals.snake_box))
        self.position = position
        self.x,self.y = position
        self.x -= (globals.snake_box//2)
        self.y -= (globals.snake_box//2)
        self.rect = self.images[0].get_rect(center=position)
    def get_position(self):
        return self.position

    def draw(self, screen, i):
        screen.blit(self.images[i%2], (self.x,self.y))
