# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from vote.utils.ethereum import log_casted_vote, privKey, pubKey, get_votes_cast_bc, create_wallet
from vote.vote.report.election_tally.election_tally import get_results
from vote.img_utils import get_headshot,get_party_symbol
from vote.vote.report.election_tally.election_tally import get_branch_voters
ILLEGAL_LOGIN = "Sorry, the Voter id or Member ID provided do not match our records"
WRONG_OTP ="Sorry, the OTP code has either been used or is invalid"
OTP_STAGED = "OTP message has been staged, click Retry if you need to resend the OTP"
MULTIPLE_BALLOT_ENTRIES ="Sorry, you cannot post a ballot twice"
PAYLOAD_NOT_PROVIDED ="Sorry, no data has been provided."
SUCCESSFUL_POSTING = "Success! Your data has been posted successfully, it will be verified before being posted into the master list. As part of verification process you may receive a call from our agents to collect some more data from you."

@frappe.whitelist(allow_guest=True)
def authenticate_voter(voter_id = '', member_id = ''):
	search_args = dict(name=voter_id, id_number = member_id)
	if not frappe.db.get_value("Institution Member", search_args,"name"):
		frappe.local.response.update({'message': 'OTP Processing Failed', 'status':'error', 'error': str(ILLEGAL_LOGIN)})
		return
	stage_otp(voter_id)
	frappe.local.response.update({'message': 'OTP Has been Staged', 'status':'success', 'alert': str(OTP_STAGED)})
	#Create Wallet for Client if none exists
	p_args = dict(name=voter_id, public_key=["!=",""], private_key =["!=",""])
	
	wallet = frappe.get_all("Institution Member", filters = p_args, fields =["private_key","public_key"])

	if not wallet:
		wallet = create_voter_wallet(frappe.get_doc("Institution Member",voter_id))
	return
def create_voter_wallet(member_doc):
	wallet = create_wallet()
	member_doc.flags.ignore_permissions = True
	member_doc.set("private_key", wallet.get("private_key"))	
	member_doc.set("public_key", wallet.get("public_key"))
	member_doc.save()
	return wallet
@frappe.whitelist(allow_guest=True)
def stage_otp(voter_id = ''):
	valid_args = dict(voter=voter_id, valid=True)
	if  frappe.db.get_value("OTP Record", valid_args): 
		frappe.get_doc("OTP Record", valid_args).send_otp()
		return
	otp_code = str(frappe.generate_hash(length=8)).upper()
	args = dict(
		doctype = "OTP Record",
		voter= voter_id,
		key= otp_code,
		valid = 1
	)
	frappe.get_doc(args).insert(ignore_permissions=True)
	return otp_code

@frappe.whitelist(allow_guest=True)
def authenticate_otp(voter_id, key, resend_otp=0):
	args = dict(voter = voter_id, key=key, valid = 1)
	resend_args = dict(valid=1, voter=voter_id)
	if resend_otp:	
		frappe.get_doc("OTP Record", resend_args).send_otp()
		return
	if not frappe.db.get_value("OTP Record", args): 
		frappe.local.response.update({'message': 'Failed to authenticate OTP', 'status':'error', 'error': str(WRONG_OTP)})
		return
	#Set OTP as Invalid and proceed
	otp_record = frappe.get_doc("OTP Record", args)
	otp_record.invalidate()
	valid_elections_for_voter = get_voter_elections(voter_id= voter_id)

	if not valid_elections_for_voter: valid_elections_for_voter = get_voter_elections(voter_id= voter_id, status= "just_any")
	
	if not valid_elections_for_voter: return {}

	ballot = get_e_ballot(election= valid_elections_for_voter[0].name, voter=voter_id)
	handle_eth_wallet(voter_id)
	return ballot
