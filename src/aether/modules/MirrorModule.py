'''
This is a very simple module that does nothing but display what a camera is seeing, a 'mirror'.

:Author: Alan LaMielle
'''

from aether.core import AetherModule
import pygame

class MirrorModule(AetherModule):

	#Default dependences
	deps=(('CameraInputProvider','face_cam'),)

	#Main 'action' method: This is called once each iteration of the game loop
	def draw(self,screen):
		#Get the current frame from the camera input provider
		curr_frame=self.face_cam.read()

		#Scale the current frame to the screen size
		scaled_curr_frame=pygame.transform.scale(curr_frame,self.dims)

		#Blit the current frame the the screen
		screen.blit(scaled_curr_frame,(0,0))
