'''
    dynamicElement class stores most of the physics information of the object and takes care of basic movement anc collission

    need to revisit collision resolution math
    need to replace moment priority with real system for moment transfer
'''
import pygame
import math

class dynamicElement(pygame.sprite.Sprite): 

    def __init__(self, levelRect, startPos, size, scale, physEnabled, inGame, floorGroup,  momentPriority, breaksOnImpact = False):
        self.levelRect = levelRect
        self.breaksOnImpact = breaksOnImpact
        self.momentPriority = momentPriority
        self.scale = scale
        size *= scale
        self.rect = pygame.Rect((0, 0), (size, size))
        self.rect.center = startPos
        self.positionVect = pygame.math.Vector2(self.rect.center)
        self.facingDir = pygame.math.Vector2(0, -1)
        pygame.sprite.Sprite.__init__(self)
        self.inGame = inGame
        inGame.add(self)
        self.floorGroup = floorGroup
        floorGroup.add(self)
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.physEnabled = physEnabled
        self.load(physEnabled)
        self.colliding = False
    
    def load(self, physEnabled):
        self.add(physEnabled)
        self.floor = 0
        #self.add(inGame)

    def update(self, frameTime, colliders):
        #damage and effects are not implemented at this moment
        self.checkCollision(colliders)
        self.rect.center = self.positionVect.x, self.positionVect.y
        pass

    def render(self, displaySurface):
        displaySurface.blit(self.surf, self.rect)
        pass

    def move(self, moveVect, frameTime):
        self.positionVect += moveVect * frameTime

    def checkCollision(self, colliders):
        #when colliding set self.colliding = True
        #returns collider
        #print(colliders)
        colliders.remove(self)
        #print(colliders)
        for collider in pygame.sprite.spritecollide(self, colliders, False):
            collider.checkCollision(colliders)
            self.handleCollision(collider)

    def handleCollision(self, collider):
        #consider implementing down the class hierarchy
        if (self in collider.subGroup or self in collider.superGroup):
            pass
            #print(collider.__class__.__name__, "in subgroup of", self.__class__.__name__)
        elif self.breaksOnImpact:
            print(self.__class__.__name__, "breaks on impact with", collider.__class__.__name__)
            self.destroy()
        elif collider.breaksOnImpact:
            print(collider.__class__.__name__, "breaks on impact with", self.__class__.__name__)
            collider.destroy()

            #revisit momentPriority
        elif collider.momentPriority >= self.momentPriority:
            print(collider.__class__.__name__, "collides with", self.__class__.__name__)
            overlap = pygame.math.Vector2(self.positionVect.x, self.positionVect.y)
            overlap -= collider.positionVect
            overlap.normalize_ip()
            minDistVect = pygame.math.Vector2(self.rect.width/2 + collider.rect.width/2, self.rect.height/2 + collider.rect.height/2)
            minDist = overlap.dot(minDistVect)
            self.positionVect += overlap * 4
        
        elif collider.momentPriority < self.momentPriority:
            collider.handleCollision(self)
            print(collider.__class__.__name__,"is pushed by",  self.__class__.__name__, "at", self.positionVect)
        else:
            pass

    def inFloor(floor):
        #returns a true if the element is in the specified floor
        return floor == self.floor

    def animate(self, frameTime):
        pass

class character(dynamicElement):
    def __init__(self, levelRect, startPos, size, scale, physEnabled, inGame, floorGroup, momentPriority=5):
        super().__init__(levelRect, startPos, size, scale, physEnabled, inGame, floorGroup, momentPriority)
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
            projectile.projectile(self.levelRect, self.rect.center, 0.5, self.scale, self.facingDir, 2, self.physEnabled, self.inGame, self.floorGroup, self.subGroup, self, 1, 'kinetic')
            #print(self.subGroup.sprites())
        elif skill == 'THROW':
            bomb.bomb(self.levelRect, self.rect.center, 1, self.scale, self.facingDir, 5, self.physEnabled, self.inGame, self.floorGroup, self.subGroup, self, 1, 'explosive')
        elif skill == 'MELE':
            pass

    def dealDamage(self):
        pass

class player(character):

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

class projectile(dynamicElement):
    def __init__(self, levelRect, startPos, size, scale, direction, speed, physEnabled, inGame, floorGroup, superGroup, parent, damage, damageType):

        damage = 10
        self.breaksOnImpact = True
        self.velocity = pygame.math.Vector2(direction * speed * scale)

        super().__init__(levelRect, startPos, size, scale, physEnabled, inGame, floorGroup, 10, self.breaksOnImpact)
        superGroup.add(self)
        self.superGroup = superGroup
        self.subGroup = pygame.sprite.Group(self)
        #self.move(self.velocity)

    def update(self, frameTime, colliders):
        #takes in physics info
        #checkCollision() will return collider for damage
        self.move(self.velocity, frameTime)
        super(projectile, self).update(frameTime, colliders)
        #print(self.rect.center)
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (0, 255, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), int(self.rect.width/2), 0)
        super(projectile, self).render(displaySurface)

    def destroy(self):
        self.kill()
        self = None
        pass

    def handleCollission(self, collider):
        dealDamage(collider)
        super(projectile, self).handleCollission(self, collider)
        self.kill()
        print(self.alive())
        self = None

    def dealDamage(self, collider):
        if collider.health > 0:
            collider.health -= self.damage
        print(collider.health)

class bomb(dynamicElement):
    def __init__(self, levelRect, startPos, size, scale, direction, speed, physEnabled, inGame, floorGroup, superGroup, parent, damage, damageType):
        damage = 20
        self.breaksOnImpact = False
        self.speed = 0
        dynamicElement.__init__(self, levelRect, startPos, size, scale, physEnabled, inGame, floorGroup, 10, self.breaksOnImpact)
        superGroup.add(self)
        self.superGroup = superGroup
        self.subGroup = pygame.sprite.Group(self)

    def autoUpdate(self):
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (0, 0, 255), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), int(self.rect.width/2), 0)
        super(bomb, self).render(displaySurface)

    def handleCollission(self, collider):
        super(bomb, self).handleCollission(self, collider)

    def destroy(self):
        self.kill()
        self = None

    def dealDamage(self, collider):
        if collider.health > 0:
            collider.health -= self.damage
        print(collider.health)
