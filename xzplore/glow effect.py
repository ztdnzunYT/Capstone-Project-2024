import pygame
import sys
import math
import random
# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Glowing Circle Example')


class Circle():
    def __init__(self,x,y,size,color,circle_radius,transparency) :
        self.x = x
        self.y = y
        self.position = (x,y)
        self.surface = pygame.Surface((size,size),pygame.SRCALPHA)
        self.size = size
        self.center = (size/2,size/2)
        self.color = color 
        self.circle_radius = circle_radius
        self.glow_radius = circle_radius + 3
        self.transparency = transparency
        self.time = 0
        
    def float(self):
        self.time +=.01
        float_amount = 2* math.sin(2*math.pi + 1 *self.time) + 300
        return float_amount

    def twinkle(self):
        transparency = round(abs(120 * math.sin(.1 * self.time/2)))
        return transparency
        
    def draw(self):
        pygame.draw.circle(self.surface,(*self.color,Circle.twinkle(self)),self.center,self.glow_radius)
        pygame.draw.circle(self.surface,self.color,self.center,self.circle_radius)
        screen.blit(self.surface,(self.x,Circle.float(self)))
        self.x +=0.01

        


# Function to create a glowing circle surface
def create_glowing_circle():
    # Create a surface with per-pixel alpha
    size = 50
    surface = pygame.Surface((size,size), pygame.SRCALPHA)
    center = (size/2,size/2)
    alpha = int(20)
    pygame.draw.circle(surface, (*(255,255,255), alpha), center, 20)
    pygame.draw.circle(surface, (255,255,255), center, 5)
    return surface
    

# Define colors and parameters


particles = []
# Create glowing circle surface
glowing_circle = create_glowing_circle()
x= 0
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Fill the screen with black
    screen.fill((0, 0, 0))

    if len(particles) < 50:
        particles.append(Circle(random.randint(0,width),random.randint(0,height),random.randint(20,30),(255,255,255),5,50))

    for particle in particles:
        particle.draw()
        
    screen.blit(glowing_circle,(x,300))


    

    

    # Update the display
    pygame.display.flip()