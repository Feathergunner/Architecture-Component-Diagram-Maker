#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import re

tex_global_scale_factor = 0.6

box_method_width = 5.5
box_method_height = 1.5

box_class_space_left = 0.5
box_class_space_right = 0.5
box_class_space_top = 1.5
box_class_space_inner = 0.5
box_class_space_bottom = 0.5

box_component_space_left = 0.5
box_component_space_right = 0.5
box_component_space_top = 1.5
box_component_space_inner = 0.5
box_component_space_bottom = 0.5

inter_component_space = 3

def clean_string(string):
	return re.sub("[^A-Za-z0-9]", "", string)

def get_box_class_totalwidth():
	return box_method_width+box_class_space_left+box_class_space_right

def get_box_class_totalheight(number_of_methods):
	return number_of_methods*box_method_height + (number_of_methods-1)*box_class_space_inner + box_class_space_top + box_class_space_bottom
	
def get_box_component_totalwidth():
	return get_box_class_totalwidth()+box_component_space_left+box_component_space_right
	
