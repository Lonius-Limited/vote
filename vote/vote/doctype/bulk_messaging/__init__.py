import frappe

def send_message():
    return frappe.get_doc("Bulk Messaging","MSG00007").send_messages()