class book:
    def __init__(self, name: str="unknown", author: str="unknown", year: str="unknown", pub_house: str="unknown", pr_vol = None, pr : str=" отсутствует") -> None:
        """Инициализация книги"""
        self.name = name
        self.author = author
        self.year = year
        self.pub_house = pub_house
        self.pr_vol = pr_vol
        self.pr = pr
    def get_book(self) -> str:
        """Получение книги"""
        return f" Книга: {self.name}\n Автор: {self.author}\n Год написания: {self.year}\n Издательство: {self.pub_house}\n Перейти в следующий том: {self.pr_vol}\n"
    
    def change_attribute(self, attr: str, x: str) -> None:
        """Смена атрибута книги"""
        if attr == "name":
            self.name = x
        elif attr == "author":
            self.author = x
        elif attr == "year":
            self.year = x
        elif attr == "pub_house":
            self.pub_house = x
        elif attr == "pr_vol":
            self.pr_vol = x
        else:
            return "Аттрибут не найден"
        
    def previous(self) -> str:
        """К предыдущей книге"""
        if self.pr_vol != " отсутствует":
            self.pr_vol.get_book()
        else:
            return "Это первая часть серии"
        
book1 = book("Mertvie dyshi. V1", "Nikolay Gogol", "1842", "Бомбора", None,)
book2 = book("Mertvie dyshi. V2", "Nikolay Gogol", "1847", "Бомбора", book1, "")
book3 = book("Mertvie dyshi. V3", "Nikolay Gogol", "2022", "Бомбора", book2, "")

print(book1.get_book())
print(book2.get_book())
book2.change_attribute("year", "1984")
print(book2.get_book())
print(book3.get_book())
print(book3.previous())
print(book1.previous())
