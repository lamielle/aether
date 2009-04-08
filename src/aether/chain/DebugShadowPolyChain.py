'''
Chain of transforms to extract laser points from a captured scene
'''

from aether.core import AetherTransformChain

class DebugShadowPolyChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'shadow':'DebugShadowPolys',
	            'shadow_poly':'ShadowPolys',
	            'thresh2pg':'CVMatPyGameSurface',
	            'camera':'CVMatPyGameSurface',
	            'threshold':'CVThreshold',
	            'invert':'CVInvert',
	            'perspective':'CVPerspective',
	            'bgr2gray':'CVTColor',
	            'cv_camera':'CVCamera',
	            }

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	#transform_deps={'laser_points':('extract_red','camera',),'extract_red':('perspective',),'perspective':('cv_camera',),'camera':('cv_camera',)}
	transform_deps={'shadow':('thresh2pg','camera','shadow_poly',),
	                'shadow_poly':('invert',),
	                'thresh2pg':('threshold',),
	                'camera':('perspective',),
	                'invert':('threshold',),
	                'threshold':('perspective',),
	                'perspective':('bgr2gray',),
	                'bgr2gray':('cv_camera',),
	                }

	transform_settings={'threshold':{'channels':[0],'thresholds':[176,0,0,0],'max_thresholds':[255,0,0,0]},'bgr2gray':{'num_channels':1,'convert_method':6},}
#bgr2rgb:
  #num_channels: 3
  #convert_method: 4 # cv.CV_BGR2RGB

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='shadow'
