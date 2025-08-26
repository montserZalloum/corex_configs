import frappe


def set_default_logo():
	"""Set default logo in Navbar Settings"""
	frappe.db.set_single_value("Navbar Settings", "app_logo", "/assets/corex_configs/images/corex_logo.ico")
