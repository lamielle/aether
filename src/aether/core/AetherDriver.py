import pygame, os, sys
from pygame.locals import *
from pygame.color import *
from pygame.image import tostring
import pygame.mouse
import Image
import aether,aether.core
from aether.core import AetherObject
from aether.error import AetherComponentLoadError

class AetherDriver(AetherObject):
	"""The driver class for Aether. This class contains the pygame event loop that drives each Aether module.
	"""

	def __init__(self):
		self.modules=[]

	#Attempts to load, create, and register each module that is specified in the settings
	def load_modules(self):
		#Update sys.path with the directories specified in aether.dirs
		self.update_path()

		#Try to import each module specified in the settings
		for mod_name in self.settings.aether.modules:
			#Create an instance of the module
			module=self.create_component(mod_name,mod_name)

			#Register the module
			self.register_module(module)

			#Recursively create the dependences for this module
			self.create_deps(module)

	#Attempts to create an instance of the component of the given name
	def create_component(self,class_name,comp_name):
		try:
			#Import the module (file) that the component is in
			exec('from %s import %s'%(class_name,class_name))
			self.debug_print("Imported component '%s'..."%(class_name))

			try:
				#Create an instance of the component
				exec('component=%s()'%(class_name))
				self.debug_print("Created component '%s'..."%(class_name))
			except Exception,e:
				raise AetherComponentLoadError("Error while instantiating component '%s'..."%(class_name),e)
		except ImportError,e:
			raise AetherComponentLoadError("Could not import component '%s'..."%(class_name),e)
		except Exception,e:
			raise AetherComponentLoadError("Error while importing component '%s': %s"%(class_name,e),e)

		#Setup default settings for the component
		component.name=comp_name
		try:
			for name,value in component.defaults.items():
				setattr(getattr(AetherObject.settings,component.name),name,value)
		except AttributeError,e: pass

		#Tell the component to initalize
		try:
			component.init()
		except AttributeError,e: pass

		return component

	#Reigsters a module with Aether
	def register_module(self,module):
		self.debug_print("Registering module '%s'..."%(module.__module__))
		self.modules.append(module)

	#Creates the dependences for the given component (module or input provider)
	def create_deps(self,component):
		#Create dependences recursively for the given component
		try:
			for dep in component.deps:
				dep_component=self.create_component(dep[0],dep[1])
				setattr(component,dep[1],dep_component)
				self.create_deps(dep_component)
		except AttributeError,e: pass

	def run(self):
		#Attempt to load the modules specified in settings
		self.load_modules()

		#Make sure we have one or more modules ready to run
		if 0==len(self.modules):
			raise AetherComponentLoadError('Aether must have at least one module registered to run.')

		#Initialize pygame
		pygame.init()

		#Setup the screen
		self.screen=pygame.display.set_mode(self.dims)

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
