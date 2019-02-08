import pygame
from terrain.floor import floor
from .character import character

class player(character):

    facingDir = [0, 0]

    def __init__(self, startPos, playerSize, scale, physEnabled, inGame):
        character.__init__(self, startPos, playerSize, scale, physEnabled, inGame, 3)
        self.actionBuffer = []

    def actionMove(self, direction, frameTime):
        super(player, self).actionMove(direction, frameTime)

    def __del__(self):
        character.__del__(self)
