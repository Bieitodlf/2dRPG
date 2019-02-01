import pygame
from terrain.floor import floor
from .character import character

class player(character):

    facingDir = [0, 0]

    def __init__(self, startPos, playerSize, scale, physEnabled, inGame):
        character.__init__(self, startPos, playerSize, scale, physEnabled, inGame, 3)
        self.actionBuffer = []

    def actionMove(self, direction):
        uvect = pygame.math.Vector2(0, 0)
        if direction == 'UP':
            uvect.x, uvect.y = 0, -1
        elif direction == 'DOWN':
            uvect.x, uvect.y = 0, 1
        elif direction == 'LEFT':
            uvect.x, uvect.y = -1, 0
        elif direction == 'RIGHT':
            uvect.x, uvect.y = 1, 0
        
        self.facingDir = uvect
        self.move(uvect * self.speed)



    def __del__(self):
        character.__del__(self)
