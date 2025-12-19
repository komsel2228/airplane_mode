# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.change_crew_status_to_on_duty()
		self.db_set('status','Completed')

	def change_crew_status_to_on_duty(self):
		for i in self.airplane_flight_crews:
			frappe.db.set_value("Airplane Crew", i.airplane_crew, "is_on_duty", 1)

def change_gate(docname,to_gate):
	get_airplane_ticket = frappe.get_all('Airplane Ticket',{'flight':docname,'status':('!=','Boarded')},'name')
	if get_airplane_ticket:
		for i in get_airplane_ticket:
			frappe.db.set_value("Airplane Ticket", i.name, 'gate', to_gate, update_modified=True)

@frappe.whitelist()
def process_change_gate(docname,to_gate):
	enqueue(change_gate, docname=docname, to_gate=to_gate, timeout=600, job_name="change_gate", job_id="change_gate", queue="short")
	return to_gate
