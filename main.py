from customer import Customer
from staff import Staff
from restaurant import RestaurantSystem
from menu import Menu
import datetime

def get_valid_input(prompt):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Input cannot be empty.")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def main():
    restaurant = RestaurantSystem()
    menu = Menu()
    print("""\

        ⢀⠔⠊⠉⠑⢄⠀⠀⣀⣀⠤⠤⠤⢀⣀⠀⠀⣀⠔⠋⠉⠒⡄⠀
        ⡎⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠘⡄
        ⣧⢢⠀⠀⠀⠀⠀⠀⠀⠀⣀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣆⡗
        ⠘⡇⠀⢀⠆⠀⠀⣀⠀⢰⣿⣿⣧⠀⢀⡀⠀⠀⠘⡆⠀⠈⡏⠀
        ⠀⠑⠤⡜⠀⠀⠈⠋⠀⢸⣿⣿⣿⠀⠈⠃⠀⠀⠀⠸⡤⠜⠀⠀
        ⠀⠀⠀⣇⠀⠀⠀⠀⠀⠢⣉⢏⣡⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀
        ⠀⠀⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠋⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢨⠃⠀⢀⠀⢀⠔⡆⠀⠀⠀⠀⠻⡄⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⡎⠀⠀⠧⠬⢾⠊⠀⠀⢀⡇⠀⠀⠟⢆⠀⠀⠀⠀
        ⠀⠀⠀⠀⢀⡇⠀⠀⡞⠀⠀⢣⣀⡠⠊⠀⠀⠀⢸⠈⣆⡀⠀⠀
        ⠀⠀⡠⠒⢸⠀⠀⠀⡇⡠⢤⣯⠅⠀⠀⠀⢀⡴⠃⠀⢸⠘⢤⠀
        ⠀⢰⠁⠀⢸⠀⠀⠀⣿⠁⠀⠙⡟⠒⠒⠉⠀⠀⠀⠀⠀⡇⡎⠀
        ⠀⠘⣄⠀⠸⡆⠀⠀⣿⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⢀⠟⠁⠀
        ⠀⠀⠘⠦⣀⣷⣀⡼⠽⢦⡀⠀⠀⢀⣀⣀⣀⠤⠄⠒⠁⠀⠀⠀
        """)
    print("Relaxing Koala Restaurant")
    while True:
        print("Welcome to the Restaurant Management System")
        print("1. Login as Customer")
        print("2. Login as Staff")
        print("3. Exit")
        choice = input("Select user type: ")
        if choice == '1':
            name = get_valid_input("Enter your name: ")
            vname = name
            customer_id = restaurant.handle_customer(vname)
            customer = Customer(vname)
            while True:
                print("1. View Menu")
                print("2. Make Reservation")
                print("3. Make Payment")
                print("4. Exit")
                customer_choice = input("Enter your choice: ").strip()
                if customer_choice == '1':
                    restaurant.menu.show_menu()
                    sub_choice = input("Press 'e' to exit, 'r' to add rating, 'o' to order: ")
                    if sub_choice == 'e':
                        continue
                    elif sub_choice == 'o':
                        order_type = input("Press 'd' for Dine-In, 't' for Takeaway: ").strip()
                        if order_type == 'd':
                            customer.place_dine_in_order(customer_id)
                            input("Press enter to return to main menu\n")
                        elif order_type == 't':
                            customer.place_takeaway_order(customer_id)
                            input("Press enter to return to main menu\n")
                        else:
                            print("Invalid choice.")
                    elif sub_choice == 'r':
                        customer.add_rating(restaurant.menu)
                    else:
                        print("Invalid choice")
                elif customer_choice == '2':
                    customer.make_reservation()
                elif customer_choice == '3':
                    restaurant.process_payment(customer_id)
                elif customer_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '2':
            name = get_valid_input("Enter your name: ")
            staff = restaurant.handle_staff(name)

            while True:
                print("1. Update Menu")
                print("2. View Sales")
                print("3. Exit")
                staff_choice = input("Enter your choice: ").strip()
                if staff_choice == '1':
                    restaurant.menu.show_menu()
                    staff.update_menu(menu)
                if staff_choice == '2':
                    restaurant.show_all_sales()
                elif staff_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
