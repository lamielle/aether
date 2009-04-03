"""A bare docstring in aether.core.__init__.py
"""
__doc__ = """Some documentation, per se"""

#AetherObject imports
from AetherObject import AetherObject

#AetherSettings imports
from AetherSettings import AetherSettings

#Module related imports
from AetherModule import AetherModule
from AetherParamModule import AetherParamModule

#Transform related imports
from AetherTransform import AetherTransform
from AetherTransformChain import AetherTransformChain
#from LazerPointerProvider import LazerPointerProvider

#Note: this is placed last as it causes problems if it is before the module related imports
from AetherDriver import AetherDriver
