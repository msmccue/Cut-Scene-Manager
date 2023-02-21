#Mike McCue
#continuous movement with keys

import pygame as pg
import sys

screenW = 600
screenH = 400

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

gravity = 0;
xLoc = 180;
yLoc = 160
xDir = 0


screen = pg.display.set_mode((screenW,screenH))
timer = 0

while True:
    screen.fill(white)

    timer = timer + 0.00001
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if (yLoc > 0):
                    gravity = gravity - 0.2 #here
            if event.key == pg.K_RIGHT:
                xDir = 0.07
               
            if event.key == pg.K_LEFT:
                xDir = -0.07
              
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                pass
            if event.key == pg.K_RIGHT:
                xDir = 0
            if event.key == pg.K_LEFT:
                xDir = 0
    xLoc = xLoc + xDir
    pg.draw.rect(screen, blue, (xLoc,yLoc,40,40), 2)
    gravity = gravity + 0.0001 #here
    if (yLoc + gravity < 360 and yLoc > 0):
        yLoc = yLoc + gravity
    else:
        yLoc = 360
        gravity = 0
    pg.display.update()
