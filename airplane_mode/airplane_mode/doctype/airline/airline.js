// Copyright (c) 2025, ndk and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airline', {
    refresh: function(frm) {
        frm.add_web_link(frm.doc.website, "Visit Website");
    }
});


// frappe.ui.form.on("Airline", {
// 	refresh(frm) {
//         if(frm.doc.website){
//             frm.add_custom_button("Visit Website"),()=>{
//                 window.open(frm.doc.website, '_blank');
//             }
//         }

// 	},
// });


// frappe.ui.form.on('Airline', {
//     refresh: function(frm) {
//         if (frm.doc.website) {
//             frm.add_custom_button(__('Visit Website'), function() {
//                 window.open(frm.doc.website, '_blank');
//             });
//         }
//     }
// });

