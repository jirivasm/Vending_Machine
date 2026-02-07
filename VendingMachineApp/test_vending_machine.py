import unittest
from app import app, db, User, Item

class TestVendingApp(unittest.TestCase):
    def setUp(self):
        """Standard setup run before every test."""
        
        # 1. Force the app into Testing Mode
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # Force SQLite
            "SQLALCHEMY_TRACK_MODIFICATIONS": False
        })

        # 2. CRITICAL FIX: Kill the old Postgres connection!
        # This forces SQLAlchemy to read the new 'sqlite' config we just set.
        with app.app_context():
            db.engine.dispose()

        # 3. Create a test client
        self.client = app.test_client()

        # 4. Create the tables in the In-Memory DB
        with app.app_context():
            db.create_all()
            
            # Seed test data
            user = User(username="TestUser", balance=5.00)
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
            user = db.session.get(User, "TestUser")
            item = db.session.get(Item, "T1")
            
            self.assertIsNotNone(user)
            self.assertEqual(user.balance, 5.00)
            self.assertEqual(item.stock, 2)

    def test_transaction_logic(self):
        """Test 2: Simulate a purchase logic directly on the DB"""
        with app.app_context():
            user = db.session.get(User, "TestUser")
            item = db.session.get(Item, "T1")
            
            # Simulate Purchase Logic
            user.balance -= item.price
            item.stock -= 1
            db.session.commit()
            
            
            # Verify Results
            updated_user = db.session.get(User, "TestUser")
            updated_item = db.session.get(Item, "T1")
            
            self.assertEqual(updated_user.balance, 3.50) # 5.00 - 1.50
            self.assertEqual(updated_item.stock, 1)      # 2 - 1

    def test_home_page(self):
        """Test 3: Ensure the web server is running"""
        # Simulate a browser visiting '/'
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

if __name__ == '__main__':
    unittest.main()