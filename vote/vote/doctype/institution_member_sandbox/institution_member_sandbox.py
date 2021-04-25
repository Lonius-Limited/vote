# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

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
			master_doc.set("member_id",self.member_id)
			master_doc.set("id_number",self.id_number)
			master_doc.set("board_number",self.board_number)
			master_doc.set("electoral_district",self.electoral_district)
			master_doc.set("surname",self.surname)
			master_doc.set("other_names",self.other_names)
			master_doc.set("cell_number",self.cell_number)
			master_doc.set("email_address",self.email_address)
			master_doc.save(ignore_permissions=True)			
			return master_doc.name
		except Exception as e:
			frappe.throw(f"{e}")

