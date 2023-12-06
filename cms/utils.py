from __future__ import unicode_literals
import frappe
import calendar
from frappe.model.document import Document
from frappe.utils import today,add_days, cint,cstr
from frappe.utils.background_jobs import enqueue
from frappe.utils.csvutils import read_csv_content

import json


@frappe.whitelist()
def clean_cms_log():
    cmslogs = frappe.get_all('CMS Log',['log','name'],{'created_dfe':0})
    for cmslog in cmslogs:
        actual_log = cmslog.log
        clean_log = actual_log.replace("'", "")
        cmslogid = frappe.get_doc('CMS Log',cmslog.name)
        cmslogid.clean_log = clean_log
        cmslogid.save(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()
def send_fca_test_email():
    date = add_days(today(),-1)
    fca = frappe.new_doc("Food Consumption Annexure")
    fca.from_date = date
    fca.to_date = date
    fca.save()

    """send email with payment link"""
    today_fca = frappe.get_value('Food Consumption Annexure',{ "from_date":date},['name'])
    email_args = {
        "recipients": ["abdulla.pi@groupteampro.com"],
        "subject": "Daily Food Usage",
        "message":"""<p>Dear Sir/Madam,</p>
            <h4>Info:</h4><p>Kindly find the attached document of Daily Usage for your reference
            </p><br> Regards <br>CanteenPRO Team""",
        "now": True,
        "attachments": [frappe.attach_print("Food Consumption Annexure", today_fca,
            file_name=today_fca, print_format="Food Consumption Annexure")]}
    enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)

@frappe.whitelist()
def send_fca_email():
    date = add_days(today(),-1)
    fca = frappe.new_doc("Food Consumption Annexure")
    fca.from_date = date
    fca.to_date = date
    fca.save()

    """send email with payment link"""
    today_fca = frappe.get_value('Food Consumption Annexure',{ "from_date":date},['name'])
    email_args = {
        "recipients": ["abdulla.pi@groupteampro.com","santhanakrishnan@foodexo.in","operationhead@foodexo.in","sundararaman@tnpetro.com",
        "admin@tnpetro.com","hr@groupteampro.com", "foodexooffice@gmail.com","accounts@foodexo.in","hr@tnpetro.com"],
        "subject": "Daily Food Usage",
        "message":"""<p>Dear Sir/Madam,</p>
            <h4>Info:</h4><p>Kindly find the attached document of Daily Usage for your reference
            </p><br> Regards <br>CanteenPRO Team""",
        "now": True,
        "attachments": [frappe.attach_print("Food Consumption Annexure", today_fca,
            file_name=today_fca, print_format="Food Consumption Annexure")]}
    enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)

@frappe.whitelist()
def create_dfe_from_cms_log_bulk():
    enqueue(method=enqueue_create_dfe_from_cms_log_bulk, queue='long', timeout=6000, is_async=True)


@frappe.whitelist()
def enqueue_create_dfe_from_cms_log_bulk():
    cms_logs = frappe.get_all("CMS Log",{'created_dfe':0},["name","clean_log"])
    for cms_log in cms_logs:
        if cms_log.clean_log:
            print(cms_log.name)
            payloads = json.loads(cms_log.clean_log)
            for payload in payloads:
                if payload:
                    food_order = frappe.new_doc("Food Order No")
                    food_order.employee = payload[0]["employee"]
                    food_order.date = payload[0]["date"]
                    food_order.save(ignore_permissions=True)
                    frappe.db.commit()
                    for py in payload:
                        for i in range(cint(py["qty"])):
                            limit = frappe.db.get_value('Food Item',py["item"],"limit") or 0
                            if frappe.db.count("Daily Food Entry",{"employee":py["employee"],"item":py["item"],"date":py["date"]}) > limit:
                                dfe = frappe.new_doc("Daily Food Entry")
                                dfe.employee = py["employee"]
                                dfe.item = py["item"]
                                dfe.date = py["date"]
                                dfe.time = py["time"]
                                dfe.food_order_no = food_order.name
                                dfe.cms_log = cms_log.name   
                                dfe.price = frappe.db.get_value("Food Item",py["item"],["original_rate"])
                                dfe.save(ignore_permissions=True)
                                frappe.db.commit()
                            else:
                                dfe = frappe.new_doc("Daily Food Entry")
                                dfe.employee = py["employee"]
                                dfe.item = py["item"]
                                dfe.date = py["date"]
                                dfe.time = py["time"]
                                dfe.food_order_no = food_order.name
                                dfe.cms_log = cms_log.name
                                dfe.price = frappe.db.get_value("Food Item",py["item"],["subsidy_rate"])
                                dfe.subsidy = 1
                                dfe.save(ignore_permissions=True)
                                frappe.db.commit()
            frappe.db.set_value("CMS Log",cms_log.name,'created_dfe',1)

@frappe.whitelist()
def create_dfe_from_cms_log(doc,method):
    if doc.clean_log:
        payloads = json.loads(doc.clean_log)
        for payload in payloads:
            if payload:
                food_order = frappe.new_doc("Food Order No")
                food_order.employee = payload[0]["employee"]
                food_order.date = payload[0]["date"]
                food_order.save(ignore_permissions=True)
                frappe.db.commit()
                for py in payload:
                    for i in range(cint(py["qty"])):
                        limit = frappe.db.get_value('Food Item',py["item"],"limit")
                        if frappe.db.count("Daily Food Entry",{"employee":py["employee"],"item":py["item"],"date":py["date"]}) > limit:
                            dfe = frappe.new_doc("Daily Food Entry")
                            dfe.employee = py["employee"]
                            dfe.item = py["item"]
                            dfe.date = py["date"]
                            dfe.time = py["time"]
                            dfe.food_order_no = food_order.name
                            dfe.cms_log = doc.name   
                            dfe.price = frappe.db.get_value("Food Item",py["item"],["original_rate"])
                            dfe.save(ignore_permissions=True)
                            frappe.db.commit()
                        else:
                            dfe = frappe.new_doc("Daily Food Entry")
                            dfe.employee = py["employee"]
                            dfe.item = py["item"]
                            dfe.date = py["date"]
                            dfe.time = py["time"]
                            dfe.food_order_no = food_order.name
                            dfe.cms_log = doc.name
                            dfe.price = frappe.db.get_value("Food Item",py["item"],["subsidy_rate"])
                            dfe.subsidy = 1
                            dfe.save(ignore_permissions=True)
                            frappe.db.commit()
        frappe.db.set_value("CMS Log",doc.name,'created_dfe',1)


    
def upload_def (filename):
    from frappe.utils.file_manager import get_file
 
    filepath = get_file(filename)

    pps = read_csv_content(filepath[1])
    for i in pps:
        print(i)
        for d in range(int(i[3])):
            dfe = frappe.new_doc('Daily Food Entry')
            dfe.date = i[0]
            dfe.item = i[1]
            dfe.price = i[2]
            dfe.plant = 'Heavy Chemicals Division'
            dfe.save(ignore_permissions=True)
            frappe.db.commit()

@frappe.whitelist()
def add_job_schedule():
    job = frappe.db.exists('Scheduled Job Type', 'send_fca_test_email')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method" : 'cms.utils.send_fca_test_email',
            "frequency" : 'Cron',
            "cron_format" : '0 3 * * *'
        })
        sjt.save(ignore_permissions=True)