'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
from pygame.color import THECOLORS
import pygame, pygame.font
from pygame.locals import *
from random import randrange

class SoundMosaic(AetherModule):

	#Chains this module needs
	#chains={'mouse':'MouseChain'}
	chains={'shadow':'ShadowPolyChain'}

	def init(self):
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,self.dims)
		# sound stuff - sucks right now.
		#pygame.mixer.quit()
		#pygame.mixer.pre_init(22050, -16, 1, 3072)
		#pygame.mixer.init()
		#pygame.mixer.set_num_channels(300)
		pygame.font.init()
		self.debug_print("Font initialized: "+str(pygame.font.get_init()))
		self.font = pygame.font.Font(None, 36)
		self.min_area_pos = (2,0)
		self.thresh_pos = (0,self.dims[1]-38)

		self.sprites = pygame.sprite.Group()

		num_across = 20
		tile_size = self.dims[0]/num_across
		num_high = self.dims[1]/tile_size
		top_margin = self.dims[1]-tile_size*num_high
		for i in range(num_high) :
			for j in range(num_across) :
				self.sprites.add(SoundTile((j*tile_size,i*tile_size+top_margin),(tile_size,tile_size),None,self,type='square'))

		#for s in SoundTile.sounds :
		#	s.play()

		self.draw_shadow = True

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#curr_frame=self.shadow.get_frame()
		polys=self.shadow.read()
		#polys = self.mouse.read()

		calibrated = self.settings.perspective.calibrated
		#calibrated = True
		if not calibrated :
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.dims),5) # this helps opencv find the checkerboard
		else :
			screen.fill((255,255,255,255))

			self.sprites.draw(screen)
			self.sprites.update()

			for s in self.sprites :
				for vset in polys :
					for p in vset :
						if s.rect.collidepoint(p) :
							s.flash()
					if self.draw_shadow and len(vset) > 2 :
							pygame.draw.polygon(screen,(10,10,10),vset,0)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_i :
				self.settings.threshold.threshold += 1
				self.debug_print('Increasing threshold: %d'%self.settings.threshold.threshold)
				return True
			elif event.key == K_k :
				self.settings.threshold.threshold -= 1
				self.debug_print('Decreasing threshold: %d'%self.settings.threshold.threshold)
				return True
			elif event.key == K_o :
				self.settings.shadow.min_area += 100
				self.debug_print('Increasing min poly area: %d'%self.shadow.min_area)
				return True
			elif event.key == K_l :
				self.settings.shadow.min_area -= 100
				self.debug_print('Decreasing min poly area: %d'%self.shadow.min_area)
				return True
			elif event.key == K_g :
				for s in self.sprites :
					s.flash()
				self.debug_print('Flash!')
				return True
		return False

class SoundTile(pygame.sprite.Sprite) :

	colors = [THECOLORS["red"],THECOLORS["blue"],THECOLORS["green"],THECOLORS["orange"],THECOLORS["gray"],THECOLORS["purple"]]
	sounds = None

	def __init__(self,pos,size,sound,parent,type='square') :
		pygame.sprite.Sprite.__init__(self)
		self.jewel = pygame.image.load(parent.file_path('%sjewel.png'%type))

		self.color_id = randrange(len(SoundTile.colors))

		self.jewel = pygame.transform.scale(self.jewel,size)
		self.image = pygame.Surface(self.jewel.get_size())
		self.image.fill(SoundTile.colors[self.color_id])
		self.image.blit(self.jewel,(0,0))

		self.rect = self.image.get_rect()
		self.rect.topleft = pos

		self.flash_phase = 0
		self.max_flash = 40
		#sound_names = ['high','mid1','mid2','low']
		sound_names = ['sine_1','sine_2','sine_3','sine_4']
		#if SoundTile.sounds is None and pygame.mixer.get_init() :
		#	SoundTile.sounds = []
		#	for sf in sound_names :
		#		SoundTile.sounds.append(pygame.mixer.Sound(parent.file_path('%s.wav'%sf)))

		#self.sound_name = sound_names[randrange(len(sound_names))]
		#self.sound = pygame.mixer.Sound(parent.file_path('%s.wav'%self.sound_name))
		#self.sound = SoundTile.sounds[randrange(len(SoundTile.sounds))]
		#self.curr_channel = None

	def flash(self) :
		self.flash_phase = self.max_flash
		#self.curr_channel = self.sound.play()

	def update(self) :
		
		self.image.fill(SoundTile.colors[self.color_id])
		self.image.blit(self.jewel,(0,0))

		if self.flash_phase != 0 :
			self.flash_phase -= 1
			self.color_id = (self.color_id + 1) % len(SoundTile.colors)
