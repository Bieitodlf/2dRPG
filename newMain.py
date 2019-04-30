import sys
import sdl2
import sdl2.ext

#utilities
signOf = lambda a: (a > 0) - (a < 0)

vectSameLength = lambda a, b: len(a) == len(b)

def vectAdd(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
        result = []
        for dimension in zip(vect1, vect2):
            result.append(dimension[0] + dimension[1])

        return result
    print("cannot add different size vectors")
    return None

def vectSub(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
        result = []
        for dimension in zip(vect1, vect2):
            result.append(dimension[0] - dimension[1])

        return result
    print("cannot subtract different size vectors")
    return None

def vectElementMult(vect1, vect2):
    if (vectSameLength(vect1, vect2)):
            result = []
            for dimension in zip(vect1, vect2):
                result.append(dimension[0] * dimension[1])
            return result
    else:
        print("cannot multiply elementwise different size vectors")
        return None

def vectAbs(vect):
    result = []
    for dimension in vect:
        result.append(abs(dimension))
    return result

def scalarAdd(vect, scalar):
    result = []
    for dimension in vect:
        result.append(dimension + scalar)
    return result

def scalarProduct(vect, scalar):
    result = []
    for dimension in vect:
        result.append(dimension * scalar)
    return result

class vector():
    def __init__(initData):
        pass

#end utilities  

class dynElement(sdl2.ext.Entity):
    def __init__(self, world, sprite, centerPos, size, velocity, mass):
        self.sprite = sprite
        print(self.sprite.position, self.sprite.size)
        self.bbox = Bbox(centerPos, size)
        topLeft = self.bbox.getPosition()
        self.sprite.position = topLeft[0], topLeft[1]
        print(self.bbox.getPosition(), self.bbox.getSize())
        self.momentum = Momentum(velocity, mass)

class ViewPort():
    #keeps track of viewPort position in relation to the map origin.
    #The map origin will be the refference point for all game elements.
    #This entity will also hold a Bbox that will be used for map scrolling logic, if needed
    def __init__(self, centerPos, size, playerBoxMargin):
        self.bbox = Bbox(centerPos, size)
        self.playerBox = Bbox(centerPos, vectSub(size, [playerBoxMargin, playerBoxMargin]))

    def setCenterPos(self, centerX, centerY):
        self.box.setCenterPos(centerX, centerY)
        self.playerBox.setCenterPos(centerX, centerY)

    def getCenterPos(self):
        return self.bbox.getCenterPos()

    def getScreenBounds(self):
        return bounds(self.bbox.getPosition(), self.box.getSize())

    def getPlayerBounds(self):
        return bounds(self.playerBox.getPosition(), self.playerBox.getSize())

    def bounds(topLeft, size):
        minX = topLeft[0]
        minY = topLeft[1]
        maxX = topLeft[0] + size[0]
        maxY = topLeft[1] + size[1]
        return (minX, maxX, minY, maxY)

class Bbox():
    #Bbox keeps track of both center position and topLeft position
    def __init__(self, centerPos, size):
        self.centerPos = centerPos
        self.size = size
        self.halfSize = [self.size[0]//2, self.size[1]//2]
        self.position = vectSub(self.centerPos, self.halfSize)

    def setSize(self, width, height):
        self.size = [width, height]
        self.halfSize = [self.size[0]//2, self.size[1]//2]

        self.position = vectSub(self.centerPos, self.halfSize)
        self.sprite.position(self.position[0], self.position[1])

    def getSize(self):
        return self.size

    def getHalfSize(self):
        return self.halfSize

    def setPosition(self, posX, posY):
        #sets the topLeft position and recalculates center
        self.position = [posX, posY]
        self.centerPos = vectAdd(self.position, self.halfSize)

    def getPosition(self):
        #returns topLeft Position
        return vectSub(self.centerPos, self.halfSize)

    def setCenterPos(self, centerPos):
        #sets center position and recalculates topLeft
        self.centerPos = centerPos
        self.position = vectSub(self.centerPos, self.halfSize)

    def getCenterPos(self):
        #returns box center position
        return self.centerPos

    def getCorners(self):
        topLeft = self.getPosition()
        return (topLeft, vectAdd(topLeft, [self.size[0], 0]), vectAdd(topLeft, self.size), vectAdd(topLeft, [0, self.size[1]]))


class Momentum():
    def __init__(self, velocity, mass):
        self.velocity = velocity
        self.mass = mass
        self.momentum = velocity * mass

    #getters and setters for Momentum class
    def setVelocity(self, velocity, x=False, y=False):
        if (x == True):
            self.velocity[0] = velocity[0]
        if (y == True):
            self.velocity[1] = velocity[1]

    def getVelocity(self):
        return self.velocity

    def setMass(self, mass):
        self.mass = mass

    def getMass(self):
        return self.mass

    def getMomentum(self):
        return self.momentum

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = Bbox, Momentum, sdl2.ext.Sprite

    def process(self, world, componentSets):
        for bbox, momentum, sprite in componentSets:
            newCenterPos = vectAdd(bbox.getCenterPos(), momentum.getVelocity())
            bbox.setCenterPos(newCenterPos)
            #
            #investigate sprite object
            #
            topLeft = bbox.getPosition()
            sprite.position = ((topLeft[0], topLeft[1]))



class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = Bbox, Momentum, sdl2.ext.Sprite

    def process(self, world, componentSets):
        colliderList = []
        for bbox, momentum, sprite in componentSets:
            colliderList.append((bbox, momentum, sprite))
        
        self.checkCollision(colliderList[0], colliderList[1:])
        ##remember checkCollision() consumes the passed list it should recieve a deep copy
        ##resolve collisions for large Bbox
        ##implement down the line fine collision logic

    def checkCollision(self, collider, colliderList):
        #recursive nature ensures each pair is only checked once. Colliders removed from list at each call
        listLen = len(colliderList)
        if listLen > 0:
            for item in colliderList:
                if self.broadPhase(collider, item):
                    self.narrowPhase(collider, item)
            self.checkCollision(colliderList.pop(), colliderList)

    def broadPhase(self, collider, item):
        #If bounding boxes overlap, narrow phase is executed
        colliderBox = collider[0]
        itemBox = item[0]
        if self.boxOverlap(colliderBox, itemBox):
            self.narrowPhase(collider, item)

    def narrowPhase(self, collider, item):
        #future detailed collision logic
        self.resolveCollision(collider, item)

    def boxOverlap(self, box1, box2):
        #corners are labeled clockwise from topLeft
        box1TopLeft = box1.getPosition()
        box1BottomRight = vectAdd(box1TopLeft, box1.getSize())
        box2TopLeft = box2.getPosition()
        box2BottomRight = vectAdd(box2TopLeft, box2.getSize())
        
        noXOverlap = box1TopLeft[0] > box2BottomRight[0] or box1BottomRight[0] < box2TopLeft[0]
        noYOverlap = box1TopLeft[1] > box2BottomRight[1] or box1BottomRight[1] < box2TopLeft[1]
        #returns true if there is overlap
        return not(noXOverlap or noYOverlap)


##############################################################################
#unused code related to collisions, will detect which vertex to aply force to
##############################################################################
    def getDirection(self, item1, item2):
        #2 dimension "vector" (x, y) where values are -1, 0 or 1 representing the required correction direction
        direction = [0, 0]
        #at the moment, we asume item boxes are rectangular
        #directions are given with respect to item1, later logic needs to account for which item to move
        item1Vertices = item1.getCorners()
        item2Vertices = item2.getCorners()
        #first we check for vertices of item2 whithin item1, if there are none, we check for vertices of item1 within item2
        #because they are axis aligned bounding boxes, there can be 1, 2 or 4 vertices of one box within the other box_
        #this leads to 9 posibilities stored as 9 bits
        caseValue = 0
        collisionOrder = 1 #this value represents whether the direction was calculated using item1 vertices(-1) or item2 vertices(1)
        for vertex in item2Vertices:
            caseValue = (caseValue << 1) + vertexInsideBox(vertex, item1)

        if (caseValue == 0):
            #no vertex was found of item2 whithin item1
            for vertex in item1Vertices:
                caseValue = (caseValue << 1) + vertexInsideBox(vertex, item2)
            if (caseValue == 0):
                print("warning, narrowPhase Collision was called but no collision happened")
            else:
                collisionOrder = -1
        else:
            #elif cascade to deal with which vertices overlap and returns the direction
            pass
        return scalarProduct(direction, collisionOrder) 

    def vertexInsideBox(self, vertex, box):
        boxTopLeft = box.getPosition()
        boxBottomRight = vectAdd(boxTopLeft, box.size)
        if (vertex[0] > boxTopLeft[0] and vertex[0] < boxBottomRight[0]
                and vertex[1] > boxTopLeft[1] and vertex[0] < boxBottomRight[1]):
            return True
        else:
            return False

####################################################################
#end unused code
####################################################################

    def resolveCollision(self, collider, item):
        if (collider[1].getMass() > 0):#the collider is movable
            if (item[1].getMass() > 0):#the item collided with is movable
                #print("conserve momentum")
                print("item is pushable")
                self.rectifyMovement(item[0], collider[0], item[1].getVelocity(), collider[1].getVelocity())
            else:#the item collided with is not movable
                print("collided with inmovable item")
                self.rectifyMovement(collider[0], item[0], collider[1].getVelocity(), item[1].getVelocity())
        else:#the collider is not movable, no sense in checking if they are both inmovable as nothing would happen
            print("item collided with inmovable object")
            self.rectifyMovement(item[0], collider[0], item[1].getVelocity(), collider[1].getVelocity())

    def rectifyMovement(self, movableBox, inmovableBox, movableVel, inmovableVel):
        direction = vectSub(inmovableVel, movableVel)
        minDistance = vectAdd(movableBox.getHalfSize(), inmovableBox.getHalfSize())
        collDistance = vectSub(inmovableBox.getCenterPos(), movableBox.getCenterPos())
        overlap = vectSub(minDistance, vectAbs(collDistance))
        minDistance = scalarAdd(minDistance, 1)#ensures that there is no collision after the correction
        correction = vectElementMult(minDistance, [signOf(direction[0]), signOf(direction[1])])
        #if else chain checks which direction the object was moving in relation with the inmovable object
        if (abs(direction[0]) > abs(direction[1])):#collision in the X direction
            movableBox.setCenterPos([inmovableBox.getCenterPos()[0] + correction[0], movableBox.getCenterPos()[1]])
            
        elif (abs(direction[0]) < abs(direction[1])):#collision in the Y direction
            movableBox.setCenterPos([movableBox.getCenterPos()[0], inmovableBox.getCenterPos()[1] + correction[1]])

        elif (abs(direction[0]) == abs(direction[1])):#collision is diagonal
            #smallest overlap direction must be the collision direction
            if (abs(overlap[0]) > abs(overlap[1])):#collision in Y direction
                movableBox.setCenterPos([movableBox.getCenterPos()[0], inmovableBox.getCenterPos()[1] + correction[1]])

            elif (abs(overlap[0]) < abs(overlap[1])):#collision in X direction
                movableBox.setCenterPos([inmovableBox.getCenterPos()[0] + correction[0], movableBox.getCenterPos()[1]])

            else: #collision is diagonal against a corner
                print("corner")#Broken. Fix, no collision if collision is directly in the corner and diagonal.
                #movableBox.setCenterPos(vectSub(inmovableBox.getCenterPos(), correction))


class HardwareRenderer(sdl2.ext.TextureSpriteRenderSystem, ViewPort):
    def __init__(self, window, viewPort):
        super().__init__(window)
        self.viewPort = viewPort

    def render(self, components):
        sdl2.ext.Renderer.clear(self)
        offset = self.viewPort.getCenterPos()
        super().render(components, x = offset[0], y = offset[1])

class EventHandler():
    def __init__(self, player):
        self.isRunning = True
        self.player = player

    def programRunning(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                return False
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_q:
                    return False
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.player.momentum.setVelocity([0, -3], y = True)
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.player.momentum.setVelocity([0, 3], y = True)
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.player.momentum.setVelocity([-3, 0], x = True)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.player.momentum.setVelocity([3, 0], x = True)


            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.player.momentum.setVelocity([0, 0], y = True)
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.player.momentum.setVelocity([0, 0], y = True)
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.player.momentum.setVelocity([0, 0], x = True)
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.player.momentum.setVelocity([0, 0], x = True)

        return self.isRunning
    
def app():
    sdl2.ext.init()
    windowSize = 1920, 1080
    window = sdl2.ext.Window("New Graphics Module", size = windowSize)
    window.show()

    appWorld = sdl2.ext.World()
    viewPort = ViewPort((windowSize[0]//2, windowSize[1]//2), windowSize, 20) 
    #instantiating components
    spriteRenderer = HardwareRenderer(window, viewPort)
    movement = MovementSystem()
    collision = CollisionSystem()

    #add components to world
    appWorld.add_system(spriteRenderer)
    appWorld.add_system(movement)
    appWorld.add_system(collision)

    spriteFactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=spriteRenderer)
    playerSprite = spriteFactory.from_color((255, 0, 255), size = (50, 50))
    #(world, sprite, centerPos, size, velocity, mass) remember player sprite size is independent from element size
    player = dynElement(appWorld, playerSprite, [0, 0], [50, 50], [0, 0], 5)
    enemySprite = spriteFactory.from_color((255, 255, 0), size = (50, 50))
    enemy = dynElement(appWorld, enemySprite, [100, 100], [50, 50], [0, 0], 5)
    eventHandler = EventHandler(player)

    while eventHandler.programRunning():
        appWorld.process()
        sdl2.SDL_Delay(50)

    sdl2.ext.quit()

if __name__ == "__main__":
    sys.exit(app())

