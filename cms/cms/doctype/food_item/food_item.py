# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class FoodItem(Document):
	def before_save(self):
		selected_days = []
		self.selected_days = []
		if self.monday:
			selected_days.append('Monday')
		if self.tuesday:
			selected_days.append('Tuesday')
		if self.wednesday:
			selected_days.append('Wednesday')
		if self.thursday:
			selected_days.append('Thursday')
		if self.friday:
			selected_days.append('Friday')
		if self.saturday:
			selected_days.append('Saturday')
		if self.sunday:
			selected_days.append('Sunday')
			
		self.selected_days = cstr(selected_days)
