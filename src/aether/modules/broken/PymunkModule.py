from pymunk.vec2d import Vec2d
from pymunk import inf
from aether.util import pymunx
from aether.core.AetherModule import AetherModule
from aether.core.AetherParamModule import AetherParamModule
from random import randint
import pygame
from pygame.color import *
from pygame.locals import *
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

class PymunkModule(AetherModule) :

	def __init__(self, driver, **kwargs) :
		AetherModule.__init__(self,driver,**kwargs)

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

	def draw(self,screen) :
		screen.fill(THECOLORS["white"])
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
		self.cursor_ball.body.position = (pos[0],self.dims[1]-pos[1])
		self.cursor_ball.body.update_position(0.01)

	def do_collision(a,b,contacts,normal) :
		#print a,b,contacts,normal
		pass

	# this method is old, left as an example for later
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
