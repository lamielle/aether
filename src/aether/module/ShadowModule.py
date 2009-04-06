'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame, pygame.font
from pygame.locals import *

class ShadowModule(AetherModule):

	#Chains this module needs
	chains={'shadow':'ShadowPolyChain'}

	def __init__(self) :
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,self.dims)
		pygame.font.init()
		self.debug_print("Font initialized: "+str(pygame.font.get_init()))
		self.font = pygame.font.Font(None, 36)
		self.min_area_pos = (2,0)
		self.thresh_pos = (0,self.dims[1]-38)

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#curr_frame=self.shadow.get_frame()
		polys=self.shadow.read()

		if not self.settings.perspective.calibrated :
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.dims),5) # this helps opencv find the checkerboard
		else :
			screen.fill((0,0,55,255))
			for p in polys :
				if len(p) > 2 :
					pygame.draw.lines(screen,(255,100,100),1,p,2)

			text = self.font.render("Min. Poly Area: %d"%self.shadow.min_area, 1, (250,250,250))
			screen.blit(text,self.min_area_pos)

			text = self.font.render("Threshold: %d"%self.settings.threshold.threshold, 1, (250,250,250))
			screen.blit(text,self.thresh_pos)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_i :
				self.settings.threshold.threshold += 1
				return True
			elif event.key == K_k :
				self.settings.threshold.threshold -= 1
				return True
			elif event.key == K_o :
				self.settings.shadow.min_area += 100
				return True
			elif event.key == K_l :
				self.settings.shadow.min_area -= 100
				return True
		return False
