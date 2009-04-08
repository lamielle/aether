'''
Transform that returns polygons found by cvFindContours for shadow regions of a camera capture

read() result: a python list of lists of points representing polygons, sorted from biggest to smallest by area

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class CVContourPolys(AetherTransform):

	input_names=('input',)
	defaults={'min_area':0,'enabled':True}

	def init(self) :
		self.storage=cv.cvCreateMemStorage(0)

	def read(self) :
		frame=self.input.read()

		if self.enabled :

			cv_rs = [cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1) for i in range(3)]
			cv.cvSplit(frame,cv_rs[0],cv_rs[1],cv_rs[2],None)

			channel_contours = []

			for frame in cv_rs[0] :
				# I think these functions are too specialized for transforms
				#cv.cvSmooth(frame,frame,cv.CV_GAUSSIAN,3, 0, 0, 0 )
				#cv.cvErode(frame, frame, None, 1)
				#cv.cvDilate(frame, frame, None, 1)
				num_contours,contours=cv.cvFindContours(frame,self.storage,cv.sizeof_CvContour,cv.CV_RETR_LIST,cv.CV_CHAIN_APPROX_NONE,cv.cvPoint(0,0))
				if contours is None :
					channel_contours.append([])
				else :
					contours = cv.cvApproxPoly( contours, cv.sizeof_CvContour, self.storage, cv.CV_POLY_APPROX_DP, 3, 1 );
					if contours is None :
						channel_contours.append([])
					else :
						final_contours = []
						for c in contours.hrange() :
							area = abs(cv.cvContourArea(c))
							#self.debug_print('Polygon Area: %f'%area)
							if area >= self.min_area :
								lst = []
								for pt in c :
									lst.append((pt.x,pt.y))
								final_contours.append(lst)
							contours = contours.h_next
						channel_contours.append(final_contours)

		return channel_contours
