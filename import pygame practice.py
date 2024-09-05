import pygame 
from pygame.locals import *

pygame.init()
# Form screen with 400x400 size 
# and with resizable 
screen = pygame.display.set_mode((600, 600))

color = (255,0,0)

screen.fill(color)
pygame.display.flip()

pygame.draw.rect(screen, (0, 0, 255), [100, 100, 400, 100], 0)
pygame.display.update()
  
# set title 
pygame.display.set_caption('WHOOOOOOOO') 
  
# run window 
running = True
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
  
# quit pygame after closing window 
pygame.quit() 