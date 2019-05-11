# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import traceback
import sys
from frappe import msgprint, _
from frappe.utils import flt, cstr, cint

def execute(filters=None):
	frappe.errprint("execute")
	columns = get_column()
	frappe.errprint('columns are ')
	frappe.errprint(columns)
	data = get_si_data(filters)
	return columns, data

def get_column():
	static= [
		_("Date") + ":Date:100",
		_("Sales Invoice") + ":Link/Sales Invoice:170", 
		_("Customer") + ":Link/Customer:120",
		_("Service") + ":Link/Item:120" ,
		_("Qty") + ":Data:120",
		_("Rate") + ":Currency:120",
		_("Amount") + ":Currency:120",
		_("Attended By") + ":Link/Service Providers:120",
		_("Total Amount") + ":Currency:120", 
		_("Total Paid") + ":Currency:120"]
	frappe.errprint("inside get columns")	


	mop=['Cash','KNET','Credit Card']
	for r in mop:
		static.append(_(r) + ":Currency:100")
	# static.append(_("Advance") + ":Currency:120")
	# static.append(_("Advance Date") + ":Date:100" )
	return static

def get_si_data(filters):
	conditions = get_conditions(filters)
	frappe.errprint('get filters')
	# doc_conditions = get_doc_conditions(filters)
	invoice_list=frappe.db.sql("""select name,posting_date,customer,total,
		paid_amount,total_advance , outstanding_amount,discount_amount
		from `tabSales Invoice`  where docstatus=1  %s  """%(conditions),as_dict=1)

	# if not invoice_list:
	# 	msgprint(_("No record found"))
	# 	return columns, invoice_list
	data=[]
	n_cash=n_ol=n_knet=n_cred=0
	for inv in invoice_list:
	# 	total_discount_amount = inv.discount_amount
		row = [
			inv.posting_date,inv.name, inv.customer
		]

		frappe.errprint(row)
		item_doctor_details = frappe.db.sql("""select parent, item_code, attended_by,qty,rate,amount,discount_amount
		from `tabSales Invoice Item` where parent LIKE "%s"   """%inv.name, as_dict=1)
		frappe.errprint(len(item_doctor_details))
		count = 0 
		docs =[]
		compiled =[]
		multi_item = False
		for doc in item_doctor_details :
			frappe.errprint("for doc in item")
			# docs = ['','','',doc.item_code ,doc.qty,doc.rate,doc.amount,doc.attended_by,0,0,0,0,0]
			# frappe.errprint(docs)
			if len(item_doctor_details) > 1 :
				frappe.errprint("lenght more")
				if count > 0:
					docs = ['','','',doc.item_code ,doc.qty,doc.rate,doc.amount,doc.attended_by,0,0,0,0,0]
					multi_item = True
					compiled.append(docs)
	# 				# total_discount_amount = total_discount_amount + doc.discount_amount
					frappe.errprint("exe if")
				else:
					row += [doc.item_code ,doc.qty,doc.rate,doc.amount,doc.attended_by]
	# 				# total_discount_amount = total_discount_amount + doc.discount_amount
	# 				# data.append(docs)
				count = count + 1
			else:
				frappe.errprint("not more than 1 service")
				row += [doc.item_code ,doc.qty,doc.rate,doc.amount,doc.attended_by]

		row +=[inv.total,inv.paid_amount]
		frappe.errprint("compiled")
		frappe.errprint(compiled)
		for com in compiled:
			frappe.errprint(com)
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
			# if cash :
			# 	row += [cash,0,0,0]
			# if ol:
			# 	row +=[0,0,0,ol]
			# if knet:
			# 	row +=[0,knet,0,0]
			# if cred:
			# 	row +=[0,0,cred,0]
			data.append(row)
			if multi_item:
				for docs in compiled:
					data.append(docs)
		else:
			row +=[0,0,0]
			data.append(row)
			if multi_item:
				for docs in compiled:
					data.append(docs)

	total = paid=discount =  out = advance= cash =chq=knet =cred =ol=  0
	try:
		for d in data:
			total = total + d[8]
			paid = paid + d[9]
			cash = cash + d[10]
			knet = knet + d[11]
			cred = cred + d[12]
	except:
		frappe.errprint("error")
		# traceback.print_stack()
		# frappe.errprint(traceback.format_exception_only(sys.last_type,sys.last_value))
		# frappe.errprint(data)
	# tot_bold =[]
	tot =['','<b>Total','','','','','','',total,paid,cash,knet,cred]
	data.append(tot) 
	# # frappe.errprint(paid)


