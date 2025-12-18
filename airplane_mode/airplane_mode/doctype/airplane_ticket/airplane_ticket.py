# Copyright (c) 2025, ndk and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document
from frappe.utils import flt

class AirplaneTicket(Document):
	# def validate(self):
	# 	self.check_capacity()

	def before_save(self):
		self.check_capacity()
		self.get_seat()
		if self.add_ons:
			arr=[]
			total=0
			for i in self.add_ons:
				if not i.item in arr:
					arr.append(i.item)
					total+= flt(i.amount)
				else:
					frappe.throw(f"Duplicate Item {i.item}")

			self.total_amount = self.flight_price + total

	def check_capacity(self):
		get_airplane = frappe.get_value('Airplane Flight',{'name':self.flight,'docstatus':1},'airplane')
		if get_airplane == None:
			get_airplane = flt(0)

		get_capacity = frappe.get_value('Airplane',{'name':get_airplane},'capacity')
		get_count = frappe.db.count('Airplane Ticket',{'flight':self.flight})
	
		if flt(get_count) >= flt(get_capacity):
			frappe.throw('Capacity is Full')
		
	def get_seat(self):
		if(self.seat == None):
			# https://docs.python.org/3/library/random.html
			numm = random.randint(1,50)
			charr = random.choice(['A','B','C','D','E'])
			self.seat = f"{numm}{charr}"

	def before_submit(self):
		if(self.status != 'Boarded'):
			frappe.throw(f"Status must boarded!")




