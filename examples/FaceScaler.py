"""
This example uses the :class:FaceInputProvider class, which does Haar Cascade Face Detection to return the rectangular coordinates of where OpenCV thinks it sees a face.

:Version: 1.0 of 2/24/2009 00:33 in the AM
:Author: Adam Labadorf
"""
from aether.core import AetherDriver, FaceInputProvider, AetherModule

import pygame.image, pygame.draw, pygame.mouse
from pygame.color import THECOLORS
import pygame.transform
from pygame.locals import *

class FaceScaler(AetherModule) :

	def __init__(self,*args) :

		AetherModule.__init__(self,*args)
		#self.bg = pygame.image.load("/home/labadorf/Documents/backgrounds/img_1191.jpg")
		self.bg = pygame.image.load("/home/lamielle/pictures/jimmy_eat_world.jpg")

		#self.d = self.dims[0] # distance from screen to face, calibrated as width by default
		self.d = 800
		self.c = 800 # 'distance' between screen and background img
		self.w,self.h = self.dims[0],self.dims[1] # screen width

		# calibrate face scale factor
		face = self.input.get_verts()
		face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
		width, height = face[1][0]-face[0][0], face[2][1]-face[1][1]
		self.face_scale_factor = self.d/width

		# scale image, might not need this...
		r = self.d+self.c
		self.m_x = r - self.w
		self.m_y = r - self.h
		r_ratio = (2.*self.m_x+self.w)/self.bg.get_width()
		s_ratio = (2.*self.m_y+self.h)/self.bg.get_height()
		new_dims = self.bg.get_width()*s_ratio,self.bg.get_height()*s_ratio
		self.bg = pygame.transform.scale(self.bg,new_dims)
		

	def draw(self,screen) :

		vwpt = self.input.get_com()
		#vwpt = pygame.mouse.get_pos()

		if vwpt is not None :
			# calculate d
			face = self.input.get_verts()
			if face is not None :
				face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
				width, height = face[1][0]-face[0][0], face[2][1]-face[1][1]
				#rect = pygame.Rect(face[0][0],face[0][1],width,height)
				#pygame.draw.rect(screen,THECOLORS['red'],rect,0)
				self.d = width*self.face_scale_factor

			vwpt = int(vwpt[0]*self.dims[0]),int(vwpt[1]*self.dims[1])

			# figure out the x bounds
			r1 = (vwpt[0]*(self.d+self.c))/float(self.d)
			r2 = ((self.w-vwpt[0])*(self.d+self.c))/float(self.d)
			x1pr = (vwpt[0]+self.m_x)-r1
			x2pr = x1pr+r1+r2

			# figure out the y bounds
			s1 = (vwpt[1]*(self.d+self.c))/float(self.d)
			s2 = ((self.w-vwpt[1])*(self.d+self.c))/float(self.d)
			y1pr = (vwpt[1]+self.m_y)-s1
			y2pr = y1pr+s1+s2
			face = self.input.get_verts()

			vwpt_rect = pygame.Rect(x1pr,y1pr,r1+r2,s1+s2)
			try :
				vwpt_bg = self.bg.subsurface(vwpt_rect)
				screen.blit(vwpt_bg,(0,0))
			except Exception, e :
				screen.fill(THECOLORS['gray'])
				print e
			print vwpt_rect, self.bg.get_size()

			pygame.draw.circle(screen,THECOLORS['red'],vwpt,2,0)
			
	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_k :
				self.d += 100
			elif event.key == K_j :
				self.d -= 100

if __name__ == "__main__" :

	# initialize a FaceInputProvider that looks for faces from the camera image
	#face_input = FaceInputProvider("/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",image_dims=(240,180),flip=True)
	face_input = FaceInputProvider(0,(320,240),"/home/lamielle/aether/examples/haarcascade_frontalface_alt.xml",flip=False)

	# create the driver
	driver = AetherDriver(640,input=face_input)

	# register the module we just wrote
	mod = FaceScaler(driver)
	driver.register_module(mod)

	# go be a tiki god
	driver.run()
