#Mike McCue


import pygame as pg
import sys
import random

screenW = 600
screenH = 400
black = (0, 0, 0)
red = (255,0,0)

white = (255,255,255)


screen = pg.display.set_mode((screenW,screenH))


while True:
    screen.fill(white)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass

        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                pass


    pg.draw.rect(screen, red, (10,10,50,50),2)

    pg.display.update()
