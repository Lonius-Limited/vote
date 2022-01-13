// Copyright (c) 2021, team_paperless and contributors
// For license information, please see license.txt

frappe.ui.form.on('Agent Ballot Tally', {
	refresh: function(frm) {
		frm.set_intro('Note: This document is digitally signed and uniquely identified by a document hash. Please note that it can only be created once for this polling station in the selected election.');
		frm.set_query("polling_station", function() {
            return {
                "filters": {
                    "is_polling_station": 1,
                    
                }
            };
        });
		frm.set_query("agent", function() {
            return {
                "filters": {
                    "institution": frm.doc.institution,
                    
                }
            };
        });
	}
});
