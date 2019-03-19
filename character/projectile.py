import pygame
from character import dynamicElement

class projectile(dynamicElement.dynamicElement):
    def __init__(self, startPos, size, scale, direction, speed, physEnabled, inGame, floorGroup, superGroup, parent, damage, damageType):

        damage = 10
        self.breaksOnImpact = True
        self.velocity = pygame.math.Vector2(direction * speed * scale)

        super().__init__(startPos, size, scale, physEnabled, inGame, floorGroup, 10, self.breaksOnImpact)
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
