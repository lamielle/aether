
from aether.core import AetherDriver, FaceInputProvider, AetherModule
from aether.sprites import FaceSprite, FaceSpriteTracker

import pygame.image, pygame.font, pygame.sprite
from pygame.color import THECOLORS
import pygame.transform

class PictureFrames(AetherModule) :

	def __init__(self,*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,*args)
		self.font = pygame.font.Font(None,24)
		self.frame = pygame.image.load("frames.png")
		self.frame_coords = ((82,94),(334,94),(454,94),(454,260),(334,260))
		self.frame_scales = ((229,302),(98,136),(98,136),(100,136),(100,136))

		self.frame_sprites = []
		self.frame_sprites.append(FaceSprite(pygame.Rect((0,0),(0,0)),lag=10))

		self.sprite_tracker = FaceSpriteTracker(max_sprites=5,tolerance=(100,100))

	def draw(self,screen) :

		raw_image = self.input.get_curr_frame()
		#raw_image = self.input.get_fd_frame()
		scaled_raw_image = pygame.transform.scale(raw_image,self.dims)
		#screen.blit(scaled_raw_image,(0,0))
		#screen.blit(raw_image,(0,0))

		faces = self.input.get_polys()
		#faces = []
		screen.blit(self.frame,(0,0))

		if len(faces) > 0 :

			for i,face in enumerate(faces) :
				face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
				dims = face[1][0]-face[0][0], face[2][1]-face[1][1]
				faces[i] = pygame.Rect(face[0],dims)

		self.sprite_tracker.update(faces,scaled_raw_image)

		print 'Sprite ages:',self.sprite_tracker._sprite_ages
		for i,sprite in enumerate(self.sprite_tracker.sprites) :
			scaled_face_surf = pygame.transform.scale(sprite.image,self.frame_scales[i])
			screen.blit(scaled_face_surf,self.frame_coords[i])
			num = self.font.render(str(i),False,THECOLORS['red'])
			screen.blit(num,self.frame_coords[i])



if __name__ == "__main__" :
	face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",flip=True)
	driver = AetherDriver(640,input=face_input)
	driver.register_module(PictureFrames(driver))
	driver.run()
