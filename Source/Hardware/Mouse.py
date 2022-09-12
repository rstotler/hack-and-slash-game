import pygame, Utility
from pygame import *

class Mouse:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.oldX = 0
        self.oldY = 0
        
        self.clickLeft = False
        self.clickRight = False
        self.hoverElementList = []
        #self.clickElement = None
        
    def updatePosition(self, WINDOW, ELEMENT_LIST=[]):
    
        # Update Position #
        self.oldX = self.x
        self.oldY = self.y
        self.x, self.y = pygame.mouse.get_pos()
        
		# Get Hover Object Data #
        self.hoverElementList = []
        for element in ELEMENT_LIST:
            if element.collideShape == "Rectangle":
                if Utility.rectRectCollide([self.x, self.y], [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
                    self.hoverElementList.append(element)
                    
            elif element.collideShape == "Circle":
                if Utility.circleCircleCollide([element.rect.left + (element.rect.width / 2), element.rect.top + (element.rect.width / 2)], element.rect.width / 2, [self.x, self.y], 0):
                    self.hoverElement.append(element)
				