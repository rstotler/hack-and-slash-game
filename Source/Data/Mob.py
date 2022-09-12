import pygame, random, Config
from pygame import *

class Mob:
	
    def __init__(self, ID, LOCATION):
        
        self.id = ID
        self.title = "Default Title"
        self.currentHP = 10
        self.maxHP = self.currentHP
        
        self.maxMoveDistance = 500
        self.facingDir = random.choice(["Left", "Right"])
        
        self.collideShape = "Rectangle"
        self.rect = None
        self.timerDict = {"Movement Cooldown": random.randrange(60, 180), "Attack Cooldown": random.randrange(60, 180)}
        
        self.loadMob(ID, LOCATION)
        
    def loadMob(self, ID, LOCATION):
    
        if ID == 0:
            self.title = "A Practice Dummy"
            self.currentHP = 1500
            self.rect = pygame.Rect([[0, 0], [51, 111]])
            del self.timerDict["Movement Cooldown"]
            del self.timerDict["Attack Cooldown"]
            
        elif ID == 1:
            self.title = "A Bat"
            self.currentHP = 25
            self.rect = pygame.Rect([[0, 0], [47, 31]])
            self.timerDict["Animation"] = 0
            self.timerDict["Animation Frame"] = 0
            
        elif ID == 2:
            self.title = "Medusa"
            self.currentHP = 1000
            self.rect = pygame.Rect([[0, 0], [56, 110]])
            self.timerDict["Animation"] = 0
            self.timerDict["Animation Frame"] = 0
            
        self.maxHP = self.currentHP
    
        # Set Location #
        if isinstance(LOCATION[0], int) : self.rect.left = LOCATION[0]
        else : self.rect.left = random.randrange(Config.SCREEN_SIZE[0] - self.rect.width)
        if isinstance(LOCATION[1], int) : self.rect.top = LOCATION[1]
        else : self.rect.top = random.randrange(int(Config.SCREEN_SIZE[1] * .35) - self.rect.height, Config.SCREEN_SIZE[1] - self.rect.height)
        