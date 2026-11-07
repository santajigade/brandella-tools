"""Copy the main site's header, footer and their CSS onto the tools pages, so /tools/
always shows exactly the same menu as brandella.in.

Source: https://brandella.in/shared-chrome/ (built by santajigade/brandella from its
Header.astro, Footer.astro and src/styles/chrome.css).

Usage:
  python3 src/sync_chrome.py                    fetch the live page, save src/site_chrome.json
  python3 src/sync_chrome.py <file.html>        same, from a local build (dist/shared-chrome/index.html)
  add --apply                                   also patch every page in tools/ in place (no full rebuild)

If the fetch fails, the saved src/site_chrome.json is kept and nothing changes.
"""
import glob, json, os, re, sys, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, 'site_chrome.json')
TOOLS = os.path.join(os.path.dirname(HERE), 'tools')
URL = 'https://brandella.in/shared-chrome/'
BASE = 'https://brandella.in'


def between(src, a, b):
    i = src.index(a) + len(a)
    return src[i:src.index(b, i)].strip()


def parse(src):
    header = between(src, '<!--chrome:header-->', '<!--/chrome:header-->')
    footer = between(src, '<!--chrome:footer-->', '<!--/chrome:footer-->')
    css = between(src, '<style id="chrome-css">', '</style>')
    # root relative links and images become absolute, so they work from any page
    fix = lambda h: re.sub(r'(\s(?:href|src|action)=")/(?!/)', r'\1' + BASE + '/', h)
    header, footer = fix(header), fix(footer)
    assert '<header class="site-header"' in header and '<footer class="site-footer"' in footer and '.site-header' in css
    assert 'https://brandella.in/tools/' in header, 'header has no tools link'
    return {'header': header, 'footer': footer, 'css': css}


def load():
    return json.load(open(SNAP))


def apply(ch):
    n = 0
    for f in glob.glob(os.path.join(TOOLS, '**', '*.html'), recursive=True):
        s = open(f).read()
        t = re.sub(r'<!--chrome:header-->.*?<!--/chrome:header-->', lambda m: '<!--chrome:header-->\n' + ch['header'] + '\n<!--/chrome:header-->', s, flags=re.S)
        t = re.sub(r'<!--chrome:footer-->.*?<!--/chrome:footer-->', lambda m: '<!--chrome:footer-->\n' + ch['footer'] + '\n<!--/chrome:footer-->', t, flags=re.S)
        t = re.sub(r'<style id="chrome-css">.*?</style>', lambda m: '<style id="chrome-css">' + ch['css'] + '</style>', t, flags=re.S)
        if t != s:
            open(f, 'w').write(t); n += 1
    return n


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    try:
        if args:
            src = open(args[0]).read()
        else:
            req = urllib.request.Request(URL, headers={'User-Agent': 'brandella-tools-sync'})
            src = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
        ch = parse(src)
    except Exception as e:
        print('sync skipped, kept saved header and footer:', e)
        sys.exit(0)
    old = load() if os.path.exists(SNAP) else {}
    if {k: old.get(k) for k in ch} != ch:
        ch['synced'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        json.dump(ch, open(SNAP, 'w'), indent=1, ensure_ascii=False)
        print('saved new header and footer')
    else:
        ch = old
        print('header and footer unchanged')
    if '--apply' in sys.argv:
        print('patched', apply(ch), 'pages')
