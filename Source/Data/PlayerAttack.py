class Attack:
	
    def __init__(self, MOUSE, SURFACE_INDEX):
        
        self.currentPointIndex = 0 # Decrease To Add Player Attack Delay
        self.surfaceIndex = SURFACE_INDEX
        
        self.mobHitList = []
        self.cordList = [[MOUSE.x, MOUSE.y]]
        self.timerDict = {}
        
    def getDistance(self):
    
        totalDistance = 0
        if len(self.cordList) > 1:
            for i, cord in enumerate(self.cordList[1::]):
                xDiff = abs(cord[0] - self.cordList[i][0])
                yDiff = abs(cord[1] - self.cordList[i][1])
                totalDistance += xDiff + yDiff
        
        return totalDistance
        