from google import genai
from google.genai import types

# config 모듈에서 설정값 가져오기
from config import config

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

generation_config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents="Who won the euro 2024?",
    config=generation_config,
)

print(response.text)