'''
Transform chain that returns the biggest face that is detected from a camera.
'''

from aether.core import AetherTransformChain

class BiggestFaceChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'faces':'CVBiggestFaces','resize':'CVResize','gray_scale':'CVTColor','cv_camera':'CVCamera'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'faces':('resize',),'resize':('gray_scale',),'gray_scale':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='faces'
