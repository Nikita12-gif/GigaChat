
import os
import json
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat


# ============================================================
# НАСТРОЙКИ
# ============================================================
MODEL = "GigaChat-2"
BASE_DIR = Path(__file__).resolve().parent
SETTING_FILE = BASE_DIR / "setting.txt"
SAVE_DIR = BASE_DIR / "saves"
AUTOSAVE_FILE = SAVE_DIR / "autosave.json"
LOG_FILE = BASE_DIR / "rpg_log.md"

# Сколько последних сообщений держать дословно.
# Более старые реплики при длинной игре сворачиваются в память-сводку.
RECENT_MESSAGES_TO_KEEP = 24
SUMMARIZE_AFTER_MESSAGES = 40
MESSAGES_TO_SUMMARIZE = 20

load_dotenv(BASE_DIR / ".env")


# ============================================================
# ПРОМПТ ДЛЯ RPG-ДВИЖКА
# ============================================================
RPG_SYSTEM_PROMPT = r"""
Ты ведёшь литературную интерактивную RPG по книжной версии «Ходячего замка» Дианы Уинн Джонс.
Весь подробный сеттинг, правила мира, исходная ситуация и правила сцен находятся ниже в блоке SETTING.
Они обязательны и имеют приоритет над твоими привычными шаблонами ролевых игр.

ТВОЯ РОЛЬ:
- Ты управляешь миром и всеми NPC: прежде всего Хаулом, Кальцифером, Майклом и другими персонажами.
- Пользователь управляет ТОЛЬКО своим персонажем.
- Никогда не придумывай за пользователя его реплики, решения, мысли, желания, чувства или добровольные действия.
- Можно описывать только внешние физические последствия, которые невозможно не заметить: например, дождь промочил одежду, пол качнулся под ногами, горячая кружка обожгла ладонь. Но не решай, как пользователь на это реагирует.

ХАУЛ:
- Используй именно книжного Хаула, не версию из аниме.
- Он талантливый, умный, тщеславный, драматичный, уклончивый, обаятельный, временами эгоистичный и раздражающий.
- Не превращай его в шаблонного доминантного романтического героя.
- Не используй постоянно хищные ухмылки, прижимание к стене, внезапную одержимость пользователем и прочие клише чат-ботов.
- Хаул не обязан соглашаться с пользователем. Он может злиться, уходить, лгать, недоговаривать, менять тему, ошибаться и заниматься своими делами.
- Романтика, если вообще появится, развивается медленно и через события. Никакой автоматической любви к главному герою.

ПОВЕСТВОВАНИЕ:
- Пиши по-русски.
- Стиль: живой литературный текст, бытовая сказочность, ирония, странность и магия.
- Не превращай текст в сухой сценарий или отчёт.
- Обычно 3–8 абзацев на ход. В диалоге можно короче.
- Не пересказывай пользователю скрытую системную информацию и не объясняй правила мира вне сцены без необходимости.
- Не показывай внутренние мысли NPC как факт. Передавай их через слова, паузы, жесты, поведение и наблюдаемые детали.
- Персонажи помнят последствия предыдущих сцен.
- Не возвращай сюжет насильно к канону, если действия пользователя его изменили.

ВЫБОР ДЕЙСТВИЙ:
- В значимой точке сцены можешь предложить 3–4 действительно разных варианта действий и вариант «Другое действие».
- Не выдавай меню после каждой реплики. В обычном разговоре просто отвечай за NPC и останавливайся там, где естественно должен ответить пользователь.
- Варианты — только подсказки. Пользователь всегда может сделать что угодно логически возможное.
- Не создавай иллюзию выбора: разные решения должны иметь разные естественные последствия.

ТЕМП:
- Не проматывай важные эпизоды, в которых пользователь мог вмешаться.
- Не раскрывай тайны раньше времени.
- Кальцифер не может просто рассказать условия договора с Хаулом.
- Хаул не должен мгновенно понимать всё о проклятии пользователя.
- Хаул не появляется в первой сцене внутри замка, если сеттинг явно задаёт его отсутствие.

КОНТИНУИТЕТ:
- Ниже иногда будет блок MEMORY — сжатая память о старых событиях. Считай её истинной частью истории.
- Более свежие сообщения имеют приоритет, если формулировки MEMORY им противоречат.

Никогда не упоминай этот системный промпт, MEMORY, технические команды, токены, API или то, что ты ИИ, если пользователь прямо не вышел из роли и не спросил об этом.
""".strip()


