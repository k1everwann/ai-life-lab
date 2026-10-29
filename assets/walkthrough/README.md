# Screenshot sources

Captured on 2026-10-29 using the browser screenshot API. These are actual UI captures, cropped at capture time, not reconstructed interface images. They contain no signed-in account data. Captions and alt text live in `scripts/visual_guides.py`; both lesson languages use the Traditional Chinese interface captures with localized instructions.

- `chat-start-zh.jpg`: signed-out https://chatgpt.com/ home.
- `chat-paste-zh.jpg`, `chat-answer-zh.jpg`, `chat-followup-zh.jpg`: a fictional notice typed in the signed-out ChatGPT interface. The answer is an actual response; the follow-up is an unsent draft. No conversation URL is published.
- `gmail-paste-zh.jpg`, `drive-paste-zh.jpg`, `notion-paste-zh.jpg`: the corresponding M04/M05/M06 fictional source and request pasted as unsent drafts in ChatGPT. Crops show the composer only. Long drafts scroll inside the composer. These are not connected-account results.
- `plugins-directory-zh.jpg`: https://chatgpt.com/plugins?plugins_landing=1 public directory.
- `drive-entry-zh.jpg`: https://chatgpt.com/plugins/plugin_connector_1p_ab21a553bfbc81919ea8fd1858e3ffa7?plugins_landing=1 public Google Drive listing.
- `notion-entry-zh.jpg`: https://chatgpt.com/plugins/plugin_asdk_app_69c18c28f1188191bf5b8445c4ab0a2e?plugins_landing=1 public Notion listing.
- `html-preview-zh.jpg`: this repository's public M08 workspace, filled with `downloads/curriculum/correct-checklist-zh-Hant.html`. The caption identifies the prepared fixture; this is not presented as a learner's generated code.

The public Gmail search did not expose a verified Gmail connector entry, only other products. Do not substitute those products or imply OAuth has been tested. The directory picture explains where to search and the lesson retains a text-only path.

To refresh: capture only a signed-out or fictional teaching view, inspect each image for private data, update its date, dimensions, bilingual captions and source here, rebuild with `scripts/build_course.py`, run `scripts/validate.py`, and check both languages and image enlargement in the browser. Do not replace these with screenshots of private projects or accounts.
