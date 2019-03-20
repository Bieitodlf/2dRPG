import pygame
from character import character

class player(character.character):

    facingDir = [0, 0]

    def __init__(self, levelRect, startPos, playerSize, scale, physEnabled, inGame, floorGroup):
        super().__init__(levelRect, startPos, playerSize, scale, physEnabled, inGame, floorGroup, 3)
        self.actionBuffer = []

    def actionMove(self, direction, uvect):
        super(player, self).actionMove(direction, uvect)

    def update(self, frameTime, colliders):
        super().update(frameTime, colliders)
        viewPortPositionX = self.rect.center[0] - self.levelRect.center[0]
        viewPortPositionY = self.rect.center[1] - self.levelRect.center[1]
        #if viewPortPositionY > maxY:
        #    pass
        #elif viewPortPositionY < minY:
        #    pass
        #
        #if viewPortPositionX > maxX:
        #    pass
        #elif viewPortPosition < minX:
        #    pass

    def moveMap(self):
        pass
