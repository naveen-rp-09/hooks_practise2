import frappe
from frappe.utils import now
@frappe.whitelist()
def get_recent_todos():
    todos = frappe.get_list(
        "ToDo",
        fields=["name", "description", "owner"],
        order_by="creation desc",
        limit_page_length=5
    )
    records = []
    for todo in todos:
        email = frappe.db.get_value(
            "User",
            todo.owner,
            "email"
        )
        records.append({
            "name": todo.name,
            "description": todo.description,
            "owner": todo.owner,
            "email": email
        })
    return {
        "timestamp": now(),
        "records": records
    }
