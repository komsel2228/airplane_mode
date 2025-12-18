# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import flt

class AirportTenant(WebsiteGenerator):
	def validate(self):
		if(self.deposit_amount == flt(0)):
			self.deposit_amount = flt(self.get_defa())

	def on_update(self):
		if(self.route==None or self.route == ''):
			route = f"tenant/{self.name}"
			frappe.db.set_value('Airport Tenant', self.name,'route', route, update_modified=True)
			self.reload()

		if(self.airport_shop): 
			if self.status == 'Expired':
				frappe.db.set_value('Airport Shop', self.airport_shop,'is_available', "Yes", update_modified=True)
			else:
				frappe.db.set_value('Airport Shop', self.airport_shop,'is_available', "No", update_modified=True)
				frappe.db.set_value('Airport Shop', self.airport_shop,'airport_tenant', self.name, update_modified=True)

	def get_defa(self):
		defa_deposit_amount = frappe.db.sql("""select deposit_amount from `tabAirport Detail Rent` where parent = %s and shop_type = %s""",(self.airport,self.shop_type),as_dict=1)
		if defa_deposit_amount == []:
			defa_deposit_amount = frappe.db.get_single_value('Airport Tenant Settings','default_deposit_amount')
		else:
			defa_deposit_amount = defa_deposit_amount[0].deposit_amount
		return defa_deposit_amount

@frappe.whitelist()
def create_rent_payment(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc, map_child_doc
    def set_missing_values(source, target):
        pass

    def update_item(source, target, source_parent):
    	start_date = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'start_date')
    	rent_amount = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'rent_amount')
    	currency = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'currency')
    	contract_number = frappe.get_value('Airport Tenant Contract',{'parent':source.name,'is_completed':0},'contract_number')
    	target.airport = source.airport
    	target.naming_series = None
    	target.posting_date = start_date
    	target.rent_type = "Rent"
    	target.is_paid = 0
    	target.amount = flt(rent_amount)
    	target.contract_number = contract_number
    	target.currency = currency

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
    	target.naming_series = None
    	target.posting_date = start_date
    	target.rent_type = "Deposit"
    	target.currency = "USD"
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

@frappe.whitelist()
def get_default_rent(airport,shop_type):
	get_default_rent = frappe.db.sql("""select rent_amount,currency from `tabAirport Detail Rent` where parent = %s and shop_type = %s""",(airport,shop_type),as_dict=1)
	if get_default_rent == []:
		get_rent = 0
		get_currency = None
	else:
		get_rent = get_default_rent[0].rent_amount
		get_currency = get_default_rent[0].currency

	return get_rent,get_currency