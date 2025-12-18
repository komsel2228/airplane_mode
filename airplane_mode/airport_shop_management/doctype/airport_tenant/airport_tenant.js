// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Tenant", {
	setup(frm) {
    frm.set_query("airport_shop", function() {
			return { filters: { airport: frm.doc.airport, disabled:0 }};
		});
	},
  refresh(frm){
    if(frm.doc.status == 'Booked'){
      frm.add_custom_button(__("Deposit Payment"), function () {
          frappe.model.open_mapped_doc({
            method: "airplane_mode.airport_shop_management.doctype.airport_tenant.airport_tenant.create_deposit_payment",
            frm: frm,
          });
        },
          __("Create")
      );
      frm.add_custom_button(__("Rent Payment"), function () {
          frappe.model.open_mapped_doc({
            method: "airplane_mode.airport_shop_management.doctype.airport_tenant.airport_tenant.create_rent_payment",
            frm: frm,
          });
        },
          __("Create")
      );
    }
  },
  airport(frm) {
    frm.set_value('airport_shop',undefined)
    frm.set_query("airport_shop", function() {
			return { filters: { airport: frm.doc.airport, disabled:0 }};
		});
	},
  update_contract_end_date(frm, cdt, cdn) {
    let row = locals[cdt][cdn]
    if(row.start_date && row.contract_term) {
      let end_date = frappe.datetime.add_months(frappe.datetime.add_days(row.start_date, -1), row.contract_term)
      frappe.model.set_value(cdt, cdn, "end_date", end_date)
    } else {
      frappe.model.set_value(cdt, cdn, "end_date", undefined)
    }
  }
});

frappe.ui.form.on("Airport Tenant Contract", {
  start_date(frm, cdt, cdn) {
    let row = locals[cdt][cdn]
    frm.events.update_contract_end_date(frm, cdt, cdn);
    if(row.start_date){
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
                frappe.model.set_value(cdt, cdn, "rent_amount", val)
              });
            }else{
              frappe.model.set_value(cdt, cdn, "rent_amount", r.message[0])
              frappe.model.set_value(cdt, cdn, "currency", r.message[1])
            }
          }
        },
      });
    }
  },
  contract_term(frm, cdt, cdn) {
    frm.events.update_contract_end_date(frm, cdt, cdn);
  },
})
