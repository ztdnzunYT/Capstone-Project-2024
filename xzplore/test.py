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


class Tile():
    def __init__(self,image,x,y,size):
        self.image = os.path.join("assets",image)
        self.surf = pygame.image.load(self.image).convert_alpha()
        self.rect = self.surf.get_rect()

orange_tile = Tile("orange_planet_tile.png",0,0,32)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)
    screen.blit(orange_tile.surf,(255,255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
