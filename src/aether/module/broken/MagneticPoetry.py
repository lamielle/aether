#!/usr/bin/env python

import pygame, pygame.key, pygame.sprite, pygame.font, pygame.time
from pygame.color import THECOLORS
from pygame.locals import *
from ildp.core import ILDParamModule
import ildp.core.input

from ConfigParser import SafeConfigParser

import math
from random import randint, sample

class MagneticPoetry(ILDParamModule) :

  def __init__(self, driver, num_peepers=10, **kwargs) :
    ILDParamModule.__init__(self,driver,**kwargs)

    config = SafeConfigParser()
    config.read('MagneticPoetryWords.txt')

    self.nouns = eval(config.get('Words','nouns'))
    self.adjectives = eval(config.get('Words','adjectives'))
    self.verbs = eval(config.get('Words','verbs'))
    self.adverbs = eval(config.get('Words','adverbs'))
    self.prepositions = eval(config.get('Words','prepositions'))
    self.pronouns = eval(config.get('Words','pronouns'))

    self.words = pygame.sprite.Group()
    self.get_new_words()

    self.font = pygame.font.Font(None,48)
    self.regen = self.font.render("New Words",2,(255,255,255),(255,50,50))
    self.regenrect = self.regen.get_rect()
    self.regenrect.center = (self.regenrect.width/2.+5,self.dims[1]-self.regenrect.height-5)

    self.fridge = pygame.image.load("images/fridge.png")

    self.clock = pygame.time.Clock()
    self.last_refresh = 0

  def get_new_words(self) :
    lst = sample(self.verbs,3)
    lst.extend(sample(self.adverbs,3))
    lst.extend(sample(self.nouns,4))
    lst.extend(sample(self.adjectives,4))
    lst.extend(sample(self.prepositions,3))
    lst.extend(sample(self.pronouns,4))

    self.words.empty()
    for w in lst :
      self.words.add(MagneticWord(w,randint(0,self.dims[0]),randint(0,self.dims[1])))


  def draw(self,screen) :

    self.clock.tick()

    #screen.fill((250,250,250,255))
    screen.blit(self.fridge,(0,0))
    screen.blit(self.regen,self.regenrect)

    # draw the shadow
    shadow_pts = self.input.verts()
    if len(shadow_pts) > 2 : pygame.draw.polygon(screen,THECOLORS["gray"],shadow_pts)
    for pt in shadow_pts :
      pygame.draw.circle(screen,THECOLORS["red"],tuple((int(i) for i in pt)),3)

    for w in self.words :
      any_collided = False
      collide_pos = None
      for p in shadow_pts :
        if w.rect.collidepoint(p) :
          any_collided = True
          collide_pos = p

      w.waitforit(any_collided, collide_pos)

    for p in shadow_pts :
      self.last_refresh += self.clock.get_time()
      if self.regenrect.collidepoint(p) and self.last_refresh  > 30000 :
        self.get_new_words()
        self.last_refresh = 0

    self.words.draw(screen)
    self.words.update()


  def process_event(self,event) :
    if event.type == KEYDOWN and event.key == K_r :
      pass
      return True
    return False


class MagneticWord(pygame.sprite.Sprite) :

  font = None
  max_wait = 25

  def __init__(self,word,x,y) :
    pygame.sprite.Sprite.__init__(self)
    if self.font is None :
      self.font = pygame.font.Font(None, 24)

    self.word = word
    self.text = self.font.render(word,1,(10,10,10))
    self.border = (6,4)
    self.image = pygame.Surface((self.text.get_rect().width+self.border[0],self.text.get_rect().height+self.border[1]),0,32)
    self.image.fill((255,255,255))
    self.rect = self.image.get_rect()
    self.image.blit(self.text,(0,0))
    self.textpos = (self.border[0]/2.,self.border[1]/2.)
    self.rect.center = (x,y)

    self.waitingforit = False
    self.waitingforitcounter = 0

    self.incolor = (255,10,10)
    self.outcolor = (10,10,10)

  def update(self) :
    color = None
    if self.waitingforit :
      color = self.incolor
    else :
      color = self.outcolor

    self.text = self.font.render(self.word,2,color)
    self.image.fill((255,255,255))
    #self.rect = self.image.get_rect()
    #self.rect.center = self.textpos
    #pygame.draw.rect(self.image,(20,20,20),self.text.get_rect(),2)
    #pygame.draw.aaline(self.image,(20,20,20),(-1,self.rect.height-2),(self.rect.width-2,self.rect.height-2),2)
    #pygame.draw.aaline(self.image,(20,20,20),(0,self.rect.width-1),(self.rect.width-2,self.rect.height-1),2)
    pygame.draw.line(self.image,(120,120,120),(0,0),(self.rect.width-1,0),1)
    pygame.draw.line(self.image,(120,120,120),(0,0),(0,self.rect.height-1),1)
    pygame.draw.line(self.image,(50,50,50),(-1,self.rect.height-2),(self.rect.width-1,self.rect.height-2),2)
    pygame.draw.line(self.image,(50,50,50),(self.rect.width-2,0),(self.rect.width-2,self.rect.height-2),2)
    self.image.blit(self.text,self.textpos)
    pass

  def move(self,pos) :
    self.rect.center = pos

  def waitforit(self,collided,pos) :
    if collided :
      if self.waitingforitcounter == self.max_wait :
        self.waitingforit = True
        self.move(pos)
      else :
        self.waitingforitcounter += 1
    else :
      self.waitingforit = False
      self.waitingforitcounter = 0

if __name__ == '__main__' :
  from ildp.core import ILDDriver
  driver = ILDDriver(640,debug=False)
  #driver.input.calibrate()
  driver.register_module(MagneticPoetry(driver))
  driver.run()
