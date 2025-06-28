# Basic pattern with new API OpenAI version
import os # for working with venv vars and pathes
from openai import OpenAI # for calling the OpenAI API

client = OpenAI()
#user_prompt = "tell me the names of 10 most famous women in the world history"
def generate_response(text_file, language):
    client=OpenAI()
    system_prompt = "You are an expert in translations, you will be sent an article and you have to translate it into the language suggested"
    completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"Translate the text below into {language}: {text_file}"}
      ]
      )
    return completion.choices[0].message.content.strip()
