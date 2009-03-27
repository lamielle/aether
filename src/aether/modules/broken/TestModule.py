from aether.core import AetherModule

class TestModule(AetherModule):

	def __init__(self, driver, color, **kwargs) :
		AetherModule.__init__(self,driver,**kwargs)
		self.driver = driver
		self.title = 'TestAetherModule'
		self.color = color
		self.letter = 'A'

	def draw(self,screen) :
		screen.fill(self.color)
		font = pygame.font.Font(None, 256)
		text = font.render(self.letter, 1, (10, 10, 10))
		textpos = text.get_rect(centerx=screen.get_width()/2,centery=screen.get_height()/2)
		screen.blit(text, textpos)

	def process_event(self,event) :
		if event.type == KEYDOWN :
			self.letter = pygame.key.name(event.key)
			return True
