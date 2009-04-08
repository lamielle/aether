'''
Chain of transforms to extract laser points from a captured scene
'''

from aether.core import AetherTransformChain

class DebugLaserPointerChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'laser':'DebugLaserPoints',
	            'thresh2pg':'CVMatPyGameSurface',
	            'red2pg':'CVMatPyGameSurface',
	            'camera':'CVMatPyGameSurface',
	            'ext_red':'CVSpecifyChannels',
	            'thresh':'CVThreshold',
	            'bgr2rgb':'CVTColor',
	            'bgr2rgb2':'CVTColor',
	            'perspective':'CVPerspective',
	            'cv_camera':'CVCamera',
	            }

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	#transform_deps={'laser_points':('extract_red','camera',),'extract_red':('perspective',),'perspective':('cv_camera',),'camera':('cv_camera',)}
	transform_deps={'laser':('thresh2pg','red2pg','camera','thresh',),
	                'thresh2pg':('thresh',),
	                'red2pg':('ext_red',),
	                'camera':('bgr2rgb',),
	                'thresh':('ext_red',),
	                'ext_red':('bgr2rgb2',),
	                'bgr2rgb2':('perspective',),
	                'bgr2rgb':('perspective',),
	                'perspective':('cv_camera',),
	                }

	transform_settings={'thresh':{'channels':[0],'thresholds':[176,0,0,0],'max_thresholds':[255,0,0,0]},'bgr2rgb':{'num_channels':3,'convert_method':4},'ext_red':{'channels':[0]}}
#bgr2rgb:
  #num_channels: 3
  #convert_method: 4 # cv.CV_BGR2RGB

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='laser'
