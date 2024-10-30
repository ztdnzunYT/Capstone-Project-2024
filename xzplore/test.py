'''
 class Enemy():

        animation_delay = 200
        time = 0 
        curr_time = pygame.time.get_ticks()
        
        def __init__(self,x,y,size,path,animations,speed,animation_delay):
            self.x = x
            self.y = y
            self.size = size
            self.path = path
            self.animations = animations
            self.image = os.path.normpath(os.path.join(self.path,self.animations[0]))
            self.surf = pygame.transform.smoothscale(pygame.image.load(self.image).convert_alpha(),(self.size,self.size))
            self.rect = self.surf.get_rect(topleft=(x,y))
            self.surface = pygame.Surface((200,200),pygame.SRCALPHA)
            self.speed = speed
            self.animation_num  = 0
            self.time = 0
            self.curr_time = 0
            self.animation_delay = animation_delay + random.randint(0,10)
      
        def draw(enemy):
   
            if len(Planet.enemy1) < 5:
                Planet.enemy1.append(Planet.Enemy(random.randint(0,300),0,100,enemy["path"],enemy["animations"],random.randint(1,5),100))

            for enemy in Planet.enemy1:
                #enemy.rect.x += 1
                screen.blit(enemy.surf,(enemy.rect.x+Planet.Tile.world_x,enemy.rect.y+Planet.Tile.world_y))
 
        def update(curr_time):
            
           
            for enemy in Planet.enemy1:
                enemy.curr_time = curr_time
                
                if enemy.animation_num >= len(enemy.animations):
                    enemy.animation_num = 0

                enemy.surf = pygame.transform.smoothscale(pygame.image.load(os.path.join(enemy.path,enemy.animations[enemy.animation_num])).convert_alpha(),(enemy.size,enemy.size))

                if enemy.curr_time > enemy.time + enemy.animation_delay:
                    enemy.animation_num +=1 
                    enemy.time = enemy.curr_time
            '''
