from aether.core import InputProvider
from opencv import cv, highgui

import pygame.transform

class FaceInputProvider(InputProvider) :

	def __init__(self,cascade_file,flip=False) :
		self.flip = flip
		self.init_camera(0)
		self.cascade = cv.cvLoadHaarClassifierCascade(cascade_file,cv.cvSize(40,40))

	def init_camera(self,cam_num=0):
		self.capture=highgui.cvCreateCameraCapture(cam_num)

		if not self.capture:
			raise IOError('Unable to open camera %d'%cam_num)

		# highgui.cvCreateCameraCapture(id) takes ownership of the pointer so cvSetCaptureProperty won't work, disown it before setting
		self.capture.disown()

		w,h = 320,240
		
		highgui.cvSetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_WIDTH,w)
		highgui.cvSetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_HEIGHT,h)

		w = highgui.cvGetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_WIDTH)
		h = highgui.cvGetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_HEIGHT)

		self.capture.acquire()

		self.image_dims = (int(w),int(h))

	def _detect_faces(self) :
		"""Run OpenCV's Haar detection on the current frame, returning the rectangle with the largest area"""
		storage=cv.cvCreateMemStorage(0)
		cv.cvClearMemStorage(storage)

		# faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		frame = self._get_cv_frame()
		faces = cv.cvHaarDetectObjects(frame,self.cascade,storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(40,40))
		cv.cvReleaseMemStorage(storage)

		# find biggest face, probably the one we want
		fat_face = None
		for f in faces :
			if fat_face is None or f.height * f.width > fat_face.height * fat_face.width :
				fat_face = f
		return fat_face

	def get_curr_frame(self) :
		"""Capture the current frame from OpenCV, returns pygame.Surface object"""
		curr_frame = self._get_cv_frame()

		# curr_frame is in BGR format, convert it to RGB so the sky isn't orange
		cvt_color = cv.cvCreateImage(cv.cvSize(curr_frame.width,curr_frame.height),curr_frame.depth,curr_frame.nChannels)
		cv.cvCvtColor(curr_frame,cvt_color,cv.CV_BGR2RGB)

		# create a pygame surface
		curr_frame_surface=pygame.image.frombuffer(cvt_color.imageData,self.image_dims,'RGB')

		return curr_frame_surface

	def _get_cv_frame(self):
		"""Capture the current frame from OpenCV, returns cvMat object"""
		frame = highgui.cvQueryFrame(self.capture)
		if self.flip :
			cv.cvFlip(frame,None,1)
		return frame

	def get_com(self) :
		"""Returns the point closest to the center of the bounding face rectangle as a tuple, calculated as (x+(width/2),y+(height/2)), normalized to [0,1]"""
		face = self._detect_faces()
		if face is not None :
			lst = (int((face.x+(face.width/2.)),int(face.y+(face.height/2.))))

			# normalize
			w,h = [float(x) for x in self.image_dims]
			lst = tuple([(x[0]/w,x[1]/h) for x in lst])
			return lst
		return None

	def get_verts(self) :
		"""Returns a tuple of points as tuples containing the bounding face rectangle wound clockwise from top left point, normalized to [0,1]"""
		face = self._detect_faces()
		if face is not None :
			lst = (face.x,face.y),((face.x+face.width),face.y),((face.x+face.width),(face.y+face.height)),(face.x,(face.y+face.width))
			# normalize
			w,h = [float(x) for x in self.image_dims]
			lst = tuple([(x[0]/w,x[1]/h) for x in lst])
			return lst
		return None

	def get_polys(self) :
		"""The same as get_verts since we're only capturing the biggest face right now"""
		return self.get_verts()
