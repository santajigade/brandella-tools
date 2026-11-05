# Brandella Free Tools: playbook

Static, browser only tool pages served at https://brandella.in/tools/ (owner: Santaji, brandella.in).
Pushing to `main` runs `.github/workflows/deploy.yml`: SEO check, then lftp upload of `tools/` to Hostinger `public_html/tools`. Live in about a minute.

## Layout
- `src/build.py`: shared header, footer, CSS, schema, page builder. Builds `tools/` from scratch every run (OG images and sitemap included). Do not hand edit anything in `tools/`.
- `src/categories.py`: category registry and roadmap. A category goes live when it has at least one tool. Order = order on /tools/.
- `src/batch_*.py`: one module per batch, auto loaded in filename order. Each exposes `add(TOOLS, STOP_JS)` and sets `cat` and `updated` on the tools it appends. Copy the shape of `src/batch_2026_10_28_seo.py`.
- `src/seo_check.py tools`: 20 checks per page. Must end with `TOTAL FAILS: 0`.
- `src/browser_test.js tools`: Chromium check for JS errors, mobile overflow and dashes. Must end with `0 with problems`.
- `docs/article-slugs.txt`: the only valid brandella.in article slugs. Never link to anything else.

## Daily batch (one category per day, 6 to 7 tools)
1. Pick the first category in `src/categories.py` that has no tools yet. If none is left, build nothing and report that the roadmap is complete, with 3 suggested next categories.
2. Research demand before choosing tools. Use web search to confirm each candidate is something people actually search for (well known tool queries such as "utm builder", "json formatter", "roas calculator", "faq schema generator"; check that established tool sites rank for it). Pick the 6 or 7 most searched, most useful tools for the category. Skip anything that duplicates an existing tool in any category.
   **Value test (Santaji, 2026-11-05).** Every tool must pass all four, or replace it:
   - Solves a real, repeated problem the visitor has today (cleans, converts, checks, calculates or generates something they then use), so they bookmark it and come back.
   - Gives a result the visitor cannot get faster elsewhere for free, such as inside the platform itself. No mockups or previews of things the platform already previews (lesson: the Google Ads preview tool brings little value).
   - Has real search demand now and stays useful as search moves to AI. Prefer tools that help with AI era work: AI search visibility, llms.txt, AI crawlers, prompts, tokens, structured content for AI answers, cleaning AI written text.
   - Is something Santaji would happily link from an article as genuinely useful.
   Within any category, include AI era tools where they fit the theme.
3. Every tool must work 100% in the browser: no APIs, no server, no fetching other sites, no API keys. It must do a real job well, not be a thin page.
4. Verify every fact you state (platform character limits, formulas, schema properties, Google rules) with a current authoritative source via web search. Link 1 or 2 official sources (Google, schema.org, Meta, MDN) in the content where helpful.
5. Write `src/batch_YYYY_MM_DD_<category-slug>.py` with all tools. Per tool:
   - `slug` (keyword first, permanent), `short` (2 to 3 letter badge, unique), `name`, `card` (one sentence)
   - `title` 30 to 60 chars, focus keyword first, no brand suffix. `desc` 120 to 160 chars. Both unique.
   - `h1`, `lead`, `tool` (HTML using existing classes: tool, card, field, row2, check, tabs, btn, btn dark, stats, stat-box, rtable, kw-result, tips, chips, code-out, toast), `js` (helpers available: `$`, `esc`, `copyText(text, 'toast')`)
   - `content`: 350+ words. What it is, How to use (ol), a table or list explaining the details, practical tips, and a closing paragraph with 2 to 3 in body links to real articles from `docs/article-slugs.txt` plus 1 link to a sibling tool.
   - `faqs`: exactly 4 genuinely useful Q and A pairs. `related`: 4 (title, slug) pairs from `docs/article-slugs.txt`.
   - Tool pages load with a realistic sample already filled in, so the tool shows a result immediately.
6. House style for all visible text: plain, friendly, short paragraphs. NO dashes or hyphens in visible text (write "long tail", "A to Z", "built in"). Literal code, tag names and attributes go inside `<code>`. Headings never contain hyphens.
7. Build and test:
   `python3 src/build.py && python3 src/seo_check.py tools && node src/browser_test.js tools`
   Then write a short Playwright script that drives each new tool (type input, click buttons, read output) and confirm the output is correct. Fix every bug found.
8. Commit with a clear message and push to `main`. Watch the run (`gh run list -R santajigade/brandella-tools -L 1`). If it fails, read the failing step, fix, push again.
9. Report to Santaji (use SendUserMessage): category name, each tool with its live URL, and these two reminders:
   - WordPress: Appearance > Menus > add Custom Link `https://brandella.in/tools/<category-slug>/` under "Tools".
   - Search Console: resubmit `tools/sitemap.xml`.

## Never
- Rename or delete a live tool or category slug (they are indexed URLs).
- Edit `.github/workflows/deploy.yml` unless the deploy itself is broken.
- Add trackers, external scripts, or anything that sends user input off the page.
- Build more than 7 tools in one day.
