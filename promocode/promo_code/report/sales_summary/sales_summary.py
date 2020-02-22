# Copyright (c) 2013, taherkhalil52@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt, cstr, cint


def execute(filters=None):
	# frappe.errprint("execute")
	columns = get_column()
	# frappe.errprint('columns are ')
	# frappe.errprint(columns)
	data = get_si_data(filters)
	return columns, data

def get_column():
	static= [
		_("Date") + ":Date:100",
		_("Sales Invoice") + ":Link/Sales Invoice:170", 
		_("Total Amount") + ":Currency:120", 
		_("Total Paid") + ":Currency:120"]
	# frappe.errprint("inside get columns")	


	mop=['Cash','KNET','Credit Card']
	for r in mop:
		static.append(_(r) + ":Currency:100")
	# static.append(_("Advance") + ":Currency:120")
	# static.append(_("Advance Date") + ":Date:100" )
	return static

def get_si_data(filters):
	conditions = ""
	conditions = get_conditions(filters)
	# frappe.errprint('get filters')
	# frappe.errprint(conditions)
	# doc_conditions = get_doc_conditions(filters)
	invoice_list=frappe.db.sql("""select name,posting_date,total,
		paid_amount from `tabSales Invoice`  where docstatus=1  %s  """%(conditions),as_dict=1)
	
	# sum_total = frappe.db.sql("""select DISTINCT (posting_date) ,
	# 	SUM(paid_amount)  from `tabSales Invoice`  where docstatus=1  %s  """%(conditions),as_dict=1) 
	# frappe.errprint(sum_total)


	# if not invoice_list:
	# 	msgprint(_("No record found"))
	# 	return columns, invoice_list
	data=[]
	n_cash=n_ol=n_knet=n_cred=0
	for inv in invoice_list:
	# 	total_discount_amount = inv.discount_amount
		row = [
			inv.posting_date,inv.name
		]

		# frappe.errprint(row)

		row +=[inv.total,inv.paid_amount]
		
		mode_of_payment=frappe.db.sql("select si.mode_of_payment,si.amount from `tabSales Invoice Payment` as si inner join `tabSales Invoice` as s on si.parent=s.name where si.parent='%s' and s.is_pos=1"%inv.name,as_dict=1)
		cash =knet=cred =chq =0
		if mode_of_payment:
			for mod in mode_of_payment:
				if mod.mode_of_payment == "Cash":
					cash = mod.amount
				if mod.mode_of_payment == "KNET":
					knet = mod.amount
				if mod.mode_of_payment =="Credit Card":
					cred = mod.amount
	

			row +=[cash,knet,cred]
			n_cash += cash
			n_knet += knet
			n_cred += cred

			data.append(row)
			
		else:
			row +=[0,0,0]
			data.append(row)
			

	# total = paid=discount =  out = advance= cash =chq=knet =cred =ol=  0
	# try:
	# 	for d in data:
	# 		total = total + d[8]
	# 		paid = paid + d[9]
	# 		cash = cash + d[10]
	# 		knet = knet + d[11]
	# 		cred = cred + d[12]
	# except:
	# 	frappe.errprint("error")
		# traceback.print_stack()
		# frappe.errprint(traceback.format_exception_only(sys.last_type,sys.last_value))
		# frappe.errprint(data)
	# tot_bold =[]
	# tot =['','<b>Total','','','','','','',total,paid,cash,knet,cred]
	# data.append(tot)
	return data

def get_conditions(filters):
	conditions = ""

	if filters.get("from_date"):
		
		conditions += " and posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	else:
		frappe.throw(_("'From Date' is required"))

	if filters.get("to_date"):
		conditions += " and posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
	else:
		frappe.throw(_("'To Date' is required"))

	if filters.get("pos_profile"):
		conditions += " and pos_profile = '%s' " % frappe.db.escape(filters["pos_profile"])

	return conditions