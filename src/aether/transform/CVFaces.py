'''
Transform that finds faces in an input OpenCV cvMat image.

read() result: list of the bounding boxes of the detected faces.

:Author Adam Labadorf and Alan LaMielle
'''

from opencv import cv,highgui
from aether.core import AetherTransform
import pygame.transform

class CVFaces(AetherTransform):

	input_names=('input',)
	defaults={'fd_dims':(180,120),'cascade_file':'haarcascade_frontalface_alt.xml'}

	def init(self):
		#Load the cascade classifier data
		self.cascade=cv.cvLoadHaarClassifierCascade(self.file_path(self.cascade_file),cv.cvSize(40,40))

		#Allocate/init storage
		self.storage=cv.cvCreateMemStorage(0)
		cv.cvClearMemStorage(self.storage)

	def __del__(self):
		#Only attempt to access self.storage if it exists as a field of this class
		if hasattr(self,'storage'):
			#Only release the field if memory has been allocated here
			if None!=self.storage:
				cv.cvReleaseMemStorage(self.storage)

	def read(self):
		'''Run OpenCV's Haar detection on the current frame, returning a list of the bounding boxes of the faces'''

		#Read the frame to run face detection on
		frame=self.input.read()

		#Detect the faces
		#cv_faces is cv.CvSeq of cv.CvRect objects that have x,y,width,height members
		cv_faces=cv.cvHaarDetectObjects(frame,self.cascade,self.storage,1.1,2,cv.CV_HAAR_DO_CANNY_PRUNING,cv.cvSize(10,10))

		return [((face.x,face.y),((face.x+face.width),face.y),((face.x+face.width),(face.y+face.height)),(face.x,(face.y+face.width))) for face in cv_faces]
