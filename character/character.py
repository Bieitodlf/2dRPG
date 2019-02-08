import pygame
from dynamicElement import dynamicElement
from projectile import projectile
from bomb import bomb

class character(dynamicElement):
    def __init__(self, startPos, size, scale, physEnabled, inGame, momentPriority=5):
        dynamicElement.__init__(self, startPos, size, scale, physEnabled, inGame, momentPriority)
        self.loadCharacter()
        self.actionBuffer = []
    
    def loadCharacter(self):
        #implement loader from file
        self.speed = 1
        self.health = 100
        self.subGroup = pygame.sprite.Group()
        self.subGroup.add(self)
        self.superGroup = pygame.sprite.Group()

    def update(self, frameTime, colliders):
        while len(self.actionBuffer) > 0:
            actionType, action =  self.actionBuffer.pop()
            if actionType == 'move':
                self.actionMove(action, frameTime)
            elif actionType =='attack':
                self.attack(action, frameTime)

        super(character, self).update(frameTime, colliders)

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), self.rect.width/2, 0)
        super(character, self).render(displaySurface)

    def addAction(self, actionType, action):
        #consider implementing player action buffer vs handling in update method
        self.actionBuffer.append((actionType, action))

    #reimplement actionMove() to allow alternative control method
    def actionMove(self, direction, frameTime):
        uvect = pygame.math.Vector2(0, 0)
        if direction == 'UP':
            uvect.y += -1
        elif direction == 'DOWN':
            uvect.y += 1
        elif direction == 'LEFT':
            uvect.x += -1
        elif direction == 'RIGHT':
            uvect.x += 1
        
        uvect.normalize_ip()
        self.facingDir = uvect
        self.move(uvect * self.speed * self.scale, frameTime)

    def attack(self, skill, frameTime):
        if skill == 'SHOOT':
            projectile(self.rect.center, 0.5, self.scale, self.facingDir, 2, self.physEnabled, self.inGame, self.subGroup, self, 1, 'kinetic')
            #print(self.subGroup.sprites())
        elif skill == 'THROW':
            bomb(self.rect.center, 1, self.scale, self.facingDir, 5, self.physEnabled, self.inGame, self.subGroup, self, 1, 'explosive')
        elif skill == 'MELE':
            pass

    def dealDamage(self):
        pass

