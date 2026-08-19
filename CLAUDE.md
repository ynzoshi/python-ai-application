# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal-use Streamlit app that wraps the Gemini API as a suite of Japanese-language writing tools (blog posts, email replies, summarization, proofreading/rewriting, title/catchcopy generation, translation). No database, no auth — intentionally out of scope per project requirements.

## Commands

```bash
# Setup (venv already created at ./venv, targets system Python 3.9.6 — no newer
# Python was available on this machine when the project was created)
source venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app.py          # serves at http://localhost:8501

# Syntax-check all files (no test suite exists in this project)
python -m py_compile app.py pages/*.py utils/*.py
```

API key setup: copy `.env.example` to `.env` and set `GEMINI_API_KEY`, or paste the key into the sidebar text input at runtime (session-only, never persisted).

Note: when running `streamlit run` via a Bash tool call, the process is not reachable from the user's actual browser (sandboxed session) — verify the command exits cleanly via `py_compile`/log inspection, but ask the user to run and check the app in their own terminal rather than curling it yourself.

## Architecture

**Page structure is Streamlit's file-based multi-page routing**, not custom routing code: `app.py` is the home page, and every file under `pages/` becomes a sidebar entry automatically, ordered by the numeric prefix in the filename (`1_📝_...py`, `2_📧_...py`, etc.). The emoji in the filename becomes the sidebar icon. Adding a new tool means adding a new numbered file to `pages/`.

**Every page follows the same shape** (see any file in `pages/` as a template):
1. `st.set_page_config(...)` + `render_sidebar()` from `utils/ui.py`
2. An `st.form(...)` collecting the tool's inputs
3. On submit, build a prompt string and call `generate_text()` from `utils/gemini_client.py`, storing the result in `st.session_state[...]` (this is what makes the result survive Streamlit's rerun-on-interaction model — without session_state the result would disappear the moment the user touches another widget)
4. Render the stored result via `render_result()` from `utils/ui.py`, which shows Markdown + a copy-friendly `st.text_area` + a download button

**`utils/gemini_client.py`** is the only place that talks to the Gemini API (`google-genai` SDK, model `gemini-2.5-flash` by default). `get_api_key()` checks `st.session_state["gemini_api_key"]` (sidebar input) first, then falls back to the `GEMINI_API_KEY` env var. `generate_text()` and `stream_text()` both raise `RuntimeError` with a Japanese user-facing message when no key is available — pages catch this and surface it via `st.error()`, so don't add key-existence checks elsewhere.

**`utils/ui.py`** holds the two cross-page UI pieces: `render_sidebar()` (API key input + status) and `render_result()` (standardized output display). Keep new pages consistent with these rather than reimplementing output rendering inline.

**Prompts are Japanese, built inline in each page** as an f-string with `#`-delimited sections (topic, tone, constraints, output rules). When adding a tool or adjusting behavior, edit the prompt template in that page's file directly — there's no shared prompt-template system.
