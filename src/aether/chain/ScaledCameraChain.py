'''
Basic camera stream that provides a PyGame surface of a captured camera image that has been scaled to the dimensions of the Aether screen (aether.dims)
'''

from aether.core import AetherTransformChain

class ScaledCameraChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'camera':'CVMatPyGameSurface','cv_camera':'CVCamera','flip_camera':'CVFlip'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'camera':('flip_camera',),'flip_camera':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='camera'
