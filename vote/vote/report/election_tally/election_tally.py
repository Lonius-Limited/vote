# Copyright (c) 2013, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	institution, election, branch, candidate = filters.get("institution"), filters.get("election"), filters.get("branch"), filters.get("candidate")
	columns, data = ["Position","Branch","Candidate","Votes"], get_data(institution, election,\
		 branch=branch or '%', candidate=candidate or '%')
	return columns, data
def get_data(institution, election, branch='%', candidate='%'):
	all_ballots = frappe.get_all("Ballot Entry",filters={"institution":institution,\
		"election": election}, fields=["name"])
	
	ballot_list = [x.get("name") for x in all_ballots]

	ballot_list_str = ''+', '.join("'{0}'".format(i) for i in ballot_list)+''

	branch_candidate_filter_cond =f"""branch LIKE '{branch}' and candidate_id LIKE '{candidate}'"""

	data = frappe.db.sql(f"""SELECT DISTINCT position, branch, candidate, sum(choice) FROM `tabBallot Entry Detail` WHERE parent IN {ballot_list_str}  GROUP BY position,branch,candidate""")

	return data
