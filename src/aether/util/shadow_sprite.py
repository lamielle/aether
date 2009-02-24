import pygame, pygame.key, pygame.sprite, pygame.surfarray
import pygame.mouse
from pygame.color import THECOLORS
import aether.core.input
import math

class Wall(pygame.sprite.Sprite) :

	def __init__(self,(p1,p2),height=2,draw=False) :
		pygame.sprite.Sprite.__init__(self)

		# calculate the vector for the height of the box
		dx = (p1[0]-p2[0])
		dy = (p1[1]-p2[1])
		norm = math.sqrt(dx**2 + dy**2)
		normal = (dx/norm,dy/norm)
		perp = (normal[1]*height,-normal[0]*height)

		self.normal = (normal[1],-normal[0])
		self.slope = normal

		# calculate the points
		self.s = [(p1[0]-perp[0],p1[1]-perp[1]),(p1[0]+perp[0],p1[1]+perp[1])]
		self.s.extend([(p2[0]+perp[0],p2[1]+perp[1]),(p2[0]-perp[0],p2[1]-perp[1])])

		# find the top left coordinate for the line
		self.pos = int(min([p[0] for p in self.s])),int(min([p[1] for p in self.s]))

		# shift all the points up to be in the rect
		self.s = [(p[0]-self.pos[0],p[1]-self.pos[1]) for p in self.s]

		# draw the polygon associated with the points
		self.image = pygame.Surface((int(abs(p1[0]-p2[0]))+5*height,int(abs(p1[1]-p2[1]))+5*height),pygame.SRCALPHA|pygame.HWSURFACE)
		self.image.set_colorkey((255,255,255,0))
		self.image.fill((255,255,255,0))

		self.rect = pygame.draw.polygon(self.image,(0,0,255),self.s)
		pygame.draw.line(self.image,(255,5,5),self.rect.center,(self.rect.center[0]+self.normal[0]*30,self.rect.center[1]+self.normal[1]*30),3)
		#self.rect = pygame.draw.rect(self.image,(0,0,0,255),self.rect,2)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos

		self.hitmask = pygame.surfarray.array_colorkey(self.image)
		self.image.unlock() # need this due to some bug in pygame		
		self.image.unlock()


	def __repr__(self) :
		return "Wall((%d,%d))"%(self.pos[0],self.pos[1])

class ShadowSprite(pygame.sprite.Sprite) :

	def __init__(self,driver,draw_polygon=False,draw_rects=False) :
		pygame.sprite.Sprite.__init__(self)

		self.driver = driver

		self.draw_polygon = draw_polygon
		self.draw_rects = draw_rects

		self.rect = pygame.Rect(0,0,driver.dims[0],driver.dims[1])
		self.image = pygame.Surface((driver.dims[0],driver.dims[1]),pygame.SRCALPHA|pygame.HWSURFACE)
		self.image.set_colorkey((255,255,255))

		# holds edge box sprites that define contour
		self.edges = pygame.sprite.Group()

		# for collision detection
		self.hitmask = pygame.surfarray.array_alpha(self.image)

	def draw_update(self,screen) :
		self.update()
		self.draw(screen)

	def draw(self,screen) :
		screen.blit(self.image,(0,0))

	def update(self) :
		pts = self.driver.input.verts()
		self.image.fill((255,255,255,0))

		if self.draw_polygon :
			if len(pts) > 2 : pygame.draw.polygon(self.image,THECOLORS["gray"],pts)
			for pt in pts :
				pygame.draw.circle(self.image,THECOLORS["red"],tuple((int(i) for i in pt)),3)

		self.edges.empty()
		npoints = len(pts)
		pts += [pts[0]]

		for i in range(npoints) :
			self.edges.add(Wall((pts[i],pts[i+1])))

		if self.draw_rects :
			self.edges.draw(self.image)
