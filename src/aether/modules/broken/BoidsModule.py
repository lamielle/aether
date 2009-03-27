import pygame, pygame.key
from pygame.color import THECOLORS
from pygame.locals import *
from aether.core import AetherParamModule

import math
from random import randint

from random import randrange
from numpy import array

"""
Explores flocking behavior of flying "boids" aka "bird android".

Thanks to Conrad Parker conrad@vergenet.net for the boids pseudocode.
http://www.vergenet.net/~conrad/boids/pseudocode.html

Eric Nilsen
September 2003
ericjnilsen@earthlink.net

Ideas for version 2.0:
		predators
		obstructions
		perching on the ground for a bit
		prevailing wind
		random flock scattering
		cone boid shape --> change boid axis to indicate direction

Code found at: http://www.vpython.org/contributed/boids.py
"""

class BoidsModule(AetherParamModule) :
	def __init__(self, driver, **kwargs) :
		AetherParamModule.__init__(self,driver,**kwargs)
		self.boid_init()

	def boid_init(self, numboids = 50):
		self.SIDE_WIDTH = self.dims[0] #unit for a side of the flight space
		self.SIDE_HEIGHT = self.dims[1]

		self.MINX = 0									 #left
		self.MINY = 0									 #bottom
		self.MAXX = self.SIDE_WIDTH		 #right
		self.MAXY = self.SIDE_HEIGHT		#top

		self.RADIUS = 5								 #radius of a boid.	I wimped and used points.
		self.NEARBY = self.RADIUS * 5	 #the 'halo' of space around each boid
		self.FACTOR = .95							 #the amount of movement to the perceived flock center
		self.NEGFACTOR = self.FACTOR * -1.0 #same thing, only negative

		self.NUMBOIDS = numboids				#the number of boids in the flock

		self.boidflock = []						 #empty list of boids
		self.DT = 0.02									#delay time between snapshots

		self.initializePositions()

	def initializePositions(self):
		c = 0																	 #initialize the color switch
		for b in range(self.NUMBOIDS):					#for each boid, ...
			x = randrange(self.MINX, self.MAXX) #random left-right
			y = randrange(self.MINY, self.MAXY) #random up-down

			if c > 2:													 #reset the color switch when it grows too big
				c = 0
			if c == 0:
				COLOR = THECOLORS['red']
			if c == 1:
				COLOR = THECOLORS['green']
			if c == 2:
				COLOR = THECOLORS['blue']

			#splat a boid, add to flock list
			self.boidflock.append(point(pos=array([x,y]),radius=self.RADIUS,color=COLOR))

			c = c + 1													 #increment the color switch

	def draw(self,screen) :
		screen.fill((200,200,255,255))
		self.boids(screen)

	def process_event(self,event) :
		if event.type == KEYDOWN and event.key == K_r :
			self.boidflock=[]
			self.initializePositions()
			return True
		return False

	def boids(self,screen):
		self.moveAllBoidsToNewPositions()	 #um ... what it says
		for b in range(self.NUMBOIDS):
			boid=self.boidflock[b]
			pygame.draw.circle(screen,boid.color,(int(boid.x),int(boid.y)),boid.radius)

	def moveAllBoidsToNewPositions(self):
		for b in range(self.NUMBOIDS):
			#manage boids hitting the torus 'boundaries'
			if self.boidflock[b].x < self.MINX:
				self.boidflock[b].x = self.MAXX

			if self.boidflock[b].x > self.MAXX:
				self.boidflock[b].x = self.MINX

			if self.boidflock[b].y < self.MINY:
				self.boidflock[b].y = self.MAXY

			if self.boidflock[b].y > self.MAXY:
				self.boidflock[b].y = self.MINY

			v1 = array([0.0,0.0,0.0])				#initialize array for rule 1
			v2 = array([0.0,0.0,0.0])				#initialize array for rule 2
			v3 = array([0.0,0.0,0.0])				#initialize array for rule 3


			v1 = self.rule1(b)							#get the array for rule 1
			v2 = self.rule2(b)							#get the array for rule 2
			v3 = self.rule3(b)							#get the array for rule 3

			boidvelocity = array([0.0,0.0])					#initialize the boid velocity
			boidvelocity = boidvelocity + v1 + v2 + v3	#accumulate the rules array results
			self.boidflock[b].pos = self.boidflock[b].pos + (boidvelocity*self.DT) #move the boid

	def rule1(self, aboid):		#Rule 1:	boids fly to perceived flock center
		pfc = array([0.0,0.0])									 #pfc: perceived flock center
		for b in range(self.NUMBOIDS):							#for all the boids
			if b != aboid:													#except the boid at hand
				pfc = pfc + self.boidflock[b].pos	#calculate the total pfc

		pfc = pfc/(self.NUMBOIDS - 1.0)						 #average the pfc

		#nudge the boid in the correct direction toward the pfc
		if pfc[0] > self.boidflock[aboid].x:
			pfc[0] = (pfc[0] - self.boidflock[aboid].x)*self.FACTOR
		if pfc[0] < self.boidflock[aboid].x:
			pfc[0] = (self.boidflock[aboid].x - pfc[0])*self.NEGFACTOR
		if pfc[1] > self.boidflock[aboid].y:
			pfc[1] = (pfc[1] - self.boidflock[aboid].y)*self.FACTOR
		if pfc[1] < self.boidflock[aboid].y:
			pfc[1] = (self.boidflock[aboid].y - pfc[1])*self.NEGFACTOR
		return pfc

	def rule2(self, aboid):		#Rule 2: boids avoid other boids
		v = array([0.0,0.0]) #initialize the avoidance array

		for b in range(self.NUMBOIDS):
			if b != aboid:
				if abs(self.boidflock[b].x - self.boidflock[aboid].x) < self.NEARBY:
					if self.boidflock[b].x > self.boidflock[aboid].x:
						v[0] = self.NEARBY * 12.0		#works better when I multiply by 12, don't know why
					if self.boidflock[b].x < self.boidflock[aboid].x:
						v[0] = -self.NEARBY * 12.0
				if abs(self.boidflock[b].y - self.boidflock[aboid].y) < self.NEARBY:
					if self.boidflock[b].y > self.boidflock[aboid].y:
						v[1] = self.NEARBY * 12.0
					if self.boidflock[b].y < self.boidflock[aboid].y:
						v[1] = -self.NEARBY * 12.0
		return v

	def rule3(self, aboid):		#Rule 3: boids try to match speed of flock
		pfv = array([0.0,0.0])	 #pfv: perceived flock velocity

		for b in range(self.NUMBOIDS):
			if b != aboid:
				pfv = pfv + self.boidflock[b].pos

			pfv = pfv/(self.NUMBOIDS - 1.0)
			pfv = pfv/(aboid + 1)		#some of the boids are more sluggish than others

		return pfv

class point(object):
	__slots__=('pos','radius','x','y','color')

	def __init__(self,pos,radius,color):
		self.pos=pos
		self.radius=radius
		self.color=color

	def __str__(self):
		return str([self.pos,self.radius])

	def get_x(self): return self.pos[0]
	def set_x(self,x): self.pos[0]=x

	def get_y(self): return self.pos[1]
	def set_y(self,y): self.pos[1]=y

	x=property(get_x,set_x)
	y=property(get_y,set_y)
