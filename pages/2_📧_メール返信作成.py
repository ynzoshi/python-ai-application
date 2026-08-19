"""メール返信作成ツール。"""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

from utils.gemini_client import generate_text
from utils.ui import render_result, render_sidebar

load_dotenv()

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
render_sidebar()

st.title("📧 メール返信作成")
st.caption("受信したメールと返信したい内容を入力すると、返信メールの文面を作成します。")

with st.form("email_form"):
    original_email = st.text_area(
        "受信したメール本文",
        height=200,
        placeholder="ここに返信したいメールの本文を貼り付けてください",
    )
    intent = st.selectbox(
        "返信の意図",
        ["依頼を承諾する", "依頼を断る", "質問・確認する", "お礼を伝える", "謝罪する", "その他（自由入力）"],
    )
    key_points = st.text_area(
        "伝えたい内容・要点（任意）",
        placeholder="例: 来週の火曜であれば対応可能、金額は要相談 など",
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["丁寧なビジネス敬語", "ややカジュアル", "非常にフォーマル"])
    with col2:
        length = st.select_slider("長さ", options=["簡潔", "標準", "やや詳しく"], value="標準")

    submitted = st.form_submit_button("返信文を生成", use_container_width=True, type="primary")

if submitted:
    if not original_email.strip():
        st.warning("受信したメール本文を入力してください。")
    else:
        prompt = f"""あなたはビジネスメール作成のプロです。以下の受信メールに対する返信メールの文面を作成してください。

# 受信したメール
{original_email}

# 返信の意図
{intent}

# 伝えたい内容・要点
{key_points or "特になし（意図に沿って自然に作成）"}

# トーン
{tone}

# 長さ
{length}

# 出力ルール
- 件名は不要。本文のみを出力する
- 宛名（〇〇様）、書き出しの挨拶、本文、結びの挨拶、署名の順で自然なメール文面にする
- 署名部分は「[お名前]」のようにプレースホルダーにする
- 日本語のビジネスメールとして適切な敬語・表現を使う
"""
        with st.spinner("返信文を生成しています..."):
            try:
                result = generate_text(prompt, temperature=0.6)
                st.session_state["email_result"] = result
            except RuntimeError as e:
                st.error(str(e))

if "email_result" in st.session_state:
    render_result(st.session_state["email_result"], download_filename="email_reply.txt")
