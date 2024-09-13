import pygame
from pygame.sprite import Group
pygame.init()
import math
import random
import sys

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 650
FPS = 120
BLACK  = (0,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),vsync=True)
Clock = pygame.time.Clock()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(50,50))
        self.surf = self.image
        self.rect = self.surf.get_rect(midright=(x,y))
        self.position = self.rect.center
        self.speed = 1

    def point_towards(self,mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dx,dy))
        self.surf = pygame.transform.rotate(self.image,angle)
        self.rect = self.surf.get_rect(center=(self.rect.center))

    def move(self,mouse_pos):
        dir = pygame.math.Vector2(mouse_pos) - self.position
        if dir.length() > 50:
            dir = dir.normalize()
            self.position += dir * self.speed
            self.rect.center = self.position

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.speed = 2
                else:
                    self.speed = 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.speed = 1

    def update(self):
        screen.blit(self.surf,self.rect) 

class Particles():
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.color = (255,255,255)
        self.size = (random.randint(1,4))
        self.lifetime = 200
        self.velocity = (random.uniform(-.1,.1),random.uniform(-.1,.1))
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.size -=.005
        self.lifetime -=.5

    def draw(self):
        if self.size > 0:
            pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
    
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

spaceship = Spaceship("assets/spaceship-3.png (2).png",SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
particles = []

while True:
    screen.fill(BLACK)

    particles.append(Particles(spaceship.rect.centerx+.5,spaceship.rect.centery+.5))
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if  particle.lifetime <=0:
            particles.remove(particle)
    mouse_pos = pygame.mouse.get_pos()
    spaceship.update()
    spaceship.point_towards(mouse_pos)
    spaceship.move(mouse_pos)

    pygame.display.flip()
    Clock.tick(FPS)
    quit_game()

