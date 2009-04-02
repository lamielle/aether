from aether.core import AetherDriver, AetherModule, MouseInputProvider, LazerPointerProvider
from aether.modules import PymunkModule
from pygame.color import THECOLORS
from pygame.locals import *
import pygame.event, pygame.draw, pygame.transform, pygame.image
import time

# get rid of this when you're done
from opencv import cv
from opencv.cv import CV_THRESH_BINARY, CV_THRESH_TOZERO

class Whiteboard(AetherModule) :

	def __init__(self,driver,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,driver,*args)
		self.blink_phase = 0
		#self.pointer_sprite = LaserPointerSprite()

		#self.button = ButtonSprite()

		self.curr_line = []
		self.lines = [self.curr_line]

		self.lazer = LazerPointerProvider(0,(480,360))

		self.is_calibrated = False

	def draw(self,screen) :

		if not self.is_calibrated :
			screen.fill(THECOLORS["white"])
			checkerboard = pygame.image.load('checkerboard.png')
			checkerboard = pygame.transform.scale(checkerboard,self.dims)
			screen.blit(checkerboard,(0,0))
			pygame.display.flip()
			corners = self.lazer._calibrate_camera()
			self.is_calibrated = True
		else :
			#frame = self.lazer.get_curr_frame()
			#screen.blit(frame,(0,0))
			pass

			"""
			pt = self.input.get_com()
			if pt is None : pt = (0,0)
			if self.blink_phase == 0 :
				self.pointer_sprite.update(pt)
			else :
				self.blink_phase -= 1
				self.pointer_sprite.update(None)

			if self.pointer_sprite.on :
				self.curr_line.append(pt)
			else :
				self.curr_line = []
				self.lines.append(self.curr_line)

			if self.pointer_sprite.clicked :
				self.button.click()

			for l in self.lines :
				if len(l) > 1 :
					pygame.draw.aalines(screen,THECOLORS["black"],False,l,1)
			"""

			# don't try this at home, kids
			frame = self.lazer._get_cv_frame()
			thresh = 248
			red = self.lazer._get_color_frame('r',frame)
			cvpt_min = cv.cvPoint(0,0)
			cvpt_max = cv.cvPoint(0,0)
			t = cv.cvMinMaxLoc(red,cvpt_min,cvpt_max)
			#print t,cvpt_min,cvpt_max

			#red = self.lazer._get_scaled_frame(red)
			#red = self.lazer._get_threshold_frame(frame=red,thresh=thresh,type=CV_THRESH_BINARY)

			blue = self.lazer._get_color_frame('b',frame)
			#blue = self.lazer._get_threshold_frame(frame=blue,thresh=thresh,type=CV_THRESH_BINARY)
			blue = self.lazer._cv_to_pygame(blue,channel=2)
			blue = pygame.transform.scale(blue,(self.dims[0]/2,self.dims[1]/2))

			green = self.lazer._get_color_frame('g',frame)
			#green = self.lazer._get_threshold_frame(frame=green,thresh=thresh,type=CV_THRESH_BINARY)
			green = self.lazer._cv_to_pygame(green,channel=1)
			green = pygame.transform.scale(green,(self.dims[0]/2,self.dims[1]/2))

			value = self.lazer._get_hsv_frame(frame)
			value = self.lazer._get_frame_channel(value,2)
			value = self.lazer._get_shifted_frame(-215,value)
			#value = self.lazer._get_threshold_frame(frame=value,thresh=thresh,type=CV_THRESH_BINARY)

			comb = self.lazer._multiply_frames(red,value)
			comb = self.lazer._cv_to_pygame(comb,channel=5)
			comb = pygame.transform.scale(comb,(self.dims[0]/2,self.dims[1]/2))

			red = self.lazer._cv_to_pygame(red,channel=0)
			red = pygame.transform.scale(red,(self.dims[0]/2,self.dims[1]/2))

			value = self.lazer._cv_to_pygame(value,channel=-1)
			value = pygame.transform.scale(value,(self.dims[0]/2,self.dims[1]/2))

			#frame = self.lazer.get_curr_frame()
			frame = self.lazer._cv_to_pygame(frame)
			frame = pygame.transform.scale(frame,(self.dims[0]/2,self.dims[1]/2))

			screen.blit(red,(0,0))
			screen.blit(blue,(self.dims[0]/2,0))
			screen.blit(green,(0,self.dims[1]/2))
			screen.blit(frame,(self.dims[0]/2,self.dims[1]/2))

			screen.fill((100,100,100,255))

			if t[1] >= 0 :
				pygame.draw.circle(screen,THECOLORS["red"],(cvpt_max.x,cvpt_max.y),5,1)
				pygame.draw.circle(screen,THECOLORS["white"],(cvpt_max.x,cvpt_max.y),3,0)

			#screen.blit(frame,(0,0))
			#screen.blit(self.button.image,(30,30))
			#screen.blit(self.pointer_sprite.image,pt)
			#print screen.get_at(pt)

	def process_event(self, event) :
		if event.type == KEYDOWN and event.key == K_b :
			self.blink_phase = 3
			return True
		return False

class ButtonSprite(pygame.sprite.Sprite) :
	
	def __init__(self) :
		pygame.sprite.Sprite.__init__(self)

		self.dims = (45,18)
		self.image = pygame.Surface(self.dims)
		self.image.fill(THECOLORS["white"])
		pygame.draw.rect(self.image,THECOLORS["black"],pygame.Rect((0,0),self.dims),2)

		self.clicked = False

	def click(self) :
		self.clicked = not self.clicked

	def update(self) :
		if self.clicked :
			self.image.fill(THECOLORS["red"])
		else : 
			self.image.fill(THECOLORS["white"])
		pygame.draw.rect(self.image,THECOLORS["black"],pygame.Rect((0,0),self.dims),2)

class LaserPointerSprite(pygame.sprite.Sprite) :

	DRAW,CURSOR = range(2)

	def __init__(self) :
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((10,10))
		self.image.set_colorkey(THECOLORS["white"])

		self.history = []
		self.history_size = 10

		self.on = False
		self.mode = LaserPointerSprite.CURSOR
		self.clicked = False

	def update(self,pt) :
		if len(self.history) == self.history_size :
			self.history.pop(0)
		self.history.append(pt)

		inds = []
		in_seq = False
		curr_seq = []
		for v in self.history :
			if v is None :
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
			self.image.fill(THECOLORS["white"])
			if self.on :
				pygame.draw.circle(self.image,THECOLORS["red"],(5,5),5,1)
			else :
				pygame.draw.rect(self.image,THECOLORS["black"],(0,0,10,10),1)
			self.history = []

if __name__ == "__main__" :
	mouse_input = MouseInputProvider()
	driver = AetherDriver(640,input=mouse_input)
	module = Whiteboard(driver)
	driver.register_module(module)
	driver.run()
