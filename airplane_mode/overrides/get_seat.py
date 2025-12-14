import frappe

def test():
    print("mamen")

def populate_seats():
    query = frappe.get_all('Airplane Ticket',{'seat':None,'name':'IndiGo-002-DJ-to-SH-006'},pluck='name')
    for i in query:
        recheck = frappe.get_doc('Airplane Ticket',i)
        seat = get_seat()
        recheck.db_set('seat',seat)
        frappe.db.commit()

def get_seat():
    import random
    numm = random.randint(1,50)
    charr = random.choice(['A','B','C','D','E'])
    seat = f"{numm}{charr}"
    return seat