@frappe.whitelist(allow_guest=True)
def voter_details_sandbox(payload=None):
	'''
	Acceptable/Sample data payload

	 {
        "member_id":"8418748729",
        "board_number":"97593592850",
        "surname":"Kamuge",
        "other_names":"Thuranira Paul",
        "id_number":"6513561537",
        "cell_number":"0772919939",
        "email_address":"dsmwaura@gmail.com",
        "electoral_district_text": "Moi Teaching and referral"

    } 
	'''
	if not payload:
		frappe.local.response.update({'message': 'Failed to post your data', 'status':'error', 'error': str(PAYLOAD_NOT_PROVIDED)})
		return
	try:
		data = json.loads(payload)
		data['doctype'] = "Institution Member Sandbox"
		doc = frappe.get_doc(data).insert(ignore_permissions=True)
		docname = doc.get("name")
		frappe.local.response.update({'message': f'Successfully Posted. Tracking ID: {docname}', 'status':'success', 'response': str(SUCCESSFUL_POSTING)})
	except Exception as e:
		frappe.local.response.update({'message': 'Failed to post your data', 'status':'error', 'error': f"{e}"})
def handle_eth_wallet(voter_id):
	pass
@frappe.whitelist(allow_guest=True)
def get_voter_elections(voter_id, status=None):
	election_status = ['Open'] if status==None else ['Closed', 'Scheduled']
	voter_registers = frappe.db.sql(f"SELECT DISTINCT parent  FROM `tabVoter Register Member` WHERE system_id = '{voter_id}' AND parent IN (SELECT applicable_voter_register FROM `tabElection` WHERE docstatus = 1)", as_dict=1)
	voter_register_list =[x.get("parent") for x in voter_registers]
	elections = frappe.db.get_all("Election", filters={"applicable_voter_register":["IN",voter_register_list], "docstatus":1, "status":["IN",election_status]},fields=["name","election_start","election_ends","status"], order_by='creation desc')
	return elections
def get_has_voted(voter='', election =''):
	args = dict(doctype="Ballot Entry", voter_id=voter, election=election)
	return frappe.db.exists(args)
@frappe.whitelist(allow_guest=True)
def get_e_ballot(election, voter = None):
	payload ={}
	
	institution = get_voter_institution(voter) 
	institution_contact = frappe.db.get_value("Institution", institution, "phone")
	voter_name = get_voter_fullname(voter)
	voter_doc = frappe.get_doc("Institution Member", voter)
	election_doc = frappe.get_doc("Election",election)
	payload["institution"] = institution
	payload["institution_contact"] = institution_contact
	payload["voter_name"]= voter_name
	###
	payload["voter_branch"]= voter_doc.get("electoral_district")
	payload["voter_phone"]= voter_doc.get("cell_number")
	payload["voter_email"]= voter_doc.get("email_address")
	###
	payload["election"] = election_doc.name
	payload["election_start"] = election_doc.election_start
	payload["election_ends"] = election_doc.election_ends
	payload["status"] = election_doc.status
	if not voter: return payload
	has_voted = 'Yes' if get_has_voted(voter, election) else 'No'
	payload ["has_voted"] = has_voted  #Initialize payload with voting status
	payload["_ps_note"] = "will not populate ballot if above answer is yes"
	if has_voted =='Yes': return payload
	applicable_domains_for_voter = [x.get("electoral_district") for x in frappe.get_doc("Institution Member", voter).get("applicable_voter_districts")]
	def _positions_for_domain(position):
		return position.branch in applicable_domains_for_voter
	positions = filter(_positions_for_domain , election_doc.get("candidate_position_settings"))
	ballot_list =[]
	for position in positions:
		candidates_list = []
		p_obj ={}
		position, branch, max_posts = position.get("position"),position.get("branch"), position.get("maximum_number_of_positions")
		candidates_list = get_candidates_per_position(election, position, branch)
		if not candidates_list : continue
		p_obj["position"] = position
		p_obj["branch"] = branch
		p_obj["maximum_number_of_positions"] = max_posts
		p_obj["candidates"] = candidates_list
		ballot_list.append(p_obj)
	payload["ballot_data"] = ballot_list
	
	return payload
	# returns list e.g [{"position":"President" ,"max_posts":1, "enforce_max":[0,1],
	#  candidates:[{"candidate_1":[0,1]}{"candidate_2":[0,1]}]}]
