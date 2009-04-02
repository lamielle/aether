#!/usr/bin/env python

import pygame, pygame.key, pygame.sprite, pygame.image, pygame.transform
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

import math
from random import randint, uniform, randrange

class EncouragerModule(ILDParamModule) :

  def __init__(self, driver, num_peepers=10, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)
    dims = driver.dims

    # put the magic box in the middle
    self.strip = pygame.Rect(0,0,50,50)
    self.strip.center = (dims[0]/2,dims[1]/2)

    # load up images
    image_fns = ['images/e%d.png'%x for x in range(1,14)]
    self.images = [pygame.image.load(s) for s in image_fns]

    # create a bunch of random sprites
    self.sprites = pygame.sprite.Group()
    self.num_sprites = 25
    for s in range(self.num_sprites) :
      self.sprites.add(EncouragementSprite(self.images[randrange(0,len(self.images))],randint(0,dims[0]),randint(0,dims[1])))

    self.in_strip = False


  def draw(self,screen) :
    screen.fill((200,200,255,255))

    rect = pygame.draw.rect(screen,THECOLORS["darkgray"],self.strip)

    # draw the shadow
    shadow_pts = self.input.verts()
    shadow_rect = None
    if len(shadow_pts) > 2 : shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
    for pt in shadow_pts :
      pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)

    if shadow_rect is not None and self.strip.colliderect(shadow_rect) :
      self.unleash_all_hell(screen)
      self.in_strip = True
    else :
      self.in_strip = False

  def unleash_all_hell(self,screen) :
    
    if self.in_strip == False :
      self.sprites.empty()
      for s in range(self.num_sprites) :
        self.sprites.add(EncouragementSprite(self.images[randrange(0,len(self.images))],randint(0,self.dims[0]),randint(0,self.dims[1])))
    self.sprites.draw(screen)
    self.sprites.update()
    pass

  def process_event(self,event) :
    if event.type == KEYDOWN and event.key == K_r :
      self.in_strip = False
      return True
    return False

class EncouragementSprite(pygame.sprite.Sprite) :
  rot_cycle = None
  scale_cycle = None
  def __init__(self,image,x,y) :
    pygame.sprite.Sprite.__init__(self)

    # set the rotation cycle if it hasn't been already
    if self.rot_cycle is None :
      self.rot_cycle = [3]*10 + [-3]*10
    self.rot_cycle_pos = randint(0,len(self.rot_cycle)-1)
    self.rotation = randint(-30,30)

    # set the scale cycle if it hasn't been already
    if self.scale_cycle is None :
      steps = 5.
      self.scale_cycle = [i/steps for i in range(int(steps))] + [1.05, 1.1, 1.15, 1.1, 1.05, 1] 
    self.scale_pos = 0

    # need to store original image so quality stays the same and rect doesn't get huge
    self.orig_image = image

    # make a copy of the original image that the sprite uses to draw on
    self.image = image.convert()

    self.scale = uniform(0.1,0.75)
    self.image = pygame.transform.rotozoom(self.image,self.rotation,self.scale*self.scale_pos)
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.orig_center = (x,y)

  def update(self) :

    # adjust rotation
    self.rotation += self.rot_cycle[self.rot_cycle_pos]
    self.rot_cycle_pos = (self.rot_cycle_pos+1)%len(self.rot_cycle)

    # adjust scale
    if self.scale_pos != len(self.scale_cycle)-1 :
      self.scale_pos += 1
    else :
      self.scale_pos = len(self.scale_cycle)-1

    self.image = pygame.transform.rotozoom(self.orig_image,self.rotation,self.scale*self.scale_cycle[self.scale_pos])
    self.rect = self.image.get_rect()
    self.rect.center = self.orig_center

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=False)
  driver.input.calibrate()
  driver.register_module(EncouragerModule(driver))
  driver.run()
