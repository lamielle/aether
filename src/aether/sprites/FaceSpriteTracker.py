from aether.sprites import FaceSprite
from random import randrange

class FaceSpriteTracker :

	RANDOM = "Random"
	LOWEST = "Lowest"
	HIGHEST = "Highest"

	def __init__(self,max_sprites=10,tolerance=(10,10),maxwait=10,replace_policy=LOWEST,fill=False) :

		if fill :
			self.sprites = [FaceSprite() for i in range(max_sprites)]
			self._sprite_ages = [0]*max_sprites
		else :
			self.sprites = []
			self._sprite_ages = []
		self.max_sprites = max_sprites
		self.tolerance = tolerance
		self.maxwait = maxwait
		self.policy = replace_policy

	def get_sprite(self,rect) :
		for i,s in enumerate(self.sprites) :
			if self._sprite_ages[i] != 0 and \
				all([abs(s.face_rect.x-rect.x) < self.tolerance[0],abs(s.face_rect.y-rect.y) < self.tolerance[1]]) :
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
						if self.policy == FaceSpriteTracker.LOWEST :
							to_replace = self._sprite_ages.index(0)
						elif self.policy == FaceSpriteTracker.HIGHEST :
							self._sprite_ages.reverse()
							to_replace == self._sprite_ages.index(0)
							self._sprite_ages.reverse()
						else :
							self._sprite_ages.index(0) # just to make sure 0 is in the list
							to_replace_lst = [i for i,x in enumerate(self._sprite_ages) if x == 0]
							to_replace = to_replace_lst[randrange(len(to_replace_lst))]

						#print 'Replacing %d of %d(%d)'%(to_replace,self._sprite_ages.count(0),len(self._sprite_ages))
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



