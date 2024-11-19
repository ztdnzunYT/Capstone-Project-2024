import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 30
MAZE_WIDTH = 20
MAZE_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * MAZE_WIDTH
WINDOW_HEIGHT = CELL_SIZE * MAZE_HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Game")

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

class MazeGame:
    def __init__(self):
        self.maze = [[Cell(x, y) for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]
        self.player_pos = [0, 0]
        self.exit_pos = [MAZE_WIDTH-1, MAZE_HEIGHT-1]
        self.generate_maze()

    def generate_maze(self):
        # Generate maze using Depth-First Search
        def get_neighbors(x, y):
            neighbors = []
            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # top, right, bottom, left
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and 
                    not self.maze[new_y][new_x].visited):
                    neighbors.append((new_x, new_y))
            return neighbors

        stack = [(0, 0)]
        self.maze[0][0].visited = True

        while stack:
            current_x, current_y = stack[-1]
            neighbors = get_neighbors(current_x, current_y)

            if not neighbors:
                stack.pop()
                continue

            next_x, next_y = random.choice(neighbors)
            
            # Remove walls between current and next cell
            if next_x > current_x:  # Remove right wall
                self.maze[current_y][current_x].walls["right"] = False
                self.maze[next_y][next_x].walls["left"] = False
            elif next_x < current_x:  # Remove left wall
                self.maze[current_y][current_x].walls["left"] = False
                self.maze[next_y][next_x].walls["right"] = False
            elif next_y > current_y:  # Remove bottom wall
                self.maze[current_y][current_x].walls["bottom"] = False
                self.maze[next_y][next_x].walls["top"] = False
            elif next_y < current_y:  # Remove top wall
                self.maze[current_y][current_x].walls["top"] = False
                self.maze[next_y][next_x].walls["bottom"] = False

            self.maze[next_y][next_x].visited = True
            stack.append((next_x, next_y))

    def draw(self):
        screen.fill(WHITE)

        # Draw maze
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell = self.maze[y][x]
                cell_x = x * CELL_SIZE
                cell_y = y * CELL_SIZE

                if cell.walls["top"]:
                    pygame.draw.line(screen, BLACK, (cell_x, cell_y),
                                   (cell_x + CELL_SIZE, cell_y))
                if cell.walls["right"]:
                    pygame.draw.line(screen, BLACK, (cell_x + CELL_SIZE, cell_y),
                                   (cell_x + CELL_SIZE, cell_y + CELL_SIZE))
                if cell.walls["bottom"]:
                    pygame.draw.line(screen, BLACK, (cell_x, cell_y + CELL_SIZE),
                                   (cell_x + CELL_SIZE, cell_y + CELL_SIZE))
                if cell.walls["left"]:
                    pygame.draw.line(screen, BLACK, (cell_x, cell_y),
                                   (cell_x, cell_y + CELL_SIZE))

        # Draw player
        player_x = self.player_pos[0] * CELL_SIZE + CELL_SIZE // 2
        player_y = self.player_pos[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, BLUE, (player_x, player_y), CELL_SIZE // 3)

        # Draw exit
        exit_x = self.exit_pos[0] * CELL_SIZE + CELL_SIZE // 2
        exit_y = self.exit_pos[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, GREEN, (exit_x, exit_y), CELL_SIZE // 3)

        pygame.display.flip()

    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            current_cell = self.maze[self.player_pos[1]][self.player_pos[0]]
            
            if dx == 1 and not current_cell.walls["right"]:
                self.player_pos[0] = new_x
            elif dx == -1 and not current_cell.walls["left"]:
                self.player_pos[0] = new_x
            elif dy == 1 and not current_cell.walls["bottom"]:
                self.player_pos[1] = new_y
            elif dy == -1 and not current_cell.walls["top"]:
                self.player_pos[1] = new_y

    def check_win(self):
        return self.player_pos == self.exit_pos

def main():
    game = MazeGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(1, 0)
                elif event.key == pygame.K_UP:
                    game.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    game.move_player(0, 1)
                elif event.key == pygame.K_r:  # Reset game
                    game = MazeGame()

        game.draw()

        if game.check_win():
            font = pygame.font.Font(None, 74)
            text = font.render('You Win!', True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            game = MazeGame()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
