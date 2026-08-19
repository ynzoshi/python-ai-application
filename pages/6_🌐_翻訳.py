"""翻訳ツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")
render_sidebar()

st.title("🌐 翻訳")
st.caption("文章をトーンを保ったまま指定した言語に翻訳します。")

with st.form("translate_form"):
    text = st.text_area("翻訳したい文章", height=250, placeholder="ここに翻訳したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox(
            "翻訳先の言語",
            ["英語", "日本語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"],
        )
    with col2:
        tone = st.selectbox("トーン", ["自然な標準的表現", "フォーマル・ビジネス向け", "カジュアル・口語的"])

    submitted = st.form_submit_button("翻訳する", use_container_width=True, type="primary")

if submitted:
    if not text.strip():
        st.warning("翻訳したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を{target_lang}に翻訳してください。

# 翻訳対象の文章
{text}

# トーン
{tone}

# 出力ルール
- 直訳ではなく、意味とニュアンスを保ったまま自然な{target_lang}にする
- 翻訳結果のみを出力し、原文や説明は付けない
"""
        with st.spinner("翻訳しています..."):
            try:
                result = generate_text(prompt, temperature=0.3)
                st.session_state["translate_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "translate_result" in st.session_state:
    render_result(st.session_state["translate_result"], download_filename="translation.txt")
