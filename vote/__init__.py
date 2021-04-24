# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import requests
from frappe import _

__version__ = '0.0.1'

MAILGUN_BASE_URL = "https://api.mailgun.net/v3/email.dalasystems.com/messages"
API = "4021f0585c350e90ff563fce35e29f3d-71b35d7e-e9e3edbd"
MAIL_FROM ="IEC KMPDU <mailgun@email.dalasystems.com>"

def sendmail(recipients=[], message="Test Message", subject ="Test Subject", args=None):
   if recipients:
     return send_simple_mailgun_message(recipients, message, subject)
def send_simple_mailgun_message(recipients, message, subject):
	return requests.post(
		MAILGUN_BASE_URL,
		auth=("api", API),
		data={"from": MAIL_FROM,
			"to": recipients,
			"subject": subject,
			"html": message})