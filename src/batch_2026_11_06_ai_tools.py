"""Batch 9 (2026-11-06): AI Tools category, 7 tools.
Facts checked 2026-11-06 against: llmstxt.org spec (H1 name is the only required part, then blockquote summary,
detail sections without headings, H2 file lists of [name](url): notes, an "Optional" H2 for secondary links,
.md versions of pages), Google Search Central AI optimization guide mythbusting (June 2026: Google Search does not
use llms.txt or other AI text files, they neither help nor harm Google rankings), OpenAI "Overview of OpenAI
crawlers" (GPTBot training, OAI-SearchBot ChatGPT search, ChatGPT-User user actions that may not follow robots.txt,
OAI-AdsBot ad landing pages), Anthropic crawler docs via Search Engine Roundtable (ClaudeBot training,
Claude-SearchBot search, Claude-User user fetch, robots.txt and Crawl-delay honoured), Perplexity crawler docs
(PerplexityBot search not training, Perplexity-User user fetch generally ignores robots.txt), Meta Web Crawlers
(Meta-ExternalAgent training, Meta-WebIndexer Meta AI search, Meta-ExternalFetcher user fetch), Amazon Developer
"About Amazonbot" (Amazonbot may train models, Amzn-SearchBot search, Amzn-User user fetch), Apple "About Applebot"
(Applebot-Extended does not crawl, it is only a robots.txt control), OpenAI Help "What are tokens" (1 token is about
4 characters or three quarters of a word in English, 100 tokens about 75 words), Claude prompting best practices
(clear explicit instructions, explain why, 3 to 5 examples, XML tags, role, say what to do not what to avoid, long
documents at the top)."""
import html as _h

T = 'https://brandella.in/tools/ai-tools/'
TS = 'https://brandella.in/tools/technical-seo-tools/'
SEO = 'https://brandella.in/tools/seo-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'
TH = '<thead><tr style="background:#2b2b2b !important;">'
def th(*cols):
    return TH + ''.join(f'<th style="background:#2b2b2b !important; color:#ffffff !important;">{c}</th>' for c in cols) + '</tr></thead>'

def F(i, label, val='', em='', tag='input', opts=None, ph='', extra='', mono=False, typ='text'):
    lab = f'<label for="{i}">{label}' + (f' <em>{em}</em>' if em else '') + '</label>'
    cls = ' class="mono"' if mono else ''
    if tag == 'select':
        o = ''
        for x in opts:
            v, t = (x, x) if isinstance(x, str) else x
            o += f'<option value="{v}"' + (' selected' if v == val else '') + f'>{t}</option>'
        ctl = f'<select id="{i}">{o}</select>'
    elif tag == 'textarea':
        ctl = f'<textarea id="{i}"{cls} spellcheck="false" placeholder="{_h.escape(ph)}"{extra}>{_h.escape(val)}</textarea>'
    else:
        ctl = f'<input id="{i}"{cls} type="{typ}" autocomplete="off" spellcheck="false" value="{_h.escape(val)}" placeholder="{_h.escape(ph)}"{extra}>'
    return f'<div class="field">{lab}{ctl}</div>'

def R2(a, b): return f'<div class="row2">{a}{b}</div>'
def S(i, label): return f'<div class="stat-box"><b id="{i}">0</b><span>{label}</span></div>'
def CK(i, label, on=True): return f'<label class="check"><input id="{i}" type="checkbox"' + (' checked' if on else '') + f'> <span>{label}</span></label>'
PRE = 'style="display:block;margin-top:0;max-height:520px;overflow:auto;word-break:normal;overflow-wrap:anywhere"'
SCROLL = 'style="overflow-x:auto;max-height:420px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px;margin-bottom:16px"'

BASEJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function issues(id, list, okMsg, max){
    max = max || 30;
    var bad = list.filter(function(i){ return i[0] === 'bad'; }), warn = list.filter(function(i){ return i[0] === 'warn'; });
    var li = function(a){ var more = a.length > max ? '<li>and ' + (a.length - max) + ' more</li>' : '';
      return '<ul style="margin:6px 0 0 18px">' + a.slice(0, max).map(function(i){ return '<li>' + i[1] + '</li>'; }).join('') + more + '</ul>'; };
    if (bad.length) say(id, 'bad', '<strong>Fix ' + bad.length + ' issue' + (bad.length > 1 ? 's' : '') + (warn.length ? ', plus ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') : '') + '.</strong>' + li(bad.concat(warn)));
    else if (warn.length) say(id, 'warn', '<strong>Looks good, with ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') + '.</strong>' + li(warn));
    else say(id, 'ok', okMsg);
  }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
  function fmtN(n){ return Number(n).toLocaleString('en-IN'); }
  function download(name, text, type){
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: (type || 'text/plain') + ';charset=utf-8'}));
    a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
  }
  function csvCell(s){ s = String(s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  // Token estimate: about 4 characters or 0.75 words per token in English (OpenAI), more for other scripts
  var CJK = /[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\uf900-\ufaff]/g, NONLAT = /[\u0370-\u03ff\u0400-\u04ff\u0590-\u06ff\u0900-\u0dff\u0e00-\u0e7f]/g;
  function estTokens(s){
    s = String(s || ''); if (!s.trim()) return 0;
    var cjk = (s.match(CJK) || []).length, other = (s.match(NONLAT) || []).length;
    var rest = s.replace(CJK, ' ').replace(NONLAT, ' '), w = 0;
    (rest.match(/[A-Za-z\u00c0-\u024f']+|\d+|[^\sA-Za-z\d\u00c0-\u024f']/g) || []).forEach(function(t){
      if (/^\d/.test(t)) w += Math.ceil(t.length / 3);
      else if (/^[A-Za-z\u00c0-\u024f']/.test(t)) w += t.length <= 7 ? 1 : Math.ceil(t.length / 5);
      else w += 1;
    });
    var byChars = rest.replace(/\s+/g, ' ').trim().length / 4;
    return Math.max(1, Math.round((w + byChars) / 2 + cjk * 1.1 + other / 2.5));
  }
  function words(s){ return (String(s).match(/[A-Za-z0-9\u00c0-\u024f\u0900-\u0dff\u0400-\u04ff']+/g) || []).length; }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. LLMS.TXT GENERATOR ----------
    LT_LINKS = '''## Guides
What Is SEO | https://brandella.in/what-is-seo/ | Beginner guide to how search engines work
llms.txt Explained | https://brandella.in/llms-txt-explained/ | What the file is and who reads it
AI Search Optimization Checklist | https://brandella.in/ai-search-optimization-checklist-25/ | 25 checks for AI visibility

## Free Tools
SEO Tools | https://brandella.in/tools/seo-tools/ | SERP preview, keyword density, slugs and meta tags
Schema Generators | https://brandella.in/tools/schema-generators/ | JSON LD for products, articles and local businesses

## Optional
AI Tools for Marketers | https://brandella.in/ai-tools-for-marketers/'''
    LT_IMPORT = '''https://brandella.in/what-is-schema-markup/
https://brandella.in/robots-txt-complete-guide/
https://brandella.in/tools/ppc-calculators/roas-calculator/'''
    TOOLS.append(dict(
        slug='llms-txt-generator', short='LT', name='llms.txt Generator',
        card='Build a valid llms.txt file for your site in minutes, with sections, link notes and an Optional list.',
        title='llms.txt Generator: Create an llms.txt File Free',
        desc='Free llms.txt generator. Add your site summary and key pages, import URLs from a sitemap, and get a valid llms.txt file that follows the llmstxt.org format.',
        h1='llms.txt Generator',
        lead='Create a clean llms.txt file that points AI assistants and agents to your most useful pages. Paste links or a sitemap, add short notes, and copy a file that follows the official format.',
        tool='''<section class="tool" aria-label="llms.txt generator" id="ltForm">
    <div class="card" style="min-width:0">
      <h2>Your Site</h2>
      ''' + F('ltName', 'Site or Project Name', 'Brandella Journal', em='becomes the H1, required') + '''
      ''' + F('ltSum', 'Short Summary', 'Brandella Journal publishes practical guides on SEO, AI search, paid media and analytics, plus free browser based marketing tools.', em='one or two sentences', tag='textarea', extra=' style="min-height:80px"') + '''
      ''' + F('ltDet', 'Extra Details', 'All guides are written for marketers and small business owners. Tool pages run fully in the browser and never upload data.', em='optional, no headings', tag='textarea', extra=' style="min-height:70px"') + '''
      ''' + F('ltLinks', 'Sections and Links', LT_LINKS, em='## Section, then Title | URL | note', tag='textarea', mono=True, extra=' style="min-height:260px"') + '''
      ''' + F('ltImp', 'Import URLs', LT_IMPORT, em='paste a sitemap or a list of URLs', tag='textarea', mono=True, extra=' style="min-height:90px"') + '''
      <div class="actions" style="margin:0 0 6px"><button type="button" class="btn btn-sm" id="ltAdd">Add These URLs as Links</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Your llms.txt File</h2>
      <div class="stats">''' + S('ltSec', 'Sections') + S('ltCnt', 'Links') + S('ltTok', 'Tokens (est.)') + '''</div>
      <div class="kw-result" id="ltCheck"></div>
      <pre class="code-out" id="ltOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="ltCopy">Copy llms.txt</button><button class="btn" id="ltDl">Download File</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips">Upload the file to your site root so it opens at <code>yourdomain.com/llms.txt</code>.</div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function abs(u){ try { var x = new URL(u); return /^https?:$/.test(x.protocol) ? x : null; } catch(e){ return null; } }
  var ACR = /^(seo|ai|ppc|roas|cpa|cpc|cpm|ctr|utm|ga4|gtm|api|faq|html|css|js|json|xml|pdf|url|txt|llms|rag|aeo|geo|b2b|b2c|crm|cms|ux|ui|usa|uk|gst)$/i;
  function nice(s){ return s.replace(/[-_]+/g, ' ').replace(/\s+/g, ' ').trim().split(' ').map(function(w){ return ACR.test(w) ? (/^llms$/i.test(w) ? 'llms' : w.toUpperCase()) : w.charAt(0).toUpperCase() + w.slice(1); }).join(' '); }
  function titleOf(u){
    var p = u.pathname.replace(/\/+$/, '').split('/').pop();
    if (!p) return 'Home';
    try { p = decodeURIComponent(p); } catch(e){}
    return nice(p.replace(/\.(html?|php|aspx?|md)$/i, '')) || 'Home';
  }
  function parseLinks(txt){
    var secs = [], cur = null, bad = [], n = 0;
    txt.split(/\r?\n/).forEach(function(raw){
      n++; var line = raw.trim(); if (!line) return;
      var h = line.match(/^#{2,}\s*(.+)$/);
      if (h){ cur = {name: h[1].trim(), items: []}; secs.push(cur); return; }
      if (/^#\s/.test(line)){ bad.push(['bad', 'Line ' + n + ' is an H1. Only the site name may be an H1, so use ' + c('## ') + ' for sections.']); return; }
      var t, u, note = '';
      var md = line.match(/^[-*]\s*\[([^\]]+)\]\(([^)\s]+)\)\s*(?::\s*(.*))?$/);
      if (md){ t = md[1]; u = md[2]; note = md[3] || ''; }
      else {
        var p = line.split('|').map(function(x){ return x.trim(); });
        if (p.length === 1 && abs(p[0])){ u = p[0]; t = titleOf(abs(p[0])); }
        else { t = p[0]; u = p[1] || ''; note = p.slice(2).join(' | '); }
      }
      if (!cur){ cur = {name: 'Pages', items: []}; secs.push(cur); }
      cur.items.push({t: t, u: u, note: note, line: n});
    });
    return {secs: secs, bad: bad};
  }
  function build(){
    var name = v('ltName'), sum = v('ltSum').replace(/\s*\n\s*/g, ' '), det = v('ltDet');
    var P = parseLinks($('ltLinks').value), list = P.bad.slice(), seen = {}, total = 0;
    if (!name) list.push(['bad', 'Add a site or project name. The H1 is the only part the format requires.']);
    if (!sum) list.push(['warn', 'Add a short summary. It is the first thing an AI model reads about your site.']);
    var out = '# ' + (name || 'Your Site') + '\n\n';
    if (sum) out += '> ' + sum + '\n\n';
    if (det) out += det.replace(/^#+\s*/gm, '') + '\n\n';
    var secs = P.secs.filter(function(s){ return s.name.toLowerCase() !== 'optional'; }).concat(P.secs.filter(function(s){ return s.name.toLowerCase() === 'optional'; }));
    if (secs.length && P.secs[P.secs.length - 1].name.toLowerCase() !== 'optional' && P.secs.some(function(s){ return s.name.toLowerCase() === 'optional'; }))
      list.push(['warn', 'The Optional section was moved to the end, where AI tools expect it.']);
    secs.forEach(function(s){
      if (!s.items.length){ list.push(['warn', 'The section ' + c(s.name) + ' has no links, so it was left out.']); return; }
      out += '## ' + s.name + '\n\n';
      s.items.forEach(function(it){
        var u = abs(it.u);
        if (!it.u) list.push(['bad', 'Line ' + it.line + ' has no URL. Use ' + c('Title | https://... | note') + '.']);
        else if (!u) list.push(['bad', 'Line ' + it.line + ': ' + c(it.u) + ' is not a full URL. Start it with ' + c('https://') + '.']);
        else if (u.protocol === 'http:') list.push(['warn', 'Line ' + it.line + ' uses http. Use the https version if your site has one.']);
        if (u){ var k = u.href.replace(/\/$/, ''); if (seen[k]) list.push(['warn', 'Line ' + it.line + ' repeats a URL already listed on line ' + seen[k] + '.']); seen[k] = it.line; }
        if (!it.t) list.push(['bad', 'Line ' + it.line + ' has no title.']);
        if (!it.note && s.name.toLowerCase() !== 'optional') list.push(['warn', 'Line ' + it.line + ' (' + esc(it.t || it.u) + ') has no note. A few words help AI tools pick the right page.']);
        out += '- [' + (it.t || 'Untitled').replace(/[\[\]]/g, '') + '](' + it.u + ')' + (it.note ? ': ' + it.note : '') + '\n';
        total++;
      });
      out += '\n';
    });
    if (!total) list.push(['warn', 'Add at least one section with links to your key pages.']);
    if (total > 300) list.push(['warn', 'This file lists ' + total + ' links. Keep llms.txt short and focused on your best pages.']);
    out = out.replace(/\n+$/, '\n');
    $('ltOut').textContent = out;
    $('ltSec').textContent = secs.filter(function(s){ return s.items.length; }).length; $('ltCnt').textContent = total; $('ltTok').textContent = fmtN(estTokens(out));
    issues('ltCheck', list, '<strong>Valid llms.txt.</strong> It has a name, a summary and ' + total + ' linked pages in the llmstxt.org format.');
    return out;
  }
  $('ltAdd').addEventListener('click', function(){
    var urls = ($('ltImp').value.match(/https?:\/\/[^\s<>"']+/g) || []).map(abs).filter(Boolean), groups = {}, order = [];
    var have = $('ltLinks').value;
    urls.forEach(function(u){
      if (/\.(xml|jpg|jpeg|png|gif|webp|svg|css|js|pdf)$/i.test(u.pathname)) return;
      if (have.indexOf(u.href) > -1) return;
      var segs = u.pathname.split('/').filter(Boolean), g = segs.length > 1 ? nice(segs[0]) : 'Pages';
      if (!groups[g]){ groups[g] = []; order.push(g); }
      if (groups[g].indexOf(u.href) < 0) groups[g].push(u.href);
    });
    var add = order.map(function(g){ return '## ' + g + '\n' + groups[g].slice(0, 300).map(function(h){ return titleOf(new URL(h)) + ' | ' + h + ' | '; }).join('\n'); }).join('\n\n');
    if (add){ $('ltLinks').value = $('ltLinks').value.replace(/\s+$/, '') + '\n\n' + add; $('ltImp').value = ''; }
    build();
  });
  $('ltForm').addEventListener('input', build);
  $('ltCopy').addEventListener('click', function(){ copyText(build(), 'toast'); });
  $('ltDl').addEventListener('click', function(){ download('llms.txt', build()); });
  build();
''',
        content=f'''
    <h2>What Is an llms.txt File?</h2>
    <p>An llms.txt file is a short Markdown file at the root of your site that tells large language models what your site is about and which pages matter most. Think of it as a hand picked map for AI tools, written in plain text instead of XML.</p>
    <p>The format comes from the <a href="https://llmstxt.org/" {EXT}>llmstxt.org proposal</a>. Coding assistants, AI agents and some chat tools read it to find clean, useful pages without crawling your whole site. This generator builds the file in your browser and checks it against that format as you type.</p>

    <h2>How to Use the llms.txt Generator</h2>
    <ol>
      <li><strong>Enter your site name.</strong> It becomes the H1, the only part the format requires.</li>
      <li><strong>Write a one or two sentence summary.</strong> It is shown as a quote block right under the name.</li>
      <li><strong>Add sections and links.</strong> Start a section with <code>## Guides</code>, then add one page per line as <code>Title | URL | short note</code>.</li>
      <li><strong>Import URLs if you like.</strong> Paste your XML sitemap or a URL list and press the button. Titles are made from each URL.</li>
      <li><strong>Fix any warnings</strong>, then copy or download the file and upload it so it opens at <code>/llms.txt</code>.</li>
    </ol>

    <h2>The llms.txt Format at a Glance</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Part', 'How it is written', 'Required?')}
      <tbody>
        <tr><td>Site name</td><td><code># Name</code> on the first line</td><td>Yes</td></tr>
        <tr><td>Summary</td><td>A quote block, <code>&gt; One line summary</code></td><td>Recommended</td></tr>
        <tr><td>Details</td><td>Plain paragraphs or lists, no headings</td><td>No</td></tr>
        <tr><td>Sections</td><td><code>## Section name</code> followed by a list of links</td><td>No, but they are the point of the file</td></tr>
        <tr><td>Links</td><td><code>- [Title](https://url): note</code></td><td>Title and URL yes, note optional</td></tr>
        <tr><td>Optional</td><td>A section called <code>## Optional</code> for pages AI tools may skip</td><td>No</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for a Useful llms.txt</h2>
    <ul>
      <li><strong>Pick your best pages, not every page.</strong> The file is a shortlist. Your XML sitemap already lists everything.</li>
      <li><strong>Write notes that answer "why read this?"</strong> Five to twelve words is plenty.</li>
      <li><strong>Group by what people need,</strong> such as guides, pricing, docs and policies, rather than by site folder.</li>
      <li><strong>Be honest about the payoff.</strong> Google says its search and AI features do not use llms.txt, so it will neither help nor harm your Google rankings. See the <a href="https://developers.google.com/search/docs/fundamentals/ai-optimization-guide" {EXT}>Google AI optimization guide</a>. The file is mainly for other AI tools and agents.</li>
      <li><strong>Keep it current.</strong> Update it when you publish a cornerstone page or retire an old one.</li>
    </ul>

    <h2>Get Your Site Ready for AI Search</h2>
    <p>Learn what the file can and cannot do in <a href="{B}llms-txt-explained/">llms.txt explained</a>, then work through our <a href="{B}ai-search-optimization-checklist-25/">AI search optimization checklist</a> and the guide to <a href="{B}ai-friendly-website-chatgpt-gemini-claude-perplexity/">building an AI friendly website</a>. To see which AI bots already visit you, try the <a href="{T}ai-crawler-log-analyzer/">AI crawler log analyzer</a>.</p>
''',
        faqs=[
            ("Does llms.txt help my Google rankings?", "No. Google says Google Search and its AI features do not use llms.txt, so the file neither helps nor harms your rankings there. It is aimed at other AI tools, agents and coding assistants that choose to read it."),
            ("Where do I put the llms.txt file?", "Upload it to the root folder of your site so it opens at yourdomain.com/llms.txt. On WordPress you can upload it with your host's file manager or an SEO plugin that supports llms.txt."),
            ("Is llms.txt the same as robots.txt?", "No. robots.txt tells crawlers what they may not visit. llms.txt is a reading list of pages you recommend. Blocking or allowing AI crawlers is still done in robots.txt."),
            ("How many links should llms.txt have?", "There is no fixed limit, but a focused list of your 10 to 100 most useful pages works best. Put nice to have pages under the Optional section so AI tools with little room can skip them."),
        ],
        related=[("llms.txt Explained", "llms-txt-explained"), ("AI Search Optimization Checklist", "ai-search-optimization-checklist-25"),
                 ("Structuring HTML for AI Crawlability", "structuring-html-for-ai-crawlability"), ("What Is an XML Sitemap in the AI Search Era", "what-is-xml-sitemap-ai-search-era")],
    ))

    # ---------- 2. AI CRAWLER LOG ANALYZER ----------
    def L(ip, t, path, st, ref, ua):
        return f'{ip} - - [06/Nov/2026:{t} +0530] "GET {path} HTTP/1.1" {st} 18452 "{ref}" "{ua}"'
    G = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot'
    OS = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot'
    CU = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot'
    CB = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)'
    CS = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +https://www.anthropic.com)'
    PB = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)'
    GB = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    BY = 'Mozilla/5.0 (Linux; Android 5.0) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; Bytespider; spider-feedback@bytedance.com)'
    ME = 'meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)'
    HU = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    LOG = '\n'.join([
        L('20.171.207.14', '06:12:03', '/what-is-seo/', 200, '-', G),
        L('20.171.207.14', '06:12:09', '/llms-txt-explained/', 200, '-', G),
        L('20.171.207.15', '06:14:41', '/old-page/', 404, '-', G),
        L('66.249.66.1', '06:20:10', '/what-is-seo/', 200, '-', GB),
        L('52.230.152.8', '06:31:55', '/ai-search-optimization-checklist-25/', 200, '-', OS),
        L('52.230.152.8', '06:32:02', '/what-is-seo/', 200, '-', OS),
        L('23.98.142.180', '07:05:19', '/tools/ppc-calculators/roas-calculator/', 200, '-', CU),
        L('49.36.21.90', '07:05:48', '/tools/ppc-calculators/roas-calculator/', 200, 'https://chatgpt.com/', HU),
        L('3.84.15.122', '07:40:12', '/what-is-schema-markup/', 200, '-', CB),
        L('3.84.15.122', '07:40:15', '/robots-txt-complete-guide/', 200, '-', CB),
        L('3.84.15.123', '07:40:19', '/wp-login.php', 403, '-', CB),
        L('34.162.10.4', '08:02:33', '/llms-txt-explained/', 200, '-', CS),
        L('44.221.181.252', '08:15:27', '/what-is-seo/', 200, '-', PB),
        L('103.21.58.4', '08:16:02', '/what-is-seo/', 200, 'https://www.perplexity.ai/', HU),
        L('110.249.201.7', '08:44:51', '/tag/seo/page/14/', 200, '-', BY),
        L('110.249.201.8', '08:44:52', '/tag/seo/page/15/', 200, '-', BY),
        L('110.249.201.8', '08:44:53', '/tag/seo/page/16/', 500, '-', BY),
        L('57.141.0.12', '09:03:40', '/what-is-schema-markup/', 200, '-', ME),
        L('157.46.88.10', '09:10:05', '/llms-txt-explained/', 200, 'https://gemini.google.com/', HU),
        L('117.99.4.31', '09:22:44', '/', 200, 'https://www.google.com/', HU),
        L('20.171.207.16', '09:30:12', '/robots.txt', 200, '-', G),
    ])
    TOOLS.append(dict(
        slug='ai-crawler-log-analyzer', short='AC', name='AI Crawler Log Analyzer',
        card='Paste server access logs and see which AI bots like GPTBot and ClaudeBot crawl your site, plus visits from ChatGPT.',
        title='AI Crawler Log Analyzer: Find GPTBot and ClaudeBot',
        desc='Free AI crawler log analyzer. Paste your access log to see GPTBot, ClaudeBot, PerplexityBot and other AI bot hits, pages, errors and AI referral visits.',
        h1='AI Crawler Log Analyzer',
        lead='Find out which AI bots really visit your site. Paste lines from your server access log and see every AI crawler by company and purpose, the pages they read, the errors they hit, and the visits you get from ChatGPT, Perplexity and Gemini.',
        tool='''<section class="tool" aria-label="AI crawler log analyzer" id="acForm" style="grid-template-columns:1fr">
    <div class="card" style="min-width:0">
      <h2>Access Log</h2>
      ''' + F('acLog', 'Paste access log lines', LOG, em='Apache, Nginx, LiteSpeed or similar', tag='textarea', mono=True, extra=' style="min-height:220px;white-space:pre;overflow-wrap:normal"') + '''
      <div class="row2">''' + CK('acSE', 'Show Googlebot and Bingbot for comparison') + CK('acFile', 'Ignore image, CSS and JS requests', False) + '''</div>
    </div>
    <div class="card" style="min-width:0">
      <h2>AI Crawler Report</h2>
      <div class="stats">''' + S('acLines', 'Lines Read') + S('acHits', 'AI Bot Hits') + S('acBots', 'AI Bots Seen') + S('acRef', 'AI Referral Visits') + '''</div>
      <div class="kw-result" id="acSum"></div>
      <h3 style="font-size:16px;margin:4px 0 10px">Bots by Company and Purpose</h3>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Bot</th><th>Company</th><th>Purpose</th><th class="num">Hits</th><th class="num">Pages</th><th class="num">Errors</th><th>Last seen</th></tr></thead><tbody id="acBody"></tbody></table></div>
      <div class="row2">
        <div style="min-width:0"><h3 style="font-size:16px;margin:4px 0 10px">Pages AI Bots Read Most</h3>
        <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Page</th><th class="num">Hits</th><th>Bots</th></tr></thead><tbody id="acPages"></tbody></table></div></div>
        <div style="min-width:0"><h3 style="font-size:16px;margin:4px 0 10px">Visits From AI Assistants</h3>
        <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Source</th><th class="num">Visits</th><th>Top landing page</th></tr></thead><tbody id="acRefs"></tbody></table></div></div>
      </div>
      <div class="actions"><button class="btn dark" id="acCsv">Download Bot Report CSV</button></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var BOTS = [
    ['GPTBot', /gptbot/i, 'OpenAI', 'Training'], ['OAI-SearchBot', /oai-searchbot/i, 'OpenAI', 'Search'],
    ['ChatGPT-User', /chatgpt-user/i, 'OpenAI', 'User fetch'], ['OAI-AdsBot', /oai-adsbot/i, 'OpenAI', 'Ads check'],
    ['ClaudeBot', /claudebot/i, 'Anthropic', 'Training'], ['Claude-SearchBot', /claude-searchbot/i, 'Anthropic', 'Search'],
    ['Claude-User', /claude-user/i, 'Anthropic', 'User fetch'], ['anthropic-ai', /anthropic-ai/i, 'Anthropic', 'Training (old name)'],
    ['PerplexityBot', /perplexitybot/i, 'Perplexity', 'Search'], ['Perplexity-User', /perplexity-user/i, 'Perplexity', 'User fetch'],
    ['Meta-ExternalAgent', /meta-externalagent/i, 'Meta', 'Training'], ['Meta-WebIndexer', /meta-webindexer/i, 'Meta', 'Search'],
    ['Meta-ExternalFetcher', /meta-externalfetcher/i, 'Meta', 'User fetch'],
    ['Amazonbot', /amazonbot/i, 'Amazon', 'Training and products'], ['Amzn-SearchBot', /amzn-searchbot/i, 'Amazon', 'Search'],
    ['Amzn-User', /amzn-user/i, 'Amazon', 'User fetch'], ['Applebot', /applebot/i, 'Apple', 'Search and AI'],
    ['Bytespider', /bytespider/i, 'ByteDance', 'Training'], ['CCBot', /ccbot/i, 'Common Crawl', 'Open dataset'],
    ['DuckAssistBot', /duckassistbot/i, 'DuckDuckGo', 'User fetch'], ['MistralAI-User', /mistralai-user/i, 'Mistral', 'User fetch'],
    ['Googlebot', /googlebot/i, 'Google', 'Search engine', 1], ['Bingbot', /bingbot/i, 'Microsoft', 'Search engine', 1]
  ];
  var REFS = [['ChatGPT', /chatgpt\.com|chat\.openai\.com|utm_source=chatgpt/i], ['Perplexity', /perplexity\.ai/i], ['Gemini', /gemini\.google\.com|bard\.google\.com/i],
    ['Copilot', /copilot\.microsoft\.com/i], ['Claude', /claude\.ai/i], ['DeepSeek', /chat\.deepseek\.com/i], ['Meta AI', /meta\.ai/i]];
  var LINE = /^(\S+) \S+ \S+ \[([^\]]+)\] "(?:[A-Z]+) (\S+)[^"]*" (\d{3}) \S+(?: "([^"]*)" "([^"]*)")?/;
  var report = [];
  function run(){
    var se = $('acSE').checked, skipFiles = $('acFile').checked;
    var lines = $('acLog').value.split(/\r?\n/).filter(function(s){ return s.trim(); });
    var bots = {}, pages = {}, refs = {}, hits = 0, refN = 0;
    lines.forEach(function(ln){
      var m = ln.match(LINE), path, st, ref, ua, when;
      if (m){ when = m[2]; path = m[3]; st = +m[4]; ref = m[5] || ''; ua = m[6] || ln; }
      else {
        path = (ln.match(/"(?:GET|POST|HEAD|PUT) (\S+)/) || ln.match(/"(?:path|uri|url|request_uri|request)"\s*:\s*"(?:[A-Z]+ )?([^" ]+)/i) || ln.match(/\s(\/\S*)/) || [, '?'])[1];
        st = +((ln.match(/"?(?:status|status_code|sc-status)"?\s*[:=]\s*"?([1-5]\d\d)\b/i) || ln.match(/["\s]([1-5]\d\d)\s/) || [, 0])[1]); ref = ln; ua = ln; when = (ln.match(/\[([^\]]+)\]/) || ln.match(/\d{4}-\d\d-\d\dT[\d:]+/) || [''])[0].replace(/[\[\]]/g, '');
      }
      if (skipFiles && /\.(png|jpe?g|gif|webp|svg|ico|css|js|woff2?)(\?|$)/i.test(path)) return;
      var b = null;
      for (var i = 0; i < BOTS.length; i++) if (BOTS[i][1].test(ua)){ b = BOTS[i]; break; }
      if (b){
        if (b[4] && !se) return;
        var k = b[0], o = bots[k] || (bots[k] = {b: b, hits: 0, pages: {}, err: 0, last: ''});
        o.hits++; o.pages[path] = 1; if (st >= 400) o.err++; o.last = when || o.last;
        if (!b[4]){ hits++; var p = pages[path] || (pages[path] = {n: 0, bots: {}}); p.n++; p.bots[k] = 1; }
        return;
      }
      for (var j = 0; j < REFS.length; j++){
        var src = m ? ref + ' ' + path : ln;
        if (REFS[j][1].test(src)){ var r = refs[REFS[j][0]] || (refs[REFS[j][0]] = {n: 0, land: {}}); r.n++; r.land[path] = (r.land[path] || 0) + 1; refN++; break; }
      }
    });
    var list = Object.keys(bots).map(function(k){ return bots[k]; }).sort(function(a, b){ return (a.b[4] || 0) - (b.b[4] || 0) || b.hits - a.hits; });
    report = list;
    $('acBody').innerHTML = list.map(function(o){
      var np = Object.keys(o.pages).length;
      return '<tr><td><code>' + esc(o.b[0]) + '</code></td><td>' + o.b[2] + '</td><td>' + o.b[3] + '</td><td class="num">' + fmtN(o.hits) + '</td><td class="num">' + np + '</td><td class="num"' + (o.err ? ' style="color:#d1351f;font-weight:700"' : '') + '>' + o.err + '</td><td>' + esc(o.last || '') + '</td></tr>';
    }).join('') || '<tr><td colspan="7" class="empty">No AI crawlers found in these lines.</td></tr>';
    var pl = Object.keys(pages).sort(function(a, b){ return pages[b].n - pages[a].n; }).slice(0, 25);
    $('acPages').innerHTML = pl.map(function(p){ return '<tr><td style="word-break:break-all">' + esc(p) + '</td><td class="num">' + pages[p].n + '</td><td>' + Object.keys(pages[p].bots).join(', ') + '</td></tr>'; }).join('') || '<tr><td colspan="3" class="empty">No pages yet.</td></tr>';
    var rl = Object.keys(refs).sort(function(a, b){ return refs[b].n - refs[a].n; });
    $('acRefs').innerHTML = rl.map(function(r){ var land = Object.keys(refs[r].land).sort(function(a, b){ return refs[r].land[b] - refs[r].land[a]; })[0];
      return '<tr><td>' + r + '</td><td class="num">' + refs[r].n + '</td><td style="word-break:break-all">' + esc(land) + '</td></tr>'; }).join('') || '<tr><td colspan="3" class="empty">No visits from AI assistants found.</td></tr>';
    var ai = list.filter(function(o){ return !o.b[4]; });
    $('acLines').textContent = fmtN(lines.length); $('acHits').textContent = fmtN(hits); $('acBots').textContent = ai.length; $('acRef').textContent = fmtN(refN);
    if (!lines.length) return say('acSum', 'warn', 'Paste some lines from your access log to start.');
    if (!ai.length) return say('acSum', 'warn', '<strong>No AI crawlers found.</strong> Check that the lines include the user agent, the last quoted part of each line in the usual log format.');
    var pur = {}; ai.forEach(function(o){ var t = /Training|dataset/.test(o.b[3]) ? 'training' : /Search/.test(o.b[3]) ? 'AI search' : 'live user requests'; pur[t] = (pur[t] || 0) + o.hits; });
    var err = ai.reduce(function(s, o){ return s + o.err; }, 0);
    var parts = Object.keys(pur).map(function(t){ return fmtN(pur[t]) + ' for ' + t; }).join(', ');
    say('acSum', err ? 'warn' : 'ok', '<strong>' + ai.length + ' AI bot' + (ai.length > 1 ? 's' : '') + ' made ' + fmtN(hits) + ' request' + (hits > 1 ? 's' : '') + '</strong>: ' + parts + '.' +
      (err ? ' They hit <strong>' + err + ' error' + (err > 1 ? 's' : '') + '</strong> (status 400 or higher). Fix or redirect those URLs so AI tools see your real pages.' : ' No errors found.') +
      ' User agents can be faked, so confirm important bots against the IP lists each company publishes.');
  }
  $('acForm').addEventListener('input', run); $('acForm').addEventListener('change', run);
  $('acCsv').addEventListener('click', function(){
    var rows = [['Bot', 'Company', 'Purpose', 'Hits', 'Pages', 'Errors', 'Last seen']].concat(report.map(function(o){ return [o.b[0], o.b[2], o.b[3], o.hits, Object.keys(o.pages).length, o.err, o.last]; }));
    download('ai-crawler-report.csv', rows.map(function(r){ return r.map(csvCell).join(','); }).join('\n'), 'text/csv');
  });
  run();
''',
        content=f'''
    <h2>What Does the AI Crawler Log Analyzer Do?</h2>
    <p>Analytics tools like GA4 cannot see AI crawlers, because bots do not run JavaScript. The only place their visits show up is your server access log. This tool reads those log lines and pulls out every known AI bot, from OpenAI, Anthropic, Perplexity, Meta, Amazon, Apple, ByteDance and others.</p>
    <p>For each bot you see who runs it, why it visits, how many requests it made, how many different pages it read and how many errors it hit. It also counts real people who arrived from ChatGPT, Perplexity, Gemini, Copilot and Claude, so you can compare bot interest with actual clicks. Your log never leaves your browser.</p>

    <h2>How to Use It</h2>
    <ol>
      <li><strong>Download your access log.</strong> In cPanel or hPanel look for Raw Access or Access Logs. On a VPS it is usually in <code>/var/log/nginx/</code> or <code>/var/log/apache2/</code>.</li>
      <li><strong>Paste the lines</strong> into the box. A day or a week of traffic works well. The common combined log format is read line by line.</li>
      <li><strong>Read the bot table</strong> to see which companies crawl you and for what purpose.</li>
      <li><strong>Check the errors column.</strong> Bots hitting 404 or 500 pages waste their visit on content that does not exist.</li>
      <li><strong>Download the CSV</strong> to keep a monthly record and spot trends.</li>
    </ol>

    <h2>AI Crawler Types Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Purpose', 'Example bots', 'What it means for you')}
      <tbody>
        <tr><td>Training</td><td><code>GPTBot</code>, <code>ClaudeBot</code>, <code>Meta-ExternalAgent</code></td><td>Collects pages that may be used to train AI models. Blocking it does not remove you from AI search.</td></tr>
        <tr><td>AI search</td><td><code>OAI-SearchBot</code>, <code>Claude-SearchBot</code>, <code>PerplexityBot</code></td><td>Indexes pages so they can be shown and cited in AI search answers. Blocking it can cost you visibility.</td></tr>
        <tr><td>User fetch</td><td><code>ChatGPT-User</code>, <code>Claude-User</code>, <code>Perplexity-User</code></td><td>Opens a page because a person asked about it right now. Some of these may not follow robots.txt.</td></tr>
        <tr><td>Search engine</td><td><code>Googlebot</code>, <code>Bingbot</code></td><td>Regular search crawling, which also feeds Google AI Overviews and Bing Copilot answers.</td></tr>
      </tbody>
    </table></div>
    <p>These purposes come from each company's own documentation, such as <a href="https://developers.openai.com/api/docs/bots" {EXT}>OpenAI's crawler overview</a>. Note that <code>Google-Extended</code> and <code>Applebot-Extended</code> never appear in logs. They are robots.txt switches, not separate crawlers.</p>

    <h2>Tips for Reading Your Results</h2>
    <ul>
      <li><strong>Search bots matter most for visibility.</strong> If you want to be cited in ChatGPT or Perplexity answers, make sure their search bots can reach your key pages.</li>
      <li><strong>Watch for crawl waste.</strong> Bots stuck on tag archives, pagination or login pages are a sign to tidy internal links or block those paths.</li>
      <li><strong>Verify big spenders.</strong> Anyone can fake a user agent. Check heavy hitters against the official IP lists before you trust or block them.</li>
      <li><strong>Compare bots with clicks.</strong> Many bot hits but few AI referral visits usually means your pages are read but rarely cited.</li>
    </ul>

    <h2>Make the Most of AI Crawlers</h2>
    <p>Learn how each assistant picks sources in <a href="{B}how-chatgpt-chooses-websites-for-answers/">how ChatGPT chooses websites</a> and <a href="{B}how-perplexity-ai-finds-ranks-sources/">how Perplexity finds sources</a>. For deeper log work, see <a href="{B}python-log-file-analysis-googlebot-crawl-behavior/">log file analysis with Python</a>. To decide which bots to allow, build your rules with the <a href="{TS}robots-txt-generator/">robots.txt generator</a>.</p>
''',
        faqs=[
            ("Why can't I see AI crawlers in Google Analytics?", "AI crawlers request your HTML but do not run JavaScript, so tracking tags like GA4 never fire. Server access logs record every request, which is why log analysis is the reliable way to measure them."),
            ("Should I block GPTBot and ClaudeBot?", "It depends on your goals. GPTBot and ClaudeBot collect content for model training. Blocking them does not stop OAI SearchBot or Claude SearchBot, which power AI search results. Many publishers block training bots and allow search bots."),
            ("Which log formats does the tool read?", "It reads the combined log format used by Apache, Nginx, LiteSpeed and most hosts. For other formats it still finds the bot name, path and status code in each line, as long as the user agent is included."),
            ("Is it safe to paste my server logs here?", "Yes. The analysis runs entirely in your browser and nothing is uploaded. Logs can include visitor IP addresses, so avoid sharing the raw file elsewhere."),
        ],
        related=[("How ChatGPT Chooses Websites for Answers", "how-chatgpt-chooses-websites-for-answers"), ("Python Log File Analysis for Googlebot", "python-log-file-analysis-googlebot-crawl-behavior"),
                 ("Robots.txt Complete Guide", "robots-txt-complete-guide"), ("Google AI Search Opt Out", "google-ai-search-opt-out")],
    ))

    # ---------- 3. AI TOKEN COUNTER ----------
    TK_TEXT = '''Large language models do not read words. They read tokens, small pieces of text that are often a whole short word, part of a longer word, a number or a punctuation mark.

Every AI model has a context window, the total number of tokens it can hold at once. Your prompt, any documents you paste, the chat history and the answer all share that space. When you go over the limit, the oldest text is cut or the request fails.

Tokens also decide the bill. API providers charge per million input tokens and per million output tokens, and output usually costs more. Knowing your token count before you send a long report or a batch of product descriptions helps you plan costs and avoid surprises.

For retrieval augmented generation, long documents are split into chunks of a few hundred tokens each, with a little overlap so no idea is cut in half. Each chunk is stored and the best matches are given to the model when a question comes in.'''
    TOOLS.append(dict(
        slug='ai-token-counter', short='TK', name='AI Token Counter',
        card='Estimate tokens for ChatGPT, Claude and Gemini prompts, check context window fit, cost and split text into chunks.',
        title='AI Token Counter: Count Tokens for ChatGPT and Claude',
        desc='Free AI token counter. Estimate tokens, words and characters, check if text fits a context window, work out API cost and split long text into RAG chunks.',
        h1='AI Token Counter',
        lead='Paste a prompt or document to estimate its tokens, see whether it fits a model\'s context window, work out the API cost and split long text into chunks for RAG or batch jobs.',
        tool='''<section class="tool" aria-label="AI token counter" id="tkForm">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('tkText', 'Paste a prompt, article or document', TK_TEXT, tag='textarea', extra=' style="min-height:300px"') + '''
      ''' + R2(F('tkWin', 'Context Window', '128000', tag='select', opts=[('8000', '8K tokens'), ('32000', '32K tokens'), ('128000', '128K tokens'), ('200000', '200K tokens'), ('400000', '400K tokens'), ('1000000', '1M tokens')]),
               F('tkOut', 'Expected Answer Length', '800', em='tokens', typ='number', extra=' min="0" step="100"')) + '''
      ''' + R2(F('tkPin', 'Input Price', '2.50', em='per 1M tokens', typ='number', extra=' min="0" step="0.05"'),
               F('tkPout', 'Output Price', '10.00', em='per 1M tokens', typ='number', extra=' min="0" step="0.05"')) + '''
      ''' + R2(F('tkCur', 'Currency', '$', tag='select', opts=[('$', 'US dollar ($)'), ('\u20b9', 'Indian rupee (\u20b9)'), ('\u20ac', 'Euro (\u20ac)'), ('\u00a3', 'Pound (\u00a3)')]),
               F('tkRuns', 'Number of Requests', '1', em='for batch jobs', typ='number', extra=' min="1" step="1"')) + '''
      <div class="tips">Prices are examples. Enter the current per million token prices from your AI provider's pricing page.</div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Token Count</h2>
      <div class="stats">''' + S('tkTok', 'Tokens (est.)') + S('tkWords', 'Words') + S('tkChars', 'Characters') + S('tkCost', 'Estimated Cost') + '''</div>
      <div class="kw-result" id="tkFit"></div>
      <div style="height:12px;background:#eee;border-radius:8px;overflow:hidden;margin:-6px 0 16px"><div id="tkBar" style="height:100%;width:0;background:#4fa61d"></div></div>
      <h3 style="font-size:16px;margin:4px 0 10px">Split Into Chunks</h3>
      ''' + R2(F('tkSize', 'Chunk Size', '120', em='tokens', typ='number', extra=' min="20" step="10"'), F('tkLap', 'Overlap', '20', em='tokens', typ='number', extra=' min="0" step="5"')) + '''
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th class="num">#</th><th class="num">Tokens</th><th>Starts with</th></tr></thead><tbody id="tkChunks"></tbody></table></div>
      <div class="actions"><button class="btn dark" id="tkJson">Download Chunks as JSON</button><button class="btn" id="tkTxt">Download as Text</button></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var chunks = [];
  function num(id, d){ var n = parseFloat($(id).value); return isFinite(n) && n >= 0 ? n : d; }
  function money(n, cur){ return cur + (n < 0.01 && n > 0 ? n.toFixed(4) : n < 10 ? n.toFixed(3) : n.toFixed(2)); }
  function units(text){
    var out = [];
    text.split(/\n\s*\n/).map(function(p){ return p.trim(); }).filter(Boolean).forEach(function(p){
      var s = p.match(/[^.!?\n]+(?:[.!?]+["')\]]*|\n|$)\s*/g) || [p];
      s.forEach(function(x, i){ x = x.trim(); if (x) out.push({t: x, end: i === s.length - 1, n: estTokens(x)}); });
    });
    return out;
  }
  function chunk(text, size, lap){
    var u = units(text), res = [], cur = [], tot = 0;
    function flush(){
      if (!cur.length) return;
      res.push(cur.map(function(x, i){ return x.t + (i < cur.length - 1 ? (x.end ? '\n\n' : ' ') : ''); }).join(''));
      var keep = [], k = 0;
      for (var i = cur.length - 1; i > 0 && lap > 0; i--){ if (k + cur[i].n > lap) break; keep.unshift(cur[i]); k += cur[i].n; }
      cur = keep; tot = k;
    }
    u.forEach(function(x){
      if (tot + x.n > size && cur.length && tot > (lap ? lap : 0)) flush();
      cur.push(x); tot += x.n;
    });
    if (cur.length && (!res.length || tot > 0)){
      var last = cur.map(function(x){ return x.t; }).join(' ');
      if (!res.length || res[res.length - 1].indexOf(last) < 0) res.push(cur.map(function(x, i){ return x.t + (i < cur.length - 1 ? (x.end ? '\n\n' : ' ') : ''); }).join(''));
    }
    return res;
  }
  function run(){
    var text = $('tkText').value, tok = estTokens(text), win = +$('tkWin').value, outT = num('tkOut', 0), runs = Math.max(1, Math.round(num('tkRuns', 1)));
    var cur = $('tkCur').value, cost = (tok * num('tkPin', 0) + outT * num('tkPout', 0)) / 1e6 * runs;
    $('tkTok').textContent = fmtN(tok); $('tkWords').textContent = fmtN(words(text)); $('tkChars').textContent = fmtN(text.length);
    $('tkCost').textContent = money(cost, cur);
    var need = tok + outT, pct = Math.min(100, need / win * 100);
    $('tkBar').style.width = pct.toFixed(1) + '%'; $('tkBar').style.background = pct > 100 || need > win ? '#d1351f' : pct > 80 ? '#c47a00' : '#4fa61d';
    var lo = Math.round(tok * 0.85), hi = Math.round(tok * 1.15), wl = $('tkWin').selectedOptions[0].textContent;
    var base = 'About <strong>' + fmtN(lo) + ' to ' + fmtN(hi) + ' tokens</strong> depending on the model. ';
    if (!tok) say('tkFit', '', 'Paste some text to count its tokens.');
    else if (need > win) say('tkFit', 'bad', base + 'With a ' + fmtN(outT) + ' token answer this needs ' + fmtN(need) + ' tokens, more than a context window of ' + wl + '. Split it into chunks or use a model with a larger window.');
    else say('tkFit', pct > 80 ? 'warn' : 'ok', base + 'Prompt plus answer uses <strong>' + pct.toFixed(pct < 1 ? 2 : 1) + '%</strong> of a context window of ' + wl + (pct > 80 ? ', which leaves little room for chat history.' : '.') +
      (runs > 1 ? ' ' + fmtN(runs) + ' requests cost about ' + money(cost, cur) + ' in total.' : ''));
    var size = Math.max(20, num('tkSize', 500)), lap = Math.min(num('tkLap', 0), Math.floor(size / 2));
    chunks = tok ? chunk(text, size, lap) : [];
    $('tkChunks').innerHTML = chunks.map(function(ch, i){ var p = ch.replace(/\s+/g, ' ');
      return '<tr><td class="num">' + (i + 1) + '</td><td class="num">' + fmtN(estTokens(ch)) + '</td><td>' + esc(p.slice(0, 90)) + (p.length > 90 ? '...' : '') + '</td></tr>'; }).join('') || '<tr><td colspan="3" class="empty">No text to split.</td></tr>';
  }
  $('tkForm').addEventListener('input', run); $('tkForm').addEventListener('change', run);
  $('tkJson').addEventListener('click', function(){ download('chunks.json', JSON.stringify(chunks.map(function(t, i){ return {id: i + 1, tokens_est: estTokens(t), text: t}; }), null, 2), 'application/json'); });
  $('tkTxt').addEventListener('click', function(){ download('chunks.txt', chunks.map(function(t, i){ return '=== Chunk ' + (i + 1) + ' ===\n' + t; }).join('\n\n')); });
  run();
''',
        content=f'''
    <h2>What Is an AI Token Counter?</h2>
    <p>An AI token counter tells you how many tokens a piece of text uses. Tokens are the units that models like ChatGPT, Claude and Gemini read and write. A token is often a short word, part of a longer word, a number group or a punctuation mark.</p>
    <p>Token counts decide two things that matter every day: whether your text fits in the model's context window, and how much an API request costs. This tool gives you a fast estimate, the share of a context window you will use, the cost of one request or a whole batch, and a chunk splitter for long documents. Your text stays in your browser.</p>

    <h2>How to Use the Token Counter</h2>
    <ol>
      <li><strong>Paste your text,</strong> such as a prompt, a report or a set of product descriptions.</li>
      <li><strong>Pick a context window size</strong> and how long you expect the answer to be.</li>
      <li><strong>Enter your model's prices</strong> per million input and output tokens, and the number of requests for batch jobs.</li>
      <li><strong>Read the result.</strong> The bar turns orange above 80% of the window and red when the text will not fit.</li>
      <li><strong>Split long text</strong> by setting a chunk size and overlap, then download the chunks as JSON or plain text.</li>
    </ol>

    <h2>Tokens, Words and Characters</h2>
    <p>OpenAI's <a href="https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them" {EXT}>guide to tokens</a> gives these rules of thumb for English text:</p>
    <div style="overflow-x:auto"><table class="lim">
      {th('Text', 'Roughly')}
      <tbody>
        <tr><td>1 token</td><td>4 characters, or three quarters of a word</td></tr>
        <tr><td>100 tokens</td><td>75 words</td></tr>
        <tr><td>1 or 2 sentences</td><td>30 tokens</td></tr>
        <tr><td>1 paragraph</td><td>100 tokens</td></tr>
        <tr><td>1,500 words</td><td>about 2,000 tokens</td></tr>
      </tbody>
    </table></div>
    <p>Hindi, Tamil, Chinese, Japanese and many other languages usually need more tokens for the same meaning, and code with lots of symbols does too. Each model family uses its own tokenizer, so the same text can differ by 10% or more between providers. That is why this tool shows a range, not one exact figure.</p>

    <h2>Tips to Use Fewer Tokens</h2>
    <ul>
      <li><strong>Convert web pages to Markdown</strong> before pasting them. Raw HTML can use several times more tokens than the same text.</li>
      <li><strong>Cut repeated instructions.</strong> Say each rule once, clearly.</li>
      <li><strong>Set an answer length.</strong> Output tokens usually cost more than input tokens.</li>
      <li><strong>Chunk long documents</strong> into 300 to 800 token pieces with 10 to 15% overlap for search and RAG systems.</li>
      <li><strong>Check the real count</strong> in your provider's usage report for billing, since this tool gives an estimate.</li>
    </ul>

    <h2>Learn More About Context and Tokens</h2>
    <p>See how models hold information in <a href="{B}ai-memory-vs-context-window-difference/">AI memory vs context window</a>, learn how chunks are used in <a href="{B}retrieval-augmented-generation-rag-explained/">RAG explained</a>, and get the basics in <a href="{B}large-language-models-explained/">large language models explained</a>. To shrink a web page before you paste it, use the <a href="{T}html-to-markdown-converter/">HTML to Markdown converter</a>.</p>
''',
        faqs=[
            ("How accurate is this token count?", "It is an estimate based on how modern tokenizers split English text, and it is usually within about 10 to 15% of the real count. Each provider uses its own tokenizer, so for exact billing check the usage numbers in your provider's dashboard."),
            ("Do ChatGPT, Claude and Gemini count tokens the same way?", "No. Each model family has its own tokenizer, so the same text gives slightly different counts. The rules of thumb, such as about 4 characters per token in English, hold for all of them."),
            ("Do spaces and punctuation count as tokens?", "Yes. Punctuation marks are often their own token, and a space is usually joined to the word after it. Long runs of spaces, line breaks or symbols in code can add up quickly."),
            ("What chunk size should I use for RAG?", "Many teams start with 300 to 800 tokens per chunk and an overlap of 10 to 15%. Smaller chunks give more precise matches, larger chunks keep more context. Test a few sizes with real questions."),
        ],
        related=[("AI Memory vs Context Window", "ai-memory-vs-context-window-difference"), ("Retrieval Augmented Generation Explained", "retrieval-augmented-generation-rag-explained"),
                 ("Large Language Models Explained", "large-language-models-explained"), ("Build an AI Chatbot With the OpenAI API", "build-ai-chatbot-openai-api")],
    ))

    # ---------- 4. AI TEXT CLEANER ----------
    TC_TEXT = ('Certainly! Here\u2019s a polished version of your product description:\n\n'
               '## Why Choose Our Cotton Kurtas\n\n'
               'Our kurtas are made from **100% organic cotton**\u00a0\u2014 soft, breathable and perfect for Indian summers.\u200b '
               'Each piece is hand finished by artisans in Jaipur, so no two are exactly alike\u2026\n\n'
               '- **Fabric:** pure cotton, pre washed\n'
               '- **Fit:** relaxed, true to size\n'
               '- **Care:** machine wash cold\u202fonly\n\n'
               'Prices start at \u20b9899 \u2013 \u20b91,499, with free delivery on orders above \u20b9999.\u200b\u200b '
               'It\u2019s the \u201ceveryday luxury\u201d your wardrobe deserves\u2014without the luxury price tag.\n\n'
               'I hope this helps! Let me know if you\u2019d like a shorter version for Instagram.')
    TOOLS.append(dict(
        slug='ai-text-cleaner', short='TC', name='AI Text Cleaner',
        card='Clean ChatGPT and AI written text: remove hidden characters, Markdown symbols, long dashes and chatbot filler.',
        title='AI Text Cleaner: Remove Hidden Characters and Markdown',
        desc='Free AI text cleaner. Remove invisible characters, odd spaces, Markdown stars and hashes, long dashes, smart quotes and chatbot filler from ChatGPT text.',
        h1='AI Text Cleaner',
        lead='Paste text from ChatGPT, Claude, Gemini or any AI tool and get clean, plain text you can publish. It removes hidden characters, odd spaces, Markdown symbols and chatbot filler, and shows exactly what changed.',
        tool='''<section class="tool" aria-label="AI text cleaner" id="tcForm">
    <div class="card" style="min-width:0">
      <h2>AI Written Text</h2>
      ''' + F('tcIn', 'Paste text to clean', TC_TEXT, tag='textarea', extra=' style="min-height:290px"') + '''
      <h3 style="font-size:16px;margin:4px 0 10px">What to Clean</h3>
      ''' + CK('tcInv', 'Remove invisible characters (zero width, BOM, soft hyphen, direction marks)') + '''
      ''' + CK('tcSp', 'Turn special spaces into normal spaces') + '''
      ''' + CK('tcMd', 'Remove Markdown symbols (##, **bold**, links, list markers)') + '''
      ''' + CK('tcBot', 'Remove chatbot openers and sign offs ("Certainly!", "I hope this helps")') + '''
      ''' + CK('tcQ', 'Straighten curly quotes and apostrophes') + '''
      ''' + CK('tcEl', 'Replace the ellipsis character with three dots') + '''
      ''' + CK('tcWs', 'Tidy spaces and blank lines') + '''
      ''' + F('tcDash', 'Long Dashes', 'comma', tag='select', opts=[('comma', 'Replace with a comma'), ('hyphen', 'Replace with a spaced hyphen'), ('keep', 'Keep them')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Clean Text</h2>
      <div class="stats">''' + S('tcHid', 'Hidden Characters') + S('tcDa', 'Long Dashes') + S('tcMk', 'Markdown Marks') + S('tcTot', 'Total Fixes') + '''</div>
      ''' + F('tcOut', 'Cleaned text', '', tag='textarea', extra=' readonly style="min-height:290px"') + '''
      <div class="actions" style="margin:-6px 0 16px"><button class="btn dark" id="tcCopy">Copy Clean Text</button><span class="toast" id="toast">Copied!</span></div>
      <div class="kw-result" id="tcRep"></div>
      <h3 style="font-size:16px;margin:4px 0 10px">Hidden Characters Found</h3>
      <pre class="code-out" id="tcMap" ''' + PRE.replace('520px', '220px') + '''></pre>
    </div>
  </section>''',
        js=BASEJS + r'''
  var INV = /[\u200b\u200c\u200d\u2060\u2061\u2062\u2063\u2064\ufeff\u00ad\u200e\u200f\u061c\u202a-\u202e\u2066-\u2069\u180e\u034f]|\uDB40[\uDC00-\uDC7F]/g;
  var SPC = /[\u00a0\u202f\u2000-\u200a\u205f\u3000\u2028\u2029]/g;
  var NAMES = {'\u200b': 'ZERO WIDTH SPACE', '\u200c': 'ZERO WIDTH NON JOINER', '\u200d': 'ZERO WIDTH JOINER', '\u2060': 'WORD JOINER', '\ufeff': 'BYTE ORDER MARK',
    '\u00ad': 'SOFT HYPHEN', '\u200e': 'LEFT TO RIGHT MARK', '\u200f': 'RIGHT TO LEFT MARK', '\u00a0': 'NO BREAK SPACE', '\u202f': 'NARROW NO BREAK SPACE',
    '\u2009': 'THIN SPACE', '\u200a': 'HAIR SPACE', '\u2002': 'EN SPACE', '\u2003': 'EM SPACE', '\u3000': 'IDEOGRAPHIC SPACE', '\u2028': 'LINE SEPARATOR', '\u2029': 'PARAGRAPH SEPARATOR'};
  var INDIC = /[\u0900-\u0dff]/;
  function keepJoiner(m, off, str){
    if (m !== '\u200d' && m !== '\u200c') return false;
    if (INDIC.test(str.charAt(off - 1)) || INDIC.test(str.charAt(off + 1))) return true;
    return m === '\u200d' && /\p{Extended_Pictographic}|\ufe0f|[\u{1F3FB}-\u{1F3FF}]/u.test(str.slice(Math.max(0, off - 2), off));
  }
  function nm(ch){ return NAMES[ch] || ('U+' + ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')); }
  function run(){
    var s = $('tcIn').value, n = {inv: 0, sp: 0, md: 0, bot: 0, q: 0, el: 0, da: 0}, found = {};
    // map of hidden characters
    var map = s.replace(new RegExp(INV.source + '|' + SPC.source, 'g'), function(m, off, str){
      if (keepJoiner(m, off, str)) return m;
      found[nm(m)] = (found[nm(m)] || 0) + 1; return '\u27e6' + nm(m) + '\u27e7';
    });
    if ($('tcInv').checked) s = s.replace(INV, function(m, off, str){ if (keepJoiner(m, off, str)) return m; n.inv++; return ''; });
    if ($('tcSp').checked) s = s.replace(SPC, function(m){ n.sp++; return /[\u2028\u2029]/.test(m) ? '\n' : ' '; });
    if ($('tcBot').checked){
      var OPEN = /^(?:certainly|sure|of course|absolutely|great question|good question|happy to help|i(?:'|\u2019)d be (?:happy|glad) to|i would be (?:happy|glad) to)\b[^\n]{0,160}$/i;
      var INTRO = /^here(?:'|\u2019)?s?(?: is| are)?\b[^\n]{0,140}:\s*$/i;
      var CLOSE = /^(?:i hope (?:this|that) helps|hope (?:this|that) helps|let me know if|feel free to|would you like me to|if you(?:'|\u2019)d like,? i can|if you would like,? i can|is there anything else)/i;
      var ls = s.split('\n'), firstIdx = ls.findIndex(function(x){ return x.trim(); });
      ls = ls.filter(function(x, i){
        var t = x.trim(); if (!t) return true;
        if (i <= firstIdx + 1 && (OPEN.test(t) || INTRO.test(t)) && t.length < 180){ n.bot++; return false; }
        if (CLOSE.test(t)){ n.bot++; return false; }
        return true;
      });
      s = ls.join('\n');
    }
    if ($('tcMd').checked){
      s = s.replace(/^[ \t]{0,3}#{1,6}[ \t]+(.*?)[ \t]*#*[ \t]*$/gm, function(m, t){ n.md++; return t; });
      s = s.replace(/^[ \t]{0,3}(?:-{3,}|\*{3,}|_{3,})[ \t]*$/gm, function(){ n.md++; return ''; });
      s = s.replace(/\*\*([^*\n]+?)\*\*/g, function(m, t){ n.md++; return t; });
      s = s.replace(/__([^_\n]+?)__/g, function(m, t){ n.md++; return t; });
      s = s.replace(/(^|[^*\w])\*(?!\s)([^*\n]+?)\*(?!\*)/g, function(m, a, t){ n.md++; return a + t; });
      s = s.replace(/~~([^~\n]+)~~/g, function(m, t){ n.md++; return t; });
      s = s.replace(/!\[([^\]]*)\]\([^)]*\)/g, function(m, t){ n.md++; return t; });
      s = s.replace(/\[([^\]]+)\]\((?:[^)\s]+)\)/g, function(m, t){ n.md++; return t; });
      s = s.replace(/`([^`\n]+)`/g, function(m, t){ n.md++; return t; });
      s = s.replace(/^```.*$/gm, function(){ n.md++; return ''; });
      s = s.replace(/^([ \t]*)[-*+][ \t]+/gm, function(m, sp){ n.md++; return sp + '\u2022 '; });
      s = s.replace(/^[ \t]{0,3}>[ \t]?/gm, function(){ n.md++; return ''; });
    }
    if ($('tcQ').checked){
      s = s.replace(/[\u2018\u2019\u201a\u201b\u2032]/g, function(){ n.q++; return "'"; });
      s = s.replace(/[\u201c\u201d\u201e\u201f\u2033]/g, function(){ n.q++; return '"'; });
    }
    if ($('tcEl').checked) s = s.replace(/\u2026/g, function(){ n.el++; return '...'; });
    var dm = $('tcDash').value;
    if (dm !== 'keep'){
      s = s.replace(/(\d)\s*\u2013\s*(?=[\d\u20b9$\u20ac\u00a3])/g, function(m, d){ n.da++; return d + ' to '; });
      s = s.replace(/(^|\n)([ \t]*)[\u2014\u2015\u2013][ \t]*/g, function(m, a, b){ n.da++; return a + b; });
      s = s.replace(/[ \t]*[\u2014\u2015][ \t]*|[ \t]+\u2013[ \t]+/g, function(m, off, str){
        n.da++; if (dm === 'hyphen') return ' - ';
        var next = str.slice(off + m.length, off + m.length + 1);
        return /[.,;:!?]/.test(next) ? '' : ', ';
      });
      s = s.replace(/,\s*,/g, ',');
    }
    if ($('tcWs').checked){
      s = s.replace(/[ \t]+$/gm, '').replace(/([^\s])[ \t]{2,}/g, '$1 ').replace(/\n{3,}/g, '\n\n').replace(/^\s+|\s+$/g, '');
      s = s.replace(/ +([,.;:!?])/g, '$1');
    }
    $('tcOut').value = s;
    var hid = n.inv + n.sp, tot = hid + n.md + n.bot + n.q + n.el + n.da;
    $('tcHid').textContent = hid; $('tcDa').textContent = n.da; $('tcMk').textContent = n.md; $('tcTot').textContent = tot;
    var rows = [];
    if (n.inv) rows.push(n.inv + ' invisible character' + (n.inv > 1 ? 's' : '') + ' removed');
    if (n.sp) rows.push(n.sp + ' special space' + (n.sp > 1 ? 's' : '') + ' replaced');
    if (n.md) rows.push(n.md + ' Markdown mark' + (n.md > 1 ? 's' : '') + ' removed');
    if (n.bot) rows.push(n.bot + ' chatbot line' + (n.bot > 1 ? 's' : '') + ' removed');
    if (n.da) rows.push(n.da + ' long dash' + (n.da > 1 ? 'es' : '') + ' replaced');
    if (n.q) rows.push(n.q + ' curly quote' + (n.q > 1 ? 's' : '') + ' straightened');
    if (n.el) rows.push(n.el + ' ellipsis character' + (n.el > 1 ? 's' : '') + ' replaced');
    say('tcRep', tot ? 'ok' : '', tot ? '<strong>' + tot + ' fix' + (tot > 1 ? 'es' : '') + ' made.</strong><ul style="margin:6px 0 0 18px">' + rows.map(function(r){ return '<li>' + r + '</li>'; }).join('') + '</ul>' : 'Nothing to clean with the options you picked.');
    var keys = Object.keys(found);
    $('tcMap').textContent = keys.length ? keys.map(function(k){ return found[k] + ' x ' + k; }).join('\n') + '\n\n' + map : 'No hidden characters or special spaces found.';
  }
  $('tcForm').addEventListener('input', run); $('tcForm').addEventListener('change', run);
  $('tcCopy').addEventListener('click', function(){ copyText($('tcOut').value, 'toast'); });
  run();
''',
        content=f'''
    <h2>What Does the AI Text Cleaner Do?</h2>
    <p>Text copied from ChatGPT, Claude, Gemini and other AI tools often carries baggage you cannot see. Zero width characters, no break spaces and direction marks hide between words. Markdown stars and hashes show up as clutter when you paste into WordPress, Word or an email. And every answer seems to open with "Certainly!" and close with "I hope this helps".</p>
    <p>This AI text cleaner strips all of that in one pass and tells you exactly what it changed. It also lists every hidden character it found, so you can see what was really in the text. Everything runs in your browser.</p>

    <h2>How to Use the AI Text Cleaner</h2>
    <ol>
      <li><strong>Paste the AI written text</strong> into the left box.</li>
      <li><strong>Choose what to clean.</strong> Every option is on by default except keeping long dashes.</li>
      <li><strong>Pick how long dashes are handled:</strong> turned into commas, turned into spaced hyphens, or kept.</li>
      <li><strong>Check the report</strong> and the hidden character list to see what was fixed.</li>
      <li><strong>Copy the clean text</strong> and paste it into your CMS, document or email.</li>
    </ol>

    <h2>What Gets Cleaned</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Problem', 'Example', 'Why it matters')}
      <tbody>
        <tr><td>Invisible characters</td><td>Zero width space <code>U+200B</code>, byte order mark <code>U+FEFF</code>, soft hyphen <code>U+00AD</code></td><td>They break search, word counts, URLs and code, and can look odd in some fonts.</td></tr>
        <tr><td>Special spaces</td><td>No break space <code>U+00A0</code>, narrow no break space <code>U+202F</code></td><td>They stop lines from wrapping normally and can confuse forms and spreadsheets.</td></tr>
        <tr><td>Markdown symbols</td><td><code>## Heading</code>, <code>**bold**</code>, <code>[text](url)</code></td><td>They show up as raw symbols outside a Markdown editor.</td></tr>
        <tr><td>Chatbot filler</td><td>"Certainly! Here is...", "Let me know if..."</td><td>It is talk aimed at you, not your readers.</td></tr>
        <tr><td>Long dashes and curly quotes</td><td><code>&mdash;</code>, <code>&ldquo; &rdquo;</code></td><td>Many writers and style guides prefer simpler punctuation.</td></tr>
      </tbody>
    </table></div>
    <p>The cleaner keeps the zero width joiners that Hindi, Marathi, Tamil and other Indian scripts need, and the joiners inside emoji, so your text still renders correctly.</p>

    <h2>Tips for Publishing AI Assisted Text</h2>
    <ul>
      <li><strong>Cleaning is not rewriting.</strong> It fixes characters and formatting. Add your own facts, examples and voice so the page is genuinely useful.</li>
      <li><strong>Removing hidden characters does not hide AI use.</strong> They are not a reliable watermark, and AI detectors look at wording, not invisible characters.</li>
      <li><strong>Want headings and lists in WordPress?</strong> Turn off the Markdown option and convert the text with the <a href="{T}markdown-to-html-converter/">Markdown to HTML converter</a> instead.</li>
      <li><strong>Read it once more</strong> after replacing dashes. A comma is right most of the time, but sometimes a full stop reads better.</li>
    </ul>

    <h2>Write Better With AI</h2>
    <p>Google's view on AI assisted content is covered in <a href="{B}google-ai-content-guidelines-2026/">Google AI content guidelines</a>. Avoid common slips with <a href="{B}25-content-writing-mistakes/">25 content writing mistakes</a> and get better first drafts with <a href="{B}prompt-engineering-marketing-professionals/">prompt engineering for marketers</a>. To check length after cleaning, use the <a href="{SEO}word-character-counter/">word and character counter</a>.</p>
''',
        faqs=[
            ("Does ChatGPT add hidden watermarks to text?", "Some AI answers contain invisible characters such as no break spaces or zero width spaces, but they are not a reliable watermark. They usually come from formatting. Removing them makes your text cleaner, but it does not change how AI detectors judge the wording."),
            ("Will it break Hindi or emoji text?", "No. The cleaner keeps zero width joiners and non joiners next to Indian script letters and inside emoji sequences, because those are needed to display the text correctly."),
            ("Why replace long dashes?", "Heavy use of long dashes has become a common sign of AI written text, and many style guides prefer commas or full stops. You can switch the option to keep them if you like them."),
            ("Can I keep the headings and bullet points?", "Yes. Untick the Markdown option to keep the symbols, or paste the text into the Markdown to HTML converter to turn headings and lists into real HTML for WordPress."),
        ],
        related=[("Google AI Content Guidelines 2026", "google-ai-content-guidelines-2026"), ("Prompt Engineering for Marketing Professionals", "prompt-engineering-marketing-professionals"),
                 ("25 Content Writing Mistakes", "25-content-writing-mistakes"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
    ))

    # ---------- 5. AI PROMPT GENERATOR ----------
    tones = [('', 'Not set'), ('friendly and plain', 'Friendly and plain'), ('professional', 'Professional'), ('persuasive', 'Persuasive'),
             ('expert and precise', 'Expert and precise'), ('casual and fun', 'Casual and fun'), ('formal', 'Formal')]
    fmts = [('', 'Not set'), ('flowing paragraphs', 'Paragraphs'), ('a bulleted list', 'Bullet list'), ('numbered steps', 'Numbered steps'),
            ('a table', 'Table'), ('Markdown with H2 and H3 headings', 'Markdown with headings'), ('valid JSON only, with no extra text', 'JSON'),
            ('plain text with no Markdown', 'Plain text, no Markdown')]
    tpls = [('', 'Start from scratch'), ('blog', 'Blog post outline'), ('meta', 'SEO titles and meta descriptions'), ('ads', 'Ad copy variations'),
            ('email', 'Marketing email'), ('social', 'Social media posts'), ('summary', 'Summarise a document'), ('rewrite', 'Rewrite or edit text'), ('faq', 'FAQ from content')]
    TOOLS.append(dict(
        slug='ai-prompt-generator', short='PG', name='AI Prompt Generator',
        card='Build clear, structured prompts for ChatGPT, Claude and Gemini with role, context, format and rules, scored as you type.',
        title='AI Prompt Generator: Build Better ChatGPT Prompts',
        desc='Free AI prompt generator for ChatGPT, Claude and Gemini. Fill in role, task, audience, format and rules, pick a marketing template and copy a structured prompt.',
        h1='AI Prompt Generator',
        lead='Turn a rough idea into a clear, structured prompt for ChatGPT, Claude, Gemini or any AI model. Pick a marketing template or start fresh, fill in the parts that matter, and copy a prompt that follows current best practice.',
        tool='''<section class="tool" aria-label="AI prompt generator" id="pgForm">
    <div class="card" style="min-width:0">
      <h2>Prompt Parts</h2>
      ''' + F('pgTpl', 'Template', 'blog', tag='select', opts=tpls) + '''
      ''' + F('pgRole', 'Role', 'an experienced SEO content strategist who writes for small business owners in India', em='"You are..."') + '''
      ''' + F('pgTask', 'Task', 'Create a detailed blog post outline for the keyword "best time to post on Instagram".', em='start with a verb', tag='textarea', extra=' style="min-height:70px"') + '''
      ''' + F('pgCtx', 'Context and Goal', 'The post is for a digital marketing blog. The goal is to rank on Google and be cited in AI answers, so each section should answer one clear question.', em='why you need this', tag='textarea', extra=' style="min-height:70px"') + '''
      ''' + R2(F('pgAud', 'Audience', 'small business owners who manage their own Instagram'), F('pgTone', 'Tone', 'friendly and plain', tag='select', opts=tones)) + '''
      ''' + R2(F('pgFmt', 'Output Format', 'Markdown with H2 and H3 headings', tag='select', opts=fmts), F('pgLen', 'Length', '8 to 10 H2 sections, each with 2 to 4 bullet points')) + '''
      ''' + F('pgRules', 'Rules', 'Include a short FAQ section with 4 questions\nSuggest where a table or checklist would help\nKeep headings under 60 characters', em='one per line', tag='textarea', extra=' style="min-height:80px"') + '''
      ''' + F('pgEx', 'Example of Good Output', '', em='optional', tag='textarea', extra=' style="min-height:60px"') + '''
      ''' + F('pgDoc', 'Source Text or Data', '', em='optional, placed at the top', tag='textarea', extra=' style="min-height:60px"') + '''
      ''' + CK('pgAsk', 'Ask clarifying questions before starting if anything is unclear', False) + '''
      ''' + CK('pgUnsure', 'Say "I am not sure" rather than guessing facts') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Prompt</h2>
      <div class="tabs" id="pgTabs"><button type="button" class="on" data-m="plain">Plain Headings</button><button type="button" data-m="xml">XML Tags</button></div>
      <div class="stats">''' + S('pgScore', 'Prompt Score') + S('pgWords', 'Words') + S('pgTok', 'Tokens (est.)') + '''</div>
      <pre class="code-out" id="pgOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="pgCopy">Copy Prompt</button><span class="toast" id="toast">Copied!</span></div>
      <h3 style="font-size:16px;margin:18px 0 10px">Prompt Check</h3>
      <div class="kw-result" id="pgCheck"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var TPL = {
    blog: {role: 'an experienced SEO content strategist who writes for small business owners in India', task: 'Create a detailed blog post outline for the keyword "best time to post on Instagram".',
      ctx: 'The post is for a digital marketing blog. The goal is to rank on Google and be cited in AI answers, so each section should answer one clear question.', aud: 'small business owners who manage their own Instagram',
      tone: 'friendly and plain', fmt: 'Markdown with H2 and H3 headings', len: '8 to 10 H2 sections, each with 2 to 4 bullet points', rules: 'Include a short FAQ section with 4 questions\nSuggest where a table or checklist would help\nKeep headings under 60 characters'},
    meta: {role: 'an SEO copywriter who writes titles that earn clicks', task: 'Write 5 SEO title tags and 5 meta descriptions for the page described below.',
      ctx: 'The page sells handmade cotton kurtas online with free delivery across India. The focus keyword is "cotton kurtas for women".', aud: 'women shopping online for comfortable everyday wear',
      tone: 'persuasive', fmt: 'a table', len: '5 rows', rules: 'Titles 50 to 60 characters with the keyword near the start\nDescriptions 140 to 155 characters with a clear call to action\nShow the character count for each'},
    ads: {role: 'a Google Ads copywriter', task: 'Write responsive search ad assets for the product below.',
      ctx: 'We sell running shoes online with free delivery, cash on delivery and 30 day returns.', aud: 'runners in India searching for new shoes',
      tone: 'persuasive', fmt: 'a bulleted list', len: '15 headlines and 4 descriptions', rules: 'Headlines up to 30 characters\nDescriptions up to 90 characters\nNo exclamation marks in headlines\nInclude at least 3 headlines with a number or offer'},
    email: {role: 'an email marketer for a direct to consumer brand', task: 'Write a promotional email announcing our festive sale.',
      ctx: 'The sale runs for 5 days with up to 40% off. Past emails that told a short story did better than plain discount emails.', aud: 'existing customers who bought at least once',
      tone: 'friendly and plain', fmt: 'plain text with no Markdown', len: 'under 150 words', rules: 'Give 3 subject line options under 45 characters\nAdd a preheader under 90 characters\nOne clear call to action'},
    social: {role: 'a social media manager', task: 'Write 5 LinkedIn posts that promote our new free SEO checklist.',
      ctx: 'The checklist has 25 points and is free to download without signup.', aud: 'marketing managers and founders',
      tone: 'professional', fmt: 'numbered steps', len: 'each post under 120 words', rules: 'Open each post with a hook line\nUse at most 3 hashtags\nVary the angle in every post'},
    summary: {role: 'a careful analyst', task: 'Summarise the document in the source text section.',
      ctx: 'I need to brief my manager in two minutes.', aud: 'a busy manager who has not read the document',
      tone: 'professional', fmt: 'a bulleted list', len: '5 to 7 bullet points, then 3 action items', rules: 'Quote exact figures from the document\nFlag anything that looks uncertain\nOnly use facts that appear in the document'},
    rewrite: {role: 'a sharp editor', task: 'Rewrite the text in the source text section so it is clearer and shorter.',
      ctx: 'The text will be published on our website product page.', aud: 'first time visitors',
      tone: 'friendly and plain', fmt: 'flowing paragraphs', len: 'about 30% shorter than the original', rules: 'Keep every fact and number\nUse short sentences\nUse active voice'},
    faq: {role: 'a content strategist who writes for search and AI answers', task: 'Write an FAQ section based on the content in the source text section.',
      ctx: 'The FAQ will go at the end of the page and should answer the questions real customers ask.', aud: 'customers comparing options before buying',
      tone: 'friendly and plain', fmt: 'Markdown with H2 and H3 headings', len: '6 questions, answers of 40 to 60 words', rules: 'Write each question the way a person would type it\nStart each answer with a direct one sentence reply\nOnly use facts from the source text'}
  };
  var mode = 'plain';
  function fill(k){
    var t = TPL[k]; if (!t) return;
    $('pgRole').value = t.role; $('pgTask').value = t.task; $('pgCtx').value = t.ctx; $('pgAud').value = t.aud;
    $('pgTone').value = t.tone; $('pgFmt').value = t.fmt; $('pgLen').value = t.len; $('pgRules').value = t.rules;
  }
  function build(){
    var role = v('pgRole'), task = v('pgTask'), ctx = v('pgCtx'), aud = v('pgAud'), tone = $('pgTone').value, fmt = $('pgFmt').value, len = v('pgLen');
    var rules = v('pgRules').split(/\r?\n/).map(function(s){ return s.replace(/^[\s\-*\u2022\d.)]+/, '').trim(); }).filter(Boolean);
    var ex = v('pgEx'), doc = v('pgDoc');
    if ($('pgUnsure').checked) rules.push('If you are not sure about a fact, say so rather than guessing.');
    if ($('pgAsk').checked) rules.push('If anything important is unclear, ask me up to 3 questions before you start.');
    var out = [], X = mode === 'xml';
    function sec(name, tag, body){ if (!body) return; out.push(X ? '<' + tag + '>\n' + body + '\n</' + tag + '>' : '## ' + name + '\n' + body); }
    if (role) out.push('You are ' + role.replace(/^you are\s+/i, '').replace(/\.$/, '') + '.');
    if (doc) sec('Source text', 'source_text', doc);
    sec('Task', 'task', task);
    sec('Context', 'context', ctx);
    var spec = [];
    if (aud) spec.push('Audience: ' + aud);
    if (tone) spec.push('Tone: ' + tone);
    if (fmt) spec.push('Format: ' + fmt);
    if (len) spec.push('Length: ' + len);
    sec('Output requirements', 'output_requirements', spec.map(function(s){ return '- ' + s; }).join('\n'));
    sec('Rules', 'rules', rules.map(function(s){ return '- ' + s.replace(/\.?$/, '.'); }).join('\n'));
    if (ex) out.push(X ? '<example>\n' + ex + '\n</example>' : '## Example of the output I want\n' + ex);
    if (doc && X) out.push('Base your answer only on the text inside the source_text tags.');
    var txt = out.join('\n\n');
    $('pgOut').textContent = txt || 'Fill in at least the task to build a prompt.';
    // score
    var chk = [], score = 0;
    function t(ok, pts, good, bad){ if (ok) score += pts; else chk.push(['warn', bad]); }
    t(task.length > 15, 25, '', 'Describe the task in a full sentence.');
    t(/^(write|create|draft|summari[sz]e|rewrite|edit|list|explain|compare|generate|give|make|plan|analy[sz]e|translate|turn|suggest|find|review|build|design|outline|convert|classify|extract)\b/i.test(task), 10, '', 'Start the task with an action verb such as ' + c('Write') + ', ' + c('Summarise') + ' or ' + c('Create') + '.');
    t(role.length > 5, 10, '', 'Add a role. Even one line like "an experienced SEO editor" changes the style of the answer.');
    t(words(ctx) >= 8, 15, '', 'Add context: what the result is for and why. Models follow rules better when they know the reason.');
    t(!!aud, 10, '', 'Name the audience so the model can pitch the language right.');
    t(!!fmt, 10, '', 'Choose an output format so you get a result you can use straight away.');
    t(!!len, 10, '', 'Set a length, such as a word count or number of items.');
    t(rules.length > 0, 5, '', 'Add one or two rules for what a great answer must include.');
    t(!!ex, 5, '', 'Add an example of good output if you have one. Examples are one of the strongest ways to steer format and style.');
    if (/\b(don'?t|do not|never|avoid)\b/i.test(v('pgRules'))) chk.push(['warn', 'Some rules say what not to do. Where you can, say what to do instead, for example "use plain text" rather than "do not use Markdown".']);
    if (!doc && /source text/i.test(task)) chk.push(['bad', 'The task mentions the source text, but the source text box is empty.']);
    $('pgScore').textContent = score + '%'; $('pgWords').textContent = fmtN(words(txt)); $('pgTok').textContent = fmtN(estTokens(txt));
    issues('pgCheck', chk, '<strong>Strong prompt.</strong> It has a role, a clear task, context, audience, format, length, rules and an example.', 12);
    return txt;
  }
  $('pgTpl').addEventListener('change', function(){ fill(this.value); build(); });
  $('pgForm').addEventListener('input', build); $('pgForm').addEventListener('change', build);
  document.querySelectorAll('#pgTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#pgTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); mode = b.getAttribute('data-m'); build(); }); });
  $('pgCopy').addEventListener('click', function(){ copyText(build(), 'toast'); });
  build();
''',
        content=f'''
    <h2>What Is an AI Prompt Generator?</h2>
    <p>An AI prompt generator helps you write prompts that get a usable answer the first time. Most weak AI results come from weak prompts: a vague task, no context, no audience and no idea of what the finished result should look like.</p>
    <p>This tool walks you through the parts that matter, puts them in a clear order, and scores your prompt as you type. It works for ChatGPT, Claude, Gemini, Copilot and any other chat model. Nothing is sent to an AI from this page. You copy the prompt and paste it where you like.</p>

    <h2>How to Use the Prompt Generator</h2>
    <ol>
      <li><strong>Pick a template</strong> such as a blog outline, meta descriptions, ad copy or an email, or start from scratch.</li>
      <li><strong>Edit the task</strong> so it starts with a verb and says exactly what you want.</li>
      <li><strong>Add context, audience, tone, format and length.</strong> Each one removes a guess the model would otherwise make.</li>
      <li><strong>Add rules and an example</strong> of good output if you have one.</li>
      <li><strong>Paste any source text</strong> you want the model to work from. It is placed at the top, where long documents work best.</li>
      <li><strong>Choose plain headings or XML tags,</strong> then copy the prompt.</li>
    </ol>

    <h2>The Parts of a Strong Prompt</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Part', 'What to write', 'Why it helps')}
      <tbody>
        <tr><td>Role</td><td>Who the model should act as</td><td>Sets vocabulary, depth and style in one line.</td></tr>
        <tr><td>Task</td><td>One clear instruction that starts with a verb</td><td>Removes the biggest source of vague answers.</td></tr>
        <tr><td>Context</td><td>What the result is for and why</td><td>Models apply rules better when they know the reason behind them.</td></tr>
        <tr><td>Audience and tone</td><td>Who will read it and how it should sound</td><td>Keeps the language at the right level.</td></tr>
        <tr><td>Format and length</td><td>Table, bullets, JSON, word count</td><td>Gives you output you can paste straight into your work.</td></tr>
        <tr><td>Examples</td><td>One to five samples of good output</td><td>The most reliable way to steer format and style.</td></tr>
      </tbody>
    </table></div>
    <p>These parts follow the <a href="https://platform.claude.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices" {EXT}>Claude prompting best practices</a>, which recommend clear and explicit instructions, explaining why, giving 3 to 5 examples, and using XML tags to separate instructions from content.</p>

    <h2>Prompt Writing Tips</h2>
    <ul>
      <li><strong>Use the colleague test.</strong> If a smart coworker with no background would be confused by your prompt, the model will be too.</li>
      <li><strong>Say what to do, not what to avoid.</strong> "Write in plain paragraphs" works better than "do not use bullet points".</li>
      <li><strong>Use XML tags for long inputs.</strong> Tags like <code>&lt;source_text&gt;</code> stop the model from mixing your instructions with your data.</li>
      <li><strong>Ask for honesty.</strong> Telling the model it may say "I am not sure" reduces made up facts.</li>
      <li><strong>Save prompts that work.</strong> Keep a library of your best prompts and reuse them.</li>
    </ul>

    <h2>Get More From AI</h2>
    <p>Go deeper with <a href="{B}prompt-engineering-marketing-professionals/">prompt engineering for marketing professionals</a>, learn why models invent facts in <a href="{B}ai-hallucinations-explained-causes-prevention/">AI hallucinations explained</a>, and explore useful apps in <a href="{B}ai-tools-for-marketers/">AI tools for marketers</a>. Before you paste a long prompt, check its size with the <a href="{T}ai-token-counter/">AI token counter</a>.</p>
''',
        faqs=[
            ("Does this prompt generator use AI?", "No. It builds your prompt from the parts you fill in, using a proven structure, right in your browser. You then paste the prompt into ChatGPT, Claude, Gemini or any other AI tool."),
            ("Should I use plain headings or XML tags?", "Both work well with modern models. XML tags are best when your prompt includes long source text or data, because they keep your instructions clearly separate from the content. Plain headings are easier to read and edit."),
            ("How long should a prompt be?", "As long as it needs to be clear, and no longer. Most good marketing prompts are 80 to 250 words plus any source text. Each extra line should remove a guess the model would otherwise make."),
            ("What does the prompt score mean?", "It checks whether your prompt has the parts that most improve answers: a clear task with a verb, a role, context, audience, format, length, rules and an example. A high score does not guarantee a perfect answer, but a low one usually means a vague result."),
        ],
        related=[("Prompt Engineering for Marketing Professionals", "prompt-engineering-marketing-professionals"), ("AI Hallucinations Explained", "ai-hallucinations-explained-causes-prevention"),
                 ("AI Tools for Marketers", "ai-tools-for-marketers"), ("AI Automation Workflows Every Business Needs", "ai-automation-workflows-every-business")],
    ))

    # ---------- 6. HTML TO MARKDOWN CONVERTER ----------
    HM_HTML = '''<!doctype html>
<html lang="en">
<head><title>Monsoon Skin Care Tips</title><style>body{font-family:Arial}</style>
<script>window.dataLayer = window.dataLayer || [];</script></head>
<body>
<header class="site-header"><a href="/">Glow Studio</a>
  <nav><ul><li><a href="/shop/">Shop</a></li><li><a href="/blog/">Blog</a></li></ul></nav>
</header>
<main>
  <article>
    <h1>5 Monsoon Skin Care Tips That Really Work</h1>
    <p>Humid weather means <strong>more oil</strong> and <em>more breakouts</em>. These simple habits keep skin calm all season.
    Read our <a href="https://www.example.com/blog/skin-types/">guide to skin types</a> first.</p>
    <img src="https://www.example.com/img/monsoon.jpg" alt="Woman applying face wash">
    <h2>Daily Routine</h2>
    <ol>
      <li>Wash with a gentle gel cleanser twice a day.</li>
      <li>Use a light moisturiser
        <ul><li>Gel based for oily skin</li><li>Lotion for dry skin</li></ul>
      </li>
      <li>Apply SPF 30 or higher, even on cloudy days.</li>
    </ol>
    <h2>Products Compared</h2>
    <table>
      <thead><tr><th>Product</th><th>Best for</th><th>Price</th></tr></thead>
      <tbody>
        <tr><td>Gel Cleanser</td><td>Oily skin</td><td>&#8377;349</td></tr>
        <tr><td>Clay Mask</td><td>Open pores</td><td>&#8377;499</td></tr>
      </tbody>
    </table>
    <blockquote><p>Drink plenty of water. Hydrated skin makes less oil.</p></blockquote>
    <p>Store your toner in the fridge and use the code <code>MONSOON10</code> for 10% off.</p>
  </article>
</main>
<footer><p>&copy; 2026 Glow Studio. All rights reserved.</p></footer>
<script src="/js/app.js"></script>
</body>
</html>'''
    TOOLS.append(dict(
        slug='html-to-markdown-converter', short='HM', name='HTML to Markdown Converter',
        card='Turn a web page or HTML snippet into clean Markdown for ChatGPT, Claude, llms.txt pages and docs, with far fewer tokens.',
        title='HTML to Markdown Converter: Clean Markdown for AI',
        desc='Free HTML to Markdown converter. Paste a web page or snippet and get clean Markdown with headings, links, lists and tables, ready for ChatGPT, Claude or docs.',
        h1='HTML to Markdown Converter',
        lead='Paste the HTML of any page or snippet and get clean Markdown. Menus, scripts and footers are stripped, while headings, links, lists, tables and images are kept, so AI tools read your content with a fraction of the tokens.',
        tool='''<section class="tool" aria-label="HTML to Markdown converter" id="hmForm">
    <div class="card" style="min-width:0">
      <h2>HTML Input</h2>
      ''' + F('hmIn', 'Paste HTML', HM_HTML, em='a full page or a snippet', tag='textarea', mono=True, extra=' style="min-height:380px;white-space:pre;overflow-wrap:normal"') + '''
      ''' + CK('hmMain', 'Keep only the main content (skip header, nav, footer, aside, forms)') + '''
      ''' + CK('hmLinks', 'Keep links') + '''
      ''' + CK('hmImg', 'Keep images') + '''
      ''' + CK('hmTbl', 'Convert tables to Markdown tables') + '''
      ''' + F('hmBul', 'Bullet Style', '-', tag='select', opts=[('-', 'Hyphen ( - item )'), ('*', 'Star ( * item )')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Markdown Output</h2>
      <div class="stats">''' + S('hmT1', 'HTML Tokens') + S('hmT2', 'Markdown Tokens') + S('hmSave', 'Tokens Saved') + '''</div>
      ''' + F('hmOut', 'Markdown', '', tag='textarea', mono=True, extra=' readonly style="min-height:380px;white-space:pre;overflow-wrap:normal"') + '''
      <div class="actions" style="margin:-6px 0 16px"><button class="btn dark" id="hmCopy">Copy Markdown</button><button class="btn" id="hmDl">Download .md</button><span class="toast" id="toast">Copied!</span></div>
      <div class="kw-result" id="hmNote"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var BUL = '-', KL = true, KI = true, KT = true;
  var SKIP = /^(script|style|noscript|template|iframe|svg|canvas|object|embed|head|meta|link|button|input|select|textarea|form)$/;
  var CHROME = /^(header|nav|footer|aside)$/;
  function inl(node){
    var out = '';
    node.childNodes.forEach(function(n){
      if (n.nodeType === 3){ out += n.nodeValue.replace(/\s+/g, ' ').replace(/([*_`\\])/g, '\\$1'); return; }
      if (n.nodeType !== 1) return;
      var t = n.tagName.toLowerCase();
      if (SKIP.test(t)) return;
      var inner = function(){ return inl(n); };
      if (t === 'br'){ out += '  \n'; return; }
      if (t === 'strong' || t === 'b'){ var x = inner().trim(); if (x) out += '**' + x + '**'; return; }
      if (t === 'em' || t === 'i'){ var y = inner().trim(); if (y) out += '*' + y + '*'; return; }
      if (t === 'del' || t === 's'){ var z = inner().trim(); if (z) out += '~~' + z + '~~'; return; }
      if (t === 'code'){ var cd = n.textContent; out += cd.indexOf('`') > -1 ? '`` ' + cd + ' ``' : '`' + cd + '`'; return; }
      if (t === 'a'){ var txt = inner().trim(), h = n.getAttribute('href') || '';
        if (!KL || !h || /^(javascript|#)/i.test(h)) out += txt; else out += '[' + (txt || h) + '](' + h.replace(/ /g, '%20').replace(/\)/g, '%29') + ')'; return; }
      if (t === 'img'){ if (KI && n.getAttribute('src')) out += '![' + (n.getAttribute('alt') || '').replace(/[\[\]]/g, '') + '](' + n.getAttribute('src') + ')'; return; }
      out += inner();
    });
    return out;
  }
  function list(el, ind){
    ind = ind || '';
    var ordered = el.tagName.toLowerCase() === 'ol', i = parseInt(el.getAttribute('start') || '1', 10), out = [];
    Array.prototype.forEach.call(el.children, function(li){
      if (li.tagName.toLowerCase() !== 'li') return;
      var mark = ordered ? (i++) + '.' : BUL, sub = ind + new Array(mark.length + 2).join(' ');
      var textParts = [], subs = [];
      li.childNodes.forEach(function(n){
        if (n.nodeType === 1 && /^(ul|ol)$/i.test(n.tagName)) subs.push(list(n, sub));
        else if (n.nodeType === 1 && /^(p|div)$/i.test(n.tagName)) textParts.push(inl(n));
        else { var w = document.createElement('span'); w.appendChild(n.cloneNode(true)); textParts.push(inl(w)); }
      });
      out.push(ind + mark + ' ' + textParts.join(' ').replace(/\s+/g, ' ').trim());
      subs.forEach(function(s){ out.push(s); });
    });
    return out.join('\n');
  }
  function table(el){
    var rows = Array.prototype.slice.call(el.querySelectorAll('tr'));
    if (!rows.length) return '';
    var grid = rows.map(function(r){ return Array.prototype.map.call(r.children, function(cell){ return inl(cell).replace(/\|/g, '\\|').replace(/\s+/g, ' ').trim(); }); });
    var w = Math.max.apply(null, grid.map(function(r){ return r.length; }));
    grid = grid.map(function(r){ while (r.length < w) r.push(''); return r; });
    var line = function(r){ return '| ' + r.join(' | ') + ' |'; };
    return [line(grid[0]), '| ' + grid[0].map(function(){ return '---'; }).join(' | ') + ' |'].concat(grid.slice(1).map(line)).join('\n');
  }
  function blocks(node, out){
    node.childNodes.forEach(function(n){
      if (n.nodeType === 3){ var tx = n.nodeValue.replace(/\s+/g, ' ').trim(); if (tx) out.push(tx); return; }
      if (n.nodeType !== 1) return;
      var t = n.tagName.toLowerCase();
      if (SKIP.test(t)) return;
      if (/^h[1-6]$/.test(t)){ var h = inl(n).trim(); if (h) out.push(new Array(+t[1] + 1).join('#') + ' ' + h); return; }
      if (t === 'p'){ var p = inl(n).trim(); if (p) out.push(p.replace(/ *\n */g, '\n').replace(/  \n$/, '')); return; }
      if (t === 'ul' || t === 'ol'){ var l = list(n, ''); if (l) out.push(l); return; }
      if (t === 'pre'){ var code = n.textContent.replace(/\n$/, ''), lang = ((n.querySelector('code') || n).className.match(/language-([\w+-]+)/) || [, ''])[1]; out.push('```' + lang + '\n' + code + '\n```'); return; }
      if (t === 'blockquote'){ var inner = []; blocks(n, inner); if (inner.length) out.push(inner.join('\n\n').split('\n').map(function(x){ return '> ' + x; }).join('\n').replace(/> $/gm, '>')); return; }
      if (t === 'hr'){ out.push('---'); return; }
      if (t === 'table'){ if (KT) out.push(table(n)); else n.querySelectorAll('tr').forEach(function(r){ var x = inl(r).replace(/\s+/g, ' ').trim(); if (x) out.push(x); }); return; }
      if (t === 'img' || t === 'a' || t === 'strong' || t === 'em' || t === 'span' || t === 'b' || t === 'i' || t === 'code'){ var w = document.createElement('span'); w.appendChild(n.cloneNode(true)); var x = inl(w).trim(); if (x) out.push(x); return; }
      if (t === 'figure'){ blocks(n, out); return; }
      if (t === 'figcaption'){ var fc = inl(n).trim(); if (fc) out.push('*' + fc + '*'); return; }
      blocks(n, out);
    });
    return out;
  }
  function run(){
    BUL = $('hmBul').value; KL = $('hmLinks').checked; KI = $('hmImg').checked; KT = $('hmTbl').checked;
    var src = $('hmIn').value, doc = new DOMParser().parseFromString(src, 'text/html'), root = doc.body, note = [];
    if ($('hmMain').checked){
      var m = doc.querySelector('main') || doc.querySelector('article') || doc.querySelector('[role=main]');
      if (m) root = m;
      root.querySelectorAll('header,nav,footer,aside').forEach(function(x){ if (!x.closest('article') || x.tagName.toLowerCase() === 'nav' || x.tagName.toLowerCase() === 'aside') x.remove(); });
      note.push(m ? 'Used the ' + c('<' + m.tagName.toLowerCase() + '>') + ' element as the main content.' : 'No ' + c('<main>') + ' or ' + c('<article>') + ' found, so the whole body was converted without header, nav and footer.');
    }
    var md = blocks(root, []).join('\n\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
    if (!md.trim()) md = '';
    $('hmOut').value = md;
    var a = estTokens(src), b = estTokens(md);
    $('hmT1').textContent = fmtN(a); $('hmT2').textContent = fmtN(b); $('hmSave').textContent = a ? Math.max(0, Math.round((1 - b / a) * 100)) + '%' : '0%';
    var title = (doc.querySelector('title') || {}).textContent;
    if (title) note.push('Page title: <strong>' + esc(title.trim()) + '</strong>.');
    if (!md) say('hmNote', 'warn', 'No readable content found. Paste HTML that contains text, headings or lists.');
    else say('hmNote', 'ok', note.join(' ') + ' Markdown uses about <strong>' + fmtN(b) + '</strong> tokens instead of ' + fmtN(a) + '.');
    return md;
  }
  $('hmForm').addEventListener('input', run); $('hmForm').addEventListener('change', run);
  $('hmCopy').addEventListener('click', function(){ copyText(run(), 'toast'); });
  $('hmDl').addEventListener('click', function(){ download('page.md', run(), 'text/markdown'); });
  run();
''',
        content=f'''
    <h2>What Is an HTML to Markdown Converter?</h2>
    <p>An HTML to Markdown converter turns web page code into Markdown, the simple text format with <code>#</code> for headings, <code>**</code> for bold and <code>-</code> for list items. Markdown keeps the structure of your content but drops all the tags, classes, scripts and styles.</p>
    <p>That makes it the best format to give AI tools. When you paste a page into ChatGPT, Claude or Gemini, or feed it to a RAG system, Markdown uses far fewer tokens than raw HTML and the model sees clear headings instead of noise. It is also the format the llms.txt proposal suggests for the clean <code>.md</code> versions of your pages.</p>

    <h2>How to Use the Converter</h2>
    <ol>
      <li><strong>Copy the HTML.</strong> In your browser, right click a page, choose View Page Source, then select all and copy. A snippet from your CMS works too.</li>
      <li><strong>Paste it</strong> into the HTML box. The conversion updates as you type.</li>
      <li><strong>Choose your options.</strong> Keep only the main content, keep or drop links and images, and convert tables.</li>
      <li><strong>Check the token savings</strong> to see how much smaller the Markdown is.</li>
      <li><strong>Copy or download</strong> the Markdown as a <code>.md</code> file.</li>
    </ol>

    <h2>How HTML Becomes Markdown</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('HTML', 'Markdown')}
      <tbody>
        <tr><td><code>&lt;h2&gt;Title&lt;/h2&gt;</code></td><td><code>## Title</code></td></tr>
        <tr><td><code>&lt;strong&gt;</code> and <code>&lt;em&gt;</code></td><td><code>**bold**</code> and <code>*italic*</code></td></tr>
        <tr><td><code>&lt;a href="url"&gt;text&lt;/a&gt;</code></td><td><code>[text](url)</code></td></tr>
        <tr><td><code>&lt;img src alt&gt;</code></td><td><code>![alt](src)</code></td></tr>
        <tr><td><code>&lt;ul&gt;</code> and <code>&lt;ol&gt;</code>, including nested lists</td><td><code>- item</code> and <code>1. item</code></td></tr>
        <tr><td><code>&lt;table&gt;</code></td><td>A pipe table with a header row</td></tr>
        <tr><td><code>&lt;pre&gt;&lt;code&gt;</code></td><td>A fenced code block with the language kept</td></tr>
        <tr><td><code>&lt;script&gt;</code>, <code>&lt;style&gt;</code>, <code>&lt;nav&gt;</code>, forms</td><td>Removed</td></tr>
      </tbody>
    </table></div>
    <p>The output follows common <a href="https://github.github.com/gfm/" {EXT}>GitHub Flavored Markdown</a>, which ChatGPT, Claude, GitHub, Notion and most docs tools understand.</p>

    <h2>Tips for Clean Results</h2>
    <ul>
      <li><strong>Use semantic HTML.</strong> Pages built with real <code>&lt;main&gt;</code>, <code>&lt;article&gt;</code> and heading tags convert most cleanly.</li>
      <li><strong>Drop links for summaries.</strong> If you only want an AI to read the text, untick links to save more tokens.</li>
      <li><strong>Check tables.</strong> Merged cells cannot be shown in Markdown, so very complex tables may need a quick tidy.</li>
      <li><strong>Nothing is fetched.</strong> The tool only converts what you paste, and images are not loaded.</li>
    </ul>

    <h2>Make Your Content Easy for AI to Read</h2>
    <p>See why structure matters in <a href="{B}structuring-html-for-ai-crawlability/">structuring HTML for AI crawlability</a> and <a href="{B}html-semantic-elements-explained/">HTML semantic elements explained</a>, then learn how this ties into <a href="{B}llms-txt-explained/">llms.txt</a>. Going the other way? Use the <a href="{T}markdown-to-html-converter/">Markdown to HTML converter</a>.</p>
''',
        faqs=[
            ("Why convert HTML to Markdown for ChatGPT or Claude?", "Markdown keeps headings, lists and links but drops tags, scripts and styles. A typical page uses far fewer tokens as Markdown, so it costs less, fits more into the context window and is easier for the model to follow."),
            ("Can I convert a page just by entering its URL?", "No. To keep everything private and in your browser, the tool does not fetch other sites. Open the page, view its source, and paste the HTML into the box."),
            ("Does it keep tables and nested lists?", "Yes. Tables become Markdown pipe tables with a header row, and nested bullet or numbered lists keep their indentation. Merged table cells cannot be shown in Markdown."),
            ("Is the converted Markdown safe to publish?", "The converter only outputs text and Markdown syntax, and scripts, styles and forms are removed. Always read the result before you publish it, especially links copied from someone else's page."),
        ],
        related=[("Structuring HTML for AI Crawlability", "structuring-html-for-ai-crawlability"), ("HTML Semantic Elements Explained", "html-semantic-elements-explained"),
                 ("llms.txt Explained", "llms-txt-explained"), ("Retrieval Augmented Generation Explained", "retrieval-augmented-generation-rag-explained")],
    ))

    # ---------- 7. MARKDOWN TO HTML CONVERTER ----------
    MH_MD = '''# How to Choose a Running Shoe

Picking the right shoe is easier than it looks. Focus on **fit**, **cushioning** and the *surface* you run on most.

## 1. Know Your Foot Type

Check the wear on your old shoes:

- Wear on the inner edge often means your foot rolls inward
- Even wear usually means a neutral stride
  - Neutral runners can choose almost any shoe
- Wear on the outer edge points to a high arch

## 2. Compare the Main Types

| Type | Best for | Typical price |
| --- | --- | ---: |
| Neutral | Most runners | \u20b94,000 |
| Stability | Feet that roll inward | \u20b96,500 |
| Trail | Rough ground and hills | \u20b97,000 |

## 3. Try Before You Buy

1. Shop in the evening, when feet are slightly larger
2. Leave a thumb width of space at the toe
3. Jog a few steps in the store

> Tip: replace running shoes every 600 to 800 km.

Read our [full sizing guide](https://www.example.com/sizing/) or use the code `RUN10` for 10% off.'''
    TOOLS.append(dict(
        slug='markdown-to-html-converter', short='MH', name='Markdown to HTML Converter',
        card='Paste Markdown from ChatGPT, Claude or Gemini and get clean HTML for WordPress, with a live preview and table support.',
        title='Markdown to HTML Converter: ChatGPT to WordPress',
        desc='Free Markdown to HTML converter. Paste a ChatGPT, Claude or Gemini answer and get clean HTML with headings, lists, tables and links, plus a live preview.',
        h1='Markdown to HTML Converter',
        lead='AI chat tools write in Markdown, but WordPress and most email and CMS editors want HTML. Paste the Markdown, preview the result, and copy clean HTML with real headings, lists, tables and links.',
        tool='''<section class="tool" aria-label="Markdown to HTML converter" id="mhForm">
    <div class="card" style="min-width:0">
      <h2>Markdown Input</h2>
      ''' + F('mhIn', 'Paste Markdown', MH_MD, em='from ChatGPT, Claude, Gemini or any editor', tag='textarea', mono=True, extra=' style="min-height:400px"') + '''
      ''' + CK('mhH1', 'Remove the first H1 (WordPress adds the post title)', False) + '''
      ''' + CK('mhShift', 'Turn every H1 into an H2', False) + '''
      ''' + CK('mhNew', 'Open external links in a new tab', False) + '''
      ''' + CK('mhNum', 'Remove numbers like "1." from the start of headings', False) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>HTML Output</h2>
      <div class="tabs" id="mhTabs"><button type="button" class="on" data-m="code">HTML Code</button><button type="button" data-m="view">Preview</button></div>
      <div class="stats">''' + S('mhHs', 'Headings') + S('mhLs', 'Lists') + S('mhTs', 'Tables') + S('mhAs', 'Links') + '''</div>
      <pre class="code-out" id="mhOut" ''' + PRE + '''></pre>
      <div id="mhView" style="display:none;border:1px solid #e6e6e6;border-radius:10px;padding:6px 16px;max-height:520px;overflow:auto;overflow-wrap:anywhere"></div>
      <div class="actions"><button class="btn dark" id="mhCopy">Copy HTML</button><button class="btn" id="mhDl">Download .html</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips">In WordPress, add a Custom HTML block and paste the code, or use the code editor view.</div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var NEW = false, cnt;
  function safeUrl(u){ u = u.trim(); return /^(https?:|mailto:|tel:|\/|#|\.{0,2}\/)/i.test(u) || !/^[a-z][a-z0-9+.-]*:/i.test(u) ? u : '#'; }
  function attr(s){ return esc(s).replace(/'/g, '&#39;'); }
  function inline(s){
    var codes = [];
    s = s.replace(/(`+)([\s\S]*?[^`])\1(?!`)/g, function(m, f, t){ codes.push('<code>' + esc(t.trim()) + '</code>'); return '\u0000' + (codes.length - 1) + '\u0000'; });
    s = esc(s);
    s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)/g, function(m, a, u, t){ return '<img src="' + attr(safeUrl(u)) + '" alt="' + a + '"' + (t ? ' title="' + t + '"' : '') + '>'; });
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)/g, function(m, t, u, ti){ cnt.a++; u = safeUrl(u.replace(/&amp;/g, '&'));
      return '<a href="' + attr(u) + '"' + (ti ? ' title="' + ti + '"' : '') + (NEW && /^https?:/i.test(u) ? ' target="_blank" rel="noopener"' : '') + '>' + t + '</a>'; });
    s = s.replace(/(^|[\s(])(https?:\/\/[^\s<]+[^\s<.,;:!?)])/g, function(m, a, u){ cnt.a++; return a + '<a href="' + u + '"' + (NEW ? ' target="_blank" rel="noopener"' : '') + '>' + u + '</a>'; });
    s = s.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>').replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/__([^_]+)__/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*\w])\*(?!\s)([^*]+?)\*(?!\*)/g, '$1<em>$2</em>').replace(/(^|[^_\w])_(?!\s)([^_]+?)_(?![_\w])/g, '$1<em>$2</em>');
    s = s.replace(/~~([^~]+)~~/g, '<del>$1</del>').replace(/ {2,}$/gm, '<br>');
    return s.replace(/\u0000(\d+)\u0000/g, function(m, i){ return codes[+i]; });
  }
  function isTableSep(l){ return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$/.test(l) && l.indexOf('-') > -1; }
  function cells(l){ return l.trim().replace(/^\|/, '').replace(/\|$/, '').split(/(?<!\\)\|/).map(function(x){ return x.trim().replace(/\\\|/g, '|'); }); }
  function parseList(lines, i){
    var first = lines[i].match(/^(\s*)([-*+]|\d+[.)])\s+/), base = first[1].length, ordered = /\d/.test(first[2]);
    var start = ordered ? parseInt(first[2], 10) : 1, items = [];
    while (i < lines.length){
      var m = lines[i].match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
      if (m && m[1].length === base){ items.push({text: m[3], sub: []}); i++; continue; }
      if (m && m[1].length > base && items.length){ var r = parseList(lines, i); items[items.length - 1].sub.push(r.html); i = r.i; continue; }
      if (!m && /^\s+\S/.test(lines[i]) && items.length && lines[i].match(/^\s*/)[0].length > base){ items[items.length - 1].text += ' ' + lines[i].trim(); i++; continue; }
      break;
    }
    cnt.l++;
    var tag = ordered ? 'ol' : 'ul';
    return {i: i, html: '<' + tag + (ordered && start !== 1 ? ' start="' + start + '"' : '') + '>\n' + items.map(function(it){
      var t = inline(it.text).replace(/^\[ \]\s*/, '&#9744; ').replace(/^\[x\]\s*/i, '&#9745; ');
      return '  <li>' + t + (it.sub.length ? '\n' + it.sub.join('\n') + '\n  ' : '') + '</li>'; }).join('\n') + '\n</' + tag + '>'};
  }
  function convert(md, opt){
    var lines = md.replace(/\r\n?/g, '\n').replace(/\t/g, '    ').split('\n'), out = [], i = 0, firstH1 = true;
    while (i < lines.length){
      var l = lines[i];
      if (!l.trim()){ i++; continue; }
      var f = l.match(/^\s*(```+|~~~+)\s*([\w+-]*)/);
      if (f){ var buf = []; i++; while (i < lines.length && lines[i].trim().indexOf(f[1]) !== 0){ buf.push(lines[i]); i++; } i++;
        out.push('<pre><code' + (f[2] ? ' class="language-' + attr(f[2]) + '"' : '') + '>' + esc(buf.join('\n')) + '</code></pre>'); continue; }
      var h = l.match(/^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/);
      if (!h && i + 1 < lines.length && l.trim() && /^\s*(=+|-+)\s*$/.test(lines[i + 1]) && !/^\s*[-*+]\s/.test(l)){ h = [0, /=/.test(lines[i + 1]) ? '#' : '##', l.trim()]; i++; }
      if (h){
        var lv = h[1].length, txt = h[2]; i++;
        if (lv === 1 && opt.h1 && firstH1){ firstH1 = false; continue; }
        if (lv === 1 && opt.shift) lv = 2;
        if (opt.num) txt = txt.replace(/^\d+[.)]\s+/, '');
        cnt.h++; out.push('<h' + lv + '>' + inline(txt) + '</h' + lv + '>'); continue;
      }
      if (/^\s{0,3}([-*_])(\s*\1){2,}\s*$/.test(l)){ out.push('<hr>'); i++; continue; }
      if (/^\s*>/.test(l)){ var q = []; while (i < lines.length && /^\s*>/.test(lines[i])){ q.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
        out.push('<blockquote>\n' + convert(q.join('\n'), {}) + '\n</blockquote>'); continue; }
      if (/^\s*([-*+]|\d+[.)])\s+/.test(l)){ var r = parseList(lines, i); out.push(r.html); i = r.i; continue; }
      if (l.indexOf('|') > -1 && i + 1 < lines.length && isTableSep(lines[i + 1])){
        var head = cells(l), al = cells(lines[i + 1]).map(function(x){ return /^:-+:$/.test(x) ? 'center' : /-:$/.test(x) ? 'right' : /^:-/.test(x) ? 'left' : ''; });
        i += 2; var body = [];
        while (i < lines.length && lines[i].indexOf('|') > -1 && lines[i].trim()){ body.push(cells(lines[i])); i++; }
        var td = function(tag, x, k){ return '<' + tag + (al[k] ? ' style="text-align:' + al[k] + '"' : '') + '>' + inline(x || '') + '</' + tag + '>'; };
        cnt.t++;
        out.push('<table>\n  <thead>\n    <tr>' + head.map(function(x, k){ return td('th', x, k); }).join('') + '</tr>\n  </thead>\n  <tbody>\n' +
          body.map(function(r){ return '    <tr>' + head.map(function(_, k){ return td('td', r[k], k); }).join('') + '</tr>'; }).join('\n') + '\n  </tbody>\n</table>');
        continue;
      }
      var para = [];
      while (i < lines.length && lines[i].trim() && !/^\s{0,3}(#{1,6}\s|>|```|~~~)/.test(lines[i]) && !/^\s*([-*+]|\d+[.)])\s+/.test(lines[i]) && !(lines[i].indexOf('|') > -1 && i + 1 < lines.length && isTableSep(lines[i + 1]))){
        if (para.length && /^\s*(=+|-+)\s*$/.test(lines[i])) break;
        para.push(lines[i]); i++;
      }
      if (!para.length){ para.push(lines[i]); i++; }
      out.push('<p>' + inline(para.map(function(x){ return x.replace(/^\s+/, ''); }).join('\n')).replace(/\n/g, ' ').replace(/<br> /g, '<br>\n') + '</p>');
    }
    return out.join('\n');
  }
  var mode = 'code';
  function run(){
    cnt = {h: 0, l: 0, t: 0, a: 0}; NEW = $('mhNew').checked;
    var html = convert($('mhIn').value, {h1: $('mhH1').checked, shift: $('mhShift').checked, num: $('mhNum').checked});
    $('mhOut').textContent = html || 'Paste some Markdown to convert.';
    $('mhView').innerHTML = html;
    $('mhView').querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(e){ e.preventDefault(); }); });
    $('mhView').querySelectorAll('table').forEach(function(t){ t.className = 'lim'; });
    $('mhHs').textContent = cnt.h; $('mhLs').textContent = cnt.l; $('mhTs').textContent = cnt.t; $('mhAs').textContent = cnt.a;
    $('mhOut').style.display = mode === 'code' ? 'block' : 'none'; $('mhView').style.display = mode === 'view' ? 'block' : 'none';
    return html;
  }
  document.querySelectorAll('#mhTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#mhTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); mode = b.getAttribute('data-m'); run(); }); });
  $('mhForm').addEventListener('input', run); $('mhForm').addEventListener('change', run);
  $('mhCopy').addEventListener('click', function(){ copyText(run(), 'toast'); });
  $('mhDl').addEventListener('click', function(){ download('content.html', run(), 'text/html'); });
  run();
''',
        content=f'''
    <h2>What Is a Markdown to HTML Converter?</h2>
    <p>ChatGPT, Claude, Gemini and most AI writing tools format their answers in Markdown. That is why copied text often arrives full of <code>##</code>, <code>**</code> and <code>|</code> symbols, or loses its headings and tables when you paste it into WordPress.</p>
    <p>A Markdown to HTML converter turns those symbols into real HTML tags: <code>&lt;h2&gt;</code> headings, <code>&lt;ul&gt;</code> and <code>&lt;ol&gt;</code> lists, <code>&lt;table&gt;</code> tables, links and bold text. The result keeps your page structure, which helps readers, search engines and AI crawlers understand it. The conversion happens in your browser.</p>

    <h2>How to Use the Converter</h2>
    <ol>
      <li><strong>Copy the AI answer as Markdown.</strong> In ChatGPT or Claude, use the copy button under the reply, which copies Markdown.</li>
      <li><strong>Paste it</strong> into the Markdown box.</li>
      <li><strong>Pick your options.</strong> Remove the first H1 if your CMS adds the title, turn H1s into H2s, open external links in a new tab, or strip step numbers from headings.</li>
      <li><strong>Check the Preview tab</strong> to see how it will look.</li>
      <li><strong>Copy the HTML</strong> and paste it into a Custom HTML block or your editor's code view.</li>
    </ol>

    <h2>Supported Markdown</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('You write', 'You get')}
      <tbody>
        <tr><td><code># Title</code> to <code>###### Title</code></td><td><code>&lt;h1&gt;</code> to <code>&lt;h6&gt;</code></td></tr>
        <tr><td><code>**bold**</code>, <code>*italic*</code>, <code>~~struck~~</code></td><td><code>&lt;strong&gt;</code>, <code>&lt;em&gt;</code>, <code>&lt;del&gt;</code></td></tr>
        <tr><td><code>- item</code> or <code>1. item</code>, with nesting</td><td><code>&lt;ul&gt;</code> or <code>&lt;ol&gt;</code> with nested lists</td></tr>
        <tr><td>Pipe tables with <code>:---:</code> alignment</td><td><code>&lt;table&gt;</code> with a header row</td></tr>
        <tr><td><code>[text](url)</code> and <code>![alt](src)</code></td><td>Links and images</td></tr>
        <tr><td><code>&gt; quote</code> and fenced code blocks</td><td><code>&lt;blockquote&gt;</code> and <code>&lt;pre&gt;&lt;code&gt;</code></td></tr>
      </tbody>
    </table></div>
    <p>The converter follows <a href="https://github.github.com/gfm/" {EXT}>GitHub Flavored Markdown</a>, the same style AI chat tools use. Any raw HTML inside your Markdown is escaped, so pasted text can never add scripts to your page.</p>

    <h2>Tips for Publishing AI Drafts</h2>
    <ul>
      <li><strong>Keep one H1 per page.</strong> Most themes print the post title as the H1, so tick the option to remove or demote the one in your draft.</li>
      <li><strong>Check heading order.</strong> Headings should step down from H2 to H3 without skipping levels.</li>
      <li><strong>Review every link.</strong> AI tools sometimes invent URLs. Click each one before publishing.</li>
      <li><strong>Add your own value.</strong> Real examples, numbers and experience are what make an AI assisted page worth ranking.</li>
    </ul>

    <h2>Publish Content That Ranks</h2>
    <p>Get the structure right with <a href="{B}html-heading-structure-best-practices/">HTML heading structure best practices</a>, write for readers with <a href="{B}how-to-write-seo-friendly-blog/">how to write an SEO friendly blog</a>, and follow <a href="{B}google-ai-content-guidelines-2026/">Google's AI content guidelines</a>. If you only need plain text without any formatting, use the <a href="{T}ai-text-cleaner/">AI text cleaner</a>.</p>
''',
        faqs=[
            ("How do I paste ChatGPT text into WordPress without losing formatting?", "Copy the answer with ChatGPT's copy button, convert it here, then paste the HTML into a Custom HTML block or the code editor. Headings, lists, tables and links all come through as real HTML."),
            ("Why does my pasted AI text show ## and ** symbols?", "Those are Markdown formatting marks. Editors that do not understand Markdown show them as plain characters. Converting to HTML turns them into real headings and bold text."),
            ("Is the HTML safe to use on my site?", "Yes. Any HTML tags inside your Markdown are escaped rather than run, and links with unsafe schemes such as javascript are removed. The output only contains standard content tags."),
            ("Does it support tables and nested lists?", "Yes. Pipe tables with header rows and column alignment, nested bullet lists, numbered lists that start at any number, task list boxes, quotes and fenced code blocks are all supported."),
        ],
        related=[("HTML Heading Structure Best Practices", "html-heading-structure-best-practices"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"),
                 ("Google AI Content Guidelines 2026", "google-ai-content-guidelines-2026"), ("HTML Semantic Elements Explained", "html-semantic-elements-explained")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'ai-tools'; t['updated'] = '2026-11-06'
