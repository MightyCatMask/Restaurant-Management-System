# Restaurant-Management-System
for college coursework


Overview

This is a simple Restaurant Management System built using Flask. It provides role-based access for managing orders and inventory in a restaurant. The system includes functionalities like adding orders, viewing in-progress and completed orders, and updating the inventory. It demonstrates core web development concepts like routing, templating, database integration, and user authentication.

## Features


  User Roles
  
    Admin:
      1. Add and view orders.
      2. Manage inventory (add new items, update stock quantities).
      3. View in-progress and completed orders.
    Wait Staff:
      1. Add orders for customers.
      2. Mark orders as completed.
      3. View in-progress and completed orders.
    Kitchen Staff:
      1. Update inventory (adjust stock levels or add new items).
  
  
  
  Order Management
    1. Add orders with selected items and quantities.
    2. Automatically deducts inventory stock when orders are placed.
    3. View in-progress orders and mark them as completed.
    4. View completed orders.
  Inventory Management
    1. View current inventory levels.
    2. Update stock quantities of existing items.
    3. Add new items to the inventory.
  Authentication
    1. Role-based access control ensures users only see options relevant to their role.
    2. Flash messages provide feedback on login, order actions, and inventory updates.


  Project Structure
  ```bash
    /project
      /static
        styles.css             # CSS for styling
      /templates
        index.html             # Login page
        dashboard.html         # User-specific dashboard
        add_order.html         # Form for adding orders
        view_orders.html       # Display orders by status
        update_inventory.html  # Form for updating inventory
      app.py                     # Main Flask application
      usermgmt.py                # User management logic
      ordermgmt.py               # Order management logic
      inventory.py               # Inventory management logic
      restaurant.db              # SQLite database



