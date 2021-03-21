// Copyright (c) 2020, team_paperless and contributors
// For license information, please see license.txt

frappe.ui.form.on('Institution Member', {
	onload_post_render: function(frm) {
		console.log("Applying filters")
		frm.set_query('electoral_district',()=>{
			return {
				"filters":{
					'is_group': 0
				}			
			}
		})
	}
});
