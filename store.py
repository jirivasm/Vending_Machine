from VendingMachine import VendingMachine
from Item import Item
from User import User



def main():
    # Setup
    machine = VendingMachine()
    machine.add_item("A1", Item("Coke", 1.50, 5))
    machine.add_item("B2", Item("Chips", 2.00, 3))
    machine.print_items()
    user = User("Jose", 100)

    while True:
        print("\n--- Vending Machine ---")
        # Logic to display menu and get user input
        choice = input("1)Insert money\n2)Select item (code)\n3)Show inventory\n 4)Quit: ").lower()

        if int(choice) == 4:
            break
        match int(choice):
            case 1:
                
                break
            case 2:
                
                break
            case 3:
                
                break
            case 4:
                break
        
        # Logic to handle choice...
        

if __name__ == "__main__":
    main()     

    
    
    
    

