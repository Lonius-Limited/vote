# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json, hashlib
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import _
from vote.utils.election_details import create_voter_wallet
import vote
from vote.utils.ethereum import (
    log_casted_vote,
    privKey,
    pubKey,
    get_votes_cast_bc,
    create_wallet,
    w3,
)


class BallotEntry(Document):
    def after_insert(self):
        return
        # self.process_blockchain()

    def process_blockchain(self):

        voter = self.get("voter_id")

        election = self.get("election")

        # ballot_entry = frappe.get_all("Ballot Entry", filters=dict(name=self.name), fields=["*"])[0]

        def _get_ballot_data(self):
            voter = self.voter_id
            choice = []
            for j in self.ballot_entry_detail:
                row = None
                row = dict(
                    position=j.position,
                    branch=j.branch,
                    candidate_id=j.candidate_id,
                    candidate_name=j.candidate_name,
                    choice=j.choice,
                )
                choice.append(row)
            return dict(voter=voter, choice=choice)

        ballot_data = _get_ballot_data(self)

        p_args = dict(name=voter, public_key=["!=", ""], private_key=["!=", ""])

        stored_wallet = frappe.get_all(
            "Institution Member", filters=p_args, fields=["private_key", "public_key"]
        )

        wallet = None

        if stored_wallet:
            wallet = stored_wallet[0]
        if not wallet:
            wallet = create_voter_wallet(frappe.get_doc("Institution Member", voter))

        chain_payload = dict(election=election, voter=voter, ballot_data=ballot_data)
        payload_hash = hashlib.sha256(
            (json.dumps(chain_payload, default=str)).encode("utf-8")
        ).hexdigest()
        ################################################To be changed
        privKey = "0x88493446687bb3ec38cd62ea85f46ea4a36e77e61bd41d1caff3bb58c5d2e1af"
        pubKey = "0x8f7B5cE33bef6ddf5cCF7ad9FcE4F7E1bfBb8E9e"

        # wallet = None
        wallet = dict(private_key=wallet.private_key, public_key=wallet.public_key)

        #############################################
        tx_id = log_casted_vote(
            json.dumps(
                {
                    "voter": voter,
                    "election": election,
                    "ballot": self.name,
                    "ballot_hash": str(payload_hash),
                }
            ),
            wallet.get("private_key"),
            wallet.get("public_key"),
        )

        if tx_id:
            self.db_set("tx_hash", tx_id)
            self.send_ballot_receipt(tx_id=tx_id)
            self.db_set("posted_to_blockchain", 1)
        return

    def get_ballot_receipt_message(self, tx_id=None):

        doc_hash = tx_id

        doc_id = self.get("name")

        voter_id = self.get("voter_id")

        time_of_voting = self.creation
        if doc_hash:
            return f"Dear voter {voter_id}! Your ballot was posted under ID: {doc_id} and blockchain hash {doc_hash}.Time of voting {time_of_voting}"
        return f"You Voted! Your ballot was posted under ID: {doc_id}.Time of voting {time_of_voting}"

    def send_ballot_receipt(self, tx_id=None):

        voter_id = self.get("voter_id")

        doc = frappe.get_doc("Institution Member", voter_id)

        telephone, email = doc.get("cell_number"), doc.get("email_address")

        message = self.get_ballot_receipt_message(tx_id)

        if telephone:
            send_sms([telephone], message)

        email_args = dict(
            recipients=[email], message=_(message), subject=_("Vote Receipt")
        )
        if email:
            vote.sendmail(
                recipients=[email], message=_(message), subject=_("Vote Receipt")
            )
            # enqueue(method=frappe.sendmail, queue="short", timeout=300, **email_args)

        self.save(ignore_permissions=True)

        return

    def add_to_tally(self):
        ballot = self.get("ballot_entry_detail")

        choices = list(filter(lambda x: x.choice == 1, ballot))

        for choice in choices:

            self.update_tally(choice, self.get("election"))

        self.db_set("tallied", 1)

        return

    def update_tally(self, choice={}, election=""):

        args = dict(election=election, candidate=choice.get("candidate_id"))

        tally_document = frappe.get_all(
            "Vote Repository", filters=args, fields=["name"]
        )

        if not tally_document:

            insert_args = dict(
                doctype="Vote Repository",
                election=election,
                branch=choice.get("branch"),
                position=choice.get("position"),
                candidate=choice.get("candidate_id"),
                vote_count=1,
                ballot=choice.get("parent"),
            )

            frappe.get_doc(insert_args).insert(ignore_permissions=True)

        else:

            tally_doc = frappe.get_doc("Vote Repository", tally_document[0].get("name"))

            vote_count_before = tally_doc.get("vote_count")

            updated_tally = vote_count_before + 1

            tally_doc.set("vote_count", updated_tally)

            tally_doc.save(ignore_permissions=True)

        return
