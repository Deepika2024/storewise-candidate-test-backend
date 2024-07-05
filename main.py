from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class MenuCompleter(Completer):
    def _init_(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        for word in self.words:
            if word.startswith(word_before_cursor):
                yield Completion(word, start_position=-len(word_before_cursor))

class McDonaldsShell:
    def _init_(self):
        self.menu = {
            'Big Mac': 5.00,
            'McChicken': 4.00,
            'Fries': 2.50,
            'Coke': 1.50
        }
        self.order = []
        self.service_charge_rate = 0.1  # 10% service charge

    def display_menu(self):
        print("\nCurrent Menu:")
        for item, price in self.menu.items():
            print(f"{item}: ${price:.2f}")
        print()

    def add_menu_item(self):
        item_name = prompt("Enter the name of the new menu item: ").strip()
        while True:
            try:
                item_price = float(prompt("Enter the price of the new menu item: ").strip())
                break
            except ValueError:
                print("Invalid price. Please enter a numeric value.")
        self.menu[item_name] = item_price
        print(f"Added {item_name} to the menu with price ${item_price:.2f}\n")

    def take_order(self):
        print("Welcome to the McDonalds Shell!")
        while True:
            action = prompt("Type 'order' to place an order, 'add' to add a new item to the menu, or 'done' to finish: ").strip().lower()
            if action == 'done':
                break
            elif action == 'add':
                self.add_menu_item()
            elif action == 'order':
                self.order_items()
            else:
                print("Invalid action. Please choose 'order', 'add', or 'done'.")

    def order_items(self):
        self.display_menu()
        menu_completer = MenuCompleter(list(self.menu.keys()))

        while True:
            item = prompt("Please select items to order (type 'done' to finish ordering): ", completer=menu_completer).strip()
            if item.lower() == 'done':
                break
            if item in self.menu:
                self.order.append(item)
                print(f"Added {item} to your order.")
            else:
                print("Item not on the menu. Please select a valid item.")

    def calculate_bill(self):
        order_amount = sum(self.menu[item] for item in self.order)
        service_charge = order_amount * self.service_charge_rate
        final_amount = order_amount + service_charge
        return order_amount, service_charge, final_amount

    def print_bill(self):
        order_amount, service_charge, final_amount = self.calculate_bill()
        print("\nYour bill:")
        print(f"Order Amount: ${order_amount:.2f}")
        print(f"Service Charge (10%): ${service_charge:.2f}")
        print(f"Final Amount: ${final_amount:.2f}")

if _name_ == "_main_":
    shell = McDonaldsShell()
    shell.take_order()
    shell.print_bill()
