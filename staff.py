from user import User
from menu import Menu

class Staff(User):

    @staticmethod
    def get_valid_input(prompt):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    raise ValueError("Input cannot be empty.")
                return user_input
            except ValueError as e:
                print(f"Error: {e}. Please try again.")

    def update_menu(self, menu):
        while True:
            print("1. Add Item")
            print("2. Delete Item")
            print("3. View Menu")
            print("4. Exit")
            choice = self.get_valid_input("Enter your choice: ")
            if choice == '1':
                name = self.get_valid_input('Enter item name: ')
                while True:
                    price_input = self.get_valid_input('Enter item price: ')
                    try:
                        price = float(price_input)
                        break
                    except ValueError:
                        print("Error: Price must be a number. Please try again.")                
                veg_input = self.get_valid_input('Is the item veg (yes/y or no/n): ').lower()
                if veg_input == 'yes':
                    veg = True
                elif veg_input == 'y':
                    veg = True
                elif veg_input == 'no':
                    veg = False
                elif veg_input == 'n':
                    veg = False
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    continue
                menu.add_item(name, price, veg)
            elif choice == '2':
                while True:
                    item_id_input = self.get_valid_input('Enter item ID to delete: ')
                    try:
                        item_id = int(item_id_input)
                        if not menu.item_exists(item_id):
                            raise ValueError("Item ID does not exist.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}. Please try again.")
                menu.delete_item(item_id)
            elif choice == '3':
                menu.show_menu()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

