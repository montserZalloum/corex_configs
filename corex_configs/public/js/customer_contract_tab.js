frappe.ui.form.on('Customer', {
    corex_contract_end_date: function(frm) {
        validate_contract_dates(frm);
    },

    corex_contract_start_date: function(frm) {
        validate_contract_dates(frm);
    }
});

// A reusable function to handle the validation logic
let validate_contract_dates = function(frm) {
    
    // Only run the validation if both date fields have values
    if (frm.doc.corex_contract_start_date && frm.doc.corex_contract_end_date) {
        // Frappe's built-in date comparison function is very useful
        if (frappe.datetime.get_diff(frm.doc.corex_contract_end_date, frm.doc.corex_contract_start_date) < 0) {
            // If the difference is negative, the end date is before the start date
            frm.set_value('corex_contract_end_date', ''); // Clear the invalid date
            frappe.throw(__("Contract End Date cannot be before the Contract Start Date."));
        }
    }
};