def get_candidates_per_position(election, position=None, branch = None):
	args ={
			"parent":election,
			"branch": branch,
			"contested_position":position
		}
	result = frappe.db.get_all("Election Candidate",filters=frappe._dict(args),fields=['candidate_id','candidate_name','political_party','party_symbol','headshot'])#..Party, Symbol, Image,
	for j in result:
		j["choice"] = 0
	return result
@frappe.whitelist(allow_guest=True)
def post_e_ballot(voter, election, ballot_data): # Must include voter, election
	'''1. Posts a ballot to a Ballot Entry Doctype
	   2. Creates a transaction in the blockchain
	   3. Alerts Voter'''
	def ballot_tally(election):
		tally_args = dict(election=election)
		ballots = frappe.get_list("Ballot Entry",filters=tally_args)
		return len(ballots) + 1
	def already_voted(voter, election):
		return frappe.db.get_all("Ballot Entry", filters = dict(voter_id=voter, election=election), fields=['name'])
	if already_voted(voter, election):
		frappe.local.response.update({'message': 'Failed to post your ballot', 'status':'error', 'error': str(MULTIPLE_BALLOT_ENTRIES)})
		return
	institution = get_voter_institution(voter)
	ballot_document = frappe.get_doc({"doctype":"Ballot Entry",\
		"institution":institution,"voter_id": voter,"election":election})
	ballot_data = json.loads(ballot_data)
	for theposition in ballot_data:
		position = theposition.get('position')
		branch = theposition.get('branch')	
		for candidate in theposition.get('candidates'):
			row = ballot_document.append("ballot_entry_detail",{})
			row.position = position
			row.branch = branch
			row.candidate_id = candidate.get('candidate_id')
			row.candidate_name = candidate.get('candidate_name')
			row.choice = candidate.get('choice')
			row.political_party = candidate.get('political_party')
			row.party_symbol = get_party_symbol(candidate.get('political_party')) if candidate.get('political_party') else None
			row.headshot = get_headshot(candidate.get('candidate_id'))
	ballot_document.current_tally = ballot_tally(election)
	ballot_document.insert(ignore_permissions=True)

	p_args = dict(name=voter, public_key=["!=",""], private_key =["!=",""])
	
	stored_wallet = frappe.get_all("Institution Member", filters = p_args, fields =["private_key","public_key"])

	wallet = None
	ballot_name =  ballot_document.get("name")
	
	#
	if stored_wallet:
		wallet = stored_wallet[0]
	if not wallet:
		wallet = create_voter_wallet(frappe.get_doc("Institution Member",voter))

	chain_payload = dict(election=election,voter=voter,ballot_data=ballot_data)

	tx_id = log_casted_vote(json.dumps(chain_payload), wallet.get("private_key"), wallet.get("public_key"))

	if tx_id:
		ballot_document.send_ballot_receipt(tx_id)
	frappe.local.response.update({'message': f'Your vote has been posted successfully under a unique ID: {ballot_name}', 'status':'success'})
	return ballot_document
def _return_branch_position_tally(election='', branch='', position='',pos_id=None):

	position_branch_results = []

	results = None

	tally = []

	position_branch_results = get_results(election, branch=branch, position=position)

	eligible_voters  = get_available_e_ballots(election, branch = branch)

	turnout = len(get_branch_voters(election, branch))

	turnout_percent = turnout*100/eligible_voters if eligible_voters > 0 else 0

	results = dict(id= pos_id, position = position, branch=branch, eligible_voters= eligible_voters, turnout=turnout, turnout_percent=turnout_percent)

	for j in position_branch_results:

		sub_tally= dict(candidate_id=j.get("candidate_id"), candidate =  j.get("candidate"), votes = j.get("votes"))

		tally.append(sub_tally)

	results["tally"] = tally

	return results

