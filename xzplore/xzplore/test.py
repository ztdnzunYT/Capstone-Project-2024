import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Surface Collision Example")

# Define rectangles
rect1 = pygame.Rect(100, 100, 50, 50)  # Blue rectangle
rect2 = pygame.Rect(400, 300, 50, 50)  # Red rectangle

# Speed
speed = 5

# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement controls for rect1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect1.x -= speed
    if keys[pygame.K_RIGHT]:
        rect1.x += speed
    if keys[pygame.K_UP]:
        rect1.y -= speed
    if keys[pygame.K_DOWN]:
        rect1.y += speed

    # Collision detection
    if rect1.colliderect(rect2):
        print("Collision detected!")

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the rectangles
    pygame.draw.rect(screen, BLUE, rect1)
    pygame.draw.rect(screen, RED, rect2)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)
