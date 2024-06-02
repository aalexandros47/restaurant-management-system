from db import db

class MenuItem:
    def __init__(self, id, name, price, veg, rating=0.0, rating_count=0):
        self.id = id
        self.name = name
        self.price = price
        self.veg = veg
        self.rating = rating
        self.rating_count = rating_count

    def add_rating(self, rating):
        result = db.fetch_one("SELECT rating, rating_count FROM MenuItems WHERE id = %s", (self.id,))
        if result:
            current_rating, rating_count = result
            new_rating_count = rating_count + 1
            new_rating = ((current_rating * rating_count) + rating) / new_rating_count
            db.execute_query(
                "UPDATE MenuItems SET rating = %s, rating_count = %s WHERE id = %s",
                (new_rating, new_rating_count, self.id)
            )
            print("Rating added successfully.")
        else:
            print("Item not found.")
