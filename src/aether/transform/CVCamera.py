'''
Transform that reads frames from a camera device using OpenCV.  This is a transform that encapsulates the details of OpenCV camera capture.

read() result: cvMat

:Author: Alan LaMielle
'''

from opencv import cv,highgui
from aether.core import AetherTransform
from aether.error import AetherCameraError

class CVCamera(AetherTransform):

	#Default values for settings this transform needs
	defaults={'capture_dims':(640,480),'cam_num':0}

	#Dictionary of capture objects
	_captures={}

	def init(self):
		'''Inititalize the camera associated with the camera number specified in the settings (cam_num).  Image captures will be of the dimensions specified in settings (capture_dims).'''

		#Set the dimensions that we should be capturing in
		self.cv_capture_dims=cv.cvSize(self.capture_dims[0],self.capture_dims[1])

		#Initialize the camera
		self._init_camera(self.cam_num)

	def _init_camera(self,cam_num):
		'''Initializes the camera associated with the given camera number'''

		#Create the OpenCV camera capture object if one has not been created already
		if cam_num not in self._captures:
			self._captures[cam_num]=highgui.cvCreateCameraCapture(cam_num)
		self._capture=self._captures[cam_num]

		#Make sure the camera object was created
		if not self._capture:
			raise AetherCameraError('Unable to open camera %d'%cam_num)

		#cvCreateCameraCapture(id) takes ownership of the camera pointer
		#cvSetCaptureProperty won't work unless we disown it before setting
		self._capture.disown()

		#Set the capture dimensions
		highgui.cvSetCaptureProperty(self._capture,highgui.CV_CAP_PROP_FRAME_WIDTH,self.capture_dims[0])
		highgui.cvSetCaptureProperty(self._capture,highgui.CV_CAP_PROP_FRAME_HEIGHT,self.capture_dims[1])

		#Take ownership again
		self._capture.acquire()

		#Read the capture dims and see if they were set to what we specified
		read_dims=(
		           int(highgui.cvGetCaptureProperty(self._capture,highgui.CV_CAP_PROP_FRAME_WIDTH)),
		           int(highgui.cvGetCaptureProperty(self._capture,highgui.CV_CAP_PROP_FRAME_HEIGHT)))

		#Set the scale flag depending on the results of setting the capture dimensions
		#If we are reading frames in the correct dimensions, we don't need to scale
		if self.capture_dims==read_dims:
			self.scale=False
		else:
			print "Tried setting capture resolution:",self.capture_dims,", got:",read_dims
			self.scale=True

	def read(self):
		'''Capture the current frame from OpenCV, returns a cvMat object'''

		#Capture the current frame
		frame=highgui.cvQueryFrame(self._capture)

		#Do we need to scale the captures?
		if self.scale:
			scaled_frame=cv.cvCreateImage(self.cv_capture_dims,frame.depth,frame.nChannels)
			cv.cvResize(frame,scaled_frame,cv.CV_INTER_NN)
			frame=scaled_frame

		return frame
