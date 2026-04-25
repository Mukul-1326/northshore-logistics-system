from database.db_connection import open_link, fetch_cursor


def build_tables():
    conn = open_link()
    cur = fetch_cursor(conn)

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sys_users (
        usr_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usr_name TEXT NOT NULL UNIQUE,
        usr_pass TEXT NOT NULL,
        usr_role TEXT NOT NULL
    )
    """)

    # WAREHOUSE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS store_hub (
        hub_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hub_name TEXT NOT NULL,
        hub_location TEXT NOT NULL
    )
    """)

    # INVENTORY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        reorder_point INTEGER NOT NULL,
        hub_id INTEGER,
        last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hub_id) REFERENCES store_hub(hub_id)
    )
    """)

    # VEHICLES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fleet_units (
        veh_id INTEGER PRIMARY KEY AUTOINCREMENT,
        veh_capacity INTEGER NOT NULL,
        veh_status TEXT NOT NULL,
        maintenance_due TEXT,
        current_hub INTEGER,
        FOREIGN KEY (current_hub) REFERENCES store_hub(hub_id)
    )
    """)

    # DRIVERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS crew_drivers (
        drv_id INTEGER PRIMARY KEY AUTOINCREMENT,
        drv_name TEXT NOT NULL,
        license_no TEXT NOT NULL,
        shift_info TEXT,
        assigned_vehicle INTEGER,
        FOREIGN KEY (assigned_vehicle) REFERENCES fleet_units(veh_id)
    )
    """)

    # SHIPMENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cargo_moves (
        ship_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_ref TEXT NOT NULL,
        sender_info TEXT NOT NULL,
        receiver_info TEXT NOT NULL,
        item_desc TEXT,
        ship_status TEXT DEFAULT 'IN_TRANSIT',
        hub_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hub_id) REFERENCES store_hub(hub_id)
    )
    """)

    # DELIVERY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drop_records (
        delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER,
        drv_id INTEGER,
        veh_id INTEGER,
        route_info TEXT,
        delivery_date TEXT,
        delivery_status TEXT DEFAULT 'PENDING',
        FOREIGN KEY (ship_id) REFERENCES cargo_moves(ship_id),
        FOREIGN KEY (drv_id) REFERENCES crew_drivers(drv_id),
        FOREIGN KEY (veh_id) REFERENCES fleet_units(veh_id)
    )
    """)

    # INCIDENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issue_logs (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER,
        issue_type TEXT NOT NULL,
        issue_note TEXT,
        issue_time TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ship_id) REFERENCES cargo_moves(ship_id)
    )
    """)

    # FINANCIALS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payment_records (
        pay_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ship_id INTEGER,
        transport_cost REAL NOT NULL,
        extra_charges REAL,
        payment_status TEXT,
        payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ship_id) REFERENCES cargo_moves(ship_id)
    )
    """)

    # WAREHOUSE ACTIVITY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS hub_activity (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hub_id INTEGER,
        activity_type TEXT NOT NULL,
        item_id INTEGER,
        quantity INTEGER,
        activity_time TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hub_id) REFERENCES store_hub(hub_id),
        FOREIGN KEY (item_id) REFERENCES stock_items(item_id)
    )
    """)

    # DRIVER ROUTE HISTORY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS driver_routes (
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        drv_id INTEGER,
        route_details TEXT,
        route_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (drv_id) REFERENCES crew_drivers(drv_id)
    )
    """)

    # VEHICLE USAGE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_usage (
        usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
        veh_id INTEGER,
        usage_details TEXT,
        usage_date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (veh_id) REFERENCES fleet_units(veh_id)
    )
    """)

    # AUDIT
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_trail (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usr_id INTEGER,
        action TEXT,
        log_time TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usr_id) REFERENCES sys_users(usr_id)
    )
    """)

    conn.commit()
    conn.close()