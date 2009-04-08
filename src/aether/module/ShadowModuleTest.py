'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame
from pygame.locals import *

class ShadowModuleTest(AetherModule):

	#Chains this module needs
	#chains = {'shadow':'DebugShadowPolyChain'}
	chains = {'shadow':'ShadowPolySaviorChain'}

	def __init__(self) :
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0]/2-10,self.dims[1]/2-10))
		#self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0],self.dims[1]))
		self.doframe = False

		self.settings.perspective.calibrated = False

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		polys = self.shadow.read()
		curr_frame,curr_thresh = self.shadow.raw_frame_surface, self.shadow.thresh_frame_surface

		screen.fill((255,255,255)) # this is necessary for some reason
		# draw the raw capture
		curr_frame = pygame.transform.scale(curr_frame,(self.dims[0]/2,self.dims[1]/2))
		screen.blit(curr_frame,(0,0))

		if not self.settings.perspective.calibrated and not self.doframe:
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			#screen.blit(self.checkerboard,(0,0))
			screen.blit(self.checkerboard,(self.dims[0]/2,self.dims[1]/2))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((self.dims[0]/2,self.dims[1]/2),self.checkerboard.get_size()),15)
		else :

			# draw the thresholded image
			curr_thresh = pygame.transform.scale(curr_thresh,(self.dims[0]/2,0))
			screen.blit(curr_thresh,(0,self.dims[1]/2))

			# draw a black box
			pygame.draw.rect(screen,(0,0,0),pygame.Rect((self.dims[0]/2+30,self.dims[1]/2+30),(30,20)),0)
			# draw the polygons of the capture points
			for p in polys :
				if len(p) > 2 :
					pygame.draw.polygon(screen,(255,0,0),p,1)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_u :
				self.doframe = not self.doframe
				return True
			elif event.key == K_i :
				self.settings.threshold.thresholds[0] += 1
				self.debug_print(self.settings.threshold.thresholds)
				return True
			elif event.key == K_k :
				self.settings.threshold.thresholds[0] -= 1
				self.debug_print(self.settings.threshold.thresholds)
				return True

		return False
