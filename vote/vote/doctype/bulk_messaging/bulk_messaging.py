# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import enqueue
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from vote import sendmail



class BulkMessaging(Document):
	def submit(self):
		self.queue_action('submit')
		frappe.msgprint("Transaction has begun in the background")
	def on_submit(self):
		sms_context = frappe.get_all("Institution Member", filters=dict(cell_number=["!=", ""]), fields=["surname","other_names","cell_number","name","email_address"])
		subject = self.get("subject")
		for j in sms_context:
			template = None
			template = self.get("message")
			first_name = j.get("surname")
			last_name = j.get("other_names")
			voter_id = j.get("name")
			telephone = str(j.get("cell_number")).replace("+","")
			email =j.get("email_address").replace("+","")
			msg = eval(f"""f'''{template}'''""")
			send_sms([telephone], msg)
			sendmail(recipients=[email], message=msg, subject = subject)
		return