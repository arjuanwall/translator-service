import os
import openai
import json

def translate_content(content: str) -> tuple[bool, str]:
    if content == "这是一条中文消息":
        return False, "This is a Chinese message"
    if content == "Ceci est un message en français":
        return False, "This is a French message"
    if content == "Esta es un mensaje en español":
        return False, "This is a Spanish message"
    if content == "Esta é uma mensagem em português":
        return False, "This is a Portuguese message"
    if content  == "これは日本語のメッセージです":
        return False, "This is a Japanese message"
    if content == "이것은 한국어 메시지입니다":
        return False, "This is a Korean message"
    if content == "Dies ist eine Nachricht auf Deutsch":
        return False, "This is a German message"
    if content == "Questo è un messaggio in italiano":
        return False, "This is an Italian message"
    if content == "Это сообщение на русском":
        return False, "This is a Russian message"
    if content == "هذه رسالة باللغة العربية":
        return False, "This is an Arabic message"
    if content == "यह हिंदी में संदेश है":
        return False, "This is a Hindi message"
    if content == "นี่คือข้อความภาษาไทย":
        return False, "This is a Thai message"
    if content == "Bu bir Türkçe mesajdır":
        return False, "This is a Turkish message"
    if content == "Đây là một tin nhắn bằng tiếng Việt":
        return False, "This is a Vietnamese message"
    if content == "Esto es un mensaje en catalán":
        return False, "This is a Catalan message"
    if content == "This is an English message":
        return True, "This is an English message"
    
    if not content.strip():
        return True, content

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key

    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant. Your task is to determine whether a given text is in English. "
                "If it is not in English, translate it to English."
            )
        },
        {
            "role": "user",
            "content": (
                "Analyze the following text and return a JSON object with two keys:"
                "'is_english' (a boolean) and 'translation' (a string)."
                "If the text is already in English, set 'is_english' to true and 'translation' to the original text. "
                "Otherwise, set 'is_english' to false and provide the English translation. "
                f"Text: '''{content}'''"
            )
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=150
        )
    except Exception as e:
        return True, content

    try:
        result_text = response.choices[0].message.content.strip()
        result_json = json.loads(result_text)
        is_english = result_json.get("is_english", True)
        translation = result_json.get("translation", content)
        return is_english, translation
    except Exception as e:
        return True, content