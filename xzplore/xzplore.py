import pygame
from pygame.sprite import Group
pygame.init()
import math
import random
import sys
import time

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 650
FPS = 120
BLACK  = (0,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),vsync=False)
pygame.mouse.set_visible(False)
Clock = pygame.time.Clock()

class World_pos():
    world_startX = SCREEN_WIDTH/2
    world_startY = SCREEN_HEIGHT/2

    dir_offset = 25

    offset_distance = 45

    def dis_calc(mouse_pos,spaceship):
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship[1])**2+(mouse_pos[0]-spaceship[0])**2))
        return mtos_dis

    x_offset = .1
    y_offset = .1

    def direction(angle,mouse_pos):
        if World_pos.dis_calc(mouse_pos,spaceship.position) > 50 :
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

class Crosshair():
    def __init__(self,size,color):
        self.center = (0,0)
        self.size = size
        self.color = color

    def update(self,mouse):
        self.center = (mouse[0],mouse[1])
       
    def draw(self): 
        pygame.draw.rect(screen,self.color,(self.center[0],self.center[1],3,3),self.size)

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
            self.acceleration +=0.01
        else:  
            self.acceleration -= 0.002
        
        if self.acceleration > self.max_speed:
            self.acceleration = self.max_speed
        elif self.acceleration < 0:
            self.acceleration = 0.0

    def update(self):
        screen.blit(self.surf,self.rect) 

class Space_station(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.surf = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(500,500))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.center = (self.x,self.y)
        self.angle = 0
        self.rot_surf = self.surf
        self.velocity = 0
        
    def update(self,angle):

        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship.position[1])**2+(mouse_pos[0]-spaceship.position[0])**2))
        if mtos_dis > World_pos.offset_distance:
            self.velocity = spaceship.acceleration  +0.4
        elif pygame.mouse.get_pressed()[0]:
            self.velocity = spaceship.acceleration  
        else:
            self.velocity = spaceship.acceleration  

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
        
        self.x += dx
        self.y +=dy
    
    def spin(self):
        self.angle +=1
        angle = math.radians(self.angle)
        self.rot_surf = pygame.transform.rotate(self.surf,angle)
        self.rect = self.rot_surf.get_rect(center=(self.x,self.y))

    def draw(self):
        screen.blit(self.rot_surf,self.rect)

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

class Star():

    def __init__(self,x,y,size,radius,transparency,layer,move):
        self.x = x 
        self.y = y
        self.pos = (self.x,self.y)
        self.surf = pygame.Surface((size,size),pygame.SRCALPHA)
        self.center = (size/2,size/2)
        self.circle_radius = radius
        self.glow_radius = radius + 2.5
        self.white = (225,225,225)
        self.white2 = (255,255,255)
        self.colors = [self.white,self.white2]
        self.color = self.white
        self.transparency = transparency
        self.layer = layer 
        self.move = move
        self.life_time = 0 


    def update(self,angle):
        dis = math.sqrt((pygame.mouse.get_pos()[1]-spaceship.position[1])**2 + (pygame.mouse.get_pos()[0] - spaceship.position[0])**2)
        if self.layer > 1:
            offset = self.layer + spaceship.acceleration
        else:
            offset = self.layer + .5
        #print(dis)

        if dis < World_pos.offset_distance:
            offset -=1

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
       
        offset = self.x,self.y
        self.pos = offset
        return self.pos

    def blink(self):
        self.life_time+=0.02
        transparency = round(50 * math.sin(self.life_time)+60) 
        return transparency

    def draw(self):
        screen.blit(self.surf,Star.update(self,World_pos.dir_offset))
        pygame.draw.circle(self.surf,((*self.white2,Star.blink(self))),(self.center),self.glow_radius)
        pygame.draw.circle(self.surf,self.color,(self.center),self.circle_radius)

    def reposition(self,xylimit,respawn_dis):
        if self.pos[0] > SCREEN_WIDTH + xylimit:
            self.x = -respawn_dis
        elif self.pos[0] < -xylimit :
            self.x = (SCREEN_WIDTH + respawn_dis)

        if self.pos[1] > SCREEN_HEIGHT + xylimit:
            self.y = -respawn_dis
        elif self.pos[1] < -xylimit :
            self.y = (SCREEN_HEIGHT + respawn_dis)

