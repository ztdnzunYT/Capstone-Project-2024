import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Maze variables
cell_size = 20
rows = height // cell_size
cols = width // cell_size
maze = [[1 for _ in range(cols)] for _ in range(rows)]

# Player variables
player_x = 1
player_y = 1
player_size = cell_size // 2

# Generate a random maze
def generate_maze():
    # Start at the center of the maze
    start_x = rows // 2
    start_y = cols // 2
    stack = [(start_x, start_y)]

    while stack:
        current_x, current_y = stack[-1]

        # Check for unvisited neighbors
        unvisited_neighbors = []
        if current_x > 1 and maze[current_x - 2][current_y] == 1:
            unvisited_neighbors.append((current_x - 2, current_y))
        if current_x < rows - 2 and maze[current_x + 2][current_y] == 1:
            unvisited_neighbors.append((current_x + 2, current_y))
        if current_y > 1 and maze[current_x][current_y - 2] == 1:
            unvisited_neighbors.append((current_x, current_y - 2))
        if current_y < cols - 2 and maze[current_x][current_y + 2] == 1:
            unvisited_neighbors.append((current_x, current_y + 2))

        if unvisited_neighbors:
            # Choose a random neighbor
            next_x, next_y = random.choice(unvisited_neighbors)

            # Remove the walls between the current cell and the chosen neighbor
            maze[(current_x + next_x) // 2][(current_y + next_y) // 2] = 0
            maze[next_x][next_y] = 0

            # Push the chosen neighbor onto the stack
            stack.append((next_x, next_y))
        else:
            # Backtrack if no unvisited neighbors
            stack.pop()

# Draw the maze
def draw_maze():
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, black, (j * cell_size, i * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, white, (j * cell_size, i * cell_size, cell_size, cell_size))

# Draw the player
def draw_player():
    pygame.draw.circle(screen, red, (player_x * cell_size + cell_size // 2, player_y * cell_size + cell_size // 2), player_size)

# Game loop
running = True
generate_maze()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 1 and maze[player_y][player_x - 2] == 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and player_x < cols - 2 and maze[player_y][player_x + 2] == 0:
        player_x += 1
    if keys[pygame.K_UP] and player_y > 1 and maze[player_y - 2][player_x] == 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and player_y < rows - 2 and maze[player_y + 2][player_x] == 0:
        player_y += 1

    # Check for win condition (reaching the exit)
    if player_x == cols - 2 and player_y == rows - 2:
        print("You Win!")
        running = False

    # Clear the screen
    screen.fill(white)

    # Draw the game elements
    draw_maze()
    draw_player()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()