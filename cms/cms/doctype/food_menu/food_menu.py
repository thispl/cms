# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
import json

class FoodMenu(Document):
	pass


@frappe.whitelist()
def calculate_amount(item,employee,food_child):
	items = json.loads(food_child)
	existing_items = []
	for i in items:
		existing_items.append(i["food_item"])
	if frappe.db.exists("Daily Food Entry",{"employee":employee,"item":item,"date":today()}):
		return frappe.db.get_value("Food Item",item,["item","original_rate"])
	else:
		if items:
			if item not in existing_items:
				frappe.errprint(existing_items)
				return frappe.db.get_value("Food Item",item,["item","subsidy_rate"])
			else:
				return frappe.db.get_value("Food Item",item,["item","original_rate"])
		else:
			return frappe.db.get_value("Food Item",item,["item","subsidy_rate"])

@frappe.whitelist()
def daily_food_entry(food_child,employee):
	items = json.loads(food_child)
	for i in items:
		# frappe.errprint(i)
		doc = frappe.new_doc("Daily Food Entry")
		doc.item = i["food_item"]
		doc.employee = employee
		doc.price = i["price"]
		doc.date = today()
		doc.save(ignore_permissions=True)
	return items