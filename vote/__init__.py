# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import requests
from frappe import _
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

__version__ = '0.0.1'

MAILGUN_BASE_URL = "https://api.mailgun.net/v3/email.dalasystems.com/messages"
API = "4021f0585c350e90ff563fce35e29f3d-71b35d7e-e9e3edbd"
MAIL_FROM ="IEC KMPDU <mailgun@email.dalasystems.com>"

def sendmail(recipients=[], message="Test Message", subject ="Test Subject", args=None):
   if recipients:
    #  return send_simple_mailgun_message(recipients, message, subject)
    return sendgrid_email(recipients, message, subject)
def send_simple_mailgun_message(recipients, message, subject):
	return requests.post(
		MAILGUN_BASE_URL,
		auth=("api", API),
		data={"from": MAIL_FROM,
			"to": recipients,
			"subject": subject,
			"html": message})




def sendgrid_email(recepients, message, subject):
    email = Mail(
        from_email='IEC KMPDU <elections@kmpdu.org>',
        to_emails=','.join(recepients),
        subject=subject,
        html_content=message
    )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(email)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return {"success": "email sent successfully"}
    except Exception as e:
        print(e.message)
        return {"error": "failed to send email. Error={}".format(e.message)}