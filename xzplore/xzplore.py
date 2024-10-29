import pygame
from pygame.sprite import Group
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=16, buffer=1024)
import math
import random
import sys
import os 
import numpy as np

from asset_dicts import *


SCREEN_WIDTH = 1200#950w
SCREEN_HEIGHT = 800 #650
FPS = 120
BLACK  = (0,0,0)
SPACESTATION_GREY = (50,50,50)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.NOFRAME ,vsync=False)

pygame.mouse.set_visible(False)
Clock = pygame.time.Clock()
Game_State = "Space"

class Sounds():
    ambience = pygame.mixer.Channel(6)
    rocket_engine = pygame.mixer.Channel(2)

    lazer = pygame.mixer.Sound(os.path.join("xzplore/sounds","laser_gun.wav"))
    boom = pygame.mixer.Sound(os.path.join("xzplore/sounds","boom.wav"))
    space_ambience = pygame.mixer.Sound(os.path.join("xzplore/sounds","space_background_noise.mp3"))
    desert_wind = pygame.mixer.Sound(os.path.join("xzplore/sounds","sandstorm.wav"))
    rocket_engine_sound = pygame.mixer.Sound(os.path.join("xzplore/sounds","short_rocket.mp3"))

    def play_sound(sound,volume): 
        while Sounds.ambience.get_busy() == False: 
            Sounds.ambience.play(sound) 
            Sounds.ambience.set_volume(volume)
    
    def play_engine():
        while Sounds.rocket_engine.get_busy() == False:
            Sounds.rocket_engine.play(Sounds.rocket_engine_sound)

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
        volume = 0
        Sounds.play_engine()
        if pygame.mouse.get_pressed()[0]:
            self.acceleration +=0.01
            Sounds.rocket_engine.set_volume(1)
        else:
            Sounds.rocket_engine.set_volume(0.5)
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
        self.spacestation_inside = pygame.transform.smoothscale(pygame.image.load(os.path.join("xzplore/assets","inside_spacestation.png")),(1800,900))
        self.spacestation_inside_rect = self.spacestation_inside.get_rect(center=(SCREEN_WIDTH/2+30,SCREEN_WIDTH/2-200))
        self.x = x
        self.y = y
        self.center = (self.x,self.y)
        self.angle = 0
        self.rot_surf = self.surf
        self.velocity = 0
        self.airlock = None
        self.move_amount = 1.5

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
    
    def move(self):
        keys = pygame.key.get_pressed()
        if Game_State == "Spacestation":
            if keys[pygame.K_a]:
                self.spacestation_inside_rect.x += self.move_amount
            if keys[pygame.K_d]:
                self.spacestation_inside_rect.x -= self.move_amount
            if keys[pygame.K_w]:
                self.spacestation_inside_rect.y += self.move_amount
            if keys[pygame.K_s]:
                self.spacestation_inside_rect.y -= self.move_amount    

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
        self.color = color
        self.radius = radius
        self.transparency = transparency    

    class Tile():

        world_x = 0 
        world_y = 0 

        move_amount = 0

        tile_map = np.array([
            [0,0,0,0,0,0,1,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0],
            [0,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
        ])
        
    
        ecosystem_map =  np.array([
            [3,0,2,4,0,1,2,0,0],
            [2,1,0,0,4,0,2,0,0],
            [0,3,0,2,0,0,2,0,0],
            [0,2,4,0,0,3,4,0,0],
            [3,0,2,0,4,2,0,0,0],
            [0,0,0,0,0,0,0,0,0],
        ])
        
        num_tile_in_tilemap = len(tile_map[0])*len(tile_map)
     
        TILE_SIZE = 200  

        def __init__(self,image,size,tile_num,x,y,item):
            self.tile_size = size
            self.image = image
            self.x = x
            self.y = y
            self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(self.tile_size,self.tile_size))
            self.rect = self.surf.get_rect(topleft=(self.x,self.y))
            self.tile_num = tile_num
            try:
                self.item = item["item"]
                self.item_description = item["description"]
            except:
                pass

    class Clouds():
    
        def __init__(self,image):
            self.x = 0
            self.y = 0
            self.width = 800
            self.height = 500
            self.speed = random.randint(2,3)
            self.image = image
            self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(self.width,self.height))
            self.surf.set_alpha(10)
            self.rect = self.surf.get_rect()
            self.start_y = random.randint(-2,7)*100
            self.start_x = random.randint(2,3)*-self.width
            

        def draw_clouds(clouds):
            
            cloud_image = os.path.normpath(os.path.join(clouds["path"],random.choice(clouds["clouds"])))

            if len(Planet.clouds) < 3:
                Planet.clouds.append(Planet.Clouds(cloud_image))

            cloud_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
            
            for cloud in Planet.clouds: 
                cloud.rect.x += 1.5
                cloud_surface.blit(cloud.surf,cloud.rect)
                screen.blit(cloud_surface,(0,0))    

                cloud.rect.y = int(Planet.Tile.world_y + cloud.start_y)

                if cloud.rect.x > SCREEN_WIDTH:
                    cloud.rect.x = cloud.start_x
         
    def draw_planet(self):
        #pygame.draw.circle(self.surf,(*self.color,self.transparency),(planet.x,planet.y),self.radius)
        #screen.blit(self.surf,(0,0))
        self.rect = self.image.get_rect(center=((self.x,self.y)))
        screen.blit(self.image,self.rect)
 
    def update(self):
        self.x += World_pos.direction(spaceship,World_pos.dir_offset)[0]
        self.y += World_pos.direction(spaceship,World_pos.dir_offset)[1]

    def draw_map(map_tile,grass,rocks,bush,gems):

        #image = os.path.normpath(("xzplore/assets/desert_planet_assets/desert_sandtiles/desert_sandtile_0.png"))
        tile_num = 0

        buried_collectible_num = 0
        rock_collectibles_num = 0
        
        for index,row in enumerate(Planet.Tile.tile_map):
            for col in range(len(row)):
                try:
                    if len(Planet.tiles) <= Planet.Tile.num_tile_in_tilemap: #hardcoded number
                        if row[col] == 0:
                            image = (os.path.normpath(os.path.join(map_tile["path"],map_tile["normal_tiles"])))
                        elif row[col] == 1:
                            image = (os.path.normpath(os.path.join(map_tile["path"],random.choice(map_tile["dig_tiles"]))))
                            if random.randint(1,5) == 2: #PUTS FOSSIL ON DIG TILE
                                Collectibles.buried_collectables.append(Item(*Collectibles.random_fossil()))
                                Collectibles.buried_collectables[buried_collectible_num].pos = int(col*Planet.Tile.TILE_SIZE)+random.randint(70,150),int((index*Planet.Tile.TILE_SIZE))+random.randint(50,150)
                                buried_collectible_num +=1
                                #print(Collectibles.buried_collectables[buried_collectible_num].pos)
                    
                        Planet.tiles.append(Planet.Tile(image,200,tile_num,0,0,None))                        
                    screen.blit(Planet.tiles[tile_num].surf,(Planet.tiles[tile_num].rect.topleft))
                    x,y = int((col*Planet.Tile.TILE_SIZE)+Planet.Tile.world_x),int((index*Planet.Tile.TILE_SIZE)+Planet.Tile.world_y)
                    Planet.tiles[tile_num].rect.topleft = x,y

                except:
                    pass 
                tile_num+=1
        
        for item in Collectibles.buried_collectables:
            item.draw()

        tile1_num = 0
        for index,row in enumerate(Planet.Tile.tile_map):
            for col in range(len(row)):                
                try:
                    if len(Planet.tiles) <= Planet.Tile.num_tile_in_tilemap:
                        if Planet.Tile.ecosystem_map[index][col] == 2:
                            grass_image = os.path.normpath(os.path.join(grass["path"],random.choice((grass["grass"]))))
                            Planet.ecosystem.append(Planet.Tile(grass_image,200,None,random.randint(75,125),random.randint(75,125),grass))
                        elif Planet.Tile.ecosystem_map[index][col] == 3:
                            rock_image = os.path.normpath(os.path.join(rocks["path"],random.choice(rocks["rocks"])))
                            Planet.ecosystem.append(Planet.Tile(rock_image,200,None,random.randint(75,125),random.randint(75,125),rocks))
                            
                            Collectibles.rock_collectables.append(Item(*Collectibles.random_gem(gems)))
                            Collectibles.rock_collectables[rock_collectibles_num].pos = int(col*Planet.Tile.TILE_SIZE)+200,int((index*Planet.Tile.TILE_SIZE))+200
                            rock_collectibles_num+=1

                        elif  Planet.Tile.ecosystem_map[index][col] == 4:
                            bush_image = os.path.normpath(os.path.join(bush["path"],random.choice(bush["bushes"])))
                            Planet.ecosystem.append(Planet.Tile(bush_image,80,None,random.randint(75,125),random.randint(75,125),bush))
                        else:
                            Planet.ecosystem.append(None)

                    if Planet.Tile.ecosystem_map[index][col] == 2 or Planet.Tile.ecosystem_map[index][col] == 3 or Planet.Tile.ecosystem_map[index][col] == 4:
                        screen.blit(Planet.ecosystem[tile1_num].surf,Planet.ecosystem[tile1_num].rect.topleft)
                    #print(Planet.ecosystem)
                    x,y = int((col*Planet.Tile.TILE_SIZE)+Planet.Tile.world_x),int((index*Planet.Tile.TILE_SIZE)+Planet.Tile.world_y)

                    shake = random.randint(0,25)
                    if shake == 0:
                        Planet.ecosystem[tile1_num].rect.topleft = (Planet.ecosystem[tile1_num].x+x)+random.randint(-1,1),(Planet.ecosystem[tile1_num].y+y)+random.randint(-1,1)
                    else:
                        Planet.ecosystem[tile1_num].rect.topleft = (Planet.ecosystem[tile1_num].x+x),(Planet.ecosystem[tile1_num].y+y)

                except:
                    pass
                tile1_num+=1

      
        for item in Collectibles.rock_collectables:    
            item.draw()
        
        
    def map_move():

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            Planet.Tile.move_amount = 1
        else:
            Planet.Tile.move_amount = .5
            
        if keys[pygame.K_a]:
            Planet.Tile.world_x +=Planet.Tile.move_amount
        elif keys[pygame.K_d]:
            Planet.Tile.world_x -=Planet.Tile.move_amount
        if keys[pygame.K_w]:
            Planet.Tile.world_y +=Planet.Tile.move_amount
        elif keys[pygame.K_s]:
            Planet.Tile.world_y -=Planet.Tile.move_amount
    
    tiles = []
    ecosystem = []
    clouds = []
    
    #orange_tile = Tile(os.path.normpath("assets\desert_planet_assets\desert_sandtiles\desert_sandtile_0.png"))

