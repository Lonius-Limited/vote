# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import _
from vote.utils.election_details import create_voter_wallet
from vote.utils.ethereum import log_casted_vote, privKey, pubKey, get_votes_cast_bc, create_wallet


class BallotEntry(Document):
	def after_insert(self):
		return
		# self.process_blockchain()
	def process_blockchain(self):

		voter = self.get("voter_id")
		
		election = self.get("election")

		ballot_data = frappe.get_all("Ballot Entry", filters=dict(name=self.name), fields=["*"])[0]

		p_args = dict(name=voter, public_key=["!=",""], private_key =["!=",""])
		
		stored_wallet = frappe.get_all("Institution Member", filters = p_args, fields =["private_key","public_key"])

		wallet = None

		if stored_wallet:
			wallet = stored_wallet[0]
		if not wallet:
			wallet = create_voter_wallet(frappe.get_doc("Institution Member",voter))

		chain_payload = dict(election=election,voter=voter,ballot_data=ballot_data)
		################################################To be changed
		privKey = '0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af'
		pubKey = '0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e'

		wallet = None
		wallet = dict(private_key=privKey, public_key=pubKey)
		
		#############################################
		tx_id = log_casted_vote(json.dumps(chain_payload, default=str), wallet.get("private_key"), wallet.get("public_key"))

		if tx_id:
			self.send_ballot_receipt(tx_id)
			self.db_set("posted_to_blockchain", 1)
		return
	def get_ballot_receipt_message(self, tx_id=''):

		doc_hash = tx_id

		doc_id = self.get("name")

		time_of_voting = self.creation

		return f"You Voted!\nYour ballot was posted under ID: {doc_id} and blockchain hash {doc_hash}.\nTime of voting {time_of_voting}"
	
	def send_ballot_receipt(self, tx_id =None):

		voter_id = self.get("voter_id")

		doc = frappe.get_doc("Institution Member", voter_id)

		telephone, email = doc.get("cell_number"), doc.get("email_address")
	
		message =  self.get_ballot_receipt_message(tx_id)


		if telephone: send_sms([telephone], message)

		email_args =dict(
			recipients = [email],
		    message = _(message),
			subject = _("Vote Receipt")
		)
		if email: enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)

		self.save(ignore_permissions=True)

		return
