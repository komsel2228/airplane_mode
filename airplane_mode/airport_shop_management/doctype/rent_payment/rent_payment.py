# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import money_in_words, get_first_day, get_last_day
from frappe.utils.data import format_date
from frappe.core.doctype.communication.email import make
from frappe.utils.background_jobs import enqueue

class RentPayment(Document):
	def validate(doc):
		doc.notes = f"Rent Payment for periode {format_date(get_first_day(doc.posting_date))} until {format_date(get_last_day(doc.posting_date))}"
		doc.in_word = money_in_words(doc.amount,doc.currency)

	def on_submit(doc):
		if(doc.rent_type == 'Deposit'):
			frappe.db.set_value('Airport Tenant', doc.airport_tenant, "deposit_payment", 1)
			frappe.db.set_value('Tenant Contract', doc.tenant_contract, "deposit_payment", 1)
		else:
			start_date = doc.check_start_date()
			if str(start_date) == str(doc.posting_date):
				frappe.db.set_value('Airport Tenant', doc.airport_tenant, "first_rent_payment", 1)
				frappe.db.set_value('Tenant Contract', doc.tenant_contract, "first_rent_payment", 1)

	def on_cancel(doc):
		if(doc.rent_type == 'Deposit'):
			frappe.db.set_value('Airport Tenant', doc.airport_tenant, "deposit_payment", 0)
			frappe.db.set_value('Tenant Contract', doc.tenant_contract, "deposit_payment", 0)
		else:
			start_date = doc.check_start_date()
			if str(start_date) == str(doc.posting_date):
				frappe.db.set_value('Airport Tenant', doc.airport_tenant, "first_rent_payment", 0)
				frappe.db.set_value('Tenant Contract', doc.tenant_contract, "first_rent_payment", 0)

	@frappe.whitelist()
	def check_start_date(doc, method=None):
		start_date = frappe.get_value('Airport Tenant Contract',{'parent': doc.airport_tenant,'is_completed':0,'contract_number':doc.contract_number},'start_date')
		if start_date:
			return start_date

	@frappe.whitelist()
	def send_mail_rent_payment(doc):
		docname = frappe.get_doc(doc.doctype,doc.name)
		context = docname.as_dict()
		defa_email_template = frappe.db.get_single_value('Airport Tenant Settings','email_template_rent')
	
		if ((defa_email_template == None) or (defa_email_template == "")):
			rent_template = frappe.get_doc("Email Template", "Rent Receipt Email Template")
		else:
			rent_template = frappe.get_doc("Email Template", defa_email_template)

		defa_print_format_template = frappe.db.get_single_value('Airport Tenant Settings','print_format_rent')
		if ((defa_print_format_template == None) or (defa_print_format_template == "")) :
			rent_print_format = "Rent Receipt"
		else:
			rent_print_format = defa_print_format_template
			
		email = frappe.get_value("Airport Tenant",{'name':doc.airport_tenant},'tenant_email')
		email_args = {
			"recipients": email,
			"subject": rent_template.subject,
			"message": frappe.render_template(rent_template.response, context),
			"now": True,
			"attachments": [
				frappe.attach_print(
					doc.doctype,
					doc.name,
					file_name=doc.doctype,
					print_format=rent_print_format
				)
			],
		}
		enqueue(
			method=frappe.sendmail,
			queue="short",
			timeout=300,
			is_async=True,
			enqueue_after_commit=True,
			**email_args,
		)

		comm = frappe.get_doc(
			{
				"doctype": "Communication",
				"subject": rent_template.subject,
				"content": frappe.render_template(rent_template.response, context),
				"sent_or_received": "Sent",
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
			}
		).insert(ignore_permissions=True)
		
		return "success"

@frappe.whitelist()
def update_status_document(status, name,tenant):
	if status == 'Unpaid':
		frappe.db.set_value('Rent Payment', name, "is_paid", 1)
		frappe.db.set_value('Rent Payment', name, "status","Paid")
		frappe.db.set_value('Airport Tenant', tenant, "status","Rent")


@frappe.whitelist()
def create_auto_repeat(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc, map_child_doc
	def set_missing_values(source, target):
	    pass

	def update_item(source, target, source_parent):
		from frappe.utils import add_months

		start_date = frappe.get_value('Airport Tenant Contract',{'parent':source.airport_tenant,'is_completed':0},'start_date')
		end_date = frappe.get_value('Airport Tenant Contract',{'parent':source.airport_tenant,'is_completed':0},'end_date')
		next_month = add_months(start_date,1)
		recipient = frappe.get_value('Airport Tenant',{'name':source.airport_tenant},'tenant_email')

		defa_print_format_template = frappe.db.get_single_value('Airport Tenant Settings','print_format_rent')
		if ((defa_print_format_template == None) or (defa_print_format_template == '')):
			rent_print_format = "Rent Receipt"
		else:
			rent_print_format = defa_print_format_template

		target.reference_doctype = source.doctype
		target.reference_document = source.name
		target.start_date = next_month
		target.end_date = end_date
		target.submit_on_creation = 1
		target.disabled = 0
		target.frequency = "Monthly"
		target.repeat_on_day = (source.posting_date).day
		target.repeat_on_last_day = 0

		#notification
		target.notify_by_email = 1
		target.recipients = recipient
		target.subject = "Rent Receipt"
		target.print_format = rent_print_format

	doclist = get_mapped_doc("Rent Payment", source_name, {
		"Rent Payment": {
			"doctype": "Auto Repeat",
			"field_map": {
			},
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

	return doclist