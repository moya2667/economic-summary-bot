# 1. 베이스 이미지 선택 (필요시 3.10, 3.12 등으로 변경 가능)
FROM python:3.12

# 2. 환경 변수 설정 (버퍼링 off, UTF-8)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Seoul \
    LANG=C.UTF-8

# 3. 작업 디렉토리 생성
WORKDIR /app

# 4. requirements 먼저 복사 및 설치 (레이어 캐시 활용)
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY config.py /app/config.py
COPY google_doc_utils.py /app/google_doc_utils.py
COPY financial_summary.py /app/financial_summary.py
COPY test_googlesearch.py /app/test_googlesearch.py

# 6. 환경변수 설정
# 실제 서비스 계정 파일은 빌드 시 COPY 하지 않고, run 시 volume으로 마운트하는 것을 추천
ENV GOOGLE_SERVICE_ACCOUNT_FILE="/secrets/moya-sa.json" \
    REPORT_DOCUMENT_TITLE="AI 금융 분석 보고서" \
    GEMINI_MODEL="gemini-2.5-flash" \
    LOG_LEVEL="INFO"

# 7. 컨테이너 실행 시 기본 명령
CMD ["python", "financial_summary.py"]
