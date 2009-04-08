'''
Transform chain that provides polygons for shadows in an autocalibrated scene
'''

from aether.core import AetherTransformChain

class ShadowPolyChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'camera':'CVMatPyGameSurface',
	            'cv_camera':'CVCamera',
	            'bgr2gray':'CVTColor',
	            'perspective':'CVPerspective',
	            'threshold':'CVThreshold',
	            'shadow':'ShadowPolys',
	            'invert':'CVInvert'
	            }

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'shadow':('threshold',),
	                'threshold':('invert',),
	                'invert':('perspective',),
	                'perspective':('bgr2gray',),
	                'bgr2gray':('cv_camera',)
	                }
	#transform_deps={'shadow':('threshold',),'threshold':('perspective',),'perspective':('bgr2gray',),'bgr2gray':('cv_camera',)}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='shadow'
