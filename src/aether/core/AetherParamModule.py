from aether.core import AetherModule
from aether.core import AetherSettings
import pygame
from pygame.locals import *

class AetherParamModule(AetherModule) :
  """ 'abstract' subclass of AetherModule that includes support for screen and parameter panels
  """

  def __init__(self, driver, **kwargs) :
    AetherModule.__init__(self, driver, **kwargs)
    self.show_params = False

    #These need to be updated as they were moved from the top
    from ocempgui.widgets import Window,Button
    from ocempgui.widgets.Constants import SIG_CLICKED

    # parameter window stuff
    self.offscreen = pygame.Surface(self.dims)
    self.re = Renderer()
    self.re.screen = driver.screen
    self.param_window = Window('Parameters')
    self.param_window.opacity = 0

    def calib_f():
      driver.input.calibrate()

    calib = Button('Calibrate')
    calib.connect_signal(SIG_CLICKED,calib_f)
    button = Button('Close')
    button.connect_signal(SIG_CLICKED,self.toggle_params)

    # add custom widgets
    widgets = self.get_parameter_widgets() 

    if driver.debug :
      from aether.core import InputProvider

      def change_sim_shape(btn) :
        btn.set_active(True)
        if self.person.active : shape = InputProvider.PERSON
        elif self.poly.active : shape = InputProvider.POLY
        else : shape = InputProvider.CIRCLE
        driver.input.sim_shadow_shape = shape

      self.circle = RadioButton("Circle")
      self.circle.active = True # circle is the default
      self.person = RadioButton("Person",self.circle)
      self.poly = RadioButton("Polygon",self.circle)

      self.circle.connect_signal(SIG_CLICKED,change_sim_shape,self.circle)
      self.person.connect_signal(SIG_CLICKED,change_sim_shape,self.person)
      self.poly.connect_signal(SIG_CLICKED,change_sim_shape,self.poly)
      widgets.append(self.circle)
      widgets.append(self.person)
      widgets.append(self.poly)

    else :
      widgets.append(calib)

    widgets.append(button)
    t = Table(len(widgets),1)
    for i,w in enumerate(widgets) :
      t.add_child(i,0,w)

    self.param_window.child = t
    self.re.add_widget(self.param_window)

  def _draw_delegate(self,screen) :
    self.draw(screen)
    self.re.update()
    if self.show_params :
      self.re.screen = screen
    else :
      self.re.screen = self.offscreen

  def toggle_params(self) :
    self.show_params = not self.show_params
    self.param_window.opacity = (0,200)[self.show_params]

  def draw(self,screen) :
    pass

  def _process_event_delegate(self,event) :
    if event.type == KEYDOWN and event.key == K_p :
      self.toggle_params()
    elif not self.process_event(event) :
      self.re.distribute_events(event)

  def process_event(self,event) :
    return False

  def get_parameter_widgets(self) :
    return []
