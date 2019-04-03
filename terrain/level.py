import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from terrain.floor import floor

class level():
    def __init__(self, screenRect, scale):
        self.tiled_map = load_pygame("terrain/testLevel.tmx")
        width = self.tiled_map.width
        height = self.tiled_map.height
        self.tileSize = scale
        self.origin = (-200, -200)#(-(width * self.tileSize)/2, -(height * self.tileSize)/2)
        self.levelRect = pygame.Rect(self.origin, (width * self.tileSize, height * self.tileSize))
        self.originVect = pygame.math.Vector2(self.levelRect.center)
        self.levelSurf = pygame.Surface(self.levelRect.size, pygame.SRCALPHA, 32)
        layers = self.tiled_map.layers
        self.backgroundSurface = pygame.Surface(self.levelRect.size)
        self.loadBackground(layers)
        self.loadFloors(self.levelRect, layers)

    def loadBackground(self, layers):
        for tile in layers[0].tiles(): 
            if tile[2] != None:
                image = pygame.transform.scale(tile[2], (self.tileSize, self.tileSize))
                self.backgroundSurface.blit(image, (tile[0] * self.tileSize, tile[1] * self.tileSize))

    def loadFloors(self, screenRect, layers):
        self.numFloors = (len(layers) - 1) / 2
        self.floors = {}
        floorNumber = 0
        layer = 1
        while floorNumber < self.numFloors:
            key = floorNumber
            value = floor(self.tileSize, screenRect, self.tiled_map, layers[layer], layers[layer + 1])
            self.floors[key] = value
            floorNumber += 1
            layer += 2

    def renderBackground(self):
        self.levelSurf.blit(self.backgroundSurface, (0, 0))
