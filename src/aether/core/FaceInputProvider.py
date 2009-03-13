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

		self._fd_dims = (180,120)

		self.image_dims=tuple((int(dim) for dim in self.capture_dims))
		self.storage = cv.cvCreateMemStorage(0)
		cv.cvClearMemStorage(self.storage)

	def __del__(self) :
		cv.cvReleaseMemStorage(self.storage)

	def _get_cv_frame(self):
		frame=CameraInputProvider.get_frame(self)
		if self.flip :
			cv.cvFlip(frame,None,1)
		return frame

	def _get_fd_frame(self,frame) :
		# convert image to grayscale and scale it down to 240,180 for speed
		cvt_gray = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),8,1)
		cv.cvCvtColor(frame,cvt_gray,cv.CV_BGR2GRAY)
		scaled_gray = cv.cvCreateImage(cv.cvSize(self._fd_dims[0],self._fd_dims[1]),8,1)
#		cv.cvResize(cvt_gray,scaled_gray,cv.CV_INTER_LINEAR)
		return scaled_gray

	def _cv_to_pygame(self,frame) :
		# curr_frame is in BGR format, convert it to RGB so the sky isn't orange
		cvt_color = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,frame.nChannels)
		cv.cvCvtColor(frame,cvt_color,cv.CV_BGR2RGB)

		# create a pygame surface
		frame_surface=pygame.image.frombuffer(cvt_color.imageData,self.image_dims,'RGB')

		return frame_surface

	def get_fd_frame(self) :
		"""Returns the image passed to Haar Classifier.  The image used for face detection is scaled down for efficiency."""
		frame = self._get_cv_frame()
		fd_frame = self._get_fd_frame(frame)
		fd_surface = self._cv_to_pygame(frame)
		return fd_surface

	def get_curr_frame(self) :
		"""Capture the current frame from OpenCV, returns pygame.Surface object"""
		curr_frame = self._get_cv_frame()
		curr_frame_surface = self._cv_to_pygame(curr_frame)
		return curr_frame_surface

	def _detect_faces(self,biggest=False) :
		"""Run OpenCV's Haar detection on the current frame, returning the rectangle with the largest area"""
		return []
		#cv.cvClearMemStorage(self.storage)

		# faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		frame = self._get_cv_frame()

		sc_w,sc_h = 180,120
		scaled_gray = self._get_fd_frame(frame)
		faces = cv.cvHaarDetectObjects(scaled_gray,self.cascade,self.storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(60,60))

		faces = []
		max_id = -1
		max_area = -1
		w,h = [float(x) for x in (sc_w,sc_h)]
		for i,face in enumerate(faces) :
			f = (face.x,face.y),((face.x+face.width),face.y),((face.x+face.width),(face.y+face.height)),(face.x,(face.y+face.width))

			# keep track of the face with the largest area in case user wants it
			if face.width*face.height > max_area :
				max_area = face.width*face.height
				max_id = i

			# normalize
			faces.append(tuple([(x[0]/w,x[1]/h) for x in f]))

		if len(faces) > 0 :
			if biggest :
				return faces[max_id]
			else :
				return faces
		return []

	def get_com(self) :
		"""Returns the point closest to the center of the bounding face rectangle as a tuple, calculated as (x+(width/2),y+(height/2)), normalized to [0,1]"""
		faces = self._detect_faces(biggest=True)
		if len(faces) > 0 :
			face = faces[0]
			w,h = face[1][0] - f[0][0],f[2][1] - f[0][1]
			lst = int(face[0][0]+(w/2.)),int(face[0][1]+(h/2.))

			# normalize
			return lst
		return None

	def get_verts(self) :
		"""Returns a tuple of points as tuples containing the bounding face rectangle wound clockwise from top left point, normalized to [0,1]"""
		faces = self._detect_faces(biggest=True)
		if len(faces) == 1 :
			return faces[0]
		return None

	def get_polys(self) :
		"""The same as get_verts since we're only capturing the biggest face right now"""
		faces = self._detect_faces()

		# sort the faces so they are in order by descending area
		#def area(f) :
		#	return f[1][0]-f[0][0]*f[2][1]-f[0][1]
		
		#faces.sort(lambda x,y: cmp(area(y),area(x)))

		return faces
