// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button(__('Assign Seat'), function() {
            let d = new frappe.ui.Dialog({
                title: 'Select Seat',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data'
                    }
                ],
                size: 'small', 
                primary_action_label: 'Assign',
                primary_action(values) {
                    frm.set_value('seat',values.seat_number)
                    d.hide();
                }
            });

            d.show();

       }, __("Action"));
	},
    flight_price(frm) {
        frm.trigger("update_total_amount")
    },
    update_total_amount(frm){
        let total_d = 0
        for(let item of frm.doc.add_ons){
            total_d += item.amount;
        }
        const amount = frm.doc.flight_price + total_d;
        frm.set_value("total_amount",amount)
    },
    
});

frappe.ui.form.on("Airplane Ticket Add-on Item", {
	amount(frm,cdt,cdn) {
        frm.trigger("update_total_amount")
	},
    items_remove(frm){
        frm.trigger("update_total_amount")
    }
});
