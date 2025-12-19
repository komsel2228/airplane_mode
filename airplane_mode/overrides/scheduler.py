import frappe
from frappe.core.doctype.communication.email import make
from frappe.utils.background_jobs import enqueue

def check_enable_rent_reminder():
    check_rent_reminder = frappe.db.get_single_value('Airport Tenant Settings','disabled_notif')
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

def send_mail_rent_payment():
    check_rent_reminder = frappe.db.get_single_value('Airport Tenant Settings','disabled_rent_reminder')
    if check_rent_reminder:
        print("send email disabled")
    else:
        res = frappe.get_all('Rent Payment',{'status':'Unpaid','docstatus':1},'name')
        if res:
            for i in res:
                docname = frappe.get_doc("Rent Payment",i.name)
                context = docname.as_dict()
                rent_template = frappe.get_doc("Email Template", "Rent Receipt Email Template")
                email = frappe.get_value("Airport Tenant",{'name':docname.airport_tenant},'tenant_email')
                email_args = {
                    "recipients": email,
                    "subject": rent_template.subject,
                    "message": frappe.render_template(rent_template.response, context),
                    "now": True,
                    "attachments": [
                        frappe.attach_print(
                            docname.doctype,
                            docname.name,
                            file_name=docname.doctype,
                            print_format="Rent Receipt"
                        )
                    ],
                }
                enqueue(
                    method=frappe.sendmail,
                    queue="short",
                    timeout=300,
                    is_async=True,
                    enqueue_after_commit=True,
                    **email_args,
                )

                comm = frappe.get_doc(
                    {
                        "doctype": "Communication",
                        "subject": rent_template.subject,
                        "content": frappe.render_template(rent_template.response, context),
                        "sent_or_received": "Sent",
                        "reference_doctype": docname.doctype,
                        "reference_name": docname.name
                    }
                ).insert(ignore_permissions=True)
                print(f"already send email for rent payment {docname.name}")
