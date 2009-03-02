"""
This is a class that encapsulates the details of OpenCV camera capture.  It should be treated as an abstract class and should only be used indirectly by a subclass.

:Author: Alan LaMielle
"""

from opencv import cv,highgui
from aether.core import InputProvider
from aether.error import AetherCameraError

class CameraInputProvider(InputProvider):

	def __init__(self,cam_num,capture_dims):
		"""Inititalize the camera associated with the given number.  Image captures will be of the given dimensions."""

		#Set the dimensions that we should be capturing in
		self.capture_dims=capture_dims
		self.cv_capture_dims=cv.cvSize(capture_dims[0],capture_dims[1])

		#Initialize the camera
		self._init_camera(cam_num)

	def _init_camera(self,cam_num):

		#Create the OpenCV camera capture object
		self._capture=highgui.cvCreateCameraCapture(cam_num)

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
		           int(highgui.cvGetCaptureProperty(self._capture,highgui.CV_CAP_PROP_FRAME_HEIGHT))
		          )

		#Set the scale flag depending on the results of setting the capture dimensions
		if self.capture_dims==read_dims:
			self.scale=False
		else: 
			self.scale=True

	def get_frame(self):
		"""Capture the current frame from OpenCV, returns a cvMat object"""

		#Capture the current frame
		frame=highgui.cvQueryFrame(self._capture)

		#Do we need to scale the captures?
		if self.scale:
			scaled_frame=cv.cvCreateImage(self.cv_capture_dims,frame.depth,frame.nChannels)
			cv.cvResize(frame,scaled_frame)
			frame=scaled_frame

		return frame
