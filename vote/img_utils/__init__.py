from __future__ import unicode_literals
import frappe

@frappe.whitelist(allow_guest=True)
def get_headshot(id=''):
    # Contex is Voter ID 
    return frappe.get_doc("Institution Member", id).get("image")
@frappe.whitelist(allow_guest=True)
def get_party_symbol(id=''):
    # Contex is Political Party Name 
    return frappe.get_doc("Political Party", id).get("party_symbol")
