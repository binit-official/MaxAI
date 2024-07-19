from openai import OpenAI
from config import apikey
client = OpenAI(api_key=apikey)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages="write an email",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
