from opencv import cv,highgui
from opencv import *
from aether.core import CameraInputProvider
import pygame.transform

class LazerPointerProvider(CameraInputProvider) :

	def __init__(self,cam_num,capture_dims) :
		#Call CameraInputProvider constructor
		CameraInputProvider.__init__(self,cam_num,capture_dims)
		print self.scale

		self.image_dims=tuple((int(dim) for dim in self.capture_dims))

		self.storage = cvCreateMemStorage(0);

		self.color_thresh = 230
		self.grid = (7,7)

		self.n_points = self.grid[0]*self.grid[1]

		self.object_points = cv.cvCreateMat(self.n_points,3,cv.CV_32F)
		self.image_points = cv.cvCreateMat(self.n_points,2,cv.CV_32F)

	def _calibrate_camera(self) :
		source = CameraInputProvider.get_frame(self)

		success, corners = cv.cvFindChessboardCorners(source, cv.cvSize(self.grid[0],self.grid[1]))
		n_points = self.grid[0]*self.grid[1]

		grid_x = self.capture_dims[0]/self.grid[0]
		grid_y = self.capture_dims[1]/self.grid[1]
		dest = []
		for i in range(0,self.grid[0]) :
			for j in range(0,self.grid[1]) :
				dest.append((j*grid_x,i*grid_y))

		self.dest = dest

		s = cv.cvCreateMat(n_points,2,cv.CV_32F)
		d = cv.cvCreateMat(n_points,2,cv.CV_32F)
		p = cv.cvCreateMat(3,3,cv.CV_32F)

		for i in range(n_points):
			s[i,0] = corners[i].x
			s[i,1] = corners[i].y

			d[i,0] = dest[i][0]
			d[i,1] = dest[i][1]

		results = cv.cvFindHomography(s,d,p)

		self.matrix = p

	def _get_cv_frame(self):
		frame = CameraInputProvider.get_frame(self)

		dst = cv.cvCreateImage(cv.cvSize(self.capture_dims[0],self.capture_dims[1]),frame.depth,frame.nChannels)
		cv.cvWarpPerspective( frame, dst, self.matrix)

		return dst

	def _cv_to_pygame(self,frame,channel=-1) :

		# scale the image to size of the window
		cvt_scale = cv.cvCreateImage(cv.cvSize(self.image_dims[0],self.image_dims[1]),frame.depth,frame.nChannels)
		#cv.cvResize(frame,cvt_scale,cv.CV_INTER_LINEAR)
		cv.cvResize(frame,cvt_scale,cv.CV_INTER_NN)

		# need to convert the colorspace differently depending on where the image came from
		cvt_color = cv.cvCreateImage(cv.cvSize(cvt_scale.width,cvt_scale.height),cvt_scale.depth,3)
		if frame.nChannels == 3 :
			# frame is in BGR format, convert it to RGB so the sky isn't orange
			cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_BGR2RGB)
		elif frame.nChannels == 1 : # image has only one channel, iow 1 color
			if channel == 0 :
				cv.cvMerge(frame,None,None,None,cvt_color)
			elif channel == 1 :
				cv.cvMerge(None,frame,None,None,cvt_color)
			elif channel == 2 :
				cv.cvMerge(None,None,frame,None,cvt_color)
			elif channel == 3 :
				cv.cvMerge(None,None,None,frame,cvt_color)
			else :
				cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_GRAY2RGB)

		# create a pygame surface
		frame_surface=pygame.image.frombuffer(cvt_color.imageData,self.image_dims,'RGB')

		return frame_surface

	def _get_shifted_frame(self,value,frame=None) :
		if frame is None :
			frame = self._get_cv_frame()
		shifted = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,frame.nChannels)
		cv.cvAddS(frame,value,shifted)
		return shifted

	def _get_scaled_frame(self,frame=None) :
		if frame is None :
			frame = self._get_cv_frame()
		scale = (480,320)
		scaled = cv.cvCreateImage(cv.cvSize(scale[0],scale[1]),frame.depth,frame.nChannels)
		#cv.cvResize(frame,scaled,cv.CV_INTER_LINEAR)
		cv.cvResize(frame,scaled,cv.CV_INTER_NN)
		return scaled

	def _get_grayscale_frame(self,frame=None) :
		if frame is None :
			frame = self._get_cv_frame()
		cvt_gray = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
		cv.cvCvtColor(frame,cvt_gray,cv.CV_BGR2GRAY)
		return cvt_gray

	def _get_hsv_frame(self,frame=None) :
		if frame is None :
			frame = self._get_cv_frame()
		cvt_hsv = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,3)
		cv.cvCvtColor(frame,cvt_hsv,cv.CV_BGR2HSV)
		return cvt_hsv

	def _get_frame_channel(self,frame=None,channel=0) :
		if frame is None :
			frame = self._get_cv_frame()

		# if frame only has one channel, just return it
		if frame.nChannels == 1 :
			return frame

		# extract the color channel
		cv_r = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
		if channel == 0 :
			cv.cvSplit(frame,cv_r,None,None,None)
		elif channel == 1 :
			cv.cvSplit(frame,None,cv_r,None,None)
		elif channel == 2 :
			cv.cvSplit(frame,None,None,cv_r,None)
		elif channel == 3 :
			cv.cvSplit(frame,None,None,None,cv_r)
		else :
			cv.cvCvtColor(frame,cv_r,cv.CV_BGR2GRAY)

		return cv_r

	def _get_color_frame(self,color="r",frame=None) :
		if frame is None :
			frame = self._get_cv_frame()

		# extract the color channel (image is in BGR format)
		cv_r = None #cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
		if color == "r" :
			cv_r = self._get_frame_channel(frame,channel=2)
		elif color == "g" :
			cv_r = self._get_frame_channel(frame,channel=1)
		elif color == "b" :
			cv_r = self._get_frame_channel(frame,channel=0)
		else :
			cv_r = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
			cv.cvCvtColor(frame,cv_r,cv.CV_BGR2GRAY)

		return cv_r

	def _get_threshold_frame(self,frame=None,thresh=None,max_thresh=255,type=cv.CV_THRESH_BINARY) :
		if frame is None :
			frame = self._get_grayscale_frame()
		if thresh is None :
			thresh = self.color_thresh
		# threshold the image for > self.color_thresh value
		cv_thresh = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
		cv.cvThreshold(frame,cv_thresh,thresh,max_thresh,type)

		return cv_thresh

	def _multiply_frames(self,frame1,frame2,scale=1.) :
		cv_mult = cv.cvCreateImage(cv.cvSize(frame1.width,frame1.height),frame1.depth,frame1.nChannels)
		cv.cvMul(frame1,frame2,cv_mult,scale)
		return cv_mult

	def _get_frame_in_range(self,color,tol=5,frame=None) :
		if frame is None :
			frame = self._get_cv_frame()

		cv_thresh = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)
		cv.cvInRangeS(self._get_color_frame('r'),color[0]-tol,color[0]+tol,cv_thresh)
		cv.cvInRangeS(self._get_color_frame('g'),color[1]-tol,color[1]+tol,cv_thresh)
		cv.cvInRangeS(self._get_color_frame('b'),color[2]-tol,color[2]+tol,cv_thresh)

		return cv_thresh

	def get_grayscale_frame(self) :
		return self._cv_to_pygame(frame)

	def get_color_frame(self,color="r") :
		return self._cv_to_pygame(self._get_color_frame(color=color),channel=color)

	def get_curr_frame(self) :
		curr_frame = self._get_cv_frame()
		curr_frame_surface = self._cv_to_pygame(curr_frame)
		return curr_frame_surface

