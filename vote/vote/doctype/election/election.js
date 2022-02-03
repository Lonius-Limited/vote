// Copyright (c) 2020, team_paperless and contributors
// For license information, please see license.txt

frappe.ui.form.on("Election", {
    onload_post_render: (frm) => {
        if (frm.is_new() || !frm.doc.election_officials[0].member) {
            console.log("is Dirty");
            frm.doc.election_officials.splice(0, 1);
            refresh_field("election_officials");
        }
    },
    refresh: function(frm) {
        frm.set_query("applicable_voter_register", () => {
            return {
                filters: {
                    institution: frm.doc.institution,
                },
            };
        });
    },
    institution: function(frm) {
        frm.set_query("applicable_voter_register", () => {
            return {
                filters: {
                    institution: frm.doc.institution,
                },
            };
        });
    },
    institution: function(frm) {
        frm.set_query("candidate_link", () => {
            return {
                filters: {
                    institution: frm.doc.institution,
                },
            };
        });
    },

    ship_voter_ids: function(frm) {
        frappe.call({
            method: "vote.utils.election_details.ship_election_voter_cards",
            args: { "election": frm.doc.name },
            callback: function(r) {
                frappe.msgprint(r)
            }
        })
    },
});

frappe.ui.form.on("Election Official", {
    refresh(frm) {
        // your code here
    },
    election_officials_add: function(frm) {
        frm.doc.institution ?
            console.log("Applying filters") :
            frappe.throw("Please select the institution first");
        var members = [];
        frm.doc.election_officials.forEach((row) => {
            if (row.member) {
                members.push(row.member);
            }
        });
        console.log(members);
        frm.set_query("member", "election_officials", () => {
            return {
                filters: {
                    institution: frm.doc.institution,
                    name: ["NOT IN", members],
                },
            };
        });
    },
});