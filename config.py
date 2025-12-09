# -*- coding: utf-8 -*-
"""
Config 파일
모든 설정값과 파일 경로를 중앙에서 관리합니다.
"""

import os


class Config:
    """애플리케이션 설정 클래스"""

    # Google Service Account 설정
    GOOGLE_SERVICE_ACCOUNT_FILE = os.path.expanduser(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "~/google-secrets/moya-sa.json")
    )

    # Google Docs 설정
    REPORT_DOCUMENT_TITLE = os.getenv("REPORT_DOCUMENT_TITLE", "AI 금융 분석 보고서")

    # Google API 스코프
    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive",
    ]

    # Gemini API 설정
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # 보고서 설정
    REPORT_SEPARATOR = "-" * 80

    # 로그 설정
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # 데이터 디렉토리 설정 (필요시 추가)
    DATA_DIR = os.path.expanduser(
        os.getenv("DATA_DIR", "~/economic-summary-bot/data")
    )

    # 백업 디렉토리 설정 (필요시 추가)
    BACKUP_DIR = os.path.expanduser(
        os.getenv("BACKUP_DIR", "~/economic-summary-bot/backups")
    )


# 기본 설정 객체 생성
config = Config()