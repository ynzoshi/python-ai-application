"""ブログ記事作成ツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
render_sidebar()

st.title("📝 ブログ記事作成")
st.caption("トピックや条件を入力すると、見出し付きのブログ記事の下書きを生成します。")

with st.form("blog_form"):
    topic = st.text_input("記事のトピック・タイトル案", placeholder="例: 在宅勤務で生産性を上げる5つの方法")
    keywords = st.text_input(
        "SEOで狙いたいキーワード（カンマ区切り、任意）",
        placeholder="例: 在宅勤務, タイムマネジメント, 集中力",
        help="タイトル・導入文・見出しに自然に含めるよう指示します。1〜3語程度がおすすめです。",
    )
    audience = st.text_input("想定読者（任意）", placeholder="例: リモートワークを始めたばかりの会社員")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["親しみやすい", "フォーマル", "専門的", "カジュアル"])
    with col2:
        length = st.select_slider(
            "文字数の目安",
            options=["短め（400字程度）", "標準（800字程度）", "長め（1500字程度）"],
            value="標準（800字程度）",
        )

    extra = st.text_area("その他の指示（任意）", placeholder="例: 箇条書きを多めに使う、具体例を入れる など")
    submitted = st.form_submit_button("記事を生成", use_container_width=True, type="primary")

if submitted:
    if not topic.strip():
        st.warning("記事のトピックを入力してください。")
    else:
        system_instruction = (
            "あなたはSEO（検索エンジン最適化）に精通したプロのブログライター兼SEOライターです。"
            "読者にとって読みやすく有益な文章を書きながら、検索エンジンにも評価されやすい構成・"
            "キーワードの使い方を徹底してください。不自然なキーワードの詰め込みは避けてください。"
        )
        prompt = f"""以下の条件でSEOを意識したブログ記事の下書きをMarkdown形式で作成してください。

# トピック
{topic}

# SEOで狙いたいキーワード
{keywords or "指定なし"}

# 想定読者
{audience or "指定なし"}

# トーン
{tone}

# 文字数の目安
{length}

# その他の指示
{extra or "特になし"}

# SEOの出力ルール
- 記事タイトルにメインキーワードを自然な形で含める
- 導入文（最初の100〜150文字程度）にメインキーワードを含め、読者の検索意図に応える内容にする
- 見出し(H2/H3)にも関連キーワードや共起語を自然に散りばめる
- 箇条書きや太字を適度に使い、流し読みでも要点が伝わる構成にする
- 記事の最後に、読者の次の行動を促す一文（まとめ）を入れる
- 本文の一番上に「## meta description案」という見出しを付け、120〜160文字程度の要約文を1つ提示する

# 出力ルール
- meta description案の後に、記事タイトル(H1相当)、導入文、複数の見出し(H2/H3)、結論の構成を続ける
- Markdown形式のみを出力し、前置きや説明文は付けない
"""
        with st.spinner("記事を生成しています..."):
            try:
                result = generate_text(prompt, system_instruction=system_instruction, temperature=0.8)
                st.session_state["blog_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "blog_result" in st.session_state:
    render_result(st.session_state["blog_result"], download_filename="blog_post.md")
