// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Tenant", {
	setup(frm) {
        frm.set_query("shop_type", function() {
			return { filters: { enabled: 1 } };
		});
	},
  refresh(frm){
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
    frm.events.update_contract_end_date(frm, cdt, cdn);

  },
  contract_term(frm, cdt, cdn) {
    frm.events.update_contract_end_date(frm, cdt, cdn);
  },
})
