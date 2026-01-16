
class VendingMachine:
    def __init__(self):
        self.inventory = {}
        self.user_balance = 0.0
        
    def add_item(self, code, item):
        self.inventory[code] = item
        
    def insert_money(self, amount):
        self.user_balance += amount
        print(f"Current balance: ${self.user_balance:.2f}")
    
    def print_items(self):
        for code in self.inventory:
            item = self.inventory[code]
            print(f"[{code}] {item}")
        
    def select_item(self, code):
        if code not in self.inventory:
            print("Invalid Code. Please try again.")
            return
        
        item = self.inventory[code]

    # 2. Check if the item is in stock
        if item.stock <= 0:
            print(f"Sorry, {item.name} is sold out!")
        
        # 3. Check if the user has enough money
        elif self.user_balance < item.price:
            needed = item.price - self.user_balance
            print(f"Insufficient funds. You need ${needed:.2f} more.")

        # 4. Success!
        else:
            item.reduce_stock()
            change = self.user_balance - item.price
            self.user_balance = 0  # Reset balance after giving change
            print(f"Dispensing {item.name}...")
            print(f"Transaction successful! Your change is: ${change:.2f}")