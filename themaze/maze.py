import pygame
from pygame.locals import *


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Game')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player:
    def __init__(self):
        self.x, self.y = 50, 50
        self.speed = 5

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 20, 20))


class Maze:
    def __init__(self):
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def draw(self, screen):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, WHITE, (x * 40, y * 40, 40, 40))


def main():
    clock = pygame.time.Clock()
    player = Player()
    maze = Maze()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.move(-1, 0)
        if keys[K_RIGHT]:
            player.move(1, 0)
        if keys[K_UP]:
            player.move(0, -1)
        if keys[K_DOWN]:
            player.move(0, 1)

        screen.fill(BLACK)
        maze.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

