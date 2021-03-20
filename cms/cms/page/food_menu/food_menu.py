import frappe
from frappe import _

@frappe.whitelist()
def add_bill_amount(item):
    r = frappe.db.get_value("Food Item",item,["name","subsidy_rate","original_rate","limit"])
    return r