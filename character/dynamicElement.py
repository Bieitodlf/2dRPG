import pygame
from terrain.floor import floor

class dynamicElement(pygame.sprite.Sprite): 

    def __init__(self, startPos, size, scale, physEnabled, inGame, momentPriority, breaksOnImpact = False):
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
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.physEnabled = physEnabled
        self.load(physEnabled)
        self.colliding = False
    
    def load(self, physEnabled):
        self.add(physEnabled)
        #self.add(inGame)

    def update(self, clock, *args):
        #damage and effects are not implemented at this moment
        if len(args) > 0:
            self.checkCollision(args[0])
        self.rect.center = self.positionVect.x, self.positionVect.y
        self.autoUpdate(clock)
        pass

    def render(self, displaySurface):
        displaySurface.blit(self.surf, self.rect)
        pass

    def move(self, moveVect):
        self.positionVect += moveVect
        self.rect.center = self.positionVect.x, self.positionVect.y

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
            self.move(overlap)# * minDist)
        elif collider.momentPriority < self.momentPriority:
            collider.handleCollision(self)
            #collider.move(overlap * -1)
            print(collider.__class__.__name__,"is pushed by",  self.__class__.__name__, "at", self.positionVect)
        else:
            pass
