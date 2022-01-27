// Copyright (c) 2016, team_paperless and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Election Tally"] = {
	"filters": [
		{
			"fieldname":"election",
			"label": __("Election"),
			"fieldtype": "Link",
			"options": "Election",
			"reqd": 1,
			
		},
		{
			"fieldname":"branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Electoral District",
			"reqd": 0,
			// Institution
			
		},
		{
			"fieldname":"position",
			"label": __("Position"),
			"fieldtype": "Link",
			"options": "Institution Position",
			"reqd": 0,
			// Eligible voter Filter
		},
		{
			"fieldname":"candidate",
			"label": __("Candidate"),
			"fieldtype": "Link",
			"options": "Institution Member",
			"reqd": 0,
			// Eligible voter Filter
		},
	]
};
