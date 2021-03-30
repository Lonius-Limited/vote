# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
ILLEGAL_LOGIN = "Sorry, the Voter id or Member ID provided do not match our records"
def authenticate_voter(voter_id, member_id):
	member = frappe.get_doc("Institution", voter_id)
	if member_id != member.institution_id: frappe.throw(ILLEGAL_LOGIN)
	send_otp(member)
def send_otp(member):
	def _stage_otp(member_id,phone,):
		pass
		# frappe.get_doc({"doctype":"OTP","member_id":"","phone":,"otp_code":""}).insert(ignore_permissions=True)
def authenticate_otp(otp):
	pass
def get_voter_elections(voter_id):
	voter_registers = frappe.db.sql(f"SELECT DISTINCT parent  FROM `tabVoter Register Member` WHERE system_id = '{voter_id}' AND parent IN (SELECT applicable_voter_register FROM `tabElection` WHERE docstatus = 1)", as_dict=1)
	voter_register_list =[x.get("parent") for x in voter_registers]
	elections = frappe.db.get_all("Election", filters={"applicable_voter_register":["IN",voter_register_list], "docstatus":1},fields=["name","election_start","election_ends","status"])
	#returns list []
	# Election ID , Status[Scheduled,Open, Closed] , Action [Vote Now, View Results], Election Date
def get_has_voted(election, voter):
	return frappe.db.exists({"doctype":"Ballot Entry","voter_id": voter,"election":election})
def get_e_ballot(election, voter = None):
	if not voter: return []
	has_voted = True if get_has_voted(voter, election) else False
	payload =[{"has_voted": has_voted}]
	if has_voted: return payload
	election_doc = frappe.get_doc("Election",election)
	applicable_domains_for_voter = [x.get("electoral_district") for x in frappe.get_doc("Institution Member", voter).get("applicable_voter_districts")]
	def _positions_for_domain(position):
		return position.branch in applicable_domains_for_voter
	positions = filter(_positions_for_domain , election_doc.get("candidate_position_settings"))
	for position in positions:
		p_obj ={}
		position, branch, max_posts = position.get("position"),position.get("branch"), position.get("maximum_number_of_positions")
		p_obj["position"] = position
		p_obj["branch"] = branch
		p_obj["maximum_number_of_positions"] = max_posts
		p_obj["candidates"] = get_candidates_per_position(election, position, branch)
		payload.append(p_obj)
	return payload
	# returns list e.g [{"position":"President" ,"max_posts":1, "enforce_max":[0,1],
	#  candidates:[{"candidate_1":[0,1]}{"candidate_2":[0,1]}]}]
def get_candidates_per_position(election, position=None, branch = None):
	args ={
			"parent":election,
			"branch": branch,
			"contested_position":position
		}
	return frappe.db.get_all("Election Candidate",filters=frappe._dict(args),fields=['candidate_id','candidate_name','political_party','party_symbol','headshot'])#..Party, Symbol, Image,
def post_e_ballot(ballot): # Must include voter, election
	ballot = json.loads(ballot)
	voter, election, institution = ballot.voter, ballot.election,\
		 get_voter_institution(ballot.voter)
	ballot_document = frappe.get_doc({"doctype":"Ballot Entry",\
		"institution":institution,"voter_id": voter,"election":election})
	for post in ballot:
		row = self.append("ballot_entry_detail",{})
		position = post.position
		branch = post.branch
		row.position = position
		for candidate in post.candidates:
			row.branch = branch
			row.candidate_id = candidate.candidate_id
			row.candidate_name = candidate.candidate_name
			row.choice = candidate.choice
			row.political_party = candidate.political_party
	ballot_document.insert(ignore_permissions=True)
	#Get  voter, current_branch
	# [{"position":"President" ,"max_posts":1, "enforce_max":[0,1],
	#  candidates:[{"candidate_1":[0,1]}{"candidate_2":[0,1]}]}]
	'''posts a ballot to a Ballot Entry Doctype'''
def get_voter_institution(voter):
	return frappe.db.get_value("Institution Member", voter, "institution")
def get_votes_cast(election, branch = None):
	pass
	#All/branch votes cast in an election
def get_available_e_ballots(election, branch = None):
	pass
	#All/branch Voters in the register
def get_percentage_votes(election, branch = None):
	#Percentage of votes cast based on available e-ballots
	pass
def get_maximum_posts_per_position(election, position, branch = None):
	# Return integer
	pass


