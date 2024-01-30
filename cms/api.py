
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today, cint,cstr
import json
from datetime import datetime
from frappe.utils.background_jobs import enqueue
from frappe.utils.csvutils import read_csv_content

def run_method():
    payloads = [[{
        "employee": "301649",
        "date": "2021-5-2",
        "time": "10:00:00",
        "item": "BREAD JAM",
        "qty": "2"
    },{
        "employee": "301649",
        "date": "2021-05-02",
        "time": "11:00:00",
        "item": "CHICKEN",
        "qty": "3"
    }],
    [{
        "employee": "12345",
        "date": "2021-05-03",
        "time": "10:00:00",
        "item": "BREAD JAM",
        "qty": "1",
    },{
        "employee": "12345",
        "date": "2021-05-04",
        "time": "11:00:00",
        "item": "CHICKEN",
        "qty": "5"
    }]]
    make_food_entry(payloads)

@frappe.whitelist(allow_guest=True)
def make_food_entry(payloads):
    payloads = json.loads(payloads)
    # frappe.log_error(message=payloads,title="payloads")
    for payload in payloads:
        payload = json.loads(payload)
        if payload:
            food_order = frappe.new_doc("Food Order No")
            food_order.employee = payload[0]["employee"]
            food_order.date = payload[0]["date"]
            food_order.save(ignore_permissions=True)
            frappe.db.commit()
            for item in payload:
                for i in range(cint(item["qty"])):
                    limit = frappe.db.get_value('Food Item',item["item"],["limit"])
                    if frappe.db.count("Daily Food Entry",{"employee":item["employee"],"item":item["item"],"date":item["date"],'subsidy':1}) > limit:
                    # if frappe.db.exists("Daily Food Entry",{"employee":item["employee"],"item":item["item"],"date":item["date"]}):
                        dfe = frappe.new_doc("Daily Food Entry")
                        dfe.employee = item["employee"]
                        dfe.item = item["item"]
                        dfe.date = item["date"]
                        dfe.time = item["time"]
                        dfe.food_order_no = food_order.name
                        dfe.price = frappe.db.get_value("Food Item",item["item"],["original_rate"])
                        dfe.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        dfe = frappe.new_doc("Daily Food Entry")
                        dfe.employee = item["employee"]
                        dfe.item = item["item"]
                        dfe.date = item["date"]
                        dfe.time = item["time"]
                        dfe.food_order_no = food_order.name
                        dfe.price = frappe.db.get_value("Food Item",item["item"],["subsidy_rate"])
                        dfe.subsidy = 1
                        dfe.save(ignore_permissions=True)
                        frappe.db.commit()
    return 'OK'

@frappe.whitelist(allow_guest=True)
def enqueue_food_entry(payloads):
    dates = ["2021-6-16"]
    # dates = ['2021-6-13','2021-6-14','2021-6-15','2021-6-16','2021-6-17','2021-6-18','2021-6-19','2021-6-20','2021-6-21','2021-6-22']
    payloads = json.loads(payloads)
    for payload in payloads:
        payload = json.loads(payload)
        if payload:
            food_order = frappe.new_doc("Food Order No")
            food_order.employee = payload[0]["employee"]
            food_order.date = payload[0]["date"]
            food_order.save(ignore_permissions=True)
            frappe.db.commit()
            for item in payload:
                for i in range(cint(item["qty"])):
                    if item['date'] in dates:
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
                        else:
                            dfe = frappe.new_doc("Daily Food Entry")
                            dfe.employee = item["employee"]
                            dfe.item = item["item"]
                            dfe.date = item["date"]
                            dfe.time = item["time"]
                            dfe.food_order_no = food_order.name
                            dfe.price = frappe.db.get_value("Food Item",item["item"],["subsidy_rate"])
                            dfe.subsidy = 1
                            dfe.save(ignore_permissions=True)
                            frappe.db.commit()
    return 'NOK'

def enqueue_csv(filename):
    enqueue(bulk_update_from_csv, queue='default', timeout=6000, event='bulk_update_from_csv',filename=filename)

