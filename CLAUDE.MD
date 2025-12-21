# Economic Summary Bot

AI 기반 경제 분석 보고서 자동 생성 봇입니다. Gemini API를 사용하여 실시간 경제 동향과 환율을 분석하고, Google Docs에 자동으로 보고서를 저장합니다.

## 주요 기능

- 🤖 **AI 기반 경제 분석**: Gemini 2.5 Flash 모델을 사용한 실시간 경제 동향 분석
- 🔍 **Google 검색 통합**: 최신 경제 뉴스와 데이터를 실시간으로 검색
- 📊 **미국 주요 경제 지표**: S&P500, Nasdaq 등 주요 증시 동향 분석
- 💱 **환율 정보**: 한국 원화 기준 실시간 환율 정보 제공
- 📝 **Google Docs 연동**: 분석 결과를 자동으로 Google Docs에 저장
- ⚙️ **설정 관리**: 중앙화된 설정 파일로 쉬운 관리

## 프로젝트 구조

```
economic-summary-bot/
├── config.py                # 중앙화된 설정 관리
├── financial_summary.py     # 메인 경제 분석 스크립트
├── google_doc_utils.py      # Google Docs API 유틸리티
├── test_googlesearch.py     # Google 검색 테스트 스크립트
├── requirements.txt         # Python 의존성
├── Dockerfile              # 컨테이너 설정
└── README.md               # 프로젝트 설명서
```

## 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Google Cloud 설정

1. **Google Cloud Console**에서 새 프로젝트 생성
2. **Google Docs API**와 **Google Drive API** 활성화
3. **서비스 계정** 생성 및 JSON 키 파일 다운로드
4. 서비스 계정에 적절한 권한 부여

### 3. 환경 설정

#### 로컬 환경
```bash
# 서비스 계정 키 파일 경로 설정
export GOOGLE_SERVICE_ACCOUNT_FILE="~/google-secrets/moya-sa.json"

# 보고서 문서 제목 설정 (선택사항)
export REPORT_DOCUMENT_TITLE="AI 금융 분석 보고서"

# Gemini 모델 설정 (선택사항)
export GEMINI_MODEL="gemini-2.5-flash"
```

#### Docker 환경
```bash
docker run -e GOOGLE_SERVICE_ACCOUNT_FILE=/secrets/service-account.json \
           -v /path/to/service-account.json:/secrets/service-account.json \
           economic-summary-bot
```

## 사용법

### 메인 경제 분석 실행

```bash
python financial_summary.py
```

실행하면:
1. 최신 경제 뉴스와 데이터를 Google 검색으로 수집
2. Gemini AI가 전문적인 금융 투자가 관점에서 분석
3. 분석 결과를 콘솔에 출력
4. Google Docs에 자동으로 보고서 저장

### Google 검색 테스트

```bash
python test_googlesearch.py
```

### 개별 모듈 테스트

```bash
python google_doc_utils.py
```

## 설정 파일 (config.py)

모든 설정값은 `config.py`에서 중앙 관리됩니다:

```python
class Config:
    # Google Service Account 설정
    GOOGLE_SERVICE_ACCOUNT_FILE = "~/google-secrets/moya-sa.json"

    # Google Docs 설정
    REPORT_DOCUMENT_TITLE = "AI 금융 분석 보고서"

    # Gemini API 설정
    GEMINI_MODEL = "gemini-2.5-flash"

    # 기타 설정들...
```

### 환경변수로 설정 오버라이드

- `GOOGLE_SERVICE_ACCOUNT_FILE`: 서비스 계정 파일 경로
- `REPORT_DOCUMENT_TITLE`: 보고서 문서 제목
- `GEMINI_MODEL`: 사용할 Gemini 모델
- `LOG_LEVEL`: 로그 레벨 설정
- `DATA_DIR`: 데이터 디렉토리 경로
- `BACKUP_DIR`: 백업 디렉토리 경로

## API 요구사항

### Google APIs
- **Google Docs API**: 문서 생성 및 편집
- **Google Drive API**: 문서 검색 및 관리

### Gemini API
- **Google Generative AI**: 경제 분석 및 콘텐츠 생성
- **Google Search Grounding**: 실시간 검색 데이터 통합

## 보고서 내용

생성되는 보고서에는 다음 내용이 포함됩니다:

1. **현재 날짜 및 시각**
2. **미국 주요 경제 지표**
   - S&P500, Nasdaq 등 주요 증시 동향
   - 주요 경제 이벤트의 시장 영향 분석
3. **한국 원화 환율**
   - 최신 은행고시 기준 환율
4. **전문가 관점의 분석**
   - 금융 투자가 시각에서의 종합 분석

## Docker 사용

### 이미지 빌드
```bash
docker build -t economic-summary-bot .
```

### 컨테이너 실행
```bash
docker run -e GOOGLE_SERVICE_ACCOUNT_FILE=/secrets/service-account.json \
           -v /path/to/service-account.json:/secrets/service-account.json \
           economic-summary-bot
```

## 주의사항

1. **API 키 보안**: 서비스 계정 JSON 파일을 안전하게 보관하세요
2. **API 사용량**: Gemini API와 Google APIs의 사용량 제한을 확인하세요
3. **권한 설정**: 서비스 계정에 Google Docs 및 Drive 접근 권한이 있는지 확인하세요

## 트러블슈팅

### 인증 오류
- 서비스 계정 JSON 파일 경로가 올바른지 확인
- 파일 권한이 적절한지 확인 (600 권장)

### API 오류
- Google Cloud Console에서 필요한 API들이 활성화되었는지 확인
- API 사용량 한도를 초과하지 않았는지 확인

### 문서 생성 오류
- 서비스 계정이 Google Drive에 문서를 생성할 권한이 있는지 확인
- 기존 문서에 대한 편집 권한이 있는지 확인

## 개발 정보

- **Python 버전**: 3.8+
- **주요 의존성**:
  - `google-generativeai`: Gemini AI API
  - `google-auth`: Google 인증
  - `google-api-python-client`: Google APIs 클라이언트

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Made with ❤️ by AI Assistant**