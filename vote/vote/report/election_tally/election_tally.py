# Copyright (c) 2013, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	
	election, branch, candidate,position = filters.get("election"), filters.get("branch"), filters.get("candidate"),filters.get("position")
	columns, data = ["Position","Branch","Candidate ID","Candidate","Votes"], get_results(election,\
		 branch=branch ,position=position, candidate=candidate)
	return columns, data
def get_results(election=None, branch=None, candidate=None, position=None, maximum_candidates_per_post=None):

	all_ballots = frappe.get_all("Ballot Entry",filters={"election": election}, fields="name")

	
	if not all_ballots: return [] #No results to announce !

	ballot_ids = [x.get("name") for x in all_ballots]

	args = search_params(branch=branch, candidate_id=candidate,position=position, page_length=maximum_candidates_per_post) 

	args["parent"] = ["IN", ballot_ids]

	data  = election_results(args)

	return data
	
def election_results(args):
	return frappe.db.get_all("Ballot Entry Detail", filters=args, \
		fields=['position','branch','candidate_id','candidate_name as candidate','sum(choice) as votes'],\
			group_by='candidate_id',\
				order_by='position, votes desc')

def get_branch_results(election, branch):
	branch_voters = get_branch_voters(election,branch)

	filtered_ballots = frappe.get_all("Ballot Entry",filters={"election": election, "voter_id":["IN", branch_voters]}, fields="name")

	ballot_ids = [x.get("name") for x in filtered_ballots]

	args = dict(parent = ["IN", ballot_ids])

	return election_results(args)

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

def get_branch_voters(election, branch):#Those who voted
	
	branch_children = []

	branch_children = get_branch_children(branch)

	args = dict(election=election,tallied=1, branch=["IN", branch_children])

	# return sum([x.get("vote_count") for x in frappe.get_all("Ballot Entry", filters=args), fields=["vote_count"]])

	return frappe.get_all("Ballot Entry", filters=args, fields=["*"])	

def search_params(branch=None, candidate_id=None, parent = None, position=None, page_length=None):
	params= dict(
		branch = branch,
		candidate_id = candidate_id,
		choice = True,
		position = position,
		parent = parent,
		page_length = page_length
	)
	to_pop =[x for x in list(params.keys()) if not params[x]]

	list(map(lambda x : params.pop(x), to_pop))

	return params
