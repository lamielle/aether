import pygame, pygame.key
from pygame.color import THECOLORS
from pygame.locals import *
from aether.core import AetherParamModule
from aether.util.padlib import particle_system

import math
from random import randint

class ParticleModule(AetherParamModule) :
	""" Simple Module illustrating things that can be done with the hull obtained from a DiffProvider.
	"""

	def __init__(self, driver, num_peepers=10, **kwargs) :
		AetherParamModule.__init__(self,driver,**kwargs)
	 
		#Define some parameters - see below
		#positions = [(50,50),(100,50),(150,50)]
		positions = [(x,-10) for x in range(10,self.dims[0],120)]
		colors = [(x,x,0) for x in range(0,200,150)] #[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(0,0,0)]
		speeds = [1,4]
		disperse = 360
		direction = 0
		density = 8
		framestolast = 200
		#Make the particle system objects
		self.systems = []
		for position in positions :
			self.systems.append(particle_system(position,colors,speeds,disperse,direction,density,framestolast))
			self.systems[-1].set_gravity((0,0.1))

	def draw(self,screen) :
		screen.fill((200,200,255,255))
		#pos = pygame.mouse.get_pos()
	
		# draw the shadow
		#shadow_pts = self.input.verts()
		#shadow_rect = None
		#if len(shadow_pts) > 2 : shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
		#for pt in shadow_pts :
		#	pygame.draw.circle(screen,THECOLORS["red"],pt,3)

		# draw the different polygons
		shadow_polys = self.input.polys()
		shadow_rects = []
		for p in shadow_polys :
			shadow_rects.append(pygame.draw.polygon(screen,THECOLORS["gray"],p))
			for pt in p :
				pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)


		# draw the avgd center
		#pygame.draw.circle(screen,THECOLORS["white"],pos,5)

		#Get the mouse position
		mpos = pygame.mouse.get_pos()
		#Change the Particle System origin to the mouse position*
		#self.p1.change_position(mpos)
		#Update all of the particles.
		for s in self.systems :
			if shadow_rects is not None :
				s.set_occluders(shadow_rects)
			else :
				s.set_occluders([])
			s.update()
			s.draw(screen)
	
	def process_event(self,event) :
		if event.type == KEYDOWN and event.key == K_r :
			self.build_some_peepers()
			return True
		return False

