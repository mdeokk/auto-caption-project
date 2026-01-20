from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai. [결과는 한국어로 표시]",
  store=True,
)

print(response.output_text);