import pygame

def message(dis, msg, color = (255,255,255), pos = (0,0), font_size = 50, font_style = 'Arial', opacity = 255):
    x,y = pos
    mesg = pygame.font.SysFont(font_style, font_size).render(msg, True, color)
    mesg.set_alpha(opacity)
    dis.blit(mesg, [x - mesg.get_width() / 2, y - mesg.get_height() / 2])

def draw_pause_overlay(screen, opacity):
    # Erstelle eine neue Surface mit der gleichen Größe wie das Display
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    # Wähle eine Farbe und setze den Alpha-Wert
    overlay.fill((0, 0, 0, opacity))  # Halbtransparentes Schwarz

    # Blitte die Overlay-Surface auf das Display
    screen.blit(overlay, (0, 0))
    message(screen, "paused",(255,255,255), (screen.get_width()//2,screen.get_height()//2), 100, "Arial", opacity)



