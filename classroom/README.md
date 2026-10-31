# Classroom workbook / 課堂講義

New, independent 90-minute Traditional Chinese classroom route for ages 14–18. The existing homepage and its bilingual curriculum are preserved.

Entry: `classroom/index.html` / proposed Pages route `/ai-life-lab/classroom/`.

## Design changes
- Compact document layout: white and gray, restrained blue, persistent left navigation.
- Eight lessons: problem, prompt, tutor, connected apps, source detective, Codex, tests, reflection.
- Short steps, expandable explanations, teacher notes and solutions; mobile menu.
- Four-field prompt composer, nine fictional source records, quizzes, self-reported progress, TXT export, sandboxed HTML workbench and downloadable starter.
- Eleven existing screenshots are referenced from `../assets/walkthrough/`; provenance and limits are retained. They are not current authenticated connector results or Codex screenshots.
- No API calls, backend, analytics, accounts or external JavaScript dependencies. Inputs are held in page memory only and cleared on reload; export first.

## References checked 2026-10-31
- https://github.com/kevinlin1/just-the-class — course navigation.
- https://github.com/just-the-docs/just-the-docs — documentation layout.
- https://github.com/carpentries/workbench-template-md — objectives, exercises and solutions.
- https://github.com/microsoft/generative-ai-for-beginners — progressive practical lessons.

These informed structure; no theme code was copied.

## Safety and fidelity
Use fictional teaching accounts. Eligible minors require parent/guardian permission. Connected-app availability and approvals vary; a read-only prompt is not a permission boundary. The embedded workbench is not Codex. Prepared code and fixed explanations are labelled. The preview has `sandbox="allow-scripts"` (without same-origin) and a restrictive CSP, but is not a guarantee of safety for arbitrary untrusted HTML. Review code before exporting and opening it outside this sandbox.

## Run locally
From repository root: `python -m http.server 8000`, then open `http://localhost:8000/classroom/`.

This new route is handwritten and separate from the generated root curriculum; no root generator files were changed.
