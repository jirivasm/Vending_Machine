class User:
    def __init__(self, name, balance):
        self.balance = float(balance)
        self.name = name
    def set_name(self, name):
        self.name = name
    def set_balance(self, balance):
        self.balance = balance
    def add_balance(self, amount):
        self.balance += amount
    def remove_balance(self, amount):
        self.balance -= amount  
     