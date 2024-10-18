import pygame
import sys
import os 
import pathlib

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Color Collision Example")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


TILE_SIZE = 70 
tile_map = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    ]

class Tile():
    def __init__(self,image,x,y,size):
        self.image = os.path.join("assets",image)
        self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(size,size))
        self.rect = self.surf.get_rect(topleft=(x,y))




orange_tile = Tile("orange_planet_tile.png",0,0,TILE_SIZE)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen

    screen.fill((0,0,0))
    screen.blit(orange_tile.surf,(0,0))

    

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
