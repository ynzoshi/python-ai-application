"""ページ間で共通のUI部品。"""

from __future__ import annotations

import os

import streamlit as st

from utils.gemini_client import DEFAULT_MODEL


def render_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ 設定")

        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key:
            st.success("✅ .env からAPIキーを読み込み済み")
        else:
            key_input = st.text_input(
                "Gemini APIキー",
                type="password",
                value=st.session_state.get("gemini_api_key", ""),
                help="Google AI Studio (https://aistudio.google.com/apikey) で取得したAPIキーを入力してください",
            )
            if key_input:
                st.session_state["gemini_api_key"] = key_input
            else:
                st.warning("APIキーが未設定です")

        st.caption(f"使用モデル: `{DEFAULT_MODEL}`")
        st.divider()
        st.caption("入力したAPIキーはこのブラウザセッション内でのみ使用され、保存・送信されません。")


def render_result(text: str, *, download_filename: str) -> None:
    """生成結果をMarkdown表示 + コピー用テキストエリア + ダウンロードボタンで表示する。"""
    st.subheader("生成結果")
    st.markdown(text)
    with st.expander("コピー用プレーンテキスト"):
        st.text_area("生成結果（コピー用）", text, height=250, label_visibility="collapsed")
    st.download_button(
        "テキストファイルとしてダウンロード",
        text,
        file_name=download_filename,
        use_container_width=True,
    )
