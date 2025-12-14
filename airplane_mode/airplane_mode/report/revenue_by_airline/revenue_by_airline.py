# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	data = get_datas(filters)

	chart = {
		"data": {
			"labels": [i[0] for i in data],
			"datasets": [{"values": [i[1] for i in data]}],
		},
		
		"type": "donut",
	}

	total_summary = 0
	for i in data:
		total_summary += flt(i[1])

	report_summary = [{"value": [total_summary], "label": _("Total Revenue"), "datatype": "Currency"},]

	return columns, data, None, chart,report_summary

def get_columns():
	return[
		_("Airline")+ ":Link/Airline:100",
		_("Revenue")+ ":Currency:100",
	]

def get_datas(filters):
	data = []

	get_airline = frappe.get_all('Airline','name',order_by='name asc')
	if get_airline:
		for i in get_airline:
			query = frappe.db.sql("""select sum(a.total_amount) as revenue from `tabAirplane Ticket` a 
					inner join `tabAirplane Flight` b on a.flight = b.name inner join `tabAirplane` c on b.airplane = c.name
					where a.docstatus = 1 and c.airline = %s group by c.airline asc""",i.name,as_dict=1)
			
			if query == []:
				data.append([
					i.name,
					flt(0)
				])
			else:
				for j in query:
					data.append([
						i.name,
						j.revenue
					])

	return data
