# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class TenantContract(Document):
	pass


@frappe.whitelist()
def create_rent_payment(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc
    def set_missing_values(source, target):
        pass

    def update_item(source, target, source_parent):
    	target.airport = source.airport
    	target.airport_tenant = source.airport_tenant
    	target.tenant_name = source.tenant_name
    	target.contract_number = source.contract_number
    	target.tenant_contract = source.name
    	target.naming_series = None
    	target.posting_date = source.start_date
    	target.rent_type = "Rent"
    	target.is_paid = 0
    	target.amount = flt(source.rent_amount)
    	target.currency = source.currency

    doclist = get_mapped_doc("Tenant Contract", source_name, {
		"Tenant Contract": {
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
    	target.airport = source.airport
    	target.airport_tenant = source.airport_tenant
    	target.tenant_name = source.tenant_name
    	target.contract_number = source.contract_number
    	target.tenant_contract = source.name
    	target.naming_series = None
    	target.posting_date = source.start_date
    	target.rent_type = "Deposit"
    	target.currency = source.currency_deposit
    	target.is_paid = 0
    	target.amount = flt(source.deposit_amount)

    doclist = get_mapped_doc("Tenant Contract", source_name, {
		"Tenant Contract": {
			"doctype": "Rent Payment",
			"field_map": {
	        },
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)

    return doclist