from database.schema import build_tables
from logs.logger_setup import init_logger, write_log
from ui.app_ui import launch_ui

from security.auth import add_user, login_user
from services.inventory_service import add_warehouse
from datetime import datetime

import tkinter as tk
from tkinter import messagebox


def seed_basic_data():
    try:
        add_user("admin_root", "admin123", "admin")
        add_warehouse("Central Hub", "Kolkata")
        write_log("Seed data inserted successfully")
    except Exception as e:
        write_log(f"Seed data skipped: {str(e)}")


# LOGIN SCREEN
def login_screen():
    root = tk.Tk()
    root.title("Login - Northshore Logistics")

    tk.Label(root, text="Username").pack()
    username = tk.Entry(root)
    username.pack()

    tk.Label(root, text="Password").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def do_login():
        user = login_user(username.get(), password.get())

        if user:
            messagebox.showinfo("Success", "Login Successful")
            root.destroy()
            launch_ui()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(root, text="Login", command=do_login).pack(pady=5)

    root.mainloop()


def boot_run():
    init_logger()
    write_log("System boot started")

    build_tables()
    write_log("Tables verified / created")

    seed_basic_data()

    print("System Ready - Northshore Logistics")

    # START WITH LOGIN
    login_screen()

    write_log(f"System session ended at {datetime.now()}")


if __name__ == "__main__":
    boot_run()