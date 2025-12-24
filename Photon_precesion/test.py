import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Angle to Mouse Pointer")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Point coordinates
point_x, point_y = 300, 200  # Center point

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle to the mouse pointer
    dx = mouse_x - point_x
    dy = mouse_y - point_y
    angle = math.degrees(math.atan2(-dy, dx))  # Invert dy because Pygame's Y-axis is flipped

    # Clear the screen
    screen.fill(WHITE)

    # Draw the point
    pygame.draw.circle(screen, RED, (point_x, point_y), 5)

    # Draw a line pointing to the mouse
    line_length = 50
    end_x = point_x + line_length * math.cos(math.radians(angle))
    end_y = point_y - line_length * math.sin(math.radians(angle))  # Invert for correct direction
    pygame.draw.line(screen, BLUE, (point_x, point_y), (end_x, end_y), 2)

    # Display the angle (optional)
    font = pygame.font.Font(None, 36)
    angle_text = font.render(f"Angle: {int(angle)}°", True, BLUE)
    screen.blit(angle_text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
