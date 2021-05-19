from __future__ import unicode_literals
import frappe, json, hashlib
from frappe.model.document import Document
def flatten_ballots():
    ballots_to_flatten = frappe.get_all("Ballot Entry", filters=dict(election='KMPDU Main Election - 2021-7391'), fields=['name'])

    for j in ballots_to_flatten:
        frappe.get_doc("Ballot Entry", j.get("name")).flatten_ballot_by_voter_branch()