from __future__ import print_function
import os
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

# config 모듈에서 설정값 가져오기
from config import config

# ----------------------------------------------------------------------
# 서비스 계정 기반 인증 함수
# ----------------------------------------------------------------------
def _get_service_account_credentials():
    """
    서비스 계정 JSON 키 파일을 이용해 Credentials 객체를 생성합니다.
    브라우저 인증이 필요 없고, 완전 자동화에 적합합니다.
    """
    if not os.path.exists(config.GOOGLE_SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(
            f"[❌ 오류] 서비스 계정 키 파일을 찾을 수 없습니다: {config.GOOGLE_SERVICE_ACCOUNT_FILE}\n"
            " - GCP 콘솔(IAM & Admin > Service Accounts)에서 JSON 키를 발급받아 저장하세요.\n"
            " - GOOGLE_SERVICE_ACCOUNT_FILE 환경변수로 경로를 지정하거나,\n"
            "   기본 경로(~/google-secrets/moya-sa.json)에 파일을 두세요."
        )

    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=config.GOOGLE_SCOPES,
    )
    return creds


def get_docs_service():
    """
    Google Docs API 서비스 객체 생성 (서비스 계정 사용)
    """
    creds = _get_service_account_credentials()
    service = build("docs", "v1", credentials=creds)
    return service


def get_drive_service():
    """
    Google Drive API 서비스 객체 생성 (서비스 계정 사용)
    """
    creds = _get_service_account_credentials()
    service = build("drive", "v3", credentials=creds)
    return service

def find_document_id_by_title(title, drive_service):
    """
    Google Drive에서 제목으로 문서를 검색하고 ID를 반환합니다.
    """
    print(f"🔍 Google Drive에서 제목 '{title}' 문서 검색 중...")

    # Drive API v3를 사용하여 문서 검색 (mimeType으로 Google Docs 필터링)
    # q='name="제목" and mimeType="application/vnd.google-apps.document"'
    results = drive_service.files().list(
        q=f"name='{title}' and mimeType='application/vnd.google-apps.document' and trashed=false",
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])

    if files:
        # 첫 번째 검색 결과의 ID를 반환합니다.
        print(f"✅ 문서 발견! Document ID: {files[0]['id']}")
        return files[0]['id']

    print("❌ 문서 발견 실패. 새로 생성합니다.")
    return None


def create_document(title, docs_service):
    """
    새 Google Doc을 생성합니다.
    """
    document = docs_service.documents().create(
        body={"title": title}
    ).execute()
    document_id = document.get('documentId')
    print(f"🎉 새 문서 생성 완료! Document ID: {document_id}")
    return document_id


def append_content_to_doc(document_id, report_title, content, docs_service):
    """
     특정 Google Doc에 내용을 추가(Append)합니다.
     """
    try:
        # 1. 문서의 현재 상태를 가져와서 삽입 위치(endIndex)를 계산합니다.
        doc = docs_service.documents().get(documentId=document_id).execute()

        # 문서의 마지막 content element의 endIndex (문서의 최종 길이)
        # 문서가 비어있을 경우를 대비하여 안전하게 1로 초기화합니다.
        full_doc_end_index = doc['body']['content'][-1].get('endIndex', 1)

        # Google Docs API는 append 시, 문서의 최종 endIndex 바로 앞(endIndex - 1)에 삽입해야
        # 깔끔하게 내용이 추가되며, 최종 섹션/문단 마커를 건드리지 않습니다.
        # 인덱스 1은 문서의 시작 위치이므로 예외 처리합니다.
        insertion_index = full_doc_end_index
        if full_doc_end_index > 1:
            insertion_index = full_doc_end_index - 1

        # 2. 새로운 보고서 블록 구성
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 이전 내용과의 구분을 위한 구분선 및 새 제목 추가
        section_header = f"\n\n{config.REPORT_SEPARATOR}\n\n[{timestamp}] {report_title}\n\n"
        full_content = section_header + content

        # 길이 계산을 위한 변수
        header_len_prefix = len(f"\n\n{config.REPORT_SEPARATOR}\n\n")  # 구분선 길이만
        title_len = len(f"[{timestamp}] {report_title}")

        # 3. 문서 업데이트 요청 목록
        requests = [
            # 전체 내용을 문서의 끝에 삽입
            {
                'insertText': {
                    # 수정된 삽입 인덱스 사용
                    'location': {'index': insertion_index},
                    'text': full_content
                }
            },
            # 삽입된 제목에 스타일 업데이트 (굵게, 크기 조정)
            {
                'updateTextStyle': {
                    'range': {
                        # 제목이 시작하는 위치 = insertion_index + 구분선 길이
                        'startIndex': insertion_index + header_len_prefix,
                        # 제목이 끝나는 위치 = insertion_index + 구분선 길이 + 제목 길이
                        'endIndex': insertion_index + header_len_prefix + title_len
                    },
                    'textStyle': {
                        'bold': True,
                        'fontSize': {'magnitude': 16, 'unit': 'PT'}
                    },
                    'fields': 'bold,fontSize'
                }
            },
        ]

        # API 호출 실행
        docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

        print(f"✅ 문서 업데이트 성공! 내용이 문서 끝에 추가되었습니다.")
        return True

    except Exception as e:
        print(f"[❌ 문서 업데이트 오류] {e}")
        return False
def save_report_to_doc(report_content: str) -> bool:
    """
    보고서 내용을 Google Doc에 저장하는 메인 함수입니다.
    문서가 없으면 생성하고, 있으면 내용을 추가합니다.
    """
    docs_service = get_docs_service()
    drive_service = get_drive_service()

    try:
        # 1. 문서 ID 찾기 또는 생성
        doc_id = find_document_id_by_title(config.REPORT_DOCUMENT_TITLE, drive_service)

        if not doc_id:
            # 문서가 없으면 생성
            doc_id = create_document(config.REPORT_DOCUMENT_TITLE, docs_service)

        if doc_id:
            # 2. 내용 추가
            append_content_to_doc(
                document_id=doc_id,
                report_title=config.REPORT_DOCUMENT_TITLE,
                content=report_content,
                docs_service=docs_service
            )
            print(f"문서 URL: https://docs.google.com/document/d/{doc_id}/edit")
            return True
        else:
            print("❌ 문서 ID를 찾거나 생성하는 데 실패했습니다.")
            return False

    except Exception as e:
        print(f"[❌ API 오류] Google 서비스 연결 중 오류 발생: {e}")
        return False


if __name__ == "__main__":
    # ⚠️ 이 파일의 기존 __main__ 코드는 테스트 목적으로만 사용되며,
    # 실제 문서 저장 로직은 save_report_to_doc 함수를 통해 실행됩니다.

    # 테스트를 위한 내용
    test_content = (
        f"[{datetime.now().strftime('%Y-%m-%d')}] "
        "이것은 find_or_create/append 로직을 테스트하기 위한 내용입니다. "
    )

    print("--- Google Docs API 통합 테스트 시작 ---")
    # 메인 함수 호출 (실제로는 gemini_analyst.py에서 호출됩니다.)
    save_report_to_doc(test_content)
    print("--- 테스트 완료 ---")