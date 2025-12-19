// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	setup(frm) {
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
    refresh(frm){
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__('Change Gate'), function () {
                let dialog = new frappe.ui.Dialog({
                    title: __("Change Gate"),
                    size: "large",
                    fields: [
                        {
                            "label": "Source Airport",
                            "fieldname": "source_airport",
                            "fieldtype": "Link",
                            "options": "Airport",
                            "default": frm.doc.source_airport,
                            "read_only": 1
                        },
                        {
                            "label": "From Gate",
                            "fieldname": "from_gate",
                            "fieldtype": "Link",
                            "options": "Airport Gate",
                            "default": frm.doc.gate,
                            "read_only": 1
                        },
                        {
                            "label": "To Gate",
                            "fieldname": "to_gate",
                            "fieldtype": "Link",
                            "options": "Airport Gate",
                            "reqd": 1,
                            get_query: () => {
                                return {
                                    filters: {
                                        name: ["not in", frm.doc.gate]
                                    },
                                };
                            },
                        },
                    ]
                });
                dialog.set_primary_action(__("Change"), () => {
                    var args = dialog.get_values();
                    if (!args) return;
                    dialog.hide();
                    return frappe.call({
                        method: "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.process_change_gate",
                        args: {
                            "docname": frm.doc.name,
                            "to_gate": args.to_gate
                        },
                        freeze: true,
                        freeze_message: "Changing Gate...",
                        callback: function (r) {
                            frm.set_value("gate",r.message)
                            frm.save("Update");
                        }
                    });
                });
                dialog.show();
            }, __('Change'));
            frm.page.set_inner_btn_group_as_primary(__('Change'));
        }
    },
    source_airport(frm){
        frm.set_value("gate",undefined)
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

