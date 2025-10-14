import frappe
from frappe.desk.desktop import get_workspace_sidebar_items
from frappe import _


def get_corex_translation(text, language="en"):
    """
    Check if a translation exists for the given text and return the translated version.
    Returns the original text if no translation is found.
    """
    try:
        # Check if a translation exists in the Translation doctype
        translation_doc = frappe.db.exists("Translation", {
            "source_text": text, 
            "language": language
        })
        
        if translation_doc:
            # Get the translated text
            translated_text = frappe.db.get_value("Translation", translation_doc, "translated_text")
            return translated_text if translated_text else text
        else:
            return text
    except Exception as e:
        # Log error but don't break the flow
        frappe.log_error(f"Error checking translation for '{text}': {str(e)}")
        return text


def get_context(context):
    """
    Get only the desk sidebar items that the current user has permission to access.
    Uses Frappe's built-in permission system.
    Redirects to login if user is not authenticated or has no permissions.
    """
    
    # Check if user is logged in - use Frappe's standard method
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = f"/login?redirect-to={frappe.request.path}"
        frappe.throw(_("You need to be logged in to access this page."), frappe.PermissionError)
    
    frappe.log_error("CMS-LANDING: get_context - fetching user-specific desk sidebar items.")
    
    # Use Frappe's built-in function that handles all permission checks
    sidebar_data = get_workspace_sidebar_items()
    
    # Extract just the name and link for each permitted workspace
    sidebar_items = []
    for page in sidebar_data.get("pages", []):
        # Get the display name (prefer title, then label, then name)
        display_name = page.get("title") or page.get("label") or page.get("name")
        
        # Apply Corex translations to the display name
        translated_display_name = get_corex_translation(display_name)
        
        # Check if this is a CRM module and redirect to CRM lead
        if translated_display_name.lower() == "crm":
            # Get the last created kanban for lead
            try:
                last_kanban = frappe.get_last_doc("Kanban Board", filters={
                    "reference_doctype": "Lead"
                })
                if last_kanban:
                    workspace_link = f"/app/lead/view/kanban/{last_kanban.name}"
                else:
                    workspace_link = "/app/lead"
            except frappe.DoesNotExistError:
                # Fallback to lead list if no kanban exists
                workspace_link = "/app/lead"
        else:
            # Generate the correct workspace link based on public/private status
            if page.get("public"):
                workspace_link = f"/app/{frappe.utils.slug(display_name)}"
            else:
                workspace_link = f"/app/private/{frappe.utils.slug(display_name)}"

            if display_name.lower() == "raven":
                workspace_link = "/raven"
        
        sidebar_items.append({
            "name": translated_display_name,  # Use translated name
            "link": workspace_link,
            "icon_name": page.get("icon"),
            "is_public": page.get("public"),
            "is_hidden": page.get("is_hidden",0),
            "parent_page": page.get("parent_page"),
        })

    # Check if user has access to any sidebar items
    if not sidebar_items:
        frappe.local.flags.redirect_location = f"/login?redirect-to={frappe.request.path}"
        frappe.throw(_("You don't have permission to access any workspace."), frappe.PermissionError)

    context.sidebar_items = sidebar_items
    context.total_items = len(sidebar_items)
    context.user_info = {
        "name": frappe.session.user,
        "has_workspace_manager": sidebar_data.get("has_access", False)
    }
    return context 