class Projectile():
    projectile_delay = 100
    def __init__(self,position,size,speed,spread,color,transparency):
        self.x = position[0] - size/2
        self.y = position[1] - size/2
        self.dir = Projectile.fire_projectile()
        self.surface = pygame.Surface((size,size),pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.position = position 
        self.center =  (size/2,size/2)
        self.speed = speed
        self.size = size
        self.spread = spread
        self.color = color 
        self.radius = size/2 - 11
        self.transparency = transparency
        
        
    def draw(self):
        self.position = (self.x,self.y)
        pygame.draw.circle(self.surface,(*self.color,self.transparency),self.center, (self.radius + 2.5))
        pygame.draw.circle(self.surface,(self.color),self.center,self.radius)
        screen.blit(self.surface,self.position)

    def fire_projectile():
        dx = pygame.mouse.get_pos()[0] - spaceship.position[0] 
        dy = pygame.mouse.get_pos()[1] - spaceship.position[1]
        dir = math.hypot(dx,dy)
        dx /= dir 
        dy /= dir
        return (dx,dy) 

    def update(self):
        self.x += (self.dir[0] + self.spread) * self.speed
        self.y += (self.dir[1] + self.spread) * self.speed


class Parasite():
    def __init__(self,x,y,image,size,speed):
        self.x = x
        self.y = y
        self.position = (self.x,self,y)
        self.image = image
        self.surface = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(size,size))
        self.rect = self.surface.get_rect()
        self.dir = (0,0)
        self.size = size
        self.speed = speed

    def update(self):
        dx = spaceship.position[0] - self.x + random.randint(-100,100)
        dy = spaceship.position[1] - self.y + random.randint(-100,100)
        dir = math.hypot(dx,dy)
        dx /= dir
        dy /= dir
        self.x += dx * self.speed/10 
        self.y += dy * self.speed/10 
        screen.blit(self.surface,(self.x,self.y))
  
        
        
'''
class Planet():
    def __init__(self,position,size,color,radius,transparency):
        self.position = position
        self.surf = pygame.Surface((size,size),pygame.SRCALPHA)
        self.color = color
        self.radius = radius
        self.transparency = transparency    
    
    def draw(self):
        pygame.draw.circle(self.surf,(*self.color,self.transparency),(planet_rec.center),self.radius)
        screen.blit(self.surf,self.position)


circle = Planet((0,0),1500,(0,223,135),720/2,20)
planet = pygame.transform.smoothscale(pygame.image.load("assets/desert_planet.png"),(50,50))
planet_rec = planet.get_rect(center=(400,400))
'''

crosshair = Crosshair(2,(170,0,0))
spaceship = Spaceship("assets/spaceship.png",SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
projectiles = []
space_station = Space_station("assets/spacestation.png",SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
smoke_particles = []
foreground_stars = []
background_stars = []
parasites = []

while True:

    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()
    
    #pygame.draw.rect(screen,(255,0,0),(250/2,250/2,SCREEN_WIDTH-250,SCREEN_HEIGHT-250),5)
    
    World_pos.dis_calc(mouse_pos,spaceship.rect.center)
    World_pos.x_offset,World_pos.y_offset = World_pos.direction(15,mouse_pos)
    
    if len(background_stars) < 150:
        background_stars.append(Star(random.randint(-25,SCREEN_WIDTH),random.randint(-25,SCREEN_HEIGHT),25,random.uniform(0,4),120,random.uniform(0.1,1),random.uniform(-.002,.002)))
    
    for star in background_stars:
        star.draw()
        star.reposition(random.randint(100,200),random.randint(10,95))

    
    #circle.draw()
    #screen.blit(planet,planet_rec)


    space_station.draw()
    space_station.update(World_pos.dir_offset)
    space_station.spin()

    smoke_particles.append(Rocket_smoke(spaceship.rect.center[0],spaceship.rect.center[1]))

    for particle in smoke_particles[:]:
        particle.draw()
        particle.update()
        particle.direction(World_pos.dir_offset,mouse_pos)
        if particle.size <=0 or particle.lifetime <= 0:
            smoke_particles.remove(particle)

    Projectile.projectile_delay +=1 

    if Projectile.projectile_delay > 30:
        if pygame.mouse.get_pressed()[2]:
            for i in range(2):
                projectiles.append(Projectile(spaceship.position,25,4,random.uniform(-.03,.03),(255,231,0),100))
            Projectile.projectile_delay = 0


    for projectile in projectiles:
        projectile.draw()
        projectile.update()
        if projectile.x > SCREEN_WIDTH +30 or projectile.x < -30:
            projectiles.remove(projectile)
        elif projectile.y > SCREEN_HEIGHT +30 or projectile.y < -30:
            projectiles.remove(projectile)


    spaceship.update()
    spaceship.point_towards(mouse_pos)
    spaceship.move(mouse_pos)

    if len(parasites) < 30:
        parasites.append(Parasite(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),"assets/parasite1.png",20,random.uniform(1,10)))
    
    for parasite in parasites:
        parasite.update()
        
    '''
    for projectile in projectiles:
        if pygame.Rect.colliderect(parasite.rect,projectile.rect):
            if parasite in parasites:
                parasites.remove(parasite)
            else:
                pass
    '''


    if len(foreground_stars) < 150:
        foreground_stars.append(Star(random.randint(-25,SCREEN_WIDTH),random.randint(-25,SCREEN_HEIGHT),25,random.uniform(0,4),120,random.uniform(5,15)/10,random.uniform(-.002,.002)))
        
    for star in foreground_stars:
        star.draw()
        star.reposition(random.randint(100,200),random.randint(10,90))

    crosshair.draw()
    crosshair.update(pygame.mouse.get_pos())


    Clock.tick(FPS)
    pygame.display.flip()
    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    quit_game()
