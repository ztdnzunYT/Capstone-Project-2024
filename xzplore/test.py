import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Transparent Image Example')

# Load the image
image = pygame.image.load('assets/grid.png')  # Replace with your PNG file path
image.set_alpha(0)
newimg = pygame.transform.smoothscale(image,(500,500))
  # Make white (255, 255, 255) transparent

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the background with a color (e.g., blue)
    window.fill((0, 0, 255))

    # Draw the image at (100, 100)
    window.blit(newimg, (100, 100))

    # Update the display
    pygame.display.flip()
