import pygame
from .dynamicElement import dynamicElement

class projectile(dynamicElement):
    def __init__(self, startPos, size, scale, direction, speed, physEnabled, inGame, superGroup, damage, damageType):
        damage = 10
        self.breaksOnImpact = True
        self.superGroup = superGroup
        self.superGroup.add(self)
        self.speed = speed
        self.velocity = pygame.math.Vector2(direction * speed)

        dynamicElement.__init__(self, startPos, size, scale, physEnabled, inGame, 10, self.breaksOnImpact)
        self.move(self.velocity)

    def autoUpdate(self):
        #takes in physics info
        #checkCollision() will return collider for damage
        self.move(self.velocity)
        print(self.rect.center)
        pass
    
    def destroy(self):
        pass

    def handleCollission(self, collider):
        self.kill()
        print(self.alive())
        self = None
        del self

