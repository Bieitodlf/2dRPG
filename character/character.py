import pygame
from dynamicElement import dynamicElement

class character(dynamicElement):
    def __init__(self, startPos, size, scale, isPhysEnabled, physEnabled, momentPriority=2):
        dynamicElement.__init__(self, startPos, size, scale, isPhysEnabled, physEnabled, momentPriority)
        self.loadCharacter()
    
    def loadCharacter(self):
        #implement loader from file
        self.speed = 0.5
        self.health = 100

    def move(self, direction):
        if direction == 'UP':
            uvect = (0, -1)
        elif direction == 'DOWN':
            uvect = (0, 1)
        elif direction == 'LEFT':
            uvect = (-1, 0)
        elif direction == 'RIGHT':
            uvect = (1, 0)
        
        facingDir = uvect
        self.rect.center = self.rect.center[0] + uvect[0] * self.speed * self.rect.width, self.rect.center[1] + uvect[1] * self.speed * self.rect.width

    def attack(self, skill):
        
        pass

    def __del__(self):
        dynamicElement.__del__(self)