class Player():

    animation_number = 0 
    animation_delay = 50
    curr_time = 0
    timer = 0

    idle_state = str(Player_animations.player_assests["down_idle"])

    tool_range = 70
    tool_distance = 0

    

    def __init__(self,image):
        self.image = image
        self.surf = pygame.transform.smoothscale(pygame.image.load(os.path.normpath(self.image)).convert_alpha(),(50,50))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    
    def get_animation(path,player_assets):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            direction = "up"
            animations_path = player_assets["up_walk_path"]
            animations = Player_animations.player_assests["up_walk"]
            Player.idle_state = str(Player_animations.player_assests["up_idle"])
            return animations_path,animations
        elif key[pygame.K_s]:
            direction = "down"
            animations_path = player_assets["down_walk_path"]
            animations = player_assets["down_walk"]
            Player.idle_state = str(Player_animations.player_assests["down_idle"])
            return animations_path,animations
        elif key[pygame.K_a]:
            direction = "left"
            animations_path = player_assets["left_walk_path"]
            animations = player_assets["left_walk"]
            Player.idle_state = str(Player_animations.player_assests["left_idle"])
            return animations_path,animations
        elif key[pygame.K_d]:
            direction = "right"
            animations_path = player_assets["right_walk_path"]
            animations = player_assets["right_walk"]
            Player.idle_state  = str(Player_animations.player_assests["right_idle"])
            return animations_path,animations
        else:
            return path,Player.idle_state
            
    def draw_player(animation):

        
        
        try:
            if Player.animation_number > len(animation[1]) -1:
                Player.animation_number = 0

            player_animation = (os.path.normpath(os.path.join(animation[0],animation[1][Player.animation_number])))

            player = pygame.transform.smoothscale(pygame.image.load(player_animation).convert_alpha(),(50,50))
        except:
            player = pygame.transform.smoothscale(pygame.image.load(Player.idle_state).convert_alpha(),(50,50))


        Player.curr_time = pygame.time.get_ticks() 
        if  Player.curr_time > Player.timer:
            Player.animation_number+=1
            Player.timer  = Player.curr_time + Player.animation_delay

            #print(Player.animation_number)

        player_rect = player.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
   
        shadow_surface = pygame.Surface((50,50),pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface,(0,0,0,50),(15,30,20,15),50)
       
       
        screen.blit(shadow_surface,player_rect)
        screen.blit(player,player_rect)

    def draw_crosshair():

        player_crosshair = pygame.transform.smoothscale(pygame.image.load(os.path.join("xzplore/assets","player_crosshair.png")).convert_alpha(),(40,40))
       
        if pygame.mouse.get_pressed()[2] == False or Player.tool_distance > Player.tool_range:
            screen.blit(player_crosshair,(pygame.mouse.get_pos()[0]-20,pygame.mouse.get_pos()[1]-20))
    
