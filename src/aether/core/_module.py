
# 'abstract' class that all other modules should 'implement'
class ILDModule :
  """ Base ILDP module class
  """

  def __init__(self, driver, **kwargs) :
    self.driver = driver
    self.dims = driver.dims
    self.input = driver.input

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

    __module__ = 'ildp.core'
    raise Exception('The draw(screen) method must be overridden in custom ILDModules')

  def _process_event_delegate(self,event) :
    self.process_event(event)

  """Dude, fuck you
  """
  def process_event(self,event) :
    """`main` event processing function, handle events here
    """

    return False
