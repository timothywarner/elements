#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Legacy Inventory Management System
================================
Created: Jan 15, 2018
Last Modified: Dec 10, 2020
Author: John Doe

This monolithic application handles inventory management for a small retail business.
It includes user authentication, inventory tracking, order processing, and reporting.
"""

import sqlite3
import datetime
import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables
DB_PATH = 'inventory.db'
SMTP_SERVER = 'smtp.company.com'
SMTP_PORT = 587
SMTP_USER = 'system@company.com'
SMTP_PASSWORD = 'password123'  # Hard-coded credentials
ADMIN_EMAIL = 'admin@company.com'

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Multiple tables created in one function
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, 
                  items TEXT, total REAL, status TEXT)''')
    
    conn.commit()
    conn.close()

# User management - no password hashing
def add_user(username, password, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
              (username, password, email))
    conn.commit()
    conn.close()
    send_email(email, "Welcome!", "Welcome to our system!")

def check_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?",
              (username, password))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Inventory management - no input validation
def add_item(name, quantity, price):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
              (name, quantity, price))
    conn.commit()
    conn.close()
    
    # Alert admin for low stock
    if quantity < 10:
        send_email(ADMIN_EMAIL, "Low Stock Alert",
                  f"Item {name} is low on stock: {quantity} remaining")

def update_quantity(item_id, new_quantity):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity=? WHERE id=?",
              (new_quantity, item_id))
    conn.commit()
    conn.close()

# Order processing - complex monolithic function
def process_order(user_id, items):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Calculate total and check inventory
    total = 0
    order_items = []
    for item_id, quantity in items.items():
        c.execute("SELECT name, quantity, price FROM inventory WHERE id=?",
                  (item_id,))
        item = c.fetchone()
        if not item:
            conn.close()
            raise Exception(f"Item {item_id} not found")
        
        name, current_quantity, price = item
        if current_quantity < quantity:
            conn.close()
            raise Exception(f"Insufficient stock for {name}")
        
        total += price * quantity
        order_items.append({
            'id': item_id,
            'name': name,
            'quantity': quantity,
            'price': price
        })
        
        # Update inventory
        new_quantity = current_quantity - quantity
        c.execute("UPDATE inventory SET quantity=? WHERE id=?",
                  (new_quantity, item_id))
    
    # Create order
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("""INSERT INTO orders (user_id, date, items, total, status)
                 VALUES (?, ?, ?, ?, ?)""",
              (user_id, date, json.dumps(order_items), total, 'pending'))
    
    order_id = c.lastrowid
    
    # Send confirmation email
    c.execute("SELECT email FROM users WHERE id=?", (user_id,))
    user_email = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    send_email(user_email, f"Order Confirmation #{order_id}",
               f"Your order total is ${total:.2f}")
    
    return order_id

# Email functionality - no error handling
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

# Reporting - inefficient data processing
def generate_monthly_report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get all orders and process in memory
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    
    total_sales = 0
    items_sold = {}
    
    for order in orders:
        order_date = datetime.datetime.strptime(order[2], '%Y-%m-%d %H:%M:%S')
        if order_date.month == datetime.datetime.now().month:
            total_sales += order[4]
            items = json.loads(order[3])
            for item in items:
                if item['name'] not in items_sold:
                    items_sold[item['name']] = 0
                items_sold[item['name']] += item['quantity']
    
    conn.close()
    
    # Generate report
    report = f"Monthly Sales Report\n"
    report += f"Total Sales: ${total_sales:.2f}\n\n"
    report += "Items Sold:\n"
    for item, quantity in items_sold.items():
        report += f"{item}: {quantity}\n"
    
    # Save report to file
    with open(f"report_{datetime.datetime.now().strftime('%Y%m')}.txt", 'w') as f:
        f.write(report)
    
    send_email(ADMIN_EMAIL, "Monthly Sales Report", report)

# Main execution
if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Example usage
    try:
        # Add test user
        add_user("test_user", "password123", "test@example.com")
        
        # Add inventory items
        add_item("Laptop", 5, 999.99)
        add_item("Mouse", 20, 24.99)
        
        # Process test order
        user_id = check_login("test_user", "password123")
        if user_id:
            order_items = {1: 1, 2: 2}  # Order 1 laptop and 2 mice
            order_id = process_order(user_id, order_items)
            print(f"Order {order_id} processed successfully")
        
        # Generate report
        generate_monthly_report()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        send_email(ADMIN_EMAIL, "System Error", str(e)) 