class Toolbar():
    tool_num = 2
    def draw_toolbar():
        
        if Game_State != "Space":
            start_x = SCREEN_WIDTH - 203
            start_y = 15

            toolbar_surface = pygame.Surface((600,150),pygame.SRCALPHA)
            pygame.draw.rect(toolbar_surface,(0,0,0,150),(391,5,200,40),border_radius=8)
            pygame.draw.rect(toolbar_surface,(0,0,0,250),(391,5,200,40),3,8)

            shovel = pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/toolbar_shovel.png").convert_alpha(),(35,30))
            shovel_rect = shovel.get_rect()
            pickaxe =  pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/toolbar_pickaxel.png").convert_alpha(),(35,30))
            pickaxe_rect = pickaxe.get_rect()
            gen5 = pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/toolbar_gen5.png").convert_alpha(),(30,30))
            gen5_rect = gen5.get_rect()
            book = pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/toolbar_book.png").convert_alpha(),(30,30))
            book_rect = book.get_rect()


            gen5_rect.x = start_x + 5
            gen5_rect.y = start_y 
            pickaxe_rect.x = start_x + 50
            pickaxe_rect.y = start_y 
            shovel_rect.x = start_x + 101
            shovel_rect.y = start_y
            book_rect.x = start_x + 155
            book_rect.y = start_y

            pygame.draw.rect(toolbar_surface,(255,255,255,50),(390 + Toolbar.tool_num * 51,4,49,41),4,border_radius=0)
            
            screen.blit(toolbar_surface,(600,5))
            screen.blit(shovel,shovel_rect)
            screen.blit(pickaxe,pickaxe_rect)
            screen.blit(gen5,gen5_rect)
            screen.blit(book,book_rect)

    def draw_tool():
    
        mouse_pos = pygame.mouse.get_pos()
        Player.tool_distance = math.sqrt(int(mouse_pos[1] - SCREEN_HEIGHT/2)**2 + int(mouse_pos[0] - SCREEN_WIDTH/2)**2)
        
        if pygame.mouse.get_pressed()[2] == True:

            pickaxe = pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/pickaxe.png").convert_alpha(),(33,30))
            pickaxe_rect = pickaxe.get_rect(topleft=(0,0))
            pickaxe_rect.centerx = mouse_pos[0]
            pickaxe_rect.centery = mouse_pos[1] + 5

            shovel = pygame.transform.smoothscale(pygame.image.load("xzplore/assets/tools/shovel.png").convert_alpha(),(40,25))
            shovel_rect = shovel.get_rect(topleft=(0,0))
            shovel_rect.centerx = mouse_pos[0]
            shovel_rect.centery = mouse_pos[1] - 5 #+ random.randint(-3,3)

            player_crosshair = pygame.transform.smoothscale(pygame.image.load(os.path.join("xzplore/assets","player_crosshair.png")).convert_alpha(),(40,40))
       
            if Player.tool_distance < Player.tool_range:
                if Toolbar.tool_num == 0:
                    screen.blit(player_crosshair,(pygame.mouse.get_pos()[0]-20,pygame.mouse.get_pos()[1]-20))
                if Toolbar.tool_num == 1:
                    screen.blit(pickaxe,pickaxe_rect)
                if Toolbar.tool_num == 2:
                    screen.blit(shovel,shovel_rect)
        

        #print(screen.get_at(mouse_pos))

