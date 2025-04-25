# This is a sample Python script.
from random import randrange
from string import whitespace
#from typing import Optional, Union, An
from Fruit import Fruit
from pygame.event import event_name
from globals import *
from Snake import Snake


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

'''
def swap(t, i, j):
    t[i], t[j] = t[j], t[i]
s = list("Hello, World")
swap(s,1,10)
print("".join(s))
print("Geben sie die Obergrenze der zu erratenden Zahlen ein:")
obergrenze = int(input())
print ("Geben sie die Anzahl an Rateversuchen des Computers ein:")
versuche = int(input())
y = [randrange(0, obergrenze)]
x = int(input())
while x > 10 or x < 0:
    print("Gebe eine 2 stellige positive Zahl ein")
    x = int(input())
for i in range(versuche):
    if x == y[i]:
        print("Der Computer hat deine Zahl erraten")
    else:
        z = randrange(0, obergrenze)
        l = len(y)
        y = set(y)
        while l <= i+1:
            z = randrange(0, obergrenze)
            y.add(z)
            l = len(y)
        print(f"Der Computer hat deine Zahl nicht erraten (sein Tipp war: {z}), er hat noch {(versuche-1)-i} Versuche")
        y = list(y)
print("Der Computer konnte deine Zahl nicht erraten")

if x==y:
    print("richtig")
else:
    print("verloren die Zahl war : %i" %y)
'''
import pygame

pygame.init()
pygame.mixer.init()
sound1 = pygame.mixer.Sound('Minecraft Eating.mp3')
deathsound = pygame.mixer.Sound('OOF.mp3')
portalsound = pygame.mixer.Sound('Nether Portal Travel Sound (Minecraft) - Sound Effect for editing.mp3')
x = [0]
y = [0]
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption(f'Snake current score: {len(x)}')
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 200, 0)
dark_green = (0, 100, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
amount_of_snake_boxes = (dis_height // snake_box) * (dis_width // snake_box)


x1_change = 0
y1_change = 0

number_of_fruits = int(input())
if number_of_fruits >= amount_of_snake_boxes:
    number_of_fruits = amount_of_snake_boxes-1

xf1 = (randrange(0, (dis_width // snake_box)) * snake_box) + (snake_box // 2)
yf1 = (randrange(0, (dis_height // snake_box)) * snake_box) + (snake_box // 2)
fruits = [(xf1, yf1)]
portals = []



def new_fruit():
    global x
    global y
    xnf = x
    ynf = y
    x_fruit = (randrange(0, (dis_width // snake_box)) * snake_box) + (snake_box // 2)
    y_fruit = (randrange(0, (dis_height // snake_box)) * snake_box) + (snake_box // 2)
    for f in fruits:
        if (x_fruit, y_fruit) == f:
            return new_fruit()
    for xy in snake1.get_snake_body():
        x, y = xy
        if (x + (snake_box // 2)) != x_fruit or (y + (snake_box // 2)) != y_fruit:
            continue
        else:
            return new_fruit()
    return x_fruit, y_fruit



for i in range(1, number_of_fruits):
    fruits.append(new_fruit())

portals.append(new_fruit())
portals.append(new_fruit())

def gone_through_portal():
    global x
    global y
    global portals
    xp1, yp1 = portals[0]
    xp2, yp2 = portals[1]
    if(x[0] + (snake_box // 2), y[0] + (snake_box // 2)) == portals[0]:
        x[0], y[0] = (xp2 - (snake_box//2)), (yp2 - (snake_box//2))
        return True
    elif(x[0] + (snake_box // 2), y[0] + (snake_box // 2)) == portals[1]:
        x[0], y[0] = (xp1 - (snake_box//2)), (yp1 - (snake_box//2))
        return True
    return False
#current_fruit = (x[0] + 3 * (snake_box // 2), y[0] + (snake_box // 2))

def has_eaten_a_fruit() -> bool:
    global fruits
    global x
    global y
    for i in range(0, len(fruits)):
        if (x[0] + (snake_box // 2), y[0] + (snake_box // 2)) == fruits[i]:
            pygame.mixer.Sound.stop(sound1)
            pygame.mixer.Sound.play(sound1)
            if amount_of_snake_boxes > (len(x) + len(fruits)):
                fruits[i] = new_fruit()
            else:
                del fruits[i]
            return True
    return False


def growing():
    x.append(x[0])
    y.append(y[0])
    pygame.display.set_caption(f'Snake current score: {len(x)}')


font_style = pygame.font.SysFont('Helvetica', 50)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 - mesg.get_height() / 2])

def draw_portal(x,y):
    portalcolors = [blue, purple]
    for i in range(snake_box//2, 0, -2):
        pygame.draw.circle(dis, portalcolors[(i//2)%2], (x,y), i)


def draw_fruit(xy):
    x_f, y_f = xy
    pygame.draw.circle(dis, red, xy, snake_box // 2)
    pygame.draw.rect(dis, green, pygame.Rect(x_f - snake_box // 10, y_f - ((snake_box // 3) * 2), snake_box // 5,
                                             (snake_box // 3) + 2))


clock = pygame.time.Clock()

game_over = False
current_event = None
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a and current_event != pygame.K_RIGHT:
                x1_change = -snake_box
                y1_change = 0
                current_event = pygame.K_LEFT
                break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and current_event != pygame.K_LEFT:
                x1_change = snake_box
                y1_change = 0
                current_event = pygame.K_RIGHT
                break
            elif event.key == pygame.K_UP or event.key == pygame.K_w and current_event != pygame.K_DOWN:
                x1_change = 0
                y1_change = -snake_box
                current_event = pygame.K_UP
                break
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s and current_event != pygame.K_UP:
                x1_change = 0
                y1_change = snake_box
                current_event = pygame.K_DOWN
                break
    # if x[0] >= dis_width or x[0] < 0 or y[0] > dis_height or y[0] <= 0:
    #game_over = True
    x[0] = (x[0] + x1_change) % dis_width
    y[0] = (y[0] + y1_change) % dis_height
    dis.fill(white)
    fruit = Fruit((100, 100))
    fruitgroup = pygame.sprite.Group()
    fruitgroup.add(fruit)
    fruitgroup.draw(dis)
    snake1 = Snake()
    snake1.draw(dis)
    for i in range(0, len(x)):
        pygame.draw.rect(dis, dark_green, pygame.Rect(x[i], y[i], snake_box, snake_box))
        pygame.draw.rect(dis, green,
                         pygame.Rect(x[i], y[i], snake_box - (snake_box // 10), snake_box - (snake_box // 10)))
    for j in range(1, len(x)):
        if x[0] == x[j] and y[0] == y[j]:
            game_over = True
    for i in range(len(x) - 1, 0, -1):
        x[i] = x[i - 1]
        y[i] = y[i - 1]

    if has_eaten_a_fruit():
        growing()
    for i in fruits:
        draw_fruit(i)
    for i in portals:
        xp, yp = i
        draw_portal(xp,yp)
    if(gone_through_portal()):
        pygame.mixer.Sound.stop(portalsound)
        pygame.mixer.Sound.play(portalsound)
    pygame.display.flip()
    clock.tick(snakespeed)
dis.fill(white)
message("Du bist gestorben", red)
pygame.mixer.Sound.play(deathsound)
pygame.display.flip()
pygame.time.wait(1000)
pygame.quit()
quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
