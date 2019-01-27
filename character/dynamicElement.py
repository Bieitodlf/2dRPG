import pygame
from terrain.floor import floor

class dynamicElement():


    def __init__(self, startPos, size, scale):
        self.position = startPos
        size *= scale
        self.size = size
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.center = [size/2, size/2]
        self.load()
        self.colliding = False
    
    def load(self):
        #load player attributes and data to substitute __init__
        self.speed = 1
        pass

    def update(self, **kwargs):
        #moveDir is a unit vector used to determine if the player is moving and update the player position
        #moveDir = kwargs.get('moveDir')
        #damage and effects are not implemented at this moment
        #damage = kwargs.get('damage')
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), self.center, self.size/2, 0)
        displaySurface.blit(self.surf, (self.position[0] - self.size/2, self.position[1] - self.size/2))
        pass

    def checkCollision(self):
        #when colliding set self.colliding = True
        #returns collider
        pass

