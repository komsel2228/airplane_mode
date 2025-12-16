# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirportShop(WebsiteGenerator):
	pass

@frappe.whitelist()
def get_terminal(airport=None):
	get_terminal = frappe.db.sql("""select terminal from `tabAirport Detail Terminal` where parent = %s""",airport,as_dict=1)
	arr = []
	for i in get_terminal:
		arr.append(i.terminal)
	
	return arr

@frappe.whitelist()
def get_sub_terminal(airport=None,terminal=None):
	get_sub_terminal = frappe.db.sql("""select sub_terminal from `tabAirport Detail Terminal` where parent = %s and terminal = %s""",(airport,terminal),as_dict=1)
	arr = []
	for i in get_sub_terminal:
		arr.append(i.sub_terminal)
	
	return arr