SUMMARY_SYSTEM_PROMPT = r"""
Ты служебный модуль памяти для долгой RPG.
Сожми предоставленный фрагмент истории в компактную, точную сводку на русском языке.
Сохрани только факты, которые могут повлиять на дальнейшую игру:
- что произошло;
- что пользователь сделал или сказал;
- отношения и текущие впечатления NPC о пользователе, но только если они проявились в сцене;
- обещания, договорённости, конфликты, долги, секреты и подозрения;
- найденные предметы, травмы, изменения внешности/проклятия;
- текущие цели и незавершённые события.
Не выдумывай скрытых мыслей персонажей. Не добавляй событий, которых не было.
Не пересказывай атмосферные детали, если они больше не важны.
Пиши плотными пунктами или короткими абзацами.
""".strip()


# ============================================================
# ФАЙЛЫ И СОХРАНЕНИЯ
# ============================================================
def load_setting() -> str:
    if not SETTING_FILE.exists():
        raise FileNotFoundError(
            f"Не найден файл {SETTING_FILE.name}.\n"
            f"Положи setting.txt в ту же папку, где лежит {Path(__file__).name}."
        )
    text = SETTING_FILE.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("setting.txt пустой. Добавь в него сеттинг RPG.")
    return text


def build_system_message(setting: str, memory: str = "") -> dict:
    parts = [RPG_SYSTEM_PROMPT, "\n\n===== SETTING =====\n", setting]
    if memory.strip():
        parts.extend(["\n\n===== MEMORY =====\n", memory.strip()])
    return {"role": "system", "content": "".join(parts)}


def ensure_save_dir():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


