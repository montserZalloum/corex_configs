import frappe

def on_login_redirect(login_manager):
    if login_manager.info.user_type == "System User":
        frappe.cache.hset("redirect_after_login", login_manager.user, "/landing")