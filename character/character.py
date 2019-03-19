import pygame
from character import dynamicElement, projectile, bomb

class character(dynamicElement.dynamicElement):
    def __init__(self, startPos, size, scale, physEnabled, inGame, floorGroup, momentPriority=5):
        super().__init__(startPos, size, scale, physEnabled, inGame, floorGroup, momentPriority)
        self.loadCharacter()
        self.actionBuffer = []
    
    def loadCharacter(self):
        #implement loader from file
        self.speed = 1
        self.health = 100
        self.subGroup = pygame.sprite.Group()
        self.subGroup.add(self)
        self.superGroup = pygame.sprite.Group()
        self.animation = []


    def update(self, frameTime, colliders):
        direction = pygame.math.Vector2(0, 0)
        while len(self.actionBuffer) > 0:
            actionType, action = self.actionBuffer.pop()
            if actionType == 'move':
                self.actionMove(action, direction)
            elif actionType =='attack':
                self.attack(action, frameTime)
        if direction.x != 0 or direction.y != 0:
            direction.normalize_ip()
            self.facingDir = direction
            self.move(direction * self.speed * self.scale, frameTime)

        super(character, self).update(frameTime, colliders)

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), int(self.rect.width/2), 0)
        super(character, self).render(displaySurface)

    def addAction(self, actionType, action):
        #consider implementing player action buffer vs handling in update method
        self.actionBuffer.append((actionType, action))

    def actionMove(self, direction, uvect):
        if direction == 'UP':
            uvect.y += -1
        elif direction == 'DOWN':
            uvect.y += 1
        elif direction == 'LEFT':
            uvect.x += -1
        elif direction == 'RIGHT':
            uvect.x += 1

    def attack(self, skill, frameTime):
        if skill == 'SHOOT':
            projectile.projectile(self.rect.center, 0.5, self.scale, self.facingDir, 2, self.physEnabled, self.inGame, self.floorGroup, self.subGroup, self, 1, 'kinetic')
            #print(self.subGroup.sprites())
        elif skill == 'THROW':
            bomb.bomb(self.rect.center, 1, self.scale, self.facingDir, 5, self.physEnabled, self.inGame, self.floorGroup, self.subGroup, self, 1, 'explosive')
        elif skill == 'MELE':
            pass

    def dealDamage(self):
        pass

