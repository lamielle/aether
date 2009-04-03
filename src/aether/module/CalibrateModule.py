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

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		curr_frame=self.camera.read()
		if not self.settings.perspective.calibrated :
			self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.dims),5)
		else :
			screen.fill((0,0,55,255))
			screen.blit(curr_frame,(0,0))

	def process_event(self,event) :
		if event.type == KEYDOWN and event.key == K_r :
			self.settings.perspective.calibrated = False
			return True
		return False
