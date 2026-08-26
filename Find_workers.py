import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat

load_dotenv()

class gigachat_chat:
    def __init__(self, MODEL: str = "GigaChat-2", SYSTEM_PROMT: str = "Ты gigathat. Помогай людям!") -> None:
        self.SYSTEM_PROMT = SYSTEM_PROMT
        
        self.MODEL = MODEL
        self.API_KEY = os.getenv("API_KEY")
        self.client = self.create_client()
        self.MESSAGES = self.create_MESSAGES()
        self.response = None
        self.role = None
        self.content = None
        
    def create_MESSAGES(self):
        return [{"role": "system", "content": self.SYSTEM_PROMT}]
        

    def create_client(self):
        return GigaChat(
            base_url="https://api.giga.chat/v1",
            credentials=self.API_KEY,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False
        )
    
    def get_response(self, user_content) -> None:
        self.MIDDLE_LIST = []
        for i in range(3):
            print("мяу")
            user_content += "\n".join(list_of_employees[(i * 35):((i + 1) * 35) % 100])
            USER_PROMPT = {"role": "user", "content": user_content}
            self.MESSAGES.append(USER_PROMPT)
                
            chat = Chat(
                model=self.MODEL,
                messages=self.MESSAGES
            )
            
            self.response =  self.client.chat(chat)
            self.role = self.response.choices[0].message.role
            self.content = self.response.choices[0].message.content
            
        
            self.MIDDLE_LIST.append(self.content)
            print(self.MIDDLE_LIST)
            
        self.MESSAGES.append({"role": self.role, "content": self.MIDDLE_LIST})
        
        
        self.MESSAGES.append({"role": "user", "content": "Выведи мне имена и информацию о 3 сотрудников с самыми высокими баллами и напиши почему они подойдут"})
        
        chat = Chat(
            model=self.MODEL,
            messages=self.MESSAGES
        )
        
        self.response =  self.client.chat(chat)
        self.role = self.response.choices[0].message.role
        self.content = self.response.choices[0].message.content
        
        self.MESSAGES.append({"role": self.role, "content": self.content})
        
        ANSWER = {"role": self.role, "content": self.content}
        self.MESSAGES.append(ANSWER)
        
        

MODEL = "GigaChat-2"
name_file = "answer.md"
SYSTEM_PROMT = "Оценивай каждого сотрудника исходя из запроса пользователя и ставь оценку от 1 до 100 с пояснением для каждого работника. Всегда проверяй людей в конце списка, вдруг они хорошо подойдут"
with open("data.csv", "r", encoding='utf-8') as LIST:
    list_of_employees = LIST.readlines()



Giga = gigachat_chat(MODEL, SYSTEM_PROMT)


while True:
    promt = input("\nВведи запрос: ")
    
    if promt == "exit":
        break

    Giga.get_response(promt)
    
    print(f"\n\nВам ответил {MODEL}: {Giga.content}")
    print(f"\nПотрачено: {Giga.response.usage.total_tokens}")