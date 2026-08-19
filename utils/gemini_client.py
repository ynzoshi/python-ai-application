"""Gemini APIを呼び出すための共通ヘルパー。"""

from __future__ import annotations

import os
from typing import Iterator, Optional

import streamlit as st
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-3.6-flash"


def get_api_key() -> Optional[str]:
    """サイドバーで入力されたキー、なければ環境変数(.env)から取得する。"""
    key = st.session_state.get("gemini_api_key")
    if key:
        return key
    return os.environ.get("GEMINI_API_KEY")


def has_api_key() -> bool:
    return bool(get_api_key())


def get_client() -> genai.Client:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Gemini APIキーが設定されていません。サイドバーからAPIキーを入力するか、"
            ".envファイルにGEMINI_API_KEYを設定してください。"
        )
    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
) -> str:
    """プロンプトを送信し、生成されたテキストを一括で返す。"""
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""


def stream_text(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
) -> Iterator[str]:
    """プロンプトを送信し、生成されたテキストをストリーミングで返す。"""
    client = get_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_instruction,
    )
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    ):
        if chunk.text:
            yield chunk.text
