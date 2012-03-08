#!/usr/bin/python

try:
	import sys
	import random
	import math
	import numbers
	import os
	import getopt
	import pygame
	from socket import *
	from pygame.locals import *
	import spritesheet	
	
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)

# fancy functional programming stuff to build a map.  deprecated
def mapRow(x):
	return map(pickTileType,x)
def pickTileType(x):
	return Tile(random.choice(TileTypesList))
	
	
class Map(pygame.sprite.Sprite):
	# TODO
	# params for building a map
	# more complicated distribution of tile types
	
	# render function, which sequentially calls tile.render for each tile?
	# update function?
	
	def __init__(self, size):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.size = size
		self.rect = (size*32, size*32)
		self.generate()

	def generate(self):
		# this is the functional stuff.  I couldnt get it to build x,y positions as it created the tiles
		# and it was less readable.
#		array = [x[:] for x in [[0]*self.size]*self.size]
#		self.tiles = map(mapRow, array)
		
		self.tiles = []
		column = []
		
		for x in range(self.size):
			for y in range(self.size):
				column.append(Tile(random.choice(TileTypesList),x,y))
			self.tiles.append(column)
			column = []
			
	def draw(self, surface):
		for row in self.tiles:
			for tile in row:
				surface.blit(bgTile, tile.rect)
				#TODO - fix this so its at least somewhat efficient
				surface.blit(tile.image,tile.rect)
		

class Tile(pygame.sprite.Sprite):
	# an individual tile in the map
	# x,y
	
	# resources stored
	
	# buildings present? this might be subsumed in tile type
	
	# units present will be stored at the unit level? or both? might be efficient to have both.
	
	# generation function for map can call generate on each tile? then we can get some game of life
	# complexity type stuff where it checks the neighboring tiles.
	
	# tile.work()? or unit.work(tile)? i think unit.  
	def __init__(self, tileType, x, y):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.tileType = tileType
		self.image = tileType.image
		self.rect = (x*32, y*32, 32, 32)
	
class TileType:
	# Name
	# Desc
	# work types avail. - theres another class - a dictionary of flags? this is like a flywheel?
	# we want to be able to easily add a new work type without hacking apart all the tile code
	
	def __init__(self, name, workAvail, image):
		self.name = name
		self.WorkAvail = workAvail
		self.image = image
	
class Work:
	# these should probably be in a dictionary, with name as the key
	def __init__(Name, APCost, ResourceCosts, Products):
		self.name = Name
		self.APCost = APCost
		self.ResourceCosts = ResourceCosts
		self.Products = Products
		# ResourceCost [ResourceType,Amount]
		# Product [ResourceType, Amount]
		# NewTileType
		# NewBuilding
	
class Building:
	# Name
	# Desc
	# hp?
	# Work Types avail
	
	def __init__():
		self.type = 0
	
class Resource:
	# Name
	# Desc
	
	# might be nice to have a list of Work that you can use it for, but I don't know the right way to do that
	# and that is more a nice to have.
	
	def __init__():
		self.type = 0
	
class Item:
	# not sure we will need this distinct from resource
	# but the cardinality here is different
	# these will be mainly small or unique runs, not big piles
	
	# Name
	# Desc
	# Type - maybe each individual item references a resource? come back to this.
	
	def __init__():
		self.type = 0

