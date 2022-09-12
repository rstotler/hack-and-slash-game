import pygame, random, Config, Utility
import math as SystemMath
from pygame import *
from Data import Mob

class Battle:
	
    def __init__(self):
        
        self.currentAttackSurfaceIndex = 0
        self.playerAttackList = []
        self.mobList = []
        self.deathAnimationList = []
        self.afterImageList = []
        self.fieldMessageList = []
        
        self.timerDict = {}
       
    def update(self, MOUSE, SCREEN, PLAYER):
        
        # Initialize Variables #
        delAttackList = []
        delMobList = []
        updateMobAfterImagesSurface = False
        updateMobSurface = False
        updateMobAnimationSurface = False
        updateFieldMessagesSurface = False
        updateUISurface = False   
        uiSurfaceFlags = {"Player Data": PLAYER}
        
        # Draw Current Attack Line #
        if "Attack Line" in self.timerDict and len(self.playerAttackList) > 0:
            self.timerDict["Attack Line"] += 1
            if self.timerDict["Attack Line"] >= 4:
                self.timerDict["Attack Line"] = 0
                self.playerAttackList[0].timerDict["Decay"] += 1
                self.addPlayerAttackPoint(MOUSE, SCREEN)
                
                if "Attack Line" not in self.timerDict:
                    if PLAYER.currentAttackCharges > 0:
                        PLAYER.currentAttackCharges -= 1
                    updateUISurface = True
                    if "Player Recharge Attack" not in self.timerDict:
                        self.timerDict["Player Recharge Attack"] = 0
        
        # Previous Attack Lines #
        for playerAttackIndex, playerAttack in enumerate(self.playerAttackList):
            if "Point" in playerAttack.timerDict:
                playerAttack.timerDict["Point"] += 1
                if playerAttack.timerDict["Point"] >= 3:
                    playerAttack.timerDict["Point"] = 0
                    
                    # Draw Second Line & Circle In Attack Line #
                    if playerAttack.attackPointIndex >= 0 and playerAttack.attackPointIndex < len(playerAttack.cordList):
                        if playerAttack.attackPointIndex > 0:
                            pygame.draw.line(SCREEN.surfaceDict["Attack Lines List"][playerAttack.surfaceIndex], [200, 0, 0], playerAttack.cordList[playerAttack.attackPointIndex], playerAttack.cordList[playerAttack.attackPointIndex - 1], 3)
                        pygame.draw.circle(SCREEN.surfaceDict["Attack Lines List"][playerAttack.surfaceIndex], [255, 255, 0], playerAttack.cordList[playerAttack.attackPointIndex], 3)
                        SCREEN.surfaceDict["Attack Lines"].blit(SCREEN.surfaceDict["Attack Lines List"][playerAttack.surfaceIndex], [0, 0])
                        SCREEN.drawDict["Attack Lines"] = True
                        
                        # Hit Enemies #
                        for mobIndex, mobData in enumerate(self.mobList):
                            if mobData not in playerAttack.mobHitList:
                                
                                # Collide Check #
                                collideCheck = False
                                targetPoint = playerAttack.cordList[playerAttack.attackPointIndex]
                                if mobData.collideShape == "Rectangle":
                                    if Utility.rectRectCollide(targetPoint, [mobData.rect.left, mobData.rect.top], [mobData.rect.width, mobData.rect.height]):
                                        collideCheck = True
                                #elif mobData.collideShape == "Circle":
                                #    if Utility.circleCircleCollide():
                                #        collideCheck = True
                                        
                                # Mob Hit #
                                if collideCheck == True:
                                    mobData.timerDict["Sprite Hit"] = 0
                                    playerAttack.mobHitList.append(mobData)
                                    updateMobSurface = True
                                    
                                    # Initialize Field Message (Damage) Data #
                                    if PLAYER.currentAttackCharges == 0:
                                        damageNum = 0
                                    else:
                                        damageNum = random.randrange(30, 200)
                                    fieldMessageFont = Config.FONT_ROMAN_25
                                    fieldMessageOutlineSize = 2
                                    fieldMessageColor = [230, 230, 230]
                                    fieldTopBuffer = -30
                                    if random.randrange(5) == 0 or ("Stunned Animation" in mobData.timerDict and random.randrange(3) == 0): # Not Final Formula
                                        damageNum = int(damageNum * 1.5) + 150
                                        fieldMessageFont = Config.FONT_ROMAN_40
                                        fieldMessageOutlineSize = 3
                                        fieldMessageColor = [230, 0 ,0]
                                        fieldTopBuffer = -45
                                        
                                    # Field Message (Damage) #
                                    fieldMessage = FieldMessage(str(damageNum), [0, mobData.rect.top + fieldTopBuffer], fieldMessageFont, fieldMessageOutlineSize, fieldMessageColor)
                                    fieldMessage.location[0] = int(mobData.rect.left + (mobData.rect.width / 2) - (fieldMessage.surface.get_rect().width / 2))
                                    self.fieldMessageList.append(fieldMessage)
                                    updateFieldMessagesSurface = True
                                    
                                    # Mob Death #
                                    mobData.currentHP -= damageNum
                                    if mobData.currentHP <= 0:
                                        delMobList.append(mobIndex)
                                        if mobData.id in SCREEN.imageDict["Mobs"]:
                                            spriteOffset = SCREEN.offsetDict[mobData.id]["Normal"][mobData.facingDir][0]
                                            if len(playerAttack.cordList) > 1 and playerAttack.getDistance() > 0:
                                                deathAnimation = MobDeathAnimation("Split", [mobData.rect.left, mobData.rect.top], SCREEN.imageDict["Mobs"][mobData.id]["Normal"]["Normal"][mobData.facingDir][0], spriteOffset, playerAttack)
                                            else:
                                                deathAnimation = MobDeathAnimation("Fade", [mobData.rect.left, mobData.rect.top], SCREEN.imageDict["Mobs"][mobData.id]["Normal"]["Normal"][mobData.facingDir][0], spriteOffset)
                                            self.deathAnimationList.append(deathAnimation)
                                            updateMobAnimationSurface = True
                        
                    # Increment Point Index #
                    playerAttack.attackPointIndex += 1
                    if playerAttack.attackPointIndex >= len(playerAttack.cordList) + 1:
                        delAttackList.append(playerAttackIndex)
        
        # Delete Attacks #
        if len(delAttackList) > 0:
            delAttackList.reverse()
            attackLineSurfaceIndexList = []
            for i in delAttackList:
                if self.playerAttackList[i].surfaceIndex not in attackLineSurfaceIndexList:
                    attackLineSurfaceIndexList.append(self.playerAttackList[i].surfaceIndex)
                SCREEN.surfaceDict["Attack Lines List"][self.playerAttackList[i].surfaceIndex].fill(0)
                del self.playerAttackList[i]
            
            SCREEN.redrawSurface("Battle", "Attack Lines", {"Player Data": PLAYER, "Attack Line Surface Index List": attackLineSurfaceIndexList})
            SCREEN.drawDict["All"] = True
        
        # Player #
        if True:
            if "Player Recharge Attack" in self.timerDict:
                self.timerDict["Player Recharge Attack"] += 1
                if self.timerDict["Player Recharge Attack"] >= 100:
                    PLAYER.currentAttackCharges += 1
                    updateUISurface = True
                    if PLAYER.currentAttackCharges >= PLAYER.maxAttackCharges:
                        del self.timerDict["Player Recharge Attack"]
                    else:
                        self.timerDict["Player Recharge Attack"] = 0
        
            if "Player Block" in self.timerDict:
                self.timerDict["Player Block"] += 1
                if self.timerDict["Player Block"] >= Config.MAX_PLAYER_BLOCK_TIME:
                    self.timerDict["Player Block Cooldown"] = 0
                    if not updateUISurface:
                        updateUISurface = True
                    del self.timerDict["Player Block"]
                    
            elif "Player Block Cooldown" in self.timerDict:
                self.timerDict["Player Block Cooldown"] += 1
                if self.timerDict["Player Block Cooldown"] >= 70:
                    if not updateUISurface:
                        updateUISurface = True
                    del self.timerDict["Player Block Cooldown"]
        
            #if "Player Hit Alpha" in self.timerDict:
            #    for hitAlphaIndex in self.timerDict["Player Hit Alpha"]:
            #        if self.timerDict["Player Hit Alpha"] > 0:
            #            self.timerDict["Player Hit Alpha"][hitAlphaIndex] -= 1
            #            if self.timerDict["Player Hit Alpha"][hitAlphaIndex] % 2 == 0:
            #                uiSurfaceFlags["Player Hit Alpha"][hitAlphaIndex] = int(self.timerDict["Player Hit Alpha"][hitAlphaIndex] / 2)
            #                if not updateUISurface:
            #                    updateUISurface = True
            #                if self.timerDict["Player Hit Alpha"][hitAlphaIndex] >= 6:
            #                    self.timerDict["Player Hit Alpha"][hitAlphaIndex] = 0
            
        # Mobs #
        if True:
        
            # Delete Mobs #
            if len(delMobList) > 0:
                delMobList.reverse()
                for i in delMobList:
                    del self.mobList[i]
                    updateMobSurface = True
            
            # Death Animations #
            if True:
                delDeathAnimationList = []
                for i, animationData in enumerate(self.deathAnimationList):
                    if "Fade" in animationData.timerDict:
                        animationData.timerDict["Fade"] += 1
                        if animationData.timerDict["Fade"] % 4 == 0:
                            animationData.alpha -= 12
                            
                            if "Split" in animationData.timerDict:
                                animationData.surfaceDict["Split 1"].set_alpha(animationData.alpha)
                                animationData.surfaceDict["Split 2"].set_alpha(animationData.alpha)
                            else:
                                animationData.surfaceDict["Normal"].set_alpha(animationData.alpha)
                                if animationData.alpha <= 0:
                                    delDeathAnimationList.append(i)
                                    
                            if not updateMobAnimationSurface:
                                updateMobAnimationSurface = True
                                
                    if "Split" in animationData.timerDict:
                        animationData.timerDict["Split"] += 1
                        if animationData.timerDict["Split"] % 4 == 0:
                            splitPercent = animationData.timerDict["Split"] / 250.0
                            
                            if abs(animationData.flags["Attack Direction"][0]) > abs(animationData.flags["Attack Direction"][1]):
                                animationData.flags["X Mod"] = animationData.flags["Relative X Location"] * splitPercent
                                animationData.flags["Y Mod"] = animationData.flags["Relative Y Location"] * splitPercent
                            else:
                                animationData.flags["X Mod"] = animationData.flags["Relative Y Location"] * splitPercent
                                animationData.flags["Y Mod"] = animationData.flags["Relative X Location"] * splitPercent
                                
                            if not updateMobAnimationSurface:
                                updateMobAnimationSurface = True
                            
                        if animationData.timerDict["Split"] == 150:
                            animationData.timerDict["Fade"] = 0
                            
                        if animationData.timerDict["Split"] >= 250:
                            delDeathAnimationList.append(i)
                            if not updateMobAnimationSurface:
                                updateMobAnimationSurface = True
                        
                if len(delDeathAnimationList) > 0:
                    delDeathAnimationList.reverse()
                    for i in delDeathAnimationList:
                        del self.deathAnimationList[i]
            
            # After Images #
            if True:
                delAfterImageList = []
                for i, afterImageData in enumerate(self.afterImageList):
                    afterImageData.fadeTimer += 1
                    if afterImageData.fadeTimer >= 6:
                        afterImageData.fadeTimer = 0
                        afterImageData.fadeLevel += 1
                        if not updateMobAfterImagesSurface:
                            updateMobAfterImagesSurface = True
                            
                        if afterImageData.fadeLevel >= 4:
                            delAfterImageList.append(i)
                            
                delAfterImageList.reverse()
                for i in delAfterImageList:
                    del self.afterImageList[i]
                    
            # Mob Updates (Sprite Animation/Movement/Attack) #
            for mobData in self.mobList:
            
                if "Animation" in mobData.timerDict:
                    mobData.timerDict["Animation"] += 1
                    if mobData.timerDict["Animation"] >= 4:
                        mobData.timerDict["Animation"] = 0
                        mobData.timerDict["Animation Frame"] += 1
                        if mobData.id in SCREEN.imageDict["Mobs"] and mobData.timerDict["Animation Frame"] >= len(SCREEN.imageDict["Mobs"][mobData.id]["Normal"]["Normal"][mobData.facingDir]):
                            mobData.timerDict["Animation Frame"] = 0
                        if not updateMobSurface:
                            updateMobSurface = True
                            SCREEN.drawDict["Mob Animations"] = True
                            SCREEN.drawDict["Attack Lines"] = True
                            
                if "Stunned Animation" in mobData.timerDict:
                    mobData.timerDict["Stunned Animation"] += 1
                    if mobData.timerDict["Stunned Animation"] % 4 == 0:
                        mobData.timerDict["Stunned Animation Frame"] += 1
                        if mobData.timerDict["Stunned Animation Frame"] >= 4:
                            mobData.timerDict["Stunned Animation Frame"] = 0
                    
                        if not updateMobSurface:
                            updateMobSurface = True
                            
                    if mobData.timerDict["Stunned Animation"] >= mobData.timerDict["Stunned Length"]:
                        del mobData.timerDict["Stunned Length"]                        
                        del mobData.timerDict["Stunned Animation"]                        
                        del mobData.timerDict["Stunned Animation Frame"]                        
                            
                if "Sprite Hit" in mobData.timerDict:
                    mobData.timerDict["Sprite Hit"] += 1
                    if mobData.timerDict["Sprite Hit"] >= 4:
                        del mobData.timerDict["Sprite Hit"]
                        if not updateMobSurface:
                            updateMobSurface = True
                            
                if "Movement" in mobData.timerDict:
                    mobData.timerDict["Movement"] += 1
                    if mobData.timerDict["Movement"] % mobData.timerDict["Movement Display Index"] == 0:
                        movePercent = mobData.timerDict["Movement"] / mobData.timerDict["Movement Time"]
                    
                        # Update After Image #
                        if mobData.timerDict["Movement"] % 6 == 0:
                            mobAnimationFrame = 0
                            if "Animation Frame" in mobData.timerDict:
                                mobAnimationFrame = mobData.timerDict["Animation Frame"]
                            newAfterImage = MobAfterImage(mobData.id, [mobData.rect.left, mobData.rect.top], mobData.facingDir, mobAnimationFrame)
                            self.afterImageList.append(newAfterImage)
                            updateMobAfterImagesSurface = True
                        
                        # Update Movement Data #
                        if mobData.timerDict["Movement Type"] == "Point To Point (Random)":
                            mobData.rect.left = mobData.timerDict["Start Move Point"][0] - (mobData.timerDict["X Diff"] * movePercent)
                            mobData.rect.top = mobData.timerDict["Start Move Point"][1] - (mobData.timerDict["Y Diff"] * movePercent)
                            
                        elif mobData.timerDict["Movement Type"] == "Circle":
                            xOffset = SystemMath.cos(SystemMath.radians(movePercent * 360)) * mobData.timerDict["Circle Radius"] * mobData.timerDict["Rotation Type"]
                            yOffset = SystemMath.sin(SystemMath.radians(movePercent * 360)) * mobData.timerDict["Circle Radius"]
                            xOffset += mobData.timerDict["Circle Radius"] * (mobData.timerDict["Rotation Type"] * -1)
                            mobData.rect.left = mobData.timerDict["Start Move Point"][0] + xOffset
                            mobData.rect.top = mobData.timerDict["Start Move Point"][1] + yOffset
                            mobData.timerDict["Y Diff"] = yOffset
                        
                        # Update Position In Mob List (1 - Up, 2 - Down) #
                        if len(self.mobList) > 1 and mobData.timerDict["Y Diff"] != 0:
                            currentIndex = self.mobList.index(mobData)
                            startIndex = -1
                            endIndex = -1
                            moveDir = int(mobData.timerDict["Y Diff"] / abs(mobData.timerDict["Y Diff"]))
                            if moveDir == 1 and currentIndex > 0:
                                startIndex = 0
                                endIndex = currentIndex
                            elif moveDir == -1 and self.mobList.index(mobData) < len(self.mobList) - 1:
                                startIndex = currentIndex + 1
                                endIndex = len(self.mobList)
                            if startIndex != -1:
                                newIndex = -1
                                for i, mobData2 in enumerate(self.mobList[startIndex:endIndex]):
                                    if moveDir == -1:
                                        mobData2 = self.mobList[endIndex - 1 - i]
                                    if (moveDir == 1 and mobData.rect.top + mobData.rect.height <= mobData2.rect.top + mobData2.rect.height) or (moveDir == -1 and mobData.rect.top + mobData.rect.height >= mobData2.rect.top + mobData2.rect.height):
                                        newIndex = i
                                        if moveDir == -1 : newIndex = endIndex - i + 1
                                        break
                                if newIndex != -1:
                                    if moveDir == 1:
                                        del self.mobList[currentIndex]
                                        self.mobList.insert(newIndex, mobData)
                                    else:
                                        self.mobList.insert(newIndex, mobData)
                                        del self.mobList[currentIndex]
                            
                        if not updateMobSurface:
                            updateMobSurface = True
                            SCREEN.drawDict["Mob Animations"] = True
                            SCREEN.drawDict["Attack Lines"] = True
                        
                    if mobData.timerDict["Movement"] >= mobData.timerDict["Movement Time"]:
                        if "Movement Point Count" in mobData.timerDict and mobData.timerDict["Movement Point Count"] > 1:
                            mobData.timerDict["Movement Point Count"] -= 1
                            self.setTargetMovement(mobData, "Point To Point (Random)")
                        else:
                            del mobData.timerDict["Movement"]
                            del mobData.timerDict["Movement Type"]
                            del mobData.timerDict["Movement Time"]
                            del mobData.timerDict["Movement Display Index"]
                            if "Start Move Point" in mobData.timerDict : del mobData.timerDict["Start Move Point"]
                            if "Target Move Point" in mobData.timerDict : del mobData.timerDict["Target Move Point"]
                            if "X Diff" in mobData.timerDict : del mobData.timerDict["X Diff"]
                            if "Y Diff" in mobData.timerDict : del mobData.timerDict["Y Diff"]
                            if "Circle Radius" in mobData.timerDict : del mobData.timerDict["Circle Radius"]
                            if "Rotation Type" in mobData.timerDict : del mobData.timerDict["Rotation Type"]
                            mobData.timerDict["Movement Cooldown"] = random.randrange(60, 180)
                            
                elif "Movement Cooldown" in mobData.timerDict and "Stunned Animation" not in mobData.timerDict:
                    mobData.timerDict["Movement Cooldown"] -= 1
                    if mobData.timerDict["Movement Cooldown"] <= 0:
                        del mobData.timerDict["Movement Cooldown"]
                        movementType = random.choice(["Point To Point (Random)", "Circle"])
                        self.setTargetMovement(mobData, movementType)
                        
                if "Stunned Bounce" in mobData.timerDict: # Not Finished
                    mobData.timerDict["Stunned Bounce"] += 1
                    if mobData.timerDict["Stunned Bounce"] % 2 == 0:
                    
                        if (mobData.timerDict["Stunned Bounce Move Direction"] == 1 and mobData.rect.left + mobData.rect.width < Config.SCREEN_SIZE[0]) or (mobData.timerDict["Stunned Bounce Move Direction"] == -1 and mobData.rect.left > 0):
                            bounceXDistance = 8
                            if mobData.timerDict["Stunned Bounce Count"] == 1:
                                bounceXDistance = 4
                            mobData.rect.left += SystemMath.sin(SystemMath.radians((mobData.timerDict["Stunned Bounce"] / 20.0) * 180)) * bounceXDistance * mobData.timerDict["Stunned Bounce Move Direction"]
                        
                            if mobData.timerDict["Stunned Bounce Move Direction"] == 1 and mobData.rect.left + mobData.rect.width >= Config.SCREEN_SIZE[0]:
                                mobData.rect.left = Config.SCREEN_SIZE[0] - mobData.rect.width
                                mobData.timerDict["Stunned Bounce Move Direction"] *= -1
                            elif mobData.timerDict["Stunned Bounce Move Direction"] == -1 and mobData.rect.left < 0:
                                mobData.rect.left = 0
                                mobData.timerDict["Stunned Bounce Move Direction"] *= -1
                           
                        bounceYDistance = -12
                        if mobData.timerDict["Stunned Bounce Count"] == 1:
                            bounceYDistance = -6
                        mobData.rect.top += SystemMath.cos(SystemMath.radians((mobData.timerDict["Stunned Bounce"] / 20.0) * 180)) * bounceYDistance
                        # Adjust Mob Y Level Surface Display Layer Here
                        
                        if not updateMobSurface:
                            updateMobSurface = True
                    
                    if mobData.timerDict["Stunned Bounce"] >= 20:
                        mobData.timerDict["Stunned Bounce Count"] += 1
                        if mobData.timerDict["Stunned Bounce Count"] == 1:
                            mobData.timerDict["Stunned Bounce"] = 0
                        else:
                            del mobData.timerDict["Stunned Bounce"]
                            del mobData.timerDict["Stunned Bounce Count"]
                            del mobData.timerDict["Stunned Bounce Move Direction"]
            
                if "Attack Flash" in mobData.timerDict:
                    mobData.timerDict["Attack Flash"] += 1
                    if mobData.timerDict["Attack Flash"] in [4, 8, 12, 28, 32]:
                        if mobData.timerDict["Attack Flash"] == 28:
                        
                            # Player Block Mob Attack #
                            if "Player Block" in self.timerDict:
                                stunPercent = self.timerDict["Player Block"] / Config.MAX_PLAYER_BLOCK_TIME
                            
                                del self.timerDict["Player Block"]
                                mobData.timerDict["Stunned Length"] = int(.40 * Config.MAX_MOB_STUN_LEGNTH) + int((.60 * Config.MAX_MOB_STUN_LEGNTH) * stunPercent) # Make Sure Stun Length It Is Not Shorter Than The Bounce For Mob To Start Moving Again
                                mobData.timerDict["Stunned Animation"] = 1
                                mobData.timerDict["Stunned Animation Frame"] = 0
                                mobData.timerDict["Stunned Bounce"] = 1
                                mobData.timerDict["Stunned Bounce Count"] = 0
                                if mobData.facingDir == "Left":
                                    mobData.timerDict["Stunned Bounce Move Direction"] = 1
                                else:
                                    mobData.timerDict["Stunned Bounce Move Direction"] = -1
                                
                                del mobData.timerDict["Attack Flash"]
                                mobData.timerDict["Attack Cooldown"] = random.randrange(60, 180)
                                if "Movement" in mobData.timerDict:
                                    del mobData.timerDict["Movement"]
                                    mobData.timerDict["Movement Cooldown"] = random.randrange(60, 180)
                                    
                                updateUISurface = True
                            
                            # Player Get Hit #
                            else:
                                PLAYER.currentHP -= 10
                                #if not updateUISurface:    
                                #    self.timerDict["Player Hit Alpha"][self.timerDict["Player Hit Alpha Index"]] = 0
                                #    uiSurfaceFlags["Player Hit Alpha"][self.timerDict["Player Hit Alpha Index"]] = 0
                                #    updateUISurface = True
                                    
                                    # Update Hit Alpha Index #
                                #    self.timerDict["Player Hit Alpha Index"] += 1
                                #    if self.timerDict["Player Hit Alpha Index"] >= 4:
                                #        self.timerDict["Player Hit Alpha Index"] = 0
                        
                        elif mobData.timerDict["Attack Flash"] == 32:
                            del mobData.timerDict["Attack Flash"]
                            mobData.timerDict["Attack Cooldown"] = random.randrange(60, 180)
                                
                        if not updateMobSurface:
                            updateMobSurface = True
                    
                elif "Attack Cooldown" in mobData.timerDict and "Stunned Animation" not in mobData.timerDict:
                    mobData.timerDict["Attack Cooldown"] -= 1
                    if mobData.timerDict["Attack Cooldown"] <= 0:
                        del mobData.timerDict["Attack Cooldown"]
                        mobData.timerDict["Attack Flash"] = 0
                        if not updateMobSurface:
                            updateMobSurface = True
            
            # Update Surfaces #
            if updateMobAnimationSurface:
                SCREEN.redrawSurface("Battle", "Mob Animations", {"Player Data": PLAYER, "Mob Animation List": self.deathAnimationList})
                SCREEN.drawDict["Background"] = True
                SCREEN.drawDict["Mob After Images"] = True
                SCREEN.drawDict["Mob Animations"] = True
                SCREEN.drawDict["Mobs"] = True
                SCREEN.drawDict["Field Messages"] = True
                SCREEN.drawDict["UI"] = True
            
            if updateMobAfterImagesSurface:
                SCREEN.redrawSurface("Battle", "Mob After Images", {"Mob After Image List": self.afterImageList})
                SCREEN.drawDict["Background"] = True
                SCREEN.drawDict["Mob After Images"] = True
                SCREEN.drawDict["Mobs"] = True
                SCREEN.drawDict["Field Messages"] = True
                SCREEN.drawDict["UI"] = True
            
            if updateMobSurface:
                SCREEN.redrawSurface("Battle", "Mobs", {"Player Data": PLAYER, "Mob List": self.mobList})
                SCREEN.drawDict["Background"] = True
                SCREEN.drawDict["Mob After Images"] = True
                SCREEN.drawDict["Mobs"] = True
                SCREEN.drawDict["Field Messages"] = True
                SCREEN.drawDict["UI"] = True
            
        # Field Messages #
        if True:
            delFieldMessageList = []
            for i, fieldMessage in enumerate(self.fieldMessageList):
                if "Movement" in fieldMessage.timerDict:
                    fieldMessage.timerDict["Movement"] += 1
                    if fieldMessage.timerDict["Movement"] >= 2:
                        fieldMessage.timerDict["Movement"] = 0
                        fieldMessage.location[1] -= 1
                        fieldMessage.timerDict["Decay"] += 1
                        fieldMessage.alpha -= 10
                        fieldMessage.surface.set_alpha(fieldMessage.alpha)
                        if fieldMessage.timerDict["Decay"] >= 30:
                            delFieldMessageList.append(i)
                        if not updateFieldMessagesSurface:
                            updateFieldMessagesSurface = True
            
            if len(delFieldMessageList) > 0:
                delFieldMessageList.reverse()
                for i in delFieldMessageList:
                    del self.fieldMessageList[i]
                    
            if updateFieldMessagesSurface:
                SCREEN.redrawSurface("Battle", "Field Messages", {"Player Data": PLAYER, "Field Messages": self.fieldMessageList})
                SCREEN.drawDict["Background"] = True
                SCREEN.drawDict["Mob Animations"] = True
                SCREEN.drawDict["Mobs"] = True
                SCREEN.drawDict["Field Messages"] = True
                SCREEN.drawDict["Attack Lines"] = True
                SCREEN.drawDict["UI"] = True
        
        # Update UI Surfaces #
        if updateUISurface:
            if "Player Block" not in uiSurfaceFlags and "Player Block" in self.timerDict:
                uiSurfaceFlags["Player Block"] = True
            elif "Player Block Cooldown" not in uiSurfaceFlags and "Player Block Cooldown" in self.timerDict:
                uiSurfaceFlags["Player Block Cooldown"] = True
            #uiSurfaceFlags["Player Hit Alpha"] = self.timerDict["Player Hit Alpha"]
        
            SCREEN.redrawSurface("Battle", "UI", uiSurfaceFlags)
            SCREEN.drawDict["Background"] = True
            SCREEN.drawDict["Mob After Images"] = True
            SCREEN.drawDict["Mob Animations"] = True
            SCREEN.drawDict["Mobs"] = True
            SCREEN.drawDict["Field Messages"] = True
            SCREEN.drawDict["UI"] = True
    
    def addPlayerAttackPoint(self, MOUSE, SCREEN, STOP_ATTACK=False):
    
        breakType = ""
        previousMouseDistance = [(self.playerAttackList[0].cordList[-1][0] - MOUSE.x), (self.playerAttackList[0].cordList[-1][1] - MOUSE.y)]
        if previousMouseDistance != [0, 0]:
            self.playerAttackList[0].cordList.append([MOUSE.x, MOUSE.y])
            
            currentPoint = self.playerAttackList[0].cordList[-1]
            previousPoint = self.playerAttackList[0].cordList[-2]
            previousPointDistance = [(currentPoint[0] - previousPoint[0]), (currentPoint[1] - previousPoint[1])]
            
            # Attack Line Exceeds Max Attack Distance - (Shorten Current Attack Point) #
            totalAttackDistance = self.playerAttackList[0].getDistance()
            if totalAttackDistance > Config.MAX_ATTACK_DISTANCE:
                previousPointDistance = [(currentPoint[0] - previousPoint[0]), (currentPoint[1] - previousPoint[1])]
                previousPointDistanceAbs = (abs(previousPointDistance[0]) + abs(previousPointDistance[1])) / 2
                if previousPointDistanceAbs > 0:
                    previousPointRatio = (totalAttackDistance - Config.MAX_ATTACK_DISTANCE) / previousPointDistanceAbs
                    self.playerAttackList[0].cordList[-1][0] -= int((previousPointDistance[0] / 2) * previousPointRatio)
                    self.playerAttackList[0].cordList[-1][1] -= int((previousPointDistance[1] / 2) * previousPointRatio)
                    breakType = "Shorten Attack"
                    
            # Add Extra Point In Long Attack Lines #
            if self.playerAttackList[0].timerDict["Decay"] < Config.MAX_ATTACK_POINTS:
                previousPointDistance = [(currentPoint[0] - previousPoint[0]), (currentPoint[1] - previousPoint[1])]
                previousPointDistanceAbs = (abs(previousPointDistance[0]) + abs(previousPointDistance[1]))
                if previousPointDistanceAbs >= 75:
                    newIndex = len(self.playerAttackList[0].cordList) - 1
                    newPoint = [currentPoint[0] - int(previousPointDistance[0] / 2), currentPoint[1] - int(previousPointDistance[1] / 2)]
                    self.playerAttackList[0].cordList.insert(newIndex, newPoint)
                    pygame.draw.line(SCREEN.surfaceDict["Attack Lines List"][self.playerAttackList[0].surfaceIndex], [255, 255, 255], self.playerAttackList[0].cordList[-2], self.playerAttackList[0].cordList[-3], 3)
                    
            # Update Attack Primary Direction #
            if previousPointDistance != [0, 0]:
                self.playerAttackList[0].attackDirection[0] += previousPointDistance[0]
                self.playerAttackList[0].attackDirection[1] += previousPointDistance[1]
                    
            # Draw Attack Line #
            pygame.draw.line(SCREEN.surfaceDict["Attack Lines List"][self.playerAttackList[0].surfaceIndex], [255, 255, 255], self.playerAttackList[0].cordList[-1], self.playerAttackList[0].cordList[-2], 3)
            SCREEN.surfaceDict["Attack Lines"].blit(SCREEN.surfaceDict["Attack Lines List"][self.playerAttackList[0].surfaceIndex], [0, 0])
            SCREEN.drawDict["Attack Lines"] = True
            
        # Stop Attack #
        if STOP_ATTACK or self.playerAttackList[0].timerDict["Decay"] >= Config.MAX_ATTACK_POINTS or breakType != "":
            self.playerAttackList[0].timerDict["Point"] = 9999
            del self.timerDict["Attack Line"]
            
            self.currentAttackSurfaceIndex += 1
            if self.currentAttackSurfaceIndex >= Config.MAX_ATTACKS:
                self.currentAttackSurfaceIndex = 0
        
    def spawnMob(self, TARGET_ID):
    
        newMob = Mob.Mob(TARGET_ID, ["Random", ""])
        newMob.rect.top = random.randrange(124, Config.SCREEN_SIZE[1] - newMob.rect.height - 75) # 75 = Bottom UI Margin Size
        
        targetIndex = 0
        for i, mobData in enumerate(self.mobList):
            if newMob.rect.top + newMob.rect.height <= mobData.rect.top + mobData.rect.height:
                targetIndex = i
                break
            if i == len(self.mobList) - 1:
                targetIndex = i + 1
                break
        self.mobList.insert(targetIndex, newMob)
        
    def setTargetMovement(self, MOB_DATA, MOVEMENT_TYPE):
    
        MOB_DATA.timerDict["Movement"] = 0
        MOB_DATA.timerDict["Movement Type"] = MOVEMENT_TYPE
        
        if MOVEMENT_TYPE == "Point To Point (Random)":
            MOB_DATA.timerDict["Movement Time"] = 250.0
            MOB_DATA.timerDict["Movement Display Index"] = 3 # Multiples Of 6 Only (For After Image Purposes)
            MOB_DATA.timerDict["Movement Point Count"] = random.choice([1, 2])
            
            mobMoveXMin = MOB_DATA.rect.left - (MOB_DATA.maxMoveDistance / 2.0)
            if mobMoveXMin < 0 : mobMoveXMin = 0
            mobMoveXMax = MOB_DATA.rect.left + (MOB_DATA.maxMoveDistance / 2.0)
            if mobMoveXMax > Config.SCREEN_SIZE[0] - MOB_DATA.rect.width : mobMoveXMax = Config.SCREEN_SIZE[0] - MOB_DATA.rect.width
            mobMoveX = None
            if mobMoveXMin < mobMoveXMax:
                mobMoveX = random.randrange(mobMoveXMin, mobMoveXMax)
            
            mobMoveYMin = MOB_DATA.rect.top - (MOB_DATA.maxMoveDistance / 2.0)
            if mobMoveYMin < 124 : mobMoveYMin = 124
            mobMoveYMax = MOB_DATA.rect.top + (MOB_DATA.maxMoveDistance / 2.0)
            if mobMoveYMax > Config.SCREEN_SIZE[1] - MOB_DATA.rect.height - 75 : mobMoveYMax = Config.SCREEN_SIZE[1] - MOB_DATA.rect.height - 75
            mobMoveY = None
            if mobMoveYMin < mobMoveYMax:
                mobMoveY = random.randrange(mobMoveYMin, mobMoveYMax)
            
            if mobMoveX != None and mobMoveY != None:
                MOB_DATA.timerDict["Start Move Point"] = [MOB_DATA.rect.left, MOB_DATA.rect.top]
                MOB_DATA.timerDict["Target Move Point"] = [mobMoveX, mobMoveY]
                MOB_DATA.timerDict["X Diff"] = MOB_DATA.timerDict["Start Move Point"][0] - MOB_DATA.timerDict["Target Move Point"][0]
                MOB_DATA.timerDict["Y Diff"] = MOB_DATA.timerDict["Start Move Point"][1] - MOB_DATA.timerDict["Target Move Point"][1]
                
                if MOB_DATA.timerDict["X Diff"] < 0 and MOB_DATA.facingDir == "Left":
                    MOB_DATA.facingDir = "Right"
                elif MOB_DATA.timerDict["X Diff"] > 0 and MOB_DATA.facingDir == "Right":
                    MOB_DATA.facingDir = "Left"
            
        elif MOVEMENT_TYPE == "Circle":
            MOB_DATA.timerDict["Movement Time"] = 125.0
            MOB_DATA.timerDict["Movement Display Index"] = 2 # Multiples Of 6 Only (For After Image Purposes)
            MOB_DATA.timerDict["Circle Radius"] = random.randrange(125, 175)
            MOB_DATA.timerDict["Start Move Point"] = [MOB_DATA.rect.left, MOB_DATA.rect.top]
            MOB_DATA.timerDict["Rotation Type"] = random.choice([1, -1]) # Clockwise/Counter Clockwise
        
    def leftClickDown(self, MOUSE, PLAYER):
        
        if PLAYER.currentHP > 0 and "Player Block" not in self.timerDict:
            self.timerDict["Attack Line"] = 0
            self.playerAttackList.insert(0, PlayerAttack(MOUSE, self.currentAttackSurfaceIndex))
        
    def leftClickUp(self, MOUSE, SCREEN, PLAYER):
    
        if "Attack Line" in self.timerDict:
            self.addPlayerAttackPoint(MOUSE, SCREEN, True)
            if PLAYER.currentAttackCharges > 0:
                PLAYER.currentAttackCharges -= 1
            if "Player Recharge Attack" not in self.timerDict:
                self.timerDict["Player Recharge Attack"] = 0
                
            uiSurfaceFlags = {"Player Data": PLAYER}
            if "Player Block" in self.timerDict:
                uiSurfaceFlags["Player Block"] = True
            elif "Player Block Cooldown" in self.timerDict:
                uiSurfaceFlags["Player Block Cooldown"] = True
            #if "Player Hit Alpha" in self.timerDict and "Player Hit Alpha" not in uiSurfaceFlags:
            #    uiSurfaceFlags["Player Hit Alpha"] = self.timerDict["Player Hit Alpha"]
                
            SCREEN.redrawSurface("Battle", "UI", uiSurfaceFlags)
            SCREEN.drawDict["Background"] = True
            SCREEN.drawDict["Mobs"] = True
            SCREEN.drawDict["Field Messages"] = True
            SCREEN.drawDict["UI"] = True
        
    def playerBlock(self, MOUSE, SCREEN, PLAYER):
    
        if PLAYER.currentHP > 0 and "Player Block" not in self.timerDict and "Player Block Cooldown" not in self.timerDict:
        
            # Stop Previous Attack #
            if "Attack Line" in self.timerDict:
                self.addPlayerAttackPoint(MOUSE, SCREEN, True)
                if PLAYER.currentAttackCharges > 0:
                    PLAYER.currentAttackCharges -= 1
                if "Player Recharge Attack" not in self.timerDict:
                    self.timerDict["Player Recharge Attack"] = 0
        
            self.timerDict["Player Block"] = 0
            SCREEN.redrawSurface("Battle", "UI", {"Player Data": PLAYER, "Player Block": True})
            SCREEN.drawDict["Background"] = True
            SCREEN.drawDict["Mobs"] = True
            SCREEN.drawDict["Field Messages"] = True
            SCREEN.drawDict["UI"] = True
        