class Tool_particles():

    def __init__(self,x,y,color,size,spread,speed,lifespan) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.spread = spread
        self.lifetime = 0
        self.lifespan = lifespan

    surface = pygame.Surface((50,50),pygame.SRCALPHA)

    def draw_particles():
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect((mouse_pos[0],mouse_pos[1],1,1))
        

        try:
            color = screen.get_at((mouse_pos[0],mouse_pos[1]+10))

            if pygame.mouse.get_pressed()[2] == True:
                if Player.tool_distance < Player.tool_range:
                    for col in range(len(color)):
                        color[col] = color[col] - random.randint(10,20)

                    for item in Planet.ecosystem:
                        if len(Tool_particles.tool_particles) < 130:

                            try:
                                item_rect = pygame.Rect(item.rect.x+(item.rect.width/3),item.rect.y+(item.rect.height/3),item.rect.width/3,item.rect.height/3)
                                #pygame.draw.rect(screen,(255,0,0),item_rect,1)
                                if pygame.Rect.colliderect(item_rect,mouse_rect):
                                    if Toolbar.tool_num == 1:
                                        Tool_particles.tool_particles.append(
                                            Tool_particles(mouse_pos[0],mouse_pos[1],
                                                           (color),size=random.randint(3,7),
                                                           spread=(random.uniform(-.5,.5),random.uniform(-.5,.5)),
                                                           speed=random.uniform(-1,1),
                                                           lifespan=random.uniform(200,400)))
                                
                                elif pygame.Rect.colliderect(item_rect,mouse_rect) == False:
                                    if Toolbar.tool_num == 2:
                                        Tool_particles.tool_particles.append(Tool_particles(mouse_pos[0],mouse_pos[1],
                                                           (color),size=random.randint(3,7),
                                                           spread=(random.uniform(-1.5,1.5),random.uniform(-1,1.5)),
                                                           speed=random.uniform(-1,1),
                                                           lifespan=random.uniform(200,250)))
                            except:
                                pass
        except:
            pass


        for particle in Tool_particles.tool_particles:
            pygame.draw.rect(screen,(particle.color),(particle.x,particle.y,particle.size,particle.size))
        
    def update():
        keys = pygame.key.get_pressed()
        for particle in Tool_particles.tool_particles:

            if particle.lifetime > 21:
                if keys[pygame.K_a]:
                    particle.x += Planet.Tile.move_amount
                elif keys[pygame.K_d]:
                    particle.x -= Planet.Tile.move_amount
                if keys[pygame.K_w]:
                    particle.y += Planet.Tile.move_amount
                elif keys[pygame.K_s]:
                    particle.y -= Planet.Tile.move_amount
                
            if particle.lifetime < random.uniform(18,20):
                particle.x += particle.spread[0] + random.randint(-1,1)
                particle.y += particle.spread[1] + random.randint(-1,1)
            
            particle.lifetime +=1
            if particle.size > 1:
                
                particle.size -= random.uniform(0,0.01)

            if particle.lifetime > particle.lifespan:
                Tool_particles.tool_particles.remove(particle)
        
    tool_particles = []

