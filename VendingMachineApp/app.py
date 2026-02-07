import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



app = Flask(__name__)
# --- DATABASE CONFIGURATION ---
if os.environ.get('TESTING') == 'true':
    # 1. TEST MODE: Force SQLite
    print("RUNNING IN TEST MODE (SQLite)")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # --- DATABASE CONFIGURATION ---
    # use .get() to provide defaults for local testing, 
    # but Kubernetes will inject the real values via Environment Variables.
else:
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'password')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME', 'postgres')

    # Connection String: postgresql://user:password@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret_vending_key" # for sessions

# Initialize the Database
db = SQLAlchemy(app)


# --- MODELS (The Database Tables) ---
# We define these HERE instead of importing them to ensure they map to the DB
class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50), primary_key=True)
    balance = db.Column(db.Float, default=0.0)

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(50), db.ForeignKey('users.username'))
    item_name = db.Column(db.String(50))

class Item(db.Model):
    __tablename__ = 'items'
    code = db.Column(db.String(10), primary_key=True) # e.g., "A1"
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

# --- INITIALIZATION (Seeding Data) ---
def init_db():
    """Create tables and seed default items if empty"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        if not db.session.get(Item, "A1"): 
            coke = Item(code="A1", name="Coke", price=1.50, stock=5)
            chips = Item(code="B2", name="Chips", price=2.00, stock=3)
            db.session.add_all([coke, chips])
            db.session.commit()
            print("Initialized Database with default items.")

@app.route('/')
def index():
    
    username = session.get('username')
    # Fetch user from DB instead of dictionary
    current_user = db.session.get(User, username) if username else None

    if not current_user:
        session.pop('username', None)
        return redirect(url_for('login'))
    
    # Fetch all items from DB to display
    items = Item.query.all()
    stack = os.getenv('APP_STACK', 'Python Flask')
    
    user_purchases = Purchase.query.filter_by(user_username=username).all()
    inventory_list = [p.item_name for p in user_purchases]
    
    # Pass 'items' list to template instead of 'machine' object
    return render_template('index.html', items=items, user=current_user, stack=stack, inventory=inventory_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    stack = os.getenv('APP_STACK', 'Python Flask')
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')

        if action == "login":
            user = User.query.get(username)
            if user:
                session['username'] = username  # This "selects" the user
                return redirect(url_for('index'))
            else:
                return "User not found! <a href='/login'>Try again</a>"

        elif action == "create":
            if User.query.get(username):
                return "Username taken! <a href='/login'>Try again</a>"
            
            balance = float(request.form.get('balance', 0))
            new_user = User(username=username, balance=balance)
            db.session.add(new_user)
            db.session.commit() # Save to Postgres
            session['username'] = username
            return redirect(url_for('index'))

    return render_template('login.html',stack=stack)

@app.route('/logout')
def logout():
    session.pop('username', None) # Clears the "selected user"
    return redirect(url_for('login'))

@app.route('/insert', methods=['POST'])
def insert():
    amount = float(request.form.get('amount'))
    username = session.get('username')
    
    user = User.query.get(username)
    if user and user.balance >= amount:
        # 1. REMOVE money from User's Wallet (Permanent DB)
        user.balance -= amount
        db.session.commit()
    # 2. ADD money to Machine Credit (Temporary Session)
        # We use the session to store "money currently in the machine"
        current_credit = session.get('machine_credit', 0.0)
        session['machine_credit'] = current_credit + amount
        
        flash(f"Inserted ${amount:.2f} into machine.")
    else:
        flash("Insufficient funds in your Wallet!")
        
    return redirect(url_for('index'))

@app.route('/purchase', methods=['POST'])
def purchase():
    code = request.form.get('code')
    username = session.get('username')
    
    # Get the item from the DB
    item = Item.query.get(code)
    
    # Get the money currently IN THE MACHINE (not the wallet)
    machine_credit = session.get('machine_credit', 0.0)
    
    if not item:
        flash("Invalid selection!")
    elif item.stock <= 0:
        flash(f"Sold Out: {item.name}")
    elif machine_credit < item.price:
        # Compare against machine_credit, NOT user.balance
        flash(f"Insert more money! Needs ${item.price:.2f}")
    else:
        # EXECUTE TRANSACTION
        # 1. Deduct cost from the MACHINE CREDIT (Session)
        session['machine_credit'] = machine_credit - item.price
        
        # 2. Update Stock (DB)
        item.stock -= 1
        
        new_purchase = Purchase(user_username=username, item_name=item.name)
        db.session.add(new_purchase)
        
        db.session.commit()
        
        flash(f"Dispensing {item.name}. Enjoy!")
    
    return redirect(url_for('index'))

@app.route('/return_change')
def return_change():
    """Optional: Returns money from Machine Credit back to Wallet"""
    username = session.get('username')
    machine_credit = session.get('machine_credit', 0.0)
    
    if machine_credit > 0:
        user = User.query.get(username)
        user.balance += machine_credit
        db.session.commit()
        
        session['machine_credit'] = 0.0
        flash(f"Returned ${machine_credit:.2f} to your wallet.")
    
    return redirect(url_for('index'))

@app.route('/health/db')
def db_health():
    try:
        # Simple query to verify connection
        db.session.execute(text('SELECT 1'))
        return "Database Connection: HEALTHY (Connected to PostgreSQL)", 200
    except Exception as e:
        return f"Database Connection Failed: {str(e)}", 500

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)