# main.py

from usermgmt import User
from ordermgmt import OrderManagement
from inventory import InventoryManagement

# User Authentication
username = input("Enter username: ")
password = input("Enter password: ")
user = User(username)
user.authenticate(password)

# Role-based Menu
if user.authenticated:
    print(f"Welcome, {user.username}! You are logged in as {user.role}.")

    if user.role in ["admin", "wait_staff"]:
        order_mgmt = OrderManagement(user)
        while True:
            print("\n--- Order Management ---")
            print("1. Add Order")
            print("2. Display In-progress Orders")
            print("3. Complete Order")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                table_id = int(input("Enter table ID: "))
                items = []
                while True:
                    item_name = input("Enter item name (or 'done' to finish): ")
                    if item_name.lower() == "done":
                        break
                    item_price = float(input(f"Enter price for {item_name}: "))
                    items.append((item_name, item_price))
                order_mgmt.add_order(table_id, items)
            elif choice == "2":
                order_mgmt.display_orders()
            elif choice == "3":
                order_id_to_complete = int(input("Enter Order ID to mark as completed: "))
                order_mgmt.complete_order(order_id_to_complete)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    elif user.role == "kitchen_staff":
        inventory_mgmt = InventoryManagement(user)
        while True:
            print("\n--- Inventory Management ---")
            print("1. Add Inventory Item")
            print("2. Update Inventory Stock")
            print("3. Display Inventory")
            print("4. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                item_name = input("Enter item name: ")
                quantity = int(input(f"Enter quantity for {item_name}: "))
                inventory_mgmt.add_item(item_name, quantity)
            elif choice == "2":
                item_name = input("Enter item name to update: ")
                quantity = int(input("Enter quantity to add or subtract: "))
                inventory_mgmt.update_stock(item_name, quantity)
            elif choice == "3":
                inventory_mgmt.display_inventory()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
else:
    print("Access denied: Invalid credentials or insufficient permissions.")
