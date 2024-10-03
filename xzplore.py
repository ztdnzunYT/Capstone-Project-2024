import pygame
from pygame.sprite import Group
pygame.init()
import math
import random
import sys
import time
import os 

SCREEN_WIDTH = 1200#950
SCREEN_HEIGHT = 800 #650
FPS = 120
BLACK  = (0,0,0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),vsync=False)
pygame.mouse.set_visible(False)
Clock = pygame.time.Clock()
Game_State = "Space"

class Sounds():
    lazer = pygame.mixer.Sound(os.path.join("sounds","laser-gun.mp3"))
    boom = pygame.mixer.Sound(os.path.join("sounds","boom.mp3"))

class World_pos():
    world_startX = SCREEN_WIDTH/2
    world_startY = SCREEN_HEIGHT/2

    dir_offset = 25
    offset_distance = 45
    movement_amount = 60
    parasite1amount = 20

    def dis_calc(mouse_pos,spaceship):
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship[1])**2+(mouse_pos[0]-spaceship[0])**2))
        return mtos_dis

    def direction(spaceship,angle):
    
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship.position[1])**2+(mouse_pos[0]-spaceship.position[0])**2))
        if mtos_dis > World_pos.offset_distance:
            offset = spaceship.acceleration  +0.4
        elif pygame.mouse.get_pressed()[0]:
           offset = spaceship.acceleration  
        else:
            offset = spaceship.acceleration  

        if (mouse_pos[0] - spaceship.position[0]) > angle:
            dx = -offset
        elif (mouse_pos[0] - spaceship.position[0]) < -angle:
            dx = offset
        else:
            dx = 0
        if (mouse_pos[1] - spaceship.position[1]) > angle:
            dy = -offset
        elif (mouse_pos[1] - spaceship.position[1]) < -angle:
            dy = offset
        else:
            dy = 0

        return (dx,dy)

class Crosshair():
    def __init__(self,x,y,size,image):
        self.x = x
        self.y = y 
        self.size = size
        self.surface = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        self.surface.set_alpha(0)
        self.original_image = image
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(self.size,self.size))
        self.rect = self.image.get_rect(center=(self.size/2,self.size/2))
        self.angle = 0 
        self.rotation_amount = 0
        self.rotated_image = pygame.transform.rotate(self.image,self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=(self.size/2,self.size/2))
    
    def update(self,mouse):
        self.x = mouse[0]
        self.y = mouse[1]
        self.rect.center = (mouse[0],mouse[1])
        self.image = pygame.transform.smoothscale(pygame.image.load(self.original_image).convert_alpha(),(self.size,self.size))
    
    def rotate(self):
        if (pygame.mouse.get_pressed()[2]):
            self.angle = (self.angle - self.rotation_amount) % 360
            self.rotation_amount +=0.3
            self.rotation_amount = min(self.rotation_amount,15)
            self.size = min(self.size + self.rotation_amount,35)
        else:
            self.angle = (self.angle - self.rotation_amount) % 360
            self.rotation_amount -=0.1
            self.rotation_amount = max(self.rotation_amount,0)
            self.size = max(self.size - self.rotation_amount,30)

        self.rotated_image = pygame.transform.rotate(self.image,self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=(self.size,self.size))
        self.rotated_rect.center = (self.x,self.y)
        
       
    def draw(self): 
        screen.blit(self.surface,self.rect)
        screen.blit(self.rotated_image,self.rotated_rect)
        Crosshair.rotate(self)
        
        
        #pygame.draw.rect(screen,(255,0,0),(self.x,self.y,3,3),self.size)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self,image,x,y,size):
        super().__init__()
        self.max_size = size
        self.size = size
        self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(self.size,self.size))
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
        
        if dir.length() > World_pos.movement_amount:
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
        self.spacestation_inside = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets","inside_spacestation.png")),(1800,900))
        self.spacestation_inside_rect = self.spacestation_inside.get_rect(center=(SCREEN_WIDTH/2,SCREEN_WIDTH/2-190))
        self.x = x
        self.y = y
        self.center = (self.x,self.y)
        self.angle = 0
        self.rot_surf = self.surf
        self.velocity = 0
        self.airlock = None


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
        surf = pygame.Surface((200,200),pygame.SRCALPHA) 
        self.airlock = surf.get_rect(center=(self.x,self.y))

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
            offset = self.layer + spaceship.acceleration +.5
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
        transparency = round(50 * math.sin(self.life_time)+self.transparency) 
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
        self.surface = pygame.Surface((size,size ),pygame.SRCALPHA)
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
        self.rect.center = self.x,self.y
        self.x += (self.dir[0] + self.spread) * self.speed
        self.y += (self.dir[1] + self.spread) * self.speed

