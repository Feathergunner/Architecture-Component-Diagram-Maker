#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import os

import globals

class Diagram:
	def __init__(self):
		self.componentcontainer = []
		self.methods = []
		self.actions = []
		self.tikzstring = ""
		
	def add_component(self, new_component):
		self.componentcontainer.append(new_component)
		return len(self.componentcontainer)-1
	
	def add_method(self, new_method):
		self.methods.append(new_method)
		return len(self.methods)-1
		
	def add_action(self, new_action):
		self.actions.append(new_action)
		action_id = len(self.actions)-1
		self.methods[self.get_method_index(new_action.source)].adjacent_actions.append(action_id)
		self.methods[self.get_method_index(new_action.target)].adjacent_actions.append(action_id)
		
	def draw(self):
		print ("Draw diagram...")
		self.componentcontainer.sort(key=lambda x: x.order_number)
		offset_x = 0
		offset_y = 0
		grid_x = 0
		grid_y = 0
		current_comp_order_number = self.componentcontainer[0].order_number
		current_column_max_width = self.componentcontainer[0].get_width()
		for c_id in range(len(self.componentcontainer)):
			component = self.componentcontainer[c_id]
			if (component.order_number > current_comp_order_number):
				offset_x += current_column_max_width + globals.inter_component_space
				grid_x += 1
				offset_y = 0
				grid_y = 0
				current_column_max_width = component.get_width()
			elif c_id > 0:
				offset_y -= self.componentcontainer[c_id-1].get_height()+globals.inter_component_space_v
				grid_y += self.componentcontainer[c_id-1].get_number_of_methods()
				current_column_max_width = max(current_column_max_width, component.get_width())
			component.draw(self, offset_x, offset_y, grid_x, grid_y)
			current_comp_order_number = component.order_number
            
			
		for action_id in range(len(self.actions)):
			action = self.actions[action_id]
			source_method_id = self.get_method_index(action.source)
			target_method_index = self.get_method_index(action.target)
			source_grid_x = self.methods[source_method_id].grid_pos_x
			source_grid_y = self.methods[source_method_id].grid_pos_y
			target_grid_x = self.methods[target_method_index].grid_pos_x
			target_grid_y = self.methods[target_method_index].grid_pos_y
			
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
			
			target_actions = self.methods[target_method_index].adjacent_actions
			if len(target_actions) > 1:
				target_action_index = [i for i,a in enumerate(target_actions) if a == action_id][0]
				target_angle_offset = (target_action_index * 20.0)/(len(target_actions)-1) - 10
			else:
				target_action_index = 1
				target_angle_offset = 0
				
			final_source_angle = int(source_angle-source_angle_offset)
			final_target_angle = int(target_angle-target_angle_offset)
				
			self.tikzstring += "\\draw[thick,->] ("+action.source+"."+str(final_source_angle)+") to[out="+str(final_source_angle)+", in="+str(final_target_angle)+"] ("+action.target+"."+str(final_target_angle)+");\n"
		print("Done.")
		
	def get_component_index(self, componentname):
		return [i for i,c in enumerate(self.componentcontainer) if c.label == componentname][0]
	
	def get_method_index(self, method_id):
		return [i for i,m in enumerate(self.methods) if m.method_id == method_id][0]
		
	def add_method_box(self, x, y, colorstring, label, id):
		self.tikzstring += "\\node [anchor=north west, rectangle, draw, fill="+colorstring+", text width="+str(globals.box_method_width)+"cm, text centered, rounded corners, minimum height="+str(globals.box_method_height)+"cm] ("+id+") at ("+str(x)+","+str(y)+") {\\large\\textbf{"+label+"}};\n"
		
	def add_component_box(self, x, y, width, height, colorstring, label):
		self.tikzstring += "\\draw [draw, fill="+colorstring+", rounded corners] ("+str(x)+","+str(y)+") rectangle ("+str(x+width)+","+str(y-height)+");\n"
		self.tikzstring += "\\node [anchor=north west] (COMP-"+globals.clean_string(label)+") at ("+str(x+0.5)+","+str(y-0.5)+") {\\Large\\textbf{"+label+"}};\n"
		
	def write_texfile(self, outputfilename="test.tex"):
		print("Write texfile...")
		texstring = ""
		templatefile = open("tex_template.txt", 'r')
		for line in templatefile:
			texstring += line
		if not os.path.exists("tex"):
			os.makedirs("tex/")
		outfile = open("tex/"+outputfilename, 'w')
		
		outfile.write(texstring)
		outfile.write("\\begin{tikzpicture}[scale="+str(globals.tex_global_scale_factor)+",  every node/.style={scale="+str(globals.tex_global_scale_factor)+"}, font=\sffamily]\n")
		outfile.write(self.tikzstring)
		outfile.write("\\end{tikzpicture}\n\\end{document}\n")
		outfile.close()
		print("Done.")
		