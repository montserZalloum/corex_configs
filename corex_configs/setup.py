import frappe
import os
import shutil

def create_landing_page():
    if not frappe.db.exists("Page", "landing"):
        frappe.get_doc({
            "doctype": "Page",
            "page_name": "landing",
            "module": "Corex Configs",
            "standard": 1,
            "title": "Landing"
        }).insert(ignore_permissions=True)
        frappe.db.commit()

def set_default_logo():
	"""Set default logo in Navbar Settings if not already set"""
	if not frappe.db.get_single_value("Navbar Settings", "app_logo"):
		frappe.db.set_single_value("Navbar Settings", "app_logo", "/assets/corex_configs/images/corex_logo.png")


def replace_default_logo():
    """
    Replaces the default ERPNext logo file with the one from the custom app.
    WARNING: This is not upgrade-safe and modifies files in the erpnext app.
    """
    try:
        # Get the full, absolute path to your custom logo
        source_logo_path = frappe.get_app_path('corex_configs', 'public', 'images', 'erpnext-logo.svg')
        
        # Get the full, absolute path to the default ERPNext logo
        destination_logo_path = frappe.get_app_path('erpnext', 'public', 'images', 'erpnext-logo.svg')

        # Check if your custom logo file actually exists
        if not os.path.exists(source_logo_path):
            print(f"ERROR: Source logo not found at {source_logo_path}")
            return

        print(f"Replacing default ERPNext logo with custom logo...")
        print(f"  Source: {source_logo_path}")
        print(f"  Destination: {destination_logo_path}")

        # Copy your file to the destination, overwriting the original
        shutil.copy2(source_logo_path, destination_logo_path)


		 # Get the full, absolute path to your custom logo
        source_logo_path = frappe.get_app_path('corex_configs', 'public', 'images', 'erpnext-favicon.svg')
        
        # Get the full, absolute path to the default ERPNext logo
        destination_logo_path = frappe.get_app_path('erpnext', 'public', 'images', 'erpnext-favicon.svg')

        # Check if your custom logo file actually exists
        if not os.path.exists(source_logo_path):
            print(f"ERROR: Source logo not found at {source_logo_path}")
            return

        # Get the full, absolute path to your custom logo
        shutil.copy2(source_logo_path, destination_logo_path)
        
        print("Default ERPNext logo replaced successfully.")

    except Exception as e:
        print(f"An error occurred while replacing the logo: {e}")