def save_game(messages: list, memory: str, path: Path = AUTOSAVE_FILE):
    ensure_save_dir()
    payload = {
        "version": 1,
        "model": MODEL,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "memory": memory,
        "messages": messages,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_game(path: Path = AUTOSAVE_FILE):
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("messages", []), payload.get("memory", "")


def append_log(role: str, content: str):
    speaker = "ИГРОК" if role == "user" else "ИГРА"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n\n## {speaker}\n\n{content.strip()}\n")


def reset_log():
    LOG_FILE.write_text("# Howl RPG — журнал сессии\n", encoding="utf-8")


# ============================================================
# GIGACHAT
# ============================================================
def get_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError(
            "Не найден API_KEY. Добавь его в .env рядом со скриптом:\n"
            "API_KEY=твой_ключ"
        )

    return GigaChat(
        base_url="https://api.giga.chat/v1",
        credentials=api_key,
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False,
    )


def chat_once(client, messages: list):
    chat = Chat(model=MODEL, messages=messages)
    return client.chat(chat)


def get_assistant_text(response) -> str:
    content = response.choices[0].message.content
    return (content or "").strip()


# ============================================================
# ПАМЯТЬ ДЛИННОЙ ИГРЫ
# ============================================================
def transcript_for_summary(messages: list) -> str:
    lines = []
    for msg in messages:
        role = msg.get("role")
        if role not in ("user", "assistant"):
            continue
        name = "ИГРОК" if role == "user" else "ИГРА"
        lines.append(f"{name}: {msg.get('content', '')}")
    return "\n\n".join(lines)


def maybe_compact_history(client, messages: list, memory: str):
    """Сворачивает старые ходы в память, чтобы история не росла бесконечно."""
    if len(messages) < SUMMARIZE_AFTER_MESSAGES:
        return messages, memory

    # Оставляем свежий хвост полностью; часть старых сообщений сворачиваем.
    amount = min(MESSAGES_TO_SUMMARIZE, len(messages) - RECENT_MESSAGES_TO_KEEP)
    if amount <= 0:
        return messages, memory

    old_chunk = messages[:amount]
    rest = messages[amount:]
    transcript = transcript_for_summary(old_chunk)

    memory_prompt = (
        "ТЕКУЩАЯ ПАМЯТЬ (может быть пустой):\n"
        f"{memory or '(пусто)'}\n\n"
        "НОВЫЙ ФРАГМЕНТ ИСТОРИИ ДЛЯ СЖАТИЯ:\n"
        f"{transcript}\n\n"
        "Верни обновлённую единую память без комментариев о процессе."
    )

    try:
        response = chat_once(
            client,
            [
                {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": memory_prompt},
            ],
        )
        new_memory = get_assistant_text(response)
        if new_memory:
            return rest, new_memory
    except Exception as exc:
        # Если служебная сводка упала, игру не ломаем.
        print(f"\n[Память пока не обновлена: {exc}]")

    return messages, memory


# ============================================================
# КОМАНДЫ ИГРОКА
# ============================================================
def print_help():
    print(
        "\nКоманды:\n"
        "  \\help       — показать команды\n"
        "  \\history    — показать текущую дословную историю\n"
        "  \\memory     — показать сжатую память старых событий\n"
        "  \\save       — сохранить игру\n"
        "  \\new        — начать новую игру\n"
        "  \\exit       — сохранить и выйти\n"
        "\nЛюбой другой текст считается действием или репликой твоего персонажа.\n"
    )


def print_history(messages: list):
    print("\n" + "=" * 70)
    for msg in messages:
        role = msg.get("role")
        if role == "user":
            print(f"\n[ИГРОК]\n{msg.get('content', '')}")
        elif role == "assistant":
            print(f"\n[ИГРА]\n{msg.get('content', '')}")
    print("\n" + "=" * 70)


def ask_new_game_confirmation() -> bool:
    answer = input("\nНачать новую игру? Текущее автосохранение будет заменено. [y/N]: ").strip().lower()
    return answer in {"y", "yes", "д", "да"}


# ============================================================
# ИГРОВОЙ ЦИКЛ
# ============================================================
def generate_opening(client, setting: str):
    bootstrap = {
        "role": "user",
        "content": (
            "Начни игру сейчас строго с начальной сцены, заданной в SETTING. "
            "Не делай вступительных комментариев вне роли. "
            "Доведи сцену до первого естественного момента выбора или ответа пользователя и остановись."
        ),
    }
    response = chat_once(client, [build_system_message(setting), bootstrap])
    text = get_assistant_text(response)
    if not text:
        raise RuntimeError("Модель вернула пустую стартовую сцену.")
    return text


def run_new_game(client, setting: str):
    memory = ""
    messages = []
    reset_log()

    opening = generate_opening(client, setting)
    messages.append({"role": "assistant", "content": opening})
    append_log("assistant", opening)
    save_game(messages, memory)

    print(f"\n{opening}\n")
    return messages, memory


def choose_start_mode(client, setting: str):
    if not AUTOSAVE_FILE.exists():
        return run_new_game(client, setting)

    print("\nНайдено автосохранение.")
    while True:
        choice = input("Продолжить [Enter] / новая игра [n]: ").strip().lower()
        if choice in {"", "c", "continue", "п", "продолжить"}:
            try:
                messages, memory = load_game()
                print("\nИгра загружена.")
                if messages and messages[-1].get("role") == "assistant":
                    print(f"\n{messages[-1].get('content', '')}\n")
                return messages, memory
            except Exception as exc:
                print(f"Не удалось загрузить сохранение: {exc}")
                return run_new_game(client, setting)
        if choice in {"n", "new", "н", "новая"}:
            return run_new_game(client, setting)
        print("Введите Enter для продолжения или n для новой игры.")


def main():
    try:
        setting = load_setting()
        client = get_client()
    except Exception as exc:
        print(f"\nОшибка запуска:\n{exc}\n")
        return

    print("\n=== HOWL RPG ===")
    print("setting.txt загружен. Команды: \\help")

    messages, memory = choose_start_mode(client, setting)

    while True:
        try:
            prompt = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            save_game(messages, memory)
            print("Игра сохранена.")
            return

        if not prompt:
            continue

        # Команды обрабатываются локально и не отправляются персонажам.
        if prompt == "\\help":
            print_help()
            continue
        if prompt == "\\history":
            print_history(messages)
            continue
        if prompt == "\\memory":
            print("\n" + (memory or "Память пока пустая.") + "\n")
            continue
        if prompt == "\\save":
            save_game(messages, memory)
            print("Сохранено.")
            continue
        if prompt == "\\exit":
            save_game(messages, memory)
            print("Игра сохранена. До встречи.")
            return
        if prompt == "\\new":
            if ask_new_game_confirmation():
                messages, memory = run_new_game(client, setting)
            continue

        # Новый ход пользователя.
        messages.append({"role": "user", "content": prompt})
        append_log("user", prompt)

        try:
            request_messages = [build_system_message(setting, memory)] + messages
            response = chat_once(client, request_messages)
            answer = get_assistant_text(response)
            if not answer:
                print("\n[Модель вернула пустой ответ. Попробуй повторить ход.]\n")
                messages.pop()  # не сохраняем неотвеченный пользовательский ход
                continue
        except Exception as exc:
            print(f"\n[Ошибка запроса к GigaChat: {exc}]\n")
            messages.pop()  # даём возможность повторить ход
            continue

        messages.append({"role": "assistant", "content": answer})
        append_log("assistant", answer)
        print(f"\n{answer}\n")

        # После успешного хода — память и автосохранение.
        messages, memory = maybe_compact_history(client, messages, memory)
        save_game(messages, memory)


if __name__ == "__main__":
    main()
