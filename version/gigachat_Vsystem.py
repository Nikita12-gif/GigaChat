import os
from dotenv import load_dotenv

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()


def client():
    client = GigaChat(
    base_url="https://api.giga.chat/v1",
    credentials=APY_KEY,
    scope="GIGACHAT_API_PERS",
    verify_ssl_certs=False)
    
    
def chat():
    chat = Chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": PROMPT}]
    )
    
APY_KEY = os.getenv("APY_KEY")

MODEL = "GigaChat-2"


client = client()

key = 1
while key:
    PROMPT = input("\nВведи запрос: ")
    
    SAVE_FILE = open("answer.md", "a",encoding="utf-8")
    
    
    if PROMPT == "exit":
        break

    chat = Chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": PROMPT}]
    )

    resp = client.chat(chat)
    print("\n\nВам овтетил", MODEL + ":", resp.choices[0].message.content)
    print("\nПротрачено: ", resp.usage.total_tokens)
    SAVE_FILE.write("\n\nВам овтетил " + MODEL + ": \n" + resp.choices[0].message.content)
    SAVE_FILE.write("\nПротрачено: " + str(resp.usage.total_tokens))
    SAVE_FILE.close()
