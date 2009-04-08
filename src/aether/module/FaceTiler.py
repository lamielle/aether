
from aether.core import AetherDriver, AetherModule
from aether.sprites import FaceSprite, FaceSpriteTracker

import pygame.image, pygame.font, pygame.sprite, pygame.transform, pygame.draw
from pygame.color import THECOLORS

class FaceTiler(AetherModule) :

	chains={'faces':'FacesChain','camera':'ScaledCameraChain'}

	def init(self):
		self.grid = (3,2)
		self.pane_size = (self.dims[0]/self.grid[0],self.dims[1]/self.grid[1])
		self.grid_coords = [(i*self.pane_size[0],j*self.pane_size[1]) for i in range(self.grid[0]) for j in range(self.grid[1])]

		self.sprite_tracker = FaceSpriteTracker(max_sprites=len(self.grid_coords),tolerance=self.pane_size,maxwait=5,replace_policy=FaceSpriteTracker.RANDOM,fill=True)

	def draw(self,screen) :

		frame=self.camera.read()

		screen.fill(THECOLORS["black"])

		faces = self.faces.read()

		for i,face in enumerate(faces) :
			face = [(int(x[0]*self.dims[0]),int(x[1]*self.dims[1])) for x in face]
			dims = face[1][0]-face[0][0], face[2][1]-face[1][1]
			faces[i] = pygame.Rect(face[0],dims)

		self.sprite_tracker.update(faces,frame)

		print 'Sprite ages:',self.sprite_tracker._sprite_ages
		for i,sprite in enumerate(self.sprite_tracker.sprites) :
			scaled_face_surf = pygame.transform.scale(sprite.image,self.pane_size)
			screen.blit(scaled_face_surf,self.grid_coords[i])

		# draw a lattice on top of the pictures
		dk_gray = (30,30,30,30)
		for i in range(self.grid[1]) :
			pygame.draw.aaline(screen,dk_gray,(0,i*self.pane_size[1]),(self.dims[0],i*self.pane_size[1]))
		for i in range(self.grid[0]) :
			pygame.draw.aaline(screen,dk_gray,(i*self.pane_size[0],0),(i*self.pane_size[0],self.dims[1]))
