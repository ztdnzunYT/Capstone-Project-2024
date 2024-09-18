import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Pygame Window")

# Set a color
background_color = (255, 255, 255)  # White

val1 = 0 
val2 = 0 
val3 = 0
x = 0 
y = 0
radius = 50 + math.pi **2
size  = 15



class Particle():
    def __init__(self,x,y,speed,size):
        self.x = x 
        self.y = y 
        self.positon = (x,y)
        self.x_max = self.x *-1
        self.speed = speed
        self.color1 = (255, 253, 208)
        self.color2 = (211, 211, 211)
        self.colors = [self.color1,self.color2]
        self.color = random.choice(self.colors)
        self.size = size
        print()

    def draw(self):
        pygame.draw.circle(window,self.color,(self.x+300,self.y+300),self.size)

    def update(self):
        self.x += self.speed
        if self.x > self.x_max:
            self.x = self.positon[0]    

        self.y += z  

particles = []

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    window.fill((0,0,0))


    val1 +=10
    val2 +=10
    val3 +=0.02

    x = radius * math.sin(val1)
    y = radius * math.cos(val2)
    up = math.sin(val1)

    z = 10 * math.sin(val3)/1.1
    print(round(x),round(y))
    #pygame.draw.circle(window,(255,255,255),(300,300),110,1)
    #pygame.draw.circle(window,(255,0,0),(x+300,y+300),size)
    #pygame.draw.circle(window,(0,0,255),(x+300,300),size)
    pygame.draw.circle(window,(0,255,0),(300,z+300),size)
    

    
    if len(particles) < 12000:
        if x < 0:
            particles.append(Particle(x ,y,1,random.uniform(1,1)))

    for part in particles:
        part.draw()
        part.update()
       
 


    # Fill the background
    

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
