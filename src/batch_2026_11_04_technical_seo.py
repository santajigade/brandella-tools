"""Batch 7 (2026-11-04): Technical SEO Tools category, 7 tools.
Facts checked 2026-11-04 against: Google "How Google interprets the robots.txt specification"
(developers.google.com/crawling/docs/robots-txt/robots-txt-spec: 500 KiB limit, user-agent/allow/disallow/sitemap only,
crawl-delay unsupported, most specific group, groups for same agent merged, longest match wins, tie goes to allow,
* and $ wildcards, case sensitive paths, percent encoded comparison, 4xx = no restrictions, 24h cache),
Google common crawlers (Googlebot-Image/Video/News fall back to Googlebot, Google-Extended does not affect Search),
OpenAI bots page (GPTBot training, OAI-SearchBot ChatGPT search), Anthropic help 8896518 (ClaudeBot, Claude-SearchBot,
Claude-User), Google "Build and submit a sitemap" (50MB or 50,000 URLs, UTF-8, absolute URLs, priority and changefreq
ignored, lastmod used if accurate, entity escaping), sitemaps.org protocol (namespace, loc under 2,048 chars, W3C Datetime,
changefreq values, priority 0.0 to 1.0, same host), Google "Localized versions of your pages" (ISO 639-1 + ISO 3166-1
alpha 2, ISO 15924 scripts, region alone invalid, UK/EU/UN reserved, es-419 not supported, return links required, self
reference, fully qualified URLs, xhtml namespace, Link header format), Google "Redirects and Google Search" (301/308
permanent, 302/303/307 temporary) and Apache mod_alias docs (Redirect is a prefix match that appends the rest of the
path, RedirectMatch uses a regex, first match wins, query strings are kept)."""
import html as _h

T = 'https://brandella.in/tools/technical-seo-tools/'
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
SCROLL = 'style="overflow-x:auto;max-height:460px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px"'

BASEJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function issues(id, list, okMsg, max){
    max = max || 40;
    var bad = list.filter(function(i){ return i[0] === 'bad'; }), warn = list.filter(function(i){ return i[0] === 'warn'; });
    var li = function(a){ var more = a.length > max ? '<li>and ' + (a.length - max) + ' more</li>' : '';
      return '<ul style="margin:6px 0 0 18px">' + a.slice(0, max).map(function(i){ return '<li>' + i[1] + '</li>'; }).join('') + more + '</ul>'; };
    if (bad.length) say(id, 'bad', '<strong>Fix ' + bad.length + ' issue' + (bad.length > 1 ? 's' : '') + (warn.length ? ', plus ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') : '') + '.</strong>' + li(bad.concat(warn)));
    else if (warn.length) say(id, 'warn', '<strong>Works, with ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') + '.</strong>' + li(warn));
    else say(id, 'ok', okMsg);
  }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
  function fmtN(n){ return Number(n).toLocaleString('en-IN'); }
  function bytes(s){ return new TextEncoder().encode(s).length; }
  function kb(n){ return n >= 1048576 ? (n / 1048576).toFixed(1) + ' MB' : n >= 1024 ? (n / 1024).toFixed(1) + ' KB' : n + ' B'; }
  function xesc(s){ return String(s).replace(/[&<>"']/g, function(ch){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[ch]; }); }
  function download(name, text, type){
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: (type || 'text/plain') + ';charset=utf-8'}));
    a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
  }
  function absUrl(s){ try { var u = new URL(s); return /^https?:$/.test(u.protocol) ? u : null; } catch(e){ return null; } }
'''

# ---------- ISO code lists shared by both hreflang tools ----------
LANGJS = r'''
  var LANGS = 'aa ab ae af ak am an ar as av ay az ba be bg bi bm bn bo br bs ca ce ch co cr cs cu cv cy da de dv dz ee el en eo es et eu fa ff fi fj fo fr fy ga gd gl gn gu gv ha he hi ho hr ht hu hy hz ia id ie ig ii ik io is it iu ja jv ka kg ki kj kk kl km kn ko kr ks ku kv kw ky la lb lg li ln lo lt lu lv mg mh mi mk ml mn mr ms mt my na nb nd ne ng nl nn no nr nv ny oc oj om or os pa pi pl ps pt qu rm rn ro ru rw sa sc sd se sg si sk sl sm sn so sq sr ss st su sv sw ta te tg th ti tk tl tn to tr ts tt tw ty ug uk ur uz ve vi vo wa wo xh yi yo za zh zu'.split(' ');
  var REGIONS = 'AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW'.split(' ');
  var SCRIPTS = {Hans: 'Simplified', Hant: 'Traditional', Latn: 'Latin', Cyrl: 'Cyrillic', Arab: 'Arabic', Deva: 'Devanagari', Beng: 'Bengali', Guru: 'Gurmukhi'};
  var LSET = new Set(LANGS), RSET = new Set(REGIONS);
  var DNL = null, DNR = null;
  try { DNL = new Intl.DisplayNames(['en'], {type: 'language'}); DNR = new Intl.DisplayNames(['en'], {type: 'region'}); } catch(e){}
  function lname(code){ try { return DNL ? DNL.of(code) : code; } catch(e){ return code; } }
  function rname(code){ try { return DNR ? DNR.of(code) : code; } catch(e){ return code; } }
  var RESERVED = {UK: 'GB', EU: '', UN: ''};
  var CONFUSE = {be: 'Belgium', ca: 'Canada', se: 'Sweden', kr: 'South Korea', ch: 'Switzerland', ae: 'the United Arab Emirates', dz: 'Algeria', cr: 'Costa Rica'};
  // Returns {ok, code, label, err, warn}
  function checkCode(raw){
    var s = String(raw || '').trim();
    if (!s) return {ok: false, err: 'The hreflang value is empty.'};
    if (/^x-default$/i.test(s)) return {ok: true, code: 'x-default', label: 'Fallback for everyone else'};
    if (/_/.test(s)) return {ok: false, err: c(s) + ' uses an underscore. Use a hyphen, like ' + c(s.replace(/_/g, '-')) + '.'};
    var p = s.split('-'), lang = p[0].toLowerCase(), out = {ok: true, code: s};
    if (!LSET.has(lang)){
      if (RSET.has(lang.toUpperCase()) || lang === 'uk') return {ok: false, err: c(s) + ' looks like a country code on its own. Google needs a language first, like ' + c('en-' + (RESERVED[lang.toUpperCase()] || lang.toUpperCase())) + '.'};
      if (lang.length === 3) return {ok: false, err: c(s) + ' uses a three letter language code. Google expects the two letter ISO 639 1 code.'};
      return {ok: false, err: c(s) + ' is not a valid language code.'};
    }
    var label = lname(lang), i = 1;
    if (p[i] && /^[A-Za-z]{4}$/.test(p[i])){
      var sc = p[i][0].toUpperCase() + p[i].slice(1).toLowerCase();
      label += ' (' + (SCRIPTS[sc] || sc) + ')'; i++;
      if (!SCRIPTS[sc]) out.warn = c(s) + ' uses the script ' + c(sc) + '. Check it is a real ISO 15924 script code.';
    }
    if (p[i]){
      var r = p[i].toUpperCase();
      if (/^\d{3}$/.test(r)) return {ok: false, err: c(s) + ' uses a numeric region. Google does not support codes like ' + c('es-419') + '. List each country instead, like ' + c('es-MX') + '.'};
      if (r in RESERVED) return {ok: false, err: c(s) + ' uses the reserved code ' + c(r) + ', which Google ignores.' + (RESERVED[r] ? ' Use ' + c(lang + '-' + RESERVED[r]) + ' for the United Kingdom.' : ' List each country separately.')};
      if (!RSET.has(r)) return {ok: false, err: c(s) + ' has an unknown country code ' + c(r) + '.'};
      label += ', ' + rname(r); i++;
    } else if (CONFUSE[lang]) {
      out.warn = c(s) + ' means ' + esc(lname(lang)) + ' language, not ' + CONFUSE[lang] + '. If you meant the country, add a language, like ' + c('en-' + lang.toUpperCase()) + '.';
    }
    if (p.length > i) return {ok: false, err: c(s) + ' has extra parts Google does not use. Use language, optional script and optional country only.'};
    out.label = label; return out;
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. ROBOTS.TXT GENERATOR ----------
    AI_TRAIN = [('GPTBot', 'GPTBot', 'OpenAI model training', True), ('ClaudeBot', 'ClaudeBot', 'Anthropic model training', True),
                ('Google-Extended', 'Google-Extended', 'Gemini training and grounding, not Google Search', False),
                ('Applebot-Extended', 'Applebot-Extended', 'Apple AI training, not Apple search', False),
                ('CCBot', 'CCBot', 'Common Crawl, a public dataset used to train many AI models', True)]
    AI_SEARCH = [('OAI-SearchBot', 'OAI-SearchBot', 'ChatGPT search results'), ('Claude-SearchBot', 'Claude-SearchBot', 'Claude search results'),
                 ('PerplexityBot', 'PerplexityBot', 'Perplexity answers')]
    def aick(k, name, note, on=False):
        return f'<label class="check"><input type="checkbox" class="rgAi" value="{k}"' + (' checked' if on else '') + f'> <span><code>{name}</code> <em style="font-weight:400;color:#666">{note}</em></span></label>'
    TOOLS.append(dict(
        slug='robots-txt-generator', short='RG', name='Robots.txt Generator',
        card='Create a clean robots.txt file with blocked folders, sitemaps and AI crawler rules, checked as you type.',
        title='Robots.txt Generator: Free Tool With AI Bot Rules',
        desc='Free robots.txt generator. Block folders, allow exceptions, add sitemaps and choose which AI crawlers like GPTBot may use your site. Follows Google rules.',
        h1='Robots.txt Generator',
        lead='Choose what crawlers may visit, add your sitemap and decide which AI bots can use your content. The tool writes a valid robots.txt file and warns you about rules that could hurt your rankings.',
        tool='''<section class="tool" aria-label="Robots.txt generator" id="rgForm">
    <div class="card" style="min-width:0">
      <h2>Your Rules</h2>
      ''' + F('rgDefault', 'All Search Engines', 'allow', tag='select', opts=[('allow', 'Allow crawling, except the paths below'), ('block', 'Block the whole site (staging or test sites only)')]) + '''
      ''' + F('rgDis', 'Paths to Block', '/wp-admin/\n/cart/\n/checkout/\n/my-account/\n/*?s=\n/*?add-to-cart=', em='one per line', tag='textarea', mono=True) + '''
      ''' + F('rgAllow', 'Exceptions to Allow', '/wp-admin/admin-ajax.php', em='one per line', tag='textarea', mono=True) + '''
      ''' + F('rgMap', 'Sitemap URLs', 'https://www.example.com/sitemap_index.xml', em='one per line', tag='textarea', mono=True) + '''
      <div class="field"><label>AI Training Crawlers to Block</label>''' + ''.join(aick(k, n, d, on) for k, n, d, on in AI_TRAIN) + '''</div>
      <div class="field"><label>AI Search Crawlers to Block <em>blocking these removes you from their answers</em></label>''' + ''.join(aick(k, n, d) for k, n, d in AI_SEARCH) + '''</div>
      ''' + F('rgOther', 'Other Bots to Block Completely', '', em='one user agent per line', tag='textarea', mono=True, ph='AhrefsBot\nSemrushBot') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your robots.txt</h2>
      <div class="stats">''' + S('rgLines', 'Lines') + S('rgGroups', 'Groups') + S('rgSize', 'Size') + '''</div>
      <div class="kw-result" id="rgCheck"></div>
      <pre class="code-out" id="rgOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="rgCopy">Copy robots.txt</button><button class="btn" id="rgDl">Download File</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Before you upload</strong><ul><li>The file must sit at the root, for example <code>https://www.example.com/robots.txt</code></li><li>Each subdomain needs its own file</li><li>Blocking a page stops crawling, not indexing. Use <code>noindex</code> to keep a page out of Google</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var out = '';
  function lines(id){ return v(id).split(/\r?\n/).map(function(s){ return s.trim(); }).filter(Boolean); }
  function cleanPath(p, iss, kind){
    var u = absUrl(p);
    if (u){ var np = u.pathname + u.search; iss.push(['warn', 'Turned the full URL ' + c(p) + ' into the path ' + c(np) + '. Rules only use the path.']); p = np; }
    if (!/^[\/*]/.test(p)){ iss.push(['bad', kind + ' path ' + c(p) + ' must start with ' + c('/') + ', for example ' + c('/' + p.replace(/^\.?\/*/, '')) + '.']); return null; }
    if (/\s/.test(p)) iss.push(['warn', c(p) + ' contains a space. Write it as ' + c(p.replace(/\s/g, '%20')) + '.']);
    return p;
  }
  function gen(){
    var iss = [], L = [], groups = 0, seen = {};
    var dis = [], allow = [];
    lines('rgDis').forEach(function(p){ p = cleanPath(p, iss, 'Blocked'); if (p && !seen['d' + p]){ seen['d' + p] = 1; dis.push(p); } });
    lines('rgAllow').forEach(function(p){ p = cleanPath(p, iss, 'Allowed'); if (p && !seen['a' + p]){ seen['a' + p] = 1; allow.push(p); } });
    var maps = lines('rgMap'), block = $('rgDefault').value === 'block';
    var host = '';
    maps.forEach(function(m){ var u = absUrl(m); if (!u) iss.push(['bad', 'The sitemap ' + c(m) + ' must be a full URL starting with ' + c('https://') + '.']); else if (!host) host = u.host; });
    L.push('# robots.txt' + (host ? ' for ' + host : ''));
    L.push('# Rules for every crawler'); L.push('User-agent: *');
    if (block){ L.push('Disallow: /'); iss.push(['warn', 'Your whole site is blocked for every crawler. Only use this on a staging or test site, never on a live site you want in Google.']); }
    else {
      dis.forEach(function(p){ L.push('Disallow: ' + p); });
      if (dis.indexOf('/') > -1) iss.push(['warn', c('Disallow: /') + ' blocks your whole site for every crawler.']);
    }
    allow.forEach(function(p){ L.push('Allow: ' + p); });
    if (!block && !dis.length && !allow.length) L.push('Allow: /');
    groups++;
    dis.forEach(function(p){
      if (/^\/wp-(includes|content)\/?$/.test(p) || /\.(css|js)\$?$/.test(p)) iss.push(['warn', 'Blocking ' + c(p) + ' can hide CSS or JavaScript from Google, which it needs to render your pages.']);
    });
    var ai = Array.from(document.querySelectorAll('.rgAi:checked')).map(function(x){ return x.value; });
    var search = ['OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot'];
    var tr = ai.filter(function(a){ return search.indexOf(a) < 0; }), se = ai.filter(function(a){ return search.indexOf(a) > -1; });
    if (tr.length){ L.push(''); L.push('# AI training crawlers'); tr.forEach(function(a){ L.push('User-agent: ' + a); }); L.push('Disallow: /'); groups++; }
    if (se.length){ L.push(''); L.push('# AI search crawlers'); se.forEach(function(a){ L.push('User-agent: ' + a); }); L.push('Disallow: /'); groups++;
      iss.push(['warn', 'You are blocking ' + se.map(c).join(', ') + '. Your pages can no longer be shown or cited in those AI search answers.']); }
    var oth = lines('rgOther').filter(function(a){ if (!/^[A-Za-z_-]+$/.test(a)){ iss.push(['bad', c(a) + ' is not a valid user agent name. Use only letters, hyphens and underscores, like ' + c('AhrefsBot') + '.']); return false; } return true; });
    if (oth.some(function(a){ return /^googlebot$/i.test(a); })) iss.push(['warn', 'You are blocking ' + c('Googlebot') + ' completely, which removes your site from Google Search over time.']);
    if (oth.length){ L.push(''); L.push('# Other blocked bots'); oth.forEach(function(a){ L.push('User-agent: ' + a); }); L.push('Disallow: /'); groups++; }
    if (maps.length){ L.push(''); maps.forEach(function(m){ L.push('Sitemap: ' + m); }); }
    else iss.push(['warn', 'Add your sitemap URL so crawlers can find all your pages.']);
    out = L.join('\n') + '\n';
    var sz = bytes(out);
    if (sz > 512000) iss.push(['bad', 'The file is over 500 KiB. Google ignores everything after that limit.']);
    $('rgOut').textContent = out; $('rgLines').textContent = L.length; $('rgGroups').textContent = groups; $('rgSize').textContent = kb(sz);
    issues('rgCheck', iss, '<strong>Valid robots.txt.</strong> Upload it to the root of your site' + (host ? ' so it opens at ' + c('https://' + host + '/robots.txt') : '') + ', then test it with our robots.txt tester.');
  }
  $('rgForm').addEventListener('input', gen); $('rgForm').addEventListener('change', gen);
  $('rgCopy').onclick = function(){ copyText(out, 'toast'); };
  $('rgDl').onclick = function(){ download('robots.txt', out); };
  gen();
