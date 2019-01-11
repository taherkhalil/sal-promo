# -*- coding: utf-8 -*-
# Copyright (c) 2017, taherkhalil52@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Promocode(Document):
	pass
def apply_promo(doc, method):
	Promocode_list =frappe.db.sql("select promocode_name from tabPromocode",as_list=1)
	pl= [x[0] for x in Promocode_list]
	frappe.errprint([Promocode_list,pl])

	if doc.promocode !="0":
		if doc.promocode in pl:
			pro = frappe.get_doc("Promocode", doc.promocode)
			discount_per = pro.dis_per
			grand_total = doc.grand_total
			discount_amount = (float(grand_total) * float(discount_per))/100


			doc.discount_amount =discount_amount
		else:
			frappe.msgprint("inValid promocode")

@frappe.whitelist()			
def from_pos_call(promo):
	frappe.errprint("in promo")
	# frappe.errprint(promo)
	Promocode_list =frappe.db.sql("select name from `tabPromo code`",as_list=1)
	pl= [x[0] for x in Promocode_list]
	frappe.errprint([Promocode_list,pl])
	if promo in pl:
		pro = frappe.get_doc("Promo code", promo)
		frappe.errprint("right promo")
		discount_per = pro.dis_per
		frappe.errprint(discount_per)
		# grand_total = doc.grand_total
		# discount_amount = (float(grand_total) * float(discount_per))/100
		# doc.discount_amount =discount_amount
		return discount_per


@frappe.whitelist()
def get_sales_order_items(so_name):
	frappe.errprint("get sales item called")
	doc = frappe.get_doc("Sales Order",so_name)
	item_dict ={}
	row ={}
	for item in doc.get("items"):
		item_dict[item.item_code]=item.qty

	so_dict ={
	'customer':doc.customer,
	'items':item_dict
	}

	return so_dict
