import json


class Library:
    def __init__(self):
        try:
            with open("api_library.json", "r") as f:
                self.home_library = json.load(f)
        except FileNotFoundError:
            self.home_library = []

    def all(self):
        return self.home_library

    def get(self, id):
        book = [book for book in self.all() if book['book_id'] == id]
        if book:
            return book[0]
        return []

    def create(self, data):
        self.home_library.append(data)
        self.save_all()

    def save_all(self):
        with open("api_library.json", "w") as f:
            json.dump(self.home_library, f)

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.home_library.index(book)
            self.home_library[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id)
        if book:
            self.home_library.remove(book)
            self.save_all()
            return True
        return False


home_library = Library()
