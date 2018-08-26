#!usr/bin/python3
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET

import Diagram as dia
import ComponentContainer as coco
import ClassContainer as clco
import Method as me
import Action as ac
import globals


def create_from_xml(filename):
	diagram = dia.Diagram()

	tree = ET.parse(filename)
	root = tree.getroot()
	current_component_name = ""
	for comp in root.iter('component'):
		new_component = coco.ComponentContainer(label=comp.attrib["label"], order_number=int(comp.attrib["order_number"]), colorstring=comp.attrib["colorstring"])
		diagram.add_component(new_component)
		current_component_name = new_component.label
		
		current_class_name = ""
		for clas in comp.iter('class'):
			new_class = clco.ClassContainer(label=clas.attrib["label"], order_number=int(clas.attrib["order_number"]))
			diagram.add_class(new_class, current_component_name)
			current_class_name = new_class.label
			
			for meth in clas.iter('method'):
				new_method = me.Method(label=meth.attrib["label"], order_number=int(meth.attrib["order_number"]))
				diagram.add_method(new_method, current_class_name)
			
	for action in root.iter('action'):
		new_action = ac.Action(source=action.attrib["source"], target=action.attrib["target"])
		diagram.add_action(new_action)

	diagram.draw()
	diagram.write_texfile()
		
if __name__ == "__main__":
	create_from_xml("test.xml")