'''
Transform chain that returns the faces that are detected from a camera.
'''

from opencv import cv
from aether.core import AetherTransformChain,AetherObject

class FacesChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'scaled_faces':'ScalePoints','faces':'CVFaces','resize':'CVResize','gray_scale':'CVTColor','flip':'CVFlip','cv_camera':'CVCamera'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'scaled_faces':('faces',),'faces':('resize',),'resize':('gray_scale',),'gray_scale':('flip',),'flip':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='scaled_faces'

	transform_settings={
	     'scaled_faces':{'in_dims':(180,120),'out_dims':AetherObject.settings.aether.dims},
	     'resize':{'new_size':(180,120),'interplation_method':cv.CV_INTER_NN},
	     'gray_scale':{'convert_method':cv.CV_BGR2GRAY,'num_channels':1}}
