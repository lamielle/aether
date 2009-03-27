from aether.core import AetherObject

# 'abstract' class that all other modules should inherit from
class AetherModule(AetherObject):
	""" Base Aether module class
	"""

	def get_verts(self) :
		return self.driver.get_verts()

	def activate(self) :
		"""setup module when switching between modules
		"""

		pass

	def deactivate(self) :
		"""cleanup module when switching between modules
		"""

		pass

	def _draw_delegate(self,screen) :
		self.draw(screen)

	def draw(self,screen) :
		"""main draw method, do everything here
		"""
		raise Exception('The draw(screen) method must be overridden in custom AetherModules')

	def _process_event_delegate(self,event) :
		self.process_event(event)

	def process_event(self,event) :
		"""`main` event processing function, handle events here
		"""

		return False
