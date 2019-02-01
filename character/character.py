import pygame
from dynamicElement import dynamicElement
from projectile import projectile

class character(dynamicElement):
    def __init__(self, startPos, size, scale, physEnabled, inGame, momentPriority=5):
        dynamicElement.__init__(self, startPos, size, scale, physEnabled, inGame, momentPriority)
        self.loadCharacter()
    
    def loadCharacter(self):
        #implement loader from file
        self.speed = 10
        self.health = 100
        self.subGroup = pygame.sprite.Group()
        self.subGroup.add(self)

    def autoUpdate(self):
        pass

    def addAction(self, actionType, action):
        #consider implementing player action buffer vs handling in update method
        if actionType == 'move':
            #print(actionType, action)
            self.actionMove(action)
        elif actionType =='attack':
            self.attack('SHOOT')

    #reimplement actionMove() to allow alternative control method
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
        self.move(uvect * self.speed * self.scale)

    def attack(self, skill):
        if skill == 'SHOOT':
            projectile(self.rect.center, 1, self.scale, self.facingDir, 5, self.physEnabled, self.inGame, self.subGroup, 1, 'kinetic')
        pass

