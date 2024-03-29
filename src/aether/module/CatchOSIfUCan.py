#!/usr/bin/env python

import pygame, pygame.key, pygame.sprite, pygame.image, pygame.transform, pygame.mouse, pygame.font
from pygame.color import THECOLORS
from pygame.locals import *
from aether.core import AetherModule
from time import time

#from math import abs
from random import randint, randrange, random

class CatchOSIfUCan(AetherModule) :

	chains = {'input':'ShadowPolySaviorChain'}
	#chains={'input':'DebugShadowPolyChain'}
	#chains={'input':'ShadowPolyChain'}
	#chains = {'input':'MouseChain'}

	def init(self):

		# set up the images
		#image_fns = ['images/freebsd-logo.png','images/fedora-logo.png','images/ubuntu-logo.png','images/windows-logo.png','images/gentoo-logo.png','images/e-logo.png','images/debian-logo.png','images/opensuse-logo.png']
		self.names = ['freebsd','fedora','ubuntu','gentoo','e','debian','opensuse','windows']
		image_fns = [self.file_path('%s-logo.png'%n) for n in self.names]

		self.settings.perspective.calibrated = False

		if not pygame.mixer.get_init() : 
			pygame.mixer.init()
		self.techno = pygame.mixer.Sound(self.file_path('techno.wav'))

		sm = 50
		lg = 100
		images = [pygame.image.load(s) for s in image_fns]
		scales = [sm]*7 + [lg]

		self.image_col = zip(self.names,images,scales)

		# create the sprite group
		self.sprites = pygame.sprite.Group()

		# game stuff
		self.maxminscore = 300
		self.score = 0
		self.update_drop_freq()
		self.update_drop_speed()
		self.add_score = 10

		pygame.font.init()
		self.font = pygame.font.Font(None, 36)
		self.text = self.font.render("Score: %d"%self.score, 1, (10, 10, 10))
		self.textpos = self.text.get_rect(centerx=self.dims[0]-100)

		self.you_won = False

		self.draw_shadow = True

		self.checkerboard = pygame.image.load(self.file_path('checkerboard.png'))
		self.checkerboard = pygame.transform.scale(self.checkerboard,(self.dims[0]-25,self.dims[1]-25))

		self.played_winning_music = False

	def update_drop_freq(self) :
		self.drop_freq = abs(self.score/10000.) + 0.1
	 
	def update_drop_speed(self) :
		self.drop_speed = abs(self.score/100.) + 3

	def draw(self,screen) :
		#print time()
		shadow_polys = self.input.read()
		#print shadow_polys, len(shadow_polys), [len(x) for x in shadow_polys]
		calibrated = self.settings.perspective.calibrated
		#calibrated = True
		if not calibrated :
			#self.debug_print('calibrating:%s'%self.settings.perspective.calibrated)
			screen.fill((255,255,255,255)) # this is necessary for some reason
			screen.blit(self.checkerboard,(12,12))
			pygame.draw.rect(screen,(255,255,255,255),pygame.Rect((12,12),self.dims),15) # this helps opencv find the checkerboard
		else :

			screen.fill((200,200,255,255))

			# check to add sprite
			if random() < self.drop_freq :
				i = self.image_col[randrange(0,len(self.image_col))]
				self.sprites.add(LogoSprite(i[0],i[1],i[2],randrange(i[2]/2.,self.dims[0]-i[2]/2),-i[2],self.drop_speed,self))

			if not self.you_won :
				# draw the shadow
				#shadow_pts = self.input.read()
				#shadow_rect = None
				#if len(shadow_pts) > 2 : shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
				#if shadow_rect is not None : pygame.draw.rect(screen,THECOLORS["red"],shadow_rect,1)
				#for pt in shadow_pts :
				#	pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)
				for shadow_pts in shadow_polys :
					if self.draw_shadow :
						if len(shadow_pts) > 2 :
							screen.lock()
							pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts,0)
							screen.unlock()
						for p in shadow_pts :
							screen.lock()
							pygame.draw.circle(screen,THECOLORS["red"],p,2,0)
							screen.unlock()
					
				for s in self.sprites :
					if s.is_dead :
						self.sprites.remove(s)
					if s.rect.y > self.dims[1]+50 :
						self.sprites.remove(s)
						if s.name in self.names[0:7] :
							self.score += [10,-10][self.score > 0]
					for shadow_pts in shadow_polys :
						for p in shadow_pts :
							if s.rect.collidepoint(p) and not s.is_dying :
								if s.name in self.names[0:7] : # good boy
									self.score = min(self.maxminscore,self.score+self.add_score)
								else : # that's a bad monkey
									self.score = max(-self.maxminscore,self.score-self.add_score)
								s.start_dying()

				self.update_drop_freq()
				self.update_drop_speed()

				#print self.score, self.drop_freq, self.drop_speed
				if self.score >= self.maxminscore :
					self.you_won = True
					self.drop_freq = 0.6
					self.drop_speed = 20

			else :

				if not self.played_winning_music :
					self.techno.play()
					self.played_winning_music = True

				self.winner = self.font.render("ALL YOUR OS ARE BELONG TO US",1,(randint(0,255),randint(0,255),randint(0,255)))
				textrect = self.winner.get_rect()
				screen.blit(self.winner,(self.dims[0]/2-textrect.width/2,self.dims[1]/2))

				for s in self.sprites :
					if s.is_dead :
						self.sprites.remove(s)
					if s.rect.y > self.dims[1]+50 :
						self.sprites.remove(s)

			self.sprites.draw(screen)
			self.sprites.update()

			self.text = self.font.render("Score: %d"%self.score, 1, (10, 10, 10))
			screen.blit(self.text,self.textpos)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			if event.key == K_r :
				self.settings.perspective.calibrated = False
				return True
			elif event.key == K_w :
				#self.draw_shadow = not self.draw_shadow
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


class LogoSprite(pygame.sprite.Sprite) :
	die_seq = None
	names = None
	pop = None

	def __init__(self,name,image,size,x,y,dy,parent) :
		pygame.sprite.Sprite.__init__(self)

		if LogoSprite.names is None :
			LogoSprite.names = [parent.file_path('poof%d.png'%s) for s in [1,2,3,4]]

		if LogoSprite.pop is None :
			#self.sound = pygame.mixer.Sound(parent.file_path('%s.wav'%self.sound_name))
			LogoSprite.pop = pygame.mixer.Sound(parent.file_path('pop.wav'))
			LogoSprite.smash = pygame.mixer.Sound(parent.file_path('smash.wav'))

		if self.die_seq is None :
			self.die_seq = [pygame.image.load(s) for s in LogoSprite.names]

		self.name = name
		self.image = pygame.transform.scale(image,(size,size))
		self.size = size
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.is_dying = False
		self.is_dead = False
		self.die_index = 0
		self.dy = dy

	def update(self) :
		if self.is_dying :
			if self.die_index != len(self.die_seq) :
				pygame.transform.scale(self.die_seq[self.die_index],(self.size,self.size),self.image)
				self.die_index += 1
			else :
				self.is_dead = True
		else :
			self.rect.center = self.rect.center[0],self.rect.center[1]+self.dy

	def start_dying(self) :
		self.is_dying = True
		if self.name == 'windows' :
			LogoSprite.smash.play()
		else :
			self.pop.play()
