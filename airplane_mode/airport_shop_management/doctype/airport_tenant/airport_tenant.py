# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class AirportTenant(Document):
	def validate(self):
		if(self.deposit_amount == flt(0)):
			self.deposit_amount = flt(self.get_defa())
	
	def get_defa(self):
		defa_deposit_amount = frappe.db.get_single_value('Airport Tenant Settings','default_deposit_amount')
		return defa_deposit_amount

@frappe.whitelist()
def create_rent_payment(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc
    def set_missing_values(source, target):
        pass

    def update_item(source, target, source_parent):
    	start_date = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'start_date')
    	rent_amount = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'rent_amount')
    	contract_number = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'contract_number')
    	target.airport_tenant = source.name
    	target.posting_date = start_date
    	target.rent_type = "Rent"
    	target.is_paid = 0
    	target.amount = flt(rent_amount)
    	target.contract_number = contract_number

    doclist = get_mapped_doc("Airport Tenant", source_name, {
		"Airport Tenant": {
			"doctype": "Rent Payment",
			"field_map": {
	       
	        },
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

    return doclist

@frappe.whitelist()
def create_deposit_payment(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc
    def set_missing_values(source, target):
        pass

    def update_item(source, target, source_parent):
    	start_date = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'start_date')
    	target.airport_tenant = source.name
    	target.posting_date = start_date
    	target.rent_type = "Deposit"
    	target.is_paid = 0
    	target.amount = flt(source.deposit_amount)

    doclist = get_mapped_doc("Airport Tenant", source_name, {
		"Airport Tenant": {
			"doctype": "Rent Payment",
			"field_map": {
	        },
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

    return doclist