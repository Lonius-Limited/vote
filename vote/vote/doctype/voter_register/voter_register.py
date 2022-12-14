# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from vote.utils.election_details import get_branch_eligible_voters
class VoterRegister(Document):
	def before_save(self):
		self.populate_active_members()
	@frappe.whitelist()
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
	def on_submit(self):
		self.persist_voter_stats()
	def persist_voter_stats(self):
		# distinct_branches = list(dict.fromkeys([x.get("branch") for x in self.get("active_members")]))
		all_branches = sorted([x.get("name") for x in frappe.get_all("Electoral District", filters=dict(institution=self.institution),fields=["name"])])
		sum_total = 0
		for j in all_branches:
			voters = len(get_branch_eligible_voters(linked_voter_register=self.name, branch=j))
			doc = frappe.get_doc("Electoral District", j)
			doc.db_set("registered_voters", voters)
			doc.db_set("active_register",self.name)
		return
   
		
		