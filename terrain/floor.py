import pygame
import pytmx
from pytmx.util_pygame import load_pygame

class floor(object):
    def __init__(self, tileSize, levelRect, tiled_map, ground, walls):
        self.tileSize = tileSize
        self.width = tiled_map.width
        self.height = tiled_map.height
        self.ground = ground
        self.walls = walls
        self.group = pygame.sprite.Group()
        self.groundSurface = pygame.Surface(levelRect.size, pygame.SRCALPHA, 32)
        self.wallSurface = pygame.Surface(levelRect.size, pygame.SRCALPHA, 32)
        self.loadLayer(self.groundSurface, ground, tiled_map)
        self.loadLayer(self.wallSurface, walls, tiled_map)

    def loadRules(self, tileRulesFile):
        pass

    def loadLayer(self, surface, layer, tiled_map):
        for tile in layer.tiles():
            if tile[2] != None:
                image = pygame.transform.scale(tile[2], (self.tileSize, self.tileSize))
                surface.blit(image, (tile[0] * self.tileSize, tile[1] * self.tileSize))

    def getTileIndices(self):
        pass

    def renderGround(self, display, origin):
        display.blit(self.groundSurface, origin)

    def renderWalls(self, display, origin):
        display.blit(self.wallSurface, origin)
