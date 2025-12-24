import pygame
import math
import random
import sys
import os 
from pathlib import Path

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Set up the display
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Pygame Window")

# Set a color
background_color = (255, 255, 255)  # White

time = 0 
val2 = 0 
val3 = 0
x = 0 
y = 0
radius = 150 + math.pi **2
size  = 15



class Particle():
    def __init__(self,x,y,speed,size):
        self.x = x 
        self.y = y 
        self.positon = (x,y)
        self.x_max = self.x *-1
        self.x_min = x
        self.speed = speed
        self.bg_speed = speed - speed/2
        self.color1 = (93, 63, 211)
        self.color2 = (207, 159, 255)
        self.color3 = (145, 95, 109)
        self.colors = [self.color1,self.color2,self.color3]
        self.color = random.choice(self.colors)
        self.size = size
        self.life_time = 0
        self.direction = 0
        

    def draw(self):
        pygame.draw.circle(window,self.color,(self.x+width/2,self.y+height/2),self.size)

    def update(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.size+=0.5
        #else:
            #if self.size >2:
                #self.size -=0.1
        
        if self.direction == 0:
            self.color = (160, 130, 170)
            self.x += self.speed
        elif self.direction == -1:
            self.color = (255, 95, 109)
            self.x -= self.bg_speed
            if self.x < self.x_min:
                self.direction = 0
        
        if self.x == self.x_max:
            particles.insert(len(particles)-1,part)
            
        if self.x > self.x_max:
            
            #self.x = self.positon[0] 
            self.direction = -1

        self.life_time += 0.05
        self.y += .1 * math.sin(self.life_time)
        

particles = []
'''
for path in (Path('C:/').rglob("assets/desert_planet.png")):
    fp = path


surf = pygame.transform.smoothscale(pygame.image.load(fp).convert_alpha(),(300,300))
rect = surf.get_rect(center=(width/2,height/2))
'''

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Quit Pygame
            pygame.quit()
            sys.exit()

    
    window.fill((0,0,0))

    time +=1
    val3 += 0.01

    x = radius * math.sin(time)
    y = radius * math.cos(time)
    up = 30 * math.sin(val3)

    #print(round(x),round(y))
    #pygame.draw.circle(window,(255,255,255),(300,300),60,1)
    #pygame.draw.circle(window,(255,0,0),(x+300,y+300),size)
    #pygame.draw.circle(window,(0,0,255),(x+300,300),size)
    #pygame.draw.circle(window,(0,255,0),(300,up+300),15)
    
    
    #print( (pygame.mouse.get_pos()[0] - width/2)/100 , (pygame.mouse.get_pos()[1] - height/3 )/100)
    
    

    if len(particles) < 5000:
        if x < 0:
            particles.append(Particle(x ,y,random.uniform(0,.3),random.uniform(1,2)))

    for part in particles:
        part.draw()
        part.update()

    # Fill the background
    

    # Update the display
    pygame.display.flip()
    clock.tick(120)

