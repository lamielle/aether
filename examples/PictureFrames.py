
from aether.core import AetherDriver, FaceInputProvider, AetherModule

import pygame.image, pygame.font, pygame.sprite
from pygame.color import THECOLORS
import pygame.transform

class PictureFrames(AetherModule) :

	def __init__(self,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,*args)
		self.font = pygame.font.Font(None,24)
		self.frame = pygame.image.load("frames.png")
		self.frame_coords = ((82,94),(334,94),(454,260),(333,260))
		self.frame_scales = ((229,302),(98,136),(100,136),(100,136))

		self.frame_sprites = []
		self.frame_sprites.append(FaceSprite(pygame.Rect((0,0),(0,0)),lag=10))

	def draw(self,screen) :

		raw_image = self.input.get_curr_frame()
		#raw_image = self.input.get_fd_frame()
		scaled_raw_image = pygame.transform.scale(raw_image,self.dims)
		#screen.blit(scaled_raw_image,(0,0))
		#screen.blit(raw_image,(0,0))

		faces = self.input.get_polys()
		screen.blit(self.frame,(0,0))

		if len(faces) > 0 :
			for i,face in enumerate(faces) :

				if i >= len(self.frame_coords) : break

				face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
				dims = face[1][0]-face[0][0], face[2][1]-face[1][1]
				self.frame_sprites[0].update(pygame.Rect(face[0],dims))
				face_surf = scaled_raw_image.subsurface(self.frame_sprites[0].rect)
				scaled_face_surf = pygame.transform.scale(face_surf,self.frame_scales[i])
				screen.blit(scaled_face_surf,self.frame_coords[i])
				num = self.font.render(str(i),False,THECOLORS['red'])
				screen.blit(num,self.frame_coords[i])

class FaceSprite(pygame.sprite.Sprite) :

	def __init__(self,rect,lag=10) :
		pygame.sprite.Sprite.__init__(self)

		self.rect = rect
		self.rect.topleft = rect.x,rect.y

		self.lag = lag
		self.history = [rect]

	def update(self,rect) :
		# calculate running average
		if len(self.history) > self.lag :
			self.history.pop(0)
		self.history.append(rect)
		width = sum([x.width for x in self.history])/len(self.history)
		height = sum([x.height for x in self.history])/len(self.history)

		self.rect = pygame.Rect(rect.x,rect.y,width,height)
		self.rect.topleft = (rect.x,rect.y)

	

if __name__ == "__main__" :
	face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",flip=True)
	driver = AetherDriver(640,input=face_input)
	driver.register_module(PictureFrames(driver))
	driver.run()
