# Brandella Free Tools

Static tool pages served at https://brandella.in/tools/

- `src/build.py` builds every page into `tools/` (shared header, footer, schema, OG images, sitemap)
- `src/seo_check.py` runs SEO checks on every page; deploy is blocked if any check fails
- Push to `main` with changes in `tools/` and GitHub Actions uploads `tools/` to Hostinger `public_html/tools` over FTP

Secrets required: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.

## Add tools
See `CLAUDE.md` for the full daily playbook.

```
python3 src/build.py && python3 src/seo_check.py tools && node src/browser_test.js tools
```
