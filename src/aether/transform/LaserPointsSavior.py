'''
Transform that provides methods for getting the coordinates of laser points in an captured image.

read() result: The image it is passed without modification
get_points(): returns coordinates of the laser points

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class LaserPointsSavior(AetherTransform):

	input_names=('input',)
	defaults={'debug':False,'enabled':True}

	def read(self):

		frame = self.input.read()
		if self.debug :
			raw_frame = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,frame.nChannels)
			cv.cvCopy(frame,raw_frame,None)
			self.raw_frame_surface=pygame.image.frombuffer(frame.imageData,(frame.width,frame.height),'RGB')

		if self.enabled :

			cvt_red = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
			cv.cvSplit(frame,None,None,cvt_red,None)

			if self.debug :
				red_frame = cv.cvCreateImage(cv.cvSize(cvt_red.width,cvt_red.height),cvt_red.depth,3)
				cv.cvMerge(cvt_red,None,None,None,red_frame)
				self.red_frame_surface = pygame.image.frombuffer(red_frame.imageData,(cvt_red.width,cvt_red.height),'RGB')

			# I think these functions are too specialized for transforms
			cv.cvSmooth(cvt_red,cvt_red,cv.CV_GAUSSIAN,3, 0, 0, 0 )
			cv.cvErode(cvt_red, cvt_red, None, 1)
			cv.cvDilate(cvt_red, cvt_red, None, 1)

			if self.debug :
				thresh_frame = cv.cvCreateImage(cv.cvSize(cvt_red.width,cvt_red.height),cvt_red.depth,3)
				cv.cvMerge(cvt_red,None,None,None,thresh_frame)
				self.thresh_frame_surface = pygame.image.frombuffer(cvt_red.imageData,(cvt_red.width,cvt_red.height),'RGB')

			cvpt_min = cv.cvPoint(0,0)
			cvpt_max = cv.cvPoint(0,0)
			t = cv.cvMinMaxLoc(cvt_red,cvpt_min,cvpt_max)

			print t
			if cvpt_max.x == 0 and cvpt_max.y == 0 :
				return []
			return [(cvpt_max.x,cvpt_max.y)]

