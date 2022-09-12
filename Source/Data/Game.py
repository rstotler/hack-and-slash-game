from Data import Player, Battle

class Game:
	
    def __init__(self):
        
        self.player = Player.Player()
        self.battle = Battle.Battle()
        
    def update(self, MOUSE, SCREEN, DISPLAY_LEVEL):
        
        if DISPLAY_LEVEL == "Battle":
            self.battle.update(MOUSE, SCREEN, self.player)
        