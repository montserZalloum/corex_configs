import frappe
import json

def modify_shortcuts():
    """Removes the 'Learn Accounting' shortcut from the Accounting workspace."""
    try:
        workspace = frappe.get_doc("Workspace", "Accounting")
    except frappe.DoesNotExistError:
        frappe.log_error("Accounting workspace not found.", "Custom App Error")
        return

    try:
        content = json.loads(workspace.get("content")) if workspace.get("content") else []
    except (json.JSONDecodeError, TypeError):
        # If content is malformed, we can't do anything.
        return

    shortcut_to_remove = "Learn Accounting"

    # Use a list comprehension to build a new list containing everything EXCEPT the target shortcut.
    # This is a safe and efficient way to remove items.
    new_content = [
        item for item in content
        if not (
            item.get("type") == "shortcut"
            and item.get("data", {}).get("shortcut_name") == shortcut_to_remove
        )
    ]

    # Only save if a change was actually made.
    if len(new_content) < len(content):
        workspace.content = json.dumps(new_content)
        workspace.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger("Custom App").info(f"Successfully removed '{shortcut_to_remove}' shortcut from Accounting workspace.")
    else:
        frappe.logger("Custom App").info(f"'{shortcut_to_remove}' shortcut not found in Accounting workspace, no changes made.")