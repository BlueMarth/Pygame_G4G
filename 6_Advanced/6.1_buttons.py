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

def inflateBtn(x,y,w,h):
        x -= 5
        y -= 5
        w += 10
        h += 10
        return x, y, w, h
    
def deflateBtn(x,y,w,h):
    x += 5
    y += 5
    w -= 10
    h -= 10
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

options_img_orig = pygame.image.load("visual/options_btn.png").convert()
play_img_orig = pygame.image.load("visual/play_btn.png").convert()
quit_img_orig = pygame.image.load("visual/quit_btn.png").convert()

def get_scaled_img_and_rect(img, drawPara):
    x, y, w, h = drawPara
    scaled_img = pygame.transform.scale(img, (w, h))
    rect = scaled_img.get_rect()
    rect.topleft = (x, y)
    return scaled_img, rect

running = True
clicked_color = "lightblue"
released_color = "lightblue4"
clicked = False

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # within Options button
            if options_rect.collidepoint(event.pos):
                x,y,w,h = options_btn_drawPara
                options_btn_drawPara = inflateBtn(x,y,w,h)
                clicked = True

            # within Play button
            elif play_rect.collidepoint(event.pos):
                x,y,w,h = play_btn_drawPara
                play_btn_drawPara = inflateBtn(x,y,w,h)
                clicked = True

            # within Quit button
            elif quit_rect.collidepoint(event.pos):
                x,y,w,h = quit_btn_drawPara
                quit_btn_drawPara = inflateBtn(x,y,w,h)
                clicked = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
            # within Options button
            if options_rect.collidepoint(event.pos):
                x,y,w,h = options_btn_drawPara
                options_btn_drawPara = deflateBtn(x,y,w,h)
                clicked = False
            # within Play button
            elif play_rect.collidepoint(event.pos):
                x,y,w,h = play_btn_drawPara
                play_btn_drawPara = deflateBtn(x,y,w,h)
                clicked = False

            # within Quit button
            elif quit_rect.collidepoint(event.pos):
                x,y,w,h = quit_btn_drawPara
                quit_btn_drawPara = deflateBtn(x,y,w,h)
                clicked = False
                running = False
    
    mouse = pygame.mouse.get_pos()

    if options_btn_coords[0] <= mouse[0] <= options_btn_coords[2] \
    and options_btn_coords[1] <= mouse[1] <= options_btn_coords[3]:
        pass
    
    if clicked:
        current_color = clicked_color
    else:
        current_color = released_color

    screen.fill(("gray5"))
    # Draw visually expanded/shrunk buttons
    options_img, options_rect = get_scaled_img_and_rect(options_img_orig, options_btn_drawPara)
    play_img, play_rect = get_scaled_img_and_rect(play_img_orig, play_btn_drawPara)
    quit_img, quit_rect = get_scaled_img_and_rect(quit_img_orig, quit_btn_drawPara)
    screen.blit(options_img, options_rect)
    screen.blit(play_img, play_rect)
    screen.blit(quit_img, quit_rect)
    pygame.display.update()

pygame.quit()