# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals 
import frappe
from frappe.model.document import Document
#from frappe.utils import _
class Election(Document):
	def before_save(self):
		voter_register = frappe.get_doc("Voter Register",self.applicable_voter_register)
		voter_count = len(voter_register.get("active_members")) or 0
		self.set("eballots", voter_count)
		#if not self.candidate_link:
		
		self.make_candidature_document()
		if self.candidate_link:
			self.retrieve_candidates()	
		self.validate_candidates()
	def on_submit(self):
		self.validate_candidates()
	def validate_candidates(self):
		officials = [x.get("member") for x in self.get("election_officials")]
		for d in self.get("candidates"):
			if d.candidate_id in officials:
				candidate = d.candidate_name
				frappe.throw(f"""Sorry, candidate {candidate}\
					 cannot be an election official at the same time""")
	def make_candidature_document(self):
		if not frappe.get_value("Candidates",{"election":self.name}, "name"):
			d =frappe.get_doc({
				"doctype":"Candidates",
				"institution": self.institution,
				"election":self.name
			})
			d.flags.ignore_user_permissions = True
			d.insert()
			self.set("candidate_link",d.name)
			dname = d.name
			frappe.msgprint(f"Success! A candidature document {dname} has been created.")
	def retrieve_candidates(self):
		candidate_doc = frappe.get_doc("Candidates", self.get("candidate_link"))	
		existing_members =[x.get("candidate_id") for x in self.get("candidates")]
		
		for d in candidate_doc.get("candidates"):
			if d.candidate_id not in existing_members:
				self.append("candidates",{
					"candidate_id": d.candidate_id,
					"candidate_name": d.candidate_name,
					"current_position": d.current_position
				})
