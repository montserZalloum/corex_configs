import os
import frappe
import openpyxl


def setup_corex_translations():
	"""
	Creates custom translations for rebranding if they don't already exist.
	This function is idempotent and safe to run multiple times.
	"""
	translations = [
		("Frappe Light", "Corex Light"),
		("Timeless Night", "Corex Night"),
		("Activity", "Timeline"),
	]

	language = "en"
	print("Checking for and creating custom Corex translations...")

	for source_text, translated_text in translations:
		if not frappe.db.exists("Translation", {"source_text": source_text, "language": language}):
			doc = frappe.new_doc("Translation")
			doc.language = language
			doc.source_text = source_text
			doc.translated_text = translated_text
			doc.insert(ignore_permissions=True)
			print(f"  Created: '{source_text}' -> '{translated_text}'")
		else:
			print(f"  Skipped (exists): '{source_text}'")

	frappe.db.commit()


def import_frappe_translations():
	"""
	Import translations from frappe_translations.xlsx into the Translation doctype.
	Skips if already imported (tracked via file mtime in tabSingles).
	Re-imports only when the xlsx file changes.
	"""
	config_key = "frappe_translations_xlsx_mtime"
	xlsx_path = os.path.join(os.path.dirname(__file__), "..", "custom", "frappe_translations.xlsx")
	xlsx_path = os.path.normpath(xlsx_path)

	if not os.path.exists(xlsx_path):
		print(f"Translation file not found: {xlsx_path}")
		return

	file_mtime = str(os.path.getmtime(xlsx_path))

	last_imported_mtime = frappe.db.sql(
		"SELECT value FROM tabSingles WHERE doctype='System Settings' AND field=%s",
		config_key,
	)
	last_imported_mtime = last_imported_mtime[0][0] if last_imported_mtime else None

	if last_imported_mtime == file_mtime:
		print("frappe_translations.xlsx already imported (unchanged). Skipping.")
		return

	print("Importing translations from frappe_translations.xlsx...")

	wb = openpyxl.load_workbook(xlsx_path, read_only=True)
	ws = wb.active

	created = 0
	updated = 0
	skipped = 0

	for row in ws.iter_rows(min_row=2, values_only=True):
		if not row or len(row) < 3:
			continue

		language, source_text, translated_text = row[0], row[1], row[2]

		if not language or not source_text or not translated_text:
			continue

		language = str(language).strip()
		source_text = str(source_text).strip()
		translated_text = str(translated_text).strip()

		if language != "ar":
			continue

		existing = frappe.db.get_value(
			"Translation",
			{"source_text": source_text, "language": language},
			["name", "translated_text"],
			as_dict=True,
		)

		if not existing:
			doc = frappe.new_doc("Translation")
			doc.language = language
			doc.source_text = source_text
			doc.translated_text = translated_text
			doc.insert(ignore_permissions=True)
			created += 1
		elif existing.translated_text != translated_text:
			frappe.db.set_value("Translation", existing.name, "translated_text", translated_text)
			updated += 1
		else:
			skipped += 1

	wb.close()

	if last_imported_mtime is not None:
		frappe.db.sql(
			"UPDATE tabSingles SET value=%s WHERE doctype='System Settings' AND field=%s",
			(file_mtime, config_key),
		)
	else:
		frappe.db.sql(
			"INSERT INTO tabSingles (doctype, field, value) VALUES ('System Settings', %s, %s)",
			(config_key, file_mtime),
		)

	frappe.db.commit()
	frappe.clear_cache()

	print(f"Done. Created: {created}, Updated: {updated}, Skipped (unchanged): {skipped}")
