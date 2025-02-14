import unittest
import os
import sys
import sqlite3

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from s4_old_app import add_item, update_quantity, check_login, process_order

class TestInventorySystem(unittest.TestCase):
    """Basic test cases for inventory system"""
    
    @classmethod
    def setUpClass(cls):
        # Use test database
        global DB_PATH
        DB_PATH = 'test_inventory.db'
        
        # Initialize test database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create tables
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS inventory
                     (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS orders
                     (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, 
                      items TEXT, total REAL, status TEXT)''')
        
        # Add test user
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  ("test_user", "test_pass", "test@test.com"))
        
        conn.commit()
        conn.close()
    
    def setUp(self):
        """Set up test database before each test"""
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
    
    def tearDown(self):
        """Clean up after each test"""
        self.conn.close()
    
    @classmethod
    def tearDownClass(cls):
        """Remove test database"""
        try:
            os.remove(DB_PATH)
        except:
            pass
    
    # Basic inventory tests
    def test_add_item(self):
        """Test adding a new item"""
        add_item("Test Item", 10, 9.99)
        
        self.c.execute("SELECT name, quantity, price FROM inventory WHERE name=?",
                      ("Test Item",))
        item = self.c.fetchone()
        
        self.assertIsNotNone(item)
        self.assertEqual(item[0], "Test Item")
        self.assertEqual(item[1], 10)
        self.assertEqual(item[2], 9.99)
    
    def test_update_quantity(self):
        """Test updating item quantity"""
        # Add test item
        self.c.execute("""INSERT INTO inventory (name, quantity, price)
                         VALUES (?, ?, ?)""", ("Update Test", 5, 19.99))
        item_id = self.c.lastrowid
        self.conn.commit()
        
        # Update quantity
        update_quantity(item_id, 10)
        
        self.c.execute("SELECT quantity FROM inventory WHERE id=?", (item_id,))
        new_quantity = self.c.fetchone()[0]
        self.assertEqual(new_quantity, 10)
    
    # Limited login test
    def test_check_login(self):
        """Test user login"""
        user_id = check_login("test_user", "test_pass")
        self.assertIsNotNone(user_id)
    
    # Basic order test - no edge cases
    def test_process_order(self):
        """Test basic order processing"""
        # Add test items
        self.c.execute("""INSERT INTO inventory (name, quantity, price)
                         VALUES (?, ?, ?)""", ("Item 1", 20, 10.00))
        item1_id = self.c.lastrowid
        
        self.c.execute("""INSERT INTO inventory (name, quantity, price)
                         VALUES (?, ?, ?)""", ("Item 2", 15, 20.00))
        item2_id = self.c.lastrowid
        
        self.conn.commit()
        
        # Process order
        items = {item1_id: 2, item2_id: 1}  # Order 2 of item1 and 1 of item2
        order_id = process_order(1, items)  # Use test user (id=1)
        
        # Check order was created
        self.c.execute("SELECT total FROM orders WHERE id=?", (order_id,))
        total = self.c.fetchone()[0]
        self.assertEqual(total, 40.00)  # 2 * 10.00 + 1 * 20.00

if __name__ == '__main__':
    unittest.main() 