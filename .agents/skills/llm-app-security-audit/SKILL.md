---
name: llm-app-security-audit
description: Audits Streamlit apps, LLM-backed apps (Gemini/OpenAI/Claude/etc.), and general API applications for security issues, then produces a severity-ranked Markdown security report. Covers hardcoded secrets and .env/gitignore hygiene, XSS via unsafe_allow_html or other unsafe rendering, injection (SQL/command/deserialization), path traversal in upload/download handlers, LLM-specific risks (prompt injection, unsafe handling of model output, excessive agency, sensitive data sent to third-party model APIs, missing rate/cost limits), dependency CVEs, and Streamlit/deployment config (XSRF/CORS, session_state isolation, error/log leakage). Use this whenever the user asks to "security check," "audit," "review for vulnerabilities," or "is this safe to deploy" for a Streamlit app, an LLM/AI wrapper app, or a Python API backend — even if they only name one file or one worry (e.g. "is my API key handling okay?") rather than asking for a full audit. Trigger proactively before a user deploys or open-sources this kind of app.
---

# LLM / Streamlit / API App Security Audit

## Why this exists

Apps that wrap an LLM API behind a lightweight UI (Streamlit, Gradio, a small
FastAPI backend, etc.) share a recurring set of security mistakes that don't
show up in a generic OWASP checklist: API keys pasted into sidebar inputs and
accidentally logged, LLM output rendered back into the page with
`unsafe_allow_html=True`, user text concatenated straight into a system
prompt with no delimiter, uploaded files fed to the model without checking
for embedded instructions. This skill exists to catch that specific class of
issue, not just generic web vulnerabilities — the LLM-specific section
(`references/checklist.md` §3) is the part a generic security review misses.

## Workflow

### 1. Map the stack before checking anything

Don't run the checklist blind. Spend a few minutes figuring out:
- UI framework (Streamlit / Gradio / Flask / FastAPI / plain script)
- Which LLM provider(s) and SDK are used, and where API calls are made
  (grep for `import openai`, `google.genai`, `anthropic`, `requests.post` to
  a model endpoint, etc.)
- Where secrets are expected to come from (`.env`, `st.secrets`,
  environment variables, a sidebar input, a config file)
- Whether the app has a database, file uploads, or any persistence
- Whether it's single-user/local-only (like a personal Streamlit tool) or
  meant to be deployed/shared — this changes how seriously to weigh things
  like missing auth or missing rate limiting. A personal local tool with no
  auth is a legitimate design choice, not automatically a finding; call it
  out as a finding only if the user's own stated intent doesn't already
  cover it (check CLAUDE.md or README for "no auth, personal use" type
  statements before flagging it).

A quick pass with Glob/Grep over the repo (entry points, `requirements.txt`
/ `pyproject.toml` / `package.json`, `.env*`, `.streamlit/`) is normally
enough. For a large or unfamiliar codebase, delegate this mapping to a
research subagent so you don't fill your own context with file contents you
won't need again.

### 2. Work through the checklist by category

Read `references/checklist.md` — it has the full checklist organized into:
1. Secrets & credential handling
2. Injection & unsafe rendering (XSS, command/SQL injection, deserialization, path traversal)
3. LLM-specific risks (prompt injection, unsafe output handling, excessive agency, data sent to third parties, cost/rate abuse)
4. Dependency vulnerabilities
5. Streamlit / deployment configuration
6. General API/web app checks (auth, CORS, headers, rate limiting) — apply only to the parts of the stack that are relevant (e.g. skip CORS checks for a pure local Streamlit app with no separate API surface)

For each item, read the actual code — don't pattern-match on function names
alone. `unsafe_allow_html=True` rendering a hardcoded string you wrote
yourself is not XSS; the same call rendering LLM output or user input is.
The checklist explains *why* each item matters so you can judge these calls
correctly rather than flagging everything that superficially matches a
pattern.

If the codebase is large, it's fine to split the six categories across
parallel subagent forks (they inherit your context) rather than reading
everything serially yourself — but do the stack-mapping step first so each
fork knows what it's looking at.

### 3. Run automated tools where available, fall back to manual review

Check what's actually installed/runnable before assuming a tool exists:

```bash
command -v pip-audit && pip-audit -r requirements.txt
command -v bandit && bandit -r . -x ./venv,./.venv
command -v safety && safety check -r requirements.txt
```

If a tool isn't available, don't stop to install it unless the user asks —
note in the report that the check was done via manual code/dependency
review instead of the automated tool, so the user knows the coverage is
narrower (manual review won't catch every known CVE the way pip-audit
would). If `npm`/`package.json` is present, `npm audit` applies the same
way.

### 4. Write the report

Use `assets/report_template.md` as the structure. Write the finished report
to a file in the repo root — `security-review-<YYYY-MM-DD>.md` — using
today's date. Then show the user a short summary in chat (finding counts by
severity, and the Critical/High items inline) rather than pasting the whole
file into the conversation; point them at the file for the rest.

Every finding needs:
- **Severity** (Critical/High/Medium/Low — see the template for the bar for each level)
- **Location**: `path/to/file.py:123`, or the config key / dependency name if not a code line
- **What's wrong and why it matters**, in concrete terms (what an attacker
  or a stray input could actually do — not just "this is insecure")
- **A specific fix** — a code change, config value, or library call, not
  just "add validation"

If a whole category has zero findings, say so explicitly in the report
rather than omitting the section — "no hardcoded secrets found" is useful
signal, not noise. Don't invent findings to pad out a category; an app with
5 real issues and a clean dependency check is a fine outcome.

### 5. Don't fix anything unless asked

This skill's job is to produce the report. If the user then asks you to fix
the findings, that's a separate step — treat it like any other code change
(explain what you're about to change, make the edit, don't sneak in
unrelated cleanup).
