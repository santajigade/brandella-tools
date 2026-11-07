"""SEO checks for every built tool page. Exit code 1 if any FAIL."""
import os, re, json, sys
from html.parser import HTMLParser

ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/brandella_tools/out/tools'

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.title=''; s.meta={}; s.links=[]; s.canon=None
        s.h1=[]; s.hs=[]; s.cur=None; s.text=[]; s.ld=[]; s.inld=False; s.imgs=[]; s.lang=None
    def handle_starttag(s, t, a):
        a=dict(a)
        if t not in ('meta','link','input','br','img','hr','source','wbr'): s.stack.append(t)
        if t=='html': s.lang=a.get('lang')
        if t=='meta':
            k=a.get('name') or a.get('property')
            if k: s.meta[k]=a.get('content','')
        if t=='link' and a.get('rel')=='canonical': s.canon=a.get('href')
        if t=='a' and a.get('href'): s.links.append(a['href'])
        if t=='img': s.imgs.append(a)
        if t in ('h1','h2','h3','h4','h5','h6'): s.cur=[t,'']
        if t=='script' and a.get('type')=='application/ld+json': s.inld=True; s.ld.append('')
    def handle_endtag(s, t):
        if t in s.stack:
            while s.stack and s.stack.pop()!=t: pass
        if s.cur and t==s.cur[0]:
            s.hs.append((s.cur[0], s.cur[1].strip()))
            if t=='h1': s.h1.append(s.cur[1].strip())
            s.cur=None
        if t=='script': s.inld=False
    def handle_data(s, d):
        if s.inld: s.ld[-1]+=d; return
        if 'title' in s.stack[-1:] : s.title+=d
        if s.cur: s.cur[1]+=d
        if not any(x in s.stack for x in ('script','style','head','textarea','pre','code','nav','select')):
            s.text.append(d)

SLUGS = set(l.strip() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'article-slugs.txt')) if l.strip() and not l.startswith('#'))
BUILT = set()
for dp_,_,fs_ in os.walk(ROOT):
    if 'index.html' in fs_: BUILT.add('https://brandella.in/' + os.path.relpath(dp_, os.path.dirname(ROOT)).rstrip('.') + '/')
def bad_links(src):
    main = src.split('<main', 1)[-1].split('</main>', 1)[0]
    out = []
    for h in re.findall(r'href="(https://brandella\.in/[^"#?]*)"', main):
        if h.startswith('https://brandella.in/tools/'):
            if h not in BUILT: out.append(h)
        elif h != 'https://brandella.in/':
            slug = h[len('https://brandella.in/'):].strip('/')
            if slug not in SLUGS: out.append(h)
    return sorted(set(out))
results=[]; titles={}; descs={}
for dp,_,fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.html'): continue
        path=os.path.join(dp,f); src=open(path).read(); p=P(); p.feed(src)
        pi=P(); pi.feed(re.sub(r'<!--chrome:(header|footer)-->.*?<!--/chrome:\1-->', '', src, flags=re.S))  # images in the shared header and footer are checked by the main site
        rel=os.path.relpath(path, os.path.dirname(ROOT))
        url='https://brandella.in/'+os.path.dirname(rel)+'/'
        R=[]
        def chk(ok, msg, level='FAIL'): R.append(('PASS' if ok else level, msg))
        t=p.title.strip(); d=p.meta.get('description','')
        chk(30<=len(t)<=60, f'Title length {len(t)} (30 to 60)')
        chk(120<=len(d)<=160, f'Meta description length {len(d)} (120 to 160)')
        chk(p.canon==url, f'Canonical self referencing ({p.canon})')
        chk(len(p.h1)==1, f'Exactly one H1 ({len(p.h1)})')
        lv=[int(h[0][1]) for h in p.hs]; skip=[ (a,b) for a,b in zip(lv,lv[1:]) if b>a+1]
        chk(not skip, f'No skipped heading levels {skip if skip else ""}', 'WARN')
        chk(all(h[1] for h in p.hs), 'No empty headings')
        chk(p.meta.get('robots','index').startswith('index'), 'Indexable (robots index)')
        chk(p.lang=='en', 'html lang set')
        chk('viewport' in p.meta, 'Viewport meta present')
        for k in ('og:title','og:description','og:url','og:image'): chk(k in p.meta, f'{k} present', 'WARN' if k=='og:image' else 'FAIL')
        types=[]; okld=True
        for b in p.ld:
            try:
                j=json.loads(b); g=j.get('@graph',[j]); types+= [x.get('@type') for x in g]
            except Exception as e: okld=False
        chk(okld and p.ld, f'Valid JSON LD ({", ".join(types)})')
        chk('BreadcrumbList' in types, 'Breadcrumb schema')
        words=len(re.findall(r"[A-Za-z0-9']+", ' '.join(p.text)))
        chk(words>=300 or rel.count('/')<=2, f'Visible word count {words} (300+ on tool pages)', 'WARN')
        internal=[l for l in p.links if 'brandella.in' in l]
        chk(len(set(internal))>=8, f'Internal links {len(set(internal))}')
        chk(all(i.get('alt') for i in pi.imgs), 'All images have alt')
        bl = bad_links(src)
        chk(not bl, f'All brandella.in links in main point to real pages {bl[:4] if bl else ""}')
        vis=' '.join(p.text); dash=re.findall(r'\w[—–]\w|\w—|—\w|\b[a-z]+-[a-z]+\b', vis)
        chk(not dash, f'No dashes in visible text {dash[:3] if dash else ""}', 'WARN')
        if t in titles: chk(False, f'Duplicate title with {titles[t]}')
        if d in descs: chk(False, f'Duplicate description with {descs[d]}')
        titles[t]=rel; descs[d]=rel
        results.append((rel,R))

fails=0
for rel,R in sorted(results):
    bad=[r for r in R if r[0]!='PASS']
    fails+=sum(1 for r in R if r[0]=='FAIL')
    print(f"\n{'OK  ' if not bad else 'FIX '} {rel}  ({sum(1 for r in R if r[0]=='PASS')}/{len(R)} pass)")
    for lvl,m in bad: print(f'   {lvl}: {m}')
print(f'\nTOTAL FAILS: {fails}')
sys.exit(1 if fails else 0)
