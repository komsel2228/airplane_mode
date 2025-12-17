# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	columns = get_columns(filters)	
	conditions = get_conditions(filters)
	data = get_query(filters, conditions)

	return columns, data

def get_columns(filters):
	count = 0
	columns = [
		{
			"fieldname":"shop_id",
			"label": _("Shop ID"),
			"fieldtype": "Link",
			"options": "Airport Shop",
			"width": 80,
			"align": "left"
		},
		{
			"fieldname":"shop_type",
			"label": _("Shop Type"),
			"fieldtype": "Data",
			"width": 100,
			"align": "left"
		},
		{
			"fieldname":"shop_area",
			"label": _("Shop Area"),
			"fieldtype": "Data",
			"width": 150,
			"align": "left"
		},
		{
			"fieldname":"airport",
			"label": _("Airport"),
			"fieldtype": "Data",
			"width": 200,
			"align": "left"
		},
		{
			"fieldname":"terminal",
			"label": _("Terminal"),
			"fieldtype": "Data",
			"width": 200,
			"align": "left"
		},
		{
			"fieldname":"sub_terminal",
			"label": _("Sub Terminal"),
			"fieldtype": "Data",
			"width": 200,
			"align": "left"
		},
		{
			"fieldname":"is_available",
			"label": _("Is Available For Rent"),
			"fieldtype": "Data",
			"width": 180,
			"align": "left"
		}
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("shop_id"): conditions+=" AND name = '{}'".format(filters.get("shop_id"))
	if filters.get("airport"): conditions+=" AND airport = '{}'".format(filters.get("airport"))
	if filters.get("is_available"): conditions+=" AND is_available = '{}'".format(filters.get("is_available"))
	
	return conditions


def get_query(filters, conditions):
	data=[]
	s={}

	getdata = frappe.db.sql("""
		SELECT name,shop_type,shop_area,airport,terminal,sub_terminal,location,is_available,disabled 
		FROM `tabAirport Shop` 
		WHERE docstatus='0'%s ORDER BY name ASC"""% conditions,as_dict=1)

	if getdata:
		for i in getdata:
			s['shop_id']= i.name
			s['shop_type']= i.shop_type
			s['shop_area']= i.shop_area
			s['airport']=i.airport
			s['terminal']=i.terminal
			s['sub_terminal']=i.sub_terminal
			s['is_available']=i.is_available
	
			data.append(frappe._dict(s))
		return data