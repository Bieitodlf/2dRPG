import pygame
from .dynamicElement import dynamicElement

class bomb(dynamicElement):
    def __init__(self, startPos, size, scale, direction, speed, physEnabled, inGame, superGroup, parent, damage, damageType):
        damage = 20
        self.breaksOnImpact = False
        self.speed = 0
        dynamicElement.__init__(self, startPos, size, scale, physEnabled, inGame, 10, self.breaksOnImpact)
        superGroup.add(self)
        self.superGroup = superGroup
        self.subGroup = pygame.sprite.Group(self)

    def autoUpdate(self):
        pass

    def render(self, displaySurface):
        pygame.draw.circle(self.surf, (0, 0, 255), (self.rect.center[0] - self.rect.topleft[0], self.rect.center[1] - self.rect.topleft[1]), self.rect.width/2, 0)
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
