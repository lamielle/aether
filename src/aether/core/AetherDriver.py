import pygame, os, sys
from pygame.locals import *
from pygame.color import *
from pygame.image import tostring
import pygame.mouse
import Image
import aether,aether.core,aether.modules
from aether.core import AetherObject,InputProvider
from aether.error import AetherModuleLoadError

class AetherDriver(AetherObject):
	"""The driver class for Aether. This class contains the pygame event loop that drives each Aether module.
	"""

	def __init__(self):
		self.modules=[]
		self.dims=(self.settings.aether.width,self.settings.aether.height)

		#Initialize pygame
		pygame.init()

		#Setup the screen
		self.screen=pygame.display.set_mode(self.dims)

	#Loads default settings values
	def load_defaults(self):
		self.debug_print('Setting up some default settings values...')
		self.settings.aether.mod_dirs=[aether.base_dir+os.sep+'modules']+self.settings.aether.mod_dirs
		self.settings.aether.data_dirs=[aether.base_dir+os.sep+'data']+self.settings.aether.data_dirs

	#Attempts to load, create, and register each module that is specified in the settings
	def load_modules(self):
		#Update sys.path with the module directories specified in aether.mod_dirs
		self.update_path()

		#Try to import each module specified in the settings
		for mod_name in self.settings.aether.modules:
			try:
				exec('from %s import %s'%(mod_name,mod_name))
				self.debug_print("Imported module '%s'..."%(mod_name))

				#Create an instance of the module and register it
				try:
					exec('module=%s()'%(mod_name))
					self.register_module(module)
				except Exception,e:
					raise AetherModuleLoadError("Error while instantiating module '%s'..."(mod_name),e)
			except ImportError,e:
				raise AetherModuleLoadError("Could not import module '%s'..."%(mod_name),e)
			except Exception,e:
				raise AetherModuleLoadError("Error while importing module '%s': %s"%(mod_name,e),e)

	#Reigsters a module with Aether
	def register_module(self,module):
		self.debug_print("Registering module '%s'..."%(module.__module__))
		self.modules.append(module)

	#Sets up input sources
	def setup_input(self):
		#This is hard-coded now to use FaceInputProvider for input
		#This will be changed in the future
		from aether.core import FaceInputProvider
		face_input=FaceInputProvider()

		#Set the 'input' and 'dims' fields on all loded modules
		for module in self.modules:
			module.input=face_input
			module.dims=self.dims

	def run(self):
		#Load default settings for Aether
		self.load_defaults()

		#Attempt to load the modules specified in settings
		self.load_modules()

		if 0==len(self.modules):
			raise AetherModuleLoadError('Aether must have at least one module registered to run.')

		#Setup the inputs for the modules
		self.setup_input()

		clock = pygame.time.Clock()
		running = True

		mod_index = 0
		self.curr_module = self.modules[mod_index]

		# do the main loop
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					running = False
				elif event.type == KEYDOWN and event.key == K_q :
					running = False
				elif event.type == KEYDOWN and event.key == K_f :
					pygame.display.toggle_fullscreen()
				elif event.type == KEYDOWN and event.key == K_c :
					# yes, this actually toggles mouse visibility
					pygame.mouse.set_visible(not pygame.mouse.set_visible(True))
				elif event.type == KEYDOWN and event.key == K_s :
					self.curr_module.deactivate()
					mod_index = (mod_index+1)%len(self.modules)
					self.curr_module = self.modules[mod_index]
					self.curr_module.activate()
				else :
					self.curr_module._process_event_delegate(event)

			self.curr_module._draw_delegate(self.screen)

			pygame.display.flip()
			clock.tick(50)