class Explosion_particles():
    def __init__(self,collision_pos,explosion_size,explosion_life,explosion_dir):
        self.collision_pos = collision_pos
        self.x = self.collision_pos[0]
        self.y = self.collision_pos[1]
        self.explosion_size = explosion_size 
        self.explosion_colors = [(210, 119, 60),(120,6,6),(150,6,6),(199,133,12)]
        self.explosion_color = random.choice(self.explosion_colors)
        self.explosion_dir = explosion_dir
        self.explosion_life = random.randint(explosion_life,explosion_life + 20)


    def draw_explosion(self):
        pygame.draw.circle(screen,self.explosion_color,(self.x,self.y),self.explosion_size)

    def update(self):
        
        self.x += (self.explosion_dir[0] + World_pos.direction(spaceship,World_pos.dir_offset)[0])
        self.y += (self.explosion_dir[1] + World_pos.direction(spaceship,World_pos.dir_offset)[1])
        self.explosion_life -= 0.2
        self.explosion_size -=0.001
        for explosion_particle in explosion_praticles:
            if explosion_particle.explosion_life < 0:
                explosion_praticles.remove(explosion_particle)

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

    def update(self,angle):
        dis = math.sqrt((pygame.mouse.get_pos()[1]-spaceship.position[1])**2 + (pygame.mouse.get_pos()[0] - spaceship.position[0])**2)
        
        if  dis > World_pos.offset_distance:
            offset = spaceship.acceleration
        else:
            offset = 0

        if World_pos.offset_distance > 60:
            offset -=1

        if (mouse_pos[0] - spaceship.position[0]) > angle:
            offsetx = -offset 
        elif (mouse_pos[0] - spaceship.position[0]) < -angle:
            offsetx = offset
        else:
            offsetx = 0

        if (mouse_pos[1] - spaceship.position[1]) > angle:
            offsety = -offset
        elif (mouse_pos[1] - spaceship.position[1]) < -angle:
            offsety = offset
        else:
            offsety = 0

        dx = spaceship.position[0] - self.x + random.randint(-100,100) 
        dy = spaceship.position[1] - self.y + random.randint(-100,100)
        dir = math.hypot(dx,dy)
        dx /= dir
        dy /= dir
        self.x += dx * self.speed/10 
        self.y += dy * self.speed/10   
        self.x += offsetx
        self.y += offsety
        self.rect.center = self.x,self.y
        screen.blit(self.surface,(self.rect))
  
class Planet():
    def __init__(self,position,image,size,color,radius,transparency):
        self.position = position 
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.surf = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        self.image = pygame.transform.smoothscale(pygame.image.load(image),(self.size/2,self.size/2))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.color = color
        self.radius = radius
        self.transparency = transparency    

    def draw(self):
        #pygame.draw.circle(self.surf,(*self.color,self.transparency),(planet.x,planet.y),self.radius)
        #screen.blit(self.surf,(0,0))
        screen.blit(self.image,(self.x,self.y))

    def update(self):
        self.x += World_pos.direction(spaceship,World_pos.dir_offset)[0]
        self.y += World_pos.direction(spaceship,World_pos.dir_offset)[1]

class Transition_screen():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y 
        self.color = color
        self.transparecy = 150
        self.surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(0,0))
        self.detection = 0
        
    def update(self,spaceship):
        screen.blit(self.surface,(0,0))
        pygame.draw.rect(self.surface,(*self.color,self.transparecy),(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship.position[1])**2+(mouse_pos[0]-spaceship.position[0])**2))
        if pygame.Rect.colliderect(spaceship.rect,space_station.airlock) and mtos_dis < World_pos.offset_distance:
            transition_screen.color = (0,0,0)
            self.transparecy = min(self.transparecy +1,255)
        else:
            self.transparecy = max(self.transparecy -1,0)
        if self.transparecy == 255:
           global Game_State 
           Game_State = "Spacestation"

        if Game_State == "SpaceStation" : 
            self.transparecy +=1


