import pygame
from pygame.color import THECOLORS
from ildp.core import ILDModule

class StubModule(ILDModule) :
  """Stub module that simply draws a point for the center of mass
  """

  def __init__(self, driver, **kwargs) :
    #Initalize paremt class
    ILDModule.__init__(self,driver,**kwargs)

  def draw(self,screen) :
    com=self.input.get_com()

    #Draw the center of mass
    pygame.draw.circle(screen,THECOLORS["white"],com,5)