@frappe.whitelist(allow_guest=True)
def get_election_results(election):
	election_args = dict(name=election)
	institution = frappe.get_value("Election", election_args, "institution")
	all_results ={}	
	k = 0
	position_args =dict(parent = election)
	advertised_positions = frappe.get_all("Candidate Position Settings", filters= position_args, fields = ["branch","position"], order_by='idx asc')
	contested_branch_results = []
	for advertised_position in advertised_positions:

		results={}

		branch = None

		position = None

		branch = advertised_position.get("branch")

		position = advertised_position.get("position")

		# print(branch, position)

		k += 1
		

		# some_args = dict(election=election,branch=branch,position=position, id=k)
		

		

		results = _return_branch_position_tally(election=election, branch=branch, position=position,pos_id=k)

		# print(results)
		
		if results.get("tally"):
			contested_branch_results.append(results)
		else:
			k -= 1
	all_results["institution"] = institution
	all_results["all_results"] = contested_branch_results

	# Broadcast the results to the channel we are listening on.
	# frappe.publish_realtime('election', f"{'message': {all_results},'vote'}")

	return all_results
def call_results(election, branch=None):
	args = dict(parent=election, branch=branch)
def get_branch_position_limits(election, branch, position=None):
	args= dict(parent=election, branch=branch, position=position)
	return frappe.get_all("Candidate Position Settings", filters=args, fields=["position","maximum_number_of_positions"])
def get_voter_institution(voter):
	return frappe.db.get_value("Institution Member", voter, "institution")
def get_votes_cast(election, branch = None):
	pass
	#All/branch votes cast in an election
def get_available_e_ballots(election, branch = None):
	applicable_voter_register = frappe.get_doc("Election", election).applicable_voter_register
	if not branch:
		return frappe.db.count("Voter Register Member",{"parent":applicable_voter_register})
	register = frappe.get_doc("Voter Register", applicable_voter_register)

	members = [x.get("system_id") for x in register.get("active_members")]

	child_branches = get_branch_children(branch)  # All sub branches members are to be included in the total number of ballots

	args = dict(electoral_district=["IN", child_branches], name = ["IN", members])

	return len(frappe.db.get_all("Institution Member",filters = args))
	#All/branch Voters in the register
def get_branch_children(branch):
	# implement recursion
	children =[branch]
	def handle_children(child):
		children.append(child)
	def get_children(branch = '', search_params = {}):	
		children = frappe.get_all("Electoral District", filters = search_params, fields=["name"])
		if children:
			child_list = [x.get("name") for x in children]
			list(map(lambda x: handle_children(x), child_list))
			for x in child_list:
				child_params = dict(parent_electoral_district = x)
				get_children(branch=x, search_params=child_params)
	args = dict(parent_electoral_district=branch)			
	get_children(branch=branch,search_params=args)
	return children
def get_voter_fullname(voter):
	return frappe.db.get_value("Institution Member", voter, "full_name")
def get_maximum_posts_per_position(election, position, branch = None):
	# Return integer
	pass
@frappe.whitelist(allow_guest=True)
def ping():
	return 'Zahari says: pong'

@frappe.whitelist(allow_guest=True)
def get_votes_from_blockchain():


	return get_votes_cast_bc()
def election_status_switch():
	from datetime import datetime
	scheduled_args =dict(docstatus=1, status="Scheduled", election_start = ["<=",datetime.now()])


	scheduled_elections = frappe.get_all("Election",filters = scheduled_args, fields =["name"])

	open_args =dict(docstatus=1, status="Open", election_ends = ["<=",datetime.now()])

	open_elections = frappe.get_all("Election",filters = open_args, fields =["name"])

	def handle_open_elections(election):
		frappe.get_doc("Election", election).db_set("status", "Closed")
		
	def handle_scheduled_election(election):
		frappe.get_doc("Election", election).db_set("status", "Open")
		
	
	if scheduled_elections: 
		scheduled_election_list = [x.get("name") for x in scheduled_elections]
		list(map(lambda x: handle_scheduled_election(x), scheduled_election_list))


	if open_elections: 
		open_election_list = [x.get("name") for x in open_elections]
		
		list(map(lambda x: handle_open_elections(x), open_election_list))

	
	return




