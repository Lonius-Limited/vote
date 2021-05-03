from __future__ import unicode_literals
import frappe

@frappe.whitelist(allow_guest=True)
def get_headshot(id=''):
    # Contex is Voter ID 
    base_url = frappe.get_doc("Institution Member", id).get("image") or ''
    if 'http' in base_url:
        return base_url
    return frappe.utils.get_url(str(base_url))
@frappe.whitelist(allow_guest=True)
def get_party_symbol(id=''):
    # Contex is Political Party Name 
    base_url = frappe.get_doc("Political Party", id).get("party_symbol") or ''
    if 'http' in base_url:
        return base_url
    return frappe.utils.get_url(str(base_url))