class Item_display():
    display_x = 170
    display_y = 50

    def __init__(self):
        self.item = None
        self.item_description = None
        self.surface = pygame.Surface((200,400),pygame.SRCALPHA)
        self.surf_rect = self.surface.get_rect(topright=(SCREEN_WIDTH-10,10))
        self.image = None
        self.rect = None
        self.font = pygame.font.Font(None,17)
        self.text = None
        self.text_rect = None
        self.window_radius = 10
  
    def draw_item_display_window(self):
        if Game_State != "Space":
                
            try:
                image,item,description = Item_display.find_item(self)
                screen.blit(self.surface,self.surf_rect)
                pygame.draw.rect(self.surface,(0,0,0,140),(30,Item_display.display_y,170,250),0,self.window_radius)
                pygame.draw.rect(self.surface,(0,0,0),(30,Item_display.display_y,170,250),3,self.window_radius)
                pygame.draw.rect(self.surface,(0,0,0),(30,Item_display.display_y,170,150),3,0,self.window_radius,self.window_radius)
                self.image = pygame.transform.smoothscale(pygame.image.load(image).convert_alpha(),(130,130))
                self.rect = self.image.get_rect()
                screen.blit(self.image,(SCREEN_WIDTH-160,Item_display.display_y+20))
                split_text = description.split()
                text_len = 0
                text_height = 0
                self.text = self.font.render(item,True,(255,255,255))
                self.text_rect = self.text.get_rect(topleft=(SCREEN_WIDTH-165+text_len,Item_display.display_y+170+text_height))
                screen.blit(self.text,self.text_rect)
                text_height = 23
                for text in split_text:
                    self.text = self.font.render(text,True,(255,255,255))
                    self.text_rect = self.text.get_rect(topleft=(SCREEN_WIDTH-165+text_len,Item_display.display_y+170+text_height))
                    width = self.text.get_width()
                    text_len += width + 5
                    if self.text_rect.x > 1090:
                        text_len = 0
                        text_height += 15
                    screen.blit(self.text,self.text_rect)
            except:
                pass
            
    def find_item(self):    

        mouse_pos = pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)
        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1], 1, 1)


        for item in Collectibles.buried_collectables:
            try:
                if pygame.Rect.colliderect(item.rect,mouse_rect) and item.detection_time <= 0:
                    return item.image,item.item,item.item_description
            except:
                pass
        
        for item in Collectibles.rock_collectables:
            try:
                item_rect = pygame.Rect(item.rect.x+(item.rect.width/3),item.rect.y+(item.rect.height/3),item.rect.width/3,item.rect.height/3)
                if pygame.Rect.colliderect(item.rect,mouse_rect) and item.detection_time <= 0: #ADD DETECTION TIME
                    return item.image,item.item,item.item_description
            except:
                pass
    

        for item in Planet.ecosystem:
            try:
                item_rect = pygame.Rect(item.rect.x+(item.rect.width/3),item.rect.y+(item.rect.height/3),item.rect.width/3,item.rect.height/3)
                #pygame.draw.rect(screen,(255,0,0),item_rect,1)
                if pygame.Rect.colliderect(item_rect,mouse_rect):
                    return item.image,item.item,item.item_description
            except:
                pass
   

        
