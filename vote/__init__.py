# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import requests
from frappe import _
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail

__version__ = "0.0.1"

MAILGUN_BASE_URL = "https://api.mailgun.net/v3/email.dalasystems.com/messages"
API = "4021f0585c350e90ff563fce35e29f3d-71b35d7e-e9e3edbd"
MAIL_FROM = "IEC KMPDU <mailgun@email.dalasystems.com>"


def sendmail(recipients=[], message="Test Message", subject="Test Subject", args=None):
	voter = None
	arg_keys = []
	if args:
		args = [x for x in list(args.keys())]
	if recipients:
		if "voter" in arg_keys:
			voter = args.get("voter")
		response = send_simple_mailgun_message(
			recipients, message, subject
		)  # Brayo hapa ndo you need to switch, or we make this dynamic

		log_args = None

		for recipient in recipients:

			log_args = dict(
				doctype="Voter Mail Log",
				voter=voter,
				email_address=recipient,
				message=message,
				subject=subject,
				response_text=f"""{response.json()}""",
			)

			#    frappe.get_doc(log_args).insert(ignore_permissions=True)

			print(log_args)

		return response
	# return sendgrid_email(recipients, message, subject)


def send_simple_mailgun_message(recipients, message, subject):
	return requests.post(
		MAILGUN_BASE_URL,
		auth=("api", API),
		data={"from": MAIL_FROM, "to": recipients, "subject": subject, "html": message},
	)


#def sendgrid_email(recepients, message, subject):
#	email = Mail(
#		from_email="IEC KMPDU <elections@kmpdu.org>",
#		to_emails=",".join(recepients),
#		subject=subject,
#		html_content=message,
#	)
#	try:
#		sg = SendGridAPIClient(
#			"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"
#		)
#		response = sg.send(email)
#		print(response.status_code)
#		print(response.body)
#		print(response.headers)
#		return {"success": "email sent successfully"}
#	except Exception as e:
#		print(f"{e}")
#		return {"error": "failed to send email. Error={}".format(f"{e}")}


def make_candidate_logins():
	election = "KMPDU Main Election - 2021-7391"
	candidates_document = frappe.get_doc("Candidates", dict(election=election))
	j = 0
	candidate_documents = [
		frappe.get_doc("Institution Member", x.get("candidate_id"))
		for x in candidates_document.get("candidates") 
	]

	filtered = list(
		filter(lambda c:
			c.get("email_address") not in [j.get("name") for j in frappe.get_all("User")],
			candidate_documents,
		)
	)[:20]
	for candidate in filtered:
		j += 1
		print("{0}. Creating account for {1} {2}".format(str(j), candidate.get("name"), candidate.get("full_name")))
		candidate.create_application_user(preferred_role_profile="KMPDU Audit")
def send_notifications(
	email_list, message, subject, doctype, docname, default_sender=None
):
	# template_args = get_common_email_args(None)
	attachments = [frappe.attach_print(doctype, docname, file_name=docname)]
	email_args = {
		"recipients": email_list,
		"sender": default_sender,
		"message": _(message),
		"subject": subject,
		"attachments": attachments or None,
		"reference_doctype": doctype,
		"reference_name": docname,
	}
	enqueue(method=frappe.sendmail, queue="short", timeout=300, **email_args)
def enable_disabled_users():
	disabled = [x.get("name") for x in frappe.get_all("User",filters = dict(enabled=0))]
	list(map(lambda x: enable_user(x), disabled))
def set_default_passwords():
	users = [x.get("name") for x in frappe.get_all("User",filters = dict(role_profile_name='KMPDU Audit'))]
	list(map(lambda x: set_default_password(x), users))	
def enable_user(user):
	doc = frappe.get_doc("User", user)
	doc.set('enabled', 1)
	doc.save()
def set_default_password(user):
	doc = frappe.get_doc("User", user)
	doc.set('new_password', doc.name+"-@123kmpdu")
	doc.save()
