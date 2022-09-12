import pygame, os, pickle, Config, Utility
from pygame import *

class Screen:

    def __init__(self):

        self.imageDict = {}
        self.surfaceDict = {}
        self.offsetDict = {}
        
        self.drawDict = {}
        self.drawRectList = []
        self.timerDict = {}
        
    def loadImageDict(self, DATA_GAME, DISPLAY_LEVEL):
        
        if DISPLAY_LEVEL == "Battle":
        
            # Background #
            if "Background Top" not in self.imageDict or "Background Bottom" not in self.imageDict:
                imageBackgroundTop = pygame.image.load("../Image/Background/Field_Top.png").convert()
                self.imageDict["Background Top"] = pygame.Surface([imageBackgroundTop.get_rect().width * 2, imageBackgroundTop.get_rect().height])
                self.imageDict["Background Top"].blit(imageBackgroundTop, [0, 0])
                self.imageDict["Background Top"].blit(imageBackgroundTop, [imageBackgroundTop.get_rect().width, 0])
                self.imageDict["Background Bottom"] = pygame.image.load("../Image/Background/Field_Bottom.png").convert_alpha()
            
            # Mobs #
            if True:
                if "Mobs" not in self.imageDict:
                    self.imageDict["Mobs"] = {}
                    
                # Get File Load/Delete Data #
                mobIDList = []
                for mobData in DATA_GAME.battle.mobList:
                    if mobData.id not in mobIDList:
                        mobIDList.append(mobData.id)
                mobImageDataDict = {}
                for filename in os.listdir("../Image/Mob"):
                    if filename[0:13] != "Stunned_Stars":
                        idNum = int(filename[0:filename.index("_")])
                        if idNum in mobIDList and idNum not in self.imageDict["Mobs"]:
                            if idNum not in mobImageDataDict:
                                mobImageDataDict[idNum] = {}
                            imageType = filename[filename.index("_") + 1:filename.rindex("_")]
                            if imageType not in mobImageDataDict[idNum]:
                                mobImageDataDict[idNum][imageType] = 1
                            else:
                                mobImageDataDict[idNum][imageType] += 1
                
                # Load Images #
                for mobID in mobImageDataDict:
                    self.imageDict["Mobs"][mobID] = {}
                    for imageType in mobImageDataDict[mobID]:
                        self.imageDict["Mobs"][mobID][imageType] = {}
                        for subImageType in ["Normal", "Hit", "Flash", "After Image 1", "After Image 2"]:
                            self.imageDict["Mobs"][mobID][imageType][subImageType] = {}
                            for facingDir in ["Left", "Right"]:
                                self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir] = []
                                
                                if imageType in mobImageDataDict[mobID]:
                                    for imageNum in range(mobImageDataDict[mobID][imageType]):
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.image.load("../Image/Mob/" + str(mobID) + "_" + imageType + "_" + str(imageNum) + ".png").convert_alpha())
                                        if subImageType == "Hit":
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([255, 0, 0], None, pygame.BLEND_RGB_ADD)
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([0, 100, 100], None, pygame.BLEND_RGB_SUB)
                                        elif subImageType == "Flash":
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([255, 255, 255], None, pygame.BLEND_RGB_ADD)
                                        elif subImageType == "After Image 1":
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([100, 100, 0], None, pygame.BLEND_RGB_SUB)
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].set_alpha(200)
                                        elif subImageType == "After Image 2":
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([200, 200, 0], None, pygame.BLEND_RGB_SUB)
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].set_alpha(100)
                                        if facingDir == "Right":
                                            self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1] = pygame.transform.flip(self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1], True, False)
                                            
                                else:
                                    self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.Surface([mobData.rect.width, mobData.rect.height]))
                                    self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([150, 150, 150])
                                    if subImageType == "Hit":
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.Surface([mobData.rect.width, mobData.rect.height]))
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([50, 50, 50])
                                    elif subImageType == "Flash":
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.Surface([mobData.rect.width, mobData.rect.height]))
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([250, 250, 250])
                                    elif subImageType == "After Image 1":
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.Surface([mobData.rect.width, mobData.rect.height]))
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([150, 150, 150])
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([100, 100, 0], None, pygame.BLEND_RGB_SUB)
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].set_alpha(200)
                                    elif subImageType == "After Image 2":
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir].append(pygame.Surface([mobData.rect.width, mobData.rect.height]))
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([150, 150, 150])
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].fill([200, 200, 0], None, pygame.BLEND_RGB_SUB)
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1].set_alpha(100)
                                    if facingDir == "Right":
                                        self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1] = pygame.transform.flip(self.imageDict["Mobs"][mobID][imageType][subImageType][facingDir][-1], True, False)
                                        
                # Delete Unused Mob Images #
                delMobImageList = []
                for mobID in self.imageDict["Mobs"]:
                    if mobID not in mobIDList:
                        delMobImageList.append(mobID)
                delMobImageList.reverse()
                for mobID in delMobImageList:
                    del self.imageDict["Mobs"][mobID]
                                              
                self.imageDict["Mobs"]["Stunned Stars"] = []
                for i in range(4):
                    imageStunStar = pygame.image.load("../Image/Mob/Stunned_Stars_" + str(i) + ".png").convert_alpha()
                    self.imageDict["Mobs"]["Stunned Stars"].append(imageStunStar)
                     
            # User Interface #
            if "UI" not in self.imageDict:
                self.imageDict["UI"] = {}
                self.imageDict["UI"]["Sword Active"] = pygame.image.load("../Image/UI/Sword.png").convert_alpha()
                self.imageDict["UI"]["Sword Inactive"] = pygame.image.load("../Image/UI/Sword.png").convert_alpha()
                self.imageDict["UI"]["Sword Inactive"].set_alpha(170)
                self.imageDict["UI"]["Shield Active"] = pygame.image.load("../Image/UI/Shield.png").convert_alpha()
                self.imageDict["UI"]["Shield Inactive"] = pygame.image.load("../Image/UI/Shield.png").convert_alpha()
                self.imageDict["UI"]["Shield Inactive"].set_alpha(170)
                self.imageDict["UI"]["Healthbar Outline"] = pygame.image.load("../Image/UI/Healthbar_Outline.png").convert_alpha()
                self.imageDict["UI"]["Healthbar Fill"] = pygame.image.load("../Image/UI/Healthbar_Fill.png").convert()
                
                self.imageDict["UI"]["Player Hit Alpha"] = []
                for i in range(4):
                    self.imageDict["UI"]["Player Hit Alpha"].append([])
                    for ii in range(4):
                        splatterImage = pygame.image.load("../Image/UI/Blood_Splatter_" + str(i + 1) + ".png").convert_alpha()
                        splatterImage.set_alpha(62 * (3 - ii))
                        self.imageDict["UI"]["Player Hit Alpha"][-1].append(splatterImage)
             
        # Load Sprite Offset Data Dict #
        file = open("../Source/Data/SpriteOffsetData.txt", "rb")
        fileData = pickle.load(file)
        file.close()
        
        self.offsetDict = fileData[0]
             
    def loadSurfaceDict(self, DISPLAY_LEVEL):
    
        self.surfaceDict = {}
    
        if DISPLAY_LEVEL == "Battle":
            self.surfaceDict["Background"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["Mob After Images"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["Mobs"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["Mob Animations"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["Field Messages"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["UI"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            
            self.surfaceDict["Attack Lines"] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
            self.surfaceDict["Attack Lines List"] = []
            for i in range(Config.MAX_ATTACKS):
                self.surfaceDict["Attack Lines List"].append([])
                self.surfaceDict["Attack Lines List"][-1] = pygame.Surface(Config.SCREEN_SIZE, pygame.SRCALPHA, 32)
    
    def update(self, PLAYER, DISPLAY_LEVEL):
        
        if "Background Scroll" in self.timerDict:
            self.timerDict["Background Scroll"] += 1
            if self.timerDict["Background Scroll"] >= 120:
                self.timerDict["Background Scroll"] = 0
                self.timerDict["Background Scroll X Loc"] -= 1
                if "Background Top" in self.imageDict and self.timerDict["Background Scroll X Loc"] < -(self.imageDict["Background Top"].get_rect().width / 2):
                    self.timerDict["Background Scroll X Loc"] = 0
                self.drawDict["Background Top"] = True
                self.redrawSurface(DISPLAY_LEVEL, "Background Top", {"Player Data": PLAYER})
              
    def redrawSurface(self, DISPLAY_LEVEL, TARGET_SURFACE, FLAGS={}):
    
        if DISPLAY_LEVEL == "Battle":
        
            if TARGET_SURFACE in ["Background", "All"]:
                backgroundTopX = 0
                if "Background Scroll X Loc" in self.timerDict:
                    backgroundTopX = self.timerDict["Background Scroll X Loc"]
                self.surfaceDict["Background"].blit(self.imageDict["Background Top"], [backgroundTopX, 0])
                self.surfaceDict["Background"].blit(self.imageDict["Background Bottom"], [0, 0])
                
            elif TARGET_SURFACE == "Background Top":
                backgroundTopX = 0
                if "Background Scroll X Loc" in self.timerDict:
                    backgroundTopX = self.timerDict["Background Scroll X Loc"]
                self.surfaceDict["Background"].blit(self.imageDict["Background Top"], [backgroundTopX, 0])
                self.surfaceDict["Background"].blit(self.imageDict["Background Bottom"], [0, 0])
            
            if TARGET_SURFACE in ["Mob Animations", "All"]:
                self.surfaceDict["Mob Animations"].fill(0)
                if "Mob Animation List" in FLAGS:
                    for animationData in FLAGS["Mob Animation List"]:
                        if animationData.type == "Fade":
                            locSurface = [animationData.location[0] + animationData.flags["Sprite Offset"][0], animationData.location[1] + animationData.flags["Sprite Offset"][1]]
                            self.surfaceDict["Mob Animations"].blit(animationData.surfaceDict["Normal"], locSurface)
                        elif animationData.type == "Split":
                            locSurface1 = [animationData.location[0] - animationData.flags["X Mod"] + animationData.flags["Sprite Offset"][0], animationData.location[1] - animationData.flags["Y Mod"] + animationData.flags["Sprite Offset"][1]]
                            locSurface2 = [animationData.location[0] + animationData.flags["X Mod"] + animationData.flags["Sprite Offset"][0], animationData.location[1] + animationData.flags["Y Mod"] + animationData.flags["Sprite Offset"][1]]
                            self.surfaceDict["Mob Animations"].blit(animationData.surfaceDict["Split 1"], locSurface1)
                            self.surfaceDict["Mob Animations"].blit(animationData.surfaceDict["Split 2"], locSurface2)
            
            if TARGET_SURFACE in ["Mob After Images", "All"]:
                self.surfaceDict["Mob After Images"].fill(0)
                if "Mob After Image List" in FLAGS:
                    for afterImageData in FLAGS["Mob After Image List"]:
                        surfaceAfterImage = self.imageDict["Mobs"][afterImageData.id]["Normal"][afterImageData.getFadeLevel()][afterImageData.facingDir][afterImageData.animationFrame]
                        spriteOffset = self.offsetDict[afterImageData.id]["Normal"][afterImageData.facingDir][afterImageData.animationFrame]
                        self.surfaceDict["Mob After Images"].blit(surfaceAfterImage, [afterImageData.location[0] + spriteOffset[0], afterImageData.location[1] + spriteOffset[1]])
                
            if TARGET_SURFACE in ["Mobs", "All"]:
                self.surfaceDict["Mobs"].fill(0)
                if "Mob List" in FLAGS:
                    for mobData in FLAGS["Mob List"]:
                        animationFrame = 0
                        if "Animation Frame" in mobData.timerDict:
                            animationFrame = mobData.timerDict["Animation Frame"]
                        mobImage = self.imageDict["Mobs"][mobData.id]["Normal"]["Normal"][mobData.facingDir][animationFrame]
                        if "Sprite Hit" in mobData.timerDict:
                            mobImage = self.imageDict["Mobs"][mobData.id]["Normal"]["Hit"][mobData.facingDir][animationFrame]
                        elif "Attack Flash" in mobData.timerDict and mobData.timerDict["Attack Flash"] in [0, 1, 2, 3, 8, 9, 10, 11, 28, 29, 30, 31]:
                            mobImage = self.imageDict["Mobs"][mobData.id]["Normal"]["Flash"][mobData.facingDir][animationFrame]
                        spriteOffset = self.offsetDict[mobData.id]["Normal"][mobData.facingDir][animationFrame]
                        self.surfaceDict["Mobs"].blit(mobImage, [mobData.rect.left + spriteOffset[0], mobData.rect.top + spriteOffset[1]])
                        
                        if "Stunned Animation" in mobData.timerDict:
                            stunnedStarsXMod = int(abs(mobData.rect.width - 59) / 2)
                            invertXMod = 1
                            if mobData.rect.width < 59 : invertXMod = -1
                            self.surfaceDict["Mobs"].blit(self.imageDict["Mobs"]["Stunned Stars"][mobData.timerDict["Stunned Animation Frame"]], [mobData.rect.left + stunnedStarsXMod * invertXMod, mobData.rect.top - 29])
            
                        # Draw Mob Rect #
                        #pygame.draw.rect(self.surfaceDict["Mobs"], [255, 0, 0], mobData.rect, 1)
                        pass
                
            if TARGET_SURFACE in ["Field Messages", "All"]:
                self.surfaceDict["Field Messages"].fill(0)
                if "Field Messages" in FLAGS:
                    for fieldMessage in FLAGS["Field Messages"]:
                        self.surfaceDict["Field Messages"].blit(fieldMessage.surface, fieldMessage.location)
                    
            if TARGET_SURFACE == "Attack Lines":
                self.surfaceDict["Attack Lines"].fill(0)
                for i in range(Config.MAX_ATTACKS):
                    if "Attack Line Surface Index List" not in FLAGS or i in FLAGS["Attack Line Surface Index List"]:
                        self.surfaceDict["Attack Lines"].blit(self.surfaceDict["Attack Lines List"][i], [0, 0])
                  
            if TARGET_SURFACE in ["UI", "All"]:
                self.surfaceDict["UI"].fill(0)
                
                if False:
                    if "Player Data" in FLAGS and FLAGS["Player Data"].currentHP >= 0:
                        totalHealthbarWidth = 244
                        currentHealthbarWidth = totalHealthbarWidth * (FLAGS["Player Data"].currentHP / FLAGS["Player Data"].maxHP)
                        surfaceHealthbarFill = pygame.transform.scale(self.imageDict["UI"]["Healthbar Fill"], [currentHealthbarWidth, 34])
                        self.surfaceDict["UI"].blit(surfaceHealthbarFill, [59, 644])
                    self.surfaceDict["UI"].blit(self.imageDict["UI"]["Healthbar Outline"], [10, 630])
                
                # Slow, Temporary Writing (Redundantly Generates New Surfaces-Fix) #
                if "Player Data" in FLAGS:
                    strPlayerHP = "HP:" + str(FLAGS["Player Data"].currentHP)
                    Utility.write(strPlayerHP, [10, Config.SCREEN_SIZE[1] - 50], [255, 255, 255], Config.FONT_ROMAN_40, self.surfaceDict["UI"])
                    strAttackCharges = str(FLAGS["Player Data"].currentAttackCharges)
                    Utility.write(strAttackCharges, [310, Config.SCREEN_SIZE[1] - 50], [255, 255, 255], Config.FONT_ROMAN_40, self.surfaceDict["UI"])
                
                if "Player Block" in FLAGS:
                    self.surfaceDict["UI"].blit(self.imageDict["UI"]["Sword Inactive"], [340, 620])
                    self.surfaceDict["UI"].blit(self.imageDict["UI"]["Shield Active"], [348, 628])
                else:
                    if "Player Block Cooldown" not in FLAGS:
                        self.surfaceDict["UI"].blit(self.imageDict["UI"]["Shield Inactive"], [348, 628])
                    self.surfaceDict["UI"].blit(self.imageDict["UI"]["Sword Active"], [340, 620])
                    
                #if "Player Hit Alpha" in FLAGS:
                #    for hitAlphaIndex in FLAGS["Player Hit Alpha"]:
                #        self.surfaceDict["UI"].blit(self.imageDict["UI"]["Player Hit Alpha"][hitAlphaIndex][FLAGS["Player Hit Alpha"][hitAlphaIndex]], [0, 0])
                        
    def draw(self, FPS, WINDOW, MOUSE, DISPLAY_LEVEL, DATA_GAME):
    
        if len(self.drawDict) > 0:
            if "All" in self.drawDict:
                self.drawDict = {"All": True}
        
            if DISPLAY_LEVEL == "Battle":
            
                # Battle Background #
                if "Background" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Background"], [0, 0])
                    self.drawDict["Mobs"] = DATA_GAME.battle.mobList
                    
                elif "Background Top" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Background"], [0, 0], [0, 0, Config.SCREEN_SIZE[0], 124])
                    self.drawRectList.append([0, 0, Config.SCREEN_SIZE[0], 124])
                    self.drawDict["Attack Lines"] = [0, 0, Config.SCREEN_SIZE[0], 124]
                    
                # Mob Animations, After Images & Mob Sprites #
                if "Mob Animations" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Mob Animations"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                
                if "Mob After Images" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Mob After Images"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                
                if "Mobs" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Mobs"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                
                # Field Messages #
                if "Field Messages" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["Field Messages"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                    
                # Attack Lines #
                if "Attack Lines" in self.drawDict: # Shouldn't Need "All" (For Now..)
                    WINDOW.blit(self.surfaceDict["Attack Lines"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                    
                # User Interface #
                if "UI" in self.drawDict or "All" in self.drawDict:
                    WINDOW.blit(self.surfaceDict["UI"], [0, 0])
                    self.drawRectList.append(Config.WINDOW_RECT)
                    
            # Render Entire Screen On "All" & "Background" #
            if "All" in self.drawDict or "Background" in self.drawDict or "Mob Animations" in self.drawDict or "Mob After Images" in self.drawDict or "Mobs" in self.drawDict or "Field Messages" in self.drawDict:
                self.drawRectList = [Config.WINDOW_RECT]
                  
        # Display FPS #
        if True:
            pygame.draw.rect(WINDOW, [0, 0, 0], [WINDOW.get_size()[0] - 46, 0, 46, 13])
            Utility.write(FPS, ["Right", 0], [200, 200, 200], Config.FONT_ROMAN_16, WINDOW)
            if "All" not in self.drawDict and "Background" not in self.drawDict:
                self.drawRectList.append(pygame.Rect([WINDOW.get_size()[0] - 46, 0, 46, 13]))
        self.drawDict = {}