def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    payloads = read_csv_content(filepath[1])

    for payload in payloads:
        if payload:
            food_order = frappe.new_doc("Food Order No")
            food_order.employee = payload[0]
            food_order.date = payload[1]
            food_order.save(ignore_permissions=True)
            frappe.db.commit()
            for i in range(cint(payload[2])):
                limit = frappe.db.get_value('Food Item',payload[3],"limit")
                if frappe.db.count("Daily Food Entry",{"employee":payload[0],"item":payload[3],"date":payload[1]}) > limit:
                    dfe = frappe.new_doc("Daily Food Entry")
                    dfe.employee = payload[0]
                    dfe.item = payload[3]
                    dfe.date = payload[1]
                    # dfe.time = payload[4]
                    dfe.plant = payload[4]
                    dfe.food_order_no = food_order.name
                    dfe.price = frappe.db.get_value("Food Item",payload[3],["original_rate"])
                    dfe.save(ignore_permissions=True)
                    frappe.db.commit()
                else:
                    dfe = frappe.new_doc("Daily Food Entry")
                    dfe.employee = payload[0]
                    dfe.item = payload[3]
                    dfe.date = payload[1]
                    # dfe.time = payload[4]
                    dfe.plant = payload[4]
                    dfe.food_order_no = food_order.name
                    dfe.price = frappe.db.get_value("Food Item",payload[3],["subsidy_rate"])
                    dfe.subsidy = 1
                    dfe.save(ignore_permissions=True)
                    frappe.db.commit()
    return 'OK'


def remove_subsidy():
    # dfes = frappe.db.sql("""select name,item from `tabDaily Food Entry` where date between '2021-05-21' and '2021-06-28' """,as_dict=True)
    dfes = frappe.db.sql("""select name,item,employee,date from `tabDaily Food Entry` where date between '2021-08-01' and '2021-08-31' and subsidy = 1 """,as_dict=True)
    print(len(dfes))
    for dfe in dfes:
        og = frappe.db.get_value('Food Item',dfe.item,"original_rate")
        frappe.db.set_value('Daily Food Entry',dfe.name,"subsidy",0)
        frappe.db.set_value('Daily Food Entry',dfe.name,"price",og)
        print(dfe)


def mark_subsidy():
    # dfes = frappe.db.sql("""select name,item,employee,date from `tabDaily Food Entry` where date between '2021-05-21' and '2021-06-28' """,as_dict=True)
    dfes = frappe.db.sql("""select name,item,employee,date from `tabDaily Food Entry` where date between '2021-08-21' and '2021-09-20' """,as_dict=True)
    print(len(dfes))
    for dfe in dfes:
        limit = frappe.db.get_value('Food Item',dfe.item,"limit")
        c = frappe.db.count("Daily Food Entry",{"employee":dfe.employee,"item":dfe.item,"date":dfe.date,"subsidy":1})
        print(c)
        if frappe.db.count("Daily Food Entry",{"employee":dfe.employee,"item":dfe.item,"date":dfe.date,'subsidy':1}) < limit:
            sp = frappe.db.get_value('Food Item',dfe.item,"subsidy_rate")
            frappe.db.set_value('Daily Food Entry',dfe.name,"subsidy",1)
            frappe.db.set_value('Daily Food Entry',dfe.name,"price",sp)

# def delete_dfe():
#     dfes = frappe.db.sql("""select name,item,employee,date from `tabDaily Food Entry` where date between '2021-10-01' and '2021-10-01' and subsidy = 0 """,as_dict=True)
#     print(len(dfes))
#     for dfe in dfes:
#         frappe.delete_doc("Daily Food Entry",dfe.name)
#         print(dfe.name)

# def update_plant():
#     dfes = frappe.db.sql("""select name,item,employee,date from `tabDaily Food Entry` where date between '2021-09-21' and '2021-10-26' and plant is null """,as_dict=True)
#     print(len(dfes))
#     for dfe in dfes:
#         frappe.set_value("Daily Food Entry",dfe.name,'plant',frappe.db.get_value('Employee',dfe.employee,'plant'))
#         print(dfe.name)

@frappe.whitelist(allow_guest=True)
def enqueue_cms_log(payloads,deviceid):
    enqueue(make_cms_log, queue='default', timeout=9000, event='make_cms_log',payloads=payloads,deviceid=deviceid)
    return 'OK'
    
def make_cms_log(payloads,deviceid):
    payloads = json.loads(payloads)
    # frappe.log_error(message=[payloads,deviceid,frappe.utils.now_datetime()],title="payloads")
    cmslog = frappe.new_doc('CMS Log')
    cmslog.time = frappe.utils.now_datetime()
    cmslog.device = cstr(deviceid)
    cmslog.log = cstr(payloads)
    cmslog.save(ignore_permissions=True)
    # frappe.log_error(message=cmslog,title="payloads_test")
    frappe.db.commit()
    return 'OK'

# def enqueue_upload_csv(filename):
#     enqueue(upload_csv, queue='default', timeout=6000, event='upload_csv',filename=filename)

