# -*- coding: utf-8 -*-
# Copyright (c) 2020, team_paperless and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.user_permission.user_permission import clear_user_permissions

class InstitutionMember(Document):
	def before_save(self):
		self.validate_member_id()
		surname = self.surname
		other_names = self.other_names
		self.full_name = f"{surname}, {other_names}"
		self.generate_voter_domains()
		return
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