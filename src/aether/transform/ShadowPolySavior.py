'''
Transform that returns polygons found by cvFindContours for shadow regions of a camera capture

read() result: a python list of lists of points representing polygons, sorted from biggest to smallest by area

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform
import pygame

class ShadowPolySavior(AetherTransform):

	input_names=('input',)
	defaults={'threshold':174,'min_area':0,'enabled':True,'debug':False}

	def init(self) :
		self.storage=cv.cvCreateMemStorage(0)

	def read(self) :
		frame=self.input.read()
		if self.debug :
			raw_frame = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,frame.nChannels)
			cv.cvCopy(frame,raw_frame,None)
			self.raw_frame_surface=pygame.image.frombuffer(frame.imageData,(frame.width,frame.height),'RGB')

		if self.enabled :
			cv_rs = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)

			# convert color
			cv.cvCvtColor(frame,cv_rs,cv.CV_BGR2GRAY)

			# invert the image
			cv.cvSubRS(cv_rs, 255, cv_rs, None);

			# threshold the image
			frame = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
			cv.cvThreshold(cv_rs, frame, self.threshold, 255, cv.CV_THRESH_BINARY)

			if self.debug :
				thresh_frame = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,3)
				cv.cvCvtColor(frame,thresh_frame,cv.CV_GRAY2RGB)
				self.thresh_frame_surface=pygame.image.frombuffer(thresh_frame.imageData,(frame.width,frame.height),'RGB')

			# I think these functions are too specialized for transforms
			cv.cvSmooth(frame,frame,cv.CV_GAUSSIAN,3, 0, 0, 0 )
			cv.cvErode(frame, frame, None, 1)
			cv.cvDilate(frame, frame, None, 1)

			num_contours,contours=cv.cvFindContours(frame,self.storage,cv.sizeof_CvContour,cv.CV_RETR_LIST,cv.CV_CHAIN_APPROX_NONE,cv.cvPoint(0,0))
			if contours is None :
				return []
			else :
				contours = cv.cvApproxPoly( contours, cv.sizeof_CvContour, self.storage, cv.CV_POLY_APPROX_DP, 3, 1 );
				if contours is None :
					return []
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
					return final_contours

		return []
