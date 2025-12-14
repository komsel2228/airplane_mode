// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	setup(frm) {
        frm.set_query("gate", function() {
			return { filters: { airport: frm.doc.source_airport } };
		});
        frm.set_query('airplane_crew', 'airplane_flight_crews',(doc, cdt, cdn) => {
            return {
                "filters": {
                    "airline": frm.doc.airline,
                    "is_on_duty": 0,
                    "is_on_leave": 0
                }
            };
		});
	},
    source_airport(frm){
        frm.set_value("gate",undefined)
        frm.set_query("gate", function() {
			return { filters: { airport: frm.doc.source_airport } };
		});
    },
    airplane(frm) {
        frm.clear_table("airplane_flight_crews")
        frm.refresh_field("airplane_flight_crews");
        frm.set_query('airplane_crew', 'airplane_flight_crews',(doc, cdt, cdn) => {
            return {
                "filters": {
                    "airline": frm.doc.airline,
                    "is_on_duty": 0,
                    "is_on_leave": 0
                }
            };
		});
	}
});

