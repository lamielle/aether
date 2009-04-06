'''
Transform chain that uses only the MouseInput transform
'''

from aether.core import AetherTransformChain

class MouseChain(AetherTransformChain):

	#Transforms in this chain: names and their type
	transforms={'mouse':'PyGameMouse'}

	#Dependences from transform to transform, referenced by names defined in the 'transforms' field
	transform_deps={'mouse':()}

	#Defines the name of the start of the chain
	#This should be automatically calculated somehow
	#Possibly by building a graph of the deps, toplolgically sorting the graph, and taking the nodes that nothing depends on
	#For now this is explicitly defined
	start='mouse'
