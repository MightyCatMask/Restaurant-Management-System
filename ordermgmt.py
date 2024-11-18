import sqlite3
import json


class OrderManagement:
    def __init__(self, user):
        self.user = user

    def add_order(self, table_id, items):
        """
        Add a new order to the database.
        :param table_id: ID of the table for the order.
        :param items: List of tuples containing item names and prices.
        """
        if self.user.role not in ["admin", "wait_staff"]:
            raise PermissionError("Only admins and wait staff can add orders.")

        # Calculate total amount
        total = sum(price for _, price in items)

        # Convert items to JSON for storage
        items_json = json.dumps(items)

        # Insert the order into the database
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Orders (table_id, items, total, status) VALUES (?, ?, ?, ?)",
            (table_id, items_json, total, "IN_PROGRESS")
        )
        conn.commit()
        conn.close()

    def display_orders(self, status="IN_PROGRESS"):
        """
        Fetch and display orders with the specified status.
        :param status: Status of the orders to fetch (e.g., "IN_PROGRESS" or "COMPLETED").
        :return: A list of orders with details.
        """
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, table_id, items, total, status FROM Orders WHERE status = ?",
            (status,)
        )
        orders = []
        for order_id, table_id, items_json, total, status in cursor.fetchall():
            # Convert JSON string back to list
            items = json.loads(items_json)
            orders.append({
                "order_id": order_id,
                "table_id": table_id,
                "items": items,
                "total": total,
                "status": status
            })
        conn.close()
        return orders

    def complete_order(self, order_id):
        """
        Mark an order as completed.
        :param order_id: ID of the order to be marked as completed.
        """
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM Orders WHERE id = ?",
            (order_id,)
        )
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Order ID {order_id} does not exist.")
        if result[0] == "COMPLETED":
            raise ValueError(f"Order ID {order_id} is already completed.")

        cursor.execute(
            "UPDATE Orders SET status = 'COMPLETED' WHERE id = ?",
            (order_id,)
        )
        conn.commit()
        conn.close()

