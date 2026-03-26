import frappe


def powered_by_footer(doc, method):
    """
    Before save hook for Website Settings.
    If the footer_powered field is blank, set it to 'Powered By Corex'.
    """
    if not doc.footer_powered:
        doc.footer_powered = "Powered By Corex"

def app_name(doc, method):
    """
    Before save hook for Website Settings.
    If the app_name field is blank or 'Frappe', set it to 'Corex'.
    """
    if not doc.app_name or doc.app_name == "Frappe":
        doc.app_name = "Corex"

def apply_website_settings():
    """
    Apply custom website settings after migration.
    Updates the Website Settings doctype with Corex branding.
    """
    try:
        website_settings = frappe.get_doc("Website Settings")
        
        # Apply the footer_powered setting
        if not website_settings.footer_powered:
            website_settings.footer_powered = "Powered By Corex"
        
        # Apply the app_name setting
        if not website_settings.app_name or website_settings.app_name == "Frappe":
            website_settings.app_name = "Corex"
        
        # Save the changes
        website_settings.save()
        frappe.db.commit()
        
        print("Website Settings updated successfully")
    except Exception as e:
        print(f"Error updating Website Settings: {str(e)}")