class User:
    def __init__(self, balance, name):
        self.balance = balance
        self.name = name
    def add_balance(self, amount):
        self.balance += amount
    def remove_balance(self, amount):
        self.balance -= amount  
    def check_balance(self):
        return self.balance      