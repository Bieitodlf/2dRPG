import sys
import sdl2
import sdl2.ext

def run():

    sdl2.ext.init()
    window = sdl2.ext.Window("Hello World!", size = (800, 600))
    window.show()

    world = sdl2.ext.World()

    spriteRenderer = SoftwareRenderer(window)
    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)
    
    world.add_system(spriteRenderer)
    world.add_system(movement)
    world.add_system(collision)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 780, 250)
    ball = Ball(world, sp_ball, 390, 290)
    ball.velocity.vx = -3

    collision.ball = ball

    events = eventHandler(player1)
    running = True
    while events.handleEvents():
        sdl2.SDL_Delay(10)
        world.process()

    sdl2.ext.quit()
    return 0

class eventHandler():
    def __init__(self, player):
        self.player = player

    def handleEvents(self):
        eventQueue = sdl2.ext.get_events()
        for event in eventQueue:
            if event.type == sdl2.SDL_QUIT:
                return False

            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_q:
                    return False
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.player.velocity.vy = -3
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.player.velocity.vy = 3

            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    self.player.velocity.vy = 0

        return True

WHITE = sdl2.ext.Color(255, 255, 255)
BLACK = sdl2.ext.Color(0, 0, 0)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super().__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super().render(components)

class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posX=0, posY=0):
        self.sprite = sprite
        self.sprite.position = posX, posY
        self.velocity = Velocity()

class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posX=0, posY=0):
        self.sprite = sprite
        self.sprite.position = posX, posY
        self.velocity = Velocity()

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minX, minY, maxX, maxY):
        super().__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

    def process(self, world, componentSets):
        for velocity, sprite in componentSets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minX, sprite.x)
            sprite.y = max(self.minY, sprite.y)

            pmaxX = sprite.x + swidth
            pmaxY = sprite.y + sheight
            if pmaxX > self.maxX:
                sprite.x = self.maxX - swidth
            if pmaxY > self.maxY:
                sprite.y = self.maxY - sheight

class Velocity():
    def __init__(self):
        self.vx = 0
        self.vy = 0

class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minX, minY, maxX, maxY):
        super().__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

    def _overlap(self, other):
        pos, sprite = other
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and btop < bottom and bbottom > top)

    def process(self, world, componentSets):
        collitems = [comp for comp in componentSets if self._overlap(comp)]
        if collitems:

            sprite = collitems[0][1]
            ballCenterY = self.ball.sprite.y + self.ball.sprite.size[1] //2
            halfHeight = sprite.size[1] // 2
            stepSize = halfHeight // 10
            degrees = 0.7
            paddleCenterY = sprite.y + halfHeight
            self.ball.velocity.vx = -self.ball.velocity.vx
            if ballCenterY < paddleCenterY:
                factor = (paddleCenterY - ballCenterY) // stepSize
                self.ball.velocity.vy = -int(round(factor * degrees))

            elif ballCenterY > paddleCenterY:
                factor = (ballCenterY - paddleCenterY) // stepSize
                self.ball.velocity.vy = int(round(factor * degrees))

            else:
                self.ball.velocity.vy = -self.ball.velocity.vy

        if (self.ball.sprite.y <= self.minY or self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxY):
                self.ball.velocity.vy = -self.ball.velocity.vy

        if (self.ball.sprite.x <= self.minX or self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxX):
                    self.ball.velocity.vx = -self.ball.velocity.vx


if __name__ == "__main__":
    sys.exit(run())