class Item():
    def __init__(self,item,item_description,pos,image,size,detection_time) -> None:
        self.pos = pos
        self.item = item
        self.item_description = item_description
        self.image = image
        self.size  = size
        self.detection_time = detection_time
        self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(self.size,self.size))
        self.rect = self.surf.get_rect()
        self.surf.set_alpha(0) #0
        
        

    def draw(self):
        self.rect.center = (self.pos[0]+Planet.Tile.world_x),(self.pos[1]+Planet.Tile.world_y)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)  #self.rect every image that passes throught the draw parameter
        screen.blit(self.surf,self.rect)
        for item in range(len(Collectibles.buried_collectables)):
            
            if pygame.mouse.get_pressed()[2] and pygame.Rect.colliderect(Collectibles.buried_collectables[item].rect ,pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)):
                if Player.tool_distance < Player.tool_range and Toolbar.tool_num == 2:
                    Collectibles.buried_collectables[item].detection_time -= 0.1
                    if Collectibles.buried_collectables[item].detection_time < 0:
                        Collectibles.buried_collectables[item].surf.set_alpha(round(Collectibles.buried_collectables[item].surf.get_alpha()+0.6))

        for item in range(len(Collectibles.rock_collectables)):
            if pygame.mouse.get_pressed()[2] and pygame.Rect.colliderect(Collectibles.rock_collectables[item].rect ,pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1)):
                if Player.tool_distance < Player.tool_range and Toolbar.tool_num == 1:
                    Collectibles.rock_collectables[item].detection_time -= 0.1
                    if Collectibles.rock_collectables[item].detection_time < 0:
                        Collectibles.rock_collectables[item].surf.set_alpha(round(Collectibles.rock_collectables[item].surf.get_alpha()+0.6))
            


