import sys
from google import genai
from google.genai import types

try:
    # 'google_doc_utils.py' 파일에서 함수를 가져옵니다.
    from google_doc_utils import save_report_to_doc
except ImportError:
    # google_doc_utils.py 파일이 없거나 오류가 있을 경우를 대비한 Placeholder 함수
    def save_report_to_doc(content):
        print("\n[⚠️ 경고] 'google_doc_utils.py' 파일을 찾을 수 없거나 인증 오류가 있습니다. Google Doc 업데이트 기능을 건너뜁니다.")
        print("해당 파일을 생성하고 필요한 라이브러리 및 인증(client_secret.json)을 설정해주세요.")
        return False

try:
    import google.genai
except ImportError:
    print("\n" + "=" * 60)
    print("이 코드를 실행하려면 구글의 AI 라이브러리가 필요해.")
    print("터미널(명령 프롬프트)을 열고 아래 명령어를 입력해서 설치해줘:")
    print("\nhttps://ai.google.dev/gemini-api/docs?hl=ko")
    print("\n설치하고 다시 실행하면 잘 될 거야! 화이팅! 💪")
    print("=" * 60 + "\n")
    sys.exit()

# -----------------------------------------------------------------------------
# 1. API 키 설정
# 발급받은 키를 아래 "YOUR_API_KEY_HERE" 자리에 넣으세요.
# -----------------------------------------------------------------------------
client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

def analyze_market_with_gemini():
    """
    Gemini API를 사용하여 실시간 경제 동향과 환율을 분석하는 함수
    """
    print("🤖AI 비서가 최신 경제 뉴스를 검색 중이야... 잠시만 기다려줘! (약 5~10초 소요)")

    # -------------------------------------------------------------------------
    # prompt
    # -------------------------------------------------------------------------

    user_query = """    
    구글 검색 통해서 오늘 날짜를 가져오고, 
    오늘 날짜 기준으로 최근 일주일간 두 가지 질문에 대해 전문적인 금융 투자가의 관점에서 답변해줘. 
    **답변을 생성할 때, 반드시 구글 검색 결과만 사용해야 하며, 모델의 내부 지식(Internal Knowledge)을 사용해서 환율을 추정하거나 추측하지 마세요.**
   
    1. 미국 주요 경제 지표 발표 내용과 미국 증시(S&P500, Nasdaq)의 흐름과 등락율도 요약해줘. 
       주요 이벤트가 있었다면 그것이 시장에 미친 영향도 포함해줘.

    2. 구글 검색 통해, 가장 최근 날짜의 은행고시 기준 한국 원화 환율을 표현해라 
    """

    # -------------------------------------------------------------------------
    # 4. AI에게 질문 던지기 (검색 결과 바탕으로 생성)
    # -------------------------------------------------------------------------
    # 검색 도구 설정: generate_content 호출 시점에 도구를 전달합니다.
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )

    try:
        # tools 인자를 generate_content 함수에 직접 전달합니다.
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=user_query, config=config
        )

        # 결과 출력
        print("\n" + "=" * 50)
        print(" 📊 [Moya Financial Report by gemini] ")
        print("=" * 50)
        print(response.text)
        print("=" * 50)

        # ---------------------------------------------------------------------
        # 5. 🚀 Google Doc 업데이트 실행
        # ---------------------------------------------------------------------
        # 문서 생성/추가 로직이 save_report_to_doc 함수 안에 모두 포함되어 있습니다.
        save_success = save_report_to_doc(response.text)

        if save_success:
            print("\n🎉 보고서 생성이 완료되었으며, Google Doc에 내용이 성공적으로 추가되었습니다.")
        else:
            print("\n⚠️ 보고서 생성이 완료되었으나, Google Doc 저장 과정에서 오류가 발생했습니다.")
        # ---------------------------------------------------------------------

        # (참고) 검색에 사용된 출처가 있다면 표시
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata.grounding_chunks:
                print("\n🔍 참조한 웹사이트:")
                for chunk in candidate.grounding_metadata.grounding_chunks:
                    if chunk.web:
                        print(f"- {chunk.web.title}: {chunk.web.uri}")

    except Exception as e:
        print(f"\n앗, 에러가 났어 ㅠㅠ: {str(e)}")


if __name__ == "__main__":
    analyze_market_with_gemini()
