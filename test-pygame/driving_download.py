# importing required library
import pygame

# activate the pygame library .
pygame.init()
X = 600
Y = 600

scrn = pygame.display.set_mode((X, Y))

pygame.display.set_caption('image')

scrn.fill((150,150,150))

img = pygame.transform.smoothscale(pygame.image.load("sprite_01.png").convert_alpha(),(100,100))
img_rect = img.get_rect(center=(300,300))



scrn.blit(img, img_rect)

# paint screen one time
pygame.display.flip()

status = True
while (status):

# iterate over the list of Event objects
# that was returned by pygame.event.get() method.
	for i in pygame.event.get():

		# if event object type is QUIT
		# then quitting the pygame
		# and program both.
		if i.type == pygame.QUIT:
			status = False

# deactivates the pygame library
pygame.quit()



