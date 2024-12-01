import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)
pygame.display.set_caption("Photon Precesion")
clock = pygame.time.Clock()
Game_state = "Main_menu"

class Main_menu():
    
    class Buttons():
        def __init__(self,x,y,width,length,text):
            self.x = x 
            self.y = y 
            self.width = width 
            self.length = length 
            self.transparency = 255
            self.rect = (self.x,self.y,self.width,self.length)
            self.font = pygame.font.Font(None,30)
            self.text = text 
            self.font_render = self.font.render(self.text,True,(255,255,255,self.transparency))
            self.font_rect = self.font_render.get_rect()
            self.game_state = text

    practice_button = Buttons(40,40,170,40,"Practice")
    versus_button = Buttons(40,110,170,40,"Versus")
    buttons = [practice_button,versus_button]


    def display_main_menu():
        surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        pygame.draw.rect(surface,(255,255,255,Main_menu.practice_button.transparency),Main_menu.practice_button.rect,1)
        screen.blit(Main_menu.practice_button.font_render,(50,50))

        
        pygame.draw.rect(surface,(255,255,255,Main_menu.versus_button.transparency),Main_menu.versus_button.rect,1)
        screen.blit(Main_menu.versus_button.font_render,(50,120))
        
        screen.blit(surface,(0,0))

        for button in Main_menu.buttons:
            if pygame.Rect.colliderect(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1),button.rect):
                button.transparency = max(180,button.transparency-1)
                if pygame.mouse.get_pressed()[0]:
                    global Game_state
                    Game_state = button.game_state 
            else:
                button.transparency = min(255,button.transparency+1)
            
            
