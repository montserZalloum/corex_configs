import frappe

def execute():
  """
  If 'Website Settings' exists and 'footer_powered' is blank,
  set it to 'Powered By Corex'.
  """
  # Check if the 'Website Settings' singleton document exists
  if not frappe.db.exists("Website Settings", "Website Settings"):
    return

  # Get the document
  doc = frappe.get_doc("Website Settings", "Website Settings")

  # Set the value if it's currently blank and save the document
  if not doc.footer_powered:
    doc.footer_powered = "Powered By Corex"
    # ignore_permissions is needed for patches to run during migrations
    doc.save(ignore_permissions=True)
    frappe.db.commit() # Commit the change to the database
    print("Default 'Powered By' footer has been set to 'Powered By Corex'.")

  if not doc.app_name or doc.app_name == "Frappe":
    doc.app_name = "Corex"
    doc.save(ignore_permissions=True)
    frappe.db.commit() # Commit the change to the database
    print("Default 'App Name' has been set to 'Corex'.")