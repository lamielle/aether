from pymunk.vec2d import Vec2d
import pymunk as pm
from aether.util import pymunx
from aether.core import AetherDriver, AetherModule, MouseInputProvider
from aether.modules import PymunkModule
from pygame.color import THECOLORS
import pygame.draw

class WindChimes(AetherModule) :

	def __init__(self,driver,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,driver,*args)

		self.world = pymunx(gravity=(0.0,0.0,0.0))

		# add the walls
		#tl, tr, bl, br = (0,0),(self.dims[0],0),(0,self.dims[1]),(self.dims[0],self.dims[1])
		#walls = ((tl,tr),(tl,bl),(tr,br),(bl,br))
		#wall_shapes = []
		#for w in walls :
		#	wall_shapes.append(self.world.add_wall(w[0],w[1],elasticity=1,friction=.5))
		#self.wall_shapes = wall_shapes

		chime_pts = ((0,0),(10,0),(10,50),(0,50))
		self.chime = self.world.add_poly(chime_pts)
		self.chime.body.position = (self.dims[0]/2,self.dims[1]/2)

		# add the circle the mouse will follow
		self.cursor_ball = self.world.add_ball(Vec2d(self.dims[0]/2,self.dims[1]/2),density=100,radius=25,elasticity=0.9,friction=0)

	def draw_ball(self,screen, ball):
		p = int(ball.body.position.x), self.dims[1]-int(ball.body.position.y)
		pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 1)

	def pymunk2pygame(self,pt) :
		return (int(pt.x),int(self.dims[1]-pt.y))

	def draw(self,screen) :
		screen.fill(THECOLORS["lightblue"])
		try :
			pts = [self.pymunk2pygame(x) for x in self.chime.get_points()]
			print pts
			pygame.draw.polygon(screen,THECOLORS["blue"],pts,1)
		except ValueError :
			#print 'junk'
			pass

		# when manually updating a body, need to set it's velocity BEFORE the call to world.update()
		velocity_scale = 10
		velocity = Vec2d([x*velocity_scale for x in pygame.mouse.get_rel()])
		self.cursor_ball.body.update_velocity(velocity,0,3)

		self.world.update()

		# when manually updating a body, need to set it's position AFTER the call to world.update()
		pos = self.input.get_com()
		self.cursor_ball.body.position = (pos[0],self.dims[1]-pos[1])
		self.cursor_ball.body.update_position(0.01)
		self.draw_ball(screen,self.cursor_ball)

if __name__ == "__main__" :
	#face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether-adam/examples/haarcascade_frontalface_alt.xml",flip=True)
	mouse_input = MouseInputProvider()
	driver = AetherDriver(640,input=mouse_input)
	driver.register_module(WindChimes(driver))
	driver.run()
