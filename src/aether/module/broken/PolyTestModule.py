#!/usr/bin/env python

import pygame, pygame.key, pygame.draw, pygame.mouse
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

import math
from random import randint

def expand_edge(p1,p2,d=2,ends=True) :

  length = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
  dvec = (d*p1[0]/length,d*p1[1]/length)

  num_pts = int(length/d)

  pts = [p1]

  for i in range(num_pts) :
    pt = (pts[-1][0]+dvec[0],pts[-1][1]+dvec[1])
    pts.append(pt)

  pts.append(p2)

  if ends :
    pts = pts[1:-1]

  return pts

class PolyTestModule(ILDParamModule) :

  def __init__(self, driver, num_peepers=10, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)


  def draw(self,screen) :
    screen.fill((200,200,255,255))

    # draw the different polygons
    shadow_polys = self.input.polys()
    for p in shadow_polys :
      shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],p)
      for pt in p :
        pygame.draw.circle(screen,THECOLORS["red"],tuple([int(i) for i in pt]),3)

    # draw the shadow
    shadow_pts = self.input.verts()
    mpos = pygame.mouse.get_pos()
    shadow_pts =
    shadow_rect = None
    if len(shadow_pts) > 2 : shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
    #if shadow_rect is not None : pygame.draw.rect(screen,THECOLORS["blue"],shadow_rect,1)
    for pt in shadow_pts :
      pygame.draw.circle(screen,THECOLORS["blue"],tuple([int(i) for i in pt]),3)

    # draw the expanded pts
    expanded_pts = []
    for i in range(len(shadow_pts)) :
      expanded_pts.append(expand_edge(shadow_pts[i],shadow_pts[(i+1)%len(shadow_pts)],ends=False))
    print expanded_pts
    for pts in expanded_pts :
      pygame.draw.circle(screen,THECOLORS["green"],tuple([int(i) for i in pt]),3)

    # draw the com
    shadow_com = self.input.com()
    print shadow_com
    if shadow_com is not None : pygame.draw.circle(screen,THECOLORS["white"],tuple((int(i) for i in shadow_com)),3)

  def process_event(self,event) :
    if event.type == KEYDOWN and event.key == K_r :
      self.build_some_peepers()
      return True
    return False

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=True)
  #s=Settings(150,[(30,30),(70,30),(70,70),(30,70)])
  #driver.input.calibrate()
  driver.register_module(PolyTestModule(driver))
  driver.run()
