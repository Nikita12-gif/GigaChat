class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def __str__(self):
        return f"Point: ({self.x}, {self.y})"
    
A = Point(0,0)
B = Point(3,4)
C = Point(-1,5)
print(A.distance_to(B))
print(B.distance_to(C))
print(A.__str__)