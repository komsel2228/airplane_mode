import frappe

def check_enable_rent_reminder():
    check_rent_reminder = frappe.db.get_single_value('Airport Tenant Settings','disabled_rent_reminder')
    if check_rent_reminder:
        get_auto_repeat = frappe.get_all('Auto Repeat',{'disabled':0,'notify_by_email':1},'name')
        if get_auto_repeat:
            for i in get_auto_repeat:
                frappe.db.set_value('Auto Repeat', i.name,'notify_by_email', 0, update_modified=True)
    else:
        get_auto_repeat = frappe.get_all('Auto Repeat',{'disabled':0,'notify_by_email':0},'name')
        if get_auto_repeat:
            for i in get_auto_repeat:
                frappe.db.set_value('Auto Repeat', i.name,'notify_by_email', 1, update_modified=True)



