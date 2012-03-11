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

	# trying to separate some of this stuff out so its not one giant file
	import chrome
	import maps
	import units
	
except ImportError, err:
	print "couldn't load module. %s" % (err)
	sys.exit(2)
		
# this stuff is staying in here until i actually implement it
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
		
		
# leaving these here until I figure out where I want to keep them
# i don't think this is a terribly good implementation		
class Highlight(pygame.sprite.Sprite):
	# the idea is that we move the selection window, rather than attempting to do the highlight on the unit.
	# probably will need to change this later.
	
	def __init__(self, x=0, y=0):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.surface.Surface((38, 38))
		self.image.fill((54, 47, 200))
		
		self.owner = []
		self.x = x
		self.y = y
		self.rect = pygame.Rect(x*32-3,y*32-3,38,38)
		
	def move(self,x,y):
		self.rect = pygame.Rect(x*32-3, y*32-3, 38,38) #prob inefficient
		self.x = x
		self.y = y
		
	def draw(self, surface):
		surface.blit(self.image, self.rect)

class Player:
	# a class that will be superclassed or subclassed to handle AI as well
	# for now it holds some game state type data that we don't really have a place fore

	def __init__(self):
		self.selection = None # the selected unit
		self.highlight = Highlight(0,0)
		
	def select(self,unit):
		if self.selection:
			self.selection.deselect
		self.selection = unit
		self.selection.select()
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
	
def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Apocalypse')
	
	# Fill background (probably deprecated?)
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	
	# Initialise units
	global ug
	ug = units.UnitGroup() 
	ug.add(units.Unit())
	ug.add(units.Unit(2,4))
	
	global player
	player = Player()

	global map
	map = maps.Map(10) # 10 is the size, in tiles
	
	# Initialise sprites
	unitsprites = pygame.sprite.RenderPlain((ug))
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
					#print player.highlight.rect
					newselect = pygame.sprite.spritecollide(player.highlight, ug, False)
					print newselect
					if newselect != []:
						# we have clicked on a unit.  
						if newselect[0] == player.selection:
							# if we click on it again, we deselect
							player.selection.deselect()
							player.selection = []
						else:
							# drop the current one, and select a new one.
							player.select(newselect[0])
							#player.selection.highlight = player.highlight
					elif player.selection:
						player.selection.move(x, y)

		map.draw(screen)

		# prob wrong
		player.highlight.draw(screen)
				
		for u in ug:
			screen.blit(background, u.rect, u.rect)
		unitsprites.update()
		unitsprites.draw(screen)
		

					
		pygame.display.flip()

if __name__ == '__main__': main()