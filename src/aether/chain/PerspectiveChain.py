'''
Transform chain that uses the CVPerspective transform to map a projector area into Aether coordinate space
'''

from aether.core import AetherTransformChain

class PerspectiveChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'camera':'CVMatPyGameSurface','cv_camera':'CVCamera','bgr2rgb':'CVTColor','perspective':'CVPerspective'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'camera':('perspective',),'perspective':('bgr2rgb',),'bgr2rgb':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='camera'
