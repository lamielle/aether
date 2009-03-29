"""
This transform input using the location of faces that are detected using Haar Cascade Face Detection.

:Author Adam Labadorf and Alan LaMielle
"""

from opencv import cv,highgui
from aether.core import CameraTransform
import pygame.transform

class FaceTransform(CameraTransform):

	def __init__(self):
		#Call CameraTransform constructor
		CameraTransform.__init__(self)

		#Load the cascade classifier data
		self.cascade=cv.cvLoadHaarClassifierCascade(self.file_path('haarcascade_frontalface_alt.xml'),cv.cvSize(40,40))

		self.storage = cv.cvCreateMemStorage(0)
		cv.cvClearMemStorage(self.storage)

		#self._fd_dims = (240,180)
		self._fd_dims = (180,120)

	def __del__(self) :
		#Only attempt to access self.storage if it exists as a field of this class
		if 'storage' in self.__dict__:
			#Only release the field if memory has been allocated here
			if None!=self.storage:
				cv.cvReleaseMemStorage(self.storage)

	def _get_cv_frame(self):
		frame=CameraTransform.get_frame(self)
		if self.settings.FaceTransform.flip:
			cv.cvFlip(frame,None,1)
		return frame

	def _get_fd_frame(self) :
		frame = self._get_cv_frame()
		# convert image to grayscale and scale it down for speed
		cvt_gray = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),8,1)
		cv.cvCvtColor(frame,cvt_gray,cv.CV_BGR2GRAY)
		scaled_gray = cv.cvCreateImage(cv.cvSize(self._fd_dims[0],self._fd_dims[1]),8,1)
		cv.cvResize(cvt_gray,scaled_gray,cv.CV_INTER_LINEAR)
		return scaled_gray

	def _cv_to_pygame(self,frame) :

		# scale the image to size of the window
		cvt_scale = cv.cvCreateImage(cv.cvSize(self.capture_dims[0],self.capture_dims[1]),frame.depth,frame.nChannels)
		cv.cvResize(frame,cvt_scale,cv.CV_INTER_LINEAR)

		# need to convert the colorspace differently depending on where the image came from
		cvt_color = cv.cvCreateImage(cv.cvSize(cvt_scale.width,cvt_scale.height),cvt_scale.depth,3)
		if frame.nChannels == 3 : # image is BGR
			# frame is in BGR format, convert it to RGB so the sky isn't orange
			cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_BGR2RGB)
		elif frame.nChannels == 1 : # image is grayscale
			# frame is grayscale
			cv.cvCvtColor(cvt_scale,cvt_color,cv.CV_GRAY2RGB)

		# create a pygame surface
		frame_surface=pygame.image.frombuffer(cvt_color.imageData,self.capture_dims,'RGB')

		return frame_surface

	def get_fd_frame(self) :
		"""Returns the image passed to Haar Classifier.  The image used for face detection is scaled down for efficiency."""
		fd_frame = self._get_fd_frame()
		fd_surface = self._cv_to_pygame(fd_frame)
		return fd_surface

	def get_curr_frame(self) :
		"""Capture the current frame from OpenCV, returns pygame.Surface object"""
		curr_frame = self._get_cv_frame()
		curr_frame_surface = self._cv_to_pygame(curr_frame)
		return curr_frame_surface

	def _detect_faces(self,biggest=False) :
		"""Run OpenCV's Haar detection on the current frame, returning the rectangle with the largest area"""

		# get smaller grayscale image
		scaled_gray = self._get_fd_frame()

		# faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		cv_faces = cv.cvHaarDetectObjects(scaled_gray,self.cascade,self.storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(10,10))

		faces = []
		max_id = -1
		max_area = -1
		w,h = [float(x) for x in self._fd_dims]
		for i,face in enumerate(cv_faces) :
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