# def upload_csv(filename):
#     from frappe.utils.file_manager import get_file
#     _file = frappe.get_doc("File", {"file_name": filename})
#     filepath = get_file(filename)
#     payloads = read_csv_content(filepath[1])
#     for p in payloads:
#         print(p[0])
#         # if not frappe.db.exists('Daily Food',{'employee':pp[1],'item':[0],'date':pp[2],'time':pp[3]}):
#         limit = frappe.db.get_value('Food Item',p[0],["limit"])
#         if frappe.db.count("Daily Food Entry",{"employee":p[1],"item":p[0],"date":p[2],'subsidy':1}) < limit:
#             dfe = frappe.new_doc("Daily Food Entry")
#             dfe.employee = p[1]
#             dfe.item = p[0]
#             dfe.date = p[2]
#             dfe.price = frappe.db.get_value("Food Item",p[0],["original_rate"])
#             dfe.save(ignore_permissions=True)
#             frappe.db.commit()
#         else:
#             dfe = frappe.new_doc("Daily Food Entry")
#             dfe.employee = p[1]
#             dfe.item = p[0]
#             dfe.date = p[2]
#             dfe.price = frappe.db.get_value("Food Item",p[0],["subsidy_rate"])
#             dfe.subsidy = 1
#             dfe.save(ignore_permissions=True)
#             frappe.db.commit()

# def upload_csv(filename):
#     from frappe.utils.file_manager import get_file
#     _file = frappe.get_doc("File", {"file_name": filename})
#     filepath = get_file(filename)
#     payloads = read_csv_content(filepath[1])
#     print(len(payloads))
#     for p in payloads:
#         print(p[0])
#         limit = frappe.db.get_value('Food Item',p[3],["limit"])
#         if frappe.db.count("Daily Food Entry",{"employee":p[0],"item":p[3],"date":p[1],'subsidy':1}) < limit:
#             dfe = frappe.new_doc("Daily Food Entry")
#             dfe.employee = p[0]
#             dfe.date = p[1]
#             dfe.time = p[2]
#             dfe.item = p[3]
#             # dfe.plant = p[3]
#             dfe.price = frappe.db.get_value("Food Item",p[3],["original_rate"])
#             dfe.save(ignore_permissions=True)
#             frappe.db.commit()
#         else:
#             dfe = frappe.new_doc("Daily Food Entry")
#             dfe.employee = p[0]
#             dfe.item = p[3]
#             dfe.date = p[1]
#             # dfe.plant = p[3]
#             dfe.price = frappe.db.get_value("Food Item",p[0],["subsidy_rate"])
#             dfe.subsidy = 1
#             dfe.save(ignore_permissions=True)
#             frappe.db.commit()


def upload_from_json(filename):
    # payloads = [{"employee": "300752", "date": "2021-9-11", "qty": "1", "item": "LUNCH MEALS"}]
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_name": filename})
    filepath = get_file(filename)
    # payloads = read_csv_content(filepath[1])
    payloads = json.loads(filepath[1])
    for payload in payloads:
        payload = payload[0]
        if payload:
            food_order = frappe.new_doc("Food Order No")
            food_order.employee = payload["employee"]
            food_order.date = payload["date"]
            food_order.save(ignore_permissions=True)
            frappe.db.commit()
            for i in range(cint(payload['qty'])):
                print(payload['item'])
                limit = frappe.db.get_value('Food Item',payload['item'],"limit")
                if frappe.db.count("Daily Food Entry",{"employee":payload["employee"],"item":payload["item"],"date":payload["date"]}) > limit:
                    dfe = frappe.new_doc("Daily Food Entry")
                    dfe.employee = payload["employee"]
                    dfe.item = payload["item"]
                    dfe.date = payload["date"]
                    dfe.time = payload["time"]
                    dfe.food_order_no = food_order.name
                    dfe.price = frappe.db.get_value("Food Item",payload["item"],["original_rate"])
                    dfe.save(ignore_permissions=True)
                    frappe.db.commit()
                else:
                    dfe = frappe.new_doc("Daily Food Entry")
                    dfe.employee = payload['employee']
                    dfe.item = payload['item']
                    dfe.date = payload["date"]
                    dfe.time = payload["time"]
                    dfe.food_order_no = food_order.name
                    dfe.price = frappe.db.get_value("Food Item",payload["item"],["subsidy_rate"])
                    dfe.subsidy = 1
                    dfe.save(ignore_permissions=True)
                    frappe.db.commit()