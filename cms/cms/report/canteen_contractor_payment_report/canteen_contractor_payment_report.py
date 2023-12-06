# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		_("Description") + ":Data:200", _("Rate/Qty") + ":Currency:200", _("Quantity")+ ":Data:200",
		_("Cntr.Value") + ":Currency:200"
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select `tabDaily Food Entry`.item,`tabFood Item`.original_rate,count(*),`tabFood Item`.original_rate * count(*)
	from `tabDaily Food Entry` left join `tabFood Item` on `tabDaily Food Entry`.item = `tabFood Item`.name 
	where %s group by `tabDaily Food Entry`.item""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	conditions += " date between '%s' and '%s' " % (filters.from_date,filters.to_date)
	if filters.plant == 'HCD':
		conditions += " and plant = 'Heavy Chemicals Division' "
	elif filters.plant == 'All':
		conditions += ''
	else:
		conditions += " and plant != 'Heavy Chemicals Division' "
	return conditions