planet = Planet((3000,-1000),os.path.join("assets","desert_planet.png"),1500,(0,223,135),720/2,20)
crosshair = Crosshair(0,0,30,os.path.join("assets","crosshair.png"))
spaceship = Spaceship(os.path.join("assets","spaceship.png"),SCREEN_WIDTH/2,SCREEN_HEIGHT/2,55)
projectiles = []
explosion_praticles = []
space_station = Space_station(os.path.join("assets","spacestation.png"),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
smoke_particles = []
foreground_stars = []
background_stars = []
parasites = []
transition_screen = Transition_screen(0,0,(0,0,0))
grid = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets","grid.png")).convert_alpha(),(270,160))
grid.set_alpha(70)
grid_rect = grid.get_rect()

while True:

    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    if Game_State == "Space":
            
        
        if len(background_stars) < 150:
            background_stars.append(Star(random.randint(-25,SCREEN_WIDTH),random.randint(-25,SCREEN_HEIGHT),25,random.uniform(0,4),50,random.uniform(0.1,1),random.uniform(-.002,.002)))
        
        for star in background_stars:
            star.draw()
            star.reposition(random.randint(100,200),random.randint(10,95))

        #circle.draw()
        planet.draw()
        planet.update()

        space_station.draw()
        space_station.update(World_pos.dir_offset)
        space_station.spin()

        smoke_particles.append(Rocket_smoke(spaceship.rect.center[0],spaceship.rect.center[1]))

        for particle in smoke_particles[:]:
            particle.draw()
            particle.update()
            particle.direction(World_pos.dir_offset,mouse_pos)
            if particle.size <= 0 or particle.lifetime <= 0:
                smoke_particles.remove(particle)

        Projectile.projectile_delay +=1 

        if Projectile.projectile_delay > 15:
            if pygame.mouse.get_pressed()[2]:
                sounds = [Sounds.lazer.set_volume(0.05),Sounds.lazer.set_volume(0.07)]
                random.choice(sounds)
                Sounds.lazer.play(loops=0)
                for projectile_num in range(2):
                    projectiles.append(Projectile(spaceship.position,25,5,random.uniform(-.03,.03),(255,231,0),100))
                Projectile.projectile_delay = 0

        for projectile in projectiles[:]:
            projectile.draw()
            
            projectile.update()
            if projectile.x > SCREEN_WIDTH +30 or projectile.x < -30:
                projectiles.remove(projectile)
            elif projectile.y > SCREEN_HEIGHT +30 or projectile.y < -30:
                projectiles.remove(projectile)
            
        spaceship.update()
        spaceship.point_towards(mouse_pos)
        spaceship.move(mouse_pos)

        if len(parasites) < World_pos.parasite1amount: #50
            parasites.append(Parasite(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),os.path.join("assets","parasite1.png"),15,random.uniform(1,10)))
        for parasite in parasites:
            parasite.update(World_pos.dir_offset)
            for projectile in projectiles:
                if pygame.Rect.colliderect(parasite.rect,projectile.rect):
                    Sounds.boom.set_volume(10)
                    Sounds.boom.play()
                    for explosion_particle_num in range(random.randint(5,7)):
                        explosion_praticles.append(Explosion_particles((parasite.x,parasite.y),random.uniform(1,3),70,[random.uniform(-0.5,0.5),random.uniform(-0.3,0.3)]))
                    try:
                        projectiles.remove(projectile)
                        parasites.remove(parasite)
                        if pygame.Rect.colliderect(spaceship.rect,space_station.airlock) == False:
                            transition_screen.color = (255,255,255)
                            transition_screen.transparecy = random.randint(0,20)
                    except:
                        pass

        for explosion in explosion_praticles:
            explosion.draw_explosion()
            explosion.update()

        if len(foreground_stars) < 150:
            foreground_stars.append(Star(random.randint(-25,SCREEN_WIDTH),random.randint(-25,SCREEN_HEIGHT),25,random.uniform(0,4),50,random.uniform(5,15)/10,random.uniform(-.002,.002)))
            
        for star in foreground_stars:
            star.draw()
            star.reposition(random.randint(100,200),random.randint(10,90))

        if pygame.Rect.colliderect(spaceship.rect,space_station.rect):
            #print("touching space station")
            pass

        screen.blit(grid,(15,SCREEN_HEIGHT-170))
        crosshair.draw()
        crosshair.update(pygame.mouse.get_pos())

    #Game_State = "Spacestation"
    #transition_screen.transparecy = 0

    if Game_State == "Spacestation":
        
        screen.blit(space_station.spacestation_inside,space_station.spacestation_inside_rect)
        pygame.draw.rect(screen,(255,214,164),(300,300,15,15))

    transition_screen.update(spaceship)
        

    Clock.tick(FPS)
    pygame.display.flip()
    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    quit_game()