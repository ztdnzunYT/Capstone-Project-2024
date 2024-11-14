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
        pass


    def display_main_menu():
        pass




















# Set up the main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill((255, 255, 255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
