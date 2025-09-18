import frappe
import json
import os

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
        # If content is malformed, we can't do anything
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



def disable_update_notification():
    """
    Sets the 'disable_system_update_notification' checkbox in the 'System Settings'
    Single DocType by modifying its value directly in the database.
    """
    try:
        # Define the DocType and the field name
        doctype = "System Settings"
        field_name = "disable_system_update_notification"
        
        # Check the current value in the database.
        # Checkboxes are stored as 0 (unchecked) or 1 (checked).
        current_value = frappe.db.get_single_value(doctype, field_name)

        # Only update if it's not already checked (value is not 1)
        if current_value != 1:
            # frappe.db.set_single_value is the correct method for Single DocTypes
            # The value for a checked box is 1
            frappe.db.set_single_value(doctype, field_name, 1)
            
            # Commit the change to the database
            frappe.db.commit()

            # Optional: Log the success for debugging purposes
            frappe.log_error(
                title="Post-Migrate Hook (corex_configs)",
                message=f"Successfully checked '{field_name}' in '{doctype}'."
            )

    except Exception as e:
        # Log any potential errors, e.g., if the field name changes in a future version
        frappe.log_error(
            title="Post-Migrate Hook Error (corex_configs)",
            message=f"Failed to set '{field_name}' in '{doctype}'. Error: {e}"
        )

def disable_onboarding_module():
    """
    Disables the 'Onboarding Module' by setting the 'enable_onboarding' checkbox
    in the 'System Settings' Single DocType.
    """
    try:
        doctype = "System Settings"
        field_name = "enable_onboarding"

        # Check the current value. 1 means it's already enabled.
        current_value = frappe.db.get_single_value(doctype, field_name)

        # Only update if it's not already enabled
        if current_value != 0:
            # Set the value to 1 to disable (check the box)
            frappe.db.set_single_value(doctype, field_name, 0)
            frappe.db.commit()

            # Log the success for debugging
            frappe.log_error(
                title="Post-Migrate Hook (corex_configs)",
                message=f"Successfully disabled '{field_name}' in '{doctype}'."
            )

    except Exception as e:
        # Log any potential errors
        frappe.log_error(
            title="Post-Migrate Hook Error (corex_configs)",
            message=f"Failed to set '{field_name}' in '{doctype}'. Error: {e}"
        )