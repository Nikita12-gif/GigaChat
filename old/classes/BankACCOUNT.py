class BankAccount:
    def __init__(self, owner, PIN, c):
        self.owner = owner
        self.PIN = PIN
        self.balance = 0
        self.c = 6
    def deposit(self, amount):
        if amount <= 0:
            return "Такую сумму положить нельзя"
        self.balance += amount
        return f"Счет успешно пополнен. Текущий баланс:{self.balance}"
        self.c = 6
    def withdraw(self, amount):
        if PIN == self.PIN:
            if amount <= 0:
                return "Такую сумму снять нельзя"
            if amount > self.balance:
                return "Недостаточно средств"
            self.balance -= amount
            return f"Сумма успешно снята. Текущий баланс:{self.balance}"
        else:
            self.c -= 1
            return f"Некорректный ПИН. осталось попыток: {self.c}"
            
        
    def info(self, PIN):
        if PIN == self.PIN:
            print(f"ВЛАДЕЛЕЦ --- {self.owner}")
            print(f"Текущий баланс --- {self.balance}")
        else:
            self.c -= 1
            print(f"Некорректный ПИН. осталось попыток: {self.c}")
            
    
    
    
    
    
USER = BankAccount(input("Введите имя"), input("Введите ПИН-код"))
while True:
    command = input("         Выберите команду и нажмите соответсвующий номер       \n 1 - Положить деньги на счет \n 2 - Снять деньги \n 3. Информация о счете")
    if command == 1:
        print(USER.deposit(int(input("Введите количество денег, которые вы желаете положить на счет:"))))
    elif command == 2:
        print(USER.withdraw(int(input("Введите количество денег, которые вы желаете снять:"))))
    elif command == 3:
          print(USER.withdraw(int(input("Введите ПИН-код:"))))