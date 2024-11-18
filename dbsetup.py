import sqlite3

def setup_database():
    """
    Set up the database with tables for Users, Orders, and Inventory.
    Populate the Inventory and Users tables with predefined data.
    """
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Create Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        items TEXT NOT NULL,  -- JSON string storing items, quantities, and prices
        total REAL NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('IN_PROGRESS', 'COMPLETED'))
    )
    """)

    # Create Inventory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL
    )
    """)

    # Insert predefined inventory items
    predefined_items = [
        ("Pizza", 12.99, 50),
        ("Pasta", 8.99, 40),
        ("Burger", 6.99, 30),
        ("Salad", 5.49, 25),
        ("Soda", 1.99, 100)
    ]
    try:
        cursor.executemany(
            "INSERT INTO Inventory (name, price, stock_quantity) VALUES (?, ?, ?)",
            predefined_items
        )
        print("Predefined menu items added to the Inventory table.")
    except sqlite3.IntegrityError:
        print("Predefined menu items already exist in the Inventory table.")

    # Insert predefined dummy users
    predefined_users = [
        ("admin_user", "admin_pass", "admin"),         # Admin user
        ("wait_staff1", "wait_pass", "wait_staff"),    # Wait staff user
        ("kitchen_staff1", "kitchen_pass", "kitchen_staff")  # Kitchen staff user
    ]
    try:
        cursor.executemany(
            "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
            predefined_users
        )
        print("Predefined users added to the Users table.")
    except sqlite3.IntegrityError:
        print("Predefined users already exist in the Users table.")

    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup completed.")
