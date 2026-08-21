import os
import random
import json
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Function, FunctionParameters
from datetime import datetime

load_dotenv()

def winwinwin():
    cur = [0] * 50 + [1]
    if random.choice(cur) == 0:
        return "Выпало 0. Ты проиграл бетмен"
    else:
        return "Выпала 1. Эмм, ладно чувак. Ты крут"
    
def multi(a, b):
    # Приводим типы, так как аргументы из API приходят строками
    a_val = float(a)
    b_val = float(b)
    r = a_val * b_val
    # Возвращаем только чистое значение
    return r
    
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_client():
    return GigaChat(
        base_url="https://api.giga.chat/v1",
        credentials=os.getenv("API_KEY"),
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False
    )

# Универсальная обработка всех функций по принципу Tool Calls
def handle_tool_calls(response, messages):
    message = response.choices[0].message
    if hasattr(message, 'function_call') and message.function_call:
        func_name = message.function_call.name
        
        # Выполняем нужную Python-функцию
        if func_name == "get_current_time":
            result = get_current_time()
        elif func_name == "winwinwin":
            result = winwinwin()
        elif func_name == "multi":
            args = message.function_call.arguments
            # arguments могут быть dict или строкой
            if isinstance(args, str):
                args = json.loads(args)
            result = multi(args.get('a'), args.get('b'))
        else:
            return False
            
        # Добавляем ПРАВИЛЬНЫЙ ответ функции в историю
        messages.append({
            "role": "tool", 
            "name": func_name,
            "content": str(result)
        })
        
        # Делаем повторный запрос к API, теперь модель знает результат
        follow_up_chat = Chat(
            model="GigaChat-2",
            messages=messages,
            functions=[
                Function(name="get_current_time", description="Получить текущее время", parameters=FunctionParameters(type="object", properties={}, required=[])),
                Function(name="winwinwin", description="Пользователь получает случайное значение", parameters=FunctionParameters(type="object", properties={}, required=[])),
                Function(name="multi", description="Перемножает числа", parameters=FunctionParameters(
                    type="object",
                    properties={
                        "a": {"type": "number", "description": "Число один"},
                        "b": {"type": "number", "description": "Число два"}
                    },
                    required=["a", "b"]
                ))
            ],
            function_call="auto"
        )
        
        final_response = client.chat(follow_up_chat)
        
        print(f"\n\nВам овтетил GigaChat-2")
        print(f"\n{final_response.choices[0].message.content}")
        print(f"\nПротрачено: {final_response.usage.total_tokens}")
        
        save_response(final_response, "GigaChat-2", result)
        return True
        
    return False

def save_response(response, model, function_result=None):
    with open("answer.md", "a", encoding="utf-8") as f:
        if function_result is not None:
            f.write(f"\n\nВам овтетил {model}: Результат функции -> {function_result}")
        else:
            f.write(f"\n\nВам овтетил {model}: \n{response.choices[0].message.content}")
        f.write(f"\nПротрачено: {response.usage.total_tokens}")

def main():
    global client
    client = get_client()
    MESSEGES = [{"role": "system", "content": "Ты — полезный ассистент."}]
    
    while True:
        prompt = input("\nВведи запрос: ")
        if prompt.lower() == "exit":
            print("Спасибо что обратились ко мне!")
            break
            
        USER_PROMT = {"role": "user", "content": prompt}
        MESSEGES.append(USER_PROMT)
        
        response = client.chat(Chat(model="GigaChat-2", messages=MESSEGES, function_call="auto"))
        
        # Если сработал инструмент, handler сам всё вывел и сохранил
        if handle_tool_calls(response, MESSEGES):
            continue
            
        # Обычный ответ
        answer = {"role": response.choices[0].message.role, "content": response.choices[0].message.content}
        MESSEGES.append(answer)
        
        print(f"\n\nВам овтетил GigaChat-2")
        print(f"\n{response.choices[0].message.content}")
        print(f"\nПротрачено: {response.usage.total_tokens}")
        
        save_response(response, "GigaChat-2")

if __name__ == "__main__":
    main()