# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShopLead(Document):
	pass

@frappe.whitelist()
def get_airport_shop(airport=None,terminal=None,sub_terminal=None):
	get_airport_shop = frappe.db.sql("""select name from `tabAirport Shop` where airport = %s and terminal = %s and sub_terminal = %s""",(airport,terminal,sub_terminal),as_dict=1)
	arr = []
	for i in get_airport_shop:
		arr.append(i.name)
	
	return arr