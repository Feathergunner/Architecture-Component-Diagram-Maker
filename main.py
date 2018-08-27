#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET

import Diagram as dia
import ComponentContainer as coco
import ClassContainer as clco
import Method as me
import Action as ac
import globals

def create_from_xml(filename_arch_specs_xml, filenameoutput_tex):
	#print("create_from_xml")
	diagram = dia.Diagram()

	tree = ET.parse(filename_arch_specs_xml)
	root = tree.getroot()
	#current_component_name = ""
	current_comp_order_num = 0
	for comp in root.iter('component'):
		#print("next component: "+comp.attrib["label"])
		if "order_number" in comp.attrib:
			current_comp_order_num = int(comp.attrib["order_number"])
		else:
			current_comp_order_num += 1
		new_component = coco.ComponentContainer(
			label=comp.attrib["label"],
			order_number=current_comp_order_num,
			colorstring=comp.attrib["colorstring"])
		current_comp_id = diagram.add_component(new_component)
		#print ("current component id: "+str(current_comp_id))
		
		#current_class_name = ""
		current_class_id = 0
		current_class_order_num = 0
		for clas in comp.iter('class'):
			#print("next class: "+clas.attrib["label"])
			if "order_number" in clas.attrib:
				current_class_order_num = int(clas.attrib["order_number"])
			else:
				current_comp_order_num += 1
			new_class = clco.ClassContainer(
				label=clas.attrib["label"],
				order_number=current_class_order_num)
			current_class_id = diagram.add_class(new_class, current_comp_id)
			#print ("current class id: "+str(current_class_id))
			
			current_method_order_num = 0
			for meth in clas.iter('method'):
				if "order_number" in meth.attrib:
					current_method_order_num = int(meth.attrib["order_number"])
				else:
					current_comp_order_num += 1
				if "id" in meth.attrib:
					current_method_id = meth.attrib["id"]
				else:
					current_method_id = "noid"
				new_method = me.Method(
					label=meth.attrib["label"],
					order_number=current_method_order_num,
					method_id=current_method_id)
				diagram.add_method(new_method, current_class_id)
			
	for action in root.iter('action'):
		new_action = ac.Action(source=action.attrib["source"], target=action.attrib["target"])
		diagram.add_action(new_action)

	diagram.draw()
	diagram.write_texfile(filenameoutput_tex)
		
if __name__ == "__main__":
	create_from_xml("test.xml")