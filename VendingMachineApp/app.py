import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from VendingMachine import VendingMachine
from Item import Item
from User import User


app = Flask(__name__)
app.secret_key = "secret_vending_key" # for sessions

# 1. Global Setup (This stays alive while the server runs)
machine = VendingMachine()
machine.add_item("A1", Item("Coke", 1.50, 5))
machine.add_item("B2", Item("Chips", 2.00, 3))

# For this example, let's keep a simple dictionary of users
users_db = {"Jose": User("Jose",100)}

@app.route('/')
def index():
    
    username = session.get('username')
    if not username or username not in users_db:
        session.pop('username', None) # Clean up the invalid session
        return redirect(url_for('login'))
    
    current_user = users_db[username]
    stack = os.getenv('APP_STACK', 'Python Flask')
    return render_template('index.html', machine=machine, user=current_user, stack=stack)

@app.route('/login', methods=['GET', 'POST'])
def login():
    stack = os.getenv('APP_STACK', 'Python Flask')
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')

        if action == "login":
            if username in users_db:
                session['username'] = username  # This "selects" the user
                return redirect(url_for('index'))
            else:
                return "User not found! <a href='/login'>Try again</a>"

        elif action == "create":
            if username in users_db:
                return "Username taken! <a href='/login'>Try again</a>"
            
            balance = float(request.form.get('balance', 0))
            # Create the object and store it in our "database" dictionary
            users_db[username] = User(username, balance)
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
    current_user = users_db[session['username']]
    
    if current_user.balance >= amount:
        current_user.remove_balance(amount)
        machine.insert_money(amount)
    return redirect(url_for('index'))

@app.route('/purchase', methods=['POST'])
def purchase():
    code = request.form.get('code')
    current_user = users_db[session['username']]
    # machine.select_item should return a message string
    machine.user = current_user
    message = machine.select_item(code) 
    # 2. "Flash" the message to the user
    flash(message)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)