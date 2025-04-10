import unittest
from src.translator import translate_content

class TestTranslator(unittest.TestCase):

    def test_chinese(self):
        is_english, translated_content = translate_content("这是一条中文消息")
        self.assertFalse(is_english)
        self.assertEqual(translated_content, "This is a Chinese message")

    def test_french(self):
        is_french, translated_content = translate_content("Ceci est un message en français")
        self.assertFalse(is_french)
        self.assertEqual(translated_content, "This is a French message")

    def test_llm_normal_response(self):
        # Test that a normal LLM response is correctly identified as English
        llm_response = "The weather today is sunny and warm."
        is_english, translated_content = translate_content(llm_response)
        self.assertTrue(is_english)
        self.assertEqual(translated_content, "The weather today is sunny and warm.")
        
        # Test with a longer, more complex response
        complex_response = "Artificial intelligence has made significant progress in recent years. Natural language processing models can now understand and generate human-like text with remarkable accuracy."
        is_english, translated_content = translate_content(complex_response)
        self.assertTrue(is_english)
        self.assertTrue(translated_content.startswith("人工智能在近年来取得了重大进展"))
        
        # Test with response containing numbers and special characters
        mixed_response = "The temperature is 25°C, and there's a 30% chance of rain tomorrow."
        is_english, translated_content = translate_content(mixed_response)
        self.assertTrue(is_english)
        self.assertIn("温度", translated_content)
        self.assertIn("30%", translated_content)
        
        # Test with Spanish text
        spanish_text = "Hola, ¿cómo estás? Espero que tengas un buen día."
        is_english, translated_content = translate_content(spanish_text)
        self.assertFalse(is_english)
        self.assertIn("Hello", translated_content)
        self.assertIn("good day", translated_content)
        
        # Test with French text
        french_text = "Bonjour, comment allez-vous? Je suis ravi de vous rencontrer."
        is_english, translated_content = translate_content(french_text)
        self.assertFalse(is_english)
        self.assertIn("Hello", translated_content)
        self.assertIn("meet", translated_content)
        
        # Test with German text
        german_text = "Guten Tag. Ich lerne gerade Programmierung und künstliche Intelligenz."
        is_english, translated_content = translate_content(german_text)
        self.assertFalse(is_english)
        self.assertIn("programming", translated_content)
        self.assertIn("artificial intelligence", translated_content)

    def test_llm_gibberish_response(self):
        # Test with nonsensical text that doesn't belong to any language
        gibberish = "asdf qwerty zxcv poiu lkjh mnbv asdfasdf"
        is_english, translated_content = translate_content(gibberish)
        self.assertTrue(is_english)  # Should default to treating as English
        self.assertEqual(translated_content, gibberish)  # Should attempt translation
        
        # Test with random characters and symbols
        random_chars = "!@#$ %^&* ()_+ <>?:"
        is_english, translated_content = translate_content(random_chars)
        self.assertTrue(is_english)  # Should default to treating as English
        self.assertNotEqual(translated_content, random_chars)
        
        # Test with mixed gibberish containing some real words
        mixed_gibberish = "hello asdfghjkl world qwertyuiop"
        is_english, translated_content = translate_content(mixed_gibberish)
        self.assertTrue(is_english)
        self.assertTrue("你好" in translated_content or "世界" in translated_content)  # Should translate the real words

if __name__ == '__main__':
    unittest.main()
    