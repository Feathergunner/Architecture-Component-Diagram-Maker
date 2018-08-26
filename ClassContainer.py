#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import globals

class ClassContainer:
	def __init__(self, label, order_number=0):
		self.label = label
		self.order_number = order_number
		self.methods = []
		
	def set_position(self, order_number):
		self.order_number = order_number
	
	def add_method(self, new_method):
		self.methods.append(new_method)
		
	def draw(self, diagram, x, y, color, grid_x, grid_y):
		print ("draw class at x: "+str(x)+", y: "+str(y))
		# draw box
		diagram.add_class_box(x=x, y=y, height=self.get_height(), colorstring=color+"!40", label=self.label)
		# draw subboxes:
		self.methods.sort(key=lambda x: x.order_number)
		class_offset_y = globals.box_class_space_top
		for method in self.methods:
			method.draw(diagram=diagram, x=x+globals.box_class_space_left, y=y-class_offset_y, color=color, grid_x=grid_x, grid_y=grid_y)
			class_offset_y += globals.box_class_space_inner+globals.box_method_height
			grid_y += 1
		
	def get_height(self):
		return globals.get_box_class_totalheight(len(self.methods))
		
	def get_clean_label(self):
		return globals.clean_string(self.label)