import frappe
import json
import os

def modify_shortcuts():
    """Removes specific 'Learn' shortcuts from their respective workspaces."""
    
    # Remove 'Learn Accounting' from the Accounting workspace
    _remove_shortcut_from_workspace(
        workspace_name="Accounting", 
        shortcut_to_remove="Learn Accounting"
    )

    # Remove 'Learn Sales Management' from the Selling workspace
    _remove_shortcut_from_workspace(
        workspace_name="Selling", 
        shortcut_to_remove="Learn Sales Management"
    )
    
    # Remove 'Learn Inventory Management' from the Stock workspace
    _remove_shortcut_from_workspace(
        workspace_name="Stock", 
        shortcut_to_remove="Learn Inventory Management"
    )
    
    # Remove 'Learn Manufacturing' from the Manufacturing workspace
    _remove_shortcut_from_workspace(
        workspace_name="Manufacturing", 
        shortcut_to_remove="Learn Manufacturing"
    )
    
    # Remove 'Learn Project Management' from the Projects workspace
    _remove_shortcut_from_workspace(
        workspace_name="Projects", 
        shortcut_to_remove="Learn Project Management"
    )
    
    # Remove 'Learn Procurement' from the Buying workspace
    _remove_shortcut_from_workspace(
        workspace_name="Buying", 
        shortcut_to_remove="Learn Procurement"
    )
    
    # Remove 'Documentation' from the lms workspace
    _remove_shortcut_from_workspace(
        workspace_name="LMS", 
        shortcut_to_remove="Documentation"
    )

def _remove_shortcut_from_workspace(workspace_name, shortcut_to_remove):
    """
    Generic helper function to remove a specific shortcut from a given workspace.
    
    :param workspace_name: The name of the Workspace (e.g., "Accounting").
    :param shortcut_to_remove: The name of the shortcut to remove (e.g., "Learn Accounting").
    """
    try:
        workspace = frappe.get_doc("Workspace", workspace_name)
    except frappe.DoesNotExistError:
        frappe.log_error(f"{workspace_name} workspace not found.", "Custom App Error")
        return

    # Skip if content is empty or not set
    if not workspace.get("content"):
        frappe.logger("Custom App").info(f"'{workspace_name}' workspace has no content, no changes made.")
        return

    try:
        content = json.loads(workspace.content)
    except (json.JSONDecodeError, TypeError):
        frappe.log_error(f"Failed to parse content for {workspace_name} workspace.", "Custom App Error")
        return

    # Use a list comprehension to build a new list without the target shortcut
    new_content = [
        item for item in content
        if not (
            item.get("type") == "shortcut"
            and item.get("data", {}).get("shortcut_name") == shortcut_to_remove
        )
    ]

    # Only save if a change was actually made
    if len(new_content) < len(content):
        workspace.content = json.dumps(new_content)
        workspace.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger("Custom App").info(f"Successfully removed '{shortcut_to_remove}' from {workspace_name} workspace.")
    else:
        frappe.logger("Custom App").info(f"'{shortcut_to_remove}' not found in {workspace_name} workspace, no changes made.")



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


def disable_email_footer():
    """
    Disables the standard email footer by setting disable_standard_email_footer=1 as a default value.
    This will prevent any default mail footer from showing up.
    """
    try:
        # Set the default value (not single value) to disable standard email footer
        frappe.db.set_default("disable_standard_email_footer", 1)
        frappe.db.commit()
        
        # Log success
        frappe.log_error(
            title="Custom Email Footer (corex_configs)",
            message="Successfully disabled standard email footer to remove ERPNext branding."
        )
 
    except Exception as e:
        # Log any potential errors
        frappe.log_error(
            title="Custom Email Footer Error (corex_configs)",
            message=f"Failed to disable standard email footer: {e}"
        )




def add_website_redirects_to_landing_page():
    """Adds a redirect from /apps to /landing in Website Settings."""
    website_settings = frappe.get_doc('Website Settings')

    # Check if the redirect already exists
    redirect_exists = False
    for redirect in website_settings.get('route_redirects'):
        if redirect.source == '/apps' and redirect.target == '/landing':
            redirect_exists = True
            break

    # If the redirect does not exist, add it
    if not redirect_exists:
        website_settings.append('route_redirects', {
            'source': '/apps',
            'target': '/landing'
        })
        website_settings.save(ignore_permissions=True)
        frappe.db.commit()
        print("Successfully added /apps to /landing redirect.")
    else:
        print("/apps to /landing redirect already exists.")