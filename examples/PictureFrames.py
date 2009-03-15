
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


class FaceSpriteTracker :

	def __init__(self,max_sprites=10,tolerance=(10,10),maxwait=10) :
		self.sprites = []
		self._sprite_ages = []
		self.max_sprites = max_sprites
		self.tolerance = tolerance
		self.maxwait = maxwait

	def get_sprite(self,rect) :
		for i,s in enumerate(self.sprites) :
			if self._sprite_ages[i] != 0 and \
				all([abs(s.face_pos[0]-rect.x) < self.tolerance[0],abs(s.face_pos[1]-rect.y) < self.tolerance[1]]) :
				return s
		return None

	def update(self,rects,image) :
		# look through each rect passed
		for r in rects :
			# try to locate the sprite that is likely to be associated with the rect
			sprite = self.get_sprite(r)

			# None means we didn't find a sprite close enough
			if sprite is None :

				# if our list of sprites hasn't reached its capacity yet, append a new one
				if len(self.sprites) < self.max_sprites :
					self.sprites.append(FaceSprite(r,image))
					self._sprite_ages.append(self.maxwait)

				# if we have reached capacity, replace the first dead sprite with this one
				else :

					# list.index(value) throws an error if it doesn't contain the value you're looking for
					try :
						to_replace = self._sprite_ages.index(0)

						# new sprite and reset the age
						self.sprites[to_replace] = FaceSprite(r,image)
						self._sprite_ages[to_replace] = self.maxwait
					except ValueError :
						pass

			# we found a sprite, reset its age and update it
			else :
				sprite_id = self.sprites.index(sprite)
				self._sprite_ages[sprite_id] = self.maxwait
				sprite.update(r,image)

		# age all the sprites
		self._sprite_ages = [max(0,x-1) for x in self._sprite_ages]


class FaceSprite(pygame.sprite.Sprite) :

	def __init__(self,rect,lag=10,frame=None) :
		pygame.sprite.Sprite.__init__(self)

		self.rect = rect
		self.rect.topleft = rect.x,rect.y
		self.face_pos = self.rect.topleft

		self.lag = lag
		self.history = [rect]

		if frame is None :
			self.image = pygame.Surface((1,1))
		else :
			self.update(rect,frame)

	def update(self,rect,frame) :


		# calculate running average
		if len(self.history) > self.lag :
			self.history.pop(0)
		self.history.append(rect)
		width = sum([x.width for x in self.history])/len(self.history)
		height = sum([x.height for x in self.history])/len(self.history)

		# if change in dimensions is less than some threshold, don't change the dims
		#TODO deltas may eventually be settings, but they work pretty well for this use case
		delta = 3
		last_rect = self.history[-2]
		if all([abs(last_rect.width-width) < delta, abs(last_rect.height - rect.height)]) :
			rect.size = last_rect.size

		# if change in position is less than some threshold, don't move the box
		delta = 5
		if all([abs(last_rect.x-rect.x) < delta,abs(last_rect.y-rect.y)]) :
			rect.topleft = last_rect.topleft

		# record the face position before we add a margin to the rect
		self.face_pos = rect.topleft

		# add a margin around the rect so we get more of the face
		# TODO these might be settings eventually too
		top,bottom,left,right = 50,26,26,26
		m_x = max(0,rect.x-left)
		m_y = max(0,rect.y-top)
		m_w = min(frame.get_rect().width-m_x,width+left+right)
		m_h = min(frame.get_rect().height-m_y,height+top+bottom)
		self.rect = pygame.Rect(m_x,m_y,m_w,m_h)

		self.image = frame.subsurface(self.rect)


if __name__ == "__main__" :
	face_input = FaceInputProvider(0,(640,480),"/home/labadorf/development/aether/examples/haarcascade_frontalface_alt.xml",flip=True)
	driver = AetherDriver(640,input=face_input)
	driver.register_module(PictureFrames(driver))
	driver.run()
