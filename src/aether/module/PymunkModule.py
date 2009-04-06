'''
This module tests the PerspectiveChain transformation sequence.  Press 'r' to reset calibration.

:Author: Adam Labadorf
'''

from aether.core import AetherModule
from pygame.color import THECOLORS
import pygame, pygame.font
from pygame.locals import *
from random import randrange

from pymunk.vec2d import Vec2d
from pymunk import inf
from aether.util import pymunx

class PymunkModule(AetherModule):

	#Chains this module needs
	#chains={'mouse':'MouseChain'}
	#chains={'shadow':'ShadowPolyChain'}

	def __init__(self) :
		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,self.dims)

		pygame.init()
		pygame.font.init()
		self.debug_print("Font initialized: "+str(pygame.font.get_init()))
		self.font = pygame.font.Font(None, 36)
		self.min_area_pos = (2,0)
		self.thresh_pos = (0,self.dims[1]-38)

		self.sprites = pygame.sprite.Group()

		self.draw_shadow = True

		# convenient access to pymunk functions
		world = pymunx(gravity=(0.0,0.0,0.0))
		self.world = world

		# add the walls
		tl, tr, bl, br = (0,0),(self.dims[0],0),(0,self.dims[1]),(self.dims[0],self.dims[1])
		walls = ((tl,tr),(tl,bl),(tr,br),(bl,br))
		wall_shapes = []
		for w in walls :
			wall_shapes.append(world.add_wall(w[0],w[1],elasticity=1,friction=.5))
		self.wall_shapes = wall_shapes

		# add balls
		ball_shapes = []
		for x in range(10) :
			x,y = randint(0,self.dims[0]),randint(0,self.dims[1])
			ball_shapes.append(world.add_ball(Vec2d(x,y),radius=7,density=0.1,inertia=1000,elasticity=0.9,friction=0.1))
			#ball_shapes.append(world.add_ball(Vec2d(x,y)))
			dx,dy = randint(-1000,1000),randint(-1000,1000)
			ball_shapes[-1].body.apply_impulse(Vec2d(dx,dy),(dx,dy))
		self.ball_shapes = ball_shapes

		# add the circle the mouse will follow
		self.cursor_ball = world.add_ball(Vec2d(self.dims[0]/2,self.dims[1]/2),density=100,radius=25,elasticity=0.9,friction=0)

	def draw_ball(self,screen, ball):
		p = int(ball.body.position.x), self.dims[1]-int(ball.body.position.y)
		pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 1)

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#curr_frame=self.shadow.get_frame()
		#polys=self.shadow.read()
		polys = self.mouse.read()

		#calibrated = self.settings.perspective.calibrated
		calibrated = True
		if not calibrated :
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(0,0))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((0,0),self.dims),5) # this helps opencv find the checkerboard
		else :
			screen.fill((255,255,255,255))

			self.sprites.draw(screen)
			self.sprites.update()

			for ball in self.ball_shapes :
				self.draw_ball(screen, ball)

			# when manually updating a body, need to set it's velocity BEFORE the call to world.update()
			velocity_scale = 10
			velocity = Vec2d([x*velocity_scale for x in pygame.mouse.get_rel()])
			self.cursor_ball.body.update_velocity(velocity,0,3)
			self.draw_ball(screen,self.cursor_ball)

			# do the update
			self.world.update()

			# when manually updating a body, need to set it's position AFTER the call to world.update()
			pos = self.input.get_com()
			#polys = self.mouse.read()
			#if len(polys) > 0 :
			#	pos = 
			self.cursor_ball.body.position = (pos[0],self.dims[1]-pos[1])
			self.cursor_ball.body.update_position(0.01)




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
