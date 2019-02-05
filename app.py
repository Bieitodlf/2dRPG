import pygame
from pygame.locals import * 
from terrain.floor import floor
from character.player import player
from character.character import character

class App:

    actionBuffer = [] #stores actions onto a buffer to send to objects


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
        self.inGame = pygame.sprite.Group()
        self.physEnabled = pygame.sprite.Group()
        self.terrain = floor(self.screenRect)
        self.scale = 100 #world scale, make adjustable in the future
        self.terrain.load(self.scale)
        self.player = player(self.screenRect.center, 1, self.scale, self.physEnabled, self.inGame) #pass center screen, playerSize and scale
        self.enemy = character((self.screenRect.center[0], self.screenRect.center[1] - 200), 1, self.scale, self.physEnabled, self.inGame)
        
        self.actionBuffer = [] #stores actions onto a buffer to send to object

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.actionBuffer.append('player.move.UP') #get key mapping. maybe clasify for easy handiling
            elif event.key == pygame.K_DOWN:
                self.actionBuffer.append('player.move.DOWN')
            elif event.key == pygame.K_LEFT:
                self.actionBuffer.append('player.move.LEFT')
            elif event.key == pygame.K_RIGHT:
                self.actionBuffer.append('player.move.RIGHT')
            #end of move
            #attack
            elif event.key == pygame.K_SPACE:
                self.actionBuffer.append('player.attack.SHOOT')
            elif event.key == pygame.K_b:
                self.actionBuffer.append('player.attack.THROW')

        # implement player events
    
    def on_loop(self):
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
        
        frameTime = self.clock.get_time()
        for element in self.inGame:
            element.update(frameTime, colliders)
        self.clock.tick()

    def on_render(self):
        #pass
        # draw map, players
        self.terrain.render(self._display_surf)
        for element in self.inGame.sprites():
            element.render(self._display_surf)
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
