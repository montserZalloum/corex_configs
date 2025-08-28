import frappe

def execute():
    # Check if Property Setter already exists
    if not frappe.db.exists("Property Setter", {
        "doc_type": "Lead",
        "property": "default_view"
    }):
        doc = frappe.get_doc({
            "doctype": "Property Setter",
            "doctype_or_field": "DocType",
            "doc_type": "Lead",
            "property": "default_view",
            "property_type": "Select",
            "value": "Kanban",
            "module": "CRM"  # Add the module field
        })
        doc.insert(ignore_permissions=True)
        frappe.clear_cache()
    else:
        # Update existing Property Setter if it exists
        property_setter = frappe.get_doc("Property Setter", {
            "doc_type": "Lead",
            "property": "default_view"
        })
        property_setter.value = "Kanban"
        property_setter.save(ignore_permissions=True)
        frappe.clear_cache()
