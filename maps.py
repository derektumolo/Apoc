import pygame
import random
import spritesheet
# there should be a way for me to do this so i dont need it in every module?

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
		self.loadTiles()
		self.generate()

	def generate(self):
		# passing tiletypeslist seems ugly.  later probably want that as an attribute of the map?
		
		self.tiles = []
		column = []
		
		for x in range(self.size):
			for y in range(self.size):
				column.append(Tile(random.choice(self.TileTypesList),x,y))
			self.tiles.append(column)
			column = []
			
	def loadTiles(self):
		ss = spritesheet.spritesheet('img/tiles.png')
		TileTypesData = [
			("wasteland", ["clean", "salvage", "housing", "factory"], ss.tileImg(4,9)),
			("plains", ["farm", "housing", "factory"], ss.tileImg(1,1)),
			("lake", ["fish", "water"], ss.tileImg(3,7)),
			("forest", ["chop", "hunt"], ss.tileImg(6,1))
		]

		self.bgTile = ss.tileImg(4,9)

		self.TileTypesList = [TileType(name, workAvailKeys, image) for name, workAvailKeys, image in TileTypesData]
			
	def draw(self, surface):
		for row in self.tiles:
			for tile in row:
				surface.blit(self.bgTile, tile.rect)
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
		self.rect = pygame.Rect(x*32, y*32, 32, 32)
	
class TileType:
	# Name
	# Desc
	# work types avail. - theres another class - a dictionary of flags? this is like a flywheel?
	# we want to be able to easily add a new work type without hacking apart all the tile code
	
	def __init__(self, name, workAvail, image):
		self.name = name
		self.WorkAvail = workAvail
		self.image = image
