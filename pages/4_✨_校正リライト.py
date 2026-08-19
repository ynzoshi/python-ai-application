"""文章の校正・リライトツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="校正・リライト", page_icon="✨", layout="wide")
render_sidebar()

st.title("✨ 校正・リライト")
st.caption("文章の誤字脱字チェックや、トーン・文体の調整を行います。")

with st.form("rewrite_form"):
    text = st.text_area("校正・リライトしたい文章", height=250, placeholder="ここに文章を貼り付けてください")

    purpose = st.selectbox(
        "やりたいこと",
        [
            "誤字脱字・文法だけをチェックする",
            "もっと簡潔にする",
            "もっと丁寧にする",
            "もっとカジュアルにする",
            "もっと説得力のある表現にする",
            "ビジネス文書らしく整える",
        ],
    )
    show_diff_note = st.checkbox("主な変更点の説明も表示する", value=True)

    submitted = st.form_submit_button("校正・リライトする", use_container_width=True, type="primary")

if submitted:
    if not text.strip():
        st.warning("校正・リライトしたい文章を入力してください。")
    else:
        diff_instruction = (
            "修正後の文章の後に「## 主な変更点」という見出しを付け、変更した箇所とその理由を箇条書きで説明する。"
            if show_diff_note
            else "修正後の文章のみを出力し、説明は付けない。"
        )
        prompt = f"""あなたは日本語の文章校正・編集のプロです。以下の文章に対して「{purpose}」という目的で校正・リライトしてください。

# 対象の文章
{text}

# 出力ルール
- 元の文章の意味・意図はできるだけ変えない
- 修正後の文章はMarkdown形式で出力する
- {diff_instruction}
"""
        with st.spinner("校正・リライトしています..."):
            try:
                result = generate_text(prompt, temperature=0.4)
                st.session_state["rewrite_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "rewrite_result" in st.session_state:
    render_result(st.session_state["rewrite_result"], download_filename="rewrite.md")
