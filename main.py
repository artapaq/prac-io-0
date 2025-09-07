import json

class Book:
    def __init__(self, title, author, year, isbn, isavailable=True):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__isbn = isbn
        self.__isavailable = isavailable

    def __str__(self):
        return f'The offline book {self.__title} by {self.__author}'

    @property
    def isbn(self):
        return self.__isbn

    @property
    def isavailable(self):
        return self.__isavailable

    def get_description(self):
        print(self)

    def check_out(self):
        self.__isavailable = False

    def return_book(self):
        self.__isavailable = True

    def to_dict(self):
        return {
            'title': str(self.__title),
            'author': str(self.__author),
            'year': str(self.__year),
            'isbn': str(self.__isbn),
            'isavailable': str(self.__isavailable)
        }

class Library:
    def __init__(self):
        self.__books = {}
        self.__users = {}

    def __getitem__(self, isbn):
        return self.__books.get(isbn, None)

    def __contains__(self, isbn):
        return isbn in self.__books

    def __str__(self):
        data = ''
        for elem in self.__books:
            data += str(elem) + " "

        return data

    @property
    def users(self):
        return self.__users

    @property
    def books(self):
        return self.__books

    def add_book(self, book):
        self.__books[book.isbn] = book

    def add_user(self, user):
        self.__users[user.user_id] = user

    def find_book(self, isbn):
        return self.__books.get(isbn, None)

    def check_available(self, book):
        if book.isbn in self.__books:
            if self.__books[book.isbn].isavailable:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def save_to_file(cls, library_instance, filename):
        with open (filename, 'w', encoding='utf-8') as file:
            data = []
            for book in library_instance.__books.values():
                data.append(book.to_dict())
            json.dump(data, file, ensure_ascii=False, indent=4)

class User:
    def __init__(self, name, user_id):
        self.__name = name
        self.__user_id = user_id
        self.__borrowed_books = []

    def __str__(self):
        return f'{self.__name} {self.__user_id}'

    @property
    def user_id(self):
        return self.__user_id

    @property
    def borrowed_books(self):
        return self.__borrowed_books

    def borrow_book(self, book_name, library_name):
        if library_name.check_available(book_name):
            self.__borrowed_books.append(
                book_name
            )
            library_name.books[book_name.isbn].check_out()

    def return_book_lib(self, book_name, library_name):
        if book_name.isbn in library_name.books:
            library_name.books[book_name.isbn].return_book()
            self.__borrowed_books.remove(book_name)