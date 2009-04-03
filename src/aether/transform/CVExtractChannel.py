'''
Transform that extracts the desired channels out of a CV image

read() result: New 3 channel image containing only the channel(s) from the read image specified
in the settings.channels list

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform

class CVExtractChannel(AetherTransform):

	input_names=('input',)
	defaults={'channel':0}

	def read(self):
		frame = self.input.read()

		# image we'll eventually return

		# which channels to combine

		# if frame only has one channel, just return it
		if frame.nChannels == 1 :
			return frame
		else :
			cv_rs = [None]*4
			cv_rs[self.channel] = cv.cvCreateImage(cv.cvSize(frame.width,frame.height),frame.depth,1)

			# extract the color channel
			cv.cvSplit(frame,cv_rs[0],cv_rs[1],cv_rs[2],cv_rs[3])

			return cv_rs[self.channel]
