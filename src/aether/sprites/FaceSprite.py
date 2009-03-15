import pygame, pygame.sprite

class FaceSprite(pygame.sprite.Sprite) :

	def __init__(self,rect=pygame.Rect(0,0,1,1),lag=10,frame=None) :
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


