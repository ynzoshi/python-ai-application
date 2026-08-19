"""AIライティングツール - ホームページ。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.ui import render_sidebar

load_dotenv()

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
)

render_sidebar()

st.title("✍️ AIライティングツール")
st.caption("Gemini APIを使った個人用のライティング支援ツール集です。左のメニューから使いたい機能を選んでください。")

st.divider()

tools = [
    ("📝", "ブログ記事作成", "pages/1_📝_ブログ記事作成.py", "トピックやキーワードから、見出し付きのブログ記事の下書きを生成します。"),
    ("📧", "メール返信作成", "pages/2_📧_メール返信作成.py", "受け取ったメールと返信の意図を入力するだけで、ビジネスメールの返信文を作成します。"),
    ("📄", "文章要約", "pages/3_📄_文章要約.py", "長い文章を一文・箇条書き・段落など好きな形式で要約します。"),
    ("✨", "校正・リライト", "pages/4_✨_校正リライト.py", "誤字脱字のチェックや、文体・トーンの調整（丁寧に／簡潔に、など）を行います。"),
    ("🏷️", "タイトル・キャッチコピー生成", "pages/5_🏷️_タイトルキャッチコピー生成.py", "記事や商品の説明から、複数のタイトル・キャッチコピー案を生成します。"),
    ("🌐", "翻訳", "pages/6_🌐_翻訳.py", "文章を指定した言語に、トーンを保ったまま翻訳します。"),
]

cols = st.columns(2)
for i, (icon, name, path, desc) in enumerate(tools):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(f"{icon} {name}")
            st.write(desc)
            st.page_link(path, label=f"{name}を開く", icon="➡️")

st.divider()
with st.expander("📌 使い方 / APIキーの取得方法"):
    st.markdown(
        """
1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセスし、Gemini APIキーを取得します。
2. 取得したキーを、プロジェクト直下の `.env` ファイルに以下の形式で保存するか、
   左サイドバーの入力欄に直接貼り付けてください。

   ```
   GEMINI_API_KEY=あなたのAPIキー
   ```

3. 左のメニューから使いたいツールを選び、必要事項を入力して生成ボタンを押してください。

このアプリはデータベースや認証機能を持たない個人利用向けのツールです。生成結果は保存されないため、
必要な場合はダウンロードボタンから保存してください。
        """
    )
