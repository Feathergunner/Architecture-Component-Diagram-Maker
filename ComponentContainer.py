#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import globals

class ComponentContainer:
	def __init__(self, label, order_number=0, colorstring = "red"):
		self.label = label
		self.order_number = order_number
		self.subcomponents = []
		self.methods = []
		self.colorstring = colorstring
		self.color_intensity = 20
		self.width = -1
		#self.is_toplevel = is_toplevel_comp
		
	def set_position(self, new_order_number):
		self.order_number = new_order_number
		
	def set_color(self, new_color):
		self.colorstring = new_color
		
	def set_color_intensity(self, new_color_intensity):
		self.color_intensity = new_color_intensity
		
	def add_subcomponent(self, subcomponent):
		subcomponent.set_color_intensity(self.color_intensity+10)
		self.subcomponents.append(subcomponent)
		
	def add_method(self, new_method):
		self.methods.append(new_method)
		
	def draw(self, diagram, x, y, grid_x, grid_y):
		# draw box
		diagram.add_component_box(x=x, y=y, width=self.get_width(), height=self.get_height(), colorstring=self.colorstring+"!"+str(self.color_intensity), label=self.label)
		
		x += globals.box_component_space_left
		offset_y = globals.box_component_space_top		
		
		# draw methods:
		self.methods.sort(key=lambda x: x.order_number)
		for method in self.methods:
			method.draw(diagram=diagram, x=x, y=y-offset_y, color=self.colorstring, grid_x=grid_x, grid_y=grid_y)
			offset_y += globals.box_class_space_inner+globals.box_method_height
			grid_y += 1
			
		if (len(self.methods) > 0) and (len(self.subcomponents) > 0):
			offset_y += globals.box_component_space_inner
			
		# draw subcomponents:
		self.subcomponents.sort(key = lambda x: x.order_number)
		for comp in self.subcomponents:
			comp.draw(diagram=diagram, x=x, y=y-offset_y, grid_x=grid_x, grid_y=grid_y)
			offset_y += comp.get_height()+globals.box_component_space_inner
			grid_y += 100
			
	def get_height(self):
		totalheight = globals.box_component_space_top
		totalheight += len(self.methods)*globals.box_method_height + (len(self.methods)-1)*globals.box_component_space_inner
		if len(self.methods) > 0 and len(self.subcomponents) > 0:
			totalheight += globals.box_component_space_inner
		for comp in self.subcomponents:
			totalheight += comp.get_height()
		totalheight += (len(self.subcomponents)-1)*globals.box_component_space_inner
		totalheight += 2*globals.box_component_space_bottom
		
		return totalheight
	
	def get_width(self):
		max_width_of_subcomponent = -1
		if len(self.subcomponents) > 0:
			for comp in self.subcomponents:
				comp_width = comp.get_width()
				if (max_width_of_subcomponent < 0) or (comp_width > max_width_of_subcomponent):
					max_width_of_subcomponent = comp_width
			width = max_width_of_subcomponent + globals.box_component_space_left + globals.box_component_space_right
		else:
			width = globals.box_method_width + globals.box_component_space_left + globals.box_component_space_right
		self.set_width(width)
		return self.width
		
	def set_width(self, new_width):
		self.width = new_width
		for comp in self.subcomponents:
			comp.set_width(new_width-globals.box_component_space_left-globals.box_component_space_right)

	def get_number_of_methods(self):
		number_of_methods = 0
		for comp in self.subcomponents:
			number_of_methods += comp.get_number_of_methods()
		return number_of_methods
		
	def get_clean_label(self):
		return globals.clean_string(self.label)