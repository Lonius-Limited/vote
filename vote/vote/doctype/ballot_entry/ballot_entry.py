# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import _

class BallotEntry(Document):
	def get_ballot_receipt_message(self, tx_id=''):

		doc_hash = tx_id

		doc_id = self.get("name")

		time_of_voting = self.creation

		return f"You Voted!\nYour ballot was posted under ID: {doc_id} and blockchain hash {doc_hash}.\nTime of voting {time_of_voting}"
	
	def send_ballot_receipt(self, tx_id =None):

		voter_id = self.get("voter_id")

		doc = frappe.get_doc("Institution Member", voter_id)

		telephone, email = doc.get("cell_number"), doc.get("email_address")
	
		message =  self.get_ballot_receipt_message(tx_id)


		if telephone: send_sms([telephone], message)

		email_args =dict(
			recipients = [email],
		    message = _(message),
			subject = _("Vote Receipt")
		)
		if email: enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)

		self.save(ignore_permissions=True)

		return
