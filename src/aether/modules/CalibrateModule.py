#!/usr/bin/env python

#--------------------------------------------------
#Aether Calibration Tool
#
#Utilizes pygame to do the drawing to the screen.
#Utilizes ocempgui for the pygame GUI library.
#
#Originally written by Alan LaMielle (lamielle AT cs DOT colostate DOT edu)
#
#AML 9/22/2008: Initial implementation.
#AML 9/25/2008: Added four point transform and enable/disable checkboxes
#AML 9/25/2008: Fixed bug with enable/disable buttons
#AML 10/3/2008: Classified! the calibrate tool so it is now self contained
#
#--------------------------------------------------

from ocempgui.widgets import Window,ImageMap,Table,HScale,Label,Button,ToggleButton,Renderer
from ocempgui.widgets.Constants import SIG_VALCHANGED,SIG_CLICKED

import pygame,pygame.locals

from PIL import ImageEnhance,ImageFilter,ImageDraw,Image

from threading import Thread

from AetherModule import AetherModule

#Circular ring buffer
class RingBuffer(object):

	def __init__(self,size):
		self.data=[None for i in xrange(size)]

	def push(self,item):
		self.data.pop(0)
		self.data.append(item)

	def clear(self):
		for i in xrange(4): self.push(None)

#Settings class for storing the current value of settings
class Settings(object):
	__slots__=('brightness','contrast','threshold','points','brightness_enable','contrast_enable','threshold_enable','points_enable','reference')

	def __init__(self):
		self.brightness=1.0
		self.contrast=1.0
		self.threshold=100
		self.points=RingBuffer(4)
		self.reference=(0,0,0)

		self.brightness_enable=True
		self.contrast_enable=True
		self.threshold_enable=True
		self.points_enable=True

