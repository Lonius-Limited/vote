# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
ILLEGAL_LOGIN = "Sorry, the Voter id or Member ID provided do not match our records"
WRONG_OTP ="Sorry, the OTP code yousenthas either been used or is invalid"
OTP_STAGED = "OTP message has been staged, click Retry if you need to resend the OTP"
@frappe.whitelist(allow_guest=True)
def authenticate_voter(voter_id, member_id):
	member = frappe.get_doc("Institution", voter_id)
	if member_id != member.institution_id: frappe.throw(ILLEGAL_LOGIN)
	_stage_otp(voter_id)
	return frappe.local.response.update({'message': 'OTP Has been Staged', 'status':'success', 'alert': str(OTP_STAGED)})
def _stage_otp(voter_id = ''):
	otp_code = str(frappe.generate_hash(length=8)).upper()
	args = dict(
		doctype = "OTP Record",
		voter= voter_id,
		key= otp_code,
		valid = 1
	)
	frappe.get_doc(args).insert(ignore_permissions=True)
	return otp_code
def authenticate_otp(voter_id, key, resend_otp=0):
	args = dict(voter = voter_id, key=key, valid = 1)
	resend_args = dict(valid=1, voter=voter_id)
	if resend_otp:	
		frappe.get_doc("OTP Record", resend_args).send_otp()
		return
	if not frappe.db.get_value("OTP Record", args): 
		return frappe.local.response.update({'message': 'Failed to authenticate OTP', 'status':'error', 'error': str(WRONG_OTP)})
	#Set OTP as Invalid and proceed
	otp_record = frappe.get_doc("OTP Record", args)
	otp_record.invalidate()
	valid_elections_for_voter = get_voter_elections(voter_id= voter_id)

	if not valid_elections_for_voter: return {}

	ballot = get_e_ballot(election= valid_elections_for_voter[0].name, voter=voter_id)
	return ballot
@frappe.whitelist(allow_guest=True)
def get_voter_elections(voter_id, status=None):
	election_status = ['Open'] if status==None else ['Closed', 'Scheduled']
	voter_registers = frappe.db.sql(f"SELECT DISTINCT parent  FROM `tabVoter Register Member` WHERE system_id = '{voter_id}' AND parent IN (SELECT applicable_voter_register FROM `tabElection` WHERE docstatus = 1)", as_dict=1)
	voter_register_list =[x.get("parent") for x in voter_registers]
	elections = frappe.db.get_all("Election", filters={"applicable_voter_register":["IN",voter_register_list], "docstatus":1, "status":["IN",election_status]},fields=["name","election_start","election_ends","status"])
	return elections
	#returns list []
	# Election ID , Status[Scheduled,Open, Closed] , Action [Vote Now, View Results], Election Date
def get_has_voted(election, voter):
	return frappe.db.exists({"doctype":"Ballot Entry","voter_id": voter,"election":election})
@frappe.whitelist(allow_guest=True)
def get_e_ballot(election, voter = None):
	if not voter: return {}
	has_voted = 'Yes' if get_has_voted(voter, election) else 'No'
	payload = {"has_voted": has_voted} #Initialize payload with voting status
	payload["_ps_note"] = "will not populate ballot if above answer is yes"
	if has_voted =='Yes': return payload
	election_doc = frappe.get_doc("Election",election)
	applicable_domains_for_voter = [x.get("electoral_district") for x in frappe.get_doc("Institution Member", voter).get("applicable_voter_districts")]
	def _positions_for_domain(position):
		return position.branch in applicable_domains_for_voter
	positions = filter(_positions_for_domain , election_doc.get("candidate_position_settings"))
	ballot_list =[]
	for position in positions:
		p_obj ={}
		position, branch, max_posts = position.get("position"),position.get("branch"), position.get("maximum_number_of_positions")
		p_obj["position"] = position
		p_obj["branch"] = branch
		p_obj["maximum_number_of_positions"] = max_posts
		p_obj["candidates"] = get_candidates_per_position(election, position, branch)
		ballot_list.append(p_obj)
	payload["ballot"] = ballot_list
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
	'''posts a ballot to a Ballot Entry Doctype'''
	ballot = json.loads(ballot)
	voter, election, institution = ballot.voter, ballot.election,\
		 get_voter_institution(ballot.voter)
	ballot_document = frappe.get_doc({"doctype":"Ballot Entry",\
		"institution":institution,"voter_id": voter,"election":election})
	for post in ballot:
		row = ballot_document.append("ballot_entry_detail",{})
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
	return ballot
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
@frappe.whitelist(allow_guest=True)
def ping():
	return 'Zahari says: pong'

