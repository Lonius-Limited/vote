# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VoterRegister(Document):
	def before_save(self):
		self.populate_active_members()
	def populate_active_members(self):
		if not self.institution:
			frappe.throw("Please select the institution")
			return
		institution = self.institution
		existing_members =[x.get("system_id") for x in self.get("active_members")]
		members = frappe.db.sql(f"""SELECT * FROM `tabInstitution Member`\
			WHERE institution ='{institution}' and member_status = 'Active'""",as_dict=True)
		for d in members:
			if d.name not in existing_members:
				self.append("active_members",{
					"member_id": d.member_id,
					"system_id": d.name,
					"member_name": d.full_name,
					"position": d.current_position
				})
	def onsubmit():
		self.alert_voters()
	def sync_