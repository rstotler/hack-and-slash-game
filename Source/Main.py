import pygame, Config
from pygame import *
from Data import Main

# Initialize Game Window #
window = pygame.display.set_mode(Config.SCREEN_SIZE, False, 32)
pygame.display.set_caption(Config.TITLE + " " + Config.VERSION)
clock = pygame.time.Clock()
main = Main.Main(window)

while True:
    lastTick = clock.tick(60) / 1000.0
    main.updateMain(str(clock.get_fps())[0:5], window)

