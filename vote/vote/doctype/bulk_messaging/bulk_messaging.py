# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import enqueue
from frappe.core.doctype.sms_settings.sms_settings import send_sms
import vote

template = """
	<div>
	<p><b>Dear {} </b></p> 
	<p>You have been registered to participate in the KMPDU elections 2021. </p>
	<p><b>VOTER ID:</b> {} </p>
	<p>Use the Voter ID and your National ID to log into the portal provided below to verify or edit your details.</p>
	<p><b>URL:</b> https://kmpdu.bizpok.com </p>
	<br/>
	<b>KMPDU IEC</b>
	</div>
"""


class BulkMessaging(Document):
    def before_save(self):
        sms_context = []

        def get_context(receiver_list=[]):
            if receiver_list:
                return frappe.get_all(
                    "Institution Member",
                    filters=dict(cell_number=["IN", receiver_list]),
                    fields=[
                        "surname",
                        "other_names",
                        "cell_number",
                        "name",
                        "email_address",
                    ],
                )
            return frappe.get_all(
                "Institution Member",
                filters=dict(cell_number=["!=", ""]),
                fields=[
                    "surname",
                    "other_names",
                    "cell_number",
                    "name",
                    "email_address",
                ],
            )

        receiver_list = []
        if self.send_to_custom_recipients and self.receiver_list:
            receiver_list = list(dict.fromkeys(self.receiver_list.split("\n")))
        sms_context = get_context(receiver_list=receiver_list)
        contacts_available = len(sms_context)
        frappe.msgprint(f" will send sms to: {contacts_available} contacts")

    def on_submit(self):
        # self.queue_action("submit")
        frappe.msgprint("Transaction has begun in the background")
        # self.submit()
    @frappe.whitelist()
    def send_messages(self):
        frappe.msgprint("Starting business")
        try:
            sms_context = []

            receiver_list = []
            
            if self.send_to_custom_recipients and self.receiver_list:
                receiver_list = list(dict.fromkeys(self.receiver_list.split("\n")))

            sms_context = self.get_context(receiver_list=receiver_list)

            subject = self.get("subject")

            # list(map(lambda x: self.deliver_text_to(j,subject), sms_context))
            for j in sms_context:
                self.deliver_text_to(j, subject)

            # self.db_set("sent", 1)
        except Exception as e:
            self.db_set("sent", 0)
            # frappe.throw(f"{e}")

    def deliver_text_to(self, j, subject):
        template = None
        email_template = None
        email_template = self.get("email")
        template = self.get("message")
        first_name = j.get("surname")
        last_name = j.get("other_names")
        voter_id = j.get("name")
        telephone = None
        if j.get("cell_number"):
            telephone = str(j.get("cell_number")).replace("+", "")
        email_address = j.get("email_address").replace("+", "")
        msg = eval(f"""f'''{template}'''""")
        print(f"Sending message for {voter_id}")

        # email_msg = eval(f"""f'''{email_template}'''""")
        if telephone:
            send_sms([telephone], msg)
        #################
        return
        # if email_address:
        #     vote.sendmail(
        #         recipients=[email_address],
        #         message=email_msg,
        #         subject=f"{subject}",
        #     )
        # docname = self.name
        # log_args = None
        # log_args = dict(
        #     doctype="Voter Mail Log",
        #     voter=voter_id,
        #     message=msg,
        #     subject=f"{subject}-{docname}",
        #     response_text=f"""AA""",
        # )

        # frappe.get_doc(log_args).insert(ignore_permissions=True)

    def get_context(self, receiver_list=[]):
        if receiver_list:
            return frappe.get_all(
                "Institution Member",
                filters=dict(cell_number=["IN", receiver_list]),
                fields=[
                    "surname",
                    "other_names",
                    "cell_number",
                    "name",
                    "email_address",
                ],
            )
        return frappe.get_all(
            "Institution Member",
            filters=dict(cell_number=["!=", ""]),
            fields=[
                "surname",
                "other_names",
                "cell_number",
                "name",
                "email_address",
            ],
        )
