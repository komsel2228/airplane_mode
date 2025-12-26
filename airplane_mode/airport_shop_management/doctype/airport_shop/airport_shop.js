// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
    setup(frm) {
        frm.set_query("shop_type", function() {
			return { filters: { enabled: 1}};
		});
	},
	onload(frm) {
        frappe.call({
            method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.get_terminal",
            args:{
                airport: frm.doc.airport || undefined
            },
            freeze: true,
            freeze_message: __("Get Terminal..."),
            callback: function(r) {
                frm.set_query("terminal", function() {
                    return { 
                        filters: { 
                            name: ["in", r.message],
                            is_group: 1
                    }};
                });
            }
        });

        frappe.call({
            method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.get_sub_terminal",
            args:{
                airport: frm.doc.airport || undefined,
                terminal: frm.doc.terminal || undefined
            },
            freeze: true,
            freeze_message: __("Get Sub Terminal..."),
            callback: function(r) {
                frm.set_query("sub_terminal", function() {
                    return { 
                        filters: {
                            parent_airport_terminal: frm.doc.terminal,
                            name: ["in", r.message],
                            is_group: 0
                    }};
                });
            }
        });
	},
    airport(frm) {
        frm.set_value("terminal",undefined)
        frm.set_value("sub_terminal",undefined)
        frappe.call({
            method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.get_terminal",
            args:{
                airport: frm.doc.airport
            },
            freeze: true,
            freeze_message: __("Get Terminal..."),
            callback: function(r) {
                frm.set_query("terminal", function() {
                    return { 
                        filters: { 
                            name: ["in", r.message],
                            is_group: 1
                    }};
                });
            }
        });
	},
    terminal(frm) {
        frm.set_value("sub_terminal",undefined)
        frappe.call({
            method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.get_sub_terminal",
            args:{
                airport: frm.doc.airport,
                terminal: frm.doc.terminal
            },
            freeze: true,
            freeze_message: __("Get Sub Terminal..."),
            callback: function(r) {
                frm.set_query("sub_terminal", function() {
                    return { 
                        filters: {
                            parent_airport_terminal: frm.doc.terminal,
                            name: ["in", r.message],
                            is_group: 0
                    }};
                });
            }
        });
	},
});