class Battle_field():

    class Tile():
        tile_size = 50

        def __init__(self,x,y,width,length):
            self.x = x + 100
            self.y = y + 50
            self.width = width 
            self.length = length
            self.border_width = random.randint(1,1)
            self.transparency = 0
            self.color = (255,255,255)

    battle_field = []
    
    for col in range(10):
        for row in range(12):
            battle_field.append(Tile(Tile.tile_size*row,Tile.tile_size*col,Tile.tile_size,Tile.tile_size))

    def draw_battle_field():
        surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        
        if pygame.mouse.get_pressed()[0]:
            Battle_field.Tile.tile_size = 100
        else:
            Battle_field.Tile.tile_size = 50

        for tile in Battle_field.battle_field:
            if pygame.Rect.colliderect(pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],1,1),pygame.Rect(tile.x,tile.y,tile.width,tile.length)):
                
                tile.transparency = max(0,tile.transparency-10)
                tile.color = (tile.color[0],tile.color[1],tile.color[2],tile.transparency)
                tile.border_width = 5
            else:
                tile.transparency = min(40,tile.transparency+1)
                tile.color = (tile.color[0],tile.color[1],tile.color[2],tile.transparency)
                tile.border_width = 1
            
            pygame.draw.rect(surface,tile.color,(tile.x,tile.y,tile.width,tile.length),tile.border_width)
        pygame.draw.rect(surface,(255,255,255,150),(100,50,600,500),1)
        screen.blit(surface,(0,0))
    
    class Player():
        def __init__(self,x,y,width,length,colors,border_wdith):
            self.x = x
            self.y = y
            self.position = None
            self.width = width
            self.length = length
            self.surface = pygame.Surface((self.width,self.length),pygame.SRCALPHA)
            self.rect = self.surface.get_rect(center=(self.x,self.y))
            self.border_width = border_wdith
            self.colors = colors
            self.x_velocity = 1
            self.y_velocity = 1
            self.velocity = 1.5
            self.speed = 1 
            self.angle = 0
            self.x_direction = None
            self.y_direction = None

        def draw_player():
            
            pygame.draw.rect(Battle_field.player1.surface,Battle_field.player1.colors,
            (0,0,Battle_field.player1.width,Battle_field.player1.length),Battle_field.player1.border_width)

            dx = pygame.mouse.get_pos()[0] - Battle_field.player1.x
            dy = pygame.mouse.get_pos()[1] - Battle_field.player1.y

            Battle_field.player1.angle = math.degrees(math.atan2(dx,dy))
                
            rot_surf = pygame.transform.rotate(Battle_field.player1.surface,Battle_field.player1.angle)
            Battle_field.player1.rect = rot_surf.get_rect(center=(int(Battle_field.player1.x),int(Battle_field.player1.y)))

            screen.blit(rot_surf,(Battle_field.player1.rect))
           
            pygame.draw.rect(screen,(255,0,0),(326,303,150,30),1,5)
        

        def move_player():
            key = pygame.key.get_pressed()
            shift_key = pygame.key.get_pressed()[pygame.K_LSHIFT]

         
 
            if key[pygame.K_w]:
                Battle_field.player1.y -= Battle_field.player1.speed 
                Battle_field.player1.y_velocity = Battle_field.player1.velocity
                Battle_field.player1.y_direction = "up"
            else:
                if shift_key:
                    if Battle_field.player1.y_direction == "up":
                        Battle_field.player1.y -= Battle_field.player1.y_velocity

            if key[pygame.K_s]:
                Battle_field.player1.y += Battle_field.player1.speed 
                Battle_field.player1.y_velocity = Battle_field.player1.velocity
                Battle_field.player1.y_direction = "down"
            else:
                if shift_key:
                    if Battle_field.player1.y_direction == "down":
                        Battle_field.player1.y += Battle_field.player1.y_velocity

            if key[pygame.K_a]:
                Battle_field.player1.x -= Battle_field.player1.speed
                Battle_field.player1.x_velocity = Battle_field.player1.velocity
                Battle_field.player1.x_direction = "left"
            else:
                if shift_key:
                    if Battle_field.player1.x_direction == "left":
                        Battle_field.player1.x -= Battle_field.player1.x_velocity

            if key[pygame.K_d]:
                Battle_field.player1.x += Battle_field.player1.speed 
                Battle_field.player1.x_velocity = Battle_field.player1.velocity
                Battle_field.player1.x_direction = "right"
            else:
                if shift_key:
                    if Battle_field.player1.x_direction == "right":
                        Battle_field.player1.x += Battle_field.player1.x_velocity

            Battle_field.player1.x_velocity = max(0,Battle_field.player1.x_velocity-.02)
            Battle_field.player1.y_velocity = max(0,Battle_field.player1.y_velocity-.02)
           # print(Battle_field.player1.x_velocity)
            
    class Disc():
        def __init__(self,x,y,radius,width):
            self.x = x
            self.y = y
            self.click_position = (0,0)
            self.throw_speed = 2
            self.throw_time = 0 
            self.radius = radius 
            self.width = width 
            self.surface = pygame.Surface((self.radius,self.radius),pygame.SRCALPHA)
            self.rect = self.surface.get_rect()
        
        
        def draw_disc():
            mouse_pos = pygame.mouse.get_pos()

 
            if pygame.mouse.get_pressed()[0]:
                Battle_field.player1_disc.click_position = pygame.mouse.get_pos()

            dx = Battle_field.player1.x - Battle_field.player1_disc.click_position[0] 
            dy = Battle_field.player1.y - Battle_field.player1_disc.click_position[1]

            dis = math.hypot(dx,dy)
            
            dx /= dis
            dy /= dis

            Battle_field.player1_disc.x -= dx * Battle_field.player1_disc.throw_speed
            Battle_field.player1_disc.y -= dy * Battle_field.player1_disc.throw_speed


            
            pygame.draw.circle(screen,(137,204,255),(Battle_field.player1_disc.x,Battle_field.player1_disc.y),Battle_field.player1_disc.radius,Battle_field.player1_disc.width)

                










    player1 = Player(420,400,25,25,(255,255,255),2)
    player1_disc = Disc(player1.x,player1.y,7,2)
    
# Set up the main loop
running = True
while running:
    fps = 120
    clock.tick(fps)
    screen.fill((0,0,0))

    pygame.draw.rect(screen,(255,255,255),(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],5,5),1)
    
    if Game_state == "Main_menu":
        Main_menu.display_main_menu()
    
    if Game_state == "Practice":
        Battle_field.draw_battle_field()
        Battle_field.Player.draw_player()
        Battle_field.Player.move_player()
        Battle_field.Disc.draw_disc()
    
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
