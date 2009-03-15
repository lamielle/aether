
from aether.core import AetherDriver, FaceInputProvider, AetherModule
from aether.sprites import FaceSprite, FaceSpriteTracker

import pygame.image, pygame.font, pygame.sprite, pygame.transform, pygame.draw
from pygame.color import THECOLORS

class FacePanes(AetherModule) :

	def __init__(self,driver,grid=(3,2),*args) :
		# need to call parent class' init method explicitly in python
		AetherModule.__init__(self,driver,*args)
		self.grid = grid
		self.pane_size = (self.dims[0]/grid[0],self.dims[1]/grid[1])
		self.grid_coords = [(i*self.pane_size[0],j*self.pane_size[1]) for i in range(grid[0]) for j in range(grid[1])]

		self.sprite_tracker = FaceSpriteTracker(max_sprites=len(self.grid_coords),tolerance=(70,70),maxwait=2,replace_policy=FaceSpriteTracker.RANDOM,fill=True)

	def draw(self,screen) :

		raw_image = self.input.get_curr_frame()
		scaled_raw_image = pygame.transform.scale(raw_image,self.dims)

		screen.fill(THECOLORS["black"])
		faces = self.input.get_polys()

		if len(faces) > 0 :

			for i,face in enumerate(faces) :
				face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
				dims = face[1][0]-face[0][0], face[2][1]-face[1][1]
				faces[i] = pygame.Rect(face[0],dims)

		self.sprite_tracker.update(faces,scaled_raw_image)

		#print 'Sprite ages:',self.sprite_tracker._sprite_ages
		for i,sprite in enumerate(self.sprite_tracker.sprites) :
			scaled_face_surf = pygame.transform.scale(sprite.image,self.pane_size)
			screen.blit(scaled_face_surf,self.grid_coords[i])

		# draw a lattice on top of the pictures
		dk_gray = (30,30,30,30)
		for i in range(self.grid[1]) :
			pygame.draw.aaline(screen,dk_gray,(0,i*self.pane_size[1]),(self.dims[0],i*self.pane_size[1]))
		for i in range(self.grid[0]) :
			pygame.draw.aaline(screen,dk_gray,(i*self.pane_size[0],0),(i*self.pane_size[0],self.dims[1]))

		


if __name__ == "__main__" :
	face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",flip=True)
	driver = AetherDriver(640,input=face_input)
	driver.register_module(FacePanes(driver,grid=(10,6)))
	driver.run()
