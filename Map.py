import sys
import sdl2
import sdl2.ext
from Utilities import *

#find a way to load either the tilemap or a tile image array containing all of the properties of each tile
#implement that as a loadingSystem
#sprite creator for walls vs plain boxes for tiles. Consult collision system
#culling system using the viewPort
import pytmx
from pytmx.util_pygame import load_pygame

class floor():
    def __init__(self, tileSize, tiled_map, ground, walls):
        self.tileSize = tileSize
        self.width = tiled_map.width
        self.height = tiled_map.height
        self.ground = ground
        self.walls = walls
        self.loadLayer(self.groundSurface, ground, tiled_map)
        self.loadLayer(self.wallSurface, walls, tiled_map)

    def loadRules(self, tileRulesFile):
        pass

    def loadLayer(self, surface, layer, tiled_map):
        for tile in layer.tiles():
            if tile[2] != None:
                image = pygame.transform.scale(tile[2], (self.tileSize, self.tileSize))
                surface.blit(image, (tile[0] * self.tileSize, tile[1] * self.tileSize))

    def getTileIndices(self):
        pass












############################################################
#Testing Code
############################################################


class ViewPort():
    #keeps track of viewPort position in relation to the map origin.
    #The map origin will be the refference point for all game elements.
    #This entity will also hold a Bbox that will be used for map scrolling logic, if needed
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

    def getCenterPos(self):
        return self.bbox.getCenterPos()

    def getPosition(self):
        return self.bbox.getPosition()

    def getScreenBounds(self):
        return bounds(self.bbox.getPosition(), vectAdd(self.bbox.getPosition, self.box.getSize()))

    def getPlayerBounds(self):
        return [self.playerBox.getPosition(), vectAdd(self.playerBox.getPosition(), self.playerBox.getSize())]
        #return self.bounds(self.playerBox.getPosition(), self.playerBox.getSize())

    def bounds(self, topLeft, size):
        minX = topLeft[0]
        minY = topLeft[1]
        maxX = topLeft[0] + size[0]
        maxY = topLeft[1] + size[1]
        return [minX, maxX], [minY, maxY]


class HardwareRenderer(sdl2.ext.TextureSpriteRenderSystem, ViewPort):
    def __init__(self, window, viewPort):
        super().__init__(window)
        self.viewPort = viewPort

    def render(self, components):
        sdl2.ext.Renderer.clear(self)
        offset = self.viewPort.getCenterPos()
        super().render(components, x = offset[0], y = offset[1])

class EventHandler():
    def __init__(self):
        self.isRunning = True

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
    viewPort = ViewPort(appWorld, (windowSize[0]//2, windowSize[1]//2), windowSize, [192, 108]) 
    #instantiating components
    spriteRenderer = HardwareRenderer(window, viewPort)

    #add components to world
    appWorld.add_system(spriteRenderer)

    spriteFactory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=spriteRenderer)
    playerSprite = spriteFactory.from_color((255, 0, 255), size = (50, 50))
    eventHandler = EventHandler()

    while eventHandler.programRunning():
        appWorld.process()
        sdl2.SDL_Delay(50)

    sdl2.ext.quit()

if __name__ == "__main__":
    from Physics import Bbox
    sys.exit(app())

