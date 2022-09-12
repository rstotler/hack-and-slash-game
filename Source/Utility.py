import pygame, random, Config
from pygame import *

def write(LABEL, LOCATION, COLOR, FONT, SCREEN):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = SCREEN.get_width() - labelSize[0]
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = SCREEN.get_height() - labelSize[1]
	
	labelRender = FONT.render(LABEL, True, COLOR)
	SCREEN.blit(labelRender, LOCATION)
    
def writeColor(LABEL, COLOR_CODE, COLOR_DICT, LOCATION, FONT, SCREEN):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = SCREEN.get_width() - labelSize[0]
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = SCREEN.get_height() - labelSize[1]
	
	# Regular Variables #
	targetColor = ""
	colorCount = 0
	printIndex = 0
	displayX = LOCATION[0]
	writeCheck = False
	
	for i, letter in enumerate(COLOR_CODE):
	
		# Sort #
		if stringIsNumber(letter):
			if colorCount != 0 : colorCount *= 10
			colorCount += int(letter)
		else:
			targetColor = targetColor + letter
			if len(COLOR_CODE) > i+1 and stringIsNumber(COLOR_CODE[i+1]):
				writeCheck = True
			
		# Write Check #
		if i+1 == len(COLOR_CODE):
			writeCheck = True
			
		# Write #
		if writeCheck == True:
			writeColor = [255, 255, 255]
			if targetColor in COLOR_DICT : writeColor = COLOR_DICT[targetColor]
			
			textString = LABEL[printIndex:printIndex+colorCount]
			textRender = FONT.render(textString, True, writeColor)	
			SCREEN.blit(textRender, [displayX, LOCATION[1]])
			
			printIndex += colorCount
			if printIndex == len(LABEL) : return
			displayX += FONT.size(textString)[0]
			colorCount = 0
			targetColor = ""
			writeCheck = False
		
def writeOutline(LABEL, FONT, PX_OUTLINE=2, COLOR_TEXT=[230, 230, 230], COLOR_OUTLINE=[10, 10, 10]):

	surfaceText = FONT.render(LABEL, True, COLOR_TEXT).convert_alpha()
	textWidth = surfaceText.get_width() + 2 * PX_OUTLINE
	textHeight = FONT.get_height()

	surfaceOutline = pygame.Surface([textWidth, textHeight + 2 * PX_OUTLINE]).convert_alpha()
	surfaceOutline.fill([0, 0, 0, 0])
	surfaceMain = surfaceOutline.copy()
	surfaceOutline.blit(FONT.render(str(LABEL), True, COLOR_OUTLINE).convert_alpha(), [0, 0])
	
	circleCache = {}
	for dx, dy in circlePoints(circleCache, PX_OUTLINE):
		surfaceMain.blit(surfaceOutline, [dx + PX_OUTLINE, dy + PX_OUTLINE])
		
	surfaceMain.blit(surfaceText, [PX_OUTLINE, PX_OUTLINE])
	
	return surfaceMain
	
def getLabel(LABEL, COLOR, FONT):
    labelSize = FONT.size(LABEL)
    labelRender = FONT.render(LABEL, True, COLOR)
    return labelRender
    
def circlePoints(CIRCLE_CACHE, R):

	R = int(round(R))
	if R in CIRCLE_CACHE:
		return CIRCLE_CACHE[R]
	
	x, y, e = R, 0 , 1 - R
	CIRCLE_CACHE[R] = points = []
	
	while x >= y:
		points.append([x, y])
		y += 1
		if e < 0:
			e += 2 * y - 1
		else:
			x -= 1
			e += 2 * (y - x) - 1
	
	points += [[y, x] for x, y in points if x > y]
	points += [[-x, y] for x, y in points if x]
	points += [[x, -y] for x, y in points if y]
	points.sort()
	
	return points
	
def outline(SCREEN, COLOR, LOCATION, SIZE, LINE_WIDTH=1):
	
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], LINE_WIDTH)                             # Top Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0], LOCATION[1] + SIZE[1] - 1], LINE_WIDTH)                             # Left Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Right Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1] + SIZE[1] - 1], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Bottom Line
	
def stringIsNumber(STRING):

	try:
		int(STRING)
		return True
	except ValueError:
		return False

def generateRandomId():
	
	randomId = str(random.randrange(1000000, 9999999))
	randomIndex = random.randrange(len(randomId))
	randomAlpha1 = random.choice(Config.ALPHABET_STRING)
	randomAlpha2 = random.choice(Config.ALPHABET_STRING)
	randomId = randomId[0:randomIndex] + randomAlpha1 + randomId[randomIndex::] + randomAlpha2
	
	return randomId
	
def rectRectCollide(RECT1_LOC, RECT2_LOC, SIZE):

	if RECT1_LOC[0] in range(RECT2_LOC[0], RECT2_LOC[0] + SIZE[0]):
		if RECT1_LOC[1] in range(RECT2_LOC[1], RECT2_LOC[1] + SIZE[1]):
			return True

	return False

def circleCircleCollide(CIRCLE1_LOC, CIRCLE1_RADIUS, CIRCLE2_LOC, CIRCLE2_RADIUS):

	import math
	dx = CIRCLE1_LOC[0] - CIRCLE2_LOC[0]
	dy = CIRCLE1_LOC[1] - CIRCLE2_LOC[1]
	dr = math.sqrt((dx ** 2) + (dy ** 2))
	
	if dr <= CIRCLE1_RADIUS + CIRCLE2_RADIUS:
		return True
	
	return False
	