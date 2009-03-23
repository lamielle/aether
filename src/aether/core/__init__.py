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

#Input provider related imports
from InputProvider import InputProvider
from CameraInputProvider import CameraInputProvider
from FaceInputProvider import FaceInputProvider
from MouseInputProvider import MouseInputProvider

#Note: this is placed last as it causes problems if it is before the module related imports
from AetherDriver import AetherDriver
