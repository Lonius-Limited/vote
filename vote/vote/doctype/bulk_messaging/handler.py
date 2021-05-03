# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import enqueue
from frappe.core.doctype.sms_settings.sms_settings import send_sms
import vote

def handle_sms_cron():
    doclist = frappe.get_all("Bulk Messaging", filters=dict(sent=0,docstatus=1), fields=["name"])
    
    docs = [frappe.get_doc("Bulk Messaging", x.get("name")) for x in doclist]

    list(map(lambda x: x.send_messages(), docs))

    return