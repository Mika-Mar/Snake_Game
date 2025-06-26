import pygame.draw

import globals

global snake_box
class Snake(pygame.sprite.Sprite):
    def __init__(self, body=None, direction=(0, 0)):
        super().__init__()
        self.direction = direction
        self.head_image = pygame.image.load("SnakeHead.png")
        self.head_image = pygame.transform.scale(
            self.head_image, (globals.snake_box, globals.snake_box)
        )
        self.body_image = pygame.image.load("SnakeBody.png").convert_alpha()
        self.body_image = pygame.transform.scale(
            self.body_image, (globals.snake_box, globals.snake_box)
        )
        self.corner_image = pygame.image.load("SnakeCorner.png").convert_alpha()
        self.corner_image = pygame.transform.scale(
            self.corner_image, (globals.snake_box, globals.snake_box)
        )
        self.body = body if body else [pygame.Rect(0, 0, globals.snake_box, globals.snake_box)]
        self.prev_body = [seg.copy() for seg in self.body]
        self.rect = self.body[0]
    def move(self):
        self.prev_body = [seg.copy() for seg in self.body]
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1].copy()
        x, y = self.body[0].center
        self.body[0].center = (
            (x + (self.direction[0] * globals.snake_box)) % globals.dis_width,
            (y + (self.direction[1] * globals.snake_box)) % globals.dis_height,
        )
    def set_direction(self, direction):
        self.direction = direction
    def _interpolated_body(self, alpha):
        rects = []
        for prev, curr in zip(self.prev_body, self.body):
            rect = curr.copy()
            cx = prev.centerx + (curr.centerx - prev.centerx) * alpha
            cy = prev.centery + (curr.centery - prev.centery) * alpha
            rect.center = (cx, cy)
            rects.append(rect)
        return rects

    def draw(self, dis, alpha=1.0):
        rects = self._interpolated_body(alpha)
        for i, rect in enumerate(rects):
            if i == 0:
                if self.direction == (1, 0):
                    dis.blit(pygame.transform.rotate(self.head_image, 180), rect)
                elif self.direction == (0, 1):
                    dis.blit(pygame.transform.rotate(self.head_image, 90), rect)
                elif self.direction == (0, -1):
                    dis.blit(pygame.transform.rotate(self.head_image, 270), rect)
                else:
                    dis.blit(self.head_image, rect)
            else:
                for j in range(-1, 2, 2):
                    if (
                        i != len(self.body) - 1
                        and self.body[i + j].x != self.body[i].x
                        and self.body[i].y != self.body[i - j].y
                    ):
                        if self.body[i + j].x > self.body[i].x and self.body[i - j].y > self.body[i].y:
                            dis.blit(pygame.transform.rotate(self.corner_image, 90), rect)
                            i += 1
                        elif self.body[i + j].x < self.body[i].x and self.body[i - j].y < self.body[i].y:
                            dis.blit(pygame.transform.rotate(self.corner_image, 270), rect)
                            i += 1
                        elif self.body[i + j].x < self.body[i].x and self.body[i - j].y > self.body[i].y:
                            dis.blit(self.corner_image, rect)
                            i += 1
                        else:
                            dis.blit(pygame.transform.rotate(self.corner_image, 180), rect)
                            i += 1
                if self.body[i - 1].y != self.body[i].y:
                    dis.blit(pygame.transform.rotate(self.body_image, 90), rect)
                else:
                    dis.blit(self.body_image, rect)
    def grow(self):
        nextbody = self.body[len(self.body)-1].copy()
        self.body.append(nextbody)
    def get_snake_head(self):
        return self.body[0]
    def get_snake_body(self):
        return self.body.copy()
    def set_snake_head(self, head):
        self.body[0].center = head
        self.prev_body = [seg.copy() for seg in self.body]

