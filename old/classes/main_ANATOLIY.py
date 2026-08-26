
class Student:
    def __init__(self, name, age): # Конструктор класса
        self.name = name
        self.age = age
        self.marks = []
        
    # Методы
    def add_mark(self, mark):# Добавить оценку
        if 2 <= mark <= 5 and mark == int(mark):
            self.marks.append(mark)
        else:
            return("Не удалось распознать число")
        
    def get_marks(self): # Вернуть все оценки
        return(self.marks)
    def get_average(self):
        return (sum(self.marks) / len(self.marks))        
        
Anatoliy = Student("Анатолий", 18)
print(Anatoliy.get_marks())
Anatoliy.add_mark(5)
Anatoliy.add_mark(2)
Anatoliy.add_mark(4)
Anatoliy.add_mark(3)
Anatoliy.add_mark(3)
Anatoliy.add_mark(5)

print(Anatoliy.get_marks())
print(Anatoliy.get_average())





Anatoliy = {"name": "Анатолий", "age": 118}

print(Anatoliy["name"], Anatoliy["age"])