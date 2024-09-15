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
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),vsync=False)

Clock = pygame.time.Clock()

class World_pos():
    world_startX = SCREEN_WIDTH/2
    world_startY = SCREEN_HEIGHT/2

    def dis_cal(mouse_pos,spaceship):
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship[1])**2+(mouse_pos[0]-spaceship[0])**2))
        return mtos_dis

    x_offset = .1
    y_offset = .1

    def direction(angle,mouse_pos):
        if World_pos.dis_cal(mouse_pos,spaceship.position) > 50 :
            if (mouse_pos[0] - spaceship.position[0]) > -angle:
                x = (spaceship.acceleration * -1)
            elif (mouse_pos[0] - spaceship.position[0]) < angle:
                x = spaceship.acceleration 
            else:
                x = .1
            if (mouse_pos[1] - spaceship.position[1]) > angle:
                y = (spaceship.acceleration *-1)
            elif (mouse_pos[1] - spaceship.position[1]) < -angle:
                y = spaceship.acceleration
            else:
                y = .1
        else:
            x = .1
            y = .1
        return (x,y)
            
class Spaceship(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(55,55))
        self.surf = self.image
        self.rect = self.surf.get_rect(center=(x,y))
        self.position = self.rect.center
        self.angle = 0
        self.max_speed = 1.5
        self.acceleration = 0
        self.speed = round(self.acceleration)
        self.dir = 0
    
    def point_towards(self,mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dx,dy))
        self.surf = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.surf.get_rect(center=(self.rect.center))

    def move(self,mouse_pos):
    
        dir = pygame.math.Vector2(mouse_pos) - self.position
        dis = math.sqrt((pygame.mouse.get_pos()[1] - spaceship.position[1])**2+(pygame.mouse.get_pos()[0] -spaceship.position[0])**2 )
        self.dir = dir
        
        if dir.length() > 60:
            dir = dir.normalize()
            self.position += dir * self.acceleration
            self.rect.center = self.position
        

        
        if pygame.mouse.get_pressed()[0]:
            self.acceleration +=0.02
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
        self.spread_amount = .15
        self.spread = (random.uniform(-self.spread_amount,self.spread_amount),random.uniform(-self.spread_amount,self.spread_amount))
        self.velocity = .03
        #print(spaceship.dir)
        
    def direction(self,angle,mouse_pos):

        if (mouse_pos[0] - spaceship.position[0]) > angle:
            dx = -self.velocity
        elif (mouse_pos[0] - spaceship.position[0]) < -angle:
            dx = self.velocity
        else:
            dx = 0
        if (mouse_pos[1] - spaceship.position[1]) > angle:
            dy = -self.velocity
        elif (mouse_pos[1] - spaceship.position[1]) < -angle:
            dy = self.velocity
        else:
            dy = 0
        self.spread = (self.spread[0]+dx,self.spread[1]+dy)

    def update(self):
        self.x += self.spread[0]
        self.y += self.spread[1]
        self.size -= random.uniform(.02,.04)
        self.lifetime -=.5
        if pygame.mouse.get_pressed()[0]:
            self.velocity = .03
            if self.lifetime >197:
                self.size = random.randint(3,7)
        else:
            self.velocity = .02
    
    def draw(self):
        if self.size > 0:
            if self.lifetime < 198:
                pygame.draw.circle(screen,self.colors,(self.x,self.y),self.size)

class Stars():
    def __init__(self,x,y,size,layer,move):
        self.x = x 
        self.y = y
        self.dx = 0
        self.dy = 0
        self.radius = size
        self.white = (255,255,255)
        self.white2 =(200,200,50)
        self.colors = [self.white,self.white2]
        self.color = self.white
        self.center = (self.x,self.y)
        self.layer = layer 
        self.move = move
        
       
    def update(self,angle):
        offset = (self.layer +spaceship.acceleration) 

        if (mouse_pos[0] - spaceship.position[0]) > angle:
            dx = -offset 
        elif (mouse_pos[0] - spaceship.position[0]) < -angle:
            dx = offset
        else:
            dx = self.move
        if (mouse_pos[1] - spaceship.position[1]) > angle:
            dy = -offset
        elif (mouse_pos[1] - spaceship.position[1]) < -angle:
            dy = offset
        else:
            dy = self.move

        self.x += dx 
        self.y += dy 
        self.dx = dx 
        self.dy = dy 

        offset = pygame.math.Vector2((self.x + self.dx),(self.y+ self.dy)) 
        offset.normalize()
        self.center = offset
        return self.center
 
    def draw(self):
        pygame.draw.circle(screen,self.color,(Stars.update(self,20)),self.radius)
    
    def reposition(self,xylimit,respawn_dis):
        if self.center[0] > SCREEN_WIDTH + xylimit:
            self.x = -respawn_dis
        elif self.center[0] < -xylimit :
            self.x = (SCREEN_WIDTH + respawn_dis)


        if self.center[1] > SCREEN_HEIGHT + xylimit:
            self.y = -respawn_dis
        elif self.center[1] < -xylimit :
            self.y = (SCREEN_HEIGHT + respawn_dis)


spaceship = Spaceship("xzplore/assets/spaceship.png",SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
particles = []
stars = []

while True:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    

    #pygame.draw.rect(screen,(255,0,0),(250/2,250/2,SCREEN_WIDTH-250,SCREEN_HEIGHT-250),5)

    World_pos.dis_cal(mouse_pos,spaceship.rect.center)
    World_pos.x_offset,World_pos.y_offset = World_pos.direction(15,mouse_pos)
    
    if len(stars) < 150:
        stars.append(Stars(random.randint(50,SCREEN_WIDTH),random.randint(50,SCREEN_HEIGHT),random.uniform(0,5),random.uniform(0.1,15)/10,random.uniform(-.002,.002)),)
    
    for star in stars:
        star.draw()
        star.reposition(random.randint(100,200),random.randint(50,90))

    particles.append(Rocket_smoke(spaceship.rect.center[0],spaceship.rect.center[1]))
    for particle in particles[:]:
        particle.draw()
        particle.update()
        particle.direction(25,mouse_pos)
        if particle.size <=0 or particle.lifetime <= 0:
            particles.remove(particle)

    spaceship.update()
    spaceship.point_towards(mouse_pos)
    spaceship.move(mouse_pos)
    
    Clock.tick(FPS)
    pygame.display.flip()
    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    quit_game()

