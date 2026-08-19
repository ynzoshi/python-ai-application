# Security Review: <App Name> — <YYYY-MM-DD>

## Summary

<One paragraph: what was reviewed (stack, providers, scope), what method
was used (automated tools available? which ones ran?), and the headline
result — e.g. "3 High, 5 Medium, 2 Low findings; no hardcoded secrets or
known-CVE dependencies found.">

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 0 |
| Medium   | 0 |
| Low      | 0 |

## Scope & Method

- **Stack:** <e.g. Streamlit + google-genai SDK, no database, no auth (by design)>
- **Automated tools run:** <e.g. pip-audit v2.7 — ran clean / bandit not
  installed, substituted manual review>
- **Not covered:** <anything explicitly out of scope — e.g. "no
  penetration testing of a live deployment; static review only">

---

## Findings

<Repeat this block per finding. Order Critical → High → Medium → Low.
If a category (see checklist.md §1–6) has zero findings, add one line
under it: "No issues found in this category." rather than omitting it.>

### [<Severity>] <Short title>

- **Category:** <Secrets / Injection & Rendering / LLM-specific / Dependencies / Streamlit & Deployment Config / General API>
- **Location:** `path/to/file.py:123`
- **Issue:** <What's wrong, in concrete terms — what input or condition
  triggers it.>
- **Impact:** <What an attacker or a stray input could actually do as a
  result — be specific, not "this is a security risk.">
- **Fix:** <A specific code change, config value, or library call.>

```python
# before
...

# after
...
```

---

## Severity bar (for reference while writing)

- **Critical** — directly exploitable, no special access needed, and
  leads to secret/data exposure, arbitrary code execution, or full
  account/data compromise. (e.g. hardcoded prod API key in a public repo;
  `eval()` on user input.)
- **High** — exploitable with plausible conditions (e.g. requires the app
  to be deployed publicly, or a specific but realistic user action), and
  has serious impact (XSS, meaningful data leakage, real-money API abuse
  at scale).
- **Medium** — real weakness but needs unusual conditions, has limited
  impact, or is a defense-in-depth gap rather than a direct hole (e.g.
  missing rate limiting on a low-traffic personal tool; prompt injection
  with no downstream excessive-agency risk).
- **Low** — hardening suggestion; best-practice deviation with minimal
  realistic impact given the app's actual deployment context (e.g.
  unpinned dependency versions, no auth on an explicitly personal
  localhost-only tool).

## Notes / Accepted risks

<Anything intentionally out of scope per the app's own stated design
(e.g. "no auth" documented as an intentional constraint in CLAUDE.md) —
list it here instead of as a finding, so the user can see it was
considered rather than missed.>
