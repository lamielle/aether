'''
Transform that reads a collection of point collections.
Example input: [[(0,0),(10,5)],[(1,5),(5,10)]]
The points are given to be in a region with dimensions 'in_dims' and are scaled to dimensions 'out_dims'.

read() result: A collection of scaled point collections.

:Author: Alan LaMielle
'''

from opencv import cv
from aether.core import AetherTransform

class ScalePoints(AetherTransform):

	#Default values for settings this transform needs
	defaults={'in_dims':(100,100),'out_dims':(100,100)}

	#Names of inputs this transform expects
	input_names=('input',)

	def read(self):
		'''Scale the given collection of point collections from the in_dims to the out_dims'''

		#Get the point collections
		point_colls=self.input.read()

		scaled_point_colls=[]

		#For each point collection
		for point_coll in point_colls:
			#Scale the points
			scaled_point_coll=[self.scale_point(point) for point in point_coll]
			scaled_point_colls.append(scaled_point_coll)

		return scaled_point_colls

	#Scales the given point from the in dimensions to the out dimensions
	def scale_point(self,point):
		scaled_point=[]
		for pos,num in enumerate(point):
			scaled_point.append(self.scale_num(num,pos))
		return tuple(scaled_point)

	#Scales the given number from the in dimension at 'index' to the out dimension at 'index'
	def scale_num(self,num,index):
		return int((float(num)/self.in_dims[index])*self.out_dims[index])
