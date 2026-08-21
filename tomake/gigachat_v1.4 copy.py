import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat

load_dotenv()


def get_client(APY_KEY):
    return GigaChat(
        base_url="https://api.giga.chat/v1",
        credentials=APY_KEY,
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False
    )

def get_response(client, mess):
    chat = Chat(
        model="GigaChat-2",
        messages=mess
    )
    return client.chat(chat)

def save_response(response, model):
    with open("answer.md", "a", encoding="utf-8") as file:
        file.write(f"\n\nВам овтетил {model}:")
        file.write(response.choices[0].message.content)
        file.write(f"\nПротрачено: {response.usage.total_tokens}")

def main():
    APY_KEY = os.getenv("APY_KEY")
    client = get_client(APY_KEY)
    model = "GigaChat-2"
    mess = [{"role": "system", "content": "Отвечай излишне помпезно"}]
    while True:
        prompt = input("\nВведи запрос: ")
        if prompt == "exit":
            break
        mess.append([{"role": "user", "content": prompt}])
        response = get_response(client, mess)
        
        answer = {"role":response.choices[0].message.role, "content":response.choices[0].message.content}
        mess.append(answer)
        
        print(f"\n\nВам овтетил {model}: {response.choices[0].message.content} {response.choices[0].message.role}")
        print(f"\nПротрачено: {response.usage.total_tokens}")
        
        save_response(response, model)

main()