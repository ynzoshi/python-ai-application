# AIライティングツール

Gemini APIを使った個人用のAIライティング支援ツール集です。データベースや認証機能は持たず、ローカルで動かすことを想定しています。

## 機能

- 📝 **ブログ記事作成** - トピックやキーワードから見出し付きの記事下書きを生成
- 📧 **メール返信作成** - 受信メールと返信の意図から返信文を作成
- 📄 **文章要約** - 長文を一文・箇条書き・段落など好きな形式で要約
- ✨ **校正・リライト** - 誤字脱字チェック、文体・トーンの調整
- 🏷️ **タイトル・キャッチコピー生成** - 記事や商品説明から複数案を生成
- 🌐 **翻訳** - トーンを保ったまま多言語に翻訳

## セットアップ

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.env.example` を `.env` にコピーし、[Google AI Studio](https://aistudio.google.com/apikey) で取得したAPIキーを設定してください。

```bash
cp .env.example .env
# .env を編集して GEMINI_API_KEY=... を設定
```

APIキーは `.env` の代わりに、アプリ起動後にサイドバーから直接入力することもできます（この場合ブラウザセッション内でのみ保持され、保存されません）。

## 起動

```bash
source venv/bin/activate
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。
