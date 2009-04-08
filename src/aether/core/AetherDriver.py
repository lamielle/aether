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
		#List of registered modules
		self.registered_modules=[]

		#Dictionary mapping transform names to transform instances
		self.registered_transforms={}

	#Attempts to create an instance of the class of the given name
	#This method involves two steps:
	#1) Imports the given class from a module of the same name: from class_name import class_name
	#2) Creates an instance of the imported class
	#This class must not require any parameters in its constructor
	#If any of these steps fails, an AetherComponentLoadError is raised
	#On success the object that was created is returned
	def create_instance(self,class_name):
		try:
			#Import the module (file) that the class is in
			exec('from %s import %s'%(class_name,class_name))
			self.debug_print("Imported class '%s'..."%(class_name))

			try:
				#Create an instance of the class
				exec('instance=%s()'%(class_name))
				self.debug_print("Created instance of class '%s'..."%(class_name))
			except Exception as e:
				raise AetherComponentLoadError("Error while instantiating class '%s'..."%(class_name),e)
		except ImportError as e:
			raise AetherComponentLoadError("Could not import class '%s'..."%(class_name),e)
		except Exception as e:
			raise AetherComponentLoadError("Error while importing class '%s': %s"%(class_name,e),e)

		return instance

	#Attempts to create and setup each module that is specified in the settings
	def load_modules(self):
		#Setup each module that should be run
		for mod_class in self.modules:
			#Create the module
			module=self.create_instance(mod_class)

			#Setup the module
			self.setup_module(module)

	#Sets up the given module:
	#-Creates and sets up all chains the module needs
	#-Registers the module
	def setup_module(self,module):
		#Define the 'name' of a module to be its class name
		module.name=module.__class__.__name__

		#Create the chains the module depends on
		try:
			for chain_name,chain_class in module.chains.items():
				#Create the chain
				chain=self.create_instance(chain_class)

				#Setup the chain
				self.setup_chain(chain)

				#Assign the chain the the proper field in the module
				self.assign_chain(module,chain_name,chain)
		except AttributeError as e:
			#Problem while setting up chains
			raise AetherComponentLoadError("Error while setting up chains for module '%s'..."%(module.name),e)
		else:
			#Setting up chains went fine (no exceptions raised)

			#Tell the module to init
			self.call_init(module)

			#Register the module
			self.register_module(module)

	#Attempts to call the init method of the given target object
	def call_init(self,target):
		#Get the init method of the targets's class
		try:
			init_method=target.__class__.init
		except AttributeError as e: pass
		else:
			#Call the init method since we found one
			init_method(target)

	#Sets up the given chain:
	#-Loads any settings specified by the chain
	#-Creates instances of all transforms needed for the chain
	#-Sets up each transform
	def setup_chain(self,chain):
		#Load settings values for this chain
		try:
			transform_settings=chain.transform_settings
		except AttributeError as e: pass
		else:
			#We found transform settings, load them now
			#For each settings section/values dict
			for section_name,section_settings in transform_settings.items():
				self.settings_load(section_name,section_settings,test_exists=True)

		print self.settings

		#Create each transform in the chain
		for trans_name,trans_class in chain.transforms.items():
			#Create the transform
			transform=self.create_instance(trans_class)

			#Setup the transform
			self.setup_transform(transform,trans_name)

			#Register the transform
			self.register_transform(transform)

		#Setup the dependences between the transforms in this chain
		self.setup_transform_deps(chain.transform_deps)

	#Sets up the given transform:
	#-Sets the transform's name so it's specific settings may be accessed directly
	#-Sets the transform's default settings
	def setup_transform(self,transform,trans_name):
		#Set the transform's name
		transform.name=trans_name

		#Setup default settings for the transform
		try:
			defaults=transform.defaults
		except AttributeError as e: pass
		else:
			self.settings_load(transform.name,defaults,test_exists=True)

		self.call_init(transform)

	#Sets up the dependences between transforms
	#The dependences should be given as a dictionary mapping
	# transform names to a collection of transforms that the
	# transform depends on
	#Ex: {'transform_name':('depends_on_1','depends_on_2')}
	def setup_transform_deps(self,deps):
		#For each collection of dependences
		for transform_name,transform_deps in deps.items():
			#For each dependence
			for transform_dep_pos in xrange(len(transform_deps)):
				#Get the name of the transform dependence
				transform_dep_name=transform_deps[transform_dep_pos]

				self.debug_print("Setting up dependence from transform '%s' to transform '%s'..."%(transform_name,transform_dep_name))

				#Get the transform instances
				transform=self.registered_transforms[transform_name]
				transform_dep=self.registered_transforms[transform_dep_name]

				#Get the local name of the dependence
				transform_dep_name_local=transform.input_names[transform_dep_pos]

				#Assign the dependences to the transform
				self.debug_print("Assigning transform '%s' to field '%s' of transform '%s'..."%(transform_dep_name,transform_dep_name_local,transform_name))
				setattr(transform,transform_dep_name_local,transform_dep)

	#Assigns the given chain to the given field name in the given module
	def assign_chain(self,module,chain_name,chain):
		setattr(module,chain_name,self.registered_transforms[chain.start])

	#Registers a transform with Aether
	def register_transform(self,transform):
		self.debug_print("Registering transform '%s(%s)'..."%(transform.name,transform.__class__.__name__))
		self.registered_transforms[transform.name]=transform

	#Registers a module with Aether
	def register_module(self,module):
		self.debug_print("Registering module '%s'..."%(module.__module__))
		self.registered_modules.append(module)

	#Run Aether!
	def run(self):
		#Update sys.path with the directories specified in aether.dirs
		self.update_path()

		#Attempt to load the modules specified in settings
		self.load_modules()

		#Make sure we have one or more modules ready to run
		if 0==len(self.registered_modules):
			raise AetherComponentLoadError('Aether must have at least one module registered to run.')

		#Initialize pygame
		pygame.init()

		#Setup the screen
		self.screen=pygame.display.set_mode(self.dims)

		clock = pygame.time.Clock()
		running = True

		mod_index = 0
		self.curr_module = self.registered_modules[mod_index]

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
					mod_index = (mod_index+1)%len(self.registered_modules)
					self.curr_module = self.registered_modules[mod_index]
					self.curr_module.activate()
				else :
					self.curr_module._process_event_delegate(event)

			self.curr_module._draw_delegate(self.screen)

			pygame.display.flip()
			clock.tick(50)
