import pygame.draw

import globals

global snake_box
class Snake(pygame.sprite.Sprite):
    def __init__(self, body = None, direction = (0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.head_image = pygame.image.load("SnakeHead.png")
        self.head_image = pygame.transform.scale(self.head_image, (globals.snake_box,globals.snake_box))
        self.body_image = pygame.image.load("SnakeBody.png").convert_alpha()
        self.body_image = pygame.transform.scale(self.body_image, (globals.snake_box,globals.snake_box))
        self.corner_image = pygame.image.load("SnakeCorner.png").convert_alpha()
        self.corner_image = pygame.transform.scale(self.corner_image, (globals.snake_box, globals.snake_box))
        self.body = body if body else [(pygame.Rect(0,0,globals.snake_box, globals.snake_box))]
        self.rect = self.body[0]
    def move(self):
        for i in range(len(self.body)-1, 0, -1):
            if i == 1:
                print("test")
            self.body[i] = self.body[i-1].copy()
        x,y = self.body[0].center
        self.body[0].center = ((x+(self.direction[0] * globals.snake_box))% globals.dis_width, (y + (self.direction[1] * globals.snake_box)) % globals.dis_height)
    def set_direction(self, direction):
        self.direction = direction
    def draw(self, dis):
        for i in range(0,len(self.body)):
            x,y = self.body[i].center
            if i == 0:
                if self.direction == (1,0):
                    dis.blit(pygame.transform.rotate(self.head_image,180), self.body[i])
                elif self.direction == (0,1):
                    dis.blit(pygame.transform.rotate(self.head_image, 90), self.body[i])
                elif self.direction == (0,-1):
                    dis.blit(pygame.transform.rotate(self.head_image, 270), self.body[i])
                else:
                    dis.blit(self.head_image, self.body[i])
            else:
                for j in range(-1,2,2):
                    if i != len(self.body)-1 and self.body[i+j].x != self.body[i].x and self.body[i].y != self.body[i-j].y:
                        if self.body[i+j].x > self.body[i].x and self.body[i-j].y > self.body[i].y:
                            dis.blit(pygame.transform.rotate(self.corner_image, 90), self.body[i])
                            i+= 1
                        elif self.body[i+j].x < self.body[i].x and self.body[i-j].y < self.body[i].y:
                            dis.blit(pygame.transform.rotate(self.corner_image, 270), self.body[i])
                            i+= 1
                        elif self.body[i+j].x < self.body[i].x and self.body[i-j].y > self.body[i].y:
                            dis.blit(self.corner_image, self.body[i])
                            i+=1
                        else:
                            dis.blit(pygame.transform.rotate(self.corner_image,180), self.body[i])
                            i+=1
                if self.body[i-1].y != self.body[i].y:
                    dis.blit(pygame.transform.rotate(self.body_image, 90), self.body[i])
                else:
                    dis.blit(self.body_image, self.body[i])
    def grow(self):
        nextbody = self.body[len(self.body)-1].copy()
        self.body.append(nextbody)
    def get_snake_head(self):
        return self.body[0]
    def get_snake_body(self):
        return self.body.copy()
    def set_snake_head(self, head):
        self.body[0].center = head

