"""文章要約ツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
render_sidebar()

st.title("📄 文章要約")
st.caption("長い文章を貼り付けると、指定した形式で要約します。")

with st.form("summary_form"):
    text = st.text_area("要約したい文章", height=300, placeholder="ここに要約したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "要約のスタイル",
            ["3行程度の要約", "一文で要約", "箇条書きで要約", "段落形式の要約"],
        )
    with col2:
        detail = st.select_slider("詳しさ", options=["簡潔", "標準", "やや詳しく"], value="標準")

    submitted = st.form_submit_button("要約する", use_container_width=True, type="primary")

if submitted:
    if not text.strip():
        st.warning("要約したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を要約してください。

# 要約対象の文章
{text}

# 要約のスタイル
{style}

# 詳しさ
{detail}

# 出力ルール
- 原文の重要なポイントを漏らさず、簡潔にまとめる
- 指定されたスタイルに厳密に従う
- 要約結果のみを出力し、前置きや「要約:」等のラベルは付けない
"""
        with st.spinner("要約を作成しています..."):
            try:
                result = generate_text(prompt, temperature=0.3)
                st.session_state["summary_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "summary_result" in st.session_state:
    render_result(st.session_state["summary_result"], download_filename="summary.txt")
