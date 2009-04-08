'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame
from pygame.locals import *

class Whiteboard(AetherModule):

	#Chains this module needs
	chains={'input':'LaserPointerChain'}

	def init(self):
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,self.dims)
		self.show_capture = False

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		curr_frame=self.input.read()
		if not self.settings.perspective.calibrated :
			self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
		else :
			screen.fill((0,0,55,255))

			if self.show_capture :
				print 'showing capture'
				screen.blit(curr_frame,(0,0))

			print self.input.get_points()

	def process_event(self,event) :
		if event.type == KEYDOWN :
			print event.key
			if event.key == K_r :
				self.settings.perspective.calibrated = False
			elif event.key == K_u :
				self.show_capture = True
			return True
		return False
