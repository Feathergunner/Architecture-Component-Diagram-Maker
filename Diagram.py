#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import os

import globals

class Diagram:
	def __init__(self):
		self.componentcontainer = []
		self.classcontainer = []
		self.methods = []
		self.actions = []
		self.tikzstring = ""
		
	def add_component(self, new_component):
		self.componentcontainer.append(new_component)
		
	def add_class(self, new_class, master_component_name):
		self.classcontainer.append(new_class)
		self.componentcontainer[self.get_component_id(master_component_name)].add_classcontainer(new_class)
	
	def add_method(self, new_method, master_class_name):
		self.methods.append(new_method)
		self.classcontainer[self.get_class_id(master_class_name)].add_method(new_method)
		
	def add_action(self, new_action):
		self.actions.append(new_action)
		action_id = len(self.actions)-1
		self.methods[self.get_method_id(new_action.source)].adjacent_actions.append(action_id)
		self.methods[self.get_method_id(new_action.target)].adjacent_actions.append(action_id)
		
	def draw(self):
		self.componentcontainer.sort(key=lambda x: x.order_number)
		offset_x = 0
		grid_x = 0
		for component in self.componentcontainer:
			component.draw(self, offset_x, grid_x)
			offset_x += globals.get_box_component_totalwidth()+globals.inter_component_space
			grid_x += 1
			
		for action_id in range(len(self.actions)):
			action = self.actions[action_id]
			source_method_id = self.get_method_id(action.source)
			target_method_id = self.get_method_id(action.target)
			source_grid_x = self.methods[source_method_id].grid_pos_x
			source_grid_y = self.methods[source_method_id].grid_pos_y
			target_grid_x = self.methods[target_method_id].grid_pos_x
			target_grid_y = self.methods[target_method_id].grid_pos_y
			
			if source_grid_x < target_grid_x:
				source_angle = 0
				target_angle = 180
			elif source_grid_x > target_grid_x:
				source_angle = 180
				target_angle = 0
			elif source_grid_y < target_grid_y:
				source_angle = 0
				target_angle = 0
			else:
				source_angle = 180
				target_angle = 180
			
			source_actions = self.methods[source_method_id].adjacent_actions
			if len(source_actions) > 1:
				source_action_index = [i for i,a in enumerate(source_actions) if a == action_id][0]
				source_angle_offset = (source_action_index * 20.0)/(len(source_actions)-1) - 10
			else:
				source_action_index = 1
				source_angle_offset = 0
			
			target_actions = self.methods[target_method_id].adjacent_actions
			if len(target_actions) > 1:
				target_action_index = [i for i,a in enumerate(target_actions) if a == action_id][0]
				target_angle_offset = (target_action_index * 20.0)/(len(target_actions)-1) - 10
			else:
				target_action_index = 1
				target_angle_offset = 0
				
			self.tikzstring += "\\draw[thick,->] (METHOD-"+globals.clean_string(action.source)+"."+str(source_angle-source_angle_offset)+") to[out="+str(source_angle-source_angle_offset)+", in="+str(target_angle-target_angle_offset)+"] (METHOD-"+globals.clean_string(action.target)+"."+str(target_angle-target_angle_offset)+");\n"
			
	def get_class_id(self, classname):
		return [i for i,c in enumerate(self.classcontainer) if c.label == classname][0]
		
	def get_component_id(self, componentname):
		return [i for i,c in enumerate(self.componentcontainer) if c.label == componentname][0]
		
	def get_method_id(self, methodname):
		return [i for i,m in enumerate(self.methods) if m.label == methodname][0]
		
	def add_method_box(self, x, y, colorstring, label):
		self.tikzstring += "\\node [anchor=north west, rectangle, draw, fill="+colorstring+", text width="+str(globals.box_method_width)+"cm, text centered, rounded corners, minimum height="+str(globals.box_method_height)+"cm] (METHOD-"+globals.clean_string(label)+") at ("+str(x)+","+str(y)+") {\\textbf{"+label+"}};\n"
		
	def add_class_box(self, x, y, height, colorstring, label):
		self.tikzstring += "\\draw [draw, fill="+colorstring+", rounded corners] ("+str(x)+","+str(y)+") rectangle ("+str(x+globals.get_box_class_totalwidth())+","+str(y-height)+");\n"
		self.tikzstring += "\\node [anchor=north west] (CLASS-"+globals.clean_string(label)+")  at ("+str(x+0.5)+","+str(y-0.5)+") {\\large\\textbf{"+label+"}};\n"
		
	def add_component_box(self, x, y, height, colorstring, label):
		self.tikzstring += "\\draw [draw, fill="+colorstring+", rounded corners] ("+str(x)+","+str(y)+") rectangle ("+str(x+globals.get_box_component_totalwidth())+","+str(y-height)+");\n"
		self.tikzstring += "\\node [anchor=north west] (COMP-"+globals.clean_string(label)+") at ("+str(x+0.5)+","+str(y-0.5)+") {\\large\\textbf{"+label+"}};\n"
		
	def write_texfile(self, outputfilename="test.tex"):
		texstring = ""
		templatefile = open("tex_template.txt", 'r')
		for line in templatefile:
			texstring += line
		if not os.path.exists("tex"):
			os.makedirs("tex/")
		outfile = open("tex/"+outputfilename, 'w')
		
		outfile.write(texstring)
		outfile.write("\\begin{tikzpicture}[scale="+str(globals.tex_global_scale_factor)+",  every node/.style={scale="+str(globals.tex_global_scale_factor)+"}]")
		outfile.write(self.tikzstring)
		outfile.write("\\end{tikzpicture}\n\\end{document}\n")
		outfile.close()
		