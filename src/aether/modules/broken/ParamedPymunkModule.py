from pymunk.vec2d import Vec2d
from pymunk import inf
from pymunx import pymunx
from AetherModule import AetherModule
from AetherModule import AetherParametrizedModule
from random import randint
import pygame
from pygame.color import *
from pygame.locals import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

class ParamedPymunkModule(AetherParametrizedModule) :

	def __init__(self, driver, **kwargs) :
		AetherParametrizedModule.__init__(self,driver,**kwargs)

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
			ball_shapes.append(world.add_ball(Vec2d(x,y),radius=7,density=.1,inertia=1000,elasticity=0.99,friction=0.0))
			dx,dy = randint(-1000,1000),randint(-1000,1000)
			ball_shapes[-1].body.apply_impulse(Vec2d(dx,dy),(dx,dy))
		self.ball_shapes = ball_shapes

		# add the circle the mouse will follow
		self.cursor_ball = world.add_ball(Vec2d(self.dims[0]/2,self.dims[1]/2),density=inf,radius=25,elasticity=5,friction=0)

	def draw_ball(self,screen, ball):
		p = int(ball.body.position.x), self.dims[1]-int(ball.body.position.y)
		pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 1)

	def draw(self,screen) :
		screen.fill(THECOLORS["white"])
		for ball in self.ball_shapes :
			self.draw_ball(screen, ball)

		pos = pygame.mouse.get_pos()
		self.cursor_ball.body.position = (pos[0],self.dims[1]-pos[1])
		rel = pygame.mouse.get_rel()
		#self.cursor_ball.body.apply_impulse(Vec2d(rel[0]*100,rel[1]*100),(rel[0],rel[1]))
		self.cursor_ball.body.update_position(0)
		self.cursor_ball.body.update_velocity(Vec2d(0,0),0,0)
		self.world.space.resize_static_hash()
		self.world.space.resize_active_hash()
		self.world.space.rehash_static()
		self.draw_ball(screen,self.cursor_ball)
		print self.cursor_ball.body.velocity, self.cursor_ball.body.position, rel
		
		self.world.update()

	def do_collision(a,b,contacts,normal) :
		print a,b,contacts,normal

	def get_parameter_widgets(self) :

		lab = Label("Gravity: (0,0)")

		def inc_grav() :
			self.world.space.gravity = (0,self.world.space.gravity[1]+20)
			lab.set_text("Gravity: (0,%d)"%self.world.space.gravity[1])
		def dec_grav() :
			self.world.space.gravity = (0,self.world.space.gravity[1]-20)
			lab.set_text("Gravity: (0,%d)"%self.world.space.gravity[1])

		inc = Button("Increase Gravity")
		inc.connect_signal(SIG_CLICKED,inc_grav)
		dec = Button("Decrease Gravity")
		dec.connect_signal(SIG_CLICKED,dec_grav)

		return [lab,inc,dec]
