// Copyright (c) 2020, team_paperless and contributors
// For license information, please see license.txt
var domains =[]
var all_branch_positions=[]
var positions =[]
var branches=[]
var filtered_positions_by_branch=[]
frappe.ui.form.on('Candidates', {
	setup_queries:function(frm){
		
		frm.set_query("branch", "candidates", function () {
            return {
                filters: {
                    name: ["IN", branches]
                }
            };
        });
		frm.set_query("contested_position", "candidates", function () {
            return {
                filters: {
                    name: ["IN", positions]
                }
            };
        });
	},
	filter_positions_by_branch:(frm)=>{
		frm.set_query("contested_position", "candidates", function () {
            return {
                filters: {
                    name: ["IN", filtered_positions_by_branch]
                }
            };
        });
		refresh_field("candidates")
	},
	election : function(frm) {
		if(frm.doc.docstatus == 1){
			return 0
		}
		get_branch_positions(frm)
	}
});
frappe.ui.form.on('Candidates List', {
	candidates_add:(frm) => {
		if(!frm.doc.election){
			// let tb_length = frm.doc.candidates.length()
			// frm.doc.candidates.splice(tb_length-1)
			frappe.throw((__('Sorry, you have to select an election first')))
		}
		get_branch_positions(frm)

	
		frappe.ui.form.trigger("Candidates", 'setup_queries');

	},
	branch:(frm,cdt,cdn) =>{
		const d = locals[cdt][cdn];
		var selectedBranch = d.branch;
		console.log(selectedBranch)
		filtered_positions_by_branch =[]
		all_branch_positions.forEach(row=>{
			console.log("Row "+row.branch)
			if(row.branch==selectedBranch){
				filtered_positions_by_branch.push(row.position)
			}
		})
		console.log(filtered_positions_by_branch);

		frm.set_query("contested_position", "candidates", function () {
            return {
                filters: {
                    name: ["IN", filtered_positions_by_branch]
                }
            };
        });
		refresh_field("contested_position")
		// frappe.ui.form.trigger("Candidates", 'filter_positions_by_branch');
	},
	contested_position:(frm,dt, dn)=>{
		// const row = locals[dt][dn]
		// var selectedBranch = row.branch;
		// var selectedPosition = row.contested_position;

		// if(!position_in_branch(selectedBranch, selectedPosition).length < 1 ){
		// 	var applicable_positions = return_branch_positions(selectedBranch, selectedPosition).join()
		// 	frappe.throw(`Sorry, selected position does not apply. Please try ${applicable_positions}`)
		// }

		// frappe.ui.form.trigger("Candidates", 'filter_positions_by_branch');
	}
})
function get_branch_positions(frm){
	if(!frm.doc.election){
		return 0
		// frappe.throw((__('Sorry, you have to select an election first')))
	}
	let args = {"election": frm.doc.election}
	positions =[];
	branches =[]
	all_branch_positions =[]
	domains = frappe.call({method:"vote.vote.doctype.candidates.candidates.retrieve_election_domains",args}).then(result=>{

		all_branch_positions = result.message;

		result.message.forEach(row=>{
			positions.push(row.position)
			branches.push(row.branch)
		})
		//frappe.ui.form.trigger("Candidates", 'setup_queries');
	})
}
function position_in_branch(selectedBranch, selectedPosition){
	let applicable_positions =[]
	all_branch_positions.forEach((row=>{
		if (row.branch == selectedBranch && row.position == selectedPosition){
			applicable_positions.push(row.position)
		}
	}))
	return applicable_positions;
}

function return_branch_positions(selectedBranch){
	let applicable_positions =[]
	all_branch_positions.forEach((row=>{
		if (row.branch == selectedBranch){
			applicable_positions.push(row.position)
		}
	}))
	return applicable_positions;
}
