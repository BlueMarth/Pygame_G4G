import pygame
pygame.init()

screen = pygame.display.set_mode((600,300))

def getBtnCorner(cx,cy,side):
    x1 = cx - side//2
    y1 = cy - side//2
    x2 = cx + side//2
    y2 = cy + side//2
    return x1, y1, x2, y2

def getBtnDrawPara(cx,cy,side):
    x = cx - side//2
    y = cy - side//2
    w = side
    h = side
    return x, y, w, h

side = 100
btnDimensions = [(100, 150, side),
               (300, 150, side),
               (500, 150, side)]

frameCoords = [(0,0,0,0),
               (0,0,0,0),
               (0,0,0,0)]

btnDrawPara = [(0,0,0,0),
               (0,0,0,0),
               (0,0,0,0)]

j = 0
for i in btnDimensions:
    cx = btnDimensions[j][0]
    cy = btnDimensions[j][1]
    side = btnDimensions[j][2]
    frameCoords[j] = getBtnCorner(cx,cy,side)
    btnDrawPara[j] = getBtnDrawPara(cx,cy,side)
    j += 1

btnTags = ["Options","Play","Exit"]

options_btn_coords = frameCoords[0]
play_btn_coords = frameCoords[1]
quit_btn_coords = frameCoords[2]

options_btn_drawPara = btnDrawPara[0]
play_btn_drawPara = btnDrawPara[1]
quit_btn_drawPara = btnDrawPara[2]

print(options_btn_coords)
print(play_btn_coords)
print(quit_btn_coords)

running = True

while running:
    screen.fill(("gray5"))
    options_btn = pygame.draw.rect(screen, "lightblue", options_btn_drawPara)
    play_btn = pygame.draw.rect(screen, "lightblue", play_btn_drawPara)
    quit_btn = pygame.draw.rect(screen, "lightblue", quit_btn_drawPara)
    
    def inflateBtn(x,y,w,h):
        x -= 6
        y -= 6
        w += 12
        h += 12
        return x, y, w, h
    
    def deflateBtn(x,y,w,h):
        x += 6
        y += 6
        w -= 12
        h -= 12
        return x, y, w, h

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # within Options button
            if options_btn_coords[0] <= mouse[0] <= options_btn_coords[2] \
            and options_btn_coords[1] <= mouse[1] <= options_btn_coords[3]:
                x = options_btn_drawPara[0]
                y = options_btn_drawPara[1]
                w = options_btn_drawPara[2]
                h = options_btn_drawPara[3]
                options_btn_drawPara = inflateBtn(x,y,w,h)
            # within Play button
            elif play_btn_coords[0] <= mouse[0] <= play_btn_coords[2] \
            and play_btn_coords[1] <= mouse[1] <= play_btn_coords[3]:
                pass
            # within Quit button
            elif quit_btn_coords[0] <= mouse[0] <= quit_btn_coords[2] \
            and quit_btn_coords[1] <= mouse[1] <= quit_btn_coords[3]:
                pass
        
        if event.type == pygame.MOUSEBUTTONUP:
            # within Options button
            if options_btn_coords[0] <= mouse[0] <= options_btn_coords[2] \
            and options_btn_coords[1] <= mouse[1] <= options_btn_coords[3]:
                x = options_btn_drawPara[0]
                y = options_btn_drawPara[1]
                w = options_btn_drawPara[2]
                h = options_btn_drawPara[3]
                options_btn_drawPara = deflateBtn(x,y,w,h)
            # within Play button
            elif play_btn_coords[0] <= mouse[0] <= play_btn_coords[2] \
            and play_btn_coords[1] <= mouse[1] <= play_btn_coords[3]:
                pass
            # within Quit button
            elif quit_btn_coords[0] <= mouse[0] <= quit_btn_coords[2] \
            and quit_btn_coords[1] <= mouse[1] <= quit_btn_coords[3]:
                running = False
    
    mouse = pygame.mouse.get_pos()

    if options_btn_coords[0] <= mouse[0] <= options_btn_coords[2] \
    and options_btn_coords[1] <= mouse[1] <= options_btn_coords[3]:
        pass
    
    

    pygame.display.update()

pygame.quit()