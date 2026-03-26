import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def add_web_page_fields():
    """
    Add a 'Contracts' tab and related fields to the Customer doctype.
    """
    custom_fields = {
        "Web Page": [
            {
                "fieldname": "is_portal_use_standard_theme",
                "label": "Is Normal Theme",
                "description": "If checked, the page will be shown without a theme",
                "fieldtype": "Check",
                "default": "0",
                "insert_after": "module"
            }
        ]
    }

    create_custom_fields(custom_fields)