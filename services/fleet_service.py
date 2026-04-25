from database.db_connection import open_link, fetch_cursor
from datetime import datetime
from security.auth import log_action
from security.encryption import simple_encrypt, simple_decrypt


# ADD VEHICLE
def register_vehicle(capacity, status, maintenance_due, hub_id, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO fleet_units (veh_capacity, veh_status, maintenance_due, current_hub)
        VALUES (?, ?, ?, ?)
        """, (capacity, status, maintenance_due, hub_id))

        conn.commit()

        log_action(user_id, f"Added vehicle at hub {hub_id}")

    finally:
        conn.close()


# UPDATE VEHICLE STATUS
def change_vehicle_status(veh_id, new_status, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        UPDATE fleet_units
        SET veh_status = ?
        WHERE veh_id = ?
        """, (new_status, veh_id))

        conn.commit()

        log_action(user_id, f"Updated vehicle {veh_id} status")

    finally:
        conn.close()


# VIEW VEHICLES
def list_vehicles():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT veh_id, veh_capacity, veh_status, maintenance_due, current_hub
        FROM fleet_units
        """)

        return cur.fetchall()

    finally:
        conn.close()


# ADD DRIVER (ENCRYPTED)
def register_driver(name, license_no, shift_info, vehicle_id=None, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        enc_name = simple_encrypt(name)
        enc_license = simple_encrypt(license_no)

        cur.execute("""
        INSERT INTO crew_drivers (drv_name, license_no, shift_info, assigned_vehicle)
        VALUES (?, ?, ?, ?)
        """, (enc_name, enc_license, shift_info, vehicle_id))

        conn.commit()

        log_action(user_id, f"Added driver")

    finally:
        conn.close()


# ASSIGN DRIVER TO VEHICLE
def assign_driver_vehicle(drv_id, veh_id, user_id=1):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        UPDATE crew_drivers
        SET assigned_vehicle = ?
        WHERE drv_id = ?
        """, (veh_id, drv_id))

        cur.execute("""
        UPDATE fleet_units
        SET veh_status = 'IN_USE'
        WHERE veh_id = ?
        """, (veh_id,))

        conn.commit()

        log_action(user_id, f"Assigned driver {drv_id} to vehicle {veh_id}")

    finally:
        conn.close()


# VIEW DRIVERS (DECRYPTED)
def list_drivers():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT drv_id, drv_name, license_no, shift_info, assigned_vehicle
        FROM crew_drivers
        """)

        rows = cur.fetchall()

        result = []
        for r in rows:
            row = dict(r)
            row["drv_name"] = simple_decrypt(row["drv_name"])
            row["license_no"] = simple_decrypt(row["license_no"])
            result.append(row)

        return result

    finally:
        conn.close()


# VEHICLE USAGE REPORT
def vehicle_usage_report():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT veh_id, usage_details, usage_date
        FROM vehicle_usage
        ORDER BY usage_date DESC
        """)

        return cur.fetchall()

    finally:
        conn.close()


# VEHICLE UTILISATION SUMMARY
def vehicle_utilisation_summary():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT veh_id, COUNT(*) as total_usage
        FROM vehicle_usage
        GROUP BY veh_id
        """)

        return cur.fetchall()

    finally:
        conn.close()


# DRIVER ROUTE HISTORY
def driver_route_history():
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT drv_id, route_details, route_date
        FROM driver_routes
        ORDER BY route_date DESC
        """)

        return cur.fetchall()

    finally:
        conn.close()