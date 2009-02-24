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

		w = highgui.cvGetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_WIDTH)
		h = highgui.cvGetCaptureProperty(self.capture,highgui.CV_CAP_PROP_FRAME_HEIGHT)
		self.image_dims = (int(w),int(h))

	def _detect_faces(self) :
		"""Run OpenCV's Haar detection on the current frame, returning the rectangle with the largest area"""
		storage=cv.cvCreateMemStorage(0)

		# faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		faces = cv.cvHaarDetectObjects(self._get_cv_frame(),self.cascade,storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(40,40))
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
		curr_frame_surface=pygame.image.frombuffer(curr_frame.imageData,self.image_dims,'RGB')
		return curr_frame_surface

	def _get_cv_frame(self):
		"""Capture the current frame from OpenCV, returns cvMat object"""
		frame = highgui.cvQueryFrame(self.capture)
		if self.flip :
			cv.cvFlip(frame,None,1)
		return frame

	def get_com(self) :
		"""Returns the point closest to the center of the bounding face rectangle as a tuple, calculated as (x+(width/2),y+(height/2))"""
		face = self._detect_faces()
		if face is not None :
			return (int(face.x+(face.width/2.)),int(face.y+(face.height/2.)))
		return None

	def get_verts(self) :
		"""Returns a tuple of points as tuples containing the bounding face rectangle wound clockwise from top left point"""
		face = self._detect_faces()
		if face is not None :
			x1,x2,x3,x4 = (face.x,face.y),(face.x+face.width,face.y),(face.x+face.width,face.y+face.height),(face.x,face.y+face.width)
			return (x1,x2,x3,x4)
		return None

	def get_polys(self) :
		"""The same as get_verts since we're """
		return self.get_verts()
