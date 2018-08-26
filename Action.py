#!usr/bin/python3
# -*- coding: utf-8 -*-import string

class Action:
	def __init__(self, source, target, time=0):
		self.source = source
		self.target = target
		self.time = time