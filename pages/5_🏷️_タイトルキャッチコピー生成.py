"""タイトル・キャッチコピー生成ツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="タイトル・キャッチコピー生成", page_icon="🏷️", layout="wide")
render_sidebar()

st.title("🏷️ タイトル・キャッチコピー生成")
st.caption("記事の内容や商品説明から、複数のタイトル・キャッチコピー案を生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事の内容・商品説明・トピック",
        height=200,
        placeholder="タイトルを付けたい内容や、記事の要約・トピックを入力してください",
    )

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "スタイル",
            ["SEOを意識した検索されやすいタイトル", "インパクト重視のキャッチコピー", "疑問形で興味を引く", "数字を使った具体的なタイトル"],
        )
    with col2:
        num_candidates = st.slider("案の数", min_value=3, max_value=10, value=5)

    submitted = st.form_submit_button("タイトル案を生成", use_container_width=True, type="primary")

if submitted:
    if not content.strip():
        st.warning("内容やトピックを入力してください。")
    else:
        prompt = f"""あなたはコピーライティングのプロです。以下の内容に対して、「{style}」を意識したタイトル・キャッチコピーを{num_candidates}個提案してください。

# 内容・トピック
{content}

# 出力ルール
- 番号付きの箇条書きリストで出力する
- それぞれ簡潔で、内容を的確に表すものにする
- 前置きや説明文は付けず、リストのみを出力する
"""
        with st.spinner("タイトル案を生成しています..."):
            try:
                result = generate_text(prompt, temperature=0.9)
                st.session_state["title_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "title_result" in st.session_state:
    render_result(st.session_state["title_result"], download_filename="title_candidates.txt")
