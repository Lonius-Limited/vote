// Copyright (c) 2016, team_paperless and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Election Tally"] = {
	"filters": [
		{
			"fieldname":"institution",
			"label": __("Institution"),
			"fieldtype": "Link",
			"options": "Institution",
			"reqd": 1,
			
		},
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
			"fieldname":"candidate",
			"label": __("Candidate"),
			"fieldtype": "Link",
			"options": "Institution Member",
			"reqd": 0,
			// Eligible voter Filter
		},
	]
};
