'''
Basic camera stream that provides a PyGame surface of a captured camera image that has been scaled to the dimensions of the Aether screen (aether.dims)
'''

from opencv import cv
from aether.core import AetherTransformChain,AetherObject

class ScaledCameraChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'camera':'CVMatPyGameSurface','flip_cam':'CVFlip','bgr2rgb':'CVTColor','cv_cam':'CVCamera'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'camera':('flip_cam',),'flip_cam':('bgr2rgb',),'bgr2rgb':('cv_cam',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='camera'

	#Settings values for transforms
	transform_settings={'cv_cam':{'capture_dims':AetherObject.settings.aether.dims}}
