
from aether.core import AetherDriver, FaceInputProvider, AetherModule

import pygame.image, pygame.font
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

	def draw(self,screen) :

		raw_image = self.input.get_curr_frame()
		scaled_raw_image = pygame.transform.scale(raw_image,self.dims)
#		screen.blit(scaled_raw_image,(0,0))
		screen.blit(self.frame,(0,0))

		faces = self.input.get_polys()

		
		if len(faces) > 0 :
			for i,face in enumerate(faces) :

				if i >= len(self.frame_coords) : break

				face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
				dims = face[1][0]-face[0][0], face[2][1]-face[1][1]
				face_surf = scaled_raw_image.subsurface(pygame.Rect(face[0],dims))
				scaled_face_surf = pygame.transform.scale(face_surf,self.frame_scales[i])
				screen.blit(scaled_face_surf,self.frame_coords[i])
				#pygame.draw.rect(screen,THECOLORS['red'],pygame.Rect(face[0],dims),1)
				num = self.font.render(str(i),False,THECOLORS['red'])
				screen.blit(num,self.frame_coords[i])

if __name__ == "__main__" :
	face_input = FaceInputProvider(0,(320,240),"/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",flip=True)
	driver = AetherDriver(640,input=face_input)
	driver.register_module(PictureFrames(driver))
	driver.run()
