'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
import pygame
from pygame.locals import *

class Whiteboard(AetherModule):

	#Chains this module needs
	#chains={'camera':'PerspectiveChain'}
	#chains = {'laser':'DebugLaserPointerChain'}
	#chains = {'laser':'LaserPointerChain'}
	chains = {'laser':'LaserPointerSaviorChain'}

	def init(self):
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		#self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0]/2,self.dims[1]/2))
		self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0]-20,self.dims[1]))
		self.checkerboard.set_alpha(255)
		self.checkerboard.set_colorkey((100,100,100))
		self.doframe = False

		self.laser_sprite = LaserPointerSprite()

		self.curr_line = []
		self.lines = [self.curr_line]

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#curr_frame,curr_thresh,curr_red,pt=self.laser.read()
		pt = self.laser.read()

		if not self.settings.perspective.calibrated and not self.doframe:
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((5,0),self.checkerboard.get_size()),20)
		else :
			screen.fill((0,200,255)) # this is necessary for some reason
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
				self.laser_sprite.update(pt)
				screen.blit(self.laser_sprite.image,self.laser_sprite.rect.topleft)

				if self.laser_sprite.on :
					self.curr_line.append(self.laser_sprite.rect.topleft)
				else :
					self.curr_line = []
					self.lines.append(self.curr_line)

			#if self.laser_sprite.clicked :
			#	self.button.click()

			for l in self.lines :
				if len(l) > 1 :
					pygame.draw.aalines(screen,(0,100,255),False,l,2)

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

class LaserPointerSprite(pygame.sprite.Sprite) :

	DRAW,CURSOR = range(2)

	def __init__(self,tolerance=(100,100)) :
		pygame.sprite.Sprite.__init__(self)

		self.tolerance = tolerance

		self.image = pygame.Surface((10,10))
		self.image.set_colorkey((255,255,255))

		self.rect = self.image.get_rect()
		self.rect.topleft = (0,0)

		self.history = []
		self.history_size = 10

		self.on = False
		self.mode = LaserPointerSprite.CURSOR
		self.clicked = False

	def update(self,pt) :
		pt = pt[0]
		if len(self.history) == 0 or len([x for x in self.history if len(x) > 0]) == 0 :
			if len(self.history) == self.history_size :
				self.history.pop(0)
			self.history.append(pt)
		else :
			prev_hist = [x for x in self.history if len(x) != 0 ][-1]
			if len(pt) != 0 and \
		      abs(prev_hist[0] - pt[0]) < self.tolerance[0] and \
		      abs(prev_hist[1] - pt[1]) < self.tolerance[1] :
				if len(self.history) == self.history_size :
					self.history.pop(0)
				self.history.append(pt)

				self.rect.topleft = pt#[x for x in self.history if len(x) != 0 ][-1]

				inds = []
				in_seq = False
				curr_seq = []
				for v in self.history :
					if len(v) == 0 :
						if in_seq :
							inds.append(curr_seq)
							in_seq = False
					else :
						if not in_seq :
							curr_seq = [v]
							in_seq = True
						else :
							curr_seq.append(v)

				if len(curr_seq) != 0 :
					inds.append(curr_seq)

				if self.clicked :
					self.clicked = False

				# clicked, toggle graphic
				if len(inds) == 2 :
					self.clicked = True
					self.on = not self.on
					self.image.fill((255,255,255))
					if self.on :
						pygame.draw.circle(self.image,(255,0,0),(5,5),5,1)
					else :
						pygame.draw.rect(self.image,(0,0,0,0),(0,0,10,10),1)
					self.history = []
			else :

				if len(self.history) == self.history_size :
					self.history.pop(0)
				self.history.append([])
			#print self.history

