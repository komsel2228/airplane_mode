// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Tenant Settings", {
	setup(frm) {
        frm.set_query("print_format_rent", function() {
            return { filters: { doc_type: 'Rent Payment', disabled:0}};
        });
	},
});
