import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from terrain.floor import floor

class level():
    def __init__(self, screenRect, scale):
        self.tiled_map = load_pygame("terrain/mapTest.tmx")
        self.width = self.tiled_map.width
        self.height = self.tiled_map.height
        self.tileSize = scale
        layers = self.tiled_map.layers
        self.backgroundSurface = pygame.Surface(screenRect.size)
        self.loadBackground(layers)
        self.loadFloors(screenRect, layers)

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

    def renderBackground(self, display):
        display.blit(self.backgroundSurface, (0, 0))