class UnitGroup(pygame.sprite.Group):
	def __init__():
		pass

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

	def __init__(self, side, x=0, y=0):
		pygame.sprite.Sprite.__init__(self)
		ss = spritesheet.spritesheet('img/asprite.bmp')
		self.image = ss.image_at((0,0,32,32), -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
#		self.speed = 10
		self.owner = []
		self.x = x
		self.y = y
		self.rect = (x*32,y*32,32,32)
		
		self.selected = False
		
		self.highlight = []
		
	def move(self,x,y):
		if self.selected:
			self.rect = (x*32, y*32, 32,32)
			self.x = x
			self.y = y

			self.highlight.move(x,y) # move the highlight with the unit
			#later, we will check distances and things
		else:
			print "ERROR - moving unselected unit."
			# TODO - make this real error handling
		
	# not sure if I will actually need these
	def select(self):
		self.selected = True
		self.highlight = Highlight(self.x, self.y)
		
	def deselect(self):
		self.selected = False
		self.highlight = []
		
	def update(self):
		pygame.event.pump()
		
	def draw(self, surface):
		print "drawing units"
		if self.selected:
			self.highlight.draw(surface)
		
class Highlight(pygame.sprite.Sprite):
	# the idea is that we move the selection window, rather than attempting to do the highlight on the unit.
	# probably will need to change this later.
	
	def __init__(self, x=0, y=0):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = ss.image_at((0,0,32,32), -1)
		screen = pygame.display.get_surface()
#		self.speed = 10
		self.owner = []
		self.x = x
		self.y = y
		self.rect = (x*32,y*32,34,34)
		
	def move(self,x,y):
		self.rect = (x*32, y*32, 34,34)
		self.x = x
		self.y = y
		
	def draw(self, surface):
		print "drawing highlight"

class Player:
	# a class that will be superclassed or subclassed to handle AI as well
	# for now it holds some game state type data that we don't really have a place fore

	def __init__(self):
		self.selection = [] # the selected unit
		self.highlight = Highlight(0,0)
		
	def select(unit):
		self.selection = unit
# Turns
	# user will have an action to end their turn
	# this iterates through the list of units, and resets their AP to max
	
# The game loop - I think its mostly going to be sprite idle animations, and input capture
	# detect clicks, and switch to a unit highlighted state for that sprite or tile
	# if a unit is already selected, the click behavior changes
		# right click presents the orders menu
			# left clicking on an order, which will also include cancel, moves the unit to the specified tile
			# and executes the order.
			
			# each order will indicate the movement AP cost, as well as the action AP cost, the total, 
			# and the amount remaining
			
		# left clicking behavior isn't actually that different - first it deselects the current unit/tile
		# then selects the new one
	
# the screen itself
	# most of the screen is the map
	# a side or bottom bar has other stuff
	# mini map, eventually
	# selected unit details
	# overall details
	# main menu button
	
# loading up the data after the classes are all set up

# refactor this so its part of the ss class? maybe?
def tileImg(ss,x,y):
	return ss.image_at((x*32, y*32, 32, 32),(0,0,0))

def loadTiles():
	ss = spritesheet.spritesheet('img/tiles.png')
	TileTypesData = [
		("wasteland", ["clean", "salvage", "housing", "factory"], tileImg(ss,4,9)),
		("plains", ["farm", "housing", "factory"],tileImg(ss,1,1)),
		("lake", ["fish", "water"],tileImg(ss,3,7)),
		("forest", ["chop", "hunt"],tileImg(ss,6,1))
	]
	
	global bgTile
	bgTile = tileImg(ss,4,9)

	global TileTypesList 
	TileTypesList = [TileType(name, workAvailKeys, image) for name, workAvailKeys, image in TileTypesData]
	
def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Apocalypse')
	
	# load up tiles, later, more initialization and data stuff.
	loadTiles()
	
	# Fill background (probably deprecated?)
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	
	# Initialise units
	global units
	units = UnitGroup() 
	units.add(Unit("left"))
	
	global player
	player = Player()

	global map
	map = Map(10) # 10 is the size, in tiles
	
	# Initialise sprites
	unitsprites = pygame.sprite.RenderPlain((units))
	mapsprites = pygame.sprite.RenderPlain(map)
	
	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	# Initialise clock
	clock = pygame.time.Clock()

	while 1:
	# Make sure game doesn't run at more than 60 frames per second
		clock.tick(60)

		# no events are used, but the remnant pong behavior is still there for ref.
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_a:
					pass
			elif event.type == MOUSEBUTTONDOWN:
				x = event.pos[0]/32
				y = event.pos[1]/32
				if event.button == 1:
					# detect collision with a unit, and select it, first deselecting the current
					player.highlight.move(x,y)
					if 
					elif player.selection:
						if player.selection.x = x and player.selection.y = y:
							# clicking a unit again deselects that unit
							player.selection.deselect()
							player.selection = []
						else:
							player.selection.move((event.pos[0]/32), (event.pos[1]/32))
		
		map.draw(screen)

		screen.blit(background, player1.rect, player1.rect)
		playersprites.update()
		playersprites.draw(screen)
					
		pygame.display.flip()

if __name__ == '__main__': main()