# 	tot_paid=flt(n_cash)+flt(n_ol)+flt(n_knet)+flt(n_cred)
# 	data.append(['','','','',0,0,0,0,0,'',0,0,0,0])
# 	cash_totals= ['<b>Total cash','','','',n_cash,0,0,0,0,'',0,0,0,0]
# 	knet_totals= ['<b>Total knet','','','',n_knet,0,0,0,0,'',0,0,0,0]
# 	credit_totals= ['<b>Total credit','','','',n_cred,0,0,0,0,'',0,0,0,0]
# 	online_totals= ['<b>Total Online link','','','',n_ol,0,0,0,0,'',0,0,0,0]
# 	data.append(['','','','',0,0,0,0,0,'',0,0,0,0])
# 	total_paid = ['<b>Total Today Payment','','','',tot_paid,0,0,0,0,'',0,0,0,0]
# 	data.append(cash_totals)
# 	data.append(knet_totals)
# 	data.append(credit_totals)
# 	data.append(online_totals)
# 	data.append(total_paid)
# 	doc_wise_income =frappe.db.sql("""select lod.name,SUM(s.paid_amount) AS "total"
# 		from `tabSales Invoice Item` si , `tabList of Doctors` lod , `tabSales Invoice` s  where  si.doctor  =  lod.name and si.parent = s.name and s.docstatus = 1 and s.is_pos=1 %s GROUP BY lod.name """%(doc_conditions),as_dict=1) 
# 	doctors_income = ['<b>Doctor Wise Income','','','',0,0,0,0,0,'',0,0,0,0]
# 	frappe.errprint("doc_wise_income"+str(doc_wise_income))
# 	data.append(doctors_income)
# 	doc_list=frappe.db.sql("""select name from `tabList of Doctors`""",as_dict=1)
# 	for doctor in doc_list:
# 		income=frappe.db.sql("""select distinct s.name,p.amount as 'total',si.doctor,p.mode_of_payment,p.amount from `tabSales Invoice` as s inner join `tabSales Invoice Item` as si on s.name=si.parent inner join `tabSales Invoice Payment` as p on p.parent=si.parent where s.is_pos=1 and s.posting_date between %s and %s and s.docstatus=1 and si.doctor=%s""",(filters["from_date"],filters["to_date"],doctor.name),as_dict=1)
# 		advance_pay=frappe.db.sql("""select sum(allocated_amount) from `tabSales Invoice Advance` where posting_date between %s and %s and doctor=%s group by doctor""",(filters["from_date"],filters["to_date"],doctor.name))
# 		frappe.errprint("advance_pay"+str(advance_pay))
# 		if len(income)>=1:
# 			total_doc=0
# 			for row1 in income:
# 				total_doc += flt(row1.total)
# 			frappe.errprint(str(doctor.name)+str(total_doc))
# 			if not total_doc==0:
# 				row=['','','',doctor.name,total_doc]
# 				data.append(row)


			

	return data

# def getAmount(inv_num,from_date,to_date,mp):
# 	data=frappe.db.sql("""select pr.allocated_amount from `tabPayment Entry Reference` as pr inner join `tabPayment Entry` as p on pr.parent=p.name where pr.reference_name=%s and p.posting_date between %s and %s and p.mode_of_payment=%s""",(inv_num,from_date,to_date,mp))
# 	total=0	
# 	frappe.errprint("Data:"+str(data))
# 	if data:
# 		for row in data:
# 			total+=flt(row[0])
# 		frappe.errprint("Total"+str(total))
# 		return total
# 	else:
# 		frappe.errprint("Total"+str(total))
# 		return total	

'''
def getAmountTotal(inv_num,from_date,to_date,mp):
	data=frappe.db.sql(""" select sum(p.amount) from `tabSales Invoice Payment` as p inner join `tabSales Invoice` as s on p.parent=s.name where s.posting_date between %s and %s and s.is_pos=1 and s.docstatus=1 and s.name=%s and p.mode_of_payment=%s""",(from_date,to_date,inv_num,mp))
	if data:
		return data[0][0]
	else:
		return 0
'''

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

	if filters.get("attended_by"):
		conditions += " and (name) IN (select parent from `tabSales Invoice Item` where attended_by = '%s') " % frappe.db.escape(filters["attended_by"])
	

	# match_conditions = frappe.build_match_conditions("Sales Invoice")

	# if match_conditions:
	# 	conditions+= " and "+match_conditions
	return conditions

def get_doc_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and s.posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	else:
		frappe.throw(_("'From Date' is required"))

	if filters.get("to_date"):
		conditions += " and s.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])
	else:
		frappe.throw(_("'To Date' is required"))

	if filters.get("doctor"):
		conditions += " and lod.name = '%s'" % frappe.db.escape(filters["doctor"])
	

	# match_conditions = frappe.build_match_conditions("Sales Invoice")

	# if match_conditions:
		# conditions+= " and "+match_conditions

	return conditions
