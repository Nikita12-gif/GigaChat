class Book:
    def __init__(self, name, writer, year):
        self.name = name
        self.writer = writer
        self.year = year
        
    def __str__(self):
        return f"Название: {self.name}, автор: {self.writer}, год{self.year}"
    
book1 = Book("Prestyplenie_i_nakazanie", "Fedor Dostoevskiy", "1865-1866")
book2 = Book("Bratya Karamazovy", "Fedor Dostoevskiy", "1878-1880")
book1.__str__()

class Library:
    def __init__(self, name):
        self.name = name
        self.list_of_books = []
        self.list_of_name = []
        
        
    def add_book(self, book):
        self.list_of_books.append(book)
        self.list_of_name.append(book[0])
        
        
    def remove_book(self, title):
        self.list_of_books.pop[self.list_of_name.index(title)]
        
        
    def find_by_author(self, author):
        self.books_of_author = []
        for i in self.list_of_books:
            if self.list_of_books[i][1] == author:
                self.books_of_author.append(self.list_of_books[i][0])
        return self.books_of_author
    
    
    def show_all(self):
        return self.list_of_books
        
        
        
        
        
lib1 = Library("Russian Classik")
lib1.add_book(book1)
lib1.add_book(book2)
lib1.find_by_author("Fedor Dostoevskiy")
lib1.show_all()
lib1.remove_book("Bratya Karamazovy")
lib1.show_all()
