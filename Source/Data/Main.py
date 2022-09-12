import pygame, random, Config
from pygame import *
from Data import Game
from Hardware import Mouse, Keyboard
from Screen import Screen

class Main:

    def __init__(self, WINDOW):
    
        self.displayLevel = ""
        self.mouse = Mouse.Mouse()
        self.keyboard = Keyboard.Keyboard()
        self.screen = Screen.Screen()
        self.dataGame = Game.Game()
        
        self.loadBattle(True)
        
    def loadBattle(self, LOAD_SURFACES=False):
        
        # Load Screen Related Game Data #
        self.displayLevel = "Battle"
        self.dataGame.player.currentHP = self.dataGame.player.maxHP
        self.dataGame.player.currentAttackCharges = self.dataGame.player.maxAttackCharges
        self.dataGame.battle.mobList = []
        self.dataGame.battle.deathAnimationList = []
        self.dataGame.battle.timerDict = {}
        
        self.dataGame.battle.spawnMob(1)
        self.dataGame.battle.spawnMob(2)
        
        # Load Images After Game Data #
        self.screen.drawDict = {"All": True}
        self.screen.timerDict = {"Background Scroll": 0, "Background Scroll X Loc": 0, "Player Hit Alpha": [0, 0, 0, 0], "Player Hit Alpha Timer": [0, 0, 0, 0], "Player Hit Alpha Index": 0}
        self.screen.loadImageDict(self.dataGame, self.displayLevel)
        if LOAD_SURFACES:
            self.screen.loadSurfaceDict(self.displayLevel)
        
        # Randomize Mob Start Animation Frames #
        for mobData in self.dataGame.battle.mobList:
            if "Animation" in mobData.timerDict:
                mobImageCount = 1
                if mobData.id in self.screen.imageDict["Mobs"]:
                    mobImageCount = len(self.screen.imageDict["Mobs"][mobData.id]["Normal"]["Normal"][mobData.facingDir])
                mobData.timerDict["Animation Frame"] = random.randrange(mobImageCount)
                
        # Redraw Surfaces Last #
        self.screen.redrawSurface("Battle", "All", {"Player Data": self.dataGame.player, "Mob List": self.dataGame.battle.mobList})
	
    def updateMain(self, FPS, WINDOW):
        
		# Update Game/Screen Data, Process User Input #
        if not Config.PAUSE_GAME:
            self.dataGame.update(self.mouse, self.screen, self.displayLevel)
            self.screen.update(self.dataGame.player, self.displayLevel)
        self.processInput(WINDOW)
		
		# Draw Screen #
        self.screen.draw(FPS, WINDOW, self.mouse, self.displayLevel, self.dataGame)
        pygame.display.update(self.screen.drawRectList)
        self.screen.drawRectList = []

    def processInput(self, WINDOW):
	
        for event in pygame.event.get():
		
            # Quit Event #
            if event.type == QUIT:
                raise SystemExit
        
            # Mouse Events #
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse.clickLeft = True
                    
                    if self.displayLevel == "Battle":
                        self.dataGame.battle.leftClickDown(self.mouse, self.dataGame.player)
                        self.screen.drawDict["Attack Lines"] = True
                        
                    #if self.mouse.hoverElement != None:
                    #    self.mouse.clickElement = self.mouse.hoverElement
                    
                elif event.button == 3:
                    self.mouse.clickRight = True
				
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse.clickLeft = False
                    
                    if self.displayLevel == "Battle":
                        self.dataGame.battle.leftClickUp(self.mouse, self.screen, self.dataGame.player)
                    
                    #if self.mouse.clickElement != None:
                    #    if self.mouse.hoverElement == self.mouse.clickElement:
                    #        self.clickElement(WINDOW, self.mouse.clickElement)
                    #    self.mouse.clickElement = None
                    
                elif event.button == 3:
                    self.mouse.clickRight = False
		
            elif event.type == MOUSEMOTION:
                self.mouse.updatePosition(WINDOW, self.getElementList())
				
            # Keyboard Events #
            elif event.type == KEYDOWN:
                keyName = pygame.key.name(event.key)
				
                # Escape #
                if event.key == K_ESCAPE : raise SystemExit
				
                # Shift, Control, & Backspace #
                elif event.key in [K_LSHIFT, K_RSHIFT] and self.keyboard.shift == False : self.keyboard.shift = True
                elif event.key in [K_LCTRL, K_RCTRL] and self.keyboard.control == False : self.keyboard.control = True
                elif event.key == K_BACKSPACE and self.keyboard.backspace == False : self.keyboard.backspace = True
				
                # Enter #
                elif keyName == "return":
                    
                    # Reset Battle #
                    if self.displayLevel == "Battle":
                        self.loadBattle()
                    
                elif keyName == "space":
                
                    # Player Block #
                    if self.displayLevel == "Battle":
                        self.dataGame.battle.playerBlock(self.mouse, self.screen, self.dataGame.player)
                        
                # Arrow Keys - Up/Down/Left/Right #
                elif keyName in ["up", "down", "left", "right"]:
                    pass
                    
                # Other Input #
                else:
                    pass
				
            elif event.type == KEYUP:
                pressedKeys = pygame.key.get_pressed()
                if self.keyboard.shift and ((event.key == K_LSHIFT and not pressedKeys[pygame.K_RSHIFT]) or (event.key == K_RSHIFT and not pressedKeys[pygame.K_LSHIFT])) : self.keyboard.shift = False
                elif self.keyboard.control and ((event.key == K_LCTRL and not pressedKeys[pygame.K_RCTRL]) or (event.key == K_RCTRL and not pressedKeys[pygame.K_LCTRL])) : self.keyboard.control = False
                elif event.key == K_BACKSPACE and self.keyboard.backspace == True : self.keyboard.backspace = False
		
    def getElementList(self):
    
        elementList = []
    
        if self.displayLevel == "Battle":
            elementList = elementList + self.dataGame.battle.mobList
        
        return elementList
       