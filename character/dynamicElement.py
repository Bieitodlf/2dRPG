import pygame
from terrain.floor import floor

class dynamicElement(pygame.sprite.Sprite):     

    def __init__(self, startPos, size, scale, isPhysEnabled, physEnabled):
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

    def update(self, physEnabled, **kwargs):
        #moveDir is a unit vector used to determine if the player is moving and update the player position
        #moveDir = kwargs.get('moveDir')
        #damage and effects are not implemented at this moment
        #damage = kwargs.get('damage')
        colliders = physEnabled.copy()
        self.checkCollision(colliders)
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (255, 0, 0), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), self.rect.width/2, 0)
        displaySurface.blit(self.surf, self.rect)
        pass

    def checkCollision(self, colliders):
        #when colliding set self.colliding = True
        #returns collider
        self.remove(colliders)
        element = pygame.sprite.spritecollide(self, colliders, False)
        #handleCollisions()
        if len(element) > 0:
            print(element)
        colliders.empty()

