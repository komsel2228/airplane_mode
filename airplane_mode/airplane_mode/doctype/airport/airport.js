// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport", {
	setup(frm) {
        frm.set_query('terminal', 'terminal_details',(doc, cdt, cdn) => {
            return {
                "filters": {
                    "is_group": 1,
                    "name": ["not in", "All Airport Terminal"]
                }
            };
		});

        frm.set_query('sub_terminal', 'terminal_details',(doc, cdt, cdn) => {
            let row = locals[cdt][cdn];
            return {
                "filters": {
                    "is_group": 0,
                    "parent_airport_terminal": row.terminal
                }
            };
		});
	},
    refresh(frm){
        frm.set_query('sub_terminal', 'terminal_details',(doc, cdt, cdn) => {
            let row = locals[cdt][cdn];
            return {
                "filters": {
                    "is_group": 0,
                    "parent_airport_terminal": row.terminal
                }
            };
		});
    }
});
