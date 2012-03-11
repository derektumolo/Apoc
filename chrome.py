import pygame

class Chrome(pygame.sprite.Sprite):
	# this group will hold the various ui elements
	def generate(self):
		pygame.sprite.Group.__init__(self)

class SideBar(pygame.sprite.Group):
	def generate(self):
		pygame.sprite.Group.__init__(self)