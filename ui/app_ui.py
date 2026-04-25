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

    # ===== LEFT SCROLLABLE AREA =====
    canvas = tk.Canvas(root, width=350)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    left_frame = tk.Frame(canvas)

    left_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=left_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="y")
    scrollbar.pack(side="left", fill="y")

    # ===== RIGHT SIDE =====
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ===== REPORTS =====
    report_frame = tk.LabelFrame(right_frame, text="Reports", padx=10, pady=10)
    report_frame.pack(fill="x")

    # ===== OUTPUT (SMALL & VISIBLE) =====
    output = tk.Text(right_frame, height=12)   # SMALL FIXED SIZE
    output.pack(fill="x", pady=10)

    def display_rows(rows):
        output.delete("1.0", tk.END)
        if not rows:
            output.insert(tk.END, "No data found\n")
            return
        for r in rows:
            output.insert(tk.END, str(dict(r)) + "\n")

    def create_section(title):
        frame = tk.LabelFrame(left_frame, text=title, padx=10, pady=10)
        frame.pack(fill="x", pady=5)
        return frame

    def add_field(frame, label):
        tk.Label(frame, text=label).pack(anchor="w")
        entry = tk.Entry(frame)
        entry.pack(fill="x")
        return entry

    # ===== SHIPMENT =====
    shipment_frame = create_section("Shipment")

    order = add_field(shipment_frame, "Order Ref")
    sender = add_field(shipment_frame, "Sender")
    receiver = add_field(shipment_frame, "Receiver")
    item = add_field(shipment_frame, "Item Description")
    hub = add_field(shipment_frame, "Warehouse ID")

    tk.Button(shipment_frame, text="Add Shipment",
              command=lambda: messagebox.showinfo(
                  "Success",
                  f"Shipment ID = {add_shipment(order.get(), sender.get(), receiver.get(), item.get(), safe_int(hub.get(),'Warehouse ID'))}"
              )).pack(pady=3)

    tk.Button(shipment_frame, text="View Shipments",
              command=lambda: display_rows(get_all_shipments())).pack(pady=3)

    # ===== DELIVERY =====
    delivery_frame = create_section("Delivery")

    ship_id = add_field(delivery_frame, "Shipment ID")
    drv_id = add_field(delivery_frame, "Driver ID")
    veh_id = add_field(delivery_frame, "Vehicle ID")
    route = add_field(delivery_frame, "Route Info")
    date = add_field(delivery_frame, "Date (YYYY-MM-DD)")

    tk.Button(delivery_frame, text="Assign Delivery",
              command=lambda: messagebox.showinfo(
                  "Success",
                  f"Delivery ID = {assign_delivery(safe_int(ship_id.get(),'Shipment ID'), safe_int(drv_id.get(),'Driver ID'), safe_int(veh_id.get(),'Vehicle ID'), route.get(), date.get())}"
              )).pack(pady=3)

    delivery_id = add_field(delivery_frame, "Delivery ID")
    new_status = add_field(delivery_frame, "New Delivery Status")

    tk.Button(delivery_frame, text="Update Delivery Status",
              command=lambda: update_delivery_status(
                  safe_int(delivery_id.get(),'Delivery ID'), new_status.get()
              )).pack(pady=3)

    # ===== INCIDENT =====
    incident_frame = create_section("Incident")

    i_ship = add_field(incident_frame, "Shipment ID")
    i_type = add_field(incident_frame, "Issue Type")
    i_desc = add_field(incident_frame, "Description")

    tk.Button(incident_frame, text="Add Incident",
              command=lambda: record_issue(
                  safe_int(i_ship.get(),'Shipment ID'), i_type.get(), i_desc.get()
              )).pack(pady=3)

    # ===== INVENTORY =====
    inv_frame = create_section("Inventory")

    iname = add_field(inv_frame, "Item Name")
    qty = add_field(inv_frame, "Quantity")
    reorder = add_field(inv_frame, "Reorder Level")
    hub2 = add_field(inv_frame, "Warehouse ID")

    tk.Button(inv_frame, text="Add Item",
              command=lambda: add_item(
                  iname.get(),
                  safe_int(qty.get(),'Quantity'),
                  safe_int(reorder.get(),'Reorder'),
                  safe_int(hub2.get(),'Warehouse ID')
              )).pack(pady=3)

    tk.Button(inv_frame, text="View Inventory",
              command=lambda: display_rows(view_inventory())).pack(pady=3)

    # ===== VEHICLE =====
    veh_frame = create_section("Vehicle")

    cap = add_field(veh_frame, "Capacity")
    stat = add_field(veh_frame, "Status")
    maint = add_field(veh_frame, "Maintenance Date")
    hub3 = add_field(veh_frame, "Hub ID")

    tk.Button(veh_frame, text="Add Vehicle",
              command=lambda: register_vehicle(
                  safe_int(cap.get(),'Capacity'),
                  stat.get(),
                  maint.get(),
                  safe_int(hub3.get(),'Hub ID')
              )).pack(pady=3)

    # ===== DRIVER =====
    drv_frame = create_section("Driver")

    dname = add_field(drv_frame, "Driver Name")
    lic = add_field(drv_frame, "License")
    shift = add_field(drv_frame, "Shift")

    tk.Button(drv_frame, text="Add Driver",
              command=lambda: register_driver(dname.get(), lic.get(), shift.get())
    ).pack(pady=3)

    # ===== PAYMENT =====
    pay_frame = create_section("Payment")

    p_ship = add_field(pay_frame, "Shipment ID")
    cost = add_field(pay_frame, "Transport Cost")
    extra = add_field(pay_frame, "Extra Charges")
    status = add_field(pay_frame, "Payment Status")

    tk.Button(pay_frame, text="Add Payment",
              command=lambda: add_payment(
                  safe_int(p_ship.get(),'Shipment ID'),
                  float(cost.get()),
                  float(extra.get()),
                  status.get()
              )).pack(pady=3)

    # ===== REPORT BUTTONS =====
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