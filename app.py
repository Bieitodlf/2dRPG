import pygame
from pygame.locals import * 
from terrain.floor import floor
from terrain.level import level
from character.player import player
from character.character import character

class App(object):

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1920, 1080
        self.screenRect = pygame.Rect((0, 0), self.size)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.screenRect.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self._running = True
        # call map loader in the future this responds to event
        self.scale = 50 #world scale, make adjustable in the future
        self.inGame = pygame.sprite.Group()
        self.physEnabled = pygame.sprite.Group()
        self.level = level(self.screenRect, self.scale)
        self.player = player(self.screenRect.center, 1, self.scale, self.physEnabled, self.inGame, self.level.floors[0].group) #pass center screen, playerSize and scale
        self.enemy = character((self.screenRect.center[0], self.screenRect.center[1] - 200), 1, self.scale, self.physEnabled, self.inGame, self.level.floors[0].group)
        
        self.actionBuffer = [] #stores actions onto a buffer to send to object

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
           ##attack
           if event.key == pygame.K_SPACE:
               self.actionBuffer.append('player.attack.SHOOT')
           elif event.key == pygame.K_b:
               self.actionBuffer.append('player.attack.THROW')

        # implement player events
    
    def heldKeys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.actionBuffer.append('player.move.UP')
        if keys[pygame.K_DOWN]:
            self.actionBuffer.append('player.move.DOWN')
        if keys[pygame.K_LEFT]:
            self.actionBuffer.append('player.move.LEFT')
        if keys[pygame.K_RIGHT]:
            self.actionBuffer.append('player.move.RIGHT')

    def on_loop(self):
        self.heldKeys()
        while (len(self.actionBuffer) != 0):
            actionElements = self.actionBuffer.pop().split(".")
            #print(actionElements)
            if len(actionElements) == 3:
                element, actionType, action = actionElements[0], actionElements[1], actionElements[2]
                if element == 'player':
                    #print(actionType, action)
                    self.player.addAction(actionType, action)
 
            else:
                print("app.py: wrong number of actionElements in actionBuffer")

        colliders = pygame.sprite.Group()
        colliders = self.physEnabled.copy()
        
        frameTime = self.clock.get_time()/1000.0
        for element in self.inGame:
            element.update(frameTime, colliders)
        self.clock.tick()

    def on_render(self):
        #draw map floor by floor, players
        self.level.renderBackground(self._display_surf)
        for floorNumber, floor in self.level.floors.items():
            floor.renderGround(self._display_surf)
            for sprite in floor.group:
                if self.inGame.has(sprite):
                   sprite.render(self._display_surf)
            floor.renderWalls(self._display_surf)

        #for element in self.inGame.sprites():
        #    element.render(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.time.delay(100)

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
