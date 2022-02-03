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
		dname = self.name
		#frappe.throw(f"{dname}")
		if self.candidate_link:
			pass
			# self.retrieve_candidates(False)	
		self.validate_candidates()
		self.generate_positions()
		
	def after_insert(self):
		self.make_candidature_document()
		if self.candidate_link:
			#self.retrieve_candidates(save_doc=True)	
			self.validate_candidates()
		self.generate_positions(True)
		self.set("status", "Scheduled")
	def before_submit(self):
		self.validate_candidates()
		self.status ='Scheduled'
		IMMATURE_VALIDATION="Cannot submit before verification/approval of the voter register and the candidates list"
		if not self.candidate_link:
			frappe.throw(IMMATURE_VALIDATION)
		if frappe.get_doc("Candidates", self.candidate_link).get("docstatus") != 1 or frappe.get_doc("Voter Register", self.applicable_voter_register).get("docstatus") != 1:
			frappe.throw(IMMATURE_VALIDATION)
	def on_submit(self):
		frappe.msgprint("Election setup and Voter IDs shipped successfully")
		
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
		return self
	def retrieve_candidates(self, save_doc = True):
		self.set('candidates',[])
		candidate_doc = frappe.get_doc("Candidates",{"election": self.name}) or frappe.get_doc("Candidates", self.get("candidate_link"))
		if not candidate_doc: return
		existing_members =[x.get("candidate_id") for x in self.get("candidates")]
		self.db_set('candidate_link', candidate_doc.name)
		for d in candidate_doc.get("candidates"):
			row = self.append("candidates",{})
			if d.candidate_id not in existing_members:
				row.branch = d.branch
				row.candidate_id = d.candidate_id
				row.candidate_name = d.candidate_name
				row.contested_position = d.contested_position
				row.current_position = d.current_position
		# frappe.msgprint(save_doc)
		if save_doc is not False: self.save(ignore_permissions=True)
		self.notify_update()
	def generate_positions(self,save_doc=False):
		existing_positions =[x.get("position") for x in self.candidate_position_settings]
		if existing_positions: return
		for post in frappe.get_all("Institution Position", filters ={"institution":self.institution, "is_elective":1}):
			if existing_positions.count(post.name) > 0 : continue  
			row = self.append("candidate_position_settings",{})
			row.position = post.name
			row.maximum_number_of_positions = 1
		if save_doc: doc.save(ignore_permissions = True)	
	def persist_voter_stats_per_district(self):
		doc = frappe.get_doc("Voter Register",self.get("applicable_voter_register"))
		doc.persist_voter_stats()

  