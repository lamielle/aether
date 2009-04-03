'''
Chain of transforms to extract laser points from a captured scene
'''

from aether.core import AetherTransformChain

class LaserPointerChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'laser_points':'LaserPoints','cv_camera':'CVCamera','extract_red':'CVExtractChannel','perspective':'CVPerspective','camera':'CVMatPyGameSurface'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'laser_points':('extract_red','camera',),'extract_red':('perspective',),'perspective':('cv_camera',),'camera':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='laser_points'
