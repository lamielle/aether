'''
Input provider that reads frames from an OpenCV IP and flips the capture.

read() result: a flipped cvMat

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherInputProvider

class FlipInputProvider(AetherInputProvider):

	#Default dependences
	deps=(('CVCameraInputProvider','camera'),)

	def read(self):
		'''Capture the current frame from the camera and flip it'''

		#Read the current frame from the camera wrapper
		frame=self.camera.read()
		cv.cvFlip(frame,None,1)
		return frame
