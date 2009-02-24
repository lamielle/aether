from pymunk.vec2d import Vec2d 
from pymunx import pymunx
from AetherModule import AetherModule
from random import randint
import pygame
from pygame.color import *

class PymunkModule(AetherModule) :

	def __init__(self, driver, **kwargs) :

		self.driver = driver
		self.dims = driver.dims

		# convenient access to pymunk functions
		world = pymunx(gravity=(0.0,0.0,0.0))
		self.world = world

		# add the walls
		tl, tr, bl, br = (0,0),(self.dims[0],0),(0,self.dims[1]),(self.dims[0],self.dims[1])
		walls = ((tl,tr),(tl,bl),(tr,br),(bl,br))
		wall_shapes = []
		for w in walls :
			wall_shapes.append(world.add_wall(w[0],w[1],elasticity=1,friction=0.0))
		self.wall_shapes = wall_shapes

		# add balls
		ball_shapes = []
		for x in range(200) :
			x,y = randint(0,self.dims[0]),randint(0,self.dims[1])
			ball_shapes.append(world.add_ball(Vec2d(x,y),radius=7,density=.1,inertia=1000,elasticity=1,friction=0))
			dx,dy = randint(-10000,10000),randint(-10000,10000)
			ball_shapes[-1].body.apply_impulse(Vec2d(dx,dy),(dx,dy))
		self.ball_shapes = ball_shapes

		# add the circle the mouse will follow
		self.cursor_ball = world.add_ball(Vec2d(self.dims[0]/2,self.dims[1]/2),radius=25,elasticity=1,friction=0)

	def activate(self) :
		pass

	def deactivate(self) :
		pass

	def draw_ball(self,screen, ball):
		p = int(ball.body.position.x), self.dims[1]-int(ball.body.position.y)
		pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 1)

	def draw(self,screen) :
		screen.fill(THECOLORS["white"])
		for ball in self.ball_shapes :
			self.draw_ball(screen, ball)

		pos = pygame.mouse.get_pos()
		self.cursor_ball.body.position = (pos[0],self.dims[1]-pos[1])
		#self.cursor_ball.body.update_position((pos[0],pos[1]))
		self.draw_ball(screen,self.cursor_ball)
		
		self.world.update()

	def process_event(self,event) :
		pass
