class Imb:
    def init(self, name, mass, leng):
        self.name=name
        self.mass=mass
        self.leng=leng/100

        self.imb=self.calc_imb()

    def str(self):
        return f"name: {self.name}, mass: {self.mass}, leng: {self.leng}, imb1: {self.imb1}, imb2: {self.imb2}"


    def calc_imb(self):
        self.Q = int(self.mass/(self.leng))
        if self.Q <= 18.5:
            return f"Ваш индекс массы: {Q}, вы дрыщ"
        elif 18.5<= self.Q <= 24.9:
            return f"Ваш индекс массы: {Q}, вcе ок"
        elif 25<= self.Q <= 30:
            return f"Ваш индекс массы: {Q}, можно похудеть(преджирение)"
        elif 30<= self.Q <= 35:
            return f"Ваш индекс массы: {Q}, пора худеть(1 стадия ожирения)"
        elif 35<= self.Q <= 40:
            return f"Ваш индекс массы: {Q}, хватит есть бургеры(2 стадия ожирения)"
        elif 40<= self.Q:
            return f"Ваш индекс массы: {Q}, вы не влазите в дверной проем(3 стадия ожирения)"

Anatoliy=Imb("Анатолий", 74, 178)

print(Anatoliy.imb)
