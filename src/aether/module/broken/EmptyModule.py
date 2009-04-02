#!/usr/bin/env python

import pygame, pygame.key
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

import math
from random import randint

class EmptyModule(ILDParamModule) :

  def __init__(self, driver, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)

  def draw(self,screen) :
    screen.fill((200,200,255,255))

    # draw the shadow
    shadow_pts = self.input.verts()
    if len(shadow_pts) > 2 : pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
    for pt in shadow_pts :
      pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)

  def process_event(self,event) :
    if event.type == KEYDOWN and event.key == K_r :
      self.build_some_peepers()
      return True
    return False

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=True)
  #s=Settings(150,[(30,30),(70,30),(70,70),(30,70)])
  driver.input.calibrate()
  driver.register_module(EmptyModule(driver))
  driver.run()
