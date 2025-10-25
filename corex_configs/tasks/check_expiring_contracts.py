import frappe
from frappe.utils import today, add_days, formatdate, getdate

def check_contracts():
    """
    This function is run daily by the scheduler.
    It finds customers with contracts expiring today or in 30 days and sends notifications.
    """
    today_str = today()
    thirty_days_from_now_str = add_days(today_str, 30)

    # Find all customers whose contract end date is either today or 30 days from now.
    expiring_customers = frappe.get_all(
        "Customer",
        filters={
            "corex_contract_end_date": ["in", [today_str, thirty_days_from_now_str]],
            "corex_is_contract_active": 1
        },
        fields=["name", "customer_name", "corex_contract_end_date", "account_manager"]
    )

    for customer in expiring_customers:
        # Convert to date objects for proper comparison
        end_date = getdate(customer.corex_contract_end_date)
        today_date = getdate(today_str)

        # Determine the reason for the notification
        if end_date == today_date:
            subject = f"Contract for {customer.customer_name} expires Today"
            message = (f"The contract for customer <strong>{customer.customer_name}</strong> "
                       f"expires today, {formatdate(customer.corex_contract_end_date)}.")
        else:
            # Contract is expiring in 30 days
            subject = f"Contract for {customer.customer_name} expires in 30 Days"
            message = (f"The contract for customer <strong>{customer.customer_name}</strong> "
                       f"is expiring in 30 days on {formatdate(customer.corex_contract_end_date)}.")

        # Send the notification to the assigned Account Manager
        if customer.account_manager:
            send_expiry_notification(
                customer_doc=customer,
                recipient_user=customer.account_manager,
                subject=subject,
                message=message
            )

def send_expiry_notification(customer_doc, recipient_user, subject, message):
    """Helper function to send both System Notification and Email."""
    
    # Create the in-system notification (bell icon)
    notification = frappe.new_doc("Notification Log")
    notification.for_user = recipient_user
    notification.document_type = "Customer"
    notification.document_name = customer_doc.name
    notification.subject = subject
    notification.insert(ignore_permissions=True)

    # Get the recipient's email address
    recipient_email = frappe.db.get_value("User", recipient_user, "email")

    # Send the email
    if recipient_email:
        frappe.sendmail(
            recipients=recipient_email,
            subject=subject,
            message=message,
            reference_doctype="Customer",
            reference_name=customer_doc.name
        )
    
    # Commit the changes to the database
    frappe.db.commit()