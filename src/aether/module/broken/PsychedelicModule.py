#!/usr/bin/env python

import pygame, pygame.key
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

import math
from math import cos,sin,pi
from random import randint

class PsychedelicModule(ILDParamModule):

  def __init__(self, driver, num_peepers=10, **kwargs):
    ILDParamModule.__init__(self,driver,**kwargs)

    self.limitX = self.dims[0]
    self.limitY = self.dims[1]

    self.reset()

  def reset(self):
    self._screen=pygame.Surface(self.dims)
    self.count=0
    self.speed=randint(5,20)
    self.fill_color=self.random_color()
    self.shadowsize=1
    self.increment=[self.speed]*4
    self.shadowincrement=[self.speed]*4
    self.color=self.random_color()
    self.shadow_color=self.random_color()
    self.loc=[randint(0,self.limitX-1),
              randint(0,self.limitY-1),
              randint(0,self.limitX-1),
              randint(0,self.limitY-1)]
    self.shadowloc=[self.loc[0],self.loc[1],self.loc[2],self.loc[3]]

  def draw_lines(self,screen,loc,color):
    pygame.draw.line(screen,color,(loc[0],loc[1]),(loc[2],loc[3]))
    pygame.draw.line(screen,color,(self.limitX - loc[0], loc[1]), (self.limitX - loc[2], loc[3]))
    pygame.draw.line(screen,color,(loc[0], self.limitY - loc[1]), (loc[2], self.limitY - loc[3]))
    pygame.draw.line(screen,color,(self.limitX - loc[0], self.limitY - loc[1]), (self.limitX - loc[2], self.limitY - loc[3]))

  def random_color(self):
    return [randint(10, 250), randint(10, 250), randint(10, 250)]

  def random_pygame_color(self):
    color=self.random_color()
    return pygame.Color(color[0],color[1],color[2])

  def draw_shadow_lines(self,screen):
    change_color=randint(0,2)
    lower=(self.shadow_color[change_color]-5)%255
    upper=(self.shadow_color[change_color]+5)%255
    if upper<lower: upper,lower=lower,upper
    self.shadow_color[change_color]=randint(lower,upper)
    self.draw_lines(screen,self.shadowloc,self.shadow_color)

  def check(self, location, index, increment, criteria, initvalue):
    collision = False
    if criteria():
      increment[index] = increment[index] * -1
      location[index] = initvalue
      collision = True
    return collision

  def update(self, location, increment, updatecolor=True):
    location[0] = location[0] + increment[0]
    collision = self.check(location, 0, increment, lambda: location[0] >= self.limitX, self.limitX-1)
    collision = collision or self.check(location, 0, increment, lambda: location[0] <= 0, 0)

    location[1] = location[1] + increment[1]

    collision = collision or self.check(location, 1, increment, lambda: location[1] >= self.limitY, self.limitY-1)
    collision = collision or self.check(location, 1, increment, lambda: location[1] <= 0, 0)

    location[2] = location[2] + increment[2]

    collision = collision or self.check(location, 2, increment, lambda: location[2] >= self.limitX, self.limitX-1)
    collision = collision or self.check(location, 2, increment, lambda: location[2] <= 0, 0)

    location[3] = location[3] + increment[3]

    collision = collision or self.check(location, 3, increment, lambda: location[3] >= self.limitY, self.limitY-1)
    collision = collision or self.check(location, 3, increment, lambda: location[3] <= 0, 0)

    if collision and updatecolor: self.color = self.random_color()

  def wavy_circle(self,center,radius,wavyness,compress,num_points):
    x=float(center[0])
    y=float(center[1])
    for theta in xrange(0,360,int(360/num_points)):
      theta=float(theta)
      pt_x=x+sin(theta*(2*pi/360))*radius
      pt_y=y+cos(theta*(2*pi/360))*radius
      #Make the point wavy based on cosine
      pt_x+=wavyness*cos(compress*theta*(2*pi/360))
      pt_y+=wavyness*cos(compress-1*theta*(2*pi/360))
      yield (int(pt_x),int(pt_y))

  def draw(self,screen):
    self.count+=1
    if 100==self.count: self.reset()
    if self.fill_color:
      self._screen.fill(self.fill_color)
      self.fill_color=None
    self.update(self.loc,self.increment)
    self.draw_lines(self._screen,self.loc,self.color)
    if self.shadowsize>0:
      self.shadowsize=self.shadowsize-1
    else:
      self.draw_shadow_lines(self._screen)
      self.update(self.shadowloc,self.shadowincrement,False)

    screen.blit(self._screen,(0,0))

    # draw the shadow
    center=self.input.com()
    pygame.draw.circle(screen,THECOLORS["red"],self.input.com(),3)
    for pt in self.input.verts():
#      for pt in self.wavy_circle(pt,50.0,5.0,8.0,100.0):
#        pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)
      pygame.draw.polygon(screen,self.random_pygame_color(),tuple(self.wavy_circle(pt,20.0,8.0,8.0,100.0)))
#    shadow_pts=self.input.verts()
#    if len(shadow_pts)>2: pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
#    for pt in shadow_pts:
#      pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)


  def process_event(self,event):
    if event.type == KEYDOWN and event.key == K_r:
      self.reset()
      return True
    return False

if __name__ == '__main__':
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=False)
  driver.register_module(PsychedelicModule(driver))
  driver.run()
