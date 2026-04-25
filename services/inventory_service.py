from database.db_connection import open_link, fetch_cursor
from datetime import datetime
from security.auth import log_action
from security.encryption import simple_encrypt, simple_decrypt


# ADD INVENTORY ITEM
def add_item(item_name, qty, reorder_point, hub_id, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        enc_name = simple_encrypt(item_name)

        cur.execute("""
        INSERT INTO stock_items (item_name, quantity, reorder_point, hub_id)
        VALUES (?, ?, ?, ?)
        """, (enc_name, qty, reorder_point, hub_id))

        item_id = cur.lastrowid

        # Log RESTOCK
        cur.execute("""
        INSERT INTO hub_activity (hub_id, activity_type, item_id, quantity)
        VALUES (?, ?, ?, ?)
        """, (hub_id, "RESTOCK", item_id, qty))

        conn.commit()

        log_action(user_id, f"Added inventory item {item_id}")

    finally:
        conn.close()


# UPDATE STOCK
def update_stock(item_id, new_qty, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("SELECT quantity, hub_id FROM stock_items WHERE item_id = ?", (item_id,))
        data = cur.fetchone()

        if not data:
            return

        old_qty = data["quantity"]
        hub_id = data["hub_id"]

        if new_qty == old_qty:
            return

        change = new_qty - old_qty

        cur.execute("""
        UPDATE stock_items
        SET quantity = ?, last_updated = ?
        WHERE item_id = ?
        """, (new_qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item_id))

        activity_type = "INBOUND" if change > 0 else "OUTBOUND"

        cur.execute("""
        INSERT INTO hub_activity (hub_id, activity_type, item_id, quantity)
        VALUES (?, ?, ?, ?)
        """, (hub_id, activity_type, item_id, abs(change)))

        conn.commit()

        log_action(user_id, f"Updated stock for item {item_id}")

    finally:
        conn.close()


# TRANSFER BETWEEN WAREHOUSES
def transfer_item(item_id, target_hub, qty, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("SELECT quantity, hub_id, item_name, reorder_point FROM stock_items WHERE item_id = ?", (item_id,))
        data = cur.fetchone()

        if not data or data["quantity"] < qty:
            return

        source_hub = data["hub_id"]
        item_name = data["item_name"]
        reorder_point = data["reorder_point"]

        # Deduct from source
        cur.execute("""
        UPDATE stock_items
        SET quantity = quantity - ?
        WHERE item_id = ?
        """, (qty, item_id))

        # Add to target
        cur.execute("""
        INSERT INTO stock_items (item_name, quantity, reorder_point, hub_id)
        VALUES (?, ?, ?, ?)
        """, (item_name, qty, reorder_point, target_hub))

        # Log transfer
        cur.execute("""
        INSERT INTO hub_activity (hub_id, activity_type, item_id, quantity)
        VALUES (?, ?, ?, ?)
        """, (source_hub, "TRANSFER_OUT", item_id, qty))

        cur.execute("""
        INSERT INTO hub_activity (hub_id, activity_type, item_id, quantity)
        VALUES (?, ?, ?, ?)
        """, (target_hub, "TRANSFER_IN", item_id, qty))

        conn.commit()

        log_action(user_id, f"Transferred item {item_id} to hub {target_hub}")

    finally:
        conn.close()


# VIEW INVENTORY (DECRYPTED)
def view_inventory():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT item_id, item_name, quantity, reorder_point, hub_id
        FROM stock_items
        """)

        rows = cur.fetchall()

        # decrypt names
        result = []
        for r in rows:
            row = dict(r)
            row["item_name"] = simple_decrypt(row["item_name"])
            result.append(row)

        return result

    finally:
        conn.close()


# LOW STOCK REPORT
def low_stock_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT item_id, item_name, quantity, reorder_point
        FROM stock_items
        WHERE quantity <= reorder_point
        """)

        rows = cur.fetchall()

        result = []
        for r in rows:
            row = dict(r)
            row["item_name"] = simple_decrypt(row["item_name"])
            result.append(row)

        return result

    finally:
        conn.close()


# WAREHOUSE ACTIVITY REPORT
def warehouse_activity_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT hub_id, activity_type, item_id, quantity, activity_time
        FROM hub_activity
        ORDER BY activity_time DESC
        """)

        return cur.fetchall()

    finally:
        conn.close()

# ADD WAREHOUSE
def add_warehouse(name, location):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO store_hub (hub_name, hub_location)
        VALUES (?, ?)
        """, (name, location))

        conn.commit()

    finally:
        conn.close()