#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import globals

class ComponentContainer:
	def __init__(self, label, order_number=0, colorstring = "red"):
		self.label = label
		self.order_number = order_number
		self.classcontainer = []
		self.colorstring = colorstring
		
	def set_position(self, new_order_number):
		self.order_number = new_order_number
		
	def set_color(self, new_color):
		self.colorstring = new_color
		
	def add_classcontainer(self, new_class):
		self.classcontainer.append(new_class)
		
	def draw(self, diagram, x, y, grid_x, grid_y):
		# draw box
		diagram.add_component_box(x=x, y=y, height=self.get_height(), colorstring=self.colorstring+"!20", label=self.label)
		# draw subboxes:
		self.classcontainer.sort(key = lambda x: x.order_number)
		offset_y = globals.box_component_space_top
		for classc in self.classcontainer:
			classc.draw(diagram=diagram, x=x+globals.box_component_space_left, y=y-offset_y, color=self.colorstring, grid_x=grid_x, grid_y=grid_y)
			offset_y += classc.get_height()+globals.box_component_space_inner
			grid_y += 100
			
	def get_height(self):
		totalheight = globals.box_component_space_top
		for classc in self.classcontainer:
			totalheight += classc.get_height()
		totalheight += (len(self.classcontainer)-1)*globals.box_component_space_inner
		totalheight += globals.box_component_space_bottom
		
		return totalheight

	def get_number_of_methods(self):
		number_of_methods = 0
		for c in self.classcontainer:
			number_of_methods += c.get_number_of_methods()
		return number_of_methods
		
	def get_clean_label(self):
		return globals.clean_string(self.label)