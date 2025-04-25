import enum


class Gamestate(enum.Enum):
    MAIN_MENU = 0
    GAME = 1
    PAUSED = 2
    GAME_OVER = 3
    FRUIT_MENU = 4
    REPLAY = 5
