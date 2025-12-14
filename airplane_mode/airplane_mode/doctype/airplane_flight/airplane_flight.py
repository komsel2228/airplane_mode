# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.change_crew_status_to_on_duty()
		self.db_set('status','Completed')

	def change_crew_status_to_on_duty(self):
		for i in self.airplane_flight_crews:
			frappe.db.set_value("Airplane Crew", i.airplane_crew, "is_on_duty", 1)

		
