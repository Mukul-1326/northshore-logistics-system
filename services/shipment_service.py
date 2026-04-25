from database.db_connection import open_link, fetch_cursor

VALID_SHIPMENT_STATUS = ["IN_TRANSIT", "DELIVERED", "DELAYED", "RETURNED"]
VALID_DELIVERY_STATUS = ["PENDING", "ASSIGNED", "DELIVERED"]


def add_shipment(order_ref, sender, receiver, item_desc, hub_id):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO cargo_moves (order_ref, sender_info, receiver_info, item_desc, ship_status, hub_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (order_ref, sender, receiver, item_desc, "IN_TRANSIT", hub_id))

        ship_id = cur.lastrowid
        conn.commit()
        return ship_id

    finally:
        conn.close()


def assign_delivery(ship_id, drv_id, veh_id, route_info, delivery_date):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO drop_records (ship_id, drv_id, veh_id, route_info, delivery_date, delivery_status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (ship_id, drv_id, veh_id, route_info, delivery_date, "ASSIGNED"))

        delivery_id = cur.lastrowid

        cur.execute("""
        INSERT INTO driver_routes (drv_id, route_details)
        VALUES (?, ?)
        """, (drv_id, route_info))

        cur.execute("""
        INSERT INTO vehicle_usage (veh_id, usage_details)
        VALUES (?, ?)
        """, (veh_id, f"Shipment {ship_id}"))

        conn.commit()
        return delivery_id

    finally:
        conn.close()


def update_status(ship_id, new_status):
    if new_status not in VALID_SHIPMENT_STATUS:
        raise ValueError("Invalid Shipment Status")

    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        UPDATE cargo_moves
        SET ship_status = ?
        WHERE ship_id = ?
        """, (new_status, ship_id))

        conn.commit()

    finally:
        conn.close()


def update_delivery_status(delivery_id, new_status):
    if new_status not in VALID_DELIVERY_STATUS:
        raise ValueError("Invalid Delivery Status")

    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        UPDATE drop_records
        SET delivery_status = ?
        WHERE delivery_id = ?
        """, (new_status, delivery_id))

        conn.commit()

    finally:
        conn.close()


def record_issue(ship_id, issue_type, issue_note):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO issue_logs (ship_id, issue_type, issue_note)
        VALUES (?, ?, ?)
        """, (ship_id, issue_type, issue_note))

        conn.commit()

    finally:
        conn.close()


def add_payment(ship_id, cost, extra, status):
    if status not in ["PAID", "PENDING", "FAILED"]:
        raise ValueError("Invalid Payment Status")

    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        # check shipment exists
        cur.execute("SELECT ship_id FROM cargo_moves WHERE ship_id = ?", (ship_id,))
        if not cur.fetchone():
            raise ValueError("Shipment does not exist")

        cur.execute("""
        INSERT INTO payment_records (ship_id, transport_cost, extra_charges, payment_status)
        VALUES (?, ?, ?, ?)
        """, (ship_id, cost, extra, status))

        conn.commit()

    finally:
        conn.close()


def get_all_shipments():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT ship_id, order_ref, sender_info, receiver_info, item_desc, ship_status
        FROM cargo_moves
        """)

        return cur.fetchall()

    finally:
        conn.close()


def get_shipments_by_status(status):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT ship_id, order_ref, sender_info, receiver_info, item_desc, ship_status
        FROM cargo_moves
        WHERE ship_status = ?
        """, (status,))

        return cur.fetchall()

    finally:
        conn.close()


def delivery_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT delivery_id, ship_id, delivery_status, delivery_date
        FROM drop_records
        """)

        return cur.fetchall()

    finally:
        conn.close()


def shipment_status_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT ship_status, COUNT(*) as total
        FROM cargo_moves
        GROUP BY ship_status
        """)

        return cur.fetchall()

    finally:
        conn.close()

def payment_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT ship_id, transport_cost, extra_charges, payment_status, payment_date
        FROM payment_records
        """)

        return cur.fetchall()

    finally:
        conn.close()