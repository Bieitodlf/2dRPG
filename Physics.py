import sys
import sdl2
import sdl2.ext
<<<<<<< HEAD
=======
import math
>>>>>>> master
from Utilities import *

class Bbox():
    #Bbox keeps track of both center position and topLeft position
    def __init__(self, centerPos, size):
        self.centerPos = centerPos
        self.size = size
<<<<<<< HEAD
        self.halfSize = [self.size[0]//2, self.size[1]//2]
=======
        self.halfSize = scalarDiv(self.size, 2)
>>>>>>> master
        self.position = vectSub(self.centerPos, self.halfSize)

    def setSize(self, width, height):
        self.size = [width, height]
<<<<<<< HEAD
        self.halfSize = [self.size[0]//2, self.size[1]//2]

        self.position = vectSub(self.centerPos, self.halfSize)
        self.sprite.position(self.position[0], self.position[1])
=======
        self.halfSize = scalarDiv(self.size, 2)

        self.position = vectSub(self.centerPos, self.halfSize)
        self.sprite.position(math.floor(self.position[0]), math.floor(self.position[1]))
>>>>>>> master

    def getSize(self):
        return self.size

    def getHalfSize(self):
        return self.halfSize

<<<<<<< HEAD
    def setPosition(self, posX, posY):
        #sets the topLeft position and recalculates center
        self.position = [posX, posY]
=======
    def setPosition(self, position):
        #sets the topLeft position and recalculates center
        self.position = position
>>>>>>> master
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

<<<<<<< HEAD
=======
    def updatePosition(self):
        self.position = vectSub(self.centerPos, self.halfSize)
>>>>>>> master

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

<<<<<<< HEAD
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


=======
class ControlInfo():
    def __init__(self, isPlayerControlled, isViewPortAttached):
        self.isPlayerControlled = isPlayerControlled
        self.isViewPortAttached = isViewPortAttached

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, viewPort):
        super().__init__()
        self.viewPort = viewPort
        self.componenttypes = Bbox, Momentum, sdl2.ext.Sprite, ControlInfo

    def process(self, world, componentSets):
        for bbox, momentum, sprite, controlinfo in componentSets:
            oldCenterPos = bbox.getCenterPos()
            velocity = momentum.getVelocity()
            newCenterPos = vectAdd(bbox.getCenterPos(), velocity)
            #
            #investigate sprite object
            #
            bbox.setCenterPos(newCenterPos)
            newTopLeft = bbox.getPosition()
            sprite.position = int(newTopLeft[0]), int(newTopLeft[1])
            
            #viewPort scrolling
            if (controlinfo.isViewPortAttached == True):
                bounds = self.viewPort.getPlayerBounds()#player box, if outside, viewPort moves
                delta = [0, 0]#how much it scrolls
                direction = [signOf(velocity[0]), signOf(velocity[1])]
                
                #X direction check
                if (newTopLeft[0] < bounds[0][0] and direction[0] < 0 or
                        (newTopLeft[0] + bbox.getSize()[0]) > bounds[1][0] and direction[0] > 0): 
                    delta = vectAdd(delta, [velocity[0], 0])

                #Y direction check
                if (newTopLeft[1] < bounds[0][1] and direction[1] < 0 or
                        (newTopLeft[1] + bbox.getSize()[1]) > bounds[1][1] and direction[1] > 0):
                    delta = vectAdd(delta, [0, velocity[1]])
                
                #viewPort displacement
                self.viewPort.setCenterPos(vectAdd(self.viewPort.getCenterPos(), delta))
>>>>>>> master

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
