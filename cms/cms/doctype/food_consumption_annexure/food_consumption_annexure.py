# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import add_days,date_diff
from frappe.model.document import Document

class FoodConsumptionAnnexure(Document):
    def get_consumption(self):
        pass

@frappe.whitelist()
def get_consumption_data(doc):
    # date = doc.from_date
    # date = "2021-05-01"
    no_of_days = date_diff(add_days(doc.to_date, 1), doc.from_date)
    dates = [add_days(doc.from_date, i) for i in range(0, no_of_days)]
    data_list = []
    for dt in dates:
        if doc.plant == 'All':
            d = frappe.db.sql("""select `tabDaily Food Entry`.item,`tabDaily Food Entry`.date,count(*) as qty,`tabFood Item`.original_rate  ,count(*) * `tabFood Item`.original_rate as price from `tabDaily Food Entry` 
            left join `tabFood Item` on `tabDaily Food Entry`.item = `tabFood Item`.name
            where date = '%s' group by item"""%(dt),as_dict=True)
        elif doc.plant == 'LAB & PO':
            d = frappe.db.sql("""select `tabDaily Food Entry`.item,`tabDaily Food Entry`.date,count(*) as qty,`tabFood Item`.original_rate  ,count(*) * `tabFood Item`.original_rate as price from `tabDaily Food Entry` 
            left join `tabFood Item` on `tabDaily Food Entry`.item = `tabFood Item`.name
            where date = '%s' and `tabDaily Food Entry`.plant in ('Propylene Oxide Division','Linear Alkyl Benzene') group by item"""%(dt),as_dict=True)
        elif doc.plant == 'HCD':
            d = frappe.db.sql("""select `tabDaily Food Entry`.item,`tabDaily Food Entry`.date,count(*) as qty,`tabFood Item`.original_rate  ,count(*) * `tabFood Item`.original_rate as price from `tabDaily Food Entry` 
            left join `tabFood Item` on `tabDaily Food Entry`.item = `tabFood Item`.name
            where date = '%s' and `tabDaily Food Entry`.plant = 'Heavy Chemicals Division' group by item"""%(dt),as_dict=True)
        total = 0
        for t in d:
            total += t.price
        d.append({"date":dt,"total":total})
        data_list.append(d)
        date = add_days(dt,1)
    print(data_list)
    return data_list