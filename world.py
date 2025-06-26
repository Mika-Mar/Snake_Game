import sys
import copy
from random import randrange
import Snake
import Fruit
import globals
import pygame
import portal
import math
from gamestate import Gamestate
import useful_funcs
from useful_funcs import draw_pause_overlay, message

fruitgroup = pygame.sprite.Group()
def draw_grid():
    for x in range(0, globals.dis_width, globals.snake_box):
        pygame.draw.line(dis, (0,0,0), (x, 0), (x, globals.dis_height))
    for y in range(0, globals.dis_height, globals.snake_box):
        pygame.draw.line(dis, (0,0,0), (0, y), (globals.dis_width, y))

pygame.init()
pygame.mixer.init()
sound1 = pygame.mixer.Sound('Minecraft Eating.mp3')
deathsound = pygame.mixer.Sound('OOF.mp3')
portalsound = pygame.mixer.Sound('Nether Portal Travel Sound (Minecraft) - Sound Effect for editing.mp3')
dis = pygame.display.set_mode((globals.dis_width, globals.dis_height))
snake1 = Snake.Snake()
pygame.display.set_caption(f'Snake current score: {len(snake1.get_snake_body())}')
clock = pygame.time.Clock()
# display frames per second
DISPLAY_FPS = 60
# time between game updates in seconds
UPDATE_INTERVAL = 1 / globals.snakespeed
replay_data = []
def save_gamestate():
    state ={
        "snake": [(segment.x, segment.y) for segment in snake1.get_snake_body()],
        "snake_direction": snake1.direction,
        "fruits": fruitgroup.sprites()
    }
    replay_data.append(state)