''',
        content='''
    <h2>What Is a Robots.txt File?</h2>
    <p>A robots.txt file is a plain text file at the root of your site that tells crawlers which pages they may visit. Search engines read it before they crawl, so a good file keeps bots away from carts, admin screens and endless search result pages, and points them at your sitemap instead.</p>
    <p>It is also the place where you decide which AI crawlers can use your content. You can block bots that collect text for AI training while still letting AI search tools show and cite your pages.</p>

    <h2>How to Use the Robots.txt Generator</h2>
    <ol>
      <li><strong>Choose the default.</strong> Live sites should allow crawling. Block the whole site only on staging copies.</li>
      <li><strong>List paths to block</strong>, one per line. Use <code>*</code> to match any characters and <code>$</code> to match the end of a URL.</li>
      <li><strong>Add exceptions</strong> for files inside a blocked folder that crawlers still need.</li>
      <li><strong>Paste your sitemap URL</strong>, or several if you have more than one.</li>
      <li><strong>Tick the AI crawlers</strong> you want to keep out, then copy or download the file and upload it to your site root.</li>
    </ol>

    <h2>Robots.txt Rules Google Follows</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Rule', 'What it does') + '''
      <tbody>
        <tr><td><code>User-agent</code></td><td>Starts a group of rules for one crawler, or <code>*</code> for all of them</td></tr>
        <tr><td><code>Disallow</code></td><td>Blocks paths that start with the value. Paths are case sensitive</td></tr>
        <tr><td><code>Allow</code></td><td>Opens a path inside a blocked folder. The longest matching rule wins</td></tr>
        <tr><td><code>Sitemap</code></td><td>Full URL of a sitemap. You can list as many as you need</td></tr>
        <tr><td><code>Crawl-delay</code></td><td>Not supported by Google, so this tool leaves it out</td></tr>
      </tbody>
    </table></div>
    <p>A crawler only follows the most specific group that names it. If you add a group for <code>Googlebot</code>, it ignores the <code>*</code> group completely, so repeat any rules it should still obey. Google explains this in <a href="https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec" ''' + EXT + '''>how Google interprets robots.txt</a>.</p>

    <h2>Tips for a Safe Robots.txt</h2>
    <ul>
      <li><strong>Do not use it to hide pages from Google.</strong> A blocked URL can still be indexed from links. Use a <code>noindex</code> tag and leave the page crawlable.</li>
      <li><strong>Never block CSS or JavaScript</strong> your pages need, or Google cannot render them properly.</li>
      <li><strong>Block crawl traps</strong> like internal search, filters and add to cart links that create endless URLs.</li>
      <li><strong>AI choices are separate.</strong> Blocking <code>Google-Extended</code> or <code>GPTBot</code> does not change your Google rankings.</li>
    </ul>

    <h2>Learn More About Crawling</h2>
    <p>Our <a href="''' + B + '''robots-txt-complete-guide/">complete robots.txt guide</a> covers every rule in depth, <a href="''' + B + '''crawl-budget-explained/">crawl budget explained</a> shows why blocking waste matters on big sites, and <a href="''' + B + '''google-ai-search-opt-out/">opting out of Google AI search</a> walks through your AI choices. Already have a file? Check it with the <a href="''' + T + '''robots-txt-tester/">robots.txt tester</a>.</p>
''',
        faqs=[
            ("Where do I put my robots.txt file?", "Upload it to the root folder of your site so it opens at yourdomain.com/robots.txt. Crawlers never look for it in subfolders, and every subdomain needs its own file."),
            ("Does blocking AI crawlers hurt my Google rankings?", "No. Google Extended, GPTBot, ClaudeBot and CCBot are separate from Googlebot, so blocking them does not change how Google Search crawls or ranks your pages."),
            ("Will robots.txt remove a page from Google?", "No. It only stops crawling. A blocked page can still appear in results if other sites link to it. To remove a page, allow crawling and add a noindex meta tag."),
            ("Should I block wp admin in WordPress?", "Blocking the wp admin folder is common and safe, as long as you allow the admin ajax file inside it, which some themes and plugins load on public pages."),
        ],
        related=[("Robots.txt Complete Guide", "robots-txt-complete-guide"), ("Crawl Budget Explained", "crawl-budget-explained"),
                 ("Google AI Search Opt Out", "google-ai-search-opt-out"), ("Dynamic Robots.txt in PHP", "dynamic-robots-txt-php")],
    ))

    # ---------- 2. ROBOTS.TXT TESTER ----------
    RT_SAMPLE = '''# Sample robots.txt, paste your own
