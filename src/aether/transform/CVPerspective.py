'''
Transform that uses the OpenCV cvFindChessboardCorners and cvWarpPerspective function to autocalibrate camera
images.

read() result: New image converted using the conversion constant specified with the convert_method setting value.

:Author: Adam Labadorf
'''

from opencv import cv
from aether.core import AetherTransform

class CVPerspective(AetherTransform):

	input_names=('input',)
	defaults={'calibrated':False,'grid':(7,7)}

	def read(self):
		source = self.input.read()
		if not self.calibrated:

			success, corners = cv.cvFindChessboardCorners(source, cv.cvSize(self.grid[0],self.grid[1]))
			self.debug_print('CVPerspective: success, corners = (%d,%s(%d))'%(success,corners,len(corners)))

			if len(corners) == self.grid[0]*self.grid[1] :
				n_points = self.grid[0]*self.grid[1]

				grid_x = self.dims[0]/self.grid[0]
				grid_y = self.dims[1]/self.grid[1]
				self.dest = []
				for i in range(0,self.grid[0]) :
					for j in range(0,self.grid[1]) :
						self.dest.append((j*grid_x,i*grid_y))

				s = cv.cvCreateMat(n_points,2,cv.CV_32F)
				d = cv.cvCreateMat(n_points,2,cv.CV_32F)
				p = cv.cvCreateMat(3,3,cv.CV_32F)

				for i in range(n_points):
					s[i,0] = corners[i].x
					s[i,1] = corners[i].y

					d[i,0] = self.dest[i][0]
					d[i,1] = self.dest[i][1]

				results = cv.cvFindHomography(s,d,p)

				self.matrix = p
				self.settings.perspective.calibrated = True
				#self.debug_print('projection matrix:%s'%p)

		if self.calibrated :
			dst = cv.cvCreateImage(cv.cvSize(self.dims[0],self.dims[1]),source.depth,source.nChannels)
			cv.cvWarpPerspective( source, dst, self.matrix)
			return dst

		return source
