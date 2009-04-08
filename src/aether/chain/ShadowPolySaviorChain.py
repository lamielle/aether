'''
Chain of transforms to extract laser points from a captured scene
'''

from aether.core import AetherTransformChain

class ShadowPolySaviorChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'shadow_savior':'ShadowPolySavior',
	            'perspective':'CVPerspective',
	            'cv_camera':'CVCamera',
	            }

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	#transform_deps={'laser_points':('extract_red','camera',),'extract_red':('perspective',),'perspective':('cv_camera',),'camera':('cv_camera',)}
	transform_deps={'shadow_savior':('perspective',),
	                'perspective':('cv_camera',),
	                }

	transform_settings={}
#bgr2rgb:
  #num_channels: 3
  #convert_method: 4 # cv.CV_BGR2RGB

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='shadow_savior'
