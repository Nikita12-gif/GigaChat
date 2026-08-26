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
        USER_PROMPT = {"role": "user", "content": user_content}
        self.MESSAGES.append(USER_PROMPT)
        
        chat = Chat(
            model=self.MODEL,
            messages=self.MESSAGES
        )
        
        self.response =  self.client.chat(chat)
        self.role = self.response.choices[0].message.role
        self.content = self.response.choices[0].message.content
        
        ANSWER = {"role": self.role, "content": self.content}
        self.MESSAGES.append(ANSWER)
        

MODEL = "GigaChat-2"
name_file = "answer.md"
SYSTEM_PROMT = "Ты gigachat. Помогай людям!"


Giga = gigachat_chat(MODEL, SYSTEM_PROMT)


while True:
    promt = input("\nВведи запрос: ")
    
    if promt == "exit":
        break

    Giga.get_response(promt)
    
    print(f"\n\nВам ответил {MODEL}: {Giga.content}")
    print(f"\nПотрачено: {Giga.response.usage.total_tokens}")