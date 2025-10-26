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
    """Adds redirects from /apps and /app to /app/landing in Website Settings."""
    website_settings = frappe.get_doc('Website Settings')

    # Define the redirects to add
    redirects_to_add = [
        {'source': '/apps', 'target': '/app/landing'},
        {'source': '/app', 'target': '/app/landing'}
    ]

    # Check and add each redirect if it doesn't exist
    for redirect_config in redirects_to_add:
        redirect_exists = False
        for redirect in website_settings.get('route_redirects'):
            if redirect.source == redirect_config['source'] and redirect.target == redirect_config['target']:
                redirect_exists = True
                break

        # If the redirect does not exist, add it
        if not redirect_exists:
            website_settings.append('route_redirects', redirect_config)
            print(f"Successfully added {redirect_config['source']} to {redirect_config['target']} redirect.")
        else:
            print(f"{redirect_config['source']} to {redirect_config['target']} redirect already exists.")

    # Save once after all redirects are added
    website_settings.save(ignore_permissions=True)
    frappe.db.commit()


def cleanup_gender_doctype():
    """
    Removes all Gender entries except 'Male' and 'Female'.
    This is run after migration to ensure only these two genders remain in the system.

    Uses an idempotency flag to prevent re-running if migration has already been executed.
    """
    try:
        # Step 1: Create the custom field if it doesn't exist
        _create_gender_cleanup_flag_field()

        # Step 2: Check if this migration has already been executed
        migration_flag = frappe.db.get_single_value("System Settings", "gender_cleanup_done")

        if migration_flag == 1:
            frappe.logger("corex_configs").info("Gender cleanup migration has already been executed. Skipping...")
            return

        # Step 3: Define the genders we want to keep
        allowed_genders = ["Male", "Female"]

        # Step 4: Get all existing Gender documents
        all_genders = frappe.get_all("Gender", fields=["name"])

        deleted_count = 0

        # Step 5: Delete all genders except Male and Female
        for gender in all_genders:
            if gender.name not in allowed_genders:
                try:
                    frappe.delete_doc("Gender", gender.name, force=True, ignore_permissions=True)
                    deleted_count += 1
                except Exception as delete_error:
                    frappe.log_error(
                        title="Gender Cleanup Error (corex_configs)",
                        message=f"Failed to delete gender '{gender.name}'. Error: {delete_error}"
                    )

        # Step 6: Commit the changes
        frappe.db.commit()

        # Step 7: Set the flag to indicate this migration has been executed
        frappe.db.set_single_value("System Settings", "gender_cleanup_done", 1)
        frappe.db.commit()

        frappe.log_error(
            title="Gender Cleanup Success (corex_configs)",
            message=f"Gender cleanup completed successfully. Deleted {deleted_count} gender entries."
        )

    except Exception as e:
        # Log any potential errors
        frappe.log_error(
            title="Gender Cleanup Error (corex_configs)",
            message=f"Failed to cleanup Gender DocType. Error: {e}"
        )


def _create_gender_cleanup_flag_field():
    """
    Helper function to create the custom field 'gender_cleanup_done' in System Settings
    if it doesn't already exist.
    """
    try:
        # Check if the custom field already exists
        field_exists = frappe.db.exists(
            "Custom Field",
            {
                "dt": "System Settings",
                "fieldname": "gender_cleanup_done"
            }
        )

        if not field_exists:
            # Create the custom field
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "System Settings",
                "fieldname": "gender_cleanup_done",
                "fieldtype": "Check",
                "label": "Gender Cleanup Done",
                "read_only": 1,
                "no_copy": 1,
                "hidden": 1,
                "insert_after": "enable_onboarding"
            })
            custom_field.insert(ignore_permissions=True)
            frappe.db.commit()
            frappe.logger("corex_configs").info("Custom field 'gender_cleanup_done' created successfully.")
        else:
            frappe.logger("corex_configs").info("Custom field 'gender_cleanup_done' already exists.")

    except Exception as e:
        frappe.log_error(
            title="Gender Cleanup Field Creation Error (corex_configs)",
            message=f"Failed to create custom field 'gender_cleanup_done'. Error: {e}"
        )


def get_portal_context(context):
    """
    Dynamically sets the body class based on a custom field in the "Web Page" DocType
    for the currently viewed page.
    """
    try:
        current_route = frappe.request.path.strip('/') or 'index'

        use_standard_theme = frappe.db.get_value(
            "Web Page",
            filters={"route": current_route},
            fieldname="is_portal_use_standard_theme"
        )

        if use_standard_theme == 1:
            theme_class = 'standard-theme'
        else:
            theme_class = 'corex-theme'

        existing_classes = context.get('body_class', '')
        context['body_class'] = f'{existing_classes} {theme_class}'.strip()

    except Exception as e:
        frappe.log_error(f"Error in get_portal_context: {e}", "Portal Context Error")
        # في حالة حدوث أي خطأ، يتم تطبيق كلاس احتياطي
        existing_classes = context.get('body_class', 'corex-theme')
        context['body_class'] = f'{existing_classes} fallback-theme'.strip()

    return context