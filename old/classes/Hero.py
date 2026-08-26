import random
class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.invent=[]
    def get_hp(self):
        return self.hp
    def take_damage(self, damage):
        if (self.hp - damage) > 0:
            self.t = self.hp - damage
            return (self.t)
        return "Вы убиты"
    def add_item(self, item):
        self.invent.append(item)
    def show_inventory(self):
        if self.invent == []:
            return "Инвентарь пуст"
        return self.invent
    
Hero = Hero(input("Введите имя героя:"))
Hero.take_damage(random.randint(1, 10000))
print(Hero.get_hp())
print(Hero.show_inventory())
Hero.add_item("snowball")
Hero.add_item("parrot")
print(*Hero.show_inventory())