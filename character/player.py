import pygame
from character import character

class player(character.character):

    facingDir = [0, 0]

    def __init__(self, startPos, playerSize, scale, physEnabled, inGame, floorGroup):
        super().__init__(startPos, playerSize, scale, physEnabled, inGame, floorGroup, 3)
        self.actionBuffer = []

    def actionMove(self, direction, uvect):
        super(player, self).actionMove(direction, uvect)

