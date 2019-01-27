import pygame
from pygame.locals import * 
from terrain.floor import floor
from character.player import player

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1920, 1080
        self.center = self.centerX, self.centerY = self.width/2, self.height/2

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self._running = True
        # call map loader in the future this responds to event
        self.terrain = floor(self.size)
        self.scale = 100 #world scale, make adjustable in the future
        self.terrain.load(self.scale)
        self.player = player(self.center, 1, self.scale) #pass center screen, playerSize and scale
        self.actionBuffer = [] #stores actions onto a buffer to send to objects

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

        # implement player events

    def on_loop(self):
        while (len(self.actionBuffer) != 0):
            actionElements = self.actionBuffer.pop().split(".")
            print(actionElements)
            if len(actionElements) == 3:
                element, actionType, action = actionElements[0], actionElements[1], actionElements[2]
                if element == 'player':
                    #print(actionType, action)
                    self.player.addAction(actionType, action)
 
            else:
                print("app.py: wrong number of actionElements in actionBuffer")
            
        # process player events from on_event()

    def on_render(self):
        #pass
        # draw map, players
        self.terrain.render(self._display_surf)
        self.player.render(self._display_surf)
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

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()