// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenant Contract", {
    refresh(frm){
        if((frm.doc.deposit_payment == 0)){
            frm.add_custom_button(__("Deposit Payment"), function () {
                frappe.model.open_mapped_doc({
                    method: "airplane_mode.airport_shop_management.doctype.tenant_contract.tenant_contract.create_deposit_payment",
                    frm: frm,
                });
                },
                __("Create")
            );
        }
        if((frm.doc.first_rent_payment == 0)){
            frm.add_custom_button(__("Rent Payment"), function () {
                frappe.model.open_mapped_doc({
                    method: "airplane_mode.airport_shop_management.doctype.tenant_contract.tenant_contract.create_rent_payment",
                    frm: frm,
                });
                },
                __("Create")
            );
        }
    },
    validate(frm) {
        if(frm.doc.rent_amount == 0){
            frappe.call({
                method: "airplane_mode.airport_shop_management.doctype.airport_tenant.airport_tenant.get_default_rent",
                args:{
                    airport: frm.doc.airport,
                    shop_type: frm.doc.shop_type
                },
                callback: function (r) {
                    if(r.message){
                        if (r.message[0] == flt(0)){
                            frappe.db.get_single_value("Airport Tenant Settings", "default_rent_amount").then((val) => {
                                frm.set_value("rent_amount", val)
                            });
                        }else{
                            frm.set_value("rent_amount", r.message[0])
                            frm.set_value("currency", r.message[1])
                        }
                    }
                },
            });
        }
    },
	update_contract_end_date(frm) {
        if(frm.doc.start_date && frm.doc.contract_term) {
            let end_date = frappe.datetime.add_months(frappe.datetime.add_days(frm.doc.start_date, -1), frm.doc.contract_term)
            frm.set_value("end_date", end_date)
        } else {
            frm.set_value("end_date", undefined)
        }
    },
    start_date(frm) {
        frm.events.update_contract_end_date(frm);
	},
    contract_term(frm) {
        frm.events.update_contract_end_date(frm);
	},
});
