# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today

class DailyFoodConsumption(Document):
	pass

@frappe.whitelist()
def get_food_consumption(employee,date):
	consumption = frappe.db.sql("""select item,count(*) as qty,sum(price) as amount from `tabDaily Food Entry` where employee = %s and date = %s group by item""",(employee,date),as_dict=True)
	subsidy = frappe.db.get_value("Employee",employee,["subsidy_amount"])
	subsidy_utilized = frappe.db.sql("select sum(price) as amount from `tabDaily Food Entry` where employee = %s and date = %s and subsidy = 1 ",(employee,date),as_dict=True)
	bill_without_subsidy = frappe.db.sql("select sum(price) as amount from `tabDaily Food Entry` where employee = %s and date = %s and subsidy = 0 ",(employee,date),as_dict=True)
	subsidy_balance = 0
	total_bill = 0
	frappe.errprint(bill_without_subsidy)
	if subsidy > 0:
		if subsidy_utilized[0].amount:
			subsidy_balance = subsidy - subsidy_utilized[0].amount
			if bill_without_subsidy[0].amount:
				total_bill = subsidy_utilized[0].amount + bill_without_subsidy[0].amount
		return consumption,subsidy_balance,total_bill
	else:
		consumption = 0
		return consumption,subsidy_balance,total_bill