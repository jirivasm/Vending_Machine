
from User import User
class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.balance = 0.0
        self.user = User("",0)
        
    def add_item(self, code, item):
        self.inventory[code] = item
        
    def insert_money(self, amount):
        self.balance += amount
        print(f"Current balance: ${self.balance:.2f}")
    
    def print_items(self):
        for code in self.inventory:
            item = self.inventory[code]
            print(f"[{code}] {item}")
        
    def select_item(self, code):
        self.change = 0.0
        if code not in self.inventory:
            print("Invalid Code. Please try again.")
            return False
        
        item = self.inventory[code]

    # 2. Check if the item is in stock
        if item.stock <= 0:
            print(f"Sorry, {item.name} is sold out!")
            return False
        
        # 3. Check if the user has enough money
        elif self.balance < item.price:
            needed = item.price - self.balance
            return False, f"Insufficient funds. You need ${needed:.2f} more."
        
           

        # 4. Success!
        else:
            item.reduce_stock()
            change = self.balance - item.price
            self.balance = 0  # Reset balance after giving change
            self.user.add_balance(change)
            return(f"Transaction successful! Your change is: ${change:.2f}")
