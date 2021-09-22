// Copyright (c) 2021, team_paperless and contributors
// For license information, please see license.txt

frappe.ui.form.on('Poll Agent', {
	refresh(frm) {
		// your code here
	}
})

frappe.ui.form.on('Agent Polling Station', {
	polling_stations_add:(frm)=>{
	     frm.set_query("polling_station","polling_stations", function() {
            return {
                "filters": {
                    "is_polling_station": 1
                }
            };
        });
	}
})
