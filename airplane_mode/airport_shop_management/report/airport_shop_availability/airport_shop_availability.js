// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.query_reports["Airport Shop Availability"] = {
	"filters": [
		{
			fieldname:"shop_id",
			label: __("Shop ID"),
			fieldtype: "Link",
			width: "80",
			options: 'Airport Shop',
		},
		{
			fieldname:"airport",
			label: __("Airport"),
			fieldtype: "Link",
			width: "80",
			options: 'Airport',
		},
		{
			fieldname:"is_available",
			label: __("Is Available for Rent"),
			fieldtype: "Select",
			options: " \nYes\nNo",
			default: "Yes",
			width: "80"
		}
	]
};