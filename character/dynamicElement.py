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

    def update(self, *args):
        #moveDir is a unit vector used to determine if the player is moving and update the player position
        #moveDir = kwargs.get('moveDir')
        #damage and effects are not implemented at this moment
        #damage = kwargs.get('damage')
        if len(args) > 0:
            self.checkCollision(args[0])
        self.rect.center = self.positionVect.x, self.positionVect.y
        self.autoUpdate()
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), self.rect.width/2, 0)
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
            self.handleCollision(collider)
            colliders.remove(collider)
        colliders.empty()

    def handleCollision(self, collider):
        if collider in superGroup:
            pass
        elif self.breaksOnImpact:
            self.destroy()
        elif collider.momentPriority >= self.momentPriority:
            overlap = pygame.math.Vector2(self.positionVect.x, self.positionVect.y)
            overlap -= collider.positionVect
            overlap.normalize_ip()
            minDistVect = pygame.math.Vector2(self.rect.width/2 + collider.rect.width/2, self.rect.height/2 + collider.rect.height/2)
            minDist = overlap.dot(minDistVect)
            self.move(overlap)# * minDist)
        elif collider.momentPriority < self.momentPriority:
            collider.handleCollision(self)
            #collider.move(overlap * -1)
            print(collider, self, self.positionVect)
        else:
            pass
