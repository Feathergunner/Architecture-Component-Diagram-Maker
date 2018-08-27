#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET

import Diagram as dia
import ComponentContainer as coco
import Method as me
import Action as ac
import globals

def parse_component(diagram, comp, order_num, master_comp=None, colorstring="blue"):
	print ("parse component: "+comp.attrib["label"])
	print ("master comp: "+str(master_comp))
	if "order_number" in comp.attrib:
		current_comp_order_num = int(comp.attrib["order_number"])
	else:
		current_comp_order_num = order_num + 1
	if "colorstring" in comp.attrib:
		color = comp.attrib["colorstring"]
	else:
		color = colorstring
	new_component = coco.ComponentContainer(
		label=comp.attrib["label"],
		order_number=current_comp_order_num,
		colorstring=color)
	if not master_comp == None:
		master_comp.add_subcomponent(new_component)
	else:
		current_comp_id = diagram.add_component(new_component)
	
	method_order_num = 1
	for child in comp:
		#print (child.tag, child.attrib)
		if child.tag == "method":
			parse_method(diagram, child, method_order_num, colorstring, new_component)
			method_order_num += 1
		elif child.tag == "component":
			parse_component(diagram, child, current_comp_order_num, master_comp=new_component, colorstring=color)

def parse_method(diagram, method, order_num, colorstring, master_component):
	print ("parse method: "+method.attrib["label"])
	if "order_number" in method.attrib:
		current_method_order_num = int(method.attrib["order_number"])
	else:
		current_method_order_num = order_num
	if "id" in method.attrib:
		current_method_id = method.attrib["id"]
	else:
		current_method_id = "noid"
	new_method = me.Method(
		label=method.attrib["label"],
		order_number=current_method_order_num,
		method_id=current_method_id)
	master_component.add_method(new_method)
	diagram.add_method(new_method)	

def parse_xml(filename_arch_specs_xml):
	#print("create_from_xml")
	diagram = dia.Diagram()

	tree = ET.parse(filename_arch_specs_xml)
	root = tree.getroot()
	#current_component_name = ""
	current_comp_order_num = 1
	for comp in root:
		if comp.tag == "component":
			parse_component(diagram, comp, current_comp_order_num)
			current_comp_order_num += 1
		elif comp.tag == "action":
			new_action = ac.Action(source=comp.attrib["source"], target=comp.attrib["target"])
			diagram.add_action(new_action)
		
	print ([c.label for c in diagram.componentcontainer])
		
	return diagram
		
if __name__ == "__main__":
	diagram = parse_xml(filename_arch_specs_xml="example.xml")
	diagram.draw()
	diagram.write_texfile("example.tex")