class CalibrateModule(AetherModule):

	def __init__(self,driver,**kwargs):
		AetherModule.__init__(self,driver,**kwargs)

		self.diffp=driver.diffp

		#Create the main window (renderer)
		self.renderer=Renderer()
		self.renderer.screen=driver.screen
		self.renderer.title='Camera Viewer'
		self.renderer.color=(234,228,223)

		#Create the settings window
		self.settings=Settings()
		self.settings_window=self.get_settings_window('Settings',(self.diffp.get_capture_size()[0]/2+60,self.diffp.get_capture_size()[1]+25),self.settings)
		self.renderer.add_widget(self.settings_window)

		#Create the raw camera feed window
		self.raw_cam_surface=pygame.Surface(self.diffp.get_capture_size())
		self.raw_cam_window=self.get_surface_window('Raw Camera Feed',(0,0),self.raw_cam_surface)
		self.raw_cam_window.set_focus()
		def clicked(imagemap):
			self.settings.points.push(imagemap.relative_position)
		self.raw_cam_window.child.connect_signal(SIG_CLICKED,clicked,self.raw_cam_window.child)
		self.renderer.add_widget(self.raw_cam_window)

		#Create the modified camera feed window
		def get_reference(imagemap):
			self.settings.reference = imagemap.image.map_rgb(imagemap.image.get_at(imagemap.relative_position)) 
			print imagemap.image.get_at(imagemap.relative_position)

		self.mod_cam_surface=pygame.Surface(self.diffp.get_capture_size())
		self.mod_cam_window=self.get_surface_window('Modified Camera Feed',(self.diffp.get_capture_size()[0]+10,0),self.mod_cam_surface)
		self.mod_cam_window.child.connect_signal(SIG_CLICKED,get_reference,self.mod_cam_window.child)
		self.renderer.add_widget(self.mod_cam_window)

	def process_event(self,event) :
		if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_x :
			print "Writing capture to disk"
			self.capture_img.save('thresh_capture.png')
		self.renderer.distribute_events(event)

	#Creates a ocempgui Window object with the given title,
	#placed at the given position, that contains an ImageMap
	#of the given pygame Surface object
	def get_surface_window(self,title,pos,surface):
		window=Window(title)
		window.child=ImageMap(surface)
		window.topleft=pos
		window.depth=1
		return window

	#Creates a window with controls for modifying the camera feed
	def get_settings_window(self,title,pos,settings):
		window=Window(title)
		window.child=Table(2,1)
		window.topleft=pos
		window.depth=1

		def brightness_changed(scale,label):
			self.settings.brightness=scale.value
			label.text='%3.2f'%self.settings.brightness
		def brightness_toggle_changed(toggle):
			self.settings.brightness_enable=not toggle.active
		def contrast_changed(scale,label):
			self.settings.contrast=scale.value
			label.text='%3.2f'%self.settings.contrast
		def contrast_toggle_changed(toggle):
			self.settings.contrast_enable=not toggle.active
		def threshold_changed(scale,label):
			self.settings.threshold=scale.value
			label.text='%d'%self.settings.threshold
		def threshold_toggle_changed(toggle):
			self.settings.threshold_enable=not toggle.active
		def points_toggle_changed(toggle):
			self.settings.points_enable=not toggle.active

		#Setup the slider table
		slider_table=Table(4,4)
		window.child.add_child(0,0,slider_table)

		brightness_label=Label('Brightness:')
		brightness_toggle=ToggleButton('')
		brightness_value_label=Label('')
		brightness_scale=HScale(0,2,0.1)
		brightness_scale.connect_signal(SIG_VALCHANGED,brightness_changed,brightness_scale,brightness_value_label)
		brightness_toggle.connect_signal(SIG_CLICKED,brightness_toggle_changed,brightness_toggle)

		slider_table.add_child(0,0,brightness_label)
		slider_table.add_child(0,1,brightness_toggle)
		slider_table.add_child(0,2,brightness_scale)
		slider_table.add_child(0,3,brightness_value_label)

		brightness_toggle.active=True
		brightness_scale.value=self.settings.brightness

		contrast_label=Label('Contrast:')
		contrast_toggle=ToggleButton('')
		contrast_value_label=Label('')
		contrast_scale=HScale(0,2,0.1)
		contrast_scale.connect_signal(SIG_VALCHANGED,contrast_changed,contrast_scale,contrast_value_label)
		contrast_toggle.connect_signal(SIG_CLICKED,contrast_toggle_changed,contrast_toggle)

		slider_table.add_child(1,0,contrast_label)
		slider_table.add_child(1,1,contrast_toggle)
		slider_table.add_child(1,2,contrast_scale)
		slider_table.add_child(1,3,contrast_value_label)

		contrast_toggle.active=True
		contrast_scale.value=self.settings.contrast

		threshold_label=Label('Threshold:')
		threshold_toggle=ToggleButton('')
		threshold_value_label=Label('')
		threshold_scale=HScale(0,255,1)
		threshold_scale.connect_signal(SIG_VALCHANGED,threshold_changed,threshold_scale,threshold_value_label)
		threshold_toggle.connect_signal(SIG_CLICKED,threshold_toggle_changed,threshold_toggle)

		slider_table.add_child(2,0,threshold_label)
		slider_table.add_child(2,1,threshold_toggle)
		slider_table.add_child(2,2,threshold_scale)
		slider_table.add_child(2,3,threshold_value_label)

		threshold_toggle.active=True
		threshold_scale.value=self.settings.threshold

		points_label=Label('Transform:')
		points_toggle=ToggleButton('')
		points_toggle.connect_signal(SIG_CLICKED,points_toggle_changed,points_toggle)

		slider_table.add_child(3,0,points_label)
		slider_table.add_child(3,1,points_toggle)

		points_toggle.active=True
		points_toggle.active=True

		def reset_settings(brightness_scale,brightness_toggle,contrast_scale,contrast_toggle,threshold_scale,threshold_toggle,points_toggle,settings):
			settings.brightness=1.0
			settings.brightness_enable=True
			settings.contrast=1.0
			settings.contrast_enable=True
			settings.threshold=100
			settings.threshold_enable=True
			settings.points.clear()
			settings.points_enable=True

			brightness_scale.value=settings.brightness
			contrast_scale.value=settings.contrast
			threshold_scale.value=settings.threshold

			brightness_toggle.active=settings.brightness_enable
			contrast_toggle.active=settings.contrast_enable
			threshold_toggle.active=settings.threshold_enable
			points_toggle.active=settings.points_enable

		reset_button=Button('Reset')
		reset_button.connect_signal(SIG_CLICKED,reset_settings,brightness_scale,brightness_toggle,contrast_scale,contrast_toggle,threshold_scale,threshold_toggle,points_toggle,self.settings)

		window.child.add_child(1,0,reset_button)

		reset_settings(brightness_scale,brightness_toggle,contrast_scale,contrast_toggle,threshold_scale,threshold_toggle,points_toggle,self.settings)

		return window

	#Order the given four points counter-clockwise
	def get_points(self,points):
		points=list(points)
		#Look for the top left point
		for point1 in points:
			less_x=0
			less_y=0
			#Look at each other point
			for point2 in (point for point in points if point!=point1):
				#See if point1 is less than the other point
				#in either the x or y dimension
				if point1[0]<=point2[0]: less_x+=1
				if point1[1]<=point2[1]: less_y+=1
			#If the current point1 was less than two other points in both
			#the x any y dimensions, it is the top left
			if less_x>1 and less_y>1:
				top_left=point1
				break
		points.remove(top_left)

		#Find the bottom left point
		for point1 in points:
			less_x=0
			for point2 in points:
				if point1[0]<=point2[0]:
					less_x+=1
			if less_x>1:
				bottom_left=point1
				break
		points.remove(bottom_left)

		#Find the bottom/top right points
		if points[0][1]<points[1][1]:
			bottom_right=points[1]
			top_right=points[0]
		else:
			bottom_right=points[0]
			top_right=points[1]

		return (top_left[0],top_left[1],bottom_left[0],bottom_left[1],bottom_right[0],bottom_right[1],top_right[0],top_right[1])

	def draw(self,screen):
		#Raw camera feed
		capture_img = self.diffp.get_curr_capture()

		if self.settings.points_enable:
			draw=ImageDraw.Draw(capture_img)
			for point in (point for point in self.settings.points.data if None is not point):
				draw.ellipse((point[0]-2,point[1]-2)+(point[0]+2,point[1]+2),outline='red',fill=True)
		capture = pygame.image.fromstring(capture_img.tostring(),capture_img.size,'RGB')
		capture = capture.convert()
		self.raw_cam_surface.blit(capture,(0,0))

		#Modified feed
		capture_img = self.diffp.get_curr_capture()

		if self.settings.brightness_enable:
			capture_img=ImageEnhance.Brightness(capture_img).enhance(self.settings.brightness)

		if self.settings.contrast_enable:
			capture_img=ImageEnhance.Contrast(capture_img).enhance(self.settings.contrast)

		if self.settings.threshold_enable:
			capture_img=capture_img.convert('I').convert('RGB')
			capture_img=capture_img.point(lambda x: [255,0][x<=self.settings.threshold])

		if self.settings.points_enable:
			if 4==len([point for point in self.settings.points.data if None is not point]):
				points=list(self.settings.points.data)
				points.sort()
				capture_img=capture_img.transform(capture_img.size,Image.QUAD,self.get_points(points))

	#	capture_img=capture_img.filter(ImageFilter.BLUR)
	#	capture_img=capture_img.filter(ImageFilter.CONTOUR)
	#	capture_img=capture_img.filter(ImageFilter.DETAIL)
	#	capture_img=capture_img.filter(ImageFilter.EDGE_ENHANCE)
	#	capture_img=capture_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	#	capture_img=capture_img.filter(ImageFilter.EMBOSS)
		capture_img=capture_img.filter(ImageFilter.FIND_EDGES)
		capture_img=capture_img.filter(ImageFilter.SMOOTH)
	#	capture_img=capture_img.filter(ImageFilter.SMOOTH_MORE)
	#	capture_img=capture_img.filter(ImageFilter.SHARPEN)

	#	capture_img=capture_img.convert('L').convert('RGB')
		self.capture_img = capture_img

		data=list(capture_img.convert('L').getdata())
		width=self.diffp.get_capture_size()[0]
		height=self.diffp.get_capture_size()[1]

		#capture_img.convert('L').save('test.png')

	#	print (data[0],data[1],data[2],data[width],data[width+1],data[width+2])
		points=[[col,row] for row in xrange(1,height-1) for col in xrange(1,width-1) if 255==data[col+width*row]]
		from quickhull2d import qhull
		from Numeric import array
	#	print array(points)
	#	print points
		new_points=[tuple(i) for i in qhull(array(points)).tolist()]
	#	print new_points
	#	print new_points

		#if len(new_points)>2:
			#draw=ImageDraw.Draw(capture_img)
			#draw.polygon(new_points,outline='red')

		capture=pygame.image.fromstring(capture_img.tostring(),capture_img.size,'RGB')
		capture=capture.convert()
		self.mod_cam_surface.blit(capture,(0,0))

		#Invalidate the ImageMaps that show the surfaces so they will get redrawn
		self.raw_cam_window.child.invalidate(pygame.Rect(0,0,self.diffp.get_capture_size()[0],self.diffp.get_capture_size()[1]))
		self.mod_cam_window.child.invalidate(pygame.Rect(0,0,self.diffp.get_capture_size()[0],self.diffp.get_capture_size()[1]))

		self.renderer.update()

#Run the calibrate tool as a standalone application
if '__main__'==__name__:
	from AetherModule import TestAetherModule
	from AetherDriver import AetherDriver
	from DiffProvider import DiffProvider
	driver=AetherDriver(640,DiffProvider())
	driver.register_module(CalibrateModule(driver))
	driver.run()
