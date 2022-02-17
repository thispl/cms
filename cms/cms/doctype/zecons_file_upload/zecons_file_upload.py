# -*- coding: utf-8 -*-
# Copyright (c) 2021, Teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content
from datetime import datetime
from datetime import timedelta, time,date

class ZeconsFileUpload(Document):
    pass

@frappe.whitelist()
def upload(file):
    from frappe.utils.file_manager import get_file
    filepath = get_file(file)
    pps = read_csv_content(filepath[1])
    date = ''
    err_list = ''
    for pp in pps:
        if pp[0] not in ('TamilNadu PetroProducts','Consumption Report for the','Slno',None,''):
            if pp[2] is not None:
                if not frappe.db.exists("Food Item",pp[2]):
                    err_list += '<ul>Item - <b>%s</b> Not Fount</ul><br>'%pp[2]
    if err_list:
        frappe.throw(err_list)
    else:
        for pp in pps:
            if pp[0] not in ('TamilNadu PetroProducts','Slno','',None):
                if pp[0] == "Consumption Report for the":
                    if pp[1]:
                        try:
                            date = datetime.strptime(pp[1],'%d/%m/%Y')
                        except:
                            date = datetime.strptime(pp[1],'%d-%m-%Y')
                if pp[2]:
                    if frappe.db.exists("Food Item",pp[2]):
                        zfe = frappe.new_doc("Zecons Food Entry")
                        zfe.date = date
                        zfe.code = pp[1]
                        zfe.item = pp[2]
                        zfe.rate = pp[3]
                        zfe.qty = pp[4]
                        zfe.cntr_value = pp[6]
                        zfe.save(ignore_permissions=True)
        return 'ok'