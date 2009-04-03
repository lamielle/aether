'''
Transform that provides methods for getting the coordinates of laser points in an captured image.

read() result: The image it is passed without modification
get_points(): returns coordinates of the laser points

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class LaserPoints(AetherTransform):

	input_names=('extract_red','camera',)
	defaults={}

	def read(self):
		return self.camera.read()
		frame = self.extract_red.read()
		cv_rs = [None]*4
		cv_rs[0] = frame
		cvt_im = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,3)
		cv.cvMerge(cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3],cvt_im)
		frame_surface=pygame.image.frombuffer(cvt_im.imageData,(frame.width,frame.height),'RGB')
		return frame_surface

	def get_points(self):
		frame = self.extract_red.read()

		cvpt_min = cv.cvPoint(0,0)
		cvpt_max = cv.cvPoint(0,0)
		t = cv.cvMinMaxLoc(frame,cvpt_min,cvpt_max)

		return t
