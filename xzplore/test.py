import pygame
import sys
import os 
import pathlib
import numpy as np

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Color Collision Example")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)




class Tile():

    world_x = 0 
    world_y = 0 

    tile_map = np.array([
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        ])


    TILE_SIZE = 200    
    def __init__(self,image):
        self.tile_size = Tile.TILE_SIZE
        self.image = os.path.join("assets",image)
        self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(self.tile_size,self.tile_size))
        self.rect = self.surf.get_rect(topleft=(0,0))

orange_tile = Tile("orange_planet_tile.png")
player_speed = .5

running = True
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    # Clear the screen

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Tile.world_x +=player_speed
    if keys[pygame.K_d]:
        Tile.world_x -=player_speed
    if keys[pygame.K_w]:
        Tile.world_y +=player_speed
    if keys[pygame.K_s]:
        Tile.world_y -=player_speed
    
    if keys[pygame.K_LSHIFT]:
        player_speed = 1
    else:
        player_speed =.5


    for _,col in enumerate(Tile.tile_map):
        for row in range(len(col)):
            x,y = (row*Tile.TILE_SIZE)+Tile.world_x,(_*Tile.TILE_SIZE)+Tile.world_y
            screen.blit(orange_tile.surf,(x,y))

    pygame.draw.rect(screen,(0,0,0),(350,300,20,20))
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
