import pygame, os, pickle, Utility, Config
from pygame import *

class Data:

    def __init__(self):
        self.frameTickDict, self.offsetDict = self.loadDataDicts()
        
    def loadDataDicts(self):
    
        frameTickDict = {}
        offsetDict = {}
        
        for filename in os.listdir("../Image/Mob"):
            if filename[0:13] != "Stunned_Stars":
                idNum = int(filename[0:filename.index("_")])
                if idNum not in frameTickDict:
                    frameTickDict[idNum] = {}
                    offsetDict[idNum] = {}
                imageType = filename[filename.index("_") + 1:filename.rindex("_")]
                if imageType not in frameTickDict[idNum]:
                    frameTickDict[idNum][imageType] = []
                    offsetDict[idNum][imageType] = {"Left":[], "Right":[]}
                for facingDir in ["Left", "Right"]:
                    offsetDict[idNum][imageType][facingDir].append([0, 0])
                frameTickDict[idNum][imageType].append(4)
        
        return frameTickDict, offsetDict

    def saveData(self):
        with open("SpriteOffsetData.txt", "wb") as file:
            dataObject = [self.offsetDict, self.frameTickDict]
            pickle.dump(dataObject, file, protocol=pickle.HIGHEST_PROTOCOL)
    
class Main:

    def __init__(self):
    
        # Window Variables #
        self.window = pygame.display.set_mode([420, 420], False, 32)
        pygame.display.set_caption("BattleSim Sprite Rigger")
        self.clock = pygame.time.Clock()
        self.control = False
        self.shift = False
        self.windowLoc = [0, 0]
        self.pause = True
        self.label = None
        self.labelTimer = -1
        self.labelAlpha = 255
        self.displayLines = True
        self.frameSkipNum = 1
        
        # Sprite Variables #
        self.id = 2
        self.imageType = "Normal"
        self.facingDir = "Left"
        self.animationFrame = 0
        self.frameTick = 0
        
        self.imageDict = self.loadImageDict()
        self.rectList = self.loadRectList()
        self.data = Data()
        self.loadData()
        
    def loadImageDict(self):
    
        imageDict = {}
        
        for filename in os.listdir("../Image/Mob"):
            if filename[0:13] != "Stunned_Stars":
                idNum = int(filename[0:filename.index("_")])
                if idNum not in imageDict:
                    imageDict[idNum] = {}
                imageType = filename[filename.index("_") + 1:filename.rindex("_")]
                if imageType not in imageDict[idNum]:
                    imageDict[idNum][imageType] = {"Left":[], "Right":[]}
                for facingDir in ["Left", "Right"]:
                    targetImage = pygame.image.load("../Image/Mob/" + filename).convert_alpha()
                    if facingDir == "Right":
                        targetImage = pygame.transform.flip(targetImage, True, False)
                    
                    imageDict[idNum][imageType][facingDir].append(targetImage)
        
        return imageDict
        
    def loadRectList(self):
    
        rectList = []
        
        rectPracticeDummy = pygame.Rect([140, 140], [51, 111])
        rectList.append(rectPracticeDummy)
        rectBat = pygame.Rect([140, 140], [47, 31])
        rectList.append(rectBat)
        rectMedusa = pygame.Rect([140, 140], [56, 110])
        rectList.append(rectMedusa)
        
        return rectList
        
    def loadData(self):
        try:
            with open("SpriteData.txt", "rb") as file:
                self.data = pickle.load(file)
            self.label = Utility.getLabel("Data Loaded!", [255, 255, 255], Config.FONT_ROMAN_16)
            self.labelTimer = 0
            self.labelAlpha = 255
        except:
            pass
        
    def processInput(self):
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                raise SystemExit
            elif event.type == KEYDOWN and event.key in [K_LCTRL, K_RCTRL]:
                self.control = True
            elif event.type == KEYUP and event.key in [K_LCTRL, K_RCTRL]:
                self.control = False
            elif event.type == KEYDOWN and event.key in [K_LSHIFT, K_RSHIFT]:
                self.shift = True
            elif event.type == KEYUP and event.key in [K_LSHIFT, K_RSHIFT]:
                self.shift = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.pause = not self.pause
                
            # Increment Frame Skip Num #
            elif event.type == KEYDOWN and event.key == 102:
                self.frameSkipNum += 1
                if self.frameSkipNum >= 6:
                    self.frameSkipNum = 1
                
            # Toggle Lines #
            elif event.type == KEYDOWN and event.key == 1073741882:
                self.displayLines = not self.displayLines
                
            # Switch Facing Direction #
            elif event.type == KEYDOWN and event.key == 100:
                if self.facingDir == "Left":
                    self.facingDir = "Right"
                else:
                    self.facingDir = "Left"
                    
            # Save Data #
            elif event.type == KEYDOWN and self.shift and event.key == 115:
                self.data.saveData()
                self.label = Utility.getLabel("Data Saved!", [255, 255, 255], Config.FONT_ROMAN_16)
                self.labelTimer = 0
                self.labelAlpha = 255
        
            # Switch Image Type #
            elif event.type == KEYDOWN and event.key == 116:
                self.animationFrame = 0
                if self.imageType == "Normal" and "Attack_Warmup" in self.data.offsetDict[self.id]:
                    self.imageType = "Attack_Warmup"
                elif self.imageType == "Attack_Warmup" and "Attack" in self.data.offsetDict[self.id]:
                    self.imageType = "Attack"
                else:
                    self.imageType = "Normal"
             
            # Scroll Window Location #
            elif self.control and self.shift and event.type == KEYDOWN and event.key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]:
                if event.key in [K_LEFT, K_UP]:
                    scrollMod = -5
                else:
                    scrollMod = 5
                    
                if event.key in [K_LEFT, K_RIGHT]:
                    self.windowLoc[0] += scrollMod
                    for r in self.rectList:
                        r.left += scrollMod
                else:
                    self.windowLoc[1] += scrollMod
                    for r in self.rectList:
                        r.top += scrollMod
                
            # Scroll Sprite ID #
            elif self.shift and event.type == KEYDOWN and event.key in [K_LEFT, K_RIGHT]:
                self.animationFrame = 0
                self.frameTick = 0
                if event.key == K_LEFT:
                    self.id -= 1
                    if self.id < 0:
                        self.id = len(self.imageDict) - 1
                elif event.key == K_RIGHT:
                    self.id += 1
                    if self.id == len(self.imageDict):
                        self.id = 0
                if self.imageType not in self.data.offsetDict[self.id]:
                    self.imageType = list(self.data.offsetDict[self.id].keys())[0]
                        
            # Change X & Y Offset #
            elif self.control and event.type == KEYDOWN and event.key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]:
                if event.key == K_LEFT:
                    self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][0] -= 1
                elif event.key == K_RIGHT:
                    self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][0] += 1
                elif event.key == K_UP:
                    self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][1] -= 1
                elif event.key == K_DOWN:
                    self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][1] += 1
                        
            # Scroll Animation Frame #
            elif self.pause and event.type == KEYDOWN and event.key in [K_LEFT, K_RIGHT]:
                self.frameTick = 0
                if event.key == K_LEFT:
                    self.animationFrame -= self.frameSkipNum
                    if self.animationFrame < 0:
                        self.animationFrame = len(self.imageDict[self.id][self.imageType][self.facingDir]) - 1
                elif event.key == K_RIGHT:
                    self.animationFrame += self.frameSkipNum
                    if self.animationFrame >= len(self.imageDict[self.id][self.imageType][self.facingDir]):
                        self.animationFrame = 0
        
            # Adjust Frame Tick #
            elif event.type == KEYDOWN and event.key in [K_UP, K_DOWN]:
                if event.key == K_UP:
                    self.data.frameTickDict[self.id][self.imageType][self.animationFrame] += 1
                elif event.key == K_DOWN and self.data.frameTickDict[self.id][self.imageType][self.animationFrame] > 1:
                    self.data.frameTickDict[self.id][self.imageType][self.animationFrame] -= 1
     
    def drawScreen(self):
        self.window.fill([0, 0, 100])
        
        if self.displayLines:
            pygame.draw.line(self.window, [255, 255, 0], [140 + self.windowLoc[0], 0], [140 + self.windowLoc[0], 420], 1) # Vertical Line #
            pygame.draw.line(self.window, [255, 255, 0], [0, 140 + self.windowLoc[1]], [420, 140 + self.windowLoc[1]], 1) # Horizontal Line #
        
        # Debug Info (Top Left) #
        if True:
            Utility.write("ID: " + str(self.id), [0, 0], [255, 255, 255], Config.FONT_ROMAN_16, self.window)
            Utility.write("Type: " + str(self.imageType) + " (" + str(self.facingDir) + ")", [0, 13], [255, 255, 255], Config.FONT_ROMAN_16, self.window)
            Utility.write("Frame: " + str(self.animationFrame + 1) + " [" + str(len(self.data.offsetDict[self.id][self.imageType][self.facingDir])) + "] (" + str(self.data.frameTickDict[self.id][self.imageType][self.animationFrame]) + ") " + str(self.frameSkipNum), [0, 26], [255, 255, 255], Config.FONT_ROMAN_16, self.window)
            strOffset = str(self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame])
            Utility.write("Offset: " + strOffset, [0, 39], [255, 255, 255], Config.FONT_ROMAN_16, self.window)
            strPlayMode = "Play"
            if self.pause : strPlayMode = "Pause"
            Utility.write("Mode: " + strPlayMode, [0, 52], [255, 255, 255], Config.FONT_ROMAN_16, self.window)
                
        # Draw Sprite #
        targetImage = self.imageDict[self.id][self.imageType][self.facingDir][self.animationFrame]
        xOffset = self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][0]
        yOffset = self.data.offsetDict[self.id][self.imageType][self.facingDir][self.animationFrame][1]
        self.window.blit(targetImage, [140 + self.windowLoc[0] + xOffset, 140 + self.windowLoc[1] + yOffset])
        
        if self.displayLines:
            spriteRect = targetImage.get_rect()
            spriteRect.left = self.rectList[self.id].left + xOffset
            spriteRect.top = self.rectList[self.id].top + yOffset
            pygame.draw.rect(self.window, [255, 0, 255], spriteRect, 1)
            pygame.draw.rect(self.window, [255, 0, 0], self.rectList[self.id], 1)
        
        if self.label != None:
            self.window.blit(self.label, [0, 407])
        
    def updateData(self):
        self.frameTick += 1
        if self.frameTick >= self.data.frameTickDict[self.id][self.imageType][self.animationFrame]:
            self.frameTick = 0
            self.animationFrame += 1
            if self.animationFrame >= len(self.imageDict[self.id][self.imageType][self.facingDir]):
                self.animationFrame = 0
                
main = Main()
while True:
    if main.pause == False:
        main.clock.tick(60)
    main.processInput()
    main.drawScreen()
    if main.pause == False:
        main.updateData()
        
    if main.labelTimer >= 0:
        main.labelTimer += 1
        if main.labelTimer % 4 == 0:
            main.labelAlpha -= 1
            main.label.set_alpha(main.labelAlpha)
        
        if main.labelTimer >= 2000:
            main.label = None
            main.labelTimer = -1
        
    pygame.display.update()
