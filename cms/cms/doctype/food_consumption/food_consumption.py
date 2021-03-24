# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today

class FoodConsumption(Document):
	pass

@frappe.whitelist()
def get_food_consumption(employee,month):
	if month == "Jan":
		mon = 1
	elif month == "Feb":
		mon = 2
	elif month == "Mar":
		mon = 3
	elif month == "Apr":
		mon = 4
	elif month == "May":
		mon = 5
	elif month == "Jun":
		mon = 6
	elif month == "July":
		mon = 7
	elif month == "Aug":
		mon = 8
	elif month == "Sep":
		mon = 9
	elif month == "Oct":
		mon = 10
	elif month == "Nov":
		mon = 11
	else:
		mon = 12
	
	consumption = frappe.db.sql("""select item,count(*) as qty,sum(price) as amount from `tabDaily Food Entry` where month(date) = %s group by item""",mon,as_dict=True)
	subsidy = frappe.db.get_value("Employee",employee,["subsidy_amount"])
	subsidy_utilized = frappe.db.sql("select sum(price) as amount from `tabDaily Food Entry` where month(date) = %s and subsidy = 1 ",mon,as_dict=True)
	bill_without_subsidy = frappe.db.sql("select sum(price) as amount from `tabDaily Food Entry` where month(date) = %s and subsidy = 0 ",mon,as_dict=True)
	subsidy_balance = 0
	total_bill = 0
	if subsidy_balance or subsidy_utilized[0].amount:
		subsidy_balance = subsidy - subsidy_utilized[0].amount
	if subsidy_utilized[0].amount or bill_without_subsidy[0].amount:
		total_bill = subsidy_utilized[0].amount + bill_without_subsidy[0].amount
	return consumption,subsidy_balance,total_bill