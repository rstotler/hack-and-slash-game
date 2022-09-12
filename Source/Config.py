import pygame, os
from pygame import *
pygame.init()

TITLE = "Battle Sim"
VERSION = "V0.131"
SCREEN_SIZE = [420, 700]
WINDOW_RECT = pygame.Rect([[0, 0], SCREEN_SIZE])
ALPHABET_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PAUSE_GAME = False
MAX_ATTACKS = 5
MAX_ATTACK_DISTANCE = 200
MAX_ATTACK_POINTS = 7
MAX_PLAYER_BLOCK_TIME = 70
MAX_MOB_STUN_LEGNTH = 150

# Fonts #
FONT_ROMAN_40 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 40)
FONT_ROMAN_25 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 25)
FONT_ROMAN_16 = pygame.font.Font(os.path.dirname(os.getcwd()) + "/Font/CodeNewRomanB.otf", 16)
