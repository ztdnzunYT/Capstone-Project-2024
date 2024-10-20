import pygame
import sys
import os 
import pathlib
import numpy as np
import random
# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Color Collision Example")
pygame.mouse.set_visible(False)
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

class Item_display():
    def __init__(self):
        self.item = None
        self.item_description = None
        self.surface = pygame.Surface((200,400),pygame.SRCALPHA)
        self.surf_rect = self.surface.get_rect(topright=(SCREEN_WIDTH-10,10))
        self.image = None
        self.rect = None
        self.font = pygame.font.Font(None,18)
        self.text = None
        self.text_rect = None
        self.window_radius = 5

    
    def draw_item_display_window(self):
        
        try:
            image,description = Item_display.find_item(self)
            screen.blit(self.surface,self.surf_rect)
            pygame.draw.rect(self.surface,(0,0,0,150),(30,0,170,250),0,self.window_radius)
            pygame.draw.rect(self.surface,(0,0,0),(30,0,170,250),4,self.window_radius)
            pygame.draw.rect(self.surface,(0,0,0),(30,0,170,150),3,0,self.window_radius,self.window_radius)
            self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(150,150))
            self.rect = self.image.get_rect()
            screen.blit(self.image,(SCREEN_WIDTH-165,11))
            split_text = description.split()
            text_len = 0
            text_height = 0
            self.text = self.font.render("Info:",True,(255,255,255))
            self.text_rect = self.text.get_rect(topleft=(SCREEN_WIDTH-165+text_len,170+text_height))
            screen.blit(self.text,self.text_rect)
            text_height = 20
            for text in split_text:
                self.text = self.font.render(text,True,(255,255,255))
                self.text_rect = self.text.get_rect(topleft=(SCREEN_WIDTH-165+text_len,170+text_height))
                width = self.text.get_width()
                text_len += width + 5
                if self.text_rect.x > 1090:
                    text_len = 0
                    text_height += 15
                screen.blit(self.text,self.text_rect)
            
                

        except:
            pass
        
    def find_item(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1], 1, 1)
        for item in items:
            if pygame.Rect.colliderect(item.rect,mouse_rect):
                return item.image,item.item_description
                
            

class Item():
    def __init__(self,item,item_description,color,image) -> None:
        self.pos = random.randint(200,800)
        self.item = item
        self.item_description = item_description
        self.color = color
        self.rect = None
        self.image = image


    def draw(self):
        self.rect = pygame.rect.Rect((self.pos+Tile.world_x,self.pos+Tile.world_y,20,20))
        pygame.draw.rect(screen,self.color,(self.rect))
        




orange_tile = Tile("orange_planet_tile.png")
player_speed = .5

item_display_window = Item_display()

Rock = Item("Rock","Naturally occurring solid made up of minerals or mineral-like substances",(198, 126, 39),"assets/orange_rock.png")
Fossil = Item("Fossil","Skeletal remains of a once living organism",(255, 228, 196),"assets/fossil-5.png")

items = [Rock,Fossil]

player_crosshair = pygame.transform.smoothscale(pygame.image.load("assets/player_crosshair.png").convert_alpha(),(40,40))
player_crosshair_rect = player_crosshair.get_rect()

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


    for index,col in enumerate(Tile.tile_map):
        for row in range(len(col)):
            x,y = (row*Tile.TILE_SIZE)+Tile.world_x,(index*Tile.TILE_SIZE)+Tile.world_y
            screen.blit(orange_tile.surf,(x,y))

    pygame.draw.rect(screen,(85,85,95),(1200/2-10,800/2-10,20,20),0,2)

    Rock.draw()
    Fossil.draw()

    item_display_window.draw_item_display_window()
    
    

    screen.blit(player_crosshair,(pygame.mouse.get_pos()[0]-20,pygame.mouse.get_pos()[1]-20))



    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
