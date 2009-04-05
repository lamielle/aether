'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame
from pygame.locals import *

class CalibrateModule(AetherModule):

	#Chains this module needs
	chains={'camera':'PerspectiveChain'}

	def __init__(self) :
		self.checkerboard = pygame.image.load(self.file_path('checkerboard2.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,self.dims)
		self.doframe = False

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		curr_frame=self.camera.read()

		if not self.settings.perspective.calibrated and not self.doframe:
			self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.dims),5)
		else :
			screen.fill((0,0,55,255))
			screen.blit(curr_frame,(0,0))

		self.grid = (7,7)
		grid_x = self.dims[0]/(self.grid[0]+1)
		grid_y = self.dims[1]/(self.grid[1]+1)
		self.dest = []
		for i in range(1,self.grid[0]+1) :
			for j in range(1,self.grid[1]+1) :
				if i == 1 and j == 1 :
					pygame.draw.circle(screen,(255,255,255),(j*grid_x,i*grid_y),2,0)
				pygame.draw.circle(screen,(0,0,0),(j*grid_x,i*grid_y),3,2)
				self.dest.append((j*grid_x,i*grid_y))

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_u :
				self.doframe = not self.doframe
				return True
		return False
