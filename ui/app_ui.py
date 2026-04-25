import tkinter as tk
from tkinter import messagebox
from services.shipment_service import add_payment, payment_report

from services.shipment_service import (
    add_shipment, get_all_shipments,
    assign_delivery, record_issue,
    update_delivery_status, shipment_status_report,
    delivery_report
)
from services.inventory_service import (
    add_item, view_inventory,
    warehouse_activity_report, low_stock_report
)
from services.fleet_service import (
    register_vehicle, register_driver,
    vehicle_usage_report, driver_route_history
)


def safe_int(value, field_name):
    if not value or not value.isdigit():
        raise ValueError(f"Enter valid {field_name}")
    return int(value)


def launch_ui():
    root = tk.Tk()
    root.title("Northshore Logistics System")
    root.geometry("1200x700")

    main = tk.Frame(root)
    main.pack(pady=10)

    output = tk.Text(root, height=10)
    output.pack(fill="x", padx=10, pady=10)

    def display_rows(rows):
        output.delete("1.0", tk.END)
        if not rows:
            output.insert(tk.END, "No data found\n")
            return
        for r in rows:
            output.insert(tk.END, str(dict(r)) + "\n")

    def create_section(parent, title):
        frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)
        frame.pack(side="left", padx=10)
        return frame

    def add_field(frame, label):
        tk.Label(frame, text=label).pack(anchor="w")
        entry = tk.Entry(frame)
        entry.pack()
        return entry

    # ================= ROW 1 =================
    row1 = tk.Frame(main)
    row1.pack()

    # SHIPMENT
    shipment_frame = create_section(row1, "Shipment")

    order = add_field(shipment_frame, "Order Ref")
    sender = add_field(shipment_frame, "Sender")
    receiver = add_field(shipment_frame, "Receiver")
    item = add_field(shipment_frame, "Item Description")
    hub = add_field(shipment_frame, "Warehouse ID")

    def add_ship():
        try:
            ship_id = add_shipment(
                order.get(), sender.get(), receiver.get(),
                item.get(), safe_int(hub.get(), "Warehouse ID")
            )
            messagebox.showinfo("Success", f"Shipment ID = {ship_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(shipment_frame, text="Add Shipment", command=add_ship).pack(pady=3)
    tk.Button(shipment_frame, text="View Shipments",
              command=lambda: display_rows(get_all_shipments())).pack(pady=3)

    # DELIVERY
    delivery_frame = create_section(row1, "Delivery")

    ship_id = add_field(delivery_frame, "Shipment ID")
    drv_id = add_field(delivery_frame, "Driver ID")
    veh_id = add_field(delivery_frame, "Vehicle ID")
    route = add_field(delivery_frame, "Route Info")
    date = add_field(delivery_frame, "Date (YYYY-MM-DD)")

    def assign_del():
        try:
            delivery_id = assign_delivery(
                safe_int(ship_id.get(), "Shipment ID"),
                safe_int(drv_id.get(), "Driver ID"),
                safe_int(veh_id.get(), "Vehicle ID"),
                route.get(), date.get()
            )
            messagebox.showinfo("Success", f"Delivery ID = {delivery_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(delivery_frame, text="Assign Delivery", command=assign_del).pack(pady=3)

    delivery_id = add_field(delivery_frame, "Delivery ID")
    new_status = add_field(delivery_frame, "New Delivery Status")

    def update_del():
        try:
            update_delivery_status(
                safe_int(delivery_id.get(), "Delivery ID"),
                new_status.get()
            )
            messagebox.showinfo("Updated", "Delivery Updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(delivery_frame, text="Update Delivery Status", command=update_del).pack(pady=3)

    # INCIDENT
    incident_frame = create_section(row1, "Incident")

    i_ship = add_field(incident_frame, "Shipment ID")
    i_type = add_field(incident_frame, "Issue Type")
    i_desc = add_field(incident_frame, "Description")

    def add_issue():
        try:
            record_issue(
                safe_int(i_ship.get(), "Shipment ID"),
                i_type.get(),
                i_desc.get()
            )
            messagebox.showinfo("Success", "Incident Added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(incident_frame, text="Add Incident", command=add_issue).pack(pady=3)

    # ================= ROW 2 =================
    row2 = tk.Frame(main)
    row2.pack(pady=10)

    # INVENTORY
    inv_frame = create_section(row2, "Inventory")

    iname = add_field(inv_frame, "Item Name")
    qty = add_field(inv_frame, "Quantity")
    reorder = add_field(inv_frame, "Reorder Level")
    hub2 = add_field(inv_frame, "Warehouse ID")

    tk.Button(inv_frame, text="Add Item",
              command=lambda: add_item(iname.get(),
                                       safe_int(qty.get(), "Quantity"),
                                       safe_int(reorder.get(), "Reorder"),
                                       safe_int(hub2.get(), "Warehouse ID"))
              ).pack(pady=3)

    tk.Button(inv_frame, text="View Inventory",
              command=lambda: display_rows(view_inventory())
              ).pack(pady=3)

    # VEHICLE
    veh_frame = create_section(row2, "Vehicle")

    cap = add_field(veh_frame, "Capacity")
    stat = add_field(veh_frame, "Status")
    maint = add_field(veh_frame, "Maintenance Date")
    hub3 = add_field(veh_frame, "Hub ID")

    tk.Button(veh_frame, text="Add Vehicle",
              command=lambda: register_vehicle(
                  safe_int(cap.get(), "Capacity"),
                  stat.get(), maint.get(),
                  safe_int(hub3.get(), "Hub ID")
              )).pack(pady=3)

    # DRIVER
    drv_frame = create_section(row2, "Driver")

    dname = add_field(drv_frame, "Driver Name")
    lic = add_field(drv_frame, "License")
    shift = add_field(drv_frame, "Shift")

    tk.Button(drv_frame, text="Add Driver",
              command=lambda: register_driver(dname.get(), lic.get(), shift.get())
              ).pack(pady=3)

    # PAYMENT (NEW SECTION)
    payment_frame = create_section(row2, "Payment")

    p_ship = add_field(payment_frame, "Shipment ID")
    cost = add_field(payment_frame, "Transport Cost")
    extra = add_field(payment_frame, "Extra Charges")
    status = add_field(payment_frame, "Payment Status (PAID/PENDING/FAILED)")

    def add_pay():
        try:
            add_payment(
                safe_int(p_ship.get(), "Shipment ID"),
                float(cost.get()),
                float(extra.get()),
                status.get()
            )
            messagebox.showinfo("Success", "Payment Added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(payment_frame, text="Add Payment", command=add_pay).pack(pady=3)

    # REPORTS
    report_frame = tk.LabelFrame(root, text="Reports", padx=10, pady=10)
    report_frame.pack(pady=10)

    tk.Button(report_frame, text="Shipment Summary",
              command=lambda: display_rows(shipment_status_report())).pack(pady=2)

    tk.Button(report_frame, text="Delivery Report",
              command=lambda: display_rows(delivery_report())).pack(pady=2)

    tk.Button(report_frame, text="Vehicle Usage",
              command=lambda: display_rows(vehicle_usage_report())).pack(pady=2)

    tk.Button(report_frame, text="Driver Routes",
              command=lambda: display_rows(driver_route_history())).pack(pady=2)

    tk.Button(report_frame, text="Warehouse Activity",
              command=lambda: display_rows(warehouse_activity_report())).pack(pady=2)

    tk.Button(report_frame, text="Low Stock",
              command=lambda: display_rows(low_stock_report())).pack(pady=2)

    tk.Button(report_frame, text="Payment Report",
              command=lambda: display_rows(payment_report())).pack(pady=2)

    root.mainloop()