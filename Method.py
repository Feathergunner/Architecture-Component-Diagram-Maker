#!usr/bin/python3
# -*- coding: utf-8 -*-import string

class Method:
	def __init__(self, label, order_number=0, method_id="noid"):
		self.label = label
		self.order_number = order_number
		self.method_id = method_id
		self.adjacent_actions = []
		self.grid_pos_x = -1
		self.grid_pos_y = -1
		
	def set_position(self, order_number):
		self.position = order_number
		
	def draw(self, diagram, x, y, color, grid_x, grid_y):
		diagram.add_method_box(x=x, y=y, colorstring=color+"!60", label=self.label, id=self.method_id)
		self.grid_pos_x = grid_x
		self.grid_pos_y = grid_y
		
	def get_height(self):
		return globals.box_method_height
	
	def get_clean_label(self):
		return globals.clean_string(self.label)