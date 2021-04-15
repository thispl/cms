# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
import json
from datetime import datetime
from frappe.utils import getdate, nowdate, add_days, add_months, flt, get_first_day, get_last_day

class FoodMenu(Document):
	def get_food_items(self):
		items = frappe.db.sql("""select item,item_image from `tabFood Item` where %s between from_time and to_time""",(datetime.now().time()),as_dict=True)
		return items



@frappe.whitelist()
def calculate_amount(item,employee,food_child):
	month_start_date = get_first_day(nowdate())
	month_end_date = get_last_day(nowdate())
	subsidy = frappe.db.get_value("Employee",employee,["subsidy_amount"])
	subsidy_utilized = frappe.db.sql("select sum(price) as amount from `tabDaily Food Entry` where employee = %s and date between %s and %s and subsidy = 1 ",(employee,month_start_date,month_end_date),as_dict=True)
	try:
		subsidy_balance = subsidy - subsidy_utilized[0].amount
	except:
		subsidy_balance = subsidy
	if subsidy >= subsidy_balance:
		items = json.loads(food_child)
		existing_items = []
		for i in items:
			existing_items.append(i["food_item"])
		if frappe.db.exists("Daily Food Entry",{"employee":employee,"item":item,"date":today()}):
			return frappe.db.get_value("Food Item",item,["item","original_rate"]),0
		else:
			if items:
				if item not in existing_items:
					return frappe.db.get_value("Food Item",item,["item","subsidy_rate"]),1
				else:
					return frappe.db.get_value("Food Item",item,["item","original_rate"]),0
			else:
				return frappe.db.get_value("Food Item",item,["item","subsidy_rate"]),1
	else:
		return frappe.db.get_value("Food Item",item,["item","original_rate"]),0

@frappe.whitelist()
def daily_food_entry(food_child,employee):
	food_order = frappe.new_doc("Food Order No")
	food_order.employee = employee
	food_order.date = today()
	food_order.save(ignore_permissions=True)
	frappe.errprint(food_order)
	items = json.loads(food_child)
	for i in items:
		frappe.errprint(i)
		doc = frappe.new_doc("Daily Food Entry")
		doc.item = i["food_item"]
		doc.employee = employee
		doc.food_order_no = food_order.name
		doc.price = i["price"]
		doc.subsidy = i["subsidy"]
		doc.date = today()
		doc.save(ignore_permissions=True)
	return items