# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	@frappe.whitelist()
	def check_start_date(doc, method=None):
		start_date = frappe.get_value('Airport Tenant Contract',{'parent': doc.airport_tenant,'is_completed':0,'contract_number':doc.contract_number},'start_date')
		if start_date:
			return start_date

@frappe.whitelist()
def update_status_document(status, name):
	if status == 'Unpaid':
		frappe.db.set_value('Rent Payment', name, "is_paid", 1)
		frappe.db.set_value('Rent Payment', name, "status","Paid")

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
    	target.print_format = "Rent Receipt"

    doclist = get_mapped_doc("Rent Payment", source_name, {
		"Rent Payment": {
			"doctype": "Auto Repeat",
			"field_map": {
	        },
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

    return doclist