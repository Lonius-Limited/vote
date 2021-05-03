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

    def send_messages(self):
        try:
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

            subject = self.get("subject")

            for j in sms_context:
                template = None
                email_template = None
                email_template = self.get("email")
                template = self.get("message")
                first_name = j.get("surname")
                last_name = j.get("other_names")
                voter_id = j.get("name")
                telephone = str(j.get("cell_number")).replace("+", "")
                email_address = j.get("email_address").replace("+", "")
                msg = eval(f"""f'''{template}'''""")

                email_msg = eval(f"""f'''{email_template}'''""")

                send_sms([telephone], msg)
                #################

                vote.sendmail(
                    recipients=[email_address], message=email_msg, subject=f"{subject}"
                )
            self.db_set("sent", 1)
        except Exception as e:
            self.db_set("sent", 0)
            frappe.throw(f"{e}")
