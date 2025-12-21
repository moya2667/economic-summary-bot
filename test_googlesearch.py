from google import genai
from google.genai import types

# config 모듈에서 설정값 가져오기
from config import config, setup_logging, get_logger

# 로깅 설정
setup_logging()
logger = get_logger(__name__)

logger.info("Google Search 테스트 시작")
logger.info("Gemini 클라이언트 초기화 중...")
client = genai.Client()

logger.info("Google Search grounding tool 설정 중...")
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

generation_config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

logger.info(f"사용 모델: {config.GEMINI_MODEL}")
logger.info("Google Search를 사용한 Gemini API 요청 전송 중...")
response = client.models.generate_content(
    model=config.GEMINI_MODEL,
    contents="Who won the euro 2024?",
    config=generation_config,
)

logger.info("Gemini API 응답 수신 완료")
logger.info(f"응답 내용: {response.text}")
logger.info("Google Search 테스트 완료")