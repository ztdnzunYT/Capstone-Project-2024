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

time = 0 
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
        self.color1 = (128, 0, 0)
        self.color2 = (255, 69, 0)
        self.color3 = (47, 79, 79)
        self.colors = [self.color1,self.color2,self.color3]
        self.color = random.choice(self.colors)
        self.size = size
        self.life_time = 0


    def draw(self):
        pygame.draw.circle(window,self.color,(self.x+300,self.y+300),self.size)

    def update(self):
        self.x += self.speed
        if self.x > self.x_max:
            self.x = self.positon[0] 
        
        self.life_time += 0.1
        self.y += .2 *  math.sin(2*math.pi+self.life_time)

        


particles = []

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    window.fill((0,0,0))


    time +=1
    val3 += 0.5

    x = radius * math.sin(time)
    y = radius * math.cos(time)
    up = math.sin(time)

    #print(round(x),round(y))
    #pygame.draw.circle(window,(255,255,255),(300,300),60,1)
    #pygame.draw.circle(window,(255,0,0),(x+300,y+300),size)
    #pygame.draw.circle(window,(0,0,255),(x+300,300),size)
    #pygame.draw.circle(window,(0,255,0),(300,z+300),size)
    

    
    if len(particles) < 6000:
        if x < 0:
            particles.append(Particle(x ,y,random.uniform(1,2),random.uniform(1,2.5)))

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
