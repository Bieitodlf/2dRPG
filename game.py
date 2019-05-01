import sys
import sdl2
import sdl2.ext
<<<<<<< HEAD
from Utilities import *
from Physics import *
from Map import *

class dynElement(sdl2.ext.Entity):
    def __init__(self, world, sprite, centerPos, size, velocity, mass):
=======
import math
from Utilities import *
from Physics import *
#from Map import *

class dynElement(sdl2.ext.Entity):
    def __init__(self, world, sprite, centerPos, size, velocity, mass, isPlayerControlled, isViewPortAttached):
>>>>>>> master
        self.sprite = sprite
        print(self.sprite.position, self.sprite.size)
        self.bbox = Bbox(centerPos, size)
        topLeft = self.bbox.getPosition()
<<<<<<< HEAD
        self.sprite.position = topLeft[0], topLeft[1]
        print(self.bbox.getPosition(), self.bbox.getSize())
        self.momentum = Momentum(velocity, mass)
=======
        self.sprite.position = math.floor(topLeft[0]), math.floor(topLeft[1])
        print(self.bbox.getPosition(), self.bbox.getSize())
        self.momentum = Momentum(velocity, mass)
        self.controlinfo = ControlInfo(isPlayerControlled, isViewPortAttached)
        print(self.controlinfo.isPlayerControlled, self.controlinfo.isViewPortAttached)
>>>>>>> master

class ViewPort():
    #keeps track of viewPort position in relation to the map origin.
    #The map origin will be the refference point for all game elements.
    #This entity will also hold a Bbox that will be used for map scrolling logic, if needed
<<<<<<< HEAD
    def __init__(self, centerPos, size, playerBoxMargin):
        self.bbox = Bbox(centerPos, size)
        self.playerBox = Bbox(centerPos, vectSub(size, [playerBoxMargin, playerBoxMargin]))

    def setCenterPos(self, centerX, centerY):
        self.box.setCenterPos(centerX, centerY)
        self.playerBox.setCenterPos(centerX, centerY)
=======
    def __init__(self, world, centerPos, size, playerBoxMargin):
        super().__init__()
        self.bbox = Bbox(centerPos, size)
        self.playerBox = Bbox(centerPos, vectSub(size, playerBoxMargin))
        marginHalfSize = scalarDiv(playerBoxMargin, 2, integer=True)

    def getOffset(self):
        return scalarProduct(self.bbox.position, -1)

    def setCenterPos(self, centerPos):
        self.bbox.setCenterPos(centerPos)
        self.playerBox.setCenterPos(self.bbox.getCenterPos())
>>>>>>> master

    def getCenterPos(self):
        return self.bbox.getCenterPos()

<<<<<<< HEAD
    def getScreenBounds(self):
        return bounds(self.bbox.getPosition(), self.box.getSize())

    def getPlayerBounds(self):
        return bounds(self.playerBox.getPosition(), self.playerBox.getSize())

    def bounds(topLeft, size):
=======
    def getPosition(self):
        return self.bbox.getPosition()

    def getScreenBounds(self):
        return bounds(self.bbox.getPosition(), vectAdd(self.bbox.getPosition, self.box.getSize()))

    def getPlayerBounds(self):
        return [self.playerBox.getPosition(), vectAdd(self.playerBox.getPosition(), self.playerBox.getSize())]
        #return self.bounds(self.playerBox.getPosition(), self.playerBox.getSize())

    def bounds(self, topLeft, size):
>>>>>>> master
        minX = topLeft[0]
        minY = topLeft[1]
        maxX = topLeft[0] + size[0]
        maxY = topLeft[1] + size[1]
<<<<<<< HEAD
        return (minX, maxX, minY, maxY)


class HardwareRenderer(sdl2.ext.TextureSpriteRenderSystem, ViewPort):
=======
        return [minX, maxX], [minY, maxY]

##################################################
#unused code, review for deletion
##################################################

class PlayerBoundary():
    def __init__(self, viewPort, position, size):
        self.position = position
        self.size = size
        self.halfSize = scalarDiv(self.size, 2)
        self.centerPos = vectAdd(self.position, self.halfSize)

    def setSize(self, width, height):
        self.size = [width, height]
        self.halfSize = scalarDiv(self.size, 2)
        self.centerPos = vectAdd(self.position, self.halfSize)

    def getSize(self):
        return self.size

    def getHalfSize(self):
        return self.halfSize

    def setPosition(self, position):
        self.position = position
        self.centerPos = vectAdd(self.position, self.halfSize)

    def getPosition(self):
        return self.position

class ViewPortManagingSystem(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = Bbox

    def process(self, world, componentSets):
        for box in componentSets:
            if box.get_entities():
                pass
################################################
#end unused code
################################################

class HardwareRenderer(sdl2.ext.TextureSpriteRenderSystem):
>>>>>>> master
    def __init__(self, window, viewPort):
        super().__init__(window)
        self.viewPort = viewPort

    def render(self, components):
        sdl2.ext.Renderer.clear(self)
<<<<<<< HEAD
        offset = self.viewPort.getCenterPos()
        super().render(components, x = offset[0], y = offset[1])
=======
        offset = self.viewPort.getOffset()
        super().render(components, x = int(offset[0]), y = int(offset[1]))#function requires integers
>>>>>>> master

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
<<<<<<< HEAD
    viewPort = ViewPort((windowSize[0]//2, windowSize[1]//2), windowSize, 20) 
    #instantiating components
    spriteRenderer = HardwareRenderer(window, viewPort)
    movement = MovementSystem()
=======
    viewPort = ViewPort(appWorld, (windowSize[0]//2, windowSize[1]//2), windowSize, [192, 108]) 
    #instantiating components
    spriteRenderer = HardwareRenderer(window, viewPort)
    movement = MovementSystem(viewPort)
>>>>>>> master
    collision = CollisionSystem()

    #add components to world
    appWorld.add_system(spriteRenderer)
    appWorld.add_system(movement)
    appWorld.add_system(collision)

    spriteFactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=spriteRenderer)
    playerSprite = spriteFactory.from_color((255, 0, 255), size = (50, 50))
    #(world, sprite, centerPos, size, velocity, mass) remember player sprite size is independent from element size
<<<<<<< HEAD
    player = dynElement(appWorld, playerSprite, [0, 0], [50, 50], [0, 0], 5)
    enemySprite = spriteFactory.from_color((255, 255, 0), size = (50, 50))
    enemy = dynElement(appWorld, enemySprite, [100, 100], [50, 50], [0, 0], 5)
=======
    player = dynElement(appWorld, playerSprite, viewPort.getCenterPos(), [50, 50], [0, 0], 5, True, True)
    enemySprite1 = spriteFactory.from_color((255, 255, 0), size = (50, 50))
    enemy1 = dynElement(appWorld, enemySprite1, vectAdd(viewPort.getCenterPos(), [100, 100]), [50, 50], [0, 0], 5, False, False)
    enemySprite2 = spriteFactory.from_color((0, 255, 255), size = (50, 50))
    enemy2 = dynElement(appWorld, enemySprite2, vectSub(viewPort.getCenterPos(), [100, 100]), [50, 50], [0, 0], 5, False, False)
>>>>>>> master
    eventHandler = EventHandler(player)

    while eventHandler.programRunning():
        appWorld.process()
<<<<<<< HEAD
        sdl2.SDL_Delay(50)
=======
        sdl2.SDL_Delay(10)
>>>>>>> master

    sdl2.ext.quit()

if __name__ == "__main__":
    sys.exit(app())

