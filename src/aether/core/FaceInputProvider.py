"""
This class provides input using the location of faces that are detected using Haar Cascade Face Detection.

:Author Adam Labadorf and Alan LaMielle
"""

from opencv import cv,highgui
from aether.core import CameraInputProvider

import pygame.transform

class FaceInputProvider(CameraInputProvider):

	def __init__(self,cam_num,capture_dims,cascade_file,flip=False):
		#Call CameraInputProvider constructor
		CameraInputProvider.__init__(self,cam_num,capture_dims)

		#Load the cascade classifier data
		self.cascade=cv.cvLoadHaarClassifierCascade(cascade_file,cv.cvSize(40,40))

		self.flip=flip

		self.image_dims=tuple((int(dim) for dim in self.capture_dims))

	def get_frame(self):
		frame=CameraInputProvider.get_frame(self)
		if self.flip :
			cv.cvFlip(frame,None,1)
		return frame

	def _detect_faces(self,biggest=False) :
		"""Run OpenCV's Haar detection on the current frame, returning the rectangle with the largest area"""
		storage=cv.cvCreateMemStorage(0)
		cv.cvClearMemStorage(storage)

		# faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		frame = self.get_frame()
		cvt_gray = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),8,1)
		cv.cvCvtColor(frame,cvt_gray,cv.CV_BGR2GRAY)
		#faces = cv.cvHaarDetectObjects(frame,self.cascade,storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(20,20))
		faces = cv.cvHaarDetectObjects(cvt_gray,self.cascade,storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(20,20))
		cv.cvReleaseMemStorage(storage)

		if biggest :
			# find biggest face, probably the one we want
			fat_face = None
			for f in faces :
				if fat_face is None or f.height * f.width > fat_face.height * fat_face.width :
					fat_face = f
			return fat_face
		else :
			return faces

	def get_curr_frame(self) :
		"""Capture the current frame from OpenCV, returns pygame.Surface object"""
		curr_frame = self.get_frame()

		# curr_frame is in BGR format, convert it to RGB so the sky isn't orange
		cvt_color = cv.cvCreateImage(cv.cvSize(curr_frame.width,curr_frame.height),curr_frame.depth,curr_frame.nChannels)
		cv.cvCvtColor(curr_frame,cvt_color,cv.CV_BGR2RGB)

		# create a pygame surface
		curr_frame_surface=pygame.image.frombuffer(cvt_color.imageData,self.image_dims,'RGB')

		return curr_frame_surface

	def get_com(self) :
		"""Returns the point closest to the center of the bounding face rectangle as a tuple, calculated as (x+(width/2),y+(height/2)), normalized to [0,1]"""
		face = self._detect_faces(biggest=True)
		if face is not None :
			lst = int(face.x+(face.width/2.)),int(face.y+(face.height/2.))

			# normalize
			w,h = [float(x) for x in self.image_dims]
			lst = (lst[0]/w,lst[1]/h)
			return lst
		return None

	def get_verts(self) :
		"""Returns a tuple of points as tuples containing the bounding face rectangle wound clockwise from top left point, normalized to [0,1]"""
		face = self._detect_faces(biggest=True)
		if face is not None :
			lst = (face.x,face.y),((face.x+face.width),face.y),((face.x+face.width),(face.y+face.height)),(face.x,(face.y+face.width))
			# normalize
			w,h = [float(x) for x in self.image_dims]
			lst = tuple([(x[0]/w,x[1]/h) for x in lst])
			return lst
		return None

	def get_polys(self) :
		"""The same as get_verts since we're only capturing the biggest face right now"""
		cv_faces = self._detect_faces()
		faces = []
		for face in cv_faces :
			f = (face.x,face.y),((face.x+face.width),face.y),((face.x+face.width),(face.y+face.height)),(face.x,(face.y+face.width))
			# normalize
			w,h = [float(x) for x in self.image_dims]
			faces.append(tuple([(x[0]/w,x[1]/h) for x in f]))

		# sort the faces so they are in order by descending area
		def area(f) :
			return f[1][0]-f[0][0]*f[2][1]-f[0][1]
		faces.sort(lambda x,y: cmp(area(y),area(x)))
		return faces
