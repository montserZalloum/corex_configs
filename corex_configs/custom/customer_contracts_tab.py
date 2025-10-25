import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_customer_contract_fields():
    """
    Add a 'Contracts' tab and related fields to the Customer doctype.
    """
    custom_fields_for_customer = {
        "Customer": [
            {
                "fieldname": "corex_contracts_tab",
                "label": "Contracts",
                "fieldtype": "Tab Break",
                "insert_after": "loyalty_program_tier"
            },
            {
                "fieldname": "corex_contract_attachment",
                "label": "Contract Attachment",
                "fieldtype": "Attach",
                "insert_after": "corex_contracts_tab"
            },
            {
                "fieldname": "corex_contract_start_date",
                "label": "Contract Start Date",
                "fieldtype": "Date",
                "insert_after": "corex_contract_attachment"
            },
            {
                "fieldname": "corex_contract_end_date",
                "label": "Contract End Date",
                "fieldtype": "Date",
                "insert_after": "corex_contract_start_date"
            },
            {
                "fieldname": "corex_is_contract_active",
                "label": "Is Contract Active",
                "fieldtype": "Check",
                "default": "0",
                "insert_after": "corex_contract_end_date"
            }
        ]
    }

    create_custom_fields(custom_fields_for_customer)