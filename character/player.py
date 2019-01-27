import pygame
from terrain.floor import floor
from .character import character

class player(character):

    facingDir = [0, 0]

    def __init__(self, startPos, playerSize, scale):
        character.__init__(self, startPos, playerSize, scale)
        self.size
        self.actionBuffer = []
    
    def addAction(self, actionType, action):
        #consider implementing player action buffer vs handling in update method
        if actionType == 'move':
            #print(actionType, action)
            self.move(action)
        elif actionType =='attack':
            pass
