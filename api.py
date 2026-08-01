import frappe
def custom_logic(doc, method):
    frappe.msgprint("Hook executed!")
@frappe.whitelist()
def purchase_order_api():

    purchase_order = frappe.qb.DocType("Purchase Order")
    supplier = frappe.qb.DocType("Supplier")
    query = (
        frappe.qb
        .from_(purchase_order)
        .inner_join(supplier)
        .on(purchase_order.supplier == supplier.name)
        .select(
            purchase_order.name,
            purchase_order.purchase_date,
            purchase_order.total_amount,
            purchase_order.status,
            supplier.supplier_name
        )
         .where(purchase_order.docstatus == 0)
    )
    results = query.run(as_dict=True)
    
    if results:
        doc = frappe.get_doc("Purchase Order", results[0]["name"])
        doc.remarks = "Updated using Document API"
        doc.save()

    for row in results:
        frappe.db.set_value(
            "Purchase Order",
            row["name"],
            "remarks",
            "Bulk Updated using Database API"
        )

    return results
