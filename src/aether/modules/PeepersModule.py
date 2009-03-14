import pygame, pygame.key
from pygame.color import THECOLORS
from pygame.locals import *
from aether.core import AetherParamModule
from aether.util import conv_to_int

import math
from random import randint

class PeepersModule(AetherParamModule) :
	""" Simple Module illustrating things that can be done with the hull obtained from a DiffProvider.
	"""

	def __init__(self, driver, num_peepers=10, **kwargs) :
		AetherParamModule.__init__(self,driver,**kwargs)
		self.num_peepers = num_peepers
		self.build_some_peepers()
		
	def build_some_peepers(self) :
		self.peepers = []
		for i in range(self.num_peepers) :
			collide = True
			# make sure none of the peepers overlap each other
			while collide :
				x,y,r = randint(30,self.dims[0]-30),randint(15,self.dims[1]/4),randint(10,20)
				peeper = Peeper(r,(x,y))
				collide = False
				for p in self.peepers :
					if peeper.rect.colliderect(p) :
						collide = True
			self.peepers.append(peeper)

	def get_avgd_shadow(self) :
		pts = self.input.verts()
		if len(pts) != 0 :
			avg = (0.0,0.0)
			for p in pts :
				avg = avg[0]+p[0],avg[1]+p[1]
			avg = avg[0]/len(pts),avg[1]/len(pts)
			return avg
		return (0,0)
		
	def draw(self,screen) :
		screen.fill((200,200,255,255))
		#pos = pygame.mouse.get_pos()
		pos = self.get_avgd_shadow()
		for p in self.peepers :
			p.look_at(pos,screen)

		# draw the shadow
		shadow_pts = self.input.verts()
		if len(shadow_pts) > 2 : pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
		for pt in shadow_pts :
			pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)

		# draw the avgd center
		pygame.draw.circle(screen,THECOLORS["white"],conv_to_int(pos),5)

		#screen = antialias(screen,2)
	
	def process_event(self,event) :
		if event.type == KEYDOWN and event.key == K_r :
			self.build_some_peepers()
			return True
		return False

class Peeper :
	
	def __init__(self, radius, origin=(0,0)) :
		self.radius = (radius)
		self.pupil_radius = (radius*0.6)
		self.origin = origin
		self.nose_width = (radius*0.2)
		self.pupil_size = (self.radius*0.3)
		self.rect = pygame.Rect(origin[0]-radius-self.nose_width,origin[1]-radius,4*radius+self.nose_width,2*radius)

		self.left_eye_pos = origin[0]-self.radius-(self.nose_width/2.), origin[1]
		self.right_eye_pos = origin[0]+self.radius+(self.nose_width/2.), origin[1]

	def look_at(self, pos, screen) :
		""" Look at the position pos, calculated relative to the peeper's origin.
		"""

		# origin-centered position
		vec = pos[0]-self.origin[0], pos[1]-self.origin[1]
		norm = math.sqrt(vec[0]**2+vec[1]**2)

		# if you get the mouse just right the norm is zero, fix it
		if norm < self.pupil_radius :
			left_pupil = self.left_eye_pos[0]-(vec[0]),self.left_eye_pos[1]+(vec[1])
			right_pupil = self.right_eye_pos[0]+(vec[0]),self.right_eye_pos[1]+(vec[1])
		else :
			if norm == 0 :
				norm = 0.001
			left_pupil = self.left_eye_pos[0]+self.pupil_radius*(vec[0]/norm),self.left_eye_pos[1]+self.pupil_radius*(vec[1]/norm)
			right_pupil = self.right_eye_pos[0]+self.pupil_radius*(vec[0]/norm),self.right_eye_pos[1]+self.pupil_radius*(vec[1]/norm)
		
		# right eye
		pygame.draw.circle(screen,THECOLORS["white"],conv_to_int(self.right_eye_pos),self.radius,0)
		pygame.draw.circle(screen,THECOLORS["black"],conv_to_int(self.right_eye_pos),self.radius,2)
		pygame.draw.circle(screen,THECOLORS["black"],conv_to_int(right_pupil),int(self.pupil_size))

		# left eye
		pygame.draw.circle(screen,THECOLORS["white"],conv_to_int(self.left_eye_pos),self.radius,0)
		pygame.draw.circle(screen,THECOLORS["black"],conv_to_int(self.left_eye_pos),self.radius,2)
		pygame.draw.circle(screen,THECOLORS["black"],conv_to_int(left_pupil),int(self.pupil_size))

if __name__ == '__main__' :
	#from DiffProviderSimulator import DiffProviderSimulator
	#from AetherDriver import AetherDriver
	from aether.core import AetherDriver

	driver = AetherDriver(640,debug=False)
	driver.register_module(PeepersModule(driver))
	driver.run()
