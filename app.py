from flask import Flask, render_template, request, redirect, url_for, flash
from usermgmt import User
from ordermgmt import OrderManagement
from inventory import InventoryManagement
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management and flash messages

# Global variables to store the current user and management instances
current_user = None
order_mgmt = None
inventory_mgmt = None


@app.route("/", methods=["GET", "POST"])
def login():
    global current_user, order_mgmt, inventory_mgmt

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate user
        current_user = User(username)
        current_user.authenticate(password)

        if current_user.authenticated:
            flash(f"Welcome, {current_user.username}! You are logged in as {current_user.role}.", "success")

            # Initialize management instances based on role
            if current_user.role in ["admin", "wait_staff"]:
                order_mgmt = OrderManagement(current_user)
            if current_user.role in ["admin", "kitchen_staff"]:
                inventory_mgmt = InventoryManagement(current_user)

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "error")

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if not current_user or not current_user.authenticated:
        return redirect(url_for("login"))

    return render_template("dashboard.html", role=current_user.role)


@app.route("/add_order", methods=["GET", "POST"])
def add_order():
    if not current_user or current_user.role not in ["admin", "wait_staff"]:
        flash("Permission denied", "error")
        return redirect(url_for("dashboard"))

    # Fetch menu items
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, stock_quantity FROM Inventory WHERE stock_quantity > 0")
    menu_items = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        try:
            # Get table ID and form data
            table_id = int(request.form.get("table_id"))
            selected_items = request.form.getlist("item_name")
            quantities = request.form.getlist("quantity")

            # Debugging
            print(f"Menu Items: {menu_items}")
            print(f"Selected Items: {selected_items}")
            print(f"Quantities: {quantities}")

            # Prepare order
            items = []
            total_price = 0
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()

            for item_name, quantity in zip(selected_items, quantities):
                quantity = int(quantity)
                if quantity <= 0:
                    continue

                # Fetch price and stock
                cursor.execute("SELECT price, stock_quantity FROM Inventory WHERE name = ?", (item_name,))
                result = cursor.fetchone()
                if not result or result[1] < quantity:
                    flash(f"Not enough stock for item: {item_name}", "error")
                    continue

                price_per_unit = result[0]
                total_price += price_per_unit * quantity
                items.append((item_name, price_per_unit, quantity))

                # Update stock
                cursor.execute(
                    "UPDATE Inventory SET stock_quantity = stock_quantity - ? WHERE name = ?",
                    (quantity, item_name)
                )

            if items:
                # Add order to database
                items_json = json.dumps(items)
                cursor.execute(
                    "INSERT INTO Orders (table_id, items, total, status) VALUES (?, ?, ?, ?)",
                    (table_id, items_json, total_price, "IN_PROGRESS")
                )
                conn.commit()
                flash("Order added successfully!", "success")
            else:
                flash("No valid items added to the order.", "error")
        except Exception as e:
            flash(f"Error adding order: {e}", "error")
            print(f"Error: {e}")  # Debugging
        finally:
            conn.close()

        return redirect(url_for("view_orders", status="in_progress"))

    return render_template("add_order.html", menu_items=menu_items)


@app.route('/view_orders/<status>')
def view_orders(status):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    try:
        # Fetch orders with the specified status
        cursor.execute("SELECT * FROM Orders WHERE status = ?", (status,))
        orders = cursor.fetchall()  # Fetch all rows

        # Debugging: Print fetched orders
        print(f"Orders fetched for status '{status}': {orders}")

        # Add a hardcoded order for demonstration
        hardcoded_order = (0, 1, '[{"item_name": "Pizza", "quantity": 1}]', 10.00, "IN_PROGRESS")
        if status.lower() == "in_progress":
            orders.append(hardcoded_order)

        # Pass orders and status to the template
        return render_template('view_orders.html', orders=orders, status=status)
    except Exception as e:
        # Flash error if fetching fails
        flash(f"Error fetching orders: {e}", "error")
        print(f"Error: {e}")  # Debugging output
        return redirect(url_for('dashboard'))
    finally:
        conn.close()

@app.route("/complete_order/<int:order_id>")
def complete_order(order_id):
    if not current_user or current_user.role not in ["admin", "wait_staff"]:
        flash("Permission denied", "error")
        return redirect(url_for("dashboard"))

    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        # Update the order's status to "COMPLETED"
        cursor.execute("UPDATE Orders SET status = 'COMPLETED' WHERE id = ?", (order_id,))
        conn.commit()

        flash(f"Order {order_id} marked as completed.", "success")
    except Exception as e:
        flash(f"Error completing order: {e}", "error")
        print(f"Error: {e}")  # Debugging
    finally:
        conn.close()

    return redirect(url_for("view_orders", status="in_progress"))


@app.route("/update_inventory", methods=["GET", "POST"])
def update_inventory():
    if not current_user or current_user.role not in ["admin", "kitchen_staff"]:
        flash("Permission denied", "error")
        return redirect(url_for("dashboard"))

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Fetch existing inventory items for updating quantities
    cursor.execute("SELECT name, stock_quantity, price FROM Inventory")
    inventory_items = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        try:
            action = request.form.get("action")
            if action == "update":
                # Update quantities of existing items
                item_name = request.form.get("item_name")
                quantity_change = int(request.form.get("quantity"))
                conn = sqlite3.connect('restaurant.db')
                cursor = conn.cursor()

                # Check if the item exists
                cursor.execute(
                    "SELECT stock_quantity FROM Inventory WHERE name = ?",
                    (item_name,)
                )
                result = cursor.fetchone()
                if not result:
                    flash(f"Item '{item_name}' does not exist.", "error")
                else:
                    # Update the stock
                    cursor.execute(
                        "UPDATE Inventory SET stock_quantity = stock_quantity + ? WHERE name = ?",
                        (quantity_change, item_name)
                    )
                    flash(f"Updated '{item_name}' quantity by {quantity_change}.", "success")
                conn.commit()
                conn.close()

            elif action == "add":
                # Add a new item to the inventory
                item_name = request.form.get("new_item_name")
                price = float(request.form.get("price"))
                quantity = int(request.form.get("new_quantity"))

                conn = sqlite3.connect('restaurant.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Inventory (name, price, stock_quantity) VALUES (?, ?, ?)",
                    (item_name, price, quantity)
                )
                conn.commit()
                conn.close()
                flash(f"Added new item '{item_name}' to inventory.", "success")
        except Exception as e:
            flash(f"Error updating inventory: {e}", "error")
        finally:
            return redirect(url_for("update_inventory"))

    return render_template("update_inventory.html", inventory_items=inventory_items)

@app.route("/logout")
def logout():
    global current_user
    current_user = None  # Clear the current user
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
