'''
This is a very simple module that does nothing but display what a camera is seeing, a 'mirror'.

:Author: Alan LaMielle
'''

from aether.core import AetherModule
import pygame

class MirrorModule(AetherModule):

	#Chains this module needs
	chains={'camera':'ScaledCameraChain'}

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#Get the current frame from the camera transform
		curr_frame=self.camera.read()

		#Blit the current frame the the screen
		screen.blit(curr_frame,(0,0))
