import pygame
pygame.init()

screen = pygame.display.set_mode((600,300))

def getFrame(cx,cy,side):
    x1 = cx-side//2
    y1 = cy-side//2
    x2 = cx+side//2
    y2 = cy+side//2
    pygame.Rect((x1,y1,x2,y2))

btnPositions = [(100, 150, 125),
               (300, 150, 150),
               (500, 150, 125)]

frameCoords = [(0,0,0,0),
               (0,0,0,0),
               (0,0,0,0)]

btnTags = ["Options","Play","Exit"]

j = 0
for i in btnPositions:
    cx = btnPositions[j][0]
    cy = btnPositions[j][1]
    side = btnPositions[j][2]
    frameCoords[j] = getFrame(cx,cy,side)
    j += 1

print(frameCoords[0])
print(frameCoords[1])
print(frameCoords[2])

while True:
    screen.fill(("gray5"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    
    
    pygame.display.update()