import sqlite3


class InventoryManagement:
    def __init__(self, user):
        """
        Initialize InventoryManagement with the current user.
        :param user: The logged-in user object.
        """
        self.user = user

    def add_item(self, name, quantity):
        """
        Add a new inventory item to the database.
        :param name: Name of the item.
        :param quantity: Initial stock quantity of the item.
        """
        if self.user.role not in ["admin", "kitchen_staff"]:
            raise PermissionError("Only admins and kitchen staff can add inventory items.")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Inventory (name, stock_quantity) VALUES (?, ?)",
                (name, quantity)
            )
            conn.commit()
            print(f"Inventory item '{name}' added with quantity {quantity}.")
        except sqlite3.IntegrityError:
            print(f"Error: Item '{name}' already exists in the inventory.")
        finally:
            conn.close()

    def update_stock(self, name, quantity):
        """
        Update the stock of an existing inventory item.
        :param name: Name of the inventory item.
        :param quantity: Quantity to add or subtract.
        """
        if self.user.role not in ["admin", "kitchen_staff"]:
            raise PermissionError("Only admins and kitchen staff can update inventory.")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stock_quantity FROM Inventory WHERE name = ?",
            (name,)
        )
        result = cursor.fetchone()

        if result:
            # Item exists, update its stock
            new_quantity = result[0] + quantity
            if new_quantity < 0:
                print(f"Error: Cannot reduce stock below zero for item '{name}'.")
            else:
                cursor.execute(
                    "UPDATE Inventory SET stock_quantity = ? WHERE name = ?",
                    (new_quantity, name)
                )
                conn.commit()
                print(f"Inventory for '{name}' updated by {quantity}. New quantity: {new_quantity}.")
        else:
            print(f"Error: Item '{name}' does not exist in the inventory.")

        conn.close()

    def display_inventory(self):
        """
        Display the current inventory with item names and stock quantities.
        """
        if self.user.role not in ["admin", "kitchen_staff"]:
            raise PermissionError("Only admins and kitchen staff can view inventory.")

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock_quantity FROM Inventory")
        items = cursor.fetchall()

        print("\nCurrent Inventory:")
        print("------------------")
        for name, stock_quantity in items:
            print(f"{name}: {stock_quantity} units")

        conn.close()
