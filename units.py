import pygame
import spritesheet

class UnitGroup(pygame.sprite.Group):
	# sort of like a unit factory? 
	def __init__(self):
		pygame.sprite.Group.__init__(self)

class Unit(pygame.sprite.Sprite):
	# basically, a sprite.  Anything that is mobile.
	
	# type - this will be where we get the image path from, and some defaults for the init fctn
	
	# APAvail
	# MaxAP
	
	# current orders? I think for now, the order is executed as the player requests it
	# so no rollback, but all that is done at EOT is to reset action points, and run the NPC orders
	
	# hp?
	
	# skills = skills() - i think we'll have a different class for the skills? maybe a map/hash
	# then we can do things like Bob.skills.salvage++
	
	# stats - like skills above, there are several of these attributes, which can be adjusted up or down

	# equipment - just a resource, attached to a particular body part.
	# inventory

	# contamination?
	
	# loyalty?

	def __init__(self, x=0, y=0, name="Smiley"):
		pygame.sprite.Sprite.__init__(self)
		ss = spritesheet.spritesheet('img/asprite.bmp')
		self.image = ss.image_at((0,0,32,32), -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
#		self.speed = 10
		self.owner = []
		self.x = x
		self.y = y
		self.name = name
		self.rect = pygame.Rect(x*32,y*32,32,32)
		
		self.selected = False
		
#		self.highlight = []
		
	def move(self,x,y):
		if self.selected:
			self.rect = pygame.Rect(x*32, y*32, 32,32)
			self.x = x
			self.y = y

#			self.highlight.move(x,y) # move the highlight with the unit
			#later, we will check distances and things
		else:
			print "ERROR - moving unselected unit."
			# TODO - make this real error handling
		
	# not sure if I will actually need these
	def select(self):
		self.selected = True
#		self.highlight = Highlight(self.x, self.y)
		
	def deselect(self):
		self.selected = False
#		self.highlight = []
		
	def update(self):
		pygame.event.pump()
		
	def draw(self, surface):
		print "drawing units"
#		if self.selected:
#			self.highlight.draw(surface)
