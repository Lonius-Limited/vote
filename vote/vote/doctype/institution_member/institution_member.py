# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.user_permission.user_permission import clear_user_permissions
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils.background_jobs import enqueue
from frappe import _
from vote.utils.election_details import stage_otp
from vote import sendmail


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
sms_template ="""
	Dear {} , You have been registered to participate in the KMPDU elections 2021. 
	VOTER ID: {}
	Use the Voter ID and your National ID to log into the portal provided below to verify or edit your details.
	URL: kmpdu.bizpok.com
"""


class InstitutionMember(Document):
	def before_save(self):
		self = self.capitalize_essential_fields()
		self.validate_member_id()	
		surname = self.surname
		other_names = self.other_names	 
		self.full_name = f"{surname}, {other_names}"
		self.generate_voter_domains()
		return
	def capitalize_essential_fields(self):
		if self.surname:
			self.set('surname',str(self.surname).upper().strip())
		if self.other_names:
			self.set('other_names',str(self.other_names).upper().strip())
		if self.electoral_district:
			self.set('electoral_district',str(self.electoral_district).upper().strip())
		if self.email_address:
			self.set('email_address',str(self.email_address).lower().strip())
		return self
	def validate_member_id(self):
		duplicate = frappe.db.get_value("Institution Member",\
			{"member_id": self.member_id,"institution": self.institution,"name":["!=",self.name]},"full_name")
		if duplicate:
			member_id = self.member_id
			frappe.throw(f"""Sorry, Member ID {member_id} is already taken by another member: {duplicate}""")
	def generate_voter_domains(self):
		electoral_district = self.electoral_district
		frappe.msgprint(f"Generating active domains for {electoral_district}")
		applicable_domains = self.member_applicable_domains(electoral_district)
		self.set("applicable_voter_districts",[])
		for j in applicable_domains:
			row = self.append('applicable_voter_districts',{})
			row.electoral_district = j
		frappe.msgprint(f"Applicable Domains {applicable_domains}")
	def member_applicable_domains(self,electoral_district):
		domain = electoral_district
		applicable_domains =[]
		proceed = True
		while proceed:
			if frappe.get_value("Electoral District", domain,"parent_electoral_district"):	
				applicable_domains.append(domain)
				domain = frappe.get_value("Electoral District",domain,'parent_electoral_district')
			else:
				applicable_domains.append(domain)
				proceed = False
		return applicable_domains
	def apply_permissions(self):
		userid = self.create_user
		self.set("user_id",userid)
		return
		#clear_user_permissions(userid,"Institution")
				#frappe.get_doc()
		institution = self.institution
		fullname = self.get("full_name")
		#if institution:
		'''
		if userid:
			frappe.get_doc(dict(
					doctype='User Permission',
					user=userid,
					allow="Institution",
					for_value=institution,
					apply_to_all_doctypes=1
			))
		frappe.msgprint("User {0} - {1} has been assigned to {2}".format(userid, fullname, institution))
		#self.flags.ignore_user_permissions=True
		self.save()'''
	def create_application_user(self):
		position = self.current_position
		
		position_settings = frappe.db.get_value("Institution Position",position,
		["requires_application_user_account","is_elective"],as_dict=True)
		#frappe.throw(f"{position_settings.requires_application_user_account}")
		if self.member_status!="Active":
			frappe.throw("Inactive members cannot have a user account. Please check Member Status")
			return
		if not position_settings.requires_application_user_account:
			frappe.throw(f"{position} not permitted to have a user account. Please update Institution Position")
			return
		role_profile = "Institution Manager"
		user = frappe.get_doc({
							'doctype': 'User',
							'send_welcome_email': 1,
							'email': self.email_address,
							'first_name': self.full_name,
							'role_profile': role_profile
							#'user_type': 'Website User'
							#'redirect_url': link
							})
		user.insert()
		frappe.msgprint(f"{user}")
		return user
	def send_voter_card(self, election=None):

		if not election: return #has to be the election document

		voter_id = self.get("name")

		doc = self

		telephone, email = doc.get("cell_number"), doc.get("email_address")
	
		# message =  self.get_voter_registration_message(election=election)
		sms_msg = sms_template.format(self.get("full_name"), self.get("name"))

		if telephone: send_sms([telephone], sms_msg)

		# email_message =f"<h3></h3><h6>{message}</h6>"
		email_message = template.format(self.full_name, voter_id )
		# email_args =dict(
		# 	recipients = [email],
		#     message = _(email_message),
		# 	subject = _("Voter Registration ID")
		# )
		# if email: enqueue(method=vote.sendmail, queue='long', timeout=300, **email_args)
		if email: sendmail(recipients=[email], message=_(email_message), subject=_("Voter Registration ID"))
		return
	def get_voter_registration_message(self, election = None):
		if not election: return
		election_type = 'Mock' if election.is_mock_elections else ''
		institution = election.get("institution")
		starts_from = election.get("election_start")
		ends = election.get("election_ends")
		voter_id = self.get("name")
		voter_name = self.get("full_name")

		link1, link2 = "https://kmpdu.bizpok.com/", "https://vote-ui.netlify.app/#/"
		links_text = f"{link1} or {link2}"
		# otp = stage_otp(self.get("name"), instant_otp = 0)
		# details =f"Voter ID: {voter_id}\nElection Starts:{starts_from}\nElection Ends: {ends}\n\nPlease use {links_text} to access the system."
		details =f"Voter ID: {voter_id}\nLink: {links_text}."

		return f"KMPDU Elections Voter Instruction:\n{details}"

		'''return f"Dear {voter_name} your\
			 voting details for the upcoming {election_type} Elections in {institution}\
				 have been generated as below\n\n{details}\n\n"'''

		