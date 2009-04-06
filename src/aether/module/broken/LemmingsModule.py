#!/usr/bin/env python

import pygame, pygame.key, pygame.sprite, pygame.image, pygame.transform
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input
from ildp.util import ShadowSprite, Wall

import math
from random import randint, randrange

class MarblesModule(ILDParamModule) :

  def __init__(self, driver, num_peepers=10, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)

    image_fns = ['images/marble%d.png'%x for x in range(1,2)]
    self.images = [pygame.image.load(s) for s in image_fns]

    self.shadow_sprite = ShadowSprite(driver,draw_polygon=False,draw_rects=True)

    self.sprites = pygame.sprite.Group()
    for im in self.images :
      self.sprites.add(MarbleSprite(im,randint(0,self.dims[0]),-10))

    self.walls = pygame.sprite.Group()
    #self.walls.add(Wall(((0,self.dims[1]),(self.dims[0],self.dims[1])),draw=True))
    #self.walls.add(Wall(((0,0),(0,self.dims[1])),draw=True))
    #self.walls.add(Wall(((self.dims[0],self.dims[1]),(self.dims[0],0)),draw=True))

  def draw(self,screen) :

    # erase what was there before
    screen.fill((200,200,255,255))

    # update shadow
    self.shadow_sprite.draw_update(screen)

    # check with each marble if it's colliding
    for s in self.sprites :
      s.check_for_collision(self.shadow_sprite.edges)
      #pygame.draw.rect(screen,(0,0,0),s.rect,2)
      s.check_for_collision(self.walls)

    # update sprites
    self.sprites.draw(screen)
    self.sprites.update()

    # update walls
    self.walls.draw(screen)

  def process_event(self,event) :
    #if event.type == KEYDOWN and event.key == K_r :
    #  pass
    #  return True
    return False


def _pixelPerfectCollisionDetection(sp1,sp2):
  """
  Internal method used for pixel perfect collision detection.
  """
  rect1 = sp1.rect;
  rect2 = sp2.rect;
  rect  = rect1.clip(rect2)

  #hm1 = pygame.surfarray.array_colorkey(sp1.image)
  #hm2 = pygame.surfarray.array_alpha(sp2.image)
  hm1 = sp1.hitmask
  hm2 = sp2.hitmask

  x1 = rect.x-rect1.x
  y1 = rect.y-rect1.y
  x2 = rect.x-rect2.x
  y2 = rect.y-rect2.y

  for r in range(0,rect.height):
    for c in range(0,rect.width):
      if hm1[c+x1][r+y1] & hm2[c+x2][r+y2]:
        return 1

  return 0

class MarbleSprite(pygame.sprite.Sprite) :

  LEFT,RIGHT = 0,1
  def __init__(self,image,x,y,d=(0,0),g=(0,.5),terminal_v=(20,20)) :
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.transform.scale(image,(50,50))
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.velocity = self.dx,self.dy = d
    self.gravity = self.gx, self.gy = g
    self.terminal_velocity = self.term_vx, self.term_vy = terminal_v

    # custom hitmask because we only want the bottom of the sprite to interact
    #self.hitmask = pygame.surfarray.array_alpha(self.image)
    self.hitmask = []
    for i in range(self.rect.height-1) :
      self.hitmask.append([0]*self.rect.width)
    self.hitmask.append([0]*(self.rect.width/2-2)+[255]*4+[0]*(self.rect.width/2-2))

    self.direction = MarbleSprite.LEFT

  def update(self) :

    if self.dx < self.term_vx :
      self.dx += self.gx

    if self.dy < self.term_vy :
      self.dy += self.gy

    self.rect.center = self.rect.center[0]+self.dx,self.rect.center[1]+self.dy

    if self.rect.center[1] > 600 :
      self.velocity = self.dx, self.dy = (0,0)
      self.rect.center = randrange(0,600),-20

    #self.hitmask = pygame.surfarray.array_alpha(self.image)

  def check_for_collision(self,group) :
    self.collide_edges = []

    for e in group :
      if self.rect.colliderect(e.rect) :
        if _pixelPerfectCollisionDetection(e,self) :
          self.collide_edges.append(e)

    if len(self.collide_edges) != 0 :
      l = self.collide_edges[0]
      self.velocity = self.dx, self.dy = l.slope[0]*2,l.slope[1]*2
      #self.velocity = self.dx, self.dy = self.dx-l.normal[0]*5,self.dy-l.normal[1]*5
      #dot = 2*(l.normal[0]*self.dx+l.normal[1]*self.dy)
      #self.velocity = self.dx,self.dy = self.dx-l.normal[0]*dot,self.dy-l.normal[1]*dot
      #self.velocity = self.dx,self.dy = self.dx*0.7,self.dy*0.7

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=True)
  driver.register_module(MarblesModule(driver))
  driver.run()
