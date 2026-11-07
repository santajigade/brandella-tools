import re, json, os, html, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'serp-snippet-preview-source.html')
OUT = os.path.join(os.path.dirname(HERE), 'tools')
BASE = 'https://brandella.in'
src = open(SRC).read()

CSS = src.split('<style>')[1].split('</style>')[0]
HEADER = '<header>' + src.split('<header>')[1].split('</header>')[0] + '</header>'
FOOTER = '<footer class="site-footer">' + src.split('<footer class="site-footer">')[1].split('</footer>')[0] + '</footer>'

# ===== New Brandella Journal design (2026-11-07): top bar, logo + inline nav, column footer =====
_C = 'https://brandella.in/category/'
NAV = [
    ('SEO', _C + 'seo/', [('Technical SEO', 'seo/technical-seo/'), ('On Page SEO', 'seo/on-page-seo/'), ('Off Page SEO', 'seo/off-page-seo/'),
        ('Local SEO', 'seo/local-seo/'), ('Mobile SEO', 'seo/mobile-seo/'), ('Core Web Vitals', 'seo/core-web-vitals/'),
        ('Keyword Research', 'seo/keyword-research/'), ('Link Building', 'seo/link-building/'), ('Google Search Console', 'seo/google-search-console/'),
        ('SEO Tools', 'seo/seo-tools/'), ('SEO Basics', 'seo/seo-basics/')]),
    ('Paid Media', _C + 'paid-media/', [('Google Ads', 'paid-media/google-ads/'), ('Meta Ads', 'paid-media/meta-ads/'), ('LinkedIn Ads', 'paid-media/linkedin-ads/'),
        ('Display Advertising', 'paid-media/display-advertising/'), ('PPC Strategy', 'paid-media/ppc-strategy/'), ('Paid Media Analytics', 'paid-media/paid-media-analytics/')]),
    ('Content', _C + 'content/', []),
    ('Social', _C + 'social/', []),
    ('Digital Marketing', _C + 'digital-marketing/', []),
    ('AI', _C + 'artificial-intelligence/', []),
    ('Development', _C + 'development/', [('GTM', 'development/gtm/'), ('HTML', 'development/html/'), ('HTML CSS', 'development/html_css/'),
        ('HTML JS', 'development/html_js/'), ('JavaScript', 'development/javascript/'), ('PHP', 'development/php/'), ('Python', 'development/python/')]),
]
LOGO_SVG = ('<svg class="bj-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#6cc82a"/>'
            '<path d="M12 9h10.2c4.6 0 7.4 2.3 7.4 5.9 0 2.4-1.3 4.1-3.4 4.8 2.7.6 4.3 2.6 4.3 5.4 0 4-3.1 6.4-8 6.4H12z'
            'M17.4 13.4v5h4.1c1.8 0 2.8-.9 2.8-2.5s-1-2.5-2.8-2.5zm0 9.1v5.6h4.6c2 0 3.2-1 3.2-2.8s-1.2-2.8-3.2-2.8z" fill="#fff"/>'
            '<circle cx="33" cy="33" r="4.2" fill="#a6ef39" stroke="#6cc82a" stroke-width="1.6"/></svg>')
CHEV = '<svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

def nav_html(tool_cats):
    li = ''
    for name, url, kids in NAV:
        if kids:
            sub = ''.join(f'<li><a href="{_C}{u}">{n}</a></li>' for n, u in kids)
            li += f'<li class="bj-has"><a href="{url}">{name}{CHEV}</a><ul class="bj-sub">{sub}</ul></li>'
        else:
            li += f'<li><a href="{url}">{name}</a></li>'
    sub = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in tool_cats) + '<li class="all"><a href="https://brandella.in/tools/">All free tools</a></li>'
    li += f'<li class="bj-has"><a class="active" href="https://brandella.in/tools/">Free Tools{CHEV}</a><ul class="bj-sub">{sub}</ul></li>'
    return li

def header_html(tool_cats):
    return f'''<header class="bj-header">
  <div class="bj-top"><div class="wrap">
    <p>SEO, paid media, AI search and web development, explained.</p>
    <ul><li><a href="https://brandella.in/about-us/">About</a></li><li><a href="https://brandella.in/contact-page/">Contact</a></li><li><a href="https://brandella.in/tools/">Free Tools</a></li><li><a href="https://brandella.in/feed/">RSS</a></li></ul>
  </div></div>
  <div class="bj-bar"><div class="wrap">
    <a class="bj-logo" href="https://brandella.in/">{LOGO_SVG}<span>Brandella <b>Journal</b></span></a>
    <button class="bj-menu" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="siteNav"><i></i><i></i><i></i></button>
    <nav class="bj-nav" id="siteNav" aria-label="Main"><ul>{nav_html(tool_cats)}</ul></nav>
  </div></div>
</header>'''

def footer_html(tool_cats):
    topics = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u, _ in NAV)
    tools = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in tool_cats)
    return f'''<footer class="bj-foot">
  <div class="wrap">
    <div class="bj-cols">
      <div class="bj-about">
        <a class="bj-logo light" href="https://brandella.in/">{LOGO_SVG}<span>Brandella <b>Journal</b></span></a>
        <p>Practical guides on SEO, paid media, AI search, analytics and web development, plus free tools that run right in your browser.</p>
      </div>
      <div><h2>Topics</h2><ul>{topics}</ul></div>
      <div><h2>Free Tools</h2><ul>{tools}<li><a href="https://brandella.in/tools/">All free tools</a></li></ul></div>
      <div><h2>Company</h2><ul><li><a href="https://brandella.in/about-us/">About Us</a></li><li><a href="https://brandella.in/contact-page/">Contact Us</a></li><li><a href="https://brandella.in/privacy-policy/">Privacy Policy</a></li><li><a href="https://brandella.in/terms-and-conditions/">Terms and Conditions</a></li><li><a href="https://brandella.in/feed/">RSS Feed</a></li></ul></div>
    </div>
    <p class="copy">Copyright &copy; <span id="yr">2026</span> Brandella Journal. All rights reserved.</p>
  </div>
</footer>'''

NEW_CSS = r'''
/* ===== NEW SITE HEADER ===== */
.bj-top{background:#111;color:#e8e8e8;font-size:13px}
.bj-top .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:40px}
.bj-top p{margin:0}
.bj-top ul{list-style:none;display:flex;gap:22px}
.bj-top a{color:#e8e8e8;text-decoration:none}
.bj-top a:hover{color:var(--lime)}
.bj-bar{background:#fff;border-bottom:1px solid var(--line);position:relative;z-index:40}
.bj-bar .wrap{display:flex;align-items:center;gap:28px;min-height:60px}
.bj-logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:#111;flex:0 0 auto}
.bj-mark{width:30px;height:30px;flex:0 0 auto}
.bj-logo span{font-size:19px;font-weight:800;letter-spacing:-.2px;white-space:nowrap}
.bj-logo b{font-weight:400;color:var(--green)}
.bj-nav{margin-left:auto}
.bj-nav > ul{list-style:none;display:flex;align-items:center;gap:2px}
.bj-nav > ul > li{position:relative}
.bj-nav a{display:flex;align-items:center;gap:6px;padding:18px 9px;font-size:14px;font-weight:700;color:#111;text-decoration:none;white-space:nowrap}
.bj-nav a:hover,.bj-nav a.active{color:var(--green)}
.bj-nav .chev{width:9px;height:6px;color:#8a8a8a}
.bj-nav a.active .chev,.bj-nav a:hover .chev{color:var(--green)}
.bj-nav .bj-sub{display:none;list-style:none;position:absolute;top:100%;left:0;min-width:230px;background:#fff;border:1px solid var(--line);border-top:3px solid var(--green);border-radius:0 0 8px 8px;padding:8px 0;box-shadow:0 14px 30px rgba(0,0,0,.12);z-index:60}
.bj-nav > ul > li:last-child .bj-sub{left:auto;right:0}
.bj-nav .bj-sub a{padding:7px 18px;font-weight:600;font-size:14px;border:0}
.bj-nav .bj-sub a:hover{background:var(--soft)}
.bj-nav .bj-sub li.all{border-top:1px solid var(--line);margin-top:6px;padding-top:6px}
.bj-nav .bj-sub li.all a{color:#3d8f12;font-weight:700}
.bj-nav .bj-has:hover .bj-sub,.bj-nav .bj-has:focus-within .bj-sub{display:block}
.bj-menu{display:none;margin-left:auto;background:none;border:0;cursor:pointer;padding:8px}
.bj-menu i{display:block;width:24px;height:2.5px;background:#111;margin:5px 0;border-radius:2px}
.hero h1{font-weight:800;letter-spacing:-.5px}

/* ===== NEW SITE FOOTER ===== */
.bj-foot{background:var(--footer);color:#cfcfcf;margin-top:70px;padding:56px 0 30px;font-size:14px}
.bj-cols{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:36px}
.bj-foot .bj-logo{color:#fff;margin-bottom:14px}
.bj-foot p{color:#a8a8a8;line-height:1.65;max-width:340px}
.bj-foot h2{color:#fff;font-size:13px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--green);display:inline-block}
.bj-foot ul{list-style:none}
.bj-foot li{margin-bottom:8px}
.bj-foot ul a{color:#cfcfcf;text-decoration:none}
.bj-foot ul a:hover{color:var(--lime)}
.bj-foot .copy{border-top:1px solid #262626;margin-top:40px;padding-top:22px;font-size:13.5px;max-width:none;color:#8f8f8f}

@media (max-width:1100px){
  .bj-nav a{padding:18px 6px;font-size:13.5px}
  .bj-bar .wrap{gap:16px}
}
@media (max-width:980px){
  .bj-top p{display:none}
  .bj-top .wrap{justify-content:flex-end}
  .bj-menu{display:block}
  .bj-bar .wrap{flex-wrap:wrap;gap:0}
  .bj-nav{display:none;flex-basis:100%;margin:0 0 10px}
  .bj-nav.open{display:block}
  .bj-nav > ul{flex-direction:column;align-items:stretch}
  .bj-nav a{padding:12px 4px;border-bottom:1px solid #f0f0f0;justify-content:space-between}
  .bj-nav .bj-sub{position:static;display:none;box-shadow:none;border:0;border-radius:0;padding:0 0 6px 14px;min-width:0}
  .bj-nav .bj-has:hover .bj-sub{display:none}
  .bj-nav .bj-has.open .bj-sub{display:block}
  .bj-cols{grid-template-columns:1fr 1fr}
  .bj-about{grid-column:1/-1}
}
@media (max-width:520px){
  .bj-cols{grid-template-columns:1fr}
  .bj-top ul{gap:16px}
}
'''

