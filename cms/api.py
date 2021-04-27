
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
import json
from datetime import datetime

def run_method():
    payload = [{
        "employee": "301649",
        "date": "2021-04-23",
        "time": "10:00:00",
        "item": "BREAD JAM" 
    },{
        "employee": "301649",
        "date": "2021-04-23",
        "time": "11:00:00",
        "item": "CHICKEN"
    }]
    make_food_entry(payload)

@frappe.whitelist(allow_guest=True)
def make_food_entry(payload):
    payload = json.loads(payload)
    food_order = frappe.new_doc("Food Order No")
    food_order.employee = payload[0]["employee"]
    food_order.date = payload[0]["date"]
    food_order.save(ignore_permissions=True)
    frappe.db.commit()
    for item in payload:
        if frappe.db.exists("Daily Food Entry",{"employee":item["employee"],"item":item["item"],"date":item["date"]}):
            dfe = frappe.new_doc("Daily Food Entry")
            dfe.employee = item["employee"]
            dfe.item = item["item"]
            dfe.date = item["date"]
            dfe.time = item["time"]
            dfe.food_order_no = food_order.name
            dfe.price = frappe.db.get_value("Food Item",item["item"],["original_rate"])
            dfe.save(ignore_permissions=True)
            frappe.db.commit()
            return 'OK'
        else:
            dfe = frappe.new_doc("Daily Food Entry")
            dfe.employee = item["employee"]
            dfe.item = item["item"]
            dfe.date = item["date"]
            dfe.time = item["time"]
            doc.food_order_no = food_order.name
            dfe.price = frappe.db.get_value("Food Item",item["item"],["subsidy_rate"])
            dfe.save(ignore_permissions=True)
            frappe.db.commit()
            return 'OK'