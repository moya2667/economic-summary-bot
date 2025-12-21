# -*- coding: utf-8 -*-
"""
Config 파일
모든 설정값과 파일 경로를 중앙에서 관리합니다.
"""

import os
import logging


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


def setup_logging(log_level=None):
    """로깅 설정을 초기화합니다."""
    if log_level is None:
        log_level = Config.LOG_LEVEL

    # 로그 레벨 설정
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # 로깅 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 기본 로깅 설정
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format
    )

    return logging.getLogger(__name__)


def get_logger(name=None):
    """로거 인스턴스를 반환합니다."""
    if name is None:
        name = __name__
    return logging.getLogger(name)


# 기본 설정 객체 생성
config = Config()