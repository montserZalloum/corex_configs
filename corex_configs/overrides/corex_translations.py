# in file: /corex_app/corex_app/install.py

import frappe

def setup_corex_translations():
  """
  Creates custom translations for rebranding if they don't already exist.
  This function is idempotent and safe to run multiple times.
  """
  # Define a list of translations to create
  # Format: (Source Text, Translated Text)
  translations = [
    # ("ERPNext Settings", "Corex Settings"),
    # ("ERPNext Integrations", "Corex Integrations"),
    ("Frappe Light", "Corex Light"),
    ("Timeless Night", "Corex Night"),
    ("Activity", "Timeline"),
  ]

  # Set the language for which you want to add translations
  language = "en" # Or any other language code

  print("Checking for and creating custom Corex translations...")

  for source_text, translated_text in translations:
    # Check if a translation for this source text already exists for the language
    if not frappe.db.exists("Translation", {"source_text": source_text, "language": language}):
      # If it doesn't exist, create a new Translation document
      doc = frappe.new_doc("Translation")
      doc.language = language
      doc.source_text = source_text
      doc.translated_text = translated_text
      doc.insert(ignore_permissions=True) # ignore_permissions is needed for migration hooks
      print(f"Created translation for '{source_text}' -> '{translated_text}'")
    else:
      print(f"Translation for '{source_text}' already exists. Skipping.")

  # Commit the changes to the database
  frappe.db.commit()