def new_fruit():
    x_fruit = (randrange(0, (globals.dis_width // globals.snake_box)) * globals.snake_box) + (globals.snake_box // 2)
    y_fruit = (randrange(0, (globals.dis_height // globals.snake_box)) * globals.snake_box) + (globals.snake_box // 2)
    for fruit in fruitgroup:
        if (x_fruit, y_fruit) == fruit.rect.center:
             return new_fruit()
    for xy in snake1.get_snake_body():
        x, y = xy.center
        if x != x_fruit or y != y_fruit:
            continue
        return new_fruit()
    return x_fruit, y_fruit
port1 = portal.Portal(new_fruit())
port2 = portal.Portal(new_fruit())
fruit_text_box = pygame.Rect(globals.dis_width // 6, globals.dis_height//3,4 * (globals.dis_width//6), (globals.dis_height//2))
fruit_text_box_active = False
text = ''
start_button = pygame.Rect(globals.dis_width // 4, globals.dis_height // 4, 2 * (globals.dis_width // 4), 2 * (globals.dis_height//4))
currentgamestate = Gamestate.MAIN_MENU
current_event = None
running = True
while running:
    while currentgamestate == Gamestate.FRUIT_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fruit_text_box.collidepoint(event.pos):
                    fruit_text_box_active = True
            if event.type == pygame.KEYDOWN:
                if fruit_text_box_active:
                    if event.key == pygame.K_RETURN:
                        globals.amount_fruits = int(text)
                        for i in range(0, globals.amount_fruits):
                            fruitgroup.add(Fruit.Fruit(new_fruit()))
                        currentgamestate = Gamestate.GAME
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        dis.fill((0,0,0))
        message(dis, "Wieviele Früchte?", (255,255,255), (globals.dis_width // 2, globals.dis_height // 6),50, 'Arial')
        pygame.draw.rect(dis, (100,100,100), fruit_text_box)
        message(dis, text, (255,255,255), fruit_text_box.center,50, 'Arial')
        pygame.display.update()
    while currentgamestate == Gamestate.MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentgamestate = Gamestate.GAME_OVER
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    currentgamestate = Gamestate.FRUIT_MENU
        dis.fill((0, 0, 0))
        pygame.draw.rect(dis, (100, 100, 100), start_button)
        pygame.draw.rect(dis, (150, 150, 150), start_button, 5)
        message(dis,"Spiel starten?",(0,255,255),start_button.center,50,"Times New Roman")
        pygame.display.update()
    accumulator = 0
    while currentgamestate == Gamestate.GAME:
        dt = clock.tick(DISPLAY_FPS) / 1000.0
        accumulator += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                currentgamestate = Gamestate.GAME_OVER
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and current_event != pygame.K_RIGHT:
                    snake1.set_direction((-1, 0))
                    current_event = pygame.K_LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and current_event != pygame.K_LEFT:
                    snake1.set_direction((1,0))
                    current_event = pygame.K_RIGHT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and current_event != pygame.K_DOWN:
                    snake1.set_direction((0,-1))
                    current_event = pygame.K_UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_event != pygame.K_UP:
                    snake1.set_direction((0,1))
                    current_event = pygame.K_DOWN
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE):
                    currentgamestate = Gamestate.PAUSED
        while accumulator >= UPDATE_INTERVAL:
            accumulator -= UPDATE_INTERVAL
            hits = pygame.sprite.spritecollide(snake1, fruitgroup, dokill=False)
            for h in hits:
                fruitgroup.remove(h)
                fruitgroup.add(Fruit.Fruit(new_fruit()))
                snake1.grow()
                pygame.display.set_caption(f'Snake current score: {len(snake1.get_snake_body())}')
                pygame.mixer.Sound.play(sound1)
            if snake1.get_snake_head().colliderect(port1):
                snake1.set_snake_head(port2.get_position())
                pygame.mixer.Sound.play(portalsound)
            elif snake1.get_snake_head().colliderect(port2):
                snake1.set_snake_head(port1.get_position())
                pygame.mixer.Sound.play(portalsound)
            save_gamestate()
            snake1.move()
            for i in range(1,len(snake1.get_snake_body())):
                if snake1.get_snake_head().colliderect(snake1.get_snake_body()[i]):
                    pygame.mixer.Sound.play(deathsound)
                    current_event = None
                    currentgamestate = Gamestate.GAME_OVER
                    break
        alpha = accumulator / UPDATE_INTERVAL
        dis.fill((100,100,100))
        draw_grid()
        port1.draw(dis, pygame.time.get_ticks()//2)
        port2.draw(dis, pygame.time.get_ticks()//2)
        snake1.draw(dis, alpha)
        fruitgroup.draw(dis)
        pygame.display.flip()
    if currentgamestate == Gamestate.PAUSED:
        alpha = accumulator / UPDATE_INTERVAL
        dis.fill((100, 100, 100))
        draw_grid()
        port1.draw(dis, pygame.time.get_ticks() // 2)
        port2.draw(dis, pygame.time.get_ticks() // 2)
        snake1.draw(dis, alpha)
        fruitgroup.draw(dis)
        draw_pause_overlay(dis, 128)
        pygame.display.flip()
        while currentgamestate == Gamestate.PAUSED:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_SPACE):
                        currentgamestate = Gamestate.GAME
    while currentgamestate == Gamestate.GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.wait(2)
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fruit_text_box.collidepoint(event.pos):
                    currentgamestate = Gamestate.REPLAY
        dis.fill((100,100,100))
        pygame.draw.rect(dis, (10, 10, 10), fruit_text_box)
        message(dis,"du bist gestorben",(255,0,0), (globals.dis_width//2, globals.dis_height//3), 150, "Times New Roman")
        message(dis,"Replay?",(255,255,255), fruit_text_box.center)
        pygame.display.flip()
    while currentgamestate == Gamestate.REPLAY:
        dis.fill((0,100,100))
        print ("Replay")
        pygame.display.flip()
        for i, data in enumerate(replay_data):
            dis.fill((100,100,100))
            draw_grid()
            snakei = Snake.Snake()
            snakei.body = [pygame.Rect(x, y, globals.snake_box, globals.snake_box) for x, y in data["snake"]]
            snakei.set_direction(data["snake_direction"])
            snakei.draw(dis)
            replay_fruits = pygame.sprite.Group()
            for f in data["fruits"]:
                replay_fruits.add(f)
            replay_fruits.draw(dis)
            pygame.display.flip()
            pygame.time.wait(100)
        currentgamestate = Gamestate.GAME_OVER

pygame.quit()
quit()