class Collectibles():

    def random_fossil():
        Fossil = ("Fossil","Skeletal remains of a once living organism",random.randint(200,800),
                  os.path.join(Colletibles.collectible_items["fossil_path"],random.choice(Colletibles.collectible_items["fossils"])),random.randint(5,8)*10,random.randint(250,300))
        return Fossil


    def random_gem(gem):
        #print(random.choice(gem))
        gem_parameters = random.choice(gem)
        Gem = (gem_parameters["item"],gem_parameters["description"],0,gem_parameters["image"],25,150)
        return Gem

    buried_collectables = []
    rock_collectables = []

class Transition_screen():

    def __init__(self,x,y,color):
        self.x = x
        self.y = y 
        self.color = color
        self.transparecy = 150
        self.surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=(0,0))
        self.detection = 0

    def change_state(self,gamestate,window_color):
        global Game_State
        transition_screen.color = window_color
        if self.detection > 200:
            self.transparecy = min(self.transparecy +1,255)
        if self.detection > 0  and self.transparecy == 255:
            Game_State = gamestate  
            Sounds.ambience.stop()
            self.detection = 0

        if Game_State == "Spacestation":
            if space_station.spacestation_inside_rect.y < -91:
                self.detection +=1
                if self.detection > 200:
                    self.transparecy = min(self.transparecy +1,255)
                if self.detection > 0  and self.transparecy == 255:
                    Game_State = "Space"   
            else:
                self.transparecy = max(self.transparecy -1,0)
        
        if Game_State == "Desert_planet":
            self.detection = 0
            self.transparecy = max(self.transparecy -1,150)


    def update(self,spaceship):
        screen.blit(self.surface,(0,0))
        pygame.draw.rect(self.surface,(*self.color,self.transparecy),(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        mtos_dis = round(math.sqrt((mouse_pos[1]-spaceship.position[1])**2+(mouse_pos[0]-spaceship.position[0])**2))
        global Game_State
        self.detection +=1 
        if mtos_dis < World_pos.offset_distance +15:
            if pygame.Rect.colliderect(spaceship.rect,space_station.airlock):
                Transition_screen.change_state(self,"Spacestation",(0,0,0))
            elif pygame.Rect.colliderect(spaceship.rect,planet.rect):
                Transition_screen.change_state(self,"Desert_planet",(191,123,32))
        else:
            if Game_State == "Space":
                self.transparecy = max(self.transparecy -1,0)
    

planet = Planet((3000,-1000),os.path.join("xzplore/assets","desert_planet.png"),1500,(0,223,135),720/2,20)
crosshair = Crosshair(0,0,30,os.path.join("xzplore/assets","crosshair.png"))
spaceship = Spaceship(os.path.join("xzplore/assets","spaceship.png"),SCREEN_WIDTH/2,SCREEN_HEIGHT/2,55)
projectiles = []
explosion_praticles = []
space_station = Space_station(os.path.join("xzplore/assets","spacestation.png"),SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
smoke_particles = []
foreground_stars = []
background_stars = []
parasites = []
transition_screen = Transition_screen(0,0,(0,0,0))
grid = pygame.transform.smoothscale(pygame.image.load(os.path.join("xzplore/assets","grid.png")).convert_alpha(),(270,160))
grid.set_alpha(70)
grid_rect = grid.get_rect()
item_display_window = Item_display()

while True:

    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    if Game_State == "Space":
        #Sounds.space_background_noise.play(loops=0)
        
        if len(background_stars) < 150:
            background_stars.append(Star(random.randint(-25,SCREEN_WIDTH),random.randint(-25,SCREEN_HEIGHT),25,random.uniform(0,4),50,random.uniform(0.1,1),random.uniform(-.002,.002)))
        
        for star in background_stars:
            star.draw()
            star.reposition(random.randint(100,200),random.randint(10,95))

        #circle.draw()
        planet.draw_planet()
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
                for projectile_num in range(2):
                    projectiles.append(Projectile(spaceship.position,25,5,random.uniform(-.03,.03),(255,231,0),100))
                Projectile.projectile_delay = 0
                pygame.mixer.Sound.play(Sounds.lazer,loops=0)

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
            parasites.append(Parasite(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT),os.path.join("xzplore/assets","parasite1.png"),15,random.uniform(1,10)))
        for parasite in parasites:
            parasite.update(World_pos.dir_offset)
            for projectile in projectiles:
                if pygame.Rect.colliderect(parasite.rect,projectile.rect):
                    Sounds.boom.set_volume(10)
                    pygame.mixer.Sound.play(Sounds.boom)
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
        
        Sounds.play_sound(Sounds.space_ambience,.1)
    if Game_State == "Spacestation":
        
        screen.blit(space_station.spacestation_inside,space_station.spacestation_inside_rect)
        pygame.draw.rect(screen,(255,214,164),(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,15,15))
        space_station.move()

    if Game_State == "Desert_planet":
        Sounds.play_sound(Sounds.desert_wind,0.1)
        Planet.draw_map(Desert_planet.map_tiles,Desert_planet.grass_assets,Desert_planet.rock_assets,Desert_planet.bush_assets,Colletibles.desert_collectibles)
        Planet.map_move()
        #Planet.Clouds.draw_clouds(Clouds.clouds_assets)
        Tool_particles.draw_particles()
        Tool_particles.update()
        
        Player.draw_player(Player.get_animation(Player_animations.path,Player_animations.player_assests))
        
        Player.draw_crosshair()
        Toolbar.draw_tool()
        
        
   
    transition_screen.update(spaceship)
    item_display_window.draw_item_display_window()
    Toolbar.draw_toolbar()

    Game_State = "Desert_planet"
    transition_screen.transparecy = 0
    
    
    Clock.tick(FPS)
    pygame.display.flip()
    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 :
                    Toolbar.tool_num -=1
                elif event.y < 0:
                    Toolbar.tool_num +=1
            if Toolbar.tool_num > 3:
                Toolbar.tool_num = 0
            if Toolbar.tool_num < 0:
                Toolbar.tool_num = 3
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    quit_game()
