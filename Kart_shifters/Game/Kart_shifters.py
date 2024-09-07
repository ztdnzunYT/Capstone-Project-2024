import pygame
import math
import os
import pygame.ftfont

#-----------------
#NOTE THIS IS THE FILE FOR THE MAC VERSION OF THE APPLICATION 


clock = pygame.time.Clock()
pygame.display.set_caption("Kart Shifters")
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY  = (150,150,150)
TARGET_FPS = 80 
SW = 800
SH = 600
screen = pygame.display.set_mode((SW,SH))

class Kart(pygame.sprite.Sprite):
    def __init__(self,rotation_val):
        super(Kart,self).__init__()
        self.abs_path = os.path.abspath("Kart_shifters/Assets/Kart.png")
        self.image = pygame.transform.smoothscale(pygame.image.load(self.abs_path).convert_alpha(),(100,100))
        self.surf = self.image 
        self.layers =  None
        self.angle = 0
        self.surf = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.surf.get_rect(center=(self.surf.get_width()/2,self.surf.get_height()/2))
        self.rect.center = (SW/2,SH/2)
        self.max_rotation_val = 3
        self.rotation_val = rotation_val
        self.drift_value = self.angle
        self.velocity = 0.5
        self.max_velocity = 6
        self.acceleration = 0.008
        
    def rotate(self,left=False,right=False):   
        if kart1.velocity > 0.6:
            if left: 
                self.angle += self.rotation_val
            if right:
                self.angle += -self.rotation_val

        if keys[pygame.K_LSHIFT] == False:
            if keys[pygame.K_a]:
                if self.drift_value > self.angle:
                    self.drift_value -=1

        if keys[pygame.K_LSHIFT] == False: 
            
            if self.drift_value + self.angle > self.angle:
                self.drift_value -=5

            if right:
                self.surf = pygame.transform.rotate(self.image,self.angle - self.drift_value)
                self.rect = self.surf.get_rect(center=(self.rect.center))
                self.angle = self.angle % 360
            if left:
                self.surf = pygame.transform.rotate(self.image,self.angle - -self.drift_value)
                self.rect = self.surf.get_rect(center=(self.rect.center))
                self.angle = self.angle % 360
        else:
            if self.drift_value <=50:
                self.drift_value +=1
            if self.velocity > 0.5:
                if right == False and left: 
                    self.surf = pygame.transform.rotate(self.image,self.angle + self.drift_value)
                    self.rect = self.surf.get_rect(center=(self.rect.center))
                    self.angle = self.angle % 360
                if left == False and right:
                    self.surf = pygame.transform.rotate(self.image,self.angle + -self.drift_value)
                    self.rect = self.surf.get_rect(center=(self.rect.center))
                    self.angle = self.angle % 360

                if left and right:
                    self.surf = pygame.transform.rotate(self.image,self.angle )
                    self.rect = self.surf.get_rect(center=(self.rect.center))
                self.angle = self.angle % 360

    def move_foward(self):
        self.velocity = min((self.velocity + self.acceleration),self.max_velocity)
        self.turn(foward=True)
    
    def brake(self):
        if self.velocity > 1:
            self.velocity -=0.02
        
    def turn(self,foward=False,backward=False):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity 
        horizontal = math.sin(radians) * self.velocity
        if foward: 
            self.rect.x -= horizontal
            self.rect.y -= vertical 
           
kart1 = Kart(3)  #sprite 

run = True
while run:
    screen.fill(GREY)
    clock.tick(TARGET_FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        kart1.move_foward()
    elif keys[pygame.K_w] == False:
        if kart1.velocity >= 0.5:
            kart1.move_foward()
            kart1.velocity -= 0.02
    if keys[pygame.K_s]:
        kart1.brake()
    if keys[pygame.K_a]:
        kart1.rotate(left=True) 
    if keys[pygame.K_d]:
        kart1.rotate(right=True)
        
    if keys[pygame.K_LSHIFT]:
        kart1.rotation_val = 1.5
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if kart1.velocity > .5:
                kart1.velocity -=0.015
    else:
        kart1.rotation_val = 3
    

    

    screen.blit(kart1.surf,kart1.rect)




    pygame.display.flip()





pygame.quit()
