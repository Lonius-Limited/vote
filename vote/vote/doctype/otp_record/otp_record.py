# -*- coding: utf-8 -*-
# Copyright (c) 2021, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import msgprint, _
from vote import sendmail


class OTPRecord(Document):
    def after_insert(self):
        if self.instant_otp:
            self.send_otp()

    def send_otp(self):
        voter_id = self.get("voter")
        otp_code = self.get("key")
        doc = frappe.get_doc("Institution Member", voter_id)
        telephone, email = doc.get("cell_number"), doc.get("email_address")
        message = f"Your OTP Code is {otp_code}.\nNB: OTP IS Case sensitive."
        send_sms([telephone], message)
        docid = self.name
        email_message = f"<p>Your OTP Code is <b>{otp_code}</b>.\nNB: This code expires after use.</p>"
        sendmail(
            recipients=[email],
            message=_(email_message),
            subject=_(f"CryptoVote One Time Pin - {docid}"),
        )
        # enqueue(method=frappe.sendmail, queue='short', timeout=300, **email_args)

        return otp_code

    def invalidate(self):
        self.set("valid", False)
        self.flags.ignore_permissions = True
        self.save()
