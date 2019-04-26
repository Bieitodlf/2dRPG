import sys
import sdl2
import sdl2.ext
from Utilities import *
from Physics import *
from Map import *

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

