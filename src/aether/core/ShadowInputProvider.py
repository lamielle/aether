#!/usr/bin/env python

import pygame, os, sys
from pygame.locals import *
from pygame.color import *
from pygame.image import tostring
from pygame import PixelArray
import pygame.mouse
import Image

from opencv import cv,highgui

class PYGameCV:
	def __init__(self,debug=False):
		pygame.init()
		self.dims=(640,480)
		self.image_dims=(320,240)
		self.screen=pygame.display.set_mode(self.dims)
		self.debug=debug
		self.capture=None
		self.init_camera(0)

	def init_camera(self,cam_num=0):
		self.capture=highgui.cvCreateCameraCapture(cam_num)

		if not self.capture:
			raise IOError('Unable to open camera %d'%cam_num)

		highgui.cvSetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_WIDTH,self.image_dims[0])
		highgui.cvSetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_HEIGHT,self.image_dims[1])

	def get_curr_frame(self):
		#Capture the current frame from OpenCV
		return highgui.cvQueryFrame(self.capture)

	def draw(self):
		#Get current frame from camera
		curr_frame=self.get_curr_frame()

		surface=self.blit_capture(curr_frame)

	def draw_contours(self,curr_frame,surface):
		#Apply a perspective transform to the frame
		#TODO: write this method
		#curr_frame=self.get_transformed(transform_points)

		#Convert the image to grayscale
		curr_frame=self.convert_to_gray(curr_frame)

		#Threshold the image
		curr_frame=self.get_thresholded(curr_frame,100)

		#Apply some filters to cleanup the image
		curr_frame=self.get_smoothed(curr_frame)

		#Get the contours of the processed image
		contours=self.get_contours(curr_frame,100)

		for contour in contours:
#			pygame.draw.polygon(surface,THECOLORS["gray"],contour)

			for point in contour:
				pygame.draw.circle(surface,THECOLORS["red"],point,1)

	def blit_capture(self,curr_frame):
		#Convert the frame to a Surface
		curr_frame_surface=pygame.image.frombuffer(curr_frame.imageData,self.image_dims,'RGB')

		self.draw_contours(curr_frame,curr_frame_surface)

		#Scale the frame's surface and blit it to the screen
		pygame.transform.scale(curr_frame_surface.convert(),self.dims,self.screen)

	#cv.cvCreateImage(size of image (use cv.cvGetSize(some_image), depth of image, channels of image)

	#use cv.cvReleaseImage to free images created with cvCreateImage

	#cv.cvCvtColor: converts from one colorspace to another
	#cv.cvCvtColor(source,dest, conversion code)
	#conversion code can be:

	def convert_to_color(self,image):
		converted=cv.cvCreateImage(cv.cvGetSize(image),image.depth,3)
		cv.cvCvtColor(image,converted,cv.CV_GRAY2RGB)
		cv.cvReleaseImage(image)
		return converted

	def convert_to_gray(self,image):
		converted=cv.cvCreateImage(cv.cvGetSize(image),image.depth,1)
		cv.cvCvtColor(image,converted,cv.CV_RGB2GRAY)
		cv.cvReleaseImage(image)
		return converted

	def get_smoothed(self,image):
		cv.cvSmooth(image,image,cv.CV_GAUSSIAN,3,0,0,0)
		cv.cvErode(image,image,None,1)
		cv.cvDilate(image,image,None,1)
		return image

	def get_thresholded(self,gray_source,threshold):
		#Allocate a new image
		threshed=cv.cvCreateImage(cv.cvGetSize(gray_source),gray_source.depth,1)

		#Subtract 255 from all values in the image?
		cv.cvSubRS(gray_source,cv.cvRealScalar(255),threshed,None)

		#Apply a binary threshold to the image
		cv.cvThreshold(gray_source,threshed,threshold,255,cv.CV_THRESH_BINARY)

		#Release the source image
		cv.cvReleaseImage(gray_source)

		return threshed

	def clone_image(self,image):
		return cv.cvCloneImage(image)

	def get_contours(self,image,threshold):
		storage=cv.cvCreateMemStorage(0)

		image=self.clone_image(image)

		num_contours,contours=cv.cvFindContours(image,storage,cv.sizeof_CvContour,cv.CV_RETR_LIST,cv.CV_CHAIN_APPROX_NONE,cv.cvPoint(0,0))

		contour_points=[[]]*num_contours
		for contour_index,contour in enumerate(contours.hrange()):
			for point in contour:
				contour_points[contour_index].append((point.x,point.y))

		cv.cvReleaseImage(image)
		cv.cvReleaseMemStorage(storage)

		return contour_points

	def run(self):
		clock=pygame.time.Clock()
		running=True

		# do the main loop
		while running:
			for event in pygame.event.get():
				if event.type==QUIT:
					running=False
				elif event.type==KEYDOWN and event.key==K_ESCAPE:
					running=False
				elif event.type==KEYDOWN and event.key==K_q:
					running=False
				elif event.type==KEYDOWN and event.key==K_f:
					pygame.display.toggle_fullscreen()
				elif event.type==KEYDOWN and event.key==K_c:
					# yes, this actually toggles mouse visibility
					pygame.mouse.set_visible(not pygame.mouse.set_visible(True))

			self.draw()

			pygame.display.flip()
			clock.tick(50)

if __name__ == '__main__':
	driver=PYGameCV()
	driver.run()
