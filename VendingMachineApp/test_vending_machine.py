import unittest
from VendingMachine import VendingMachine
from Item import Item

class testVendingMAchine(unittest.TestCase):
    def setUp(self):
        """Standard setup run before every test."""
        self.vm = VendingMachine()
        self.item = Item("Coke", 1.50, 1) # Only 1 in stock
        self.vm.add_item("A1", self.item)
        
    def test_insert_money(self):
        self.vm.insert_money(2.00)
        self.assertEqual(self.vm.balance, 2.00)

    def test_purchase_success(self):
        self.vm.insert_money(2.00)
        self.vm.select_item("A1")
        self.assertEqual(self.vm.inventory["A1"].stock, 0)

    def test_insufficient_funds(self):
        self.vm.insert_money(1.00)
        success, result = self.vm.select_item("A1")
        self.assertFalse(success, "Should not allow purchase with insufficient funds")

    def test_invalid_code(self):
        result = self.vm.select_item("X99")
        self.assertFalse(result, "Should handle non-existent codes gracefully")

if __name__ == '__main__':
    unittest.main()

