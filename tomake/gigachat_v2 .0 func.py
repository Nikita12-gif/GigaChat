import os
import random
import json
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Function, FunctionParameters
from datetime import datetime

load_dotenv()

def winwinwin():
    cur = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    if random.choice(cur) == 0:
        return ["winwinwin", "Выпало 0. Ты проиграл бетмен"]
    else:
        return ["winwinwin", "Выпала 1. Эмм, ладно чувак. Ты крут"]
    
def multi(a, b):
    r = int(a) * int(b)
    return ["multi", r]
    
def print_MASSAGES(MESSEGES):
    for elem in MESSEGES:
         print(elem)

def get_current_time():
    return ["get_current_time", datetime.now().strftime("%H:%M:%S")]

def get_client():
    return GigaChat(
        base_url="https://api.giga.chat/v1",
        credentials=os.getenv("API_KEY"),
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False
    )
def get_response(client, MESSEGES):
    chat = Chat(
        model="GigaChat-2",
        
        messages=MESSEGES,
        
        functions=[
            Function(
                name="get_current_time",
                description="Получить текущее время",
                parameters=FunctionParameters(
                    type="object",
                    properties={},
                    required=[]
                )
            ),
            Function(
                name="winwinwin",
                description="Пользователь получает случайное значение",
                parameters=FunctionParameters(
                    type="object",
                    properties={},
                    required=[]
                )
            ),
            Function(
                name="multi",
                description="Перемножает числа",
                parameters=FunctionParameters(
                    type="object",
                    properties={"a": {"type": "number",
                                      "decription" : "Число один"},
                                "b": {"type": "number",
                                      "decription" : "Число два"}},
                    required=["a", "b"]
                )
            )
        ],
        function_call="auto"
    )
    return client.chat(chat)

def handle_function_call(response):
    if hasattr(response.choices[0].message, 'function_call') and response.choices[0].message.function_call:
        func_name = response.choices[0].message.function_call.name
        if func_name == "get_current_time":
            return get_current_time()
        elif func_name == "winwinwin":
            return winwinwin()
        elif func_name == "multi":
            args = response.choices[0].message.function_call.arguments
            return multi(args['a'], args['b'])
    return None

def save_response(response, model, function_result=None):
    with open("answer.md", "a", encoding="utf-8") as f:
        if function_result:
            f.write(f"\n\nВам овтетил {model}: Сейчас {function_result}")
        else:
            f.write(f"\n\nВам овтетил {model}: \n{response.choices[0].message.content}")
        f.write(f"\nПротрачено: {response.usage.total_tokens}")

def main():
    client = get_client()
    model = "GigaChat-2"
    MESSEGES = [{"role": "system", "content": ""}]
    
    while True:
        prompt = input("\nВведи запрос: ")
        print()
        USER_PROMT = {"role": "user", "content": prompt}
        MESSEGES.append(USER_PROMT)
        
        if prompt == "exit":
            print("Спасибо что обратились ко мне!")
            break
            
        response = get_response(client, MESSEGES)
        answer = {"role": response.choices[0].message.role, "content": response.choices[0].message.content}
        MESSEGES.append(answer)
        
        function_result = handle_function_call(response)
        if function_result[0] == "get_current_time":
            print(f"\n\nСейчас {function_result[1]}")
            FUNCTION_CALL_MESSAGE = {"role": "function",
                                     "content": response.choices[0].message.content,
                                     "function_call": {
                                        "name": "get_current_time",
                                        "arguments": response.choices[0].message.function_call.arguments}}
            MESSEGES.append(FUNCTION_CALL_MESSAGE)
            MESSEGES.append({"role": response.choices[0].message.role,
                            "content": str(function_result[1])})  
        elif function_result[0] == "winwinwin":
            print(f"{function_result[1]}")
            FUNCTION_CALL_MESSAGE = {"role": "function",
                                     "content": response.choices[0].message.content,
                                     "function_call": {
                                        "name": "winwinwin",
                                        "arguments": response.choices[0].message.function_call.arguments}}
            MESSEGES.append(FUNCTION_CALL_MESSAGE)
            MESSEGES.append({"role": response.choices[0].message.role,
                            "content": str(function_result[1])})   
        elif function_result[0] == "multi":
            print(f"{function_result[1]}")
            FUNCTION_CALL_MESSAGE = {"role": "function",
                                     "content": response.choices[0].message.content,
                                     "function_call": {
                                        "name": "multi",
                                        "arguments": response.choices[0].message.function_call.arguments}}
            MESSEGES.append(FUNCTION_CALL_MESSAGE)
            MESSEGES.append({"role": response.choices[0].message.role,
                            "content": str(function_result[1])})
            
        print(f"\n\nВам овтетил {model}")
        print(f"\n{response.choices[0].message.content}")
        
        print(f"\nПротрачено: {response.usage.total_tokens}")
        
        print_MASSAGES(MESSEGES)
        
        save_response(response, model, function_result)

if __name__ == "__main__":
    main()