EXTRA_CSS = r'''
/* ===== SHARED TOOL EXTRAS ===== */
.full{grid-column:1/-1}
.field select{width:100%;border:1px solid #cfcfcf;border-radius:8px;padding:10px 12px;font:inherit;font-size:15px;background:#fff;color:#111}
.field textarea.big{min-height:230px;font-size:14.5px}
.mono{font-family:Consolas,Monaco,monospace !important;font-size:13.5px !important}
.btn-sm{padding:5px 12px;font-size:13px;border-width:1.5px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(105px,1fr));gap:10px;margin-bottom:16px}
.stat-box{background:var(--soft);border:1px solid #dbefc8;border-radius:10px;padding:10px 8px;text-align:center}
.stat-box b{display:block;font-size:22px;line-height:1.2}
.stat-box span{font-size:12.5px;color:var(--muted);font-weight:600}
.rtable{width:100%;border-collapse:collapse;font-size:14.5px}
.rtable th{background:#2b2b2b;color:#fff;text-align:left;padding:8px 10px;font-weight:700}
.rtable td{border-bottom:1px solid var(--line);padding:7px 10px}
.rtable td.num,.rtable th.num{text-align:right;font-variant-numeric:tabular-nums}
.rtable tr.hit td{background:#eef8e6;font-weight:700}
.empty{color:var(--muted);font-size:14.5px;padding:14px 0}
.kw-result{border-radius:10px;padding:12px 14px;margin-bottom:16px;font-size:14.5px;border:1px solid var(--line);background:#fafafa}
.kw-result.ok{background:#eef8e6;border-color:#cfeab4}
.kw-result.warn{background:#fff6e5;border-color:#f3d79b}
.kw-result.bad{background:#fdecea;border-color:#f5c2bb}
.slug-row{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:8px;display:flex;justify-content:space-between;gap:10px;align-items:center}
.slug-row .s{font:600 15px/1.4 Consolas,Monaco,monospace;color:#111;word-break:break-all}
.slug-row small{display:block;color:var(--muted);font-size:12.5px;word-break:break-all;margin-top:2px}
.slug-row small.warn{color:#c47a00;font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.chip{border:1px solid var(--line);border-radius:20px;padding:4px 12px;font-size:13.5px;font-weight:700;background:#fff}
.chip.zero{color:#aaa}
.outline{max-height:460px;overflow:auto;border:1px solid var(--line);border-radius:10px;padding:6px 12px}
.o-row{display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-bottom:1px dashed #eee;font-size:14.5px}
.o-row:last-child{border-bottom:0}
.o-tag{flex:0 0 auto;font:700 12px/1 Consolas,Monaco,monospace;padding:5px 7px;border-radius:5px;color:#fff;background:#111}
.o-tag.h1{background:#2f7a0c}.o-tag.h2{background:#4fa61d}.o-tag.h3{background:#6cc82a}.o-tag.h4{background:#8a8a8a}.o-tag.h5{background:#a5a5a5}.o-tag.h6{background:#bdbdbd}
.o-issue{display:inline-block;font-size:12px;color:#d1351f;font-weight:700;margin-left:6px}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;margin:30px 0 10px}
.tcard{border:1px solid var(--line);border-radius:12px;padding:22px;text-decoration:none;display:flex;flex-direction:column;gap:10px;transition:all .15s;background:#fff;color:#111}
.tcard:hover{border-color:var(--green);box-shadow:0 8px 22px rgba(0,0,0,.07);transform:translateY(-2px)}
.tbadge{width:48px;height:48px;border-radius:12px;background:#111;color:var(--lime);display:grid;place-items:center;font-weight:800;font-size:16px}
.tcard h2,.tcard h3{font-size:18px;line-height:1.3;margin:0}
.tcard p{font-size:14.5px;color:var(--muted);flex:1;line-height:1.55}
.tcard .go{font-weight:700;color:#3d8f12;font-size:14px}
.tcard.soon{opacity:.55;pointer-events:none}
.tcard.soon .tbadge{background:#ddd;color:#777}
.tcard.soon .go{color:var(--muted)}
.more-tools{margin-top:10px}
'''
CSS_ALL = CSS + EXTRA_CSS + NEW_CSS

BASE_JS = r'''
  var d = new Date();
  document.getElementById('yr').textContent = d.getFullYear();
  var nav = document.getElementById('siteNav'), mb = document.getElementById('menuBtn');
  mb.addEventListener('click', function(){ var open = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', open); });
  nav.querySelectorAll('.bj-has > a').forEach(function(a){
    a.addEventListener('click', function(e){
      if (window.innerWidth > 980) return;
      var li = a.parentNode; if (!li.classList.contains('open')){ e.preventDefault(); li.classList.add('open'); }
    });
  });
  var $ = function(id){ return document.getElementById(id); };
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function copyText(text, toastId){
    var done = function(){ var t = $(toastId); if(!t) return; t.classList.add('show'); setTimeout(function(){ t.classList.remove('show'); }, 1600); };
    if (navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(done, function(){ fallback(); done(); }); }
    else { fallback(); done(); }
    function fallback(){ var ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta); }
  }
'''

AD = '''<div class="bx-ad">
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>'''

HUB = BASE + '/tools/seo-tools/'  # legacy, used only by SEO hub intro

