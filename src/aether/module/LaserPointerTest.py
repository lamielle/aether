'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame
from pygame.locals import *

class LaserPointerTest(AetherModule):

	#Chains this module needs
	#chains={'camera':'PerspectiveChain'}
	#chains = {'laser':'DebugLaserPointerChain'}
	#chains = {'laser':'LaserPointerChain'}
	chains = {'laser':'LaserPointerSaviorChain'}

	def __init__(self) :
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		#self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0]/2,self.dims[1]/2))
		self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0],self.dims[1]))
		self.checkerboard.set_alpha(255)
		self.checkerboard.set_colorkey((100,100,100))
		self.doframe = False

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#curr_frame,curr_thresh,curr_red,pt=self.laser.read()
		pt = self.laser.read()

		if not self.settings.perspective.calibrated and not self.doframe:
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.checkerboard.get_size()),20)
		else :
			screen.fill((255,255,255)) # this is necessary for some reason
			# draw the raw capture
			#curr_frame = pygame.transform.scale(curr_frame,(self.dims[0]/2,self.dims[1]/2))
			#screen.blit(curr_frame,(self.dims[0]/2,self.dims[1]/2))

			# draw the red channel
			#curr_red = pygame.transform.scale(curr_red,(self.dims[0]/2,self.dims[1]/2))
			#screen.blit(curr_red,(self.dims[0]/2,0))

			# draw the thresholded image
			#curr_thresh = pygame.transform.scale(curr_thresh,(self.dims[0]/2,self.dims[1]/2))
			#screen.blit(curr_thresh,(0,self.dims[1]/2))

			# draw the polygons of the capture points
			if len(pt) != 0 :
				pygame.draw.rect(screen,(0,0,0),pygame.Rect(pt[0],(5,5)),1)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_u :
				self.doframe = not self.doframe
				return True
			elif event.key == K_i :
				self.settings.thresh.thresholds[0] += 1
				self.debug_print(self.settings.thresh.thresholds)
				return True
			elif event.key == K_k :
				self.settings.thresh.thresholds[0] -= 1
				self.debug_print(self.settings.thresh.thresholds)
				return True

		return False
