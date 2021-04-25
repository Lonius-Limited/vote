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
			args = None
			args = frappe.get_all("Institution Member Sandbox",filters=dict(name=self.name),fields=["*"])[0]
			args.doctype = "Institution Member"
			args.pop("electoral_district_text")
			master_doc = frappe.new_doc(args).insert(ignore_permissions=True) 
			return master_doc.name
		except Exception as e:
			frappe.throw(f"{e}")
