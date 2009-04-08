'''
Transform that provides methods for getting the coordinates of laser points in an captured image.

read() result: The image it is passed without modification
get_points(): returns coordinates of the laser points

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class DebugLaserPoints(AetherTransform):

	input_names=('thresh2pg','red2pg','camera','thresh',)
	defaults={}

	def read(self):
		src = self.camera.read()
		thresh = self.thresh2pg.read()
		red = self.red2pg.read()
		raw_thresh = self.thresh.read()

		cvt_red = cv.cvCreateImage(cv.cvSize(raw_thresh.width,raw_thresh.height),raw_thresh.depth,1)
		cv.cvSplit(raw_thresh,cvt_red,None,None,None)
		cvpt_min = cv.cvPoint(0,0)
		cvpt_max = cv.cvPoint(0,0)
		t = cv.cvMinMaxLoc(cvt_red,cvpt_min,cvpt_max)

		return src,thresh,red,(cvpt_max.x,cvpt_max.y)

