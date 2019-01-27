import pygame
from dynamicElement import dynamicElement

class character(dynamicElement):
    def __init__(self, startPos, size, scale):
        dynamicElement.__init__(self, startPos, size, scale)
        self.load()
    
    def load(self):
        #implement loader from file
        self.speed = 1
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
        self.position = self.position[0] + uvect[0] * self.speed * self.size, self.position[1] + uvect[1] * self.speed * self.size

    def attack(self, skill):
        
        pass