def page(title, desc, url, schema, main, js='', og='tools'):
    ogimg = BASE + '/tools/assets/og-' + og + '.png'
    ld = json.dumps(schema, indent=2, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Brandella Journal">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ogimg}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
<script type="application/ld+json">
{ld}
</script>
<style>{CSS_ALL}</style>
</head>
<body>

{HEADER}

<main class="wrap">
{main}
</main>

{FOOTER}

<script>
(function(){{
{BASE_JS}
{js}
}})();
</script>
</body>
</html>
'''

def crumbs(items):
    parts = []
    for name, url in items:
        parts.append(f'<a href="{url}">{name}</a>' if url else name)
    return '<div class="crumbs">' + ' &rsaquo; '.join(parts) + '</div>'

def bc_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs):
    out = ['<h2>Frequently Asked Questions</h2>']
    for i, (q, a) in enumerate(faqs, 1):
        out.append(f'<details class="faq-item" open><summary><span class="faq-num">{i}</span>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>')
    return '\n    '.join(out)

def related_html(links, heading='Related Articles'):
    cards = '\n      '.join(f'<a href="{BASE}/{s}/">{n} <span>&rarr;</span></a>' if not s.startswith('http') else f'<a href="{s}">{n} <span>&rarr;</span></a>' for n, s in links)
    return f'<h2>{heading}</h2>\n    <div class="related">\n      {cards}\n    </div>'

# ======================= TOOL DEFINITIONS =======================
TOOLS = []

# ---------- 1. SERP SNIPPET PREVIEW (from existing file) ----------
serp_tool = re.search(r'(<section class="tool".*?</section>)', src, re.S).group(1)
serp_content = src.split('<article class="content">')[1].split('<h2>Frequently Asked Questions</h2>')[0]
serp_content = re.sub(r'\s*<div class="bx-ad">.*?</div>\s*', '\n', serp_content, flags=re.S)
serp_content = serp_content.replace('serp-snippet-preview/', 'seo-tools/serp-snippet-preview/')
serp_tool = serp_tool.replace('https://brandella.in/tools/serp-snippet-preview/', 'https://brandella.in/tools/seo-tools/serp-snippet-preview/')
serp_tool = serp_tool.replace('<h3 class="g-title" id="gTitle"></h3>', '<div class="g-title" id="gTitle" role="presentation"></div>')
serp_js = src.split('/* ===== SERP tool ===== */')[1]
serp_js = serp_js.rsplit('})();', 1)[0]
serp_js = serp_js.replace('function esc(s){', 'function escOld(s){')

TOOLS.append(dict(
    slug='serp-snippet-preview', short='SP', name='SERP Snippet Preview',
    card='See how your title and meta description look in Google on desktop and mobile, with real pixel width limits.',
    title='SERP Snippet Preview Tool: Free Google Result Checker',
    desc='Free SERP snippet preview tool. See how your title and meta description look in Google on desktop and mobile, with real pixel limits.',
    h1='SERP Snippet Preview Tool',
    lead='See exactly how your page will look in Google search results on desktop and mobile. Real pixel width limits, live truncation, and ready to copy meta tags.',
    tool=serp_tool, content=serp_content, js=serp_js,
    faqs=[
        ("How long should a title tag be for Google?", "Google truncates titles by pixel width, not character count. On desktop the limit is roughly 600 pixels, which is usually around 50 to 60 characters depending on the letters used."),
        ("How long should a meta description be?", "Aim for roughly 920 pixels on desktop and about 680 pixels on mobile. In practice that is around 120 to 155 characters, with the key message placed in the first 120 characters."),
        ("Does Google always show my meta description?", "No. Google often rewrites snippets using text from the page when it believes that text better matches the search query. A clear, relevant meta description still improves the chance it is used."),
        ("Is this SERP snippet preview tool free?", "Yes. The tool is completely free, needs no signup, and runs entirely in your browser, so nothing you type is sent to any server."),
    ],
    related=[("Title Tag Optimization", "title-tag-optimization"), ("Dynamic Meta Tags in PHP", "dynamic-meta-tags-php"),
             ("Search Console Performance Report", "search-console-performance-report"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
))

# ---------- 2. KEYWORD DENSITY CHECKER ----------
STOP_JS = r'''var STOP = new Set('a about above after again against all also am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves'.split(' '));'''

TOOLS.append(dict(
    slug='keyword-density-checker', short='KD', name='Keyword Density Checker',
    card='Paste any text or HTML and see the most used 1, 2 and 3 word phrases with their exact density.',
    title='Keyword Density Checker: Free 1, 2 and 3 Word Analyzer',
    desc='Free keyword density checker. Paste text or HTML to see top 1, 2 and 3 word phrases, word count, and the exact density of your focus keyword.',
    h1='Keyword Density Checker',
    lead='Paste your article text or HTML and instantly see which words and phrases you use most, plus the exact density of your focus keyword.',
    tool=r'''<section class="tool" aria-label="Keyword density checker">
    <div class="card">
      <h2>Paste Your Content</h2>
      <div class="field">
        <label for="kdText">Text or HTML <em id="kdChars">0 chars</em></label>
        <textarea id="kdText" class="big" placeholder="Paste your article text or full HTML here...">Keyword density tells you how often a keyword appears compared to the total words on a page. A keyword density checker helps you spot when a phrase is used too little or too much. Search engines reward content that reads naturally, so keyword density should support your writing, not drive it. Use this keyword density checker after drafting, then adjust the copy if one phrase dominates the page.</textarea>
      </div>
      <div class="field">
        <label for="kdKw">Focus Keyword <em>optional</em></label>
        <input id="kdKw" type="text" value="" placeholder="e.g. keyword density">
      </div>
      <label class="check"><input id="kdStop" type="checkbox" checked> Ignore common stop words (the, and, of...)</label>
      <div class="actions">
        <button class="btn" id="kdClear">Clear</button>
        <button class="btn" id="kdCsv">Download CSV</button>
      </div>
    </div>

    <div class="card">
      <h2>Results</h2>
      <div class="stats">
        <div class="stat-box"><b id="sWords">0</b><span>Words</span></div>
        <div class="stat-box"><b id="sUnique">0</b><span>Unique</span></div>
        <div class="stat-box"><b id="sSent">0</b><span>Sentences</span></div>
        <div class="stat-box"><b id="sRead">0</b><span>Min Read</span></div>
      </div>
      <div class="kw-result" id="kwResult">Add a focus keyword to see its density.</div>
      <div class="tabs" role="tablist">
        <button class="on" data-n="1">1 Word</button>
        <button data-n="2">2 Words</button>
        <button data-n="3">3 Words</button>
      </div>
      <div id="kdTable"></div>
    </div>
  </section>''',
    js=STOP_JS + r'''
  var tEl=$('kdText'), kEl=$('kdKw'), sEl=$('kdStop'), cur=1, last={};
  function plain(t){
    if (/<[a-z][\s\S]*>/i.test(t)){
      var doc = new DOMParser().parseFromString(t,'text/html');
      doc.querySelectorAll('script,style,noscript').forEach(function(n){ n.remove(); });
      return doc.body ? doc.body.textContent : t;
    }
    return t;
  }
  function words(t){ return (t.toLowerCase().replace(/[’]/g,"'").match(/[a-z0-9À-ɏ]+(?:'[a-z]+)?/g) || []); }
  function grams(w, n, stop){
    var m = {};
    for (var i=0;i+n<=w.length;i++){
      var g = w.slice(i,i+n);
      if (stop){
        if (n===1 && STOP.has(g[0])) continue;
        if (n>1 && (STOP.has(g[0]) || STOP.has(g[n-1]))) continue;
      }
      if (n===1 && /^\d+$/.test(g[0])) continue;
      var k = g.join(' ');
      m[k] = (m[k]||0) + 1;
    }
    return Object.keys(m).map(function(k){ return [k, m[k]]; }).filter(function(x){ return n===1 || x[1]>1; })
      .sort(function(a,b){ return b[1]-a[1] || a[0].localeCompare(b[0]); });
  }
  function countPhrase(w, p){
    if (!p.length) return 0; var c=0;
    for (var i=0;i+p.length<=w.length;i++){ var ok=true; for (var j=0;j<p.length;j++){ if (w[i+j]!==p[j]){ ok=false; break; } } if (ok) c++; }
    return c;
  }
  function pct(c,n,total){ return total ? (c*n/total*100) : 0; }
  function run(){
    var raw = tEl.value, txt = plain(raw), w = words(txt), total = w.length;
    $('kdChars').textContent = txt.trim().length + ' chars';
    $('sWords').textContent = total;
    $('sUnique').textContent = new Set(w).size;
    $('sSent').textContent = (txt.match(/[^.!?]+[.!?]+(\s|$)/g) || (txt.trim()? [1] : [])).length;
    $('sRead').textContent = total ? Math.max(1, Math.ceil(total/200)) : 0;
    var kw = words(kEl.value), box = $('kwResult');
    if (kw.length && total){
      var c = countPhrase(w, kw), p = pct(c, kw.length, total), cls, msg;
      if (c===0){ cls='bad'; msg='Not found in the text.'; }
      else if (p < 0.5){ cls='warn'; msg='Low. Consider using it a little more.'; }
      else if (p <= 2.5){ cls='ok'; msg='Healthy range.'; }
      else if (p <= 3.5){ cls='warn'; msg='High. Make sure it still reads naturally.'; }
      else { cls='bad'; msg='Too high. This may look like keyword stuffing.'; }
      box.className = 'kw-result ' + cls;
      box.innerHTML = '<strong>"' + esc(kw.join(' ')) + '"</strong> appears <strong>' + c + '</strong> time' + (c===1?'':'s') + ', density <strong>' + p.toFixed(2) + '%</strong>. ' + msg;
    } else { box.className='kw-result'; box.textContent = 'Add a focus keyword to see its density.'; }
    last = { total: total, w: w };
    table();
  }
  function table(){
    var g = grams(last.w || [], cur, sEl.checked).slice(0,25), kwk = words(kEl.value).join(' ');
    if (!g.length){ $('kdTable').innerHTML = '<p class="empty">No repeated ' + cur + ' word phrases found yet.</p>'; return; }
    var rows = g.map(function(x,i){ return '<tr' + (x[0]===kwk?' class="hit"':'') + '><td>' + (i+1) + '</td><td>' + esc(x[0]) + '</td><td class="num">' + x[1] + '</td><td class="num">' + pct(x[1],cur,last.total).toFixed(2) + '%</td></tr>'; }).join('');
    $('kdTable').innerHTML = '<table class="rtable"><thead><tr><th>#</th><th>Phrase</th><th class="num">Count</th><th class="num">Density</th></tr></thead><tbody>' + rows + '</tbody></table>';
  }
  document.querySelectorAll('.tabs button').forEach(function(b){
    b.addEventListener('click', function(){
      document.querySelectorAll('.tabs button').forEach(function(x){ x.classList.remove('on'); });
      b.classList.add('on'); cur = +b.getAttribute('data-n'); table();
    });
  });
  [tEl,kEl].forEach(function(e){ e.addEventListener('input', run); });
  sEl.addEventListener('change', run);
  $('kdClear').onclick = function(){ tEl.value=''; kEl.value=''; run(); tEl.focus(); };
  $('kdCsv').onclick = function(){
    var lines = ['Phrase,Words,Count,Density %'];
    [1,2,3].forEach(function(n){ grams(last.w||[], n, sEl.checked).forEach(function(x){ lines.push('"' + x[0] + '",' + n + ',' + x[1] + ',' + pct(x[1],n,last.total).toFixed(2)); }); });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([lines.join('\n')], {type:'text/csv'}));
    a.download = 'keyword-density.csv'; a.click();
  };
  run();
''',
    content=r'''
    <h2>What Is Keyword Density?</h2>
    <p>Keyword density is the share of a page's words taken up by a specific keyword or phrase, shown as a percentage.</p>
    <p>It is a quick way to see whether your focus keyword actually features in the content, or whether one phrase is being repeated so often that the writing starts to sound forced.</p>

    <h2>How This Keyword Density Checker Works</h2>
    <ol>
      <li><strong>Paste your content.</strong> Plain text works, and so does full HTML. Tags, scripts and styles are stripped automatically so only visible text is counted.</li>
      <li><strong>Add your focus keyword.</strong> The tool counts exact phrase matches and shows the density with a simple healthy, low or high verdict.</li>
      <li><strong>Review the phrase tables.</strong> Switch between 1, 2 and 3 word phrases to see what the page is really about from a search engine's point of view.</li>
      <li><strong>Export if needed.</strong> Download a CSV of every phrase for a content audit or to share with a writer.</li>
    </ol>

    <h2>How Density Is Calculated</h2>
    <p>The formula is simple: phrase count multiplied by the number of words in the phrase, divided by total words, multiplied by 100.</p>
    <p>For example, a 2 word keyword used 10 times in a 1,000 word article gives (10 &times; 2) &divide; 1,000 &times; 100 = 2.0%.</p>
    <p>Counting the words inside the phrase keeps longer keywords comparable with single words, which is why this tool and most SEO plugins use this method.</p>

    <h2>What Is a Good Keyword Density?</h2>
    <p>There is no official number from Google. Most SEO practitioners treat roughly 0.5% to 2.5% as a comfortable range for a focus keyword.</p>
    <p>Far more important is that the keyword appears in the places that matter: the title, the first paragraph, at least one subheading, and naturally throughout the body.</p>
    <p>If the density climbs above about 3%, read the page out loud. If it sounds repetitive, swap some mentions for synonyms or related terms.</p>

    <h2>Tips for Natural Keyword Use</h2>
    <ul>
      <li>Write for the reader first, then check density as a final pass.</li>
      <li>Use variations and related phrases instead of repeating one exact term.</li>
      <li>Check the 2 and 3 word tabs to discover topics you cover strongly without realising.</li>
      <li>Compare your page with top ranking pages to see which subtopics you might be missing.</li>
    </ul>
    <p>To go deeper, read our guides on <a href="https://brandella.in/semantic-seo-explained-google-understands/">semantic SEO</a>, <a href="https://brandella.in/what-is-search-intent-practical-guide/">search intent</a>, and <a href="https://brandella.in/how-to-write-seo-friendly-blog/">writing an SEO friendly blog</a>.</p>
''',
    faqs=[
        ("What is keyword density in SEO?", "Keyword density is the percentage of words on a page that belong to a specific keyword or phrase. It helps you see whether a keyword is used enough, or so often that it reads as stuffing."),
        ("What is the ideal keyword density?", "Google has never published an ideal number. A focus keyword in the range of about 0.5% to 2.5% usually reads naturally, but placement and readability matter more than hitting an exact figure."),
        ("Can I paste HTML into this keyword density checker?", "Yes. The tool removes tags, scripts and styles before counting, so only the visible text of the page is analysed."),
        ("Is my content stored anywhere?", "No. The keyword density checker runs entirely in your browser. Nothing you paste is uploaded or saved."),
    ],
    related=[("Semantic SEO Explained", "semantic-seo-explained-google-understands"), ("What Is Search Intent", "what-is-search-intent-practical-guide"),
             ("Search Volume vs Keyword Difficulty", "search-volume-vs-keyword-difficulty"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
))

# ---------- 3. SEO SLUG GENERATOR ----------
TOOLS.append(dict(
    slug='seo-slug-generator', short='SG', name='SEO Slug Generator',
    card='Turn any title into a short, clean, search friendly URL slug. Works in bulk, one title per line.',
    title='SEO Slug Generator: Free Clean URL Slug Maker (Bulk)',
    desc='Free SEO slug generator. Turn titles into short, clean URL slugs, remove stop words and accents, and convert many titles at once.',
    h1='SEO Slug Generator',
    lead='Turn page titles into short, clean, search friendly URL slugs. Paste one title or a whole list, one per line.',
    tool=r'''<section class="tool" aria-label="SEO slug generator">
    <div class="card">
      <h2>Enter Titles</h2>
      <div class="field">
        <label for="sgText">Titles <em>one per line</em></label>
        <textarea id="sgText" class="big">How to Improve Your Website's Core Web Vitals in 2026
10 Best Free SEO Tools Every Marketer Should Use
Café Marketing Guide: Résumé of Local SEO &amp; Google Reviews</textarea>
      </div>
      <div class="field">
        <label for="sgBase">Base URL</label>
        <input id="sgBase" type="text" value="https://brandella.in/">
      </div>
      <div class="row2">
        <div class="field">
          <label for="sgSep">Separator</label>
          <select id="sgSep"><option value="-">Hyphen ( - ) recommended</option><option value="_">Underscore ( _ )</option></select>
        </div>
        <div class="field">
          <label for="sgMax">Max Words</label>
          <select id="sgMax"><option value="0">No limit</option><option value="3">3</option><option value="4">4</option><option value="5" selected>5</option><option value="6">6</option><option value="8">8</option></select>
        </div>
      </div>
      <label class="check"><input id="sgStop" type="checkbox" checked> Remove stop words (a, the, of, to...)</label>
      <label class="check"><input id="sgNum" type="checkbox"> Remove numbers and years</label>
      <label class="check"><input id="sgSlash" type="checkbox" checked> Add trailing slash to full URL</label>
    </div>

    <div class="card">
      <h2>Your Slugs</h2>
      <div id="sgOut"></div>
      <div class="actions">
        <button class="btn dark" id="sgCopyAll">Copy All Slugs</button>
        <button class="btn" id="sgClear">Clear</button>
        <span class="toast" id="toast">Copied!</span>
      </div>
      <div class="tips"><strong>Good slug checklist</strong><ul>
        <li>Short, usually 3 to 5 words</li><li>Contains the main keyword</li><li>Lowercase with hyphens</li><li>No dates if the content will be updated</li></ul></div>
    </div>
  </section>''',
    js=STOP_JS + r'''
  function slugify(t, o){
    var s = t.normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/ß/g,'ss').replace(/[æÆ]/g,'ae').replace(/[øØ]/g,'o');
    s = s.replace(/&/g,' and ').replace(/['’]/g,'');
    var ws = s.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
    if (o.num){ ws = ws.filter(function(w){ return !/^\d+$/.test(w); }); }
    if (o.stop){ var f = ws.filter(function(w){ return !STOP.has(w); }); if (f.length) ws = f; }
    if (o.max > 0) ws = ws.slice(0, o.max);
    return ws.join(o.sep);
  }
  var slugs = [];
  function run(){
    var o = { sep:$('sgSep').value, max:+$('sgMax').value, stop:$('sgStop').checked, num:$('sgNum').checked };
    var base = $('sgBase').value.trim(); if (base && !/\/$/.test(base)) base += '/';
    var lines = $('sgText').value.split('\n').map(function(x){ return x.trim(); }).filter(Boolean);
    slugs = lines.map(function(l){ return slugify(l, o); });
    if (!lines.length){ $('sgOut').innerHTML = '<p class="empty">Your slugs will appear here.</p>'; return; }
    $('sgOut').innerHTML = slugs.map(function(s, i){
      var full = base + s + ($('sgSlash').checked && s ? '/' : '');
      var note = s.length > 60 ? '<small class="warn">' + s.length + ' characters, consider shortening</small>' : '<small>' + s.length + ' characters</small>';
      return '<div class="slug-row"><div><div class="s">' + esc(s || '(empty)') + '</div><small>' + esc(full) + '</small>' + note + '</div><button class="btn btn-sm" data-i="' + i + '">Copy</button></div>';
    }).join('');
    $('sgOut').querySelectorAll('button').forEach(function(b){ b.onclick = function(){ copyText(slugs[+b.getAttribute('data-i')], 'toast'); }; });
  }
  ['sgText','sgBase'].forEach(function(id){ $(id).addEventListener('input', run); });
  ['sgSep','sgMax','sgStop','sgNum','sgSlash'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('sgCopyAll').onclick = function(){ copyText(slugs.join('\n'), 'toast'); };
  $('sgClear').onclick = function(){ $('sgText').value=''; run(); $('sgText').focus(); };
  run();
''',
    content=r'''
    <h2>What Is a URL Slug?</h2>
    <p>The slug is the readable part of a URL that identifies a specific page. In <code>brandella.in/title-tag-optimization/</code>, the slug is <code>title-tag-optimization</code>.</p>
    <p>A good slug tells both people and search engines what the page is about before they even click.</p>

    <h2>How to Use This SEO Slug Generator</h2>
    <ol>
      <li><strong>Paste your titles.</strong> Add one title, or a whole list with one title per line for bulk conversion.</li>
      <li><strong>Choose your options.</strong> Remove stop words, limit the number of words, and pick hyphens or underscores.</li>
      <li><strong>Check the result.</strong> Each slug shows its full URL and character count, with a warning if it gets too long.</li>
      <li><strong>Copy.</strong> Copy one slug at a time, or every slug at once for a content plan or spreadsheet.</li>
    </ol>

    <h2>What the Generator Cleans Up</h2>
    <ul>
      <li>Converts everything to lowercase so you never end up with duplicate URLs that differ only by case.</li>
      <li>Turns accented letters into plain ones, so "Café Résumé" becomes "cafe resume".</li>
      <li>Replaces "&amp;" with "and" and drops apostrophes, quotes and other symbols.</li>
      <li>Removes filler words like "the", "of" and "to" when you want a tighter slug.</li>
      <li>Joins words with a single separator and never leaves double or trailing separators.</li>
    </ul>

    <h2>Best Practices for SEO Friendly Slugs</h2>
    <p>Google's own guidance recommends simple, descriptive URLs that use words people understand, separated by hyphens rather than underscores.</p>
    <p>Keep slugs short and focused on the main keyword. Three to five words is usually plenty.</p>
    <p>Avoid putting years or numbers in a slug if you plan to refresh the article later. A slug like <code>seo-best-practices</code> can be updated every year, while one ending in a year will look dated.</p>
    <p>Most importantly, do not change a slug on a published page unless you add a 301 redirect. Our guide to building a <a href="https://brandella.in/redirect-manager-in-php/">redirect manager in PHP</a> shows how. For more on URL design, see <a href="https://brandella.in/url-structure-for-ai-seo/">URL structure for AI SEO</a> and <a href="https://brandella.in/generate-seo-friendly-urls-php/">generating SEO friendly URLs in PHP</a>.</p>
''',
    faqs=[
        ("What makes a URL slug SEO friendly?", "An SEO friendly slug is short, lowercase, descriptive, includes the main keyword, and uses hyphens between words. It avoids stop words, symbols and dates that may go out of date."),
        ("Should I use hyphens or underscores in URLs?", "Use hyphens. Google recommends hyphens to separate words in URLs, because underscores can cause words to be read as one combined term."),
        ("Should I remove stop words from slugs?", "Usually yes, because it keeps the slug short and focused. Keep a stop word only when removing it changes the meaning or makes the slug hard to read."),
        ("Can I convert many titles at once?", "Yes. Paste one title per line and the SEO slug generator creates a slug for each, which you can copy individually or all together."),
    ],
    related=[("URL Structure for AI SEO", "url-structure-for-ai-seo"), ("Generate SEO Friendly URLs in PHP", "generate-seo-friendly-urls-php"),
             ("Redirect Manager in PHP", "redirect-manager-in-php"), ("URL Parameters Explained", "url-parameters-explained-do-they-hurt-seo")],
))

# ---------- 4. META TAG GENERATOR ----------
TOOLS.append(dict(
    slug='meta-tag-generator', short='MT', name='Meta Tag Generator',
    card='Generate title, description, robots, canonical, Open Graph and Twitter tags ready to paste into your page.',
    title='Meta Tag Generator: Free SEO, Open Graph, Twitter Tags',
    desc='Free meta tag generator. Create title, meta description, robots, canonical, Open Graph and Twitter Card tags with live length checks.',
    h1='Meta Tag Generator',
    lead='Fill in a few fields and get clean, ready to paste meta tags for SEO, Facebook, LinkedIn and X (Twitter), with live length checks.',
    tool=r'''<section class="tool" aria-label="Meta tag generator">
    <div class="card">
      <h2>Page Details</h2>
      <div class="field">
        <label for="mtTitle">Page Title <em id="mtTc">0 chars</em></label>
        <input id="mtTitle" type="text" value="Meta Tag Generator: Free SEO, Open Graph and Twitter Tags">
        <div class="meter"><b id="mtTb"></b></div>
        <div class="stat"><span>Best: 50 to 60 characters</span><span id="mtTm"></span></div>
      </div>
      <div class="field">
        <label for="mtDesc">Meta Description <em id="mtDc">0 chars</em></label>
        <textarea id="mtDesc">Free meta tag generator. Create title, meta description, robots, canonical, Open Graph and Twitter Card tags with live length checks.</textarea>
        <div class="meter"><b id="mtDb"></b></div>
        <div class="stat"><span>Best: 120 to 158 characters</span><span id="mtDm"></span></div>
      </div>
      <div class="field">
        <label for="mtUrl">Canonical URL</label>
        <input id="mtUrl" type="text" value="https://brandella.in/tools/seo-tools/meta-tag-generator/">
      </div>
      <div class="field">
        <label for="mtImg">Share Image URL <em>1200 &times; 630 px</em></label>
        <input id="mtImg" type="text" placeholder="https://example.com/image.jpg">
      </div>
      <div class="row2">
        <div class="field">
          <label for="mtSite">Site Name</label>
          <input id="mtSite" type="text" value="Brandella Journal">
        </div>
        <div class="field">
          <label for="mtTw">X / Twitter Handle <em>optional</em></label>
          <input id="mtTw" type="text" placeholder="@yourhandle">
        </div>
      </div>
      <div class="row2">
        <div class="field">
          <label for="mtIndex">Indexing</label>
          <select id="mtIndex"><option value="index">Index</option><option value="noindex">Noindex</option></select>
        </div>
        <div class="field">
          <label for="mtFollow">Links</label>
          <select id="mtFollow"><option value="follow">Follow</option><option value="nofollow">Nofollow</option></select>
        </div>
      </div>
      <div class="row2">
        <div class="field">
          <label for="mtType">Content Type</label>
          <select id="mtType"><option value="website">Website / page</option><option value="article">Article / blog post</option><option value="product">Product</option></select>
        </div>
        <div class="field">
          <label for="mtLang">Language</label>
          <select id="mtLang"><option value="en_US">English (US)</option><option value="en_GB">English (UK)</option><option value="en_IN">English (India)</option><option value="">Not set</option></select>
        </div>
      </div>
      <label class="check"><input id="mtBasic" type="checkbox" checked> Include charset and viewport tags</label>
    </div>

    <div class="card">
      <h2>Your Meta Tags</h2>
      <pre class="code-out" id="mtCode" style="display:block;margin-top:0;max-height:560px;overflow:auto;word-break:normal;overflow-wrap:anywhere"></pre>
      <div class="actions">
        <button class="btn dark" id="mtCopy">Copy Code</button>
        <button class="btn" id="mtClear">Clear</button>
        <span class="toast" id="toast">Copied!</span>
      </div>
      <div class="tips"><strong>Where to paste</strong><ul>
        <li>Inside the <code>&lt;head&gt;</code> section of your page</li>
        <li>WordPress users: enter the title and description in Rank Math or Yoast instead</li>
        <li>Test social previews after publishing</li></ul></div>
    </div>
  </section>''',
    js=r'''
  var ids = ['mtTitle','mtDesc','mtUrl','mtImg','mtSite','mtTw','mtIndex','mtFollow','mtType','mtLang','mtBasic'];
  function meter(len, lo, hi, bar, msg){
    var max = hi * 1.25;
    bar.style.width = Math.min(100, len/max*100) + '%';
    if (!len){ bar.className=''; msg.textContent=''; msg.className=''; return; }
    if (len > hi){ bar.className='bad'; msg.textContent='Too long'; msg.className='bad'; }
    else if (len < lo){ bar.className='warn'; msg.textContent='A bit short'; msg.className='warn'; }
    else { bar.className=''; msg.textContent='Good length'; msg.className='ok'; }
  }
  function a(s){ return esc(s.trim()); }
  function build(){
    var t=$('mtTitle').value.trim(), dsc=$('mtDesc').value.trim().replace(/\s+/g,' '), u=$('mtUrl').value.trim(), img=$('mtImg').value.trim(),
        site=$('mtSite').value.trim(), tw=$('mtTw').value.trim(), type=$('mtType').value, lang=$('mtLang').value;
    if (tw && tw.charAt(0) !== '@') tw = '@' + tw;
    $('mtTc').textContent = t.length + ' chars'; $('mtDc').textContent = dsc.length + ' chars';
    meter(t.length, 50, 60, $('mtTb'), $('mtTm')); meter(dsc.length, 120, 158, $('mtDb'), $('mtDm'));
    var L = [];
    if ($('mtBasic').checked){ L.push('<meta charset="UTF-8">'); L.push('<meta name="viewport" content="width=device-width, initial-scale=1">'); }
    L.push('');
    L.push('<!-- Primary SEO tags -->');
    if (t) L.push('<title>' + a(t) + '</title>');
    if (dsc) L.push('<meta name="description" content="' + a(dsc) + '">');
    L.push('<meta name="robots" content="' + $('mtIndex').value + ', ' + $('mtFollow').value + '">');
    if (u) L.push('<link rel="canonical" href="' + a(u) + '">');
    L.push('');
    L.push('<!-- Open Graph (Facebook, LinkedIn, WhatsApp) -->');
    L.push('<meta property="og:type" content="' + type + '">');
    if (t) L.push('<meta property="og:title" content="' + a(t) + '">');
    if (dsc) L.push('<meta property="og:description" content="' + a(dsc) + '">');
    if (u) L.push('<meta property="og:url" content="' + a(u) + '">');
    if (img){ L.push('<meta property="og:image" content="' + a(img) + '">'); L.push('<meta property="og:image:width" content="1200">'); L.push('<meta property="og:image:height" content="630">'); }
    if (site) L.push('<meta property="og:site_name" content="' + a(site) + '">');
    if (lang) L.push('<meta property="og:locale" content="' + lang + '">');
    L.push('');
    L.push('<!-- X (Twitter) Card -->');
    L.push('<meta name="twitter:card" content="' + (img ? 'summary_large_image' : 'summary') + '">');
    if (t) L.push('<meta name="twitter:title" content="' + a(t) + '">');
    if (dsc) L.push('<meta name="twitter:description" content="' + a(dsc) + '">');
    if (img) L.push('<meta name="twitter:image" content="' + a(img) + '">');
    if (tw) L.push('<meta name="twitter:site" content="' + a(tw) + '">');
    while (L.length && L[0]==='') L.shift();
    $('mtCode').textContent = L.join('\n');
  }
  ids.forEach(function(id){ var e=$(id); e.addEventListener(e.tagName==='SELECT' || e.type==='checkbox' ? 'change' : 'input', build); });
  $('mtCopy').onclick = function(){ copyText($('mtCode').textContent, 'toast'); };
  $('mtClear').onclick = function(){ ['mtTitle','mtDesc','mtUrl','mtImg','mtTw'].forEach(function(id){ $(id).value=''; }); build(); $('mtTitle').focus(); };
  build();
''',
    content=r'''
    <h2>What Are Meta Tags?</h2>
    <p>Meta tags are small pieces of HTML in a page's <code>&lt;head&gt;</code> that describe the page to search engines and social networks. Visitors do not see them on the page itself.</p>
    <p>They control the blue title and description in Google, whether a page can be indexed, which URL is the main version, and how the link looks when someone shares it.</p>

    <h2>How to Use This Meta Tag Generator</h2>
    <ol>
      <li><strong>Enter your title and description.</strong> The bars show whether each one is a comfortable length.</li>
      <li><strong>Add the canonical URL and a share image.</strong> A 1200 by 630 pixel image works well on every major network.</li>
      <li><strong>Pick indexing options.</strong> Leave "Index" and "Follow" for normal pages. Use "Noindex" for thank you pages, internal search results or staging copies.</li>
      <li><strong>Copy the code.</strong> Paste it inside the head of your page, replacing any older duplicates.</li>
    </ol>

    <h2>Tags This Tool Creates</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Tag</th><th style="background:#2b2b2b !important; color:#ffffff !important;">What It Does</th></tr></thead>
      <tbody>
        <tr><td>Title</td><td>The clickable headline in search results and the browser tab name</td></tr>
        <tr><td>Meta description</td><td>The summary Google may show under your title</td></tr>
        <tr><td>Robots</td><td>Tells search engines whether to index the page and follow its links</td></tr>
        <tr><td>Canonical</td><td>Names the preferred URL when similar versions exist</td></tr>
        <tr><td>Open Graph</td><td>Controls link previews on Facebook, LinkedIn and WhatsApp</td></tr>
        <tr><td>Twitter Card</td><td>Controls link previews on X</td></tr>
      </tbody>
    </table>

    <h2>Common Meta Tag Mistakes</h2>
    <ul>
      <li>Reusing the same title and description on many pages.</li>
      <li>Leaving a "noindex" tag on a page after it moves from staging to live.</li>
      <li>Pointing the canonical tag at the wrong URL, or at a page that redirects.</li>
      <li>Forgetting the share image, which makes social posts look bare.</li>
    </ul>
    <p>Learn more in our guides to <a href="https://brandella.in/meta-robots-tags-explained/">meta robots tags</a>, <a href="https://brandella.in/what-is-canonical-tag/">the canonical tag</a>, and <a href="https://brandella.in/title-tag-optimization/">title tag optimization</a>. You can also check how your title will look with our <a href="https://brandella.in/tools/seo-tools/serp-snippet-preview/">SERP snippet preview tool</a>.</p>
''',
    faqs=[
        ("Which meta tags are most important for SEO?", "The title tag and meta description matter most for how your result looks in Google. The robots and canonical tags matter for whether and how the page is indexed."),
        ("Does the meta keywords tag help SEO?", "No. Google has ignored the meta keywords tag for many years, so this meta tag generator does not include it."),
        ("What is the difference between Open Graph and Twitter Card tags?", "Open Graph tags control link previews on Facebook, LinkedIn, WhatsApp and many other apps. Twitter Card tags do the same for X, which also falls back to Open Graph when its own tags are missing."),
        ("I use WordPress. Do I still need this?", "SEO plugins like Rank Math and Yoast create these tags for you. The generator is still useful for custom pages, landing pages, static sites and for checking what your plugin should output."),
    ],
    related=[("Meta Robots Tags Explained", "meta-robots-tags-explained"), ("What Is a Canonical Tag", "what-is-canonical-tag"),
             ("Title Tag Optimization", "title-tag-optimization"), ("Dynamic Meta Tags in PHP", "dynamic-meta-tags-php")],
))

# ---------- 5. HEADING STRUCTURE CHECKER ----------
TOOLS.append(dict(
    slug='heading-structure-checker', short='HS', name='Heading Structure Checker',
    card='Paste page HTML to see its H1 to H6 outline and catch missing H1s, duplicates and skipped levels.',
    title='Heading Structure Checker: Free H1 to H6 Outline Tool',
    desc='Free heading structure checker. Paste HTML to see the H1 to H6 outline and find missing or multiple H1s, skipped levels and empty headings.',
    h1='Heading Structure Checker',
    lead='Paste your page HTML to see its heading outline at a glance, and catch missing H1s, skipped levels and other structure problems.',
    tool=r'''<section class="tool" aria-label="Heading structure checker">
    <div class="card">
      <h2>Paste Page HTML</h2>
      <div class="field">
        <label for="hsText">HTML Source <em id="hsChars">0 chars</em></label>
        <textarea id="hsText" class="big mono" placeholder="Paste the full HTML of your page here..."></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="hsSample">Load Sample</button>
        <button class="btn" id="hsClear">Clear</button>
      </div>
      <div class="tips"><strong>How to get the HTML</strong><ul>
        <li>Open your page in Chrome and press <strong>Ctrl + U</strong> (Mac: Cmd + Option + U)</li>
        <li>Select all, copy, and paste it here</li>
        <li>Or paste just the article HTML from your editor</li></ul></div>
    </div>

    <div class="card">
      <h2>Heading Outline</h2>
      <div class="chips" id="hsChips"></div>
      <div class="kw-result" id="hsSummary">Paste HTML to check its headings.</div>
      <div id="hsOutline"></div>
    </div>
  </section>''',
    js=r'''
  var SAMPLE = '<h1>Complete Guide to Local SEO</h1>\n<p>Intro...</p>\n<h2>What Is Local SEO?</h2>\n<h3>Why It Matters</h3>\n<h2>Google Business Profile</h2>\n<h4>Choosing Categories</h4>\n<h2>Local Citations</h2>\n<h1>Get More Reviews</h1>\n<h3></h3>\n<h2>Local Citations</h2>';
  function run(){
    var raw = $('hsText').value;
    $('hsChars').textContent = raw.length + ' chars';
    var doc = new DOMParser().parseFromString(raw, 'text/html');
    var hs = Array.prototype.slice.call(doc.querySelectorAll('h1,h2,h3,h4,h5,h6'));
    var counts = [0,0,0,0,0,0];
    hs.forEach(function(h){ counts[+h.tagName[1]-1]++; });
    $('hsChips').innerHTML = counts.map(function(c,i){ return '<span class="chip' + (c?'':' zero') + '">H' + (i+1) + ': ' + c + '</span>'; }).join('');
    var box = $('hsSummary');
    if (!raw.trim()){ box.className='kw-result'; box.textContent='Paste HTML to check its headings.'; $('hsOutline').innerHTML=''; return; }
    if (!hs.length){ box.className='kw-result bad'; box.textContent='No headings found. Search engines and screen readers rely on headings to understand page structure.'; $('hsOutline').innerHTML=''; return; }
    var issues = [], prev = 0, seen = {}, rowIssues = [];
    hs.forEach(function(h, i){
      var lvl = +h.tagName[1], txt = h.textContent.replace(/\s+/g,' ').trim(), my = [];
      if (prev && lvl > prev + 1) my.push('Skips from H' + prev + ' to H' + lvl);
      if (!txt) my.push('Empty heading');
      if (txt.length > 70) my.push('Long (' + txt.length + ' chars)');
      var key = lvl + '|' + txt.toLowerCase();
      if (txt && seen[key]) my.push('Duplicate'); seen[key] = 1;
      rowIssues.push(my); prev = lvl;
    });
    if (counts[0] === 0) issues.push('No H1 found. Every page should have one main heading.');
    if (counts[0] > 1) issues.push(counts[0] + ' H1 tags found. Use one H1 for the main topic.');
    if (+hs[0].tagName[1] !== 1) issues.push('The first heading is not an H1.');
    var rowCount = rowIssues.filter(function(x){ return x.length; }).length;
    if (rowCount) issues.push(rowCount + ' heading' + (rowCount===1?' has':'s have') + ' an issue, marked in red below.');
    if (!issues.length){ box.className='kw-result ok'; box.innerHTML='<strong>Looks good.</strong> ' + hs.length + ' headings with one H1 and no skipped levels.'; }
    else { box.className='kw-result ' + (counts[0]!==1 ? 'bad' : 'warn'); box.innerHTML='<strong>' + issues.length + ' thing' + (issues.length===1?'':'s') + ' to fix:</strong><br>' + issues.map(esc).join('<br>'); }
    $('hsOutline').innerHTML = '<div class="outline">' + hs.map(function(h, i){
      var lvl = +h.tagName[1], txt = h.textContent.replace(/\s+/g,' ').trim();
      return '<div class="o-row" style="padding-left:' + ((lvl-1)*20) + 'px"><span class="o-tag h' + lvl + '">H' + lvl + '</span><span>' + (txt ? esc(txt) : '<em style="color:#999">(empty)</em>') +
        rowIssues[i].map(function(x){ return '<span class="o-issue">' + esc(x) + '</span>'; }).join('') + '</span></div>';
    }).join('') + '</div>';
  }
  $('hsText').addEventListener('input', run);
  $('hsSample').onclick = function(){ $('hsText').value = SAMPLE; run(); };
  $('hsClear').onclick = function(){ $('hsText').value = ''; run(); $('hsText').focus(); };
  $('hsText').value = SAMPLE; run();
''',
    content=r'''
    <h2>Why Heading Structure Matters</h2>
    <p>Headings (H1 to H6) are the outline of your page. They help readers scan, help screen reader users jump between sections, and help search engines understand which topics the page covers.</p>
    <p>A clean outline is one of the simplest on page improvements you can make, and it often reveals content gaps at the same time.</p>

    <h2>How to Use This Heading Structure Checker</h2>
    <ol>
      <li><strong>Copy your page HTML.</strong> In Chrome, press Ctrl + U to view the source, then copy everything. Pasting just the article HTML also works.</li>
      <li><strong>Paste it into the box.</strong> The outline appears instantly, indented by level.</li>
      <li><strong>Read the summary.</strong> It flags missing or multiple H1s and tells you how many headings need attention.</li>
      <li><strong>Fix the red notes.</strong> Each problem heading shows exactly what is wrong next to it.</li>
    </ol>

    <h2>What the Checker Looks For</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Check</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Why It Matters</th></tr></thead>
      <tbody>
        <tr><td>Missing H1</td><td>The page has no clear main topic heading</td></tr>
        <tr><td>Multiple H1s</td><td>The main topic becomes less clear</td></tr>
        <tr><td>Skipped levels</td><td>Jumping from H2 to H4 breaks the logical outline</td></tr>
        <tr><td>Empty headings</td><td>Often left by page builders, confusing for screen readers</td></tr>
        <tr><td>Duplicate headings</td><td>Two sections with the same name usually signal repetition</td></tr>
        <tr><td>Very long headings</td><td>Headings over 70 characters are harder to scan</td></tr>
      </tbody>
    </table>

    <h2>Tips for a Clean Heading Outline</h2>
    <ul>
      <li>Use one H1 that matches the page's main topic and keyword.</li>
      <li>Use H2s for the main sections and H3s for points inside them.</li>
      <li>Never pick a heading level just to change the font size. Use CSS for styling.</li>
      <li>Read the outline on its own. If it tells the story of the page, it is doing its job.</li>
    </ul>
    <p>For more detail, read our guides on <a href="https://brandella.in/html-heading-structure-best-practices/">HTML heading structure best practices</a>, <a href="https://brandella.in/html-semantic-elements-explained/">HTML semantic elements</a>, and <a href="https://brandella.in/structuring-html-for-ai-crawlability/">structuring HTML for AI crawlability</a>.</p>
''',
    faqs=[
        ("Can a page have more than one H1?", "HTML allows it, and Google has said it is not a ranking problem on its own. Still, one clear H1 makes the main topic obvious for readers, screen readers and search engines, so it remains the recommended approach."),
        ("Is skipping heading levels bad for SEO?", "It is unlikely to hurt rankings directly, but skipped levels break the logical outline and make pages harder to navigate with assistive technology. Fixing them is a quick accessibility win."),
        ("Does this heading structure checker fetch my live page?", "No. For privacy and reliability it works only with HTML you paste. Everything runs in your browser and nothing is uploaded."),
        ("Why does my WordPress page show extra headings?", "Themes and page builders often add headings in the sidebar, footer or widgets. Paste only the article HTML if you want to check the content alone."),
    ],
    related=[("HTML Heading Structure Best Practices", "html-heading-structure-best-practices"), ("HTML Semantic Elements Explained", "html-semantic-elements-explained"),
             ("Structuring HTML for AI Crawlability", "structuring-html-for-ai-crawlability"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
))


# ======================= LOAD BATCHES AND CATEGORIES =======================
import glob, importlib, datetime
from categories import CATEGORIES
for t in TOOLS:
    t.setdefault('cat', 'seo-tools'); t.setdefault('updated', '2026-10-28')
for f in sorted(glob.glob(os.path.join(HERE, 'batch*.py'))):
    importlib.import_module(os.path.basename(f)[:-3]).add(TOOLS, STOP_JS)
for t in TOOLS:
    t.setdefault('cat', 'seo-tools'); t.setdefault('updated', '2026-10-28')
CAT = {c['slug']: c for c in CATEGORIES}
for t in TOOLS: assert t['cat'] in CAT, 'unknown category ' + t['cat']
slugs = [t['cat'] + '/' + t['slug'] for t in TOOLS]; assert len(slugs) == len(set(slugs)), 'duplicate tool slug'
def tools_in(cat): return [t for t in TOOLS if t['cat'] == cat]
LIVE = [c for c in CATEGORIES if tools_in(c['slug'])]
def caturl(c): return BASE + '/tools/' + c + '/'
def turl(t): return caturl(t['cat']) + t['slug'] + '/'

# Tools dropdown in header lists every live category
_sub = ''.join(f'\n            <li><a href="{caturl(c["slug"])}">{c["name"]}</a></li>' for c in LIVE)
_tc = [(c['name'], caturl(c['slug'])) for c in LIVE]
HEADER = header_html(_tc)
FOOTER = footer_html(_tc)

def card(t, h='h3'):
    return f'<a class="tcard" href="{turl(t)}"><div class="tbadge">{t["short"]}</div><{h}>{t["name"]}</{h}><p>{t["card"]}</p><span class="go">Open tool &rarr;</span></a>'

def more_tools(t):
    c = CAT[t['cat']]
    same = [x for x in tools_in(t['cat']) if x['slug'] != t['slug']]
    other = [x for x in TOOLS if x['cat'] != t['cat']][:max(0, 3 - len(same))]
    return f"""<section class="content more-tools" style="max-width:1140px">
    <h2>More Free {c['name']}</h2>
    <div class="tgrid">
      {chr(10).join(card(x) for x in same + other)}
    </div>
    <p><a href="{caturl(c['slug'])}">See all {c['name'].lower()} &rarr;</a> &nbsp;|&nbsp; <a href="{BASE}/tools/">Browse every free tool &rarr;</a></p>
  </section>"""

def build_tool(t):
    c = CAT[t['cat']]; url = turl(t)
    bc = [("Home", BASE + '/'), ("Tools", BASE + '/tools/'), (c['name'], caturl(c['slug'])), (t['name'], url)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": t['name'], "url": url, "applicationCategory": c.get('app_category', 'BusinessApplication'),
         "operatingSystem": "Any (web browser)", "description": t['desc'],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "publisher": {"@type": "Organization", "name": "Brandella Journal", "url": BASE + '/'}},
        bc_schema(bc), faq_schema(t['faqs'])]}
    main = f"""
  {crumbs([(n, u) for n, u in bc[:-1]] + [(t['name'], None)])}

  <section class="hero">
    <span class="pill">Free {c['pill']} Tool</span>
    <h1>{t['h1']}</h1>
    <p>{t['lead']}</p>
  </section>

  {t['tool']}

  {AD}

  <article class="content">
{t['content']}
    {AD}

    {faq_html(t['faqs'])}

    {related_html(t['related'])}
  </article>

  {more_tools(t)}
"""
    return page(t['title'], t['desc'], url, schema, main, t['js'], og=t['slug'])

def build_hub(c):
    url = caturl(c['slug']); ts = tools_in(c['slug'])
    bc = [("Home", BASE + '/'), ("Tools", BASE + '/tools/'), (c['name'], url)]
    faqs = c.get('faqs') or [
        (f"Are these {c['name'].lower()} free?", "Yes. Every tool on this page is free, needs no signup, and has no usage limits."),
        ("Is my data safe?", "All tools run entirely in your browser. Anything you type or paste is never uploaded or stored on our servers."),
        ("Will you add more tools?", "Yes. New free tools are added to Brandella Journal regularly across SEO, paid media, analytics, content and development.")]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Free " + c['name'], "url": url, "description": c['hub_desc'],
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": t['name'], "url": turl(t)} for i, t in enumerate(ts)]}},
        bc_schema(bc), faq_schema(faqs)]}
    intro = c.get('hub_intro') or (f"<h2>About These {c['name']}</h2>\n    <p>{c['hub_lead']}</p>\n    <ul>\n" +
        '\n'.join(f'      <li><a href="{turl(t)}"><strong>{t["name"]}</strong></a>: {t["card"]}</li>' for t in ts) + '\n    </ul>')
    main = f"""
  {crumbs([("Home", BASE + '/'), ("Tools", BASE + '/tools/'), (c['name'], None)])}

  <section class="hero">
    <span class="pill">Free Tools</span>
    <h1>Free {c['name']}</h1>
    <p>{c['hub_lead']}</p>
  </section>

  <div class="tgrid">
    {chr(10).join(card(t, 'h2') for t in ts)}
  </div>

  {AD}

  <article class="content">
    {intro}

    {faq_html(faqs)}
  </article>
"""
    return page(c['hub_title'], c['hub_desc'], url, schema, main, og='cat-' + c['slug'])

def build_index():
    url = BASE + '/tools/'
    bc = [("Home", BASE + '/'), ("Tools", url)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Free Marketing Tools", "url": url, "description": "Free SEO and digital marketing tools by Brandella Journal.",
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": c['name'], "url": caturl(c['slug'])} for i, c in enumerate(LIVE)]}},
        bc_schema(bc)]}
    cards = []
    for c in CATEGORIES:
        n = len(tools_in(c['slug']))
        if n: cards.append(f'<a class="tcard" href="{caturl(c["slug"])}"><div class="tbadge">{c["short"]}</div><h2>{c["name"]}</h2><p>{c["card"]}</p><span class="go">{n} tools &rarr;</span></a>')
        else: cards.append(f'<div class="tcard soon"><div class="tbadge">{c["short"]}</div><h2>{c["name"]}</h2><p>{c["card"]}</p><span class="go">Coming soon</span></div>')
    total = len(TOOLS)
    main = f"""
  {crumbs([("Home", BASE + '/'), ("Tools", None)])}

  <section class="hero">
    <span class="pill">Free Tools</span>
    <h1>Free Marketing Tools</h1>
    <p>{total} free, browser based tools for SEO, paid media, content and analytics. Built by Brandella Journal to make everyday marketing tasks faster.</p>
  </section>

  <div class="tgrid">
    {chr(10).join(cards)}
  </div>

  {AD}
"""
    return page('Free Marketing Tools: SEO, PPC and Content Tools',
                f'{total} free browser based marketing tools from Brandella Journal for SEO, PPC, content, social media and analytics. No signup needed.',
                url, schema, main)

# ======================= WRITE =======================
if os.path.exists(OUT): shutil.rmtree(OUT)
def w(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w').write(s)
w(OUT + '/index.html', build_index())
for c in LIVE:
    w(OUT + '/' + c['slug'] + '/index.html', build_hub(c))
for t in TOOLS:
    w(OUT + '/' + t['cat'] + '/' + t['slug'] + '/index.html', build_tool(t))
print('built', len(TOOLS), 'tools in', len(LIVE), 'categories')

# ======================= OG IMAGES =======================
from PIL import Image, ImageDraw, ImageFont
def font(size, bold=True):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(f, size) if os.path.exists(f) else ImageFont.load_default()
def og_image(name, title, sub, badge):
    im = Image.new('RGB', (1200, 630), '#0a0a0a'); d = ImageDraw.Draw(im)
    d.rectangle([0, 600, 1200, 630], fill='#a6ef39')
    d.text((70, 60), 'Brandella ', font=font(40), fill='#bbbbbb')
    d.text((70 + d.textlength('Brandella ', font=font(40)), 60), 'Journal', font=font(40), fill='#6cc82a')
    bw = d.textlength(badge, font=font(24))
    d.rounded_rectangle([70, 150, 70 + bw + 50, 200], radius=25, outline='#6cc82a', width=3)
    d.text((95, 160), badge, font=font(24), fill='#a6ef39')
    lines, cur = [], ''
    for w_ in title.split():
        if d.textlength((cur + ' ' + w_).strip(), font=font(78)) > 1060: lines.append(cur); cur = w_
        else: cur = (cur + ' ' + w_).strip()
    lines.append(cur)
    y = 240
    for l in lines[:2]: d.text((70, y), l, font=font(78), fill='#ffffff'); y += 95
    d.text((70, y + 20), sub, font=font(30, False), fill='#b5b5b5')
    os.makedirs(OUT + '/assets', exist_ok=True); im.save(OUT + f'/assets/og-{name}.png', optimize=True)
for t in TOOLS: og_image(t['slug'], t['name'], 'No signup. Runs in your browser.', 'FREE ' + CAT[t['cat']]['pill'].upper() + ' TOOL')
for c in LIVE: og_image('cat-' + c['slug'], 'Free ' + c['name'], f"{len(tools_in(c['slug']))} free tools. No signup needed.", 'FREE TOOLS')
og_image('tools', 'Free Marketing Tools', f'{len(TOOLS)} free tools for SEO, PPC, content and analytics.', 'FREE TOOLS')

# ======================= SITEMAP =======================
def mx(ds): return max(ds) if ds else '2026-10-28'
urls = [(BASE + '/tools/', mx([t['updated'] for t in TOOLS]))]
for c in LIVE:
    urls.append((caturl(c['slug']), mx([t['updated'] for t in tools_in(c['slug'])])))
    urls += [(turl(t), t['updated']) for t in tools_in(c['slug'])]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     ''.join(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n' for u, d in urls) + '</urlset>\n'
w(OUT + '/sitemap.xml', sm)
print('og images + sitemap with', len(urls), 'urls')
