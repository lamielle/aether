from aether.core import AetherDriver, AetherModule, MouseInputProvider
from aether.modules import PymunkModule
from pygame.color import THECOLORS
from pygame.locals import *
import pygame.event, pygame.draw

class Whiteboard(AetherModule) :

	def __init__(self,driver,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,driver,*args)
		self.blink_phase = 0
		self.pointer_sprite = LaserPointerSprite()

		self.lines = [[]]
		self.curr_line = []

	def draw(self,screen) :
		screen.fill(THECOLORS["white"])

		pt = self.input.get_com()
		if self.blink_phase == 0 :
			self.pointer_sprite.update(pt)
		else :
			self.blink_phase -= 1
			self.pointer_sprite.update(None)

		if self.pointer_sprite.draw :
			self.curr_line.append(pt)
			self.lines[-1] = self.curr_line
		else :
			self.lines.append(self.curr_line)
			self.curr_line = []

		for l in self.lines :
			if len(l) > 1 :
				pygame.draw.aalines(screen,THECOLORS["black"],False,l,1)

		screen.blit(self.pointer_sprite.image,pt)

	def process_event(self, event) :
		if event.type == KEYDOWN and event.key == K_b :
			self.blink_phase = 3
			return True
		return False

class LaserPointerSprite(pygame.sprite.Sprite) :

	DRAW,CURSOR = range(2)
	

	def __init__(self) :
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((10,10))
		self.image.set_colorkey(THECOLORS["white"])

		self.history = []
		self.history_size = 10

		self.draw = False
		self.mode = LaserPointerSprite.CURSOR

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

		# clicked, toggle graphic
		if len(inds) == 2 :
			self.draw = not self.draw
			self.image.fill(THECOLORS["white"])
			if self.draw :
				pygame.draw.circle(self.image,THECOLORS["red"],(5,5),5,1)
			else :
				pygame.draw.rect(self.image,THECOLORS["black"],(0,0,10,10),1)
			self.history = []

if __name__ == "__main__" :
	#face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether-adam/examples/haarcascade_frontalface_alt.xml",flip=True)
	mouse_input = MouseInputProvider()
	driver = AetherDriver(640,input=mouse_input)
	driver.register_module(Whiteboard(driver))
	driver.run()
