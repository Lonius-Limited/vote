# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

import frappe
import hashlib,json
from frappe.model.document import Document

class AgentBallotTally(Document):
	
	def before_save(self):
		doc_hash = self.make_hash()
		frappe.msgprint("Hashed document: "+doc_hash)
		# frappe.msgprint("Important: This document is only entered once after branch polls are tallied and verified.")
		self.set("document_hash", doc_hash)
		domains = self.member_applicable_domains(self.polling_station)
		frappe.msgprint(f"{domains}")
		candidates = self.make_candidates_dict(filtered_districts=domains)
		if self.applicable_voter_positions: return
		self.set('applicable_voter_positions', [])
		for candidate in candidates:
			row= self.append("applicable_voter_positions",{})
			row.candidate = candidate.candidate_id
			row.candidate_name = candidate.candidate_name
			row.branch = candidate.branch
			row.position = candidate.contested_position
			
		# self.set('applicable_voter_positions', candidates)
	def make_hash(self):
		chain_payload = dict(election=self.get("election"), polling_station=self.get("polling_station"))
		payload_hash = hashlib.sha256(
			(json.dumps(chain_payload, default=str)).encode("utf-8")
		).hexdigest()
		return payload_hash
	def make_candidates_dict(self, filtered_districts=[]):
		if not frappe.get_all("Candidates", filters=dict(election=self.get("election"), docstatus =1)): return []

		return [x for x in frappe.get_doc("Candidates",dict(election=self.election)).get("candidates") if x.get("branch") in filtered_districts]
	def member_applicable_domains(self,polling_station):
		domain = polling_station
		applicable_domains =[]
		proceed = True
		while proceed:
			if frappe.get_value("Electoral District", domain,"parent_electoral_district"):	
				applicable_domains.append(domain)
				domain = frappe.get_value("Electoral District",domain,'parent_electoral_district')
			else:
				applicable_domains.append(domain)
				proceed = False
		return applicable_domains
	
	def before_submit(self):
    	# self.validate_votes_entered()
		r_voters = self.registered_voters
		
				
		for choice in self.applicable_voter_positions:
			if choice.vote_count != choice.vote_count_verification: frappe.throw("Please validate the votes for <b>[{0} - Candidate {1}]</b>".format(choice.position, choice.candidate_name))
			
			if choice.vote_count > r_voters: frappe.throw("Votes cast for {0} exceed the total registered voters".format(choice.position, choice.candidate_name))
			args = dict(election=self.election, candidate=choice.get("candidate"))
			tally_document = frappe.get_all(
				"Vote Repository", filters=args, fields=["name"]
			)
			if not tally_document:
				insert_args = dict(
					doctype="Vote Repository",
					election=self.election,
					branch=choice.get("branch"),
					position=choice.get("position"),
					candidate=choice.get("candidate"),
					vote_count=choice.get("vote_count"),
					registered_voters=self.registered_voters
					# ballot=choice.get("parent"),
				)
				frappe.get_doc(insert_args).insert(ignore_permissions=True)
			else:
				frappe.msgprint("Results for <b>[{0} - Candidate {1}]</b> have already been entered and therefore skipped".format(choice.position, choice.candidate_name))
