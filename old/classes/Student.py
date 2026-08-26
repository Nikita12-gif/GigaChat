class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.self_grades = []
        
    def __str__(self):
        return f"Имя: {self.name}, Id: {self.student_id}"
        
    def add_grade(self, mark):
        self.self_grades.append(mark)
    def get_average(self):
        if self.self_grades == []:
            return 0.0
        self.t = sum(self.self_grades) / len(self.self_grades)
        return t
    def is_excellent(self):
        if self.t >= 4.5:
            return True
        return False
        
Niki = Student(input("Введите имя:"), int(input("Введите id:")))
Niki.add_grade(5)
Niki.add_grade(2)
Niki.add_grade(4)
Niki.add_grade(3)
Niki.add_grade(3)
Niki.add_grade(5)
print(Niki.get_average())
print(Niki.is_excellent())