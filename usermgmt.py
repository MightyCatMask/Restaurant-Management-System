# user_management.py

import sqlite3

class User:
    def __init__(self, username):
        self.username = username
        self.role = None
        self.authenticated = False

    def authenticate(self, password):
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE username=? AND password=?", (self.username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.role = result[0]
            self.authenticated = True
            print(f"Welcome, {self.username}! You are logged in as {self.role}.")
        else:
            print("Invalid credentials")

    def is_admin(self):
        return self.authenticated and self.role == "admin"
