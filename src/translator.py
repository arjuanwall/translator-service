import os
import openai
import json

def translate_content(content: str) -> tuple[bool, str]:
    if not content.strip():
        return True, content

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key

    client = openai.OpenAI(api_key=api_key)

    def get_language(post: str) -> str:
        context = (
            "You are a language detection model. "
            "Given a piece of text, respond with the language name only, e.g., 'English', 'French', 'German'."
            "If the language is gibberish or random characters, respond with 'English'."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": f"Which language is this text in?\n\n{post}"}
            ]
        )

        language = response.choices[0].message.content.strip()

        return language

    def get_translation(post: str) -> str:
        context = (
            "You are a helpful assistant specialized in translation."
            "Your task is to read any text (in any language) and return its English translation."
            "If the text is already in English, you should return it as is."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": f"Translate this text to English:\n\n{post}"}
            ]
        )

        translation = response.choices[0].message.content.strip()
        print(translation)

        return translation
    
    if get_language(content) == "English":
        return True, content
    else:
        translation = get_translation(content)
        return False, translation