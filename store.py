from VendingMachine import VendingMachine
from Item import Item
from User import User



def main():
    # Setup
    
    
    user_list = []
    user = User("Jose", 100)
    user_list.append(user)
    selected_user = User("",0)

    while selected_user.name == "":
        choice = input("1)Select user\n2)Create new user\n3)quit\n")
        if int(choice) == 1:
            username =  input("Please enter your username or q to restart: ")
            if username == "q":
                    break
            for users in user_list:
                if users.name  == username:
                    selected_user.set_name(username)
                    selected_user.set_balance(users.balance)
                    print(f"{username} was selected. please continue to the vending machine")
                    break

                print("no username found")
            break
        elif int(choice) == 2:
            username = input("please enter your username: ")
            while username in user_list:
                print("username already taken. please try again")

            balance = input("how much money do you want to add?: ")
            new_user = User(int(balance), username)
            user_list.append(new_user)
            print("A new user was added. Thanks")
        else:
            break

    machine = VendingMachine()
    machine.user = selected_user

    machine.add_item("A1", Item("Coke", 1.50, 5))
    machine.add_item("B2", Item("Chips", 2.00, 3))

    while True:
        if machine.user.name == "":
            break
        print("\n--- User ---")
        print(f"User: {machine.user.name}, Balance: {machine.user.balance}")

        print("\n--- Vending Machine ---")
       
        print(f"Machine balance: {machine.balance}")
        machine.print_items()
        # Logic to display menu and get user input
        choice = input("1)Insert money\n2)Select item (code)\n3)Show inventory\n4)Quit\n")

        match int(choice):
            case 1:
                amount = input("How muh money would you like to insert? ")
                amount_inserted = float(amount)
                if selected_user.balance < amount_inserted:
                    print("You dont have that kind of money")
                else:
                    machine.insert_money(amount_inserted)
                    selected_user.remove_balance(amount_inserted)
                    print(f"thanks. the balance of the machine is now. {machine.balance:.2f}")
                    
            case 2:
                if machine.balance == 0:
                    print("Please insert money first!!")
                else:
                    code = input("Please select the code: ")
                    machine.select_item(code)
            case 3:
                machine.print_items
                pass
            case 4:
                break
        
        # Logic to handle choice...
        

if __name__ == "__main__":
    main()     

    
    
    
    

