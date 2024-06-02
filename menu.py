from db import db
from menu_item import MenuItem

class Menu:
    def __init__(self):
        self.items = self.load_menu()

    def load_menu(self):
        items = []
        rows = db.fetch_all("SELECT * FROM MenuItems")
        for row in rows:
            items.append(MenuItem(id=row[0], name=row[1], price=row[2], veg=row[3], rating=row[4], rating_count=row[5]))
        return items

    def show_menu(self):
        rows = db.fetch_all("SELECT id, name, price, rating, rating_count FROM MenuItems")
        print('-'*80)
        print(f'{"ID":<5} {"Name":<40} {"Price":<10} {"Rating":<10} {"Rating Count":<10}')
        print('-'*80)
        for row in rows:
            item_id, name, price, rating, rating_count = row
            rating = f"{rating:.1f}" if rating_count > 0 else 'None'
            print(f'{item_id:<5} {name[:40]:<40} {price:<10} {rating:<10} {rating_count:<10}')
        print('-'*80)

    def add_item(self, name, price, veg):
        db.execute_query("INSERT INTO MenuItems (name, price, veg) VALUES (%s, %s, %s)", (name, price, veg))
        print('Item added successfully.')

    def delete_item(self, item_id):
        db.execute_query("DELETE FROM MenuItems WHERE id = %s", (item_id,))
        if db.cursor.rowcount > 0:
            print(f'Item with ID {item_id} deleted successfully.')
        else:
            print(f'Item with ID {item_id} not found.')

    def add_rating(self, item_id, rating):
        item = db.fetch_one("SELECT name FROM MenuItems WHERE id = %s", (item_id,))
        if not item:
            print(f"Item with ID {item_id} not found.")
            return

        current_rating, rating_count = db.fetch_one("SELECT rating, rating_count FROM MenuItems WHERE id = %s", (item_id,))

        if rating_count == 0:
            new_rating = rating
        else:
            new_rating = (current_rating * rating_count + rating) / (rating_count + 1)

        new_rating_count = rating_count + 1

        db.execute_query(
            "UPDATE MenuItems SET rating = %s, rating_count = %s WHERE id = %s",
            (new_rating, new_rating_count, item_id)
        )
        print(f"Rating added successfully. New average rating for item ID {item_id} is {new_rating:.1f} based on {new_rating_count} ratings.")

    def item_exists(self, item_id):
        """
        Check if an item with the given ID exists in the menu.
        """
        return any(item.id == item_id for item in self.items)