import os
import json
import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


class Gemini:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
        }

        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        self.gemini = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=self.safety_settings,
        )

    def generate(self, prompt):
        try:
          response = self.gemini.generate_content(prompt, safety_settings=self.safety_settings).text
          return response
        except Exception as e:
          response = self.gemini.generate_content(prompt, safety_settings=self.safety_settings).candidates[0].content.parts[0].text
          return response

    def start_chat(self):
        return self.gemini.start_chat(history=[])
