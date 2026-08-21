import os
from gigachat import GigaChat
from dotenv import load_dotenv
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()

APY_KEY = os.getenv("APY_KEY")

client = GigaChat(
    base_url="https://api.giga.chat/v1",
    credentials="APY_KEY",
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False
    
)
while True:
    print("##############")
    PROMPT = input("Введите ваш запрос:")
    if PROMPT=="exit":
        break

    chat = Chat(
        model="GigaChat-2",
        messages=[Messages(role=MessagesRole.USER, content=PROMPT)]
    )

    resp = client.chat(chat)
    ## print(resp)
    print(resp.choices[0].message.content) 
    print()
    print("Использованная вами модель:", resp.model)
    print()
    print("Количество затраченных токенов:", resp.usage.total_tokens)