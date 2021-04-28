# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.user_permission.user_permission import clear_user_permissions
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import _
from vote.utils.election_details import stage_otp
from vote import sendmail

verification_confirmation_template ="""Dear Dr. {},\nYour request for change of details has been {}.\nYour Voter ID is {}\nThe voting_link is https://kmpdu.bizpok.com"""


class InstitutionMemberSandbox(Document):
	def before_submit(self):
		self.validate_institution_and_branch()
		self.move_to_master()
	def validate_institution_and_branch(self):
		if not self.institution:
			frappe.throw(f"Missing Institution")
		if not self.electoral_district:
			frappe.throw("Missing electoral district/branch")
		return
	def move_to_master(self):
		try:
			if self.create_a_new_record: frappe.throw("Not Implemented yet!")
			master_doc = frappe.get_doc("Institution Member", self.link_with_document)
			master_doc.set("cell_number",self.get("cell_number"))
			master_doc.set("email_address",self.get("email_address"))
   			master_doc.set("id_number",self.get("id_number"))
			master_doc.save(ignore_permissions=True)	
			# master_doc.db_set("board_number",self.board_number)		
			return master_doc.name
		except Exception as e:
			frappe.throw(f"{e}")
	def on_submit(self):

		master_doc = frappe.get_doc("Institution Member", self.link_with_document)

		surname = master_doc.get("surname")

		telephone, email = self.cell_number, self.email_address

		status = "Rejected" if self.get("rejected") else "Approved"

		sms_msg = verification_confirmation_template.format(surname, status, self.link_with_document)


		if telephone: send_sms([telephone], sms_msg)

		return

