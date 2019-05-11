// Copyright (c) 2016, taherkhalil52@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Sales Report"] = {
"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default":frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"attended_by",
			"label": __("Service Provider"),
			"fieldtype": "Link",
			"options": "Service Providers",
			"width": "80",
			"reqd": 0
		},
	]
}

