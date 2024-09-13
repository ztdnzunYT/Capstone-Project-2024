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
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(55,55))
        self.surf = self.image
        self.rect = self.surf.get_rect(midright=(x,y))
        self.position = self.rect.center
        self.speed = 1
        self.angle = 0
        self.max_speed = 2
        self.acceleration = 0
        self.dir = 0
    
    def point_towards(self,mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dx,dy))
        self.surf = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.surf.get_rect(center=(self.rect.center))

    def move(self,mouse_pos):
        dir = pygame.math.Vector2(mouse_pos) - self.position
        self.dir = dir
        if dir.length() > 50:
            dir = dir.normalize()
            self.position += dir * self.acceleration
            self.rect.center = self.position
        
        if pygame.mouse.get_pressed()[0]:
            self.acceleration +=0.01
        else:  
            self.acceleration -= 0.002
        
        if self.acceleration > self.max_speed:
            self.acceleration = self.max_speed
        elif self.acceleration < 0:
            self.acceleration = 0.05

    def update(self):
        screen.blit(self.surf,self.rect) 

class Rocket_smoke():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.white = (255,255,255)
        self.white2 = (220,220,220)
        self.colors = random.choice([self.white,self.white2])
        self.size = (random.randint(1,4))
        self.lifetime = 200
        self.velocity = (random.uniform(-.1,.1),random.uniform(-.1,.1))
        #print(spaceship.dir)
        
 

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos[0] - spaceship.position[0]) > 0:
            dx = -.01
        elif (mouse_pos[0] - spaceship.position[0]) < 0:
            dx = .01
        if (mouse_pos[1] - spaceship.position[1]) > 0:
            dy = -.01
        elif (mouse_pos[1] - spaceship.position[1]) < 0:
            dy = .01

        self.velocity = (self.velocity[0]+dx,self.velocity[1]+dy)



        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.size -=.01
        self.lifetime -=.5
        if pygame.mouse.get_pressed()[0]:
            if self.lifetime > 190:
                self.size = random.randint(4,6)
    
    def draw(self):
        if self.size > 0:
            if self.lifetime < 195:
                pygame.draw.circle(screen,self.colors,(self.x,self.y),self.size)

spaceship = Spaceship("assets\spaceship.png",SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
particles = []


while True:
    
    screen.fill(BLACK)

    particles.append(Rocket_smoke(spaceship.rect.centerx+.5,spaceship.rect.centery+.5))

    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.size <=0 or particle.lifetime <= 0:
            particles.remove(particle)

    mouse_pos = pygame.mouse.get_pos()
    spaceship.update()
    spaceship.point_towards(mouse_pos)
    spaceship.move(mouse_pos)
    

    pygame.display.flip()
    Clock.tick(FPS)

    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    quit_game()

