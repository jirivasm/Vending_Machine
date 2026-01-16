class Item:
    def __init__(self, name,price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        
    def is_available(self):
        return self.stock > 0
    
    def reduce_stock(self):
        if(self.is_available):
            self.stock -=1
    def __str__(self):
        """
        Optional: This tells Python how to print the item 
        info (e.g., 'Coke: $1.50')
        """
        return f"{self.name} (${self.price:.2f}) - Stock: {self.stock}"