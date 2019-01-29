import pygame
from terrain.floor import floor

class dynamicElement(pygame.sprite.Sprite): 

    def __init__(self, startPos, size, scale, isPhysEnabled, physEnabled, momentPriority):
        self.momentPriority = momentPriority
        size *= scale
        self.rect = pygame.Rect((0, 0), (size, size))
        self.rect.center = startPos
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.load(isPhysEnabled, physEnabled)
        self.colliding = False
    
    def load(self, isPhysEnabled, physEnabled):
        if isPhysEnabled:
            self.add(physEnabled)
            #self.add(inGame)

    def update(self, *argv):
        #moveDir is a unit vector used to determine if the player is moving and update the player position
        #moveDir = kwargs.get('moveDir')
        #damage and effects are not implemented at this moment
        #damage = kwargs.get('damage')
        if len(argv) > 0:
            self.checkCollision(argv[0])
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), self.rect.width/2, 0)
        displaySurface.blit(self.surf, self.rect)
        pass

    def checkCollision(self, colliders):
        #when colliding set self.colliding = True
        #returns collider
        #print(colliders)
        colliders.remove(self)
        #print(colliders)
        for collider in pygame.sprite.spritecollide(self, colliders, False):
            self.handleCollisions(collider)
            colliders.remove(collider)
        colliders.empty()

    def handleCollisions(self, collider):
        direction = -(collider.rect.center[0] - self.rect.center[0]), -(collider.rect.center[1] - self.rect.center[1])

        minDistance = (collider.rect.width + self.rect.width)/2, (collider.rect.height + self.rect.height)/2
        print(collider.momentPriority, self.momentPriority)
        if collider.momentPriority >= self.momentPriority:
            self.rect.move_ip(direction)
       
        elif collider.momentPriority < self.momentPriority:
            collider.rect.move_ip(-direction[0], -direction[1])
        
        else:
            pass
    
    def __del__(self):
        pass
