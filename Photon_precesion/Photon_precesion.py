import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Photon Precesion")

Game_state = "Main_menu"

class Main_menu():
    
    class Buttons():
        def __init__(self,x,y,width,length,text):
            self.x = x 
            self.y = y 
            self.width = width 
            self.length = length 
            self.transparency = 255
            self.rect = (self.x,self.y,self.width,self.length)
            self.font = pygame.font.Font(None,30)
            self.text = text 
            self.font_render = self.font.render(self.text,True,(255,255,255))
            self.font_rect = self.font_render.get_rect()

    practice_button = Buttons(40,40,170,40,"Practice")
    versus_button = Buttons(40,110,170,40,"Versus")
    buttons = []


    def display_main_menu():
        surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        pygame.draw.rect(surface,(255,255,255,Main_menu.practice_button.transparency),Main_menu.practice_button.rect,1)
        screen.blit(Main_menu.practice_button.font_render,(50,50))


        pygame.draw.rect(surface,(255,255,255,Main_menu.versus_button.transparency),Main_menu.versus_button.rect,1)
        screen.blit(Main_menu.versus_button.font_render,(50,120))
        
        screen.blit(surface,(0,0))











# Set up the main loop
running = True
while running:
    screen.fill((0,0,0))

    Main_menu.display_main_menu()

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