class FieldMessage:
    
    def __init__(self, LABEL, LOCATION, FONT, OUTLINE_SIZE, COLOR):
        
        self.location = LOCATION
        self.surface = Utility.writeOutline(LABEL, FONT, OUTLINE_SIZE, COLOR)
        self.alpha = 255
        
        self.timerDict = {"Movement": 0, "Decay": 0}
        
class PlayerAttack:
	
    def __init__(self, MOUSE, SURFACE_INDEX):
        
        self.attackPointIndex = 0 # Decrease To Add Player Attack Delay
        self.surfaceIndex = SURFACE_INDEX
        
        self.attackDirection = [0, 0]
        self.mobHitList = []
        self.cordList = [[MOUSE.x, MOUSE.y]]
        
        self.timerDict = {"Decay": 1} # Decay Represents Attack Timer Length
        
    def getDistance(self):
    
        totalDistance = 0
        if len(self.cordList) > 1:
            for i, cord in enumerate(self.cordList[1::]):
                xDiff = abs(cord[0] - self.cordList[i][0])
                yDiff = abs(cord[1] - self.cordList[i][1])
                totalDistance += xDiff + yDiff
        
        return totalDistance
        
class MobDeathAnimation:

    def __init__(self, TYPE, LOCATION, MOB_IMAGE, SPRITE_OFFSET, ATTACK_DATA=None):
        
        self.type = TYPE
        self.location = LOCATION
        self.surfaceDict = {"Normal": MOB_IMAGE.copy()}
        self.alpha = 255
        
        self.timerDict = {"Fade": 0}
        self.flags = {"Sprite Offset": SPRITE_OFFSET}
        
        if TYPE == "Split":
            
            # Clean & Add Mask Points #
            mask1PointList = []
            mask2PointList = []
            for attackPoint in ATTACK_DATA.cordList:
                mask1PointList.append([attackPoint[0] - LOCATION[0] - SPRITE_OFFSET[0], attackPoint[1] - LOCATION[1] - SPRITE_OFFSET[1]])
                mask2PointList.append(mask1PointList[-1])
            
            # Initialize Variables #
            self.surfaceDict = {}
            self.timerDict = {"Split": 0}
            self.flags["Attack Direction"] = ATTACK_DATA.attackDirection
            self.flags["X Mod"] = 0
            self.flags["Y Mod"] = 0
            targetPointIndex = int(len(ATTACK_DATA.cordList) / 2) + 1
            slope = 0
            
            # Create Mask Coordinates #
            if abs(ATTACK_DATA.attackDirection[0]) > abs(ATTACK_DATA.attackDirection[1]):
            
                # Get Slope Data #
                yLoc1 = mask2PointList[-1][1]
                yLoc2 = mask2PointList[0][1]
                diffX1 = MOB_IMAGE.get_width() - mask2PointList[-1][0]
                diffX2 = mask2PointList[0][0] - MOB_IMAGE.get_width()
                if mask2PointList[-1][1] != mask2PointList[-targetPointIndex][1]:
                    slope = (mask2PointList[-1][0] - mask2PointList[-targetPointIndex][0]) / (mask2PointList[-1][1] - mask2PointList[-targetPointIndex][1])
                
                # Moving To The Right #
                if ATTACK_DATA.cordList[0][0] < ATTACK_DATA.cordList[-1][0]:
                    if slope != 0:
                        yLoc1 += int(diffX1 / slope)
                        yLoc2 += int(diffX2 / slope)
                    mask1PointList.extend([[MOB_IMAGE.get_width(), yLoc1], [MOB_IMAGE.get_width(), MOB_IMAGE.get_height()], [0, MOB_IMAGE.get_height()], [0, yLoc2], mask1PointList[0]])
                    mask2PointList.extend([[MOB_IMAGE.get_width(), yLoc1], [MOB_IMAGE.get_width(), 0], [0, 0], [0, yLoc2], mask2PointList[0]])
                
                # Moving To The Left #
                else:
                    if slope != 0:
                        yLoc1 -= int(diffX1 / slope)
                        yLoc2 -= int(diffX2 / slope)
                    mask1PointList.extend([[0, yLoc1], [0, MOB_IMAGE.get_height()], [MOB_IMAGE.get_width(), MOB_IMAGE.get_height()], [MOB_IMAGE.get_width(), yLoc2], mask2PointList[0]])
                    mask2PointList.extend([[0, yLoc1], [0, 0], [MOB_IMAGE.get_width(), 0], [MOB_IMAGE.get_width(), yLoc2], mask2PointList[0]])
            else:
            
                # Get Slope Data #
                xLoc1 = mask2PointList[-1][0]
                xLoc2 = mask2PointList[0][0]
                diffY1 = MOB_IMAGE.get_height() - mask2PointList[-1][1]
                diffY2 = mask2PointList[0][1] - MOB_IMAGE.get_height()
                if mask2PointList[-1][0] != mask2PointList[-targetPointIndex][0]:
                    slope = (mask2PointList[-1][1] - mask2PointList[-targetPointIndex][1]) / (mask2PointList[-1][0] - mask2PointList[-targetPointIndex][0])
            
                # Player Attack Moving Up #
                if ATTACK_DATA.cordList[0][1] > ATTACK_DATA.cordList[-1][1]:
                    if slope != 0:
                        xLoc1 -= int(diffY1 / slope)
                        xLoc2 -= int(diffY2 / slope)
                    mask1PointList.extend([[xLoc1, 0], [MOB_IMAGE.get_width(), 0], [MOB_IMAGE.get_width(), MOB_IMAGE.get_height()], [xLoc2, MOB_IMAGE.get_height()], mask2PointList[0]])
                    mask2PointList.extend([[xLoc1, 0], [0, 0], [0, MOB_IMAGE.get_height()], [xLoc2, MOB_IMAGE.get_height()], mask2PointList[0]])
                
                # Player Attack Moving Down #
                else:
                    if slope != 0:
                        xLoc1 += int(diffY1 / slope)
                        xLoc2 += int(diffY2 / slope)
                    mask1PointList.extend([[xLoc1, MOB_IMAGE.get_height()], [MOB_IMAGE.get_width(), MOB_IMAGE.get_height()], [MOB_IMAGE.get_width(), 0], [xLoc2, 0], mask2PointList[0]])
                    mask2PointList.extend([[xLoc1, MOB_IMAGE.get_height()], [0, MOB_IMAGE.get_height()], [0, 0], [xLoc2, 0], mask2PointList[0]])
                
            # Create Masked Surfaces #
            maskSurfTop = pygame.Surface([MOB_IMAGE.get_width(), MOB_IMAGE.get_height()])
            pygame.draw.polygon(maskSurfTop, [255, 255, 255], mask1PointList)
            self.surfaceDict["Split 1"] = MOB_IMAGE.copy()
            self.surfaceDict["Split 1"].set_colorkey([255, 255, 255])
            self.surfaceDict["Split 1"].blit(maskSurfTop, [0, 0], None, pygame.BLEND_RGB_ADD)
            
            maskSurfBottom = pygame.Surface([MOB_IMAGE.get_width(), MOB_IMAGE.get_height()])
            pygame.draw.polygon(maskSurfBottom, [255, 255, 255], mask2PointList)
            self.surfaceDict["Split 2"] = MOB_IMAGE.copy()
            self.surfaceDict["Split 2"].set_colorkey([255, 255, 255])
            self.surfaceDict["Split 2"].blit(maskSurfBottom, [0, 0], None, pygame.BLEND_RGB_ADD)
            
            # Set Slope Data #
            splitDistance = 40
            if slope == 0 : slope = splitDistance
            if slope > 0 : self.flags["Relative X Location"] = splitDistance - ((splitDistance / 2.0) / slope)
            else : self.flags["Relative X Location"] = -(splitDistance - ((splitDistance / 2.0) / abs(slope)))
            self.flags["Relative Y Location"] = splitDistance - abs(self.flags["Relative X Location"])
            
class MobAfterImage:

    def __init__(self, ID, LOCATION, FACING_DIRECTION, ANIMATION_FRAME):
    
        self.id = ID
        self.location = LOCATION
        self.facingDir = FACING_DIRECTION
        self.animationFrame = ANIMATION_FRAME
        self.fadeLevel = 1
        self.fadeTimer = 0
        
    def getFadeLevel(self):
    
        if self.fadeLevel == 1:
            return "Normal"
        elif self.fadeLevel == 2:
            return "After Image 1"
        elif self.fadeLevel == 3:
            return "After Image 2"
