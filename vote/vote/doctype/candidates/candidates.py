# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


@frappe.whitelist()
def retrieve_election_domains(election):
	position_args =dict(parent = election)
	advertised_positions = frappe.get_all("Candidate Position Settings", filters= position_args, fields = ["branch","position"])
	return advertised_positions
class Candidates(Document):
	def after_insert(self):
		pass
		#self.generate_positions(True)
	def before_save(self):
		self.validate_candidates()
		#self.generate_positions()
	def on_submit(self):
		frappe.get_doc("Election", self.get("election")).retrieve_candidates(True)
	def validate_candidates(self):
		all_candidates =[x.get("candidate_name") for x in self.get("candidates") if x.get("candidate_name")]
		def _check_duplicate(all_candidates):
			for i in range(len(all_candidates)):
				if all_candidates.index(all_candidates[i]) != i:
					candidate = all_candidates[i]
					idx = all_candidates.index(all_candidates[i])
					frappe.throw(f" Sorry, candidate: {candidate} entered severally in row {idx} and {i}")
		_check_duplicate(all_candidates)