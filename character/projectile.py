from . import dynamicElement

class projectile(dynamicElement):
    def __init__(self, startPos, size, scale, direction, speed, physEnabled, damage, damageType):
        dynamicElement.__init__(self, startPos, size, scale, physEnabled)
        self.damage = 10

    def update():
        #takes in physics info
        #checkCollision() will return collider for damage
        pass
    
    def move():
        pass