User-agent: *
Disallow: /cart/
Disallow: /*?sort=
Disallow: /*.pdf$
Allow: /cart/help/
Crawl-delay: 5

User-agent: Googlebot
Disallow: /private/
Allow: /

User-agent: GPTBot
Disallow: /

Sitemap: https://www.example.com/sitemap.xml'''
    RT_URLS = '''https://www.example.com/cart/
https://www.example.com/cart/help/returns/
/shop/shoes/?sort=price
/files/price-list.pdf
/files/price-list.pdf?v=2
/private/report.html
/blog/robots-txt-guide/'''
    agents = [('googlebot', 'Googlebot (Google Search)'), ('googlebot-image', 'Googlebot Image'), ('googlebot-news', 'Googlebot News'),
              ('bingbot', 'Bingbot (Bing)'), ('gptbot', 'GPTBot (OpenAI training)'), ('oai-searchbot', 'OAI SearchBot (ChatGPT search)'),
              ('claudebot', 'ClaudeBot (Anthropic training)'), ('google-extended', 'Google Extended (Gemini)'), ('perplexitybot', 'PerplexityBot'),
              ('*', 'Any other crawler'), ('custom', 'Custom user agent')]
    TOOLS.append(dict(
        slug='robots-txt-tester', short='RT', name='Robots.txt Tester',
        card='Paste a robots.txt file and test which URLs Googlebot, Bingbot or AI crawlers may crawl, rule by rule.',
        title='Robots.txt Tester: Check if a URL Is Blocked',
        desc='Free robots.txt tester and validator. Paste your file, pick Googlebot or an AI crawler and see which URLs are allowed or blocked, and by which exact rule.',
        h1='Robots.txt Tester',
        lead='Paste any robots.txt file, choose a crawler and test a list of URLs. You see whether each one is allowed or blocked, the exact rule that decided it, and any lines Google ignores.',
        tool='''<section class="tool" aria-label="Robots.txt tester" id="rtForm">
    <div class="card" style="min-width:0">
      <h2>Robots.txt File</h2>
      ''' + F('rtFile', 'Paste robots.txt', RT_SAMPLE, tag='textarea', mono=True, extra=' style="min-height:330px"') + '''
      ''' + R2(F('rtAgent', 'Crawler', 'googlebot', tag='select', opts=agents), F('rtCustom', 'Custom User Agent', 'AhrefsBot', mono=True)) + '''
      ''' + F('rtUrls', 'URLs or Paths to Test', RT_URLS, em='one per line', tag='textarea', mono=True, extra=' style="min-height:170px"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Test Results</h2>
      <div class="stats">''' + S('rtOk', 'Allowed') + S('rtNo', 'Blocked') + S('rtRules', 'Rules Used') + '''</div>
      <div class="kw-result" id="rtGroup"></div>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>URL</th><th>Result</th><th>Deciding rule</th></tr></thead><tbody id="rtBody"></tbody></table></div>
      <h3 style="font-size:16px;margin:18px 0 10px">File Check</h3>
      <div class="kw-result" id="rtCheck"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var FAM = {'googlebot-image': ['googlebot-image', 'googlebot'], 'googlebot-news': ['googlebot-news', 'googlebot'], 'googlebot-video': ['googlebot-video', 'googlebot']};
  function norm(s){
    s = String(s).replace(/%[0-9a-fA-F]{2}/g, function(m){ return m.toUpperCase(); });
    return s.replace(/[^\x21-\x7e]+/g, function(m){ try { return encodeURIComponent(m); } catch(e){ return m; } });
  }
  function toRe(p){
    var end = /\$$/.test(p); if (end) p = p.slice(0, -1);
    var r = p.split('*').map(function(x){ return x.replace(/[.+?^${}()|[\]\\]/g, '\\$&'); }).join('.*');
    return new RegExp('^' + r + (end ? '$' : ''));
  }
  function parse(txt){
    var groups = [], cur = null, lastUA = false, warn = [], maps = [], n = 0;
    if (bytes(txt) > 512000) warn.push(['bad', 'This file is over 500 KiB. Google ignores every rule after that limit.']);
    txt.split(/\r\n|\r|\n/).forEach(function(raw){
      n++; var line = raw.replace(/#.*$/, '').trim(); if (!line) return;
      var m = line.match(/^([A-Za-z][A-Za-z -]*?)\s*:\s*(.*)$/);
      if (!m){ warn.push(['warn', 'Line ' + n + ' ' + c(raw.trim()) + ' is not a valid rule and is ignored. Rules look like ' + c('Disallow: /path') + '.']); return; }
      var k = m[1].toLowerCase().replace(/\s+/g, '-'), val = m[2].trim();
      if (k === 'user-agent' || k === 'useragent'){
        if (!lastUA || !cur){ cur = {agents: [], names: {}, rules: [], line: n}; groups.push(cur); }
        var tok = val === '*' ? '*' : ((val.match(/^[A-Za-z_-]+/) || [''])[0].toLowerCase());
        if (!tok) warn.push(['warn', 'Line ' + n + ' has an empty or invalid user agent.']);
        else { cur.agents.push(tok); cur.names[tok] = val === '*' ? '*' : (val.match(/^[A-Za-z_-]+/) || [tok])[0]; }
        lastUA = true; return;
      }
      lastUA = false;
      if (k === 'allow' || k === 'disallow'){
        if (!cur){ warn.push(['bad', 'Line ' + n + ' ' + c(raw.trim()) + ' comes before any ' + c('User-agent') + ' line, so crawlers ignore it.']); return; }
        if (!val){ if (k === 'disallow') cur.rules.push({type: 'disallow', path: '', line: n, empty: true}); return; }
        if (!/^[\/*]/.test(val)){ warn.push(['bad', 'Line ' + n + ': the path ' + c(val) + ' must start with ' + c('/') + '. It is ignored.']); return; }
        cur.rules.push({type: k, path: val, line: n, re: toRe(norm(val)), len: norm(val).length});
        if (k === 'disallow' && val === '/' && cur.agents.indexOf('*') > -1) warn.push(['warn', 'Line ' + n + ' blocks the whole site for every crawler that has no group of its own.']);
        return;
      }
      if (k === 'sitemap'){ maps.push(val); if (!absUrl(val)) warn.push(['bad', 'Line ' + n + ': the sitemap must be a full URL, like ' + c('https://www.example.com/sitemap.xml') + '.']); return; }
      if (k === 'crawl-delay'){ warn.push(['warn', 'Line ' + n + ': Google ignores ' + c('Crawl-delay') + '. Some other crawlers may still read it.']); return; }
      if (k === 'noindex' || k === 'nofollow'){ warn.push(['bad', 'Line ' + n + ': ' + c(m[1] + ':') + ' is not supported in robots.txt. Use a robots meta tag or the ' + c('X-Robots-Tag') + ' header.']); return; }
      if (k === 'host' || k === 'clean-param'){ warn.push(['warn', 'Line ' + n + ': ' + c(m[1]) + ' is not a standard rule. Google ignores it.']); return; }
      warn.push(['warn', 'Line ' + n + ': ' + c(m[1]) + ' is not a rule Google understands, so it is ignored. Check the spelling.']);
    });
    return {groups: groups, warn: warn, maps: maps};
  }
  function pick(groups, agent){
    var chain = agent === '*' ? [] : (FAM[agent] || [agent]);
    for (var i = 0; i < chain.length; i++){
      var g = groups.filter(function(x){ return x.agents.indexOf(chain[i]) > -1; });
      if (g.length) return {token: chain[i], groups: g};
    }
    var s = groups.filter(function(x){ return x.agents.indexOf('*') > -1; });
    return s.length ? {token: '*', groups: s} : null;
  }
  function decide(rules, path){
    if (path === '/robots.txt') return {allowed: true, rule: null, note: 'robots.txt itself is always allowed'};
    var target = norm(path), best = null;
    rules.forEach(function(r){
      if (r.empty || !r.re.test(target)) return;
      if (!best || r.len > best.len || (r.len === best.len && r.type === 'allow' && best.type === 'disallow')) best = r;
    });
    return {allowed: !best || best.type === 'allow', rule: best};
  }
  function run(){
    var P = parse($('rtFile').value), sel = $('rtAgent').value;
    $('rtCustom').parentNode.style.display = sel === 'custom' ? '' : 'none';
    var agent = sel === 'custom' ? ((v('rtCustom').match(/^[A-Za-z_-]+/) || ['*'])[0].toLowerCase()) : sel;
    var g = pick(P.groups, agent), rules = g ? [].concat.apply([], g.groups.map(function(x){ return x.rules; })) : [];
    var nm = sel === 'custom' ? agent : $('rtAgent').selectedOptions[0].textContent;
    if (!P.groups.length) say('rtGroup', 'warn', 'No ' + c('User-agent') + ' groups found, so every URL is allowed.');
    else if (!g) say('rtGroup', 'ok', '<strong>' + esc(nm) + '</strong> has no matching group, so it may crawl everything.');
    else {
      var lines = g.groups.map(function(x){ return x.line; }).join(' and ');
      var note = g.token === '*' ? 'It has no group of its own, so it follows the ' + c('User-agent: *') + ' group on line ' + lines + '.'
        : 'It follows the ' + c('User-agent: ' + (g.groups[0].names[g.token] || g.token)) + ' group on line ' + lines + (g.groups.length > 1 ? ' (groups merged)' : '') + ' and ignores every other group' + (P.groups.some(function(x){ return x.agents.indexOf('*') > -1; }) ? ', including ' + c('*') : '') + '.';
      say('rtGroup', '', '<strong>' + esc(nm) + '</strong>: ' + note);
    }
    var ok = 0, no = 0, used = {}, rows = [];
    v('rtUrls').split(/\r?\n/).map(function(s){ return s.trim(); }).filter(Boolean).forEach(function(raw){
      var path;
      var u = absUrl(raw);
      if (u) path = u.pathname + u.search;
      else if (/^\//.test(raw)) path = raw;
      else { rows.push('<tr><td>' + esc(raw) + '</td><td style="color:#c47a00;font-weight:700">Check</td><td>Enter a full URL or a path starting with /</td></tr>'); return; }
      var d = decide(rules, path);
      if (d.allowed) ok++; else no++;
      if (d.rule) used[d.rule.line] = 1;
      var why = d.rule ? '<code>' + esc((d.rule.type === 'allow' ? 'Allow: ' : 'Disallow: ') + d.rule.path) + '</code> line ' + d.rule.line : (d.note ? esc(d.note) : 'No rule matches');
      rows.push('<tr><td style="word-break:break-all">' + esc(raw) + '</td><td style="font-weight:700;color:' + (d.allowed ? '#2f7a0c' : '#d1351f') + '">' + (d.allowed ? 'Allowed' : 'Blocked') + '</td><td>' + why + '</td></tr>');
    });
    $('rtBody').innerHTML = rows.join('') || '<tr><td colspan="3" class="empty">Add a URL or path to test.</td></tr>';
    $('rtOk').textContent = ok; $('rtNo').textContent = no; $('rtRules').textContent = Object.keys(used).length;
    var w = P.warn.slice();
    if (!P.maps.length) w.push(['warn', 'No ' + c('Sitemap') + ' line found. Adding one helps crawlers find your pages.']);
    issues('rtCheck', w, '<strong>No problems found.</strong> Every line in this file is valid for Google.');
  }
  $('rtForm').addEventListener('input', run); $('rtForm').addEventListener('change', run);
  run();
''',
        content='''
    <h2>What Does a Robots.txt Tester Do?</h2>
    <p>A robots.txt tester tells you whether a crawler is allowed to visit a URL on your site. It reads your file the same way Google does: it picks the right group for the crawler, compares every rule with the URL, and lets the most specific rule decide.</p>
    <p>Google Search Console no longer has its old robots.txt tester, so a quick private check like this is the fastest way to catch a rule that blocks pages you want in search. Everything runs in your browser, and nothing is fetched from your site.</p>

    <h2>How to Use the Robots.txt Tester</h2>
    <ol>
      <li><strong>Paste your robots.txt.</strong> Open <code>yourdomain.com/robots.txt</code> in a browser and copy the whole file.</li>
      <li><strong>Pick a crawler</strong>, such as Googlebot, Bingbot or an AI bot, or type a custom user agent.</li>
      <li><strong>List the URLs to test</strong>, one per line. Full URLs and paths both work.</li>
      <li><strong>Read the results.</strong> Each URL shows Allowed or Blocked and the line that decided it.</li>
      <li><strong>Fix the file check items</strong>, such as rules Google ignores or paths without a leading slash.</li>
    </ol>

    <h2>How Google Decides Which Rule Wins</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Situation', 'What happens') + '''
      <tbody>
        <tr><td>Crawler has its own group</td><td>It uses only that group and ignores <code>*</code></td></tr>
        <tr><td>Several groups name the same crawler</td><td>Their rules are merged into one</td></tr>
        <tr><td>Allow and Disallow both match</td><td>The longer, more specific path wins</td></tr>
        <tr><td>Two matching rules are the same length</td><td>Allow wins, as the least restrictive rule</td></tr>
        <tr><td><code>*</code> in a path</td><td>Matches any characters, including none</td></tr>
        <tr><td><code>$</code> at the end</td><td>The URL must end exactly there</td></tr>
        <tr><td>Upper and lower case</td><td>Paths are case sensitive, so <code>/Shop</code> and <code>/shop</code> differ</td></tr>
      </tbody>
    </table></div>
    <p>These are the rules in Google's <a href="https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec" ''' + EXT + '''>robots.txt specification</a>, which follows the RFC 9309 standard. Crawlers like <code>Googlebot-Image</code> fall back to the <code>Googlebot</code> group when they have none of their own, and the tester copies that behaviour.</p>

    <h2>Tips for Testing</h2>
    <ul>
      <li><strong>Test pages you want ranked</strong>, not only pages you meant to block. Accidental blocks are the costly mistake.</li>
      <li><strong>Include query strings.</strong> Rules like <code>/*?sort=</code> only match URLs with that parameter.</li>
      <li><strong>Check each crawler.</strong> A Googlebot group means Google skips your general rules, which surprises many site owners.</li>
      <li><strong>Remember the cache.</strong> Google usually caches robots.txt for up to a day, so changes take a little time to apply.</li>
    </ul>

    <h2>Go Further With Crawling</h2>
    <p>Learn how bots move through a site in <a href="''' + B + '''how-google-crawls-websites/">how Google crawls websites</a>, spot crawl problems in the <a href="''' + B + '''understanding-crawl-stats-report/">crawl stats report</a>, and confirm a live page with the <a href="''' + B + '''url-inspection-tool-diagnose-indexing-problems/">URL Inspection tool</a>. Need a new file? Build one with the <a href="''' + T + '''robots-txt-generator/">robots.txt generator</a>.</p>
''',
        faqs=[
            ("Why does Googlebot ignore my rules for all user agents?", "A crawler only follows the most specific group that names it. If your file has a Googlebot group, Google uses that group alone and skips the general group, so copy any shared rules into it."),
            ("Does a blocked URL disappear from Google?", "Not always. Google can still index a blocked URL without its content if other pages link to it. Use a noindex tag on a crawlable page to keep it out of results."),
            ("Is the tester the same as Google's?", "It follows Google's published rules for groups, wildcards and rule priority. For a final check on a live page, use the URL Inspection tool in Search Console."),
            ("Is my robots.txt sent anywhere?", "No. The file and URLs you paste are tested inside your browser. Nothing is uploaded or fetched from your site."),
        ],
        related=[("Robots.txt Complete Guide", "robots-txt-complete-guide"), ("How Google Crawls Websites", "how-google-crawls-websites"),
                 ("Understanding the Crawl Stats Report", "understanding-crawl-stats-report"), ("Meta Robots Tags Explained", "meta-robots-tags-explained")],
    ))

    # ---------- 3. XML SITEMAP GENERATOR ----------
    XS_SAMPLE = '''https://www.example.com/
https://www.example.com/about/ 2026-09-14
https://www.example.com/services/seo-audit/ 2026-10-30
https://www.example.com/blog/ 2026-11-02
https://www.example.com/blog/technical-seo-checklist/ 2026-11-02
/blog/core-web-vitals-guide/ 2026-10-21
/contact/
https://www.example.com/shop/?category=shoes&size=9
https://www.example.com/about/
https://www.example.com/pricing/#plans'''
    TOOLS.append(dict(
        slug='xml-sitemap-generator', short='XS', name='XML Sitemap Generator',
        card='Turn a list of URLs into a valid XML sitemap with lastmod dates, split files and a sitemap index.',
        title='XML Sitemap Generator: Free From a List of URLs',
        desc='Free XML sitemap generator. Paste your URLs, add lastmod dates and download a valid sitemap. Large lists are split into files with a sitemap index for you.',
        h1='XML Sitemap Generator',
        lead='Paste the pages you want in Google, one per line, and get a clean XML sitemap that follows the sitemaps.org protocol. Duplicates, fragments and bad URLs are fixed or flagged for you.',
        tool='''<section class="tool" aria-label="XML sitemap generator" id="xsForm">
    <div class="card" style="min-width:0">
      <h2>Your Pages</h2>
      ''' + F('xsUrls', 'URLs', XS_SAMPLE, em='one per line, date optional', tag='textarea', mono=True, extra=' style="min-height:270px"') + '''
      ''' + F('xsBase', 'Site Address', 'https://www.example.com', em='used for paths like /contact/', mono=True) + '''
      ''' + R2(F('xsLast', 'Last Modified Date', 'line', tag='select', opts=[('line', 'Only dates in my list'), ('today', 'Today for URLs without a date'), ('none', 'Leave out lastmod')]),
               F('xsMax', 'URLs per File', '50000', typ='number', extra=' min="1" max="50000"')) + '''
      ''' + CK('xsExtra', 'Add <code>changefreq</code> and <code>priority</code> (Google ignores both)', False) + '''
      ''' + CK('xsQuery', 'Keep URLs with query strings like <code>?sort=</code>', True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Sitemap</h2>
      <div class="stats">''' + S('xsCount', 'URLs') + S('xsSkip', 'Skipped') + S('xsFiles', 'Files') + S('xsSize', 'Size') + '''</div>
      <div class="kw-result" id="xsCheck"></div>
      <div class="field" id="xsPickRow" style="display:none"><label for="xsPick">Show File</label><select id="xsPick"></select></div>
      <pre class="code-out" id="xsOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="xsCopy">Copy XML</button><button class="btn" id="xsDl">Download This File</button><button class="btn" id="xsDlAll" style="display:none">Download All Files</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Next steps</strong><ul><li>Upload the file to your site root, for example <code>/sitemap.xml</code></li><li>Add a <code>Sitemap:</code> line to robots.txt</li><li>Submit it in Search Console under Sitemaps</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var files = [];
  function today(){ var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  var W3C = /^\d{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01])(T([01]\d|2[0-3]):[0-5]\d(:[0-5]\d(\.\d+)?)?(Z|[+-]([01]\d|2[0-3]):[0-5]\d))?)?)?$/;
  function prio(u){ var depth = u.pathname.split('/').filter(Boolean).length; return depth === 0 ? '1.0' : depth === 1 ? '0.8' : '0.6'; }
  function build(){
    var iss = [], seen = {}, list = [], skipped = 0, base = absUrl(v('xsBase')), host = null, protos = {}, mode = $('xsLast').value, extra = $('xsExtra').checked;
    if (!base) iss.push(['bad', 'The site address must be a full URL, like ' + c('https://www.example.com') + '.']);
    var frag = 0, dup = 0, qs = 0, badDate = 0;
    v('xsUrls').split(/\r?\n/).forEach(function(line, i){
      line = line.trim(); if (!line || line[0] === '#') return;
      var parts = line.split(/[\s,]+/), raw = parts[0], date = parts[1] || '', u = null;
      if (/^\//.test(raw) && base) u = absUrl(base.origin + raw);
      else if (/^https?:\/\//i.test(raw)) u = absUrl(raw);
      else if (base && /^[\w.-]+\.[a-z]{2,}(\/|$)/i.test(raw)) u = absUrl('https://' + raw);
      if (!u){ skipped++; iss.push(['bad', 'Line ' + (i + 1) + ': ' + c(line) + ' is not a URL, so it was skipped.']); return; }
      if (u.hash){ frag++; u.hash = ''; }
      if (u.search && !$('xsQuery').checked){ skipped++; qs++; return; }
      if (!host) host = u.host;
      if (u.host !== host){ skipped++; iss.push(['bad', c(u.href) + ' is on a different host than ' + c(host) + '. One sitemap can only list URLs from one host.']); return; }
      protos[u.protocol] = 1;
      var href = u.href;
      if (href.length > 2048){ skipped++; iss.push(['bad', 'A URL longer than 2,048 characters was skipped.']); return; }
      if (seen[href]){ dup++; return; }
      if (date && !W3C.test(date)){ badDate++; iss.push(['warn', 'Line ' + (i + 1) + ': ' + c(date) + ' is not a valid date. Use ' + c('YYYY-MM-DD') + '. The date was left out.']); date = ''; }
      if (!date && mode === 'today') date = today();
      if (mode === 'none') date = '';
      seen[href] = 1; list.push({u: u, href: href, date: date});
    });
    if (frag) iss.push(['warn', 'Removed the ' + c('#') + ' part from ' + frag + ' URL' + (frag > 1 ? 's' : '') + '. Search engines ignore fragments.']);
    if (dup) iss.push(['warn', 'Removed ' + dup + ' duplicate URL' + (dup > 1 ? 's' : '') + '.']);
    if (qs) iss.push(['warn', 'Skipped ' + qs + ' URL' + (qs > 1 ? 's' : '') + ' with query strings.']);
    if (Object.keys(protos).length > 1) iss.push(['warn', 'Your list mixes http and https URLs. List only the version you want in search.']);
    if (base && host && base.host !== host) iss.push(['warn', 'Your URLs are on ' + c(host) + ' but the site address is ' + c(base.host) + '. Check you are using the right domain.']);
    var withQ = list.filter(function(x){ return x.u.search; }).length;
    if (withQ) iss.push(['warn', withQ + ' URL' + (withQ > 1 ? 's have' : ' has') + ' a query string. Only list them if they are the canonical version of the page.']);
    var max = Math.max(1, Math.min(50000, Math.floor(+$('xsMax').value) || 50000));
    files = [];
    for (var s = 0; s < list.length; s += max){
      var chunk = list.slice(s, s + max), L = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'];
      chunk.forEach(function(x){
        L.push('  <url>'); L.push('    <loc>' + xesc(x.href) + '</loc>');
        if (x.date) L.push('    <lastmod>' + x.date + '</lastmod>');
        if (extra){ L.push('    <changefreq>weekly</changefreq>'); L.push('    <priority>' + prio(x.u) + '</priority>'); }
        L.push('  </url>');
      });
      L.push('</urlset>');
      files.push({name: list.length > max ? 'sitemap-' + (files.length + 1) + '.xml' : 'sitemap.xml', xml: L.join('\n') + '\n'});
    }
    if (files.length > 1 && host){
      var origin = list[0].u.origin, I = ['<?xml version="1.0" encoding="UTF-8"?>', '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'];
      files.forEach(function(f){ I.push('  <sitemap>'); I.push('    <loc>' + xesc(origin + '/' + f.name) + '</loc>'); I.push('    <lastmod>' + today() + '</lastmod>'); I.push('  </sitemap>'); });
      I.push('</sitemapindex>');
      files.unshift({name: 'sitemap-index.xml', xml: I.join('\n') + '\n', index: true});
      iss.push(['warn', 'Your list was split into ' + (files.length - 1) + ' sitemap files. Upload them all to your site root and submit ' + c('sitemap-index.xml') + '.']);
    }
    var total = files.reduce(function(a, f){ return a + bytes(f.xml); }, 0);
    files.forEach(function(f){ if (bytes(f.xml) > 52428800) iss.push(['bad', c(f.name) + ' is larger than 50 MB. Lower the URLs per file.']); });
    $('xsCount').textContent = fmtN(list.length); $('xsSkip').textContent = skipped; $('xsFiles').textContent = files.length; $('xsSize').textContent = kb(total);
    var pk = $('xsPick'), prev = pk.value;
    pk.innerHTML = files.map(function(f, i){ return '<option value="' + i + '">' + esc(f.name) + '</option>'; }).join('');
    if (prev && files[+prev]) pk.value = prev;
    $('xsPickRow').style.display = files.length > 1 ? '' : 'none'; $('xsDlAll').style.display = files.length > 1 ? '' : 'none';
    show();
    if (!list.length) iss.push(['bad', 'Add at least one URL.']);
    issues('xsCheck', iss, '<strong>Valid sitemap with ' + fmtN(list.length) + ' URL' + (list.length === 1 ? '' : 's') + '.</strong> Download it, upload it to your site root and submit it in Search Console.');
  }
  function show(){ var f = files[+$('xsPick').value || 0]; $('xsOut').textContent = f ? f.xml : ''; }
  $('xsForm').addEventListener('input', function(e){ if (e.target.id !== 'xsPick') build(); });
  $('xsForm').addEventListener('change', function(e){ if (e.target.id === 'xsPick') show(); else build(); });
  $('xsCopy').onclick = function(){ copyText($('xsOut').textContent, 'toast'); };
  $('xsDl').onclick = function(){ var f = files[+$('xsPick').value || 0]; if (f) download(f.name, f.xml, 'application/xml'); };
  $('xsDlAll').onclick = function(){ files.forEach(function(f, i){ setTimeout(function(){ download(f.name, f.xml, 'application/xml'); }, i * 400); }); };
  build();
''',
        content='''
    <h2>What Is an XML Sitemap?</h2>
    <p>An XML sitemap is a file that lists the pages on your site you want search engines to find. It does not guarantee indexing, but it helps Google discover new and updated pages faster, especially on large sites, new sites and pages with few internal links.</p>
    <p>Most sitemap generators crawl your site from their own servers. This one works the other way: you paste the URLs you already know you want indexed, for example from your CMS, a spreadsheet or a crawl export, and it builds the file in your browser.</p>

    <h2>How to Use the XML Sitemap Generator</h2>
    <ol>
      <li><strong>Paste your URLs</strong>, one per line. Add a date after a space if you know when the page last changed, like <code>2026-10-30</code>.</li>
      <li><strong>Set your site address</strong> so short paths like <code>/contact/</code> become full URLs.</li>
      <li><strong>Choose how to handle dates.</strong> Only add a date that reflects a real change to the page.</li>
      <li><strong>Check the warnings</strong> for duplicates, other domains and URLs with parameters.</li>
      <li><strong>Download the file</strong>, upload it to your site root and submit it in Search Console.</li>
    </ol>

    <h2>Sitemap Tags and Limits</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Item', 'Rule', 'Used by Google') + '''
      <tbody>
        <tr><td><code>loc</code></td><td>Full URL with https, under 2,048 characters, special characters escaped</td><td>Yes, required</td></tr>
        <tr><td><code>lastmod</code></td><td>Date in W3C format, like 2026-11-04</td><td>Yes, if it is accurate</td></tr>
        <tr><td><code>changefreq</code></td><td>always, hourly, daily, weekly, monthly, yearly or never</td><td>No, ignored</td></tr>
        <tr><td><code>priority</code></td><td>0.0 to 1.0, default 0.5</td><td>No, ignored</td></tr>
        <tr><td>File size</td><td>Up to 50,000 URLs and 50 MB uncompressed</td><td>Larger files must be split</td></tr>
      </tbody>
    </table></div>
    <p>These limits come from <a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap" ''' + EXT + '''>Google's sitemap guide</a> and the <a href="https://www.sitemaps.org/protocol.html" ''' + EXT + '''>sitemaps.org protocol</a>. The generator escapes characters like <code>&amp;</code> for you, which is the most common reason a hand made sitemap fails.</p>

    <h2>Tips for a Better Sitemap</h2>
    <ul>
      <li><strong>List canonical URLs only.</strong> Leave out redirects, error pages, noindex pages and filtered duplicates.</li>
      <li><strong>Be honest with lastmod.</strong> Google stops trusting dates that change on every page every day.</li>
      <li><strong>Pick one version of your domain.</strong> Do not mix http and https, or www and non www.</li>
      <li><strong>Split big sites by type</strong>, such as posts, products and categories, so Search Console reports are easier to read.</li>
    </ul>

    <h2>Learn More About Sitemaps</h2>
    <p>Read <a href="''' + B + '''what-is-xml-sitemap-ai-search-era/">what an XML sitemap is in the AI search era</a>, compare <a href="''' + B + '''html-sitemap-vs-xml-sitemap-difference/">HTML and XML sitemaps</a>, and automate the job with our guide to <a href="''' + B + '''build-xml-sitemap-generator-php/">building a sitemap generator in PHP</a>. Already have a sitemap? Check it with the <a href="''' + T + '''xml-sitemap-validator/">XML sitemap validator</a>.</p>
''',
        faqs=[
            ("How many URLs can one sitemap hold?", "Up to 50,000 URLs and 50 MB uncompressed. For more, split the list into several files and list them in a sitemap index. The generator does this for you."),
            ("Should I add priority and changefreq?", "You can, but Google ignores both. A correct lastmod date is far more useful, so the generator leaves the other two out unless you turn them on."),
            ("Where do I upload my sitemap?", "Upload it to the root of your site, such as yourdomain.com/sitemap.xml, add a Sitemap line to your robots.txt file, and submit the URL in Google Search Console."),
            ("Does a sitemap get my pages indexed?", "It helps Google find them, but it is only a hint. Pages still need to be useful, crawlable and not blocked or marked noindex to be indexed."),
        ],
        related=[("What Is an XML Sitemap", "what-is-xml-sitemap-ai-search-era"), ("HTML vs XML Sitemap", "html-sitemap-vs-xml-sitemap-difference"),
                 ("Build an XML Sitemap Generator in PHP", "build-xml-sitemap-generator-php"), ("Large Scale XML Sitemaps in PHP", "large-scale-xml-sitemaps-php-index-files")],
    ))

    # ---------- 4. XML SITEMAP VALIDATOR ----------
    SV_SAMPLE = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2026-11-02</lastmod>
  </url>
  <url>
    <loc>https://www.example.com/services/seo-audit/</loc>
    <lastmod>2026-10-30T09:15:00+05:30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>/blog/technical-seo-checklist/</loc>
    <lastmod>28/10/2026</lastmod>
  </url>
  <url>
    <loc>https://www.example.com/blog/core web vitals/</loc>
    <changefreq>sometimes</changefreq>
    <priority>1.5</priority>
  </url>
  <url>
    <loc>http://www.example.com/contact/</loc>
  </url>
  <url>
    <loc>https://www.example.com/services/seo-audit/</loc>
  </url>
</urlset>'''
    TOOLS.append(dict(
        slug='xml-sitemap-validator', short='SV', name='XML Sitemap Validator',
        card='Paste a sitemap or sitemap index and find XML errors, bad URLs, wrong dates and broken limits.',
        title='XML Sitemap Validator: Check Sitemap Errors Free',
        desc='Free XML sitemap validator. Paste a sitemap or sitemap index to find XML errors, relative URLs, bad lastmod dates, duplicates and size limits before Google.',
        h1='XML Sitemap Validator',
        lead='Paste the XML of any sitemap or sitemap index. The validator checks the file against the sitemaps.org protocol and Google\'s rules, and lists every problem with the exact URL to fix.',
        tool='''<section class="tool" aria-label="XML sitemap validator" id="svForm">
    <div class="card" style="min-width:0">
      <h2>Your Sitemap</h2>
      ''' + F('svXml', 'Paste Sitemap XML', SV_SAMPLE, tag='textarea', mono=True, extra=' style="min-height:400px"') + '''
      ''' + F('svAt', 'Sitemap Location', 'https://www.example.com/sitemap.xml', em='optional, checks host and folder', mono=True) + '''
      <p style="font-size:13.5px;color:#666;margin:-6px 0 0">Tip: open your sitemap in a browser, press Ctrl+U to view the source, then copy everything.</p>
    </div>
    <div class="card" style="min-width:0">
      <h2>Validation Report</h2>
      <div class="stats">''' + S('svUrls', 'URLs') + S('svErr', 'Errors') + S('svWarn', 'Warnings') + S('svSize', 'Size') + '''</div>
      <div class="kw-result" id="svCheck"></div>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>#</th><th>URL</th><th>Problem</th></tr></thead><tbody id="svBody"></tbody></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var NS = 'http://www.sitemaps.org/schemas/sitemap/0.9';
  var W3C = /^\d{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01])(T([01]\d|2[0-3]):[0-5]\d(:[0-5]\d(\.\d+)?)?(Z|[+-]([01]\d|2[0-3]):[0-5]\d))?)?)?$/;
  var FREQ = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never'];
  function kids(el, name){ return Array.from(el.children).filter(function(x){ return x.localName === name; }); }
  function txt(el){ return el ? el.textContent : ''; }
  function run(){
    var raw = $('svXml').value, rows = [], err = 0, warn = 0, sum = [];
    function add(n, url, lvl, msg){ if (lvl === 'bad') err++; else warn++; rows.push([n, url, lvl, msg]); }
    var size = bytes(raw); $('svSize').textContent = kb(size);
    if (!raw.trim()){ $('svUrls').textContent = 0; $('svErr').textContent = 0; $('svWarn').textContent = 0; $('svBody').innerHTML = ''; say('svCheck', '', 'Paste the XML of a sitemap to check it.'); return; }
    var doc = new DOMParser().parseFromString(raw.replace(/^﻿/, ''), 'application/xml'), pe = doc.getElementsByTagName('parsererror')[0];
    if (pe){
      var m = (pe.textContent.match(/line (\d+)/i) || []), msg = pe.textContent.replace(/\s+/g, ' ').replace(/^.*?error[^:]*:\s*/i, '').replace(/Below is a rendering.*$/i, '').trim();
      $('svUrls').textContent = 0; $('svErr').textContent = 1; $('svWarn').textContent = 0; $('svBody').innerHTML = '';
      var hint = /&/.test(raw) && /EntityRef|entity|&/i.test(msg) ? ' A raw ' + c('&') + ' inside a URL must be written as ' + c('&amp;') + '.' : '';
      say('svCheck', 'bad', '<strong>This is not valid XML' + (m[1] ? ', the first error is on line ' + m[1] : '') + '.</strong> Google cannot read the file until it is fixed.' + hint + '<br><span style="font-size:13px;color:#666">' + esc(msg.slice(0, 220)) + '</span>');
      return;
    }
    var root = doc.documentElement, type = root.localName, isIdx = type === 'sitemapindex';
    if (type !== 'urlset' && !isIdx){ $('svBody').innerHTML = ''; say('svCheck', 'bad', '<strong>The root element is ' + c('<' + root.nodeName + '>') + '.</strong> A sitemap must start with ' + c('<urlset>') + ' or ' + c('<sitemapindex>') + '.'); $('svErr').textContent = 1; return; }
    if (root.namespaceURI !== NS){ err++; sum.push(['bad', 'The ' + c('<' + type + '>') + ' tag must declare ' + c('xmlns="' + NS + '"') + '.']); }
    if (!/^\s*(﻿)?<\?xml/.test(raw)) sum.push(['warn', 'Add ' + c('<?xml version="1.0" encoding="UTF-8"?>') + ' as the first line.']);
    var items = kids(root, isIdx ? 'sitemap' : 'url'), seen = {}, at = absUrl(v('svAt')), host = at ? at.host : null, proto = {}, dates = {}, dated = 0, hasPF = false;
    var dir = at ? at.pathname.replace(/[^\/]*$/, '') : '/';
    if (!items.length){ err++; sum.push(['bad', 'No ' + c(isIdx ? '<sitemap>' : '<url>') + ' entries found.']); }
    var now = Date.now() + 86400000;
    items.forEach(function(it, i){
      var n = i + 1, locs = kids(it, 'loc'), loc = txt(locs[0]), show = loc.trim() || '(no loc)';
      if (!locs.length || !loc.trim()){ add(n, show, 'bad', 'Missing ' + c('<loc>') + '. Every entry needs one.'); return; }
      if (locs.length > 1) add(n, show, 'bad', 'Has more than one ' + c('<loc>') + '.');
      if (loc !== loc.trim()) add(n, show, 'warn', 'Spaces or line breaks around the URL. Remove them.');
      loc = loc.trim();
      var u = absUrl(loc);
      if (!u) add(n, show, 'bad', 'Not a full URL. Use ' + c('https://') + ' and the domain, not a relative path.');
      else {
      if (/[\s<>"{}|\\^`]|[^\x00-\x7f]/.test(loc)) add(n, show, 'bad', 'Contains spaces or special characters. Encode them, like ' + c(u.href.slice(0, 60)) + '.');
      if (loc.length > 2048) add(n, show, 'bad', 'Longer than 2,048 characters.');
      if (u.hash) add(n, show, 'warn', 'Contains a ' + c('#') + ' fragment, which search engines ignore.');
      if (!host) host = u.host;
      if (u.host !== host) add(n, show, 'bad', 'Host ' + c(u.host) + ' differs from ' + c(host) + '. One sitemap can only list URLs from its own host, unless both sites are verified in Search Console.');
      else if (at && u.pathname.indexOf(dir) !== 0) add(n, show, 'warn', 'Outside the folder ' + c(dir) + ' where the sitemap lives. This only works if you submit the sitemap in Search Console.');
      proto[u.protocol] = 1;
      }
      if (seen[loc]) add(n, show, 'warn', 'Duplicate of entry ' + seen[loc] + '.'); else seen[loc] = n;
      if (/[?&](utm_[a-z]+|gclid|fbclid|sessionid)=/i.test(loc)) add(n, show, 'warn', 'Has a tracking or session parameter. List the clean canonical URL instead.');
      var lm = kids(it, 'lastmod')[0];
      if (lm){
        var d = txt(lm).trim(); dated++;
        if (!W3C.test(d)) add(n, show, 'bad', c(d) + ' is not a valid W3C date. Use ' + c('2026-11-04') + ' or ' + c('2026-11-04T10:30:00+05:30') + '.');
        else { dates[d] = (dates[d] || 0) + 1; if (Date.parse(d.length === 10 ? d + 'T00:00:00Z' : d) > now) add(n, show, 'warn', 'The lastmod date ' + c(d) + ' is in the future.'); }
      }
      if (!isIdx){
        var cf = kids(it, 'changefreq')[0], pr = kids(it, 'priority')[0];
        if (cf){ hasPF = true; if (FREQ.indexOf(txt(cf).trim()) < 0) add(n, show, 'bad', c(txt(cf).trim()) + ' is not a valid changefreq. Use one of ' + FREQ.join(', ') + '.'); }
        if (pr){ hasPF = true; var p = txt(pr).trim(); if (!/^(0(\.\d+)?|1(\.0+)?)$/.test(p)) add(n, show, 'bad', 'Priority ' + c(p) + ' must be a number from 0.0 to 1.0.'); }
      }
      Array.from(it.children).forEach(function(ch){
        if (ch.namespaceURI === NS && ['loc', 'lastmod', 'changefreq', 'priority'].indexOf(ch.localName) < 0) add(n, show, 'warn', 'Unknown tag ' + c('<' + ch.localName + '>') + '.');
      });
    });
    if (Object.keys(proto).length > 1) sum.push(['warn', 'The sitemap mixes http and https URLs. List only the version you want indexed.']);
    if (items.length > 50000){ err++; sum.push(['bad', 'There are ' + fmtN(items.length) + ' entries. The limit is 50,000 per file, so split it and use a sitemap index.']); }
    if (size > 52428800){ err++; sum.push(['bad', 'The file is larger than 50 MB uncompressed. Split it into smaller sitemaps.']); }
    var top = Object.keys(dates).sort(function(a, b){ return dates[b] - dates[a]; })[0];
    if (dated >= 10 && top && dates[top] / dated > 0.9) sum.push(['warn', 'Almost every URL has the lastmod ' + c(top) + '. That looks like the date the file was made. Google only uses lastmod when it is accurate.']);
    if (hasPF) sum.push(['warn', 'Google ignores ' + c('changefreq') + ' and ' + c('priority') + '. They are valid but you can remove them.']);
    if (isIdx) sum.push(['warn', 'This is a sitemap index. Paste each child sitemap here too, to check the URLs inside them.']);
    warn += sum.filter(function(s){ return s[0] === 'warn'; }).length;
    $('svUrls').textContent = fmtN(items.length); $('svErr').textContent = err; $('svWarn').textContent = warn;
    $('svBody').innerHTML = rows.slice(0, 300).map(function(r){
      return '<tr><td class="num">' + r[0] + '</td><td style="word-break:break-all">' + esc(r[1]) + '</td><td><b style="color:' + (r[2] === 'bad' ? '#d1351f' : '#c47a00') + '">' + (r[2] === 'bad' ? 'Error' : 'Warning') + '</b> ' + r[3] + '</td></tr>';
    }).join('') + (rows.length > 300 ? '<tr><td colspan="3" class="empty">And ' + (rows.length - 300) + ' more.</td></tr>' : '') || '<tr><td colspan="3" class="empty">No problems in any entry.</td></tr>';
    var label = isIdx ? 'sitemap index with ' + fmtN(items.length) + ' sitemap' + (items.length === 1 ? '' : 's') : 'sitemap with ' + fmtN(items.length) + ' URL' + (items.length === 1 ? '' : 's');
    var head = err ? '<strong>Found ' + err + ' error' + (err > 1 ? 's' : '') + ' in this ' + label + '.</strong> Errors can stop Google reading some or all URLs.' : warn ? '<strong>Valid ' + label + ', with ' + warn + ' warning' + (warn > 1 ? 's' : '') + '.</strong>' : '<strong>Valid ' + label + '.</strong> No problems found. Submit it in Search Console.';
    say('svCheck', err ? 'bad' : warn ? 'warn' : 'ok', head + (sum.length ? '<ul style="margin:6px 0 0 18px">' + sum.map(function(s){ return '<li>' + s[1] + '</li>'; }).join('') + '</ul>' : ''));
  }
  $('svForm').addEventListener('input', run);
  run();
''',
        content='''
    <h2>What Is an XML Sitemap Validator?</h2>
    <p>An XML sitemap validator checks that your sitemap is a file search engines can read and trust. One stray character, such as an unescaped <code>&amp;</code> in a URL, can break the whole file. Smaller mistakes, like relative URLs or badly formatted dates, quietly cause Google to skip entries.</p>
    <p>Paste the XML and the validator reads it in your browser, checks every entry and tells you exactly which URL to fix and why. Nothing is uploaded, so it works for staging sites and private projects too.</p>

    <h2>How to Validate Your Sitemap</h2>
    <ol>
      <li><strong>Open your sitemap</strong>, for example <code>yourdomain.com/sitemap.xml</code>, and view the page source.</li>
      <li><strong>Copy all of the XML</strong> and paste it into the box.</li>
      <li><strong>Add the sitemap location</strong> so the tool can check the host and folder rules.</li>
      <li><strong>Fix every error first</strong>, then review the warnings.</li>
      <li><strong>Resubmit the sitemap</strong> in Search Console once it is clean.</li>
    </ol>

    <h2>What the Validator Checks</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Check', 'Why it matters') + '''
      <tbody>
        <tr><td>Well formed XML</td><td>A single syntax error makes the whole file unreadable</td></tr>
        <tr><td>Root tag and namespace</td><td><code>urlset</code> or <code>sitemapindex</code> with the sitemaps.org namespace</td></tr>
        <tr><td>Full, encoded URLs</td><td>Every <code>loc</code> needs the protocol and domain, with spaces encoded</td></tr>
        <tr><td>Same host and folder</td><td>A sitemap normally covers only URLs on its own host and below its folder</td></tr>
        <tr><td>Valid lastmod dates</td><td>W3C format only. Dates like 28/10/2026 are rejected</td></tr>
        <tr><td>changefreq and priority</td><td>Must use allowed values, though Google ignores both</td></tr>
        <tr><td>Duplicates and tracking codes</td><td>Waste crawling and send mixed signals about the canonical URL</td></tr>
        <tr><td>50,000 URLs and 50 MB</td><td>The hard limits for one file</td></tr>
      </tbody>
    </table></div>
    <p>The rules follow the <a href="https://www.sitemaps.org/protocol.html" ''' + EXT + '''>sitemaps.org protocol</a> and <a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap" ''' + EXT + '''>Google's sitemap guidelines</a>.</p>

    <h2>Tips After Validating</h2>
    <ul>
      <li><strong>Valid is not the same as useful.</strong> Make sure every URL returns a 200 status, is canonical and is not marked noindex.</li>
      <li><strong>Watch the Sitemaps report</strong> in Search Console for fetch errors and the number of discovered pages.</li>
      <li><strong>Fix the source, not the file.</strong> If your CMS or plugin writes bad dates, change its settings so the problem does not return.</li>
      <li><strong>Check child sitemaps.</strong> For an index file, validate each listed sitemap as well.</li>
    </ul>

    <h2>Keep Your Sitemaps Healthy</h2>
    <p>Fix pages Google found but skipped with <a href="''' + B + '''discovered-currently-not-indexed-fix/">discovered, currently not indexed</a>, learn how to manage big sites with a <a href="''' + B + '''php-sitemap-index-generator/">sitemap index generator in PHP</a>, and see whether <a href="''' + B + '''indexnow-explained-can-it-help-google-index-faster/">IndexNow can speed up indexing</a>. Need a fresh file? Build one with the <a href="''' + T + '''xml-sitemap-generator/">XML sitemap generator</a>.</p>
''',
        faqs=[
            ("Why does Search Console say my sitemap could not be read?", "Usually the file is not valid XML, often because of an unescaped ampersand, a missing closing tag, or an HTML error page served instead of the sitemap. Paste the XML here to find the first error."),
            ("Are relative URLs allowed in a sitemap?", "No. Every loc must be a full URL including https and the domain. A path like /contact/ on its own is rejected by Google."),
            ("What date format should lastmod use?", "Use the W3C datetime format. A simple date like 2026-11-04 is fine, or add the time and time zone, like 2026-11-04T10:30:00+05:30."),
            ("Can I validate a sitemap index file?", "Yes. Paste a sitemap index and the tool checks each listed sitemap URL and date. Then paste each child sitemap to check the pages inside it."),
        ],
        related=[("What Is an XML Sitemap", "what-is-xml-sitemap-ai-search-era"), ("PHP Sitemap Index Generator", "php-sitemap-index-generator"),
                 ("Discovered Currently Not Indexed Fix", "discovered-currently-not-indexed-fix"), ("IndexNow Explained", "indexnow-explained-can-it-help-google-index-faster")],
    ))

    # ---------- 5. HREFLANG TAG GENERATOR ----------
    TOOLS.append(dict(
        slug='hreflang-tag-generator', short='HG', name='Hreflang Tag Generator',
        card='Build hreflang link tags, sitemap entries or HTTP headers for every language and country version of a page.',
        title='Hreflang Tag Generator: HTML, Sitemap and Header',
        desc='Free hreflang tag generator. Add each language and country version of a page and get valid hreflang tags for HTML, XML sitemaps or HTTP headers, with x-default.',
        h1='Hreflang Tag Generator',
        lead='List every language and country version of a page and get hreflang code that follows Google\'s rules. Choose HTML tags, XML sitemap entries or an HTTP header, and add a fallback page for everyone else.',
        tool='''<section class="tool" aria-label="Hreflang tag generator" id="hgForm">
    <div class="card" style="min-width:0">
      <h2>Page Versions</h2>
      <div id="hgRows"></div>
      <div class="actions" style="margin:0 0 16px"><button type="button" class="btn btn-sm" id="hgAdd">Add a Version</button></div>
      ''' + F('hgDef', 'Fallback Page', 'https://www.example.com/', em='optional', mono=True) + '''
      <div class="tips" style="margin-top:4px"><strong>Codes</strong><ul><li>Language is required, country is optional</li><li>The fallback page becomes the <code>x-default</code> tag for visitors who match no version</li><li>Pick a country only when content differs by country, such as prices or spelling</li></ul></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Hreflang Code</h2>
      <div class="tabs" id="hgTabs"><button type="button" class="on" data-m="html">HTML Tags</button><button type="button" data-m="xml">XML Sitemap</button><button type="button" data-m="http">HTTP Header</button></div>
      <div class="kw-result" id="hgCheck"></div>
      <pre class="code-out" id="hgOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="hgCopy">Copy Code</button><span class="toast" id="toast">Copied!</span></div>
      <p id="hgWhere" style="font-size:14px;color:#555;margin-top:12px"></p>
    </div>
  </section>''',
        js=BASEJS + LANGJS + r'''
  var mode = 'html', out = '';
  var SAMPLE = [['en', '', 'https://www.example.com/'], ['en', 'IN', 'https://www.example.com/en-in/'], ['hi', 'IN', 'https://www.example.com/hi-in/'],
                ['en', 'GB', 'https://www.example.com/en-gb/'], ['de', 'DE', 'https://www.example.com/de-de/']];
  var LOPT = LANGS.map(function(l){ return [l, lname(l)]; }).concat([['zh-Hans', 'Chinese (Simplified)'], ['zh-Hant', 'Chinese (Traditional)'], ['sr-Latn', 'Serbian (Latin)'], ['sr-Cyrl', 'Serbian (Cyrillic)']])
    .sort(function(a, b){ return a[1].localeCompare(b[1]); }).map(function(x){ return '<option value="' + x[0] + '">' + esc(x[1]) + ' (' + x[0] + ')</option>'; }).join('');
  var ROPT = '<option value="">Any country</option>' + REGIONS.filter(function(r){ return !(r in RESERVED); }).map(function(r){ return [r, rname(r)]; })
    .sort(function(a, b){ return a[1].localeCompare(b[1]); }).map(function(x){ return '<option value="' + x[0] + '">' + esc(x[1]) + ' (' + x[0] + ')</option>'; }).join('');
  var rid = 0;
  function addRow(l, r, u){
    rid++; var d = document.createElement('div');
    d.className = 'hgRow'; d.style.cssText = 'border:1px solid #e6e6e6;border-radius:10px;padding:12px 12px 2px;margin-bottom:12px';
    d.innerHTML = '<div class="row2"><div class="field"><label for="hgL' + rid + '">Language</label><select id="hgL' + rid + '" class="hgL">' + LOPT + '</select></div>'
      + '<div class="field"><label for="hgR' + rid + '">Country</label><select id="hgR' + rid + '" class="hgR">' + ROPT + '</select></div></div>'
      + '<div class="field"><label for="hgU' + rid + '">Page URL <button type="button" class="btn btn-sm hgDel" style="float:right;padding:2px 10px">Remove</button></label><input id="hgU' + rid + '" class="hgU mono" type="text" autocomplete="off" spellcheck="false" placeholder="https://www.example.com/fr/"></div>';
    $('hgRows').appendChild(d);
    d.querySelector('.hgL').value = l || 'en'; d.querySelector('.hgR').value = r || ''; d.querySelector('.hgU').value = u || '';
    d.querySelector('.hgDel').onclick = function(){ d.remove(); gen(); };
  }
  function rows(){
    return Array.from(document.querySelectorAll('.hgRow')).map(function(d){
      var l = d.querySelector('.hgL').value, r = d.querySelector('.hgR').value;
      return {code: l + (r ? '-' + r : ''), url: d.querySelector('.hgU').value.trim()};
    });
  }
  function gen(){
    var R = rows(), iss = [], seen = {}, seenU = {}, set = [];
    R.forEach(function(x, i){
      if (!x.url){ iss.push(['bad', 'Version ' + (i + 1) + ' (' + c(x.code) + ') has no URL.']); return; }
      if (!absUrl(x.url)){ iss.push(['bad', c(x.url) + ' must be a full URL with ' + c('https://') + '. Relative URLs are ignored by Google.']); return; }
      var chk = checkCode(x.code); if (!chk.ok){ iss.push(['bad', chk.err]); return; }
      if (chk.warn) iss.push(['warn', chk.warn]);
      if (seen[x.code.toLowerCase()]){ iss.push(['bad', c(x.code) + ' is used twice. Each language and country pair can point to only one URL.']); return; }
      if (seenU[x.url]) iss.push(['warn', c(x.url) + ' is used for both ' + c(seenU[x.url]) + ' and ' + c(x.code) + '. That is allowed, but check it is what you want.']);
      seen[x.code.toLowerCase()] = 1; seenU[x.url] = x.code; set.push(x);
    });
    var def = v('hgDef');
    if (def){ if (!absUrl(def)) iss.push(['bad', 'The fallback URL must be a full URL with ' + c('https://') + '.']); else set.push({code: 'x-default', url: def}); }
    var real = set.filter(function(x){ return x.code !== 'x-default'; });
    if (real.length < 2) iss.push(['warn', 'Hreflang is for pages with at least two language or country versions. Add another version.']);
    var langs = {}; real.forEach(function(x){ var l = x.code.split('-')[0]; (langs[l] = langs[l] || []).push(x.code); });
    Object.keys(langs).forEach(function(l){ if (langs[l].every(function(cd){ return cd.indexOf('-') > -1; }) && langs[l].length > 1) iss.push(['warn', 'Every ' + esc(lname(l)) + ' version targets a country. Consider one plain ' + c(l) + ' version, or the fallback, for ' + esc(lname(l)) + ' speakers elsewhere.']); });
    var L = [];
    if (mode === 'html'){
      set.forEach(function(x){ L.push('<link rel="alternate" hreflang="' + x.code + '" href="' + xesc(x.url) + '" />'); });
      $('hgWhere').innerHTML = 'Paste the same block inside the ' + c('<head>') + ' of <strong>every</strong> page listed, including the page itself.';
    } else if (mode === 'xml'){
      L.push('<?xml version="1.0" encoding="UTF-8"?>');
      L.push('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'); L.push('        xmlns:xhtml="http://www.w3.org/1999/xhtml">');
      var pages = []; set.forEach(function(x){ if (pages.indexOf(x.url) < 0) pages.push(x.url); });
      pages.forEach(function(p){
        L.push('  <url>'); L.push('    <loc>' + xesc(p) + '</loc>');
        set.forEach(function(x){ L.push('    <xhtml:link rel="alternate" hreflang="' + x.code + '" href="' + xesc(x.url) + '" />'); });
        L.push('  </url>');
      });
      L.push('</urlset>');
      $('hgWhere').innerHTML = 'Each URL gets its own ' + c('<url>') + ' entry listing every version. Use this instead of HTML tags, not as well as them.';
    } else {
      L.push('Link: ' + set.map(function(x){ return '<' + x.url + '>; rel="alternate"; hreflang="' + x.code + '"'; }).join(', '));
      $('hgWhere').innerHTML = 'Send this same header with every version. It suits files without a ' + c('<head>') + ', such as PDFs.';
    }
    out = L.join('\n');
    $('hgOut').textContent = out;
    issues('hgCheck', iss, '<strong>Valid hreflang set with ' + real.length + ' versions' + (def ? ' and a fallback' : '') + '.</strong> Every version lists itself and all the others, so the return links are in place.');
  }
  SAMPLE.forEach(function(s){ addRow(s[0], s[1], s[2]); });
  $('hgAdd').onclick = function(){ addRow('fr', 'FR', ''); gen(); var u = document.querySelectorAll('.hgU'); u[u.length - 1].focus(); };
  document.querySelectorAll('#hgTabs button').forEach(function(b){ b.onclick = function(){
    document.querySelectorAll('#hgTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); mode = b.getAttribute('data-m'); gen(); }; });
  $('hgForm').addEventListener('input', gen); $('hgForm').addEventListener('change', gen);
  $('hgCopy').onclick = function(){ copyText(out, 'toast'); };
  gen();
''',
        content='''
    <h2>What Are Hreflang Tags?</h2>
    <p>Hreflang tags tell Google that several pages are versions of the same content for different languages or countries. Google then shows each searcher the version that fits them best, so a visitor in India sees your English India page while a visitor in Germany sees the German one.</p>
    <p>The tags do not change rankings by themselves. They stop the wrong version from showing up, and help Google treat similar pages, like English for India and English for the UK, as a related set instead of duplicates.</p>

    <h2>How to Use the Hreflang Generator</h2>
    <ol>
      <li><strong>Add one row per version</strong> of the page. Pick the language, and a country only when the content is made for that country.</li>
      <li><strong>Paste the full URL</strong> of each version, including <code>https://</code>.</li>
      <li><strong>Set a fallback page</strong> with <code>x-default</code>, such as your main page or a language picker.</li>
      <li><strong>Choose a format</strong>: HTML tags, XML sitemap entries or an HTTP header.</li>
      <li><strong>Add the same code to every version.</strong> Each page must list itself and all the others.</li>
    </ol>

    <h2>Hreflang Rules Google Uses</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Rule', 'Example') + '''
      <tbody>
        <tr><td>Language first, in ISO 639 1 format</td><td><code>en</code>, <code>hi</code>, <code>de</code></td></tr>
        <tr><td>Optional country, in ISO 3166 1 format</td><td><code>en-IN</code>, <code>en-GB</code></td></tr>
        <tr><td>A country alone is not allowed</td><td><code>in</code> or <code>gb</code> on their own are wrong</td></tr>
        <tr><td>Reserved codes do nothing</td><td>Use <code>en-GB</code>, never <code>en-UK</code></td></tr>
        <tr><td>Optional script for some languages</td><td><code>zh-Hans</code>, <code>zh-Hant</code></td></tr>
        <tr><td>Fully qualified URLs only</td><td><code>https://www.example.com/de-de/</code></td></tr>
        <tr><td>Return links are required</td><td>If A points to B, B must point back to A</td></tr>
      </tbody>
    </table></div>
    <p>These rules come from Google's guide to <a href="https://developers.google.com/search/docs/specialty/international/localized-versions" ''' + EXT + '''>localized versions of your pages</a>. Google also says region codes like <code>es-419</code> are not supported, so this generator lists real countries only.</p>

    <h2>Practical Hreflang Tips</h2>
    <ul>
      <li><strong>Pick one method.</strong> HTML tags, sitemap entries and headers do the same job. Using more than one only adds room for mistakes.</li>
      <li><strong>Match your canonicals.</strong> Each version should have a self referencing canonical tag, not one that points to another language.</li>
      <li><strong>Translate the whole page.</strong> Hreflang works best when the main content, not just the menu, is in the target language.</li>
      <li><strong>Keep the set identical.</strong> When you add a new language, update the tags on every existing version too.</li>
    </ul>

    <h2>Learn More About International SEO</h2>
    <p>Start with <a href="''' + B + '''hreflang-tags-explained/">hreflang tags explained</a>, then make sure every version has the right <a href="''' + B + '''canonical-tag-implementation-guide/">canonical tag</a> and a clear <a href="''' + B + '''url-structure-for-ai-seo/">URL structure</a>. Already live? Test your tags with the <a href="''' + T + '''hreflang-checker/">hreflang checker</a>.</p>
''',
        faqs=[
            ("Do I need a country code in hreflang?", "No. A language code alone, like en or hi, is often the best choice. Add a country only when the page is made for that country, for example different prices, currency or spelling."),
            ("What is the x default hreflang value for?", "It names the page to show visitors whose language or country matches none of your versions. Many sites use their main English page or a language picker page."),
            ("Should a page include a hreflang tag for itself?", "Yes. Google asks every version to list itself as well as all the other versions. The generator builds one shared block that does this for you."),
            ("Can hreflang point to another domain?", "Yes. Versions can live on different domains, such as example.in and example.de, as long as every URL is fully qualified and every page links back."),
        ],
        related=[("Hreflang Tags Explained", "hreflang-tags-explained"), ("Canonical Tag Implementation Guide", "canonical-tag-implementation-guide"),
                 ("URL Structure for AI SEO", "url-structure-for-ai-seo"), ("What Is a Canonical Tag", "what-is-canonical-tag")],
    ))

    # ---------- 6. HREFLANG CHECKER ----------
    HC_SAMPLE = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.example.com/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/" />
    <xhtml:link rel="alternate" hreflang="en-IN" href="https://www.example.com/en-in/" />
    <xhtml:link rel="alternate" hreflang="en-UK" href="https://www.example.com/en-gb/" />
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/" />
  </url>
  <url>
    <loc>https://www.example.com/en-in/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/" />
    <xhtml:link rel="alternate" hreflang="en-IN" href="https://www.example.com/en-in/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/" />
  </url>
  <url>
    <loc>https://www.example.com/de/</loc>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de/" />
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/" />
    <xhtml:link rel="alternate" hreflang="en-IN" href="https://www.example.com/en-in/" />
  </url>
</urlset>'''
    TOOLS.append(dict(
        slug='hreflang-checker', short='HC', name='Hreflang Checker',
        card='Validate hreflang codes, self references, fallback tags and return links from a sitemap, page HTML or header.',
        title='Hreflang Checker: Validate Tags and Return Links',
        desc='Free hreflang checker. Paste a sitemap, page HTML or Link header to find invalid language codes, missing return links, self references and x-default issues.',
        h1='Hreflang Checker',
        lead='Paste a hreflang sitemap, the HTML of a page or its Link header. The checker validates every language and country code and, for sitemaps, confirms that every page links back to the others.',
        tool='''<section class="tool" aria-label="Hreflang checker" id="hcForm">
    <div class="card" style="min-width:0">
      <h2>Your Hreflang Tags</h2>
      ''' + F('hcIn', 'Paste a Sitemap, HTML or Link Header', HC_SAMPLE, tag='textarea', mono=True, extra=' style="min-height:420px"') + '''
      ''' + F('hcPage', 'Page URL', 'https://www.example.com/', em='needed for HTML or a header only', mono=True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Check Results</h2>
      <div class="stats">''' + S('hcPages', 'Pages') + S('hcTags', 'Tags') + S('hcErr', 'Errors') + S('hcWarn', 'Warnings') + '''</div>
      <p id="hcMode" style="font-size:13.5px;color:#666;margin:-6px 0 12px"></p>
      <div class="kw-result" id="hcCheck"></div>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Code</th><th>Means</th><th>URL</th></tr></thead><tbody id="hcBody"></tbody></table></div>
    </div>
  </section>''',
        js=BASEJS + LANGJS + r'''
  function parseInput(raw){
    var t = raw.trim();
    if (/<urlset[\s>]/i.test(t)){
      var doc = new DOMParser().parseFromString(t, 'application/xml'), pe = doc.getElementsByTagName('parsererror')[0];
      if (pe) return {err: 'This sitemap is not valid XML' + ((pe.textContent.match(/line \d+/i) || [''])[0] ? ', see ' + (pe.textContent.match(/line \d+/i) || [''])[0] : '') + '. Check that ' + c('xmlns:xhtml') + ' is declared and every tag is closed.'};
      var pages = Array.from(doc.documentElement.children).filter(function(x){ return x.localName === 'url'; }).map(function(u){
        var loc = (Array.from(u.children).find(function(x){ return x.localName === 'loc'; }) || {}).textContent || '';
        var links = Array.from(u.children).filter(function(x){ return x.localName === 'link'; }).map(function(l){
          return {code: l.getAttribute('hreflang') || '', href: (l.getAttribute('href') || '').trim(), rel: l.getAttribute('rel') || '', ns: l.namespaceURI};
        });
        return {url: loc.trim(), links: links};
      });
      return {mode: 'sitemap', pages: pages};
    }
    if (/^\s*link\s*:/i.test(t) || /^<https?:[^>]+>\s*;/i.test(t)){
      var links = [], re = /<([^>]*)>([^,<]*)/g, m;
      t = t.replace(/^\s*link\s*:/i, '');
      while ((m = re.exec(t))){
        var p = m[2], rel = (p.match(/rel\s*=\s*"?([^";]+)"?/i) || [])[1] || '', hl = (p.match(/hreflang\s*=\s*"?([^";,\s]+)"?/i) || [])[1];
        if (hl) links.push({code: hl, href: m[1].trim(), rel: rel});
      }
      return {mode: 'header', pages: [{url: v('hcPage'), links: links}]};
    }
    var d = new DOMParser().parseFromString(t, 'text/html');
    var ls = Array.from(d.querySelectorAll('link[hreflang]')).map(function(l){
      return {code: l.getAttribute('hreflang'), href: (l.getAttribute('href') || '').trim(), rel: l.getAttribute('rel') || '', media: l.hasAttribute('media'), inBody: !!l.closest('body')};
    });
    var canon = d.querySelector('link[rel="canonical"]');
    return {mode: 'html', pages: [{url: v('hcPage'), links: ls, canon: canon ? canon.getAttribute('href') : null}]};
  }
  function slashAlt(u){ return /\/$/.test(u) ? u.slice(0, -1) : u + '/'; }
  function run(){
    var P = parseInput($('hcIn').value), iss = [], rows = [], tags = 0;
    if (P.err){ ['hcPages', 'hcTags', 'hcWarn'].forEach(function(i){ $(i).textContent = 0; }); $('hcErr').textContent = 1; $('hcBody').innerHTML = ''; $('hcMode').textContent = ''; say('hcCheck', 'bad', '<strong>' + P.err + '</strong>'); return; }
    $('hcMode').innerHTML = {sitemap: 'Read as an XML sitemap. Return links are checked across all pages.', html: 'Read as page HTML. Paste a sitemap to check return links across pages.', header: 'Read as an HTTP Link header.'}[P.mode];
    var byUrl = {}; P.pages.forEach(function(p){ byUrl[p.url] = p; });
    P.pages.forEach(function(p, pi){
      var who = P.mode === 'sitemap' ? c(p.url || 'entry ' + (pi + 1)) : 'This page';
      if (!p.url) iss.push(['bad', P.mode === 'sitemap' ? 'Entry ' + (pi + 1) + ' has no ' + c('<loc>') + '.' : 'Enter the page URL so the self reference can be checked.']);
      if (!p.links.length){ iss.push(['bad', who + ' has no hreflang tags.']); return; }
      if (P.mode === 'sitemap') rows.push('<tr><td colspan="3" style="background:#f4f4f4;font-weight:700;word-break:break-all">' + esc(p.url) + '</td></tr>');
      var codes = {}, self = false, hasDef = false;
      p.links.forEach(function(l){
        tags++;
        var k = checkCode(l.code), st = '';
        if (!k.ok){ iss.push(['bad', who + ': ' + k.err]); st = 'bad'; }
        else if (k.warn){ iss.push(['warn', who + ': ' + k.warn]); st = 'warn'; }
        if (!/(^|\s)alternate(\s|$)/i.test(l.rel)) iss.push(['bad', who + ': the tag for ' + c(l.code) + ' needs ' + c('rel="alternate"') + '.']);
        if (l.media) iss.push(['bad', who + ': the tag for ' + c(l.code) + ' also has a ' + c('media') + ' attribute. Google asks you not to combine them.']);
        if (l.inBody) iss.push(['warn', who + ': the tag for ' + c(l.code) + ' sits in the ' + c('<body>') + '. Hreflang tags belong in the ' + c('<head>') + '.']);
        if (!absUrl(l.href)){ iss.push(['bad', who + ': ' + c(l.href || '(empty)') + ' for ' + c(l.code) + ' is not a full URL. Use ' + c('https://') + ' and the domain.']); st = 'bad'; }
        var key = String(l.code).toLowerCase();
        if (codes[key] && codes[key] !== l.href) iss.push(['bad', who + ': ' + c(l.code) + ' points to two different URLs.']);
        else if (codes[key]) iss.push(['warn', who + ': ' + c(l.code) + ' is listed twice.']);
        codes[key] = l.href;
        if (key === 'x-default') hasDef = true;
        if (p.url && l.href === p.url) self = true;
        rows.push('<tr><td><code' + (st ? ' style="color:' + (st === 'bad' ? '#d1351f' : '#c47a00') + '"' : '') + '>' + esc(l.code) + '</code></td><td>' + (k.ok ? esc(k.label) : '<b style="color:#d1351f">Invalid</b>') + '</td><td style="word-break:break-all">' + esc(l.href) + '</td></tr>');
      });
      if (p.url && !self){
        var near = p.links.some(function(l){ return l.href === slashAlt(p.url); });
        iss.push(['bad', who + ' does not list itself.' + (near ? ' A tag points to ' + c(slashAlt(p.url)) + ', which differs only by the trailing slash. URLs must match exactly.' : ' Every version must include a tag for its own URL.')]);
      }
      if (!hasDef) iss.push(['warn', who + ' has no ' + c('x-default') + ' tag. It is optional, but it tells Google which page to show everyone else.']);
      if (P.mode === 'html' && p.canon && absUrl(p.canon) && p.url && p.canon !== p.url) iss.push(['warn', 'The canonical tag points to ' + c(p.canon) + ', not this page. Each language version should be its own canonical.']);
      if (P.mode === 'sitemap' && p.url){
        p.links.forEach(function(l){
          if (!absUrl(l.href) || l.href === p.url) return;
          var other = byUrl[l.href];
          if (!other){
            var alt = byUrl[slashAlt(l.href)];
            iss.push([alt ? 'bad' : 'warn', who + ' points to ' + c(l.href) + (alt ? ', but the sitemap lists ' + c(slashAlt(l.href)) + '. The trailing slash must match exactly.' : ', which is not in this sitemap, so its return link cannot be checked.')]);
            return;
          }
          if (!other.links.some(function(x){ return x.href === p.url; })) iss.push(['bad', c(l.href) + ' does not link back to ' + c(p.url) + '. Without a return link Google ignores the pair.']);
        });
      }
    });
    var err = iss.filter(function(i){ return i[0] === 'bad'; }).length, warn = iss.length - err;
    $('hcPages').textContent = P.pages.length; $('hcTags').textContent = tags; $('hcErr').textContent = err; $('hcWarn').textContent = warn;
    $('hcBody').innerHTML = rows.join('') || '<tr><td colspan="3" class="empty">No hreflang tags found.</td></tr>';
    issues('hcCheck', iss, '<strong>All hreflang tags are valid.</strong> Codes are correct, every page lists itself' + (P.mode === 'sitemap' ? ' and every return link is in place' : '') + '.', 60);
  }
  $('hcForm').addEventListener('input', run);
  run();
''',
        content='''
    <h2>What Does a Hreflang Checker Do?</h2>
    <p>Hreflang is easy to get almost right and still have Google ignore it. A single wrong code like <code>en-UK</code>, a missing trailing slash, or one page that forgets to link back is enough to break the connection between versions. This checker finds those problems before they cost you traffic.</p>
    <p>It reads three formats: an XML sitemap with <code>xhtml:link</code> entries, the HTML of a page with <code>link</code> tags, or an HTTP <code>Link</code> header. With a sitemap it can check the whole set at once, including every return link.</p>

    <h2>How to Use the Hreflang Checker</h2>
    <ol>
      <li><strong>Paste your tags.</strong> Copy the hreflang sitemap, the page source from your browser, or the Link header from your server.</li>
      <li><strong>Add the page URL</strong> if you pasted HTML or a header, so the tool can check the self reference.</li>
      <li><strong>Read the code table.</strong> Each code is translated into plain words, so a slip like Belarusian instead of Belgium stands out.</li>
      <li><strong>Fix the errors</strong>, starting with invalid codes and missing return links.</li>
      <li><strong>Paste again</strong> until the result turns green.</li>
    </ol>

    <h2>Common Hreflang Errors It Finds</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Error', 'How to fix it') + '''
      <tbody>
        <tr><td>Country code on its own</td><td>Add a language first, like <code>en-IN</code> instead of <code>in</code></td></tr>
        <tr><td>Reserved or wrong country</td><td>Use <code>GB</code> for the United Kingdom, never <code>UK</code></td></tr>
        <tr><td>Underscore instead of hyphen</td><td>Write <code>en-US</code>, not <code>en_US</code></td></tr>
        <tr><td>Missing self reference</td><td>Each page must include a tag for its own URL</td></tr>
        <tr><td>Missing return link</td><td>If page A lists page B, page B must list page A</td></tr>
        <tr><td>Trailing slash mismatch</td><td>Use exactly the same URL everywhere, including the final slash</td></tr>
        <tr><td>Relative URLs</td><td>Every <code>href</code> needs <code>https://</code> and the domain</td></tr>
      </tbody>
    </table></div>
    <p>The checks follow Google's guide to <a href="https://developers.google.com/search/docs/specialty/international/localized-versions" ''' + EXT + '''>localized versions of your pages</a>, which says that if two pages do not both point to each other, the tags are ignored.</p>

    <h2>Tips for Clean Hreflang</h2>
    <ul>
      <li><strong>Generate tags from one list.</strong> Building every version from the same source keeps sets identical.</li>
      <li><strong>Use the final URL.</strong> Never point hreflang at a URL that redirects or is blocked by robots.txt.</li>
      <li><strong>Check after every launch.</strong> New languages are where missing return links usually creep in.</li>
      <li><strong>Crawl large sites.</strong> For thousands of pages, a crawler export pasted here in parts saves hours.</li>
    </ul>

    <h2>Learn More About Hreflang</h2>
    <p>Read <a href="''' + B + '''hreflang-tags-explained/">hreflang tags explained</a> for the full picture, line up your canonicals with the <a href="''' + B + '''canonical-tag-implementation-guide/">canonical tag guide</a>, and audit at scale with our <a href="''' + B + '''screaming-frog-seo-spider-beginners-guide/">Screaming Frog beginner guide</a>. Need to write new tags? Use the <a href="''' + T + '''hreflang-tag-generator/">hreflang tag generator</a>.</p>
''',
        faqs=[
            ("Why is Google ignoring my hreflang tags?", "The most common reasons are missing return links, invalid codes like en UK, URLs that do not match exactly, and pages that do not list themselves. Paste your sitemap here to find which one applies."),
            ("Can this tool check return links?", "Yes, when you paste an XML sitemap that contains all the versions. It checks that every page listed by another page links back to it. For a single page, paste a sitemap or check each version in turn."),
            ("Is a missing x default tag an error?", "No. It is optional. It is still worth adding, because it tells Google which page to show visitors whose language or country matches none of your versions."),
            ("Does the checker fetch my live pages?", "No. It only reads what you paste, inside your browser. Nothing is uploaded or fetched, so it works for staging sites too."),
        ],
        related=[("Hreflang Tags Explained", "hreflang-tags-explained"), ("Canonical Tag Implementation Guide", "canonical-tag-implementation-guide"),
                 ("Screaming Frog Beginners Guide", "screaming-frog-seo-spider-beginners-guide"), ("URL Inspection Tool", "url-inspection-tool-diagnose-indexing-problems")],
    ))

    # ---------- 7. HTACCESS REDIRECT GENERATOR ----------
    HR_SAMPLE = '''/old-page/ /new-page/
/blog/seo-tips-2024/ https://www.example.com/blog/seo-tips/
/services.html /services/
/shop/?id=42 /shop/blue-running-shoes/
/about-us/ /about/
/about/ /company/'''
    TOOLS.append(dict(
        slug='htaccess-redirect-generator', short='HR', name='Htaccess Redirect Generator',
        card='Turn a list of old and new URLs into 301 redirect rules for Apache, with chain and loop checks.',
        title='Htaccess Redirect Generator: Bulk 301 Redirects',
        desc='Free htaccess redirect generator. Paste old and new URLs to create 301 or 302 redirects for Apache, force HTTPS and www, and catch redirect chains and loops.',
        h1='Htaccess Redirect Generator',
        lead='Paste old and new URLs, one pair per line, and get redirect rules ready for your Apache or LiteSpeed .htaccess file. Chains are flattened, loops are caught, and query string URLs are handled correctly.',
        tool='''<section class="tool" aria-label="Htaccess redirect generator" id="hrForm">
    <div class="card" style="min-width:0">
      <h2>Your Redirects</h2>
      ''' + F('hrList', 'Old URL and New URL', HR_SAMPLE, em='one pair per line, separated by a space', tag='textarea', mono=True, extra=' style="min-height:220px"') + '''
      ''' + F('hrSite', 'Your Domain', 'https://www.example.com', em='used for new URLs written as paths', mono=True) + '''
      ''' + R2(F('hrType', 'Redirect Type', '301', tag='select', opts=[('301', '301 Permanent (recommended)'), ('308', '308 Permanent'), ('302', '302 Temporary')]),
               F('hrMethod', 'Rule Style', 'match', tag='select', opts=[('match', 'RedirectMatch, exact URL'), ('rewrite', 'RewriteRule (mod_rewrite)'), ('redirect', 'Redirect, URL and everything below it')])) + '''
      ''' + CK('hrSlash', 'Match each old URL with or without the trailing slash', True) + '''
      ''' + CK('hrFlat', 'Fix chains by sending every old URL straight to its final page', True) + '''
      ''' + R2(F('hrHttps', 'Force HTTPS', 'yes', tag='select', opts=[('yes', 'Yes'), ('no', 'No')]),
               F('hrWww', 'Preferred Host', 'keep', tag='select', opts=[('keep', 'Keep as is'), ('www', 'Force www'), ('bare', 'Force no www')])) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your .htaccess Rules</h2>
      <div class="stats">''' + S('hrCount', 'Redirects') + S('hrChains', 'Chains Fixed') + S('hrErr', 'Problems') + '''</div>
      <div class="kw-result" id="hrCheck"></div>
      <pre class="code-out" id="hrOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="hrCopy">Copy Rules</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Before you paste</strong><ul><li>Download a backup of your current .htaccess file</li><li>In WordPress, paste the rules above the <code># BEGIN WordPress</code> line</li><li>Test a few old URLs in a private window afterwards</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var out = '';
  function rx(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/ /g, '\\s'); }
  function dec(s){ try { return decodeURIComponent(s); } catch(e){ return s; } }
  function q(s){ return /[\s"]/.test(s) ? '"' + s.replace(/"/g, '\\"') + '"' : s; }
  function key(path, slash){ var p = path.split('?')[0]; return (slash && p.length > 1 ? p.replace(/\/$/, '') : p) + (path.indexOf('?') > -1 ? '?' + path.split('?')[1] : ''); }
  function gen(){
    var iss = [], site = absUrl(v('hrSite')), type = $('hrType').value, method = $('hrMethod').value, slash = $('hrSlash').checked;
    var https = $('hrHttps').value === 'yes', www = $('hrWww').value;
    if (!site) iss.push(['bad', 'Your domain must be a full URL, like ' + c('https://www.example.com') + '.']);
    var origin = site ? site.origin : 'https://www.example.com';
    var pairs = [], seen = {};
    v('hrList').split(/\r?\n/).forEach(function(line, i){
      line = line.trim(); if (!line || line[0] === '#') return;
      var parts = line.split(/[\s,\t]+/);
      if (parts.length < 2){ iss.push(['bad', 'Line ' + (i + 1) + ' needs an old URL and a new URL.']); return; }
      var o = parts[0], n = parts[1], ou = absUrl(o), op;
      if (ou){ op = ou.pathname + ou.search; if (site && ou.host !== site.host && ou.host.replace(/^www\./, '') !== site.host.replace(/^www\./, '')) iss.push(['warn', 'Line ' + (i + 1) + ': ' + c(ou.host) + ' is not your domain. These rules only work in the .htaccess file of the site that receives the old URL.']); }
      else if (o[0] === '/') op = o;
      else { iss.push(['bad', 'Line ' + (i + 1) + ': the old URL ' + c(o) + ' must be a full URL or start with ' + c('/') + '.']); return; }
      op = op.replace(/#.*$/, '');
      var nu = absUrl(n) || (n[0] === '/' ? absUrl(origin + n) : null);
      if (!nu){ iss.push(['bad', 'Line ' + (i + 1) + ': the new URL ' + c(n) + ' must be a full URL or start with ' + c('/') + '.']); return; }
      var target = nu.href;
      var k = key(op, slash);
      if (seen[k]){ iss.push(['bad', 'Line ' + (i + 1) + ': ' + c(op) + ' is already redirected on line ' + seen[k] + '. Only the first rule would run, so this line was skipped.']); return; }
      if (nu.origin === origin && key(nu.pathname + nu.search, slash) === k){ iss.push(['bad', 'Line ' + (i + 1) + ': ' + c(op) + ' redirects to itself, which creates a loop. It was skipped.']); return; }
      if (op === '/') iss.push(['warn', 'Line ' + (i + 1) + ' redirects your home page. Make sure that is intended.']);
      seen[k] = i + 1;
      pairs.push({line: i + 1, old: op, k: k, target: target});
    });
    var map = {}; pairs.forEach(function(p){ map[p.k] = p; });
    var chains = 0;
    pairs.forEach(function(p){
      var t = p.target, hops = 0, visited = {}; visited[p.k] = 1;
      while (true){
        var tu = absUrl(t); if (!tu || tu.origin !== origin) break;
        var tk = key(tu.pathname + tu.search, slash), nx = map[tk];
        if (!nx) break;
        if (visited[tk]){ p.loop = true; break; }
        visited[tk] = 1; t = nx.target; hops++;
      }
      if (p.loop) iss.push(['bad', c(p.old) + ' is part of a redirect loop. Change one of the new URLs.']);
      else if (hops){
        if ($('hrFlat').checked){ chains++; p.final = t; }
        else iss.push(['warn', c(p.old) + ' goes through ' + (hops + 1) + ' redirects before it reaches ' + c(t) + '. Turn on chain fixing to send it there directly.']);
      }
    });
    if (chains) iss.push(['warn', chains + ' redirect chain' + (chains > 1 ? 's were' : ' was') + ' fixed, so old URLs now go straight to their final page.']);
    var needRw = pairs.some(function(p){ return p.old.indexOf('?') > -1; }) || https || www !== 'keep';
    var style = method;
    if (needRw && method !== 'rewrite'){
      style = 'rewrite';
      iss.push(['warn', 'Switched every rule to ' + c('RewriteRule') + ' because ' + (pairs.some(function(p){ return p.old.indexOf('?') > -1; }) ? 'some old URLs have query strings' : 'you chose HTTPS or host rules') + '. Mixing rule styles makes the order hard to predict.']);
    }
    var L = ['# Redirects for ' + (site ? site.host : 'your site')];
    if (style === 'rewrite') L.push('RewriteEngine On');
    var list = pairs.filter(function(p){ return !p.loop; });
    if (style === 'redirect'){
      list = list.slice().sort(function(a, b){ return b.old.length - a.old.length; });
      list.forEach(function(p, i){ list.slice(i + 1).forEach(function(o){ if (o.old !== '/' && p.old.indexOf(o.old.replace(/\/$/, '') + '/') === 0) iss.push(['warn', c(p.old) + ' sits inside ' + c(o.old) + '. It was placed first so it still works.']); }); });
    }
    list.forEach(function(p){
      var t = p.final || p.target, path = dec(p.old.split('?')[0]), qs = p.old.split('?')[1];
      var last = path.split('/').pop(), opt = slash && path.length > 1 && (/\/$/.test(path) || last.indexOf('.') < 0);
      var base = opt ? path.replace(/\/$/, '') : path;
      if (style === 'redirect'){ L.push('Redirect ' + type + ' ' + q(path) + ' ' + q(t)); return; }
      if (style === 'match'){
        if (/\$/.test(t)) iss.push(['warn', 'The new URL ' + c(t) + ' contains ' + c('$') + ', which RedirectMatch treats as a capture. Use RewriteRule instead.']);
        L.push('RedirectMatch ' + type + ' ' + q('^' + rx(base) + (opt ? '/?' : '') + '$') + ' ' + q(t)); return;
      }
      var pat = '^' + rx(base.replace(/^\//, '')) + (opt ? '/?' : '') + '$';
      if (base === '/') pat = '^$';
      var flags = ['R=' + type, 'L'], tq = absUrl(t);
      if (/%/.test(t)) flags.push('NE');
      if (qs && !(tq && tq.search)) flags.push('QSD');
      if (qs) L.push('RewriteCond %{QUERY_STRING} ^' + rx(qs) + '$');
      L.push('RewriteRule ' + q(pat) + ' ' + q(t.replace(/([%$])/g, '\\$1')) + ' [' + flags.join(',') + ']');
    });
    if (https || www !== 'keep'){
      var host = site ? site.host.replace(/^www\./, '') : 'example.com', want = www === 'www' ? 'www.' + host : www === 'bare' ? host : null;
      var scheme = https ? 'https' : (site ? site.protocol.replace(':', '') : 'https');
      L.push(''); L.push('# ' + (https ? 'Force HTTPS' : '') + (https && want ? ' and ' : '') + (want ? 'use ' + want : ''));
      var conds = [];
      if (https) conds.push('RewriteCond %{HTTPS} off');
      if (www === 'www') conds.push('RewriteCond %{HTTP_HOST} !^www\\. [NC]');
      if (www === 'bare') conds.push('RewriteCond %{HTTP_HOST} ^www\\. [NC]');
      conds.forEach(function(cd, i){ if (i < conds.length - 1) cd = /\[NC\]$/.test(cd) ? cd.replace('[NC]', '[NC,OR]') : cd + ' [OR]'; L.push(cd); });
      L.push('RewriteRule ^ ' + scheme + '://' + (want || '%{HTTP_HOST}') + '%{REQUEST_URI} [L,R=301]');
      if (site && want && site.host !== want) iss.push(['warn', 'Your domain is ' + c(site.host) + ' but you chose to force ' + c(want) + '. New URLs above use ' + c(site.host) + ', which would add an extra hop.']);
      if (site && https && site.protocol !== 'https:') iss.push(['warn', 'Your domain starts with http, but you chose to force HTTPS. Use ' + c('https://') + ' in the domain field.']);
    }
    out = L.join('\n') + '\n';
    $('hrOut').textContent = out;
    $('hrCount').textContent = list.length; $('hrChains').textContent = chains; $('hrErr').textContent = iss.filter(function(i){ return i[0] === 'bad'; }).length;
    if (type === '302') iss.push(['warn', '302 redirects are temporary, so Google keeps the old URL in results. Use 301 for moves that will not be undone.']);
    issues('hrCheck', iss, '<strong>' + list.length + ' redirect' + (list.length === 1 ? '' : 's') + ' ready.</strong> Paste the rules near the top of your .htaccess file.');
  }
  $('hrForm').addEventListener('input', gen); $('hrForm').addEventListener('change', gen);
  $('hrCopy').onclick = function(){ copyText(out, 'toast'); };
  gen();
''',
        content='''
    <h2>What Is an Htaccess Redirect Generator?</h2>
    <p>When you change a URL, delete a page or move to a new site structure, a redirect sends visitors and search engines from the old address to the new one. On Apache and LiteSpeed hosting, which includes most shared hosting, these rules live in a file called <code>.htaccess</code> at the root of your site.</p>
    <p>Writing the rules by hand is slow and easy to get wrong. This generator turns a simple list of old and new URLs into correct rules, and checks the list for problems like chains, loops and duplicates first.</p>

    <h2>How to Use the Redirect Generator</h2>
    <ol>
      <li><strong>Paste your redirects</strong>, one per line: the old URL, a space, then the new URL.</li>
      <li><strong>Enter your domain</strong> so new URLs written as paths become full URLs.</li>
      <li><strong>Choose 301</strong> for permanent moves. Use 302 only when the old page is coming back.</li>
      <li><strong>Pick a rule style.</strong> RedirectMatch redirects the exact URL only, which is the safest choice.</li>
      <li><strong>Copy the rules</strong> into your <code>.htaccess</code> file, near the top, then test a few old URLs.</li>
    </ol>

    <h2>Redirect Types and Rule Styles</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Option', 'What it does') + '''
      <tbody>
        <tr><td>301 and 308</td><td>Permanent. Google shows the new URL in results and passes signals to it</td></tr>
        <tr><td>302</td><td>Temporary. Google keeps showing the old URL</td></tr>
        <tr><td><code>RedirectMatch</code></td><td>Matches one exact path, with or without the trailing slash</td></tr>
        <tr><td><code>Redirect</code></td><td>Matches the path and everything below it, and keeps the rest of the path</td></tr>
        <tr><td><code>RewriteRule</code></td><td>Needed for old URLs with query strings, and for HTTPS or www rules</td></tr>
      </tbody>
    </table></div>
    <p>Google explains how it treats each status code in <a href="https://developers.google.com/search/docs/crawling-indexing/301-redirects" ''' + EXT + '''>redirects and Google Search</a>, and the Apache manual covers <a href="https://httpd.apache.org/docs/current/mod/mod_alias.html" ''' + EXT + '''><code>Redirect</code> and <code>RedirectMatch</code></a> in detail. Apache runs the first rule that matches, so the order of your rules matters.</p>

    <h2>Tips for Safe Redirects</h2>
    <ul>
      <li><strong>Redirect to the closest match</strong>, not the home page. A redirect to an unrelated page may be treated as a soft 404.</li>
      <li><strong>Avoid chains.</strong> Each extra hop slows visitors down. This tool points every old URL straight to its final page.</li>
      <li><strong>Update internal links too.</strong> Redirects are a safety net. Your menus and posts should link to the new URLs directly.</li>
      <li><strong>Keep redirects in place</strong> for as long as old links and bookmarks may still be used. For a site move that means years.</li>
      <li><strong>Not on Apache?</strong> Nginx does not read <code>.htaccess</code>. Ask your host or use a redirect plugin instead.</li>
    </ul>

    <h2>Learn More About Redirects</h2>
    <p>Understand every status code in <a href="''' + B + '''http-status-codes-for-seo-explained/">HTTP status codes for SEO</a>, plan a safe switch with <a href="''' + B + '''https-migration-seo-impact/">the SEO impact of moving to HTTPS</a>, and manage redirects in code with our <a href="''' + B + '''redirect-manager-in-php/">redirect manager in PHP</a>. Moving pages around? Update your sitemap with the <a href="''' + T + '''xml-sitemap-generator/">XML sitemap generator</a>.</p>
''',
        faqs=[
            ("Should I use a 301 or 302 redirect?", "Use a 301 when the move is permanent, which is almost always the case for SEO. Google then shows the new URL in results. Use a 302 only when the old page will come back soon."),
            ("Where do I put the redirect rules?", "Paste them near the top of the .htaccess file in your site root. In WordPress, put them above the BEGIN WordPress block so WordPress does not handle the URL first."),
            ("Why do old URLs with a question mark not redirect?", "Simple Redirect rules cannot match query strings. The generator detects old URLs with a question mark and writes RewriteRule code with a query string condition instead."),
            ("What is a redirect chain?", "A chain is when page A redirects to B and B redirects to C. It slows visitors and wastes crawling. Turn on chain fixing and the tool sends A straight to C."),
        ],
        related=[("HTTP Status Codes for SEO", "http-status-codes-for-seo-explained"), ("HTTPS Migration SEO Impact", "https-migration-seo-impact"),
                 ("Redirect Manager in PHP", "redirect-manager-in-php"), ("Soft 404 Errors Explained", "soft-404-errors-explained")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'technical-seo-tools'; t['updated'] = '2026-11-04'
