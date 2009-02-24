import pygame, os, sys
from pygame.locals import *
from pygame.color import *
from pygame.image import tostring
import pygame.mouse
import Image
import aether,aether.core,aether.modules
from aether.core import InputProvider

class AetherDriver :
  """The driver class for the Interactive Light Display system.  This class controls the pygame event loop that drives each of its component AetherModules.  Example usage::

    driver = AetherDriver(640,DiffProviderSimulator())
    driver.register_module(TestAetherModule(driver,THECOLORS["blue"]))
    driver.register_module(PymunkModule(driver))
    driver.register_module(TestAetherModule(driver,THECOLORS["white"]))
    driver.run()

The above instantiates an AetherDriver object with screen width of 640 pixels and a DiffProviderSimulator that does not require a connected camera.  If a camera is attached and all the necessary supporting software is available the DiffProvider object will fetch images and translate them into something potentially useful.  See DiffProvider and AetherCalibrationModule documentation for more details.

See the appropriate documentation for TestAetherModule and PymunkModule modules.
  """

  def __init__(self,height,modules=[],debug=False) :
    pygame.init()
    self.dims = (height,int(height*.75))
    self.screen = pygame.display.set_mode(self.dims)
    self.modules = modules
    self.input=InputProvider(dims=self.dims,settings_file_name='settings.cfg',debug=debug)
    self.debug = debug

  def register_module(self,module) :
    """wtf mate?
    """

    self.modules.append(module)

  def run(self) :

    if len(self.modules) == 0 :
      raise Exception('AetherDriver must have at least one module registered.')

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
