#!/usr/bin/env python

import pygame, pygame.key, pygame.sprite, pygame.image, pygame.transform, pygame.mouse, pygame.font
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

#from math import abs
from random import randint, randrange, random

from EncouragerModule import EncouragementSprite

class CatchOSIfUCan(ILDParamModule) :

  def __init__(self, driver, num_peepers=10, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)

    # set up the images
    #image_fns = ['images/freebsd-logo.png','images/fedora-logo.png','images/ubuntu-logo.png','images/windows-logo.png','images/gentoo-logo.png','images/e-logo.png','images/debian-logo.png','images/opensuse-logo.png']
    self.names = ['freebsd','fedora','ubuntu','gentoo','e','debian','opensuse','windows']
    image_fns = ['images/%s-logo.png'%n for n in self.names]

    sm = 50
    lg = 100
    images = [pygame.image.load(s) for s in image_fns]
    scales = [sm]*7 + [lg]

    self.image_col = zip(self.names,images,scales)

    # create the sprite group
    self.sprites = pygame.sprite.Group()

    # game stuff
    self.maxminscore = 1000
    self.score = 0
    self.update_drop_freq()
    self.update_drop_speed()
    self.add_score = 10

    self.font = pygame.font.Font(None, 36)
    self.text = self.font.render("Score: %d"%self.score, 1, (10, 10, 10))
    self.textpos = self.text.get_rect(centerx=self.dims[0]-100)

    self.you_won = False
    
    self.draw_shadow = False

  def update_drop_freq(self) :
    self.drop_freq = abs(self.score/10000.) + 0.03
   
  def update_drop_speed(self) :
    self.drop_speed = abs(self.score/100.) + 3

  def draw(self,screen) :
    screen.fill((200,200,255,255))

    # check to add sprite
    if random() < self.drop_freq :
      i = self.image_col[randrange(0,len(self.image_col))]
      self.sprites.add(LogoSprite(i[0],i[1],i[2],randrange(i[2]/2.,self.dims[0]-i[2]/2),-i[2],self.drop_speed))

    if not self.you_won :
      # draw the shadow
      shadow_pts = self.input.verts()
      shadow_rect = None
      if len(shadow_pts) > 2 : shadow_rect = pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
      if shadow_rect is not None : pygame.draw.rect(screen,THECOLORS["red"],shadow_rect,1)
      for pt in shadow_pts :
        pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)

      shadow_polys = self.input.polys()

      for s in self.sprites :
        if s.is_dead :
          self.sprites.remove(s)
        if s.rect.y > self.dims[1]+50 :
          self.sprites.remove(s)
          if s.name in self.names[0:7] :
            self.score += [10,-10][self.score > 0]
        for shadow_pts in shadow_polys :
          if self.draw_shadow :
            pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
          for p in shadow_pts :
            if s.rect.collidepoint(p) and not s.is_dying :
              if s.name in self.names[0:7] : # good boy
                self.score = min(self.maxminscore,self.score+self.add_score)
              else : # that's a bad monkey
                self.score = max(-self.maxminscore,self.score-self.add_score)
              s.start_dying()

      self.update_drop_freq()
      self.update_drop_speed()

      #print self.score, self.drop_freq, self.drop_speed
      if self.score >= self.maxminscore :
        self.you_won = True
        self.drop_freq = 0.5
        self.drop_speed = 15

    else :

      self.winner = self.font.render("ALL YOUR OS ARE BELONG TO US",1,(randint(0,255),randint(0,255),randint(0,255)))
      textrect = self.winner.get_rect()
      screen.blit(self.winner,(self.dims[0]/2-textrect.width/2,self.dims[1]/2))

      for s in self.sprites :
        if s.is_dead :
          self.sprites.remove(s)
        if s.rect.y > self.dims[1]+50 :
          self.sprites.remove(s)
 
          
    self.sprites.draw(screen)
    self.sprites.update()

    self.text = self.font.render("Score: %d"%self.score, 1, (10, 10, 10))
    screen.blit(self.text,self.textpos)

  def process_event(self,event) :
    if event.type == KEYDOWN and event.key == K_r :
      self.draw_shadow = not self.draw_shadow
      return True
    return False

class LogoSprite(pygame.sprite.Sprite) :
  die_seq = None

  def __init__(self,name,image,size,x,y,dy) :
    pygame.sprite.Sprite.__init__(self)

    if self.die_seq is None :
      names = ['images/poof%d.png'%s for s in [1,2,3,4]]
      self.die_seq = [pygame.image.load(s) for s in names]

    self.name = name
    self.image = pygame.transform.scale(image,(size,size))
    self.size = size
    self.rect = self.image.get_rect()
    self.rect.center = (x,y)
    self.is_dying = False
    self.is_dead = False
    self.die_index = 0
    self.dy = dy

  def update(self) :
    if self.is_dying :
      if self.die_index != len(self.die_seq) :
        pygame.transform.scale(self.die_seq[self.die_index],(self.size,self.size),self.image)
        self.die_index += 1
      else :
        self.is_dead = True
    else :
      self.rect.center = self.rect.center[0],self.rect.center[1]+self.dy

  def start_dying(self) :
    self.is_dying = True

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=False)
  #driver.input.calibrate()
  driver.register_module(CatchOSIfUCan(driver))
  driver.run()
