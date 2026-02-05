import unittest
from app import app, db, User, Item

class TestVendingApp(unittest.TestCase):
    def setUp(self):
        """
        Runs before EACH test. 
        Sets up a temporary "In-Memory" database so we don't touch the real Postgres.
        """
        # Configure Flask for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Fast RAM DB
        app.config['WTF_CSRF_ENABLED'] = False # Disable security tokens for testing

        # Create a test client (simulates a browser)
        self.client = app.test_client()

        # Create the database tables
        with app.app_context():
            db.create_all()
            
            # Add a test user
            user = User(username="TestUser", balance=5.00)
            # Add a test item
            item = Item(code="T1", name="TestSoda", price=1.50, stock=2)
            
            db.session.add(user)
            db.session.add(item)
            db.session.commit()

    def tearDown(self):
        """Runs after EACH test. Cleans up the database."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_models(self):
        """Test 1: Verify data is actually saving to the DB"""
        with app.app_context():
            user = User.query.get("TestUser")
            item = Item.query.get("T1")
            
            self.assertIsNotNone(user)
            self.assertEqual(user.balance, 5.00)
            self.assertEqual(item.stock, 2)

    def test_transaction_logic(self):
        """Test 2: Simulate a purchase logic directly on the DB"""
        with app.app_context():
            user = User.query.get("TestUser")
            item = Item.query.get("T1")
            
            # Simulate Purchase Logic
            user.balance -= item.price
            item.stock -= 1
            db.session.commit()
            
            # Verify Results
            updated_user = User.query.get("TestUser")
            updated_item = Item.query.get("T1")
            
            self.assertEqual(updated_user.balance, 3.50) # 5.00 - 1.50
            self.assertEqual(updated_item.stock, 1)      # 2 - 1

    def test_home_page(self):
        """Test 3: Ensure the web server is running"""
        # Simulate a browser visiting '/'
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check if our login page text appears (since we aren't logged in)
        self.assertIn(b'Welcome to the Vending Machine', response.data)

if __name__ == '__main__':
    unittest.main()