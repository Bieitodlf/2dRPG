import pygame

class floor():
      
    def __init__(self, screenSize):
        #pass
        self.mapSurface = pygame.Surface(screenSize)
        self.mapSize = self.width, self.height = screenSize
        self.screenCenter = self.width/2, self.height/2

    def load(self, scale):
        self.scale = scale
        self.gridDimensions = self.scale
        self.visibleGrid = self.visibleX, self.visibleY = 15, 15
        x_gridPos = 0
        y_gridPos = 0
        
        #fill in 10x10 point grid with screen coordinates
        #possibly substitute with numpy matrices to use transformations
        self.floorGrid = [
                [(x * self.gridDimensions, y * self.gridDimensions) for y in range(self.visibleGrid[0])] for x in range(self.visibleGrid[1])
                ]

        #implement map grid for terrain and initial movement mechanics
        gridStartX = self.screenCenter[0] - self.visibleX/2 * self.gridDimensions
        gridStartY = self.screenCenter[1] - self.visibleY/2 * self.gridDimensions
        self.floorGridLines = [
                [(gridStartX + col * self.gridDimensions, 0), (gridStartX + col * self.gridDimensions, self.mapSize[1])] for col in range(self.visibleX)
                ] 
        floorGridLines_hori = [
                [(0, gridStartY + row * self.gridDimensions), (self.mapSize[0], gridStartY + row * self.gridDimensions)] for row in range(self.visibleY)
                ]
        for pointPair in floorGridLines_hori:
            self.floorGridLines.append(pointPair)

        #find a way to render only the visible map

    def render(self, displaySurf):
        #pass
        self.mapSurface = self.mapSurface.convert()
     
        #draw grid
        [pygame.draw.line(self.mapSurface, (255, 255, 255), pointPair[0], pointPair[1], 5) for pointPair in self.floorGridLines]

        #draw grid centered dots
        #[[pygame.draw.circle(self.mapSurface, (255, 255, 255), coord, 5, 0) for coord in col] for col in self.floorGrid]
        displaySurf.blit(self.mapSurface, (0, 0))
