// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Payment", {
	refresh(frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Unpaid") {
			frm.add_custom_button(__('Paid'), function() {
				frappe.confirm(('Are you sure to change status from unpaid to paid for this document ?'), ()=>{
					frappe.ui.form.is_saving = true;
					frappe.call({
						method: "airplane_mode.airport_shop_management.doctype.rent_payment.rent_payment.update_status_document",
						args: {"status": "Unpaid", "name": frm.doc.name,'tenant':frm.doc.airport_tenant},
						callback: function(r) {frm.reload_doc()},
						always: function() {
							frappe.ui.form.is_saving = false;
						}
					});
					
				})
			}, __('Status'));
		}

        if (frm.doc.docstatus == 1 && frm.doc.status == "Paid" && frm.doc.rent_type == 'Rent') {
            frappe.call({
				doc: frm.doc,
				method: "check_start_date",
				callback: function(res) {
                    if(res.message == frm.doc.posting_date){
                        frm.add_custom_button(__('Auto Repeat'), function() {
                            frappe.confirm(('Are you sure to create auto repeat from this document ?'), ()=>{
                                frappe.model.open_mapped_doc({
                                    method: "airplane_mode.airport_shop_management.doctype.rent_payment.rent_payment.create_auto_repeat",
                                    frm: frm
                                });
                            })
                        }, __('Create'));
                    }
                }
			});			
		}

		if(frm.doc.status == 'Unpaid'){
			frm.add_custom_button(__("Send Mail"), function () {
				frappe.db.get_single_value("Airport Tenant Settings", "disabled_rent_reminder").then((val) => {
					if (val == 1){
						frappe.msgprint(__("Send email disabled"));
					}else{
						frappe.call({
						doc: frm.doc,
						method: "send_mail_rent_payment",
						freeze: true,
						freeze_message: __("Sending email..."),
						callback: function(res) {
							if(res.message == "success") {
								frm.reload_doc()
								// frappe.msgprint(__("Already send email"));
								frappe.show_alert({
									message: __("Already send email"),
									indicator: "green",
								});
							}
						}
					});
					}
				});
			},
				__("Send")
			);
		}
	},
});