"""Batch 8 (2026-11-05): Google Ads Tools category, 7 tools.
Facts checked 2026-11-05 against: Google Ads Help "About responsive search ads" (7684791: up to 15 headlines and 4
descriptions, minimum 3 and 2, headline 30, description 90, path 15, double width characters count as 2, up to 3
headlines shown, H1 and D1 usually show, pins to H1, H2 and D1 always show, H3 and D2 not guaranteed, 2 or 3 assets per
pinned position, every position pinned means unpinned assets never show), "Set up keyword insertion" (6371157:
{keyword:default text} syntax and capitalization styles, default text used when the keyword cannot be inserted),
"Set up tracking with ValueTrack parameters" (6305348: parameter list and values, {lpurl} only in tracking templates,
template must contain a URL insertion parameter, ? replaced with & when the final URL already has a query string),
"Final URL suffix and tracking templates" (9695952: suffix for landing page parameters, only ValueTrack parameters),
"Create custom parameters" (6325879: up to 8 per level, name up to 16 alphanumeric characters, value up to 250,
no account level), "About negative keywords" (2453972: negative broad, phrase and exact behaviour, no close variants,
disallowed symbols , ! @ % ^ ( ) = { } ; ~ ` < > ? \\ |, minus inside a keyword ignored), "Add keywords" (7476658: up to
10 words, match type formatting), Google Ads API KeywordInfo (80 characters), Ads editorial policies (6021546, 14847994:
repeated punctuation, gimmicky capitalization, extra spacing, unsupported characters such as emoji), and the asset
limits sitelink text 25, sitelink description lines 35, callouts 25, structured snippet values 25 (3 to 10 per header),
business name 25."""
import html as _h

T = 'https://brandella.in/tools/google-ads-tools/'
PPC = 'https://brandella.in/tools/ppc-calculators/'
ANL = 'https://brandella.in/tools/analytics-tools/'
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
def CK(i, label, on=True, cls=''): return f'<label class="check"><input id="{i}" type="checkbox"' + (f' class="{cls}"' if cls else '') + (' checked' if on else '') + f'> <span>{label}</span></label>'
PRE = 'style="display:block;margin-top:0;max-height:520px;overflow:auto;word-break:normal;overflow-wrap:anywhere"'
def ST_(base, extra): return base[:-1] + ';' + extra + '"'
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
    else if (warn.length) say(id, 'warn', '<strong>Looks good, with ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') + '.</strong>' + li(warn));
    else say(id, 'ok', okMsg);
  }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
  function fmtN(n){ return Number(n).toLocaleString('en-IN'); }
  function lines(id){ return String($(id).value).split(/\r?\n/).map(function(s){ return s.trim(); }).filter(Boolean); }
  function download(name, text, type){
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: (type || 'text/plain') + ';charset=utf-8'}));
    a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
  }
  function csvCell(s){ s = String(s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  // Google Ads counts double width characters (Chinese, Japanese, Korean) as 2
  function wide(cp){ return (cp >= 0x1100 && cp <= 0x115F) || (cp >= 0x2E80 && cp <= 0xA4CF) || (cp >= 0xAC00 && cp <= 0xD7A3) || (cp >= 0xF900 && cp <= 0xFAFF) || (cp >= 0xFE30 && cp <= 0xFE4F) || (cp >= 0xFF00 && cp <= 0xFF60) || (cp >= 0xFFE0 && cp <= 0xFFE6) || (cp >= 0x20000 && cp <= 0x3FFFD); }
  function glen(s){ var n = 0; for (var ch of String(s)) n += wide(ch.codePointAt(0)) ? 2 : 1; return n; }
  // Keyword insertion: {keyword:default text}
  var DKI = /\{(keyword):([^{}]*)\}/gi, DKI1 = /\{keyword:[^{}]*\}/i;
  function dkiDefault(s){ return String(s).replace(DKI, function(m, k, d){ return d; }); }
  function capWord(w){ return w ? w.charAt(0).toUpperCase() + w.slice(1).toLowerCase() : w; }
  function dkiStyle(k, kw){
    var w = kw.toLowerCase().split(/\s+/).filter(Boolean);
    if (k === 'keyword') return w.join(' ');
    if (k === 'Keyword') return w.length ? capWord(w[0]) + (w.length > 1 ? ' ' + w.slice(1).join(' ') : '') : '';
    if (k === 'KeyWord') return w.map(capWord).join(' ');
    if (k === 'KEYWord') return w.map(function(x, i){ return i === 0 ? x.toUpperCase() : capWord(x); }).join(' ');
    if (k === 'KeyWORD') return w.map(function(x, i){ return i === 0 ? capWord(x) : x.toUpperCase(); }).join(' ');
    return w.map(capWord).join(' ');
  }
  function dkiFill(s, kw, limit){
    if (!DKI1.test(s)) return s;
    if (!kw) return dkiDefault(s);
    var out = String(s).replace(DKI, function(m, k){ return dkiStyle(k, kw); });
    return glen(out) <= limit ? out : dkiDefault(s);
  }
  function dkiCheck(s){
    var bad = [];
    String(s).replace(DKI, function(m, k){ if (['keyword', 'Keyword', 'KeyWord', 'KEYWord', 'KeyWORD'].indexOf(k) < 0) bad.push(k); return m; });
    if (/\{[^}]*$/.test(s) || /\{(?!keyword:)[^}]*\}/i.test(s)) bad.push('syntax');
    return bad;
  }
  var ACRO = /^(UK|USA|UAE|EMI|GST|COD|SUV|LED|HD|PDF|SEO|PPC|CRM|SAAS|NASA|ISO|IIT|MBA|BBA|NEET|JEE|ICSE|CBSE|IELTS|GMAT|ASAP|FAQ|ATM|AC|TV|PC|USB|DSLR|OLED|QLED|SIM|UPI|EV|NGO|HR|IT|AI|API|CEO|SME|MSME|ISI|BIS|FSSAI|HDFC|ICICI|SBI|IKEA|LG|BMW|ASICS)$/;
  // Editorial checks Google applies to ad text
  function policy(s){
    var out = [];
    if (/([!?.,;:])\1/.test(s)) out.push('repeats punctuation, like ' + c((s.match(/([!?.,;:])\1+/) || [''])[0]) + ', which Google disapproves');
    if (/\p{Extended_Pictographic}/u.test(s)) out.push('contains an emoji or symbol Google does not support in ad text');
    if (/\s{2,}/.test(s)) out.push('has extra spaces between words');
    var caps = (dkiDefault(s).match(/\b[A-Z]{4,}\b/g) || []).filter(function(w){ return !ACRO.test(w); });
    if (caps.length) out.push('uses ' + c(caps[0]) + ' in capitals. Google only allows this for acronyms and brand names');
    if (/[a-z][@$][a-z]|[a-z][013][a-z]{2}/i.test(s)) out.push('may use numbers or symbols in place of letters');
    var bad = dkiCheck(s);
    if (bad.length) out.push('has keyword insertion code Google may not read. Use ' + c('{KeyWord:Default text}'));
    return out;
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. GOOGLE ADS PREVIEW TOOL ----------
    HS = [('{KeyWord:Running Shoes} Sale', ''), ('Free Delivery Across India', ''), ('Up to 40% Off Top Brands', ''),
          ('Easy 30 Day Returns', ''), ('Shop Nike, Puma and Asics', ''), ('Cash on Delivery Available', ''),
          ('Stride Sports Official Store', ''), ('New Arrivals Every Week', ''), ('Cushioned Shoes for Daily Runs', ''),
          ('Sizes UK 6 to 12 in Stock', '')] + [('', '')] * 5
    DS = ['Shop running shoes from top brands with free delivery, easy returns and cash on delivery.',
          'Light, cushioned shoes for road and trail. Find your perfect size and order today.',
          'Over 500 styles in stock. Get expert fit advice from our team on chat, 7 days a week.', '']
    def hrow(i, t):
        opts = ''.join(f'<option value="{v}">{l}</option>' for v, l in [('', 'Any'), ('1', 'H1'), ('2', 'H2'), ('3', 'H3')])
        return (f'<div style="display:grid;grid-template-columns:1fr 64px 46px;gap:6px;align-items:center;margin-bottom:6px">'
                f'<input id="apH{i}" class="apF" type="text" autocomplete="off" aria-label="Headline {i+1}" placeholder="Headline {i+1}" value="{_h.escape(t)}" style="width:100%;border:1px solid #cfcfcf;border-radius:8px;padding:8px 10px;font:inherit;font-size:14.5px;min-width:0">'
                f'<select id="apHP{i}" class="apF" aria-label="Pin headline {i+1}" style="border:1px solid #cfcfcf;border-radius:8px;padding:8px 4px;font:inherit;font-size:13px;background:#fff">{opts}</select>'
                f'<small id="apHC{i}" style="font-size:12.5px;font-weight:700;text-align:right;color:#6b6b6b">0</small></div>')
    def drow(i, t):
        opts = ''.join(f'<option value="{v}">{l}</option>' for v, l in [('', 'Any'), ('1', 'D1'), ('2', 'D2')])
        return (f'<div style="display:grid;grid-template-columns:1fr 64px 46px;gap:6px;align-items:start;margin-bottom:6px">'
                f'<textarea id="apD{i}" class="apF" aria-label="Description {i+1}" placeholder="Description {i+1}" spellcheck="false" style="width:100%;border:1px solid #cfcfcf;border-radius:8px;padding:8px 10px;font:inherit;font-size:14.5px;min-height:62px;resize:vertical;min-width:0">{_h.escape(t)}</textarea>'
                f'<select id="apDP{i}" class="apF" aria-label="Pin description {i+1}" style="border:1px solid #cfcfcf;border-radius:8px;padding:8px 4px;font:inherit;font-size:13px;background:#fff">{opts}</select>'
                f'<small id="apDC{i}" style="font-size:12.5px;font-weight:700;text-align:right;color:#6b6b6b;padding-top:9px">0</small></div>')
    TOOLS.append(dict(
        slug='google-ads-preview-tool', short='AP', name='Google Ads Preview Tool',
        card='Write a responsive search ad and preview how Google shows it on mobile and desktop, with pins and keyword insertion.',
        title='Google Ads Preview Tool: Responsive Search Ad Mockup',
        desc='Free Google Ads preview tool. Write up to 15 headlines and 4 descriptions, pin assets, test keyword insertion and see your ad on mobile and desktop.',
        h1='Google Ads Preview Tool',
        lead='Type your headlines and descriptions to see how your responsive search ad can look in Google on mobile and desktop. Shuffle through combinations, test pins and keyword insertion, and catch policy problems before you publish.',
        tool='''<section class="tool" aria-label="Google Ads preview tool" id="apForm">
    <div class="card" style="min-width:0">
      <h2>Your Ad</h2>
      ''' + F('apUrl', 'Final URL', 'https://www.example.in/running-shoes/', mono=True) + '''
      ''' + R2(F('apP1', 'Path 1', 'Running', em='15 max'), F('apP2', 'Path 2', 'Shoes', em='15 max')) + '''
      ''' + R2(F('apBiz', 'Business Name', 'Stride Sports', em='25 max'), F('apKw', 'Test Keyword', 'running shoes for men', em='for keyword insertion')) + '''
      <div class="field"><label>Headlines <em>30 characters, 3 to 15</em></label>''' + ''.join(hrow(i, t) for i, (t, p) in enumerate(HS)) + '''</div>
      <div class="field"><label>Descriptions <em>90 characters, 2 to 4</em></label>''' + ''.join(drow(i, t) for i, t in enumerate(DS)) + '''</div>
      ''' + F('apSl', 'Sitelinks', "Men's Running Shoes\nWomen's Running Shoes\nTrail Shoes\nSale Under 2999", em='one per line, 25 max', tag='textarea') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Ad Preview</h2>
      <div class="tabs" id="apTabs"><button type="button" class="on" data-d="m">Mobile</button><button type="button" data-d="d">Desktop</button></div>
      <div class="serp mobile" id="apSerp">
        <div style="font-size:14px;font-weight:700;color:#202124;margin-bottom:8px">Sponsored</div>
        <div class="g-site"><div class="g-fav" id="apFav">S</div><div style="min-width:0"><div class="g-name" id="apName"></div><div class="g-url" id="apDisp"></div></div></div>
        <div class="g-title" id="apTitle"></div>
        <div class="g-desc" id="apDesc"></div>
        <div id="apLinks" style="display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:10px;font-size:14px"></div>
      </div>
      <div class="actions"><button class="btn dark" id="apShuffle" type="button">Show Another Combination</button><button class="btn" id="apCopy" type="button">Copy Ad Text</button><span class="toast" id="toast">Copied!</span></div>
      <div class="stats" style="margin-top:18px">''' + S('apHn', 'Headlines') + S('apDn', 'Descriptions') + S('apCombo', 'Combinations') + '''</div>
      <div class="kw-result" id="apCheck"></div>
      <div class="tips"><strong>What Google guarantees</strong><ul><li>Headline 1 and Description 1 usually show</li><li>Headline 3 and Description 2 may not show, so keep key details out of them</li><li>Text pinned to Headline 1, Headline 2 or Description 1 always shows</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var device = 'm', seed = 7, shown = {h: [], d: []};
  function rnd(n){ seed = (seed * 9301 + 49297) % 233280; return Math.floor(seed / 233280 * n); }
  function assets(kind, n, limit){
    var out = [];
    for (var i = 0; i < n; i++){
      var t = $('ap' + kind + i).value.replace(/^\s+|\s+$/g, ''), pin = $('ap' + kind + 'P' + i).value;
      var len = glen(dkiDefault(t)), cEl = $('ap' + kind + 'C' + i);
      cEl.textContent = t ? len + '/' + limit : '';
      cEl.style.color = len > limit ? '#d1351f' : len > limit - 3 ? '#c47a00' : '#3d8f12';
      if (t) out.push({t: t, pin: pin, i: i, len: len});
    }
    return out;
  }
  function perm(n, k){ var r = 1; for (var i = 0; i < k; i++) r *= Math.max(n - i, 0); return r; }
  function slots(list, count){
    var res = [], used = {}, free = list.filter(function(a){ return !a.pin; });
    for (var p = 1; p <= count; p++){
      var pinned = list.filter(function(a){ return a.pin === String(p); });
      var pool = pinned.length ? pinned : free.filter(function(a){ return !used[a.i]; });
      if (!pool.length) continue;
      var a = pool[rnd(pool.length)]; used[a.i] = 1; res.push(a);
    }
    return res;
  }
  function combos(list, count){
    var total = 1, freeSlots = 0;
    for (var p = 1; p <= count; p++){ var k = list.filter(function(a){ return a.pin === String(p); }).length; if (k) total *= k; else freeSlots++; }
    var free = list.filter(function(a){ return !a.pin; }).length;
    return total * perm(free, Math.min(freeSlots, free));
  }
  function render(){
    var H = assets('H', 15, 30), D = assets('D', 4, 90), iss = [], kw = v('apKw');
    var u = null; try { u = new URL(v('apUrl')); } catch(e){}
    if (!u || !/^https?:$/.test(u.protocol)) iss.push(['bad', 'Add a full final URL starting with ' + c('https://') + '.']);
    var host = u ? u.hostname : 'www.example.com', p1 = v('apP1'), p2 = v('apP2'), biz = v('apBiz');
    [['Path 1', p1, 15], ['Path 2', p2, 15], ['Business name', biz, 25]].forEach(function(x){ if (glen(dkiDefault(x[1])) > x[2]) iss.push(['bad', x[0] + ' is ' + glen(dkiDefault(x[1])) + ' characters. The limit is ' + x[2] + '.']); });
    if (p2 && !p1) iss.push(['bad', 'Fill in Path 1 before Path 2.']);
    if (/\s/.test(p1 + p2)) iss.push(['warn', 'Display paths read best without spaces. Try ' + c((p1 || p2).replace(/\s+/g, '')) + '.']);
    if (H.length < 3) iss.push(['bad', 'Add at least 3 headlines. Google needs 3 to save the ad.']);
    if (D.length < 2) iss.push(['bad', 'Add at least 2 descriptions. Google needs 2 to save the ad.']);
    H.concat(D).forEach(function(a){
      var lim = H.indexOf(a) > -1 ? 30 : 90, name = (lim === 30 ? 'Headline ' : 'Description ') + (a.i + 1);
      if (a.len > lim) iss.push(['bad', name + ' is ' + a.len + ' characters. Cut ' + (a.len - lim) + ' to fit the ' + lim + ' limit.']);
      policy(a.t).forEach(function(m){ iss.push(['warn', name + ' ' + m + '.']); });
    });
    var seen = {};
    H.concat(D).forEach(function(a){ var k = dkiDefault(a.t).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim(); if (seen[k]) iss.push(['warn', c(a.t) + ' repeats another asset. Duplicates add no new combinations.']); seen[k] = 1; });
    [1, 2, 3].forEach(function(p){ var k = H.filter(function(a){ return a.pin === String(p); }).length; if (k === 1) iss.push(['warn', 'Only one headline is pinned to position ' + p + '. Google suggests 2 or 3 options per pinned spot.']); });
    if (H.length && [1, 2, 3].every(function(p){ return H.some(function(a){ return a.pin === String(p); }); }) && H.some(function(a){ return !a.pin; }))
      iss.push(['warn', 'Every headline position is pinned, so your unpinned headlines will never show.']);
    if (H.some(function(a){ return a.pin === '3'; }) && !H.some(function(a){ return a.pin === '1' || a.pin === '2'; })) iss.push(['warn', 'Headline 3 is not guaranteed to show. Pin must show text to position 1 or 2.']);
    if (kw){
      var k = kw.toLowerCase(), hit = H.some(function(a){ return DKI1.test(a.t) || dkiDefault(a.t).toLowerCase().indexOf(k) > -1; });
      if (!hit) iss.push(['warn', 'No headline contains ' + c(kw) + '. Using the keyword in at least one headline makes the ad more relevant.']);
      H.forEach(function(a){ if (DKI1.test(a.t)){ var f = dkiFill(a.t, kw, 30); if (f === dkiDefault(a.t)) iss.push(['warn', 'In Headline ' + (a.i + 1) + ', ' + c(kw) + ' is too long to insert, so Google shows the default text ' + c(f) + '.']); } });
    }
    if (H.length < 8 && H.length >= 3) iss.push(['warn', 'You have ' + H.length + ' headlines. Adding more unique ones gives Google more combinations to test.']);
    // build preview
    var hs = slots(H, 3), ds = slots(D, 2);
    if (device === 'm'){ hs = hs.slice(0, 3); }
    shown = {h: hs.map(function(a){ return dkiFill(a.t, kw, 30); }), d: ds.map(function(a){ return dkiFill(a.t, kw, 90); })};
    $('apTitle').textContent = shown.h.join(' | ') || 'Your headline here';
    $('apDesc').textContent = shown.d.join(' ') || 'Your description here.';
    $('apName').textContent = biz || host.replace(/^www\./, '');
    $('apFav').textContent = (biz || host.replace(/^www\./, '')).charAt(0).toUpperCase();
    var path = [dkiFill(p1, kw, 15), dkiFill(p2, kw, 15)].filter(Boolean).join('/');
    $('apDisp').textContent = host + (path ? '/' + path : '');
    var sl = lines('apSl');
    sl.forEach(function(s){ if (glen(s) > 25) iss.push(['bad', 'Sitelink ' + c(s) + ' is ' + glen(s) + ' characters. The limit is 25.']); });
    $('apLinks').innerHTML = sl.slice(0, device === 'm' ? 4 : 6).map(function(s){ return '<span style="color:' + (device === 'm' ? '#1558d6' : '#1a0dab') + '">' + esc(s) + '</span>'; }).join('');
    $('apSerp').className = 'serp' + (device === 'm' ? ' mobile' : '');
    $('apHn').textContent = H.length + '/15'; $('apDn').textContent = D.length + '/4';
    var cb = combos(H, 3) * combos(D, 2); $('apCombo').textContent = cb > 99999 ? '99,999+' : fmtN(cb);
    issues('apCheck', iss, '<strong>Your ad is ready.</strong> Every asset fits its limit and passes the quick policy checks.');
  }
  $('apForm').addEventListener('input', render); $('apForm').addEventListener('change', render);
  document.querySelectorAll('#apTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#apTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); device = b.getAttribute('data-d'); render(); }); });
  $('apShuffle').onclick = function(){ seed = (seed + 1 + Math.floor(Math.random() * 1000)) % 233280; render(); };
  $('apCopy').onclick = function(){
    var H = assets('H', 15, 30), D = assets('D', 4, 90);
    copyText('Headlines\n' + H.map(function(a){ return a.t + (a.pin ? '  (pinned to H' + a.pin + ')' : ''); }).join('\n') + '\n\nDescriptions\n' + D.map(function(a){ return a.t + (a.pin ? '  (pinned to D' + a.pin + ')' : ''); }).join('\n'), 'toast');
  };
  render();
''',
        content='''
    <h2>What Is a Google Ads Preview Tool?</h2>
    <p>A responsive search ad is a set of up to 15 headlines and 4 descriptions. Google mixes them into different combinations for each search, so you never write one fixed ad. That makes it hard to picture what people will actually see.</p>
    <p>This Google Ads preview tool builds a realistic mockup of a sponsored result on mobile and desktop. Click to shuffle through the combinations Google could show, test pins and keyword insertion, and fix limits and policy issues before your ad goes for review.</p>

    <h2>How to Use the Google Ads Preview Tool</h2>
    <ol>
      <li><strong>Add your final URL</strong> and up to two display paths. The domain comes from your URL.</li>
      <li><strong>Write at least 3 headlines and 2 descriptions.</strong> The counter beside each one turns red if it is over the limit.</li>
      <li><strong>Pin only when you must.</strong> Choose H1, H2 or H3 for a headline, or D1 or D2 for a description.</li>
      <li><strong>Type a test keyword</strong> to see how keyword insertion fills in your ad.</li>
      <li><strong>Click Show Another Combination</strong> a few times and read every version out loud. Each one must make sense.</li>
    </ol>

    <h2>Responsive Search Ad Limits</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Asset', 'Limit', 'How many') + '''
      <tbody>
        <tr><td>Headline</td><td>30 characters</td><td>3 to 15, up to 3 shown at once</td></tr>
        <tr><td>Description</td><td>90 characters</td><td>2 to 4, up to 2 shown at once</td></tr>
        <tr><td>Display path</td><td>15 characters each</td><td>2 paths</td></tr>
        <tr><td>Business name</td><td>25 characters</td><td>1</td></tr>
        <tr><td>Sitelink text</td><td>25 characters</td><td>Up to 4 on mobile</td></tr>
      </tbody>
    </table></div>
    <p>Chinese, Japanese and Korean characters count as two each. You can read the full rules in Google's guide <a href="https://support.google.com/google-ads/answer/7684791" ''' + EXT + '''>about responsive search ads</a>.</p>

    <h3>How Keyword Insertion Works</h3>
    <p>Write <code>{KeyWord:Running Shoes}</code> and Google swaps in the keyword that matched the search. <code>{keyword:...}</code> keeps it in lower case, <code>{Keyword:...}</code> capitalizes the first word and <code>{KeyWord:...}</code> capitalizes every word. If the keyword would push the headline over 30 characters, Google shows your default text instead, and so does this preview.</p>

    <h2>Tips for Better Responsive Search Ads</h2>
    <ul>
      <li><strong>Make every headline stand alone.</strong> Any headline can appear next to any other, so avoid ones that only work as a pair.</li>
      <li><strong>Mix the angles.</strong> Write some headlines about the product, some about offers and some about trust, like delivery or returns.</li>
      <li><strong>Keep musts in guaranteed spots.</strong> Headline 3 and Description 2 do not always show, so never rely on them for prices or legal text.</li>
      <li><strong>Pin sparingly.</strong> Each pin cuts the number of combinations Google can test. If you pin, give that spot 2 or 3 options.</li>
    </ul>

    <h2>Learn More About Ad Copy</h2>
    <p>See how ads are ranked in <a href="''' + B + '''how-google-ads-auction-works/">how the Google Ads auction works</a>, learn how relevance lifts your <a href="''' + B + '''google-ads-quality-score-explained/">Quality Score</a>, and plan fair tests with <a href="''' + B + '''ppc-ad-copy-testing/">PPC ad copy testing</a>. Want to check every asset in one go? Paste them into the <a href="''' + T + '''google-ads-character-counter/">Google Ads character counter</a>.</p>
''',
        faqs=[
            ("Is this the same as the Google Ads Ad Preview and Diagnosis tool?", "No. Google's own tool shows whether a live ad is showing for a search. This tool is a mockup for ads you are still writing, so you can check the copy before it goes live."),
            ("Why does my ad show only two headlines?", "Google shows up to three headlines, but often drops the third one on smaller screens or when space is tight. That is why Headline 3 is never guaranteed."),
            ("Does pinning lower Ad Strength?", "Yes, it usually does. Pinning reduces the combinations Google can test. Pin only text that must always appear, such as a brand name or a legal line."),
            ("Why does the preview show my default text instead of the keyword?", "Keyword insertion falls back to the default text when the keyword would make the headline longer than 30 characters. Use a shorter keyword or shorter text around it."),
        ],
        related=[("Google Ads Quality Score Explained", "google-ads-quality-score-explained"), ("PPC Ad Copy Testing", "ppc-ad-copy-testing"),
                 ("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"), ("How the Google Ads Auction Works", "how-google-ads-auction-works")],
    ))

    # ---------- 2. GOOGLE ADS CHARACTER COUNTER ----------
    TOOLS.append(dict(
        slug='google-ads-character-counter', short='GC', name='Google Ads Character Counter',
        card='Count every headline, description, path, sitelink, callout and snippet against Google Ads limits in one go.',
        title='Google Ads Character Counter: Headlines and Assets',
        desc='Free Google Ads character counter. Check headlines (30), descriptions (90), paths, sitelinks, callouts and snippets in bulk, with policy checks built in.',
        h1='Google Ads Character Counter',
        lead='Paste all your ad text at once. Every headline, description, path, sitelink, callout and snippet value is counted against Google Ads limits, with warnings for duplicates and common policy problems.',
        tool='''<section class="tool" aria-label="Google Ads character counter" id="ccForm">
    <div class="card" style="min-width:0">
      <h2>Your Ad Text</h2>
      ''' + F('ccH', 'Headlines', 'Running Shoes for Men\nFree Delivery Across India\nUp to 40% Off Top Brands\nEasy 30 Day Returns\nShop Lightweight Running Shoes Now\nBest Price!!', em='one per line, 30 max', tag='textarea', extra=' style="min-height:150px"') + '''
      ''' + F('ccD', 'Descriptions', 'Shop running shoes from top brands with free delivery, easy returns and cash on delivery.\nLight, cushioned shoes for road and trail. Over 500 styles in stock with sizes from UK 6 to UK 12.', em='one per line, 90 max', tag='textarea') + '''
      ''' + R2(F('ccP1', 'Path 1', 'Running'), F('ccP2', 'Path 2', 'Mens-Shoes')) + '''
      ''' + F('ccBiz', 'Business Name', 'Stride Sports', em='25 max') + '''
      ''' + F('ccSl', 'Sitelink Text', "Men's Running Shoes\nWomen's Running Shoes\nTrail and Hiking Shoes for All\nSale", em='one per line, 25 max', tag='textarea') + '''
      ''' + F('ccSd', 'Sitelink Descriptions', 'Cushioned shoes for daily runs\nFree delivery on every order today', em='one per line, 35 max', tag='textarea') + '''
      ''' + F('ccCo', 'Callouts', 'Free Delivery\nCash on Delivery\n30 Day Returns\nGenuine Brands Only', em='one per line, 25 max', tag='textarea') + '''
      ''' + F('ccSn', 'Structured Snippet Values', 'Nike\nPuma\nAsics\nAdidas', em='one per line, 25 max', tag='textarea') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Character Counts</h2>
      <div class="stats">''' + S('ccN', 'Assets') + S('ccOk', 'Within Limit') + S('ccOver', 'Over Limit') + S('ccW', 'Warnings') + '''</div>
      <div class="kw-result" id="ccCheck"></div>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Asset</th><th>Text</th><th class="num">Count</th></tr></thead><tbody id="ccBody"></tbody></table></div>
      <div class="actions"><button class="btn dark" id="ccCsv" type="button">Download CSV</button><button class="btn" id="ccCopy" type="button">Copy Assets That Fit</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var rows = [];
  var TYPES = [['ccH', 'Headline', 30, 3, 15], ['ccD', 'Description', 90, 2, 4], ['ccP1', 'Path 1', 15, 0, 1], ['ccP2', 'Path 2', 15, 0, 1],
               ['ccBiz', 'Business name', 25, 0, 1], ['ccSl', 'Sitelink', 25, 0, 0], ['ccSd', 'Sitelink description', 35, 0, 0],
               ['ccCo', 'Callout', 25, 0, 0], ['ccSn', 'Snippet value', 25, 3, 10]];
  function run(){
    rows = []; var iss = [], warnN = 0;
    TYPES.forEach(function(t){
      var list = lines(t[0]), seen = {};
      if (t[3] && list.length && list.length < t[3]) iss.push(['warn', 'Add at least ' + t[3] + ' ' + t[1].toLowerCase() + 's. You have ' + list.length + '.']);
      if (t[4] && list.length > t[4]) iss.push(['bad', 'You have ' + list.length + ' ' + t[1].toLowerCase() + 's. Google allows up to ' + t[4] + '.']);
      list.forEach(function(s, i){
        var n = glen(dkiDefault(s)), notes = policy(s), k = s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
        if (seen[k]) notes.push('repeats another ' + t[1].toLowerCase()); seen[k] = 1;
        if (n > t[2]) iss.push(['bad', t[1] + ' ' + c(s) + ' is ' + n + ' characters. Cut ' + (n - t[2]) + ' to fit ' + t[2] + '.']);
        notes.forEach(function(m){ iss.push(['warn', t[1] + ' ' + c(s) + ' ' + m + '.']); warnN++; });
        rows.push({type: t[1] + (t[4] === 1 ? '' : ' ' + (i + 1)), text: s, n: n, lim: t[2]});
      });
    });
    var over = rows.filter(function(r){ return r.n > r.lim; }).length;
    $('ccBody').innerHTML = rows.length ? rows.map(function(r){
      var col = r.n > r.lim ? '#d1351f' : r.n > r.lim - 3 ? '#c47a00' : '#3d8f12';
      return '<tr><td style="white-space:nowrap">' + esc(r.type) + '</td><td>' + esc(r.text) + '</td><td class="num" style="color:' + col + ';font-weight:700;white-space:nowrap">' + r.n + ' / ' + r.lim + '</td></tr>';
    }).join('') : '<tr><td colspan="3" class="empty">Type some ad text to count it.</td></tr>';
    $('ccN').textContent = rows.length; $('ccOk').textContent = rows.length - over; $('ccOver').textContent = over; $('ccW').textContent = warnN;
    issues('ccCheck', iss, '<strong>Everything fits.</strong> All ' + rows.length + ' assets are within Google Ads limits.');
  }
  $('ccForm').addEventListener('input', run);
  $('ccCsv').onclick = function(){ download('google-ads-character-count.csv', 'Asset,Text,Characters,Limit\n' + rows.map(function(r){ return [r.type, r.text, r.n, r.lim].map(csvCell).join(','); }).join('\n'), 'text/csv'); };
  $('ccCopy').onclick = function(){ copyText(rows.filter(function(r){ return r.n <= r.lim; }).map(function(r){ return r.text; }).join('\n'), 'toast'); };
  run();
''',
        content='''
    <h2>What Is a Google Ads Character Counter?</h2>
    <p>Every piece of text in a Google Ads campaign has a strict limit. Go one character over and the ad editor will not let you save. Most counters only check one line at a time, which is slow when a single ad group has 15 headlines, 4 descriptions and a dozen assets.</p>
    <p>This Google Ads character counter checks all of it in one pass. It counts each line the way Google does, flags anything that is too long, and warns you about duplicates and text that often gets disapproved, such as repeated punctuation or words in capitals.</p>

    <h2>How to Use the Character Counter</h2>
    <ol>
      <li><strong>Paste your headlines</strong> and descriptions, one per line. You can copy them straight from a spreadsheet.</li>
      <li><strong>Add your paths, business name and assets</strong> such as sitelinks, callouts and snippet values.</li>
      <li><strong>Read the table.</strong> Green counts fit, orange is close to the limit and red needs cutting.</li>
      <li><strong>Fix the warnings</strong>, then download a CSV or copy only the lines that fit.</li>
    </ol>

    <h2>Google Ads Character Limits</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Text', 'Limit', 'Notes') + '''
      <tbody>
        <tr><td>Headline</td><td>30</td><td>Up to 15 per responsive search ad</td></tr>
        <tr><td>Description</td><td>90</td><td>Up to 4 per responsive search ad</td></tr>
        <tr><td>Path 1 and Path 2</td><td>15 each</td><td>Shown after your domain</td></tr>
        <tr><td>Business name</td><td>25</td><td>Shown beside your logo</td></tr>
        <tr><td>Sitelink text</td><td>25</td><td>Two optional description lines of 35 each</td></tr>
        <tr><td>Callout</td><td>25</td><td>Short benefits like free delivery</td></tr>
        <tr><td>Structured snippet value</td><td>25</td><td>3 to 10 values per header</td></tr>
      </tbody>
    </table></div>
    <p>Characters in Chinese, Japanese and Korean count as two each, and this counter does the same. If you use keyword insertion, Google counts the default text, so <code>{KeyWord:Running Shoes}</code> counts as 13 characters.</p>

    <h3>Policy Checks Built In</h3>
    <p>Google's <a href="https://support.google.com/adspolicy/answer/6021546" ''' + EXT + '''>editorial policy</a> rejects gimmicky text. The counter warns you about repeated punctuation like <code>!!</code>, emoji, extra spaces, words written in capitals that are not acronyms, and numbers used in place of letters.</p>

    <h2>Tips for Writing Within the Limits</h2>
    <ul>
      <li><strong>Use the full space in descriptions.</strong> Ninety characters is room for a benefit and a clear call to action.</li>
      <li><strong>Write short and long headline versions.</strong> A mix of lengths lets Google fit more headlines on small screens.</li>
      <li><strong>Swap long words for short ones.</strong> Use "get" not "receive", and numerals like "3" instead of "three".</li>
      <li><strong>Keep sitelinks specific.</strong> "Men's Running Shoes" beats "Click Here" and stays well within 25 characters.</li>
    </ul>

    <h2>Write Better Ads</h2>
    <p>Get more from your copy with <a href="''' + B + '''ppc-ad-copy-testing/">PPC ad copy testing</a> and our <a href="''' + B + '''25-google-ads-optimization-tips/">Google Ads optimization tips</a>. Once your text fits, see it as a real result in the <a href="''' + T + '''google-ads-preview-tool/">Google Ads preview tool</a>.</p>
''',
        faqs=[
            ("Do spaces count in Google Ads character limits?", "Yes. Spaces and punctuation each count as one character, just like letters and numbers."),
            ("What is the character limit for Google Ads headlines?", "Each headline in a responsive search ad can be up to 30 characters, and each description up to 90. Display paths can be up to 15 characters each."),
            ("Why does my Japanese or Chinese text count double?", "Google counts double width characters such as Chinese, Japanese and Korean as two characters each, so a headline in those languages fits about 15 characters."),
            ("Can I use exclamation marks in Google Ads?", "A single exclamation mark is fine in most text, but repeated punctuation such as two exclamation marks breaks Google's editorial policy and gets the ad disapproved."),
        ],
        related=[("PPC Ad Copy Testing", "ppc-ad-copy-testing"), ("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"),
                 ("Google Ads Quality Score Explained", "google-ads-quality-score-explained"), ("Search Campaign vs Performance Max", "search-campaign-vs-performance-max")],
    ))

    # ---------- 3. KEYWORD MATCH TYPE GENERATOR ----------
    TOOLS.append(dict(
        slug='keyword-match-type-generator', short='MT', name='Keyword Match Type Generator',
        card='Turn a keyword list into broad, "phrase" and [exact] match, cleaned and ready for Google Ads or Ads Editor.',
        title='Keyword Match Type Generator for Google Ads',
        desc='Free keyword match type generator. Wrap keywords in phrase quotes and exact brackets, clean invalid symbols and export a Google Ads Editor CSV in seconds.',
        h1='Keyword Match Type Generator',
        lead='Paste a keyword list and get it back in broad, phrase and exact match, with quotes and brackets added for you. Invalid symbols, old plus signs and duplicates are cleaned up, and you can export a CSV for Google Ads Editor.',
        tool='''<section class="tool" aria-label="Keyword match type generator" id="mtForm">
    <div class="card" style="min-width:0">
      <h2>Your Keywords</h2>
      ''' + F('mtIn', 'Keywords', 'running shoes\n+buy +running +shoes online\nRunning Shoes For Men\n"trail running shoes"\n[nike running shoes]\nrunning shoes!!\nrunning shoes\nbest running shoes for flat feet and heel pain under 3000 rupees in india', em='one per line', tag='textarea', extra=' style="min-height:200px"') + '''
      <div class="field"><label>Match Types</label>''' + CK('mtB', 'Broad match <em style="font-weight:400;color:#666">running shoes</em>', True, 'mtT') + CK('mtP', 'Phrase match <em style="font-weight:400;color:#666">"running shoes"</em>', True, 'mtT') + CK('mtE', 'Exact match <em style="font-weight:400;color:#666">[running shoes]</em>', True, 'mtT') + '''</div>
      <div class="field"><label>Clean Up</label>''' + CK('mtLow', 'Convert to lower case') + CK('mtSym', 'Remove symbols Google does not accept') + CK('mtDup', 'Remove duplicates') + '''</div>
      ''' + F('mtFmt', 'Output Format', 'list', tag='select', opts=[('list', 'Plain list, grouped by match type'), ('mixed', 'Plain list, each keyword in every match type'), ('csv', 'CSV for Google Ads Editor')]) + '''
      ''' + R2(F('mtCamp', 'Campaign', 'Search | Running Shoes', em='for CSV'), F('mtAg', 'Ad Group', 'Running Shoes', em='for CSV')) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Formatted Keywords</h2>
      <div class="stats">''' + S('mtKw', 'Keywords') + S('mtOut', 'Output Lines') + S('mtFix', 'Cleaned') + S('mtRej', 'Rejected') + '''</div>
      <div class="kw-result" id="mtCheck"></div>
      <pre class="code-out" id="mtRes" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="mtCopy" type="button">Copy Keywords</button><button class="btn" id="mtDl" type="button">Download</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Paste into Google Ads</strong><ul><li>The plain list pastes straight into the keyword box of an ad group</li><li>The CSV imports into Google Ads Editor with Account, Import, From file</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var out = '', BADSYM = /[,!@%^()={};~`<>?\\|]/g;
  function run(){
    var iss = [], kws = [], seen = {}, fixed = 0, rej = 0;
    lines('mtIn').forEach(function(raw){
      var k = raw, before = raw;
      k = k.replace(/^-\s*/, '').replace(/^\[(.*)\]$/, '$1').replace(/^"(.*)"$/, '$1').replace(/(^|\s)\+(?=\S)/g, '$1');
      if ($('mtLow').checked) k = k.toLowerCase();
      if ($('mtSym').checked) k = k.replace(BADSYM, ' ');
      k = k.replace(/["\[\]]/g, ' ').replace(/\s+/g, ' ').trim();
      if (!k) return;
      if (k !== before) fixed++;
      var syms = k.match(BADSYM);
      if (syms){ iss.push(['bad', c(k) + ' contains ' + c(syms.join(' ')) + ', which Google Ads does not accept in keywords.']); rej++; return; }
      var words = k.split(' ').length;
      if (words > 10){ iss.push(['bad', c(k) + ' has ' + words + ' words. Google Ads allows up to 10, so it was left out.']); rej++; return; }
      if (k.length > 80){ iss.push(['bad', c(k) + ' is ' + k.length + ' characters. The limit is 80.']); rej++; return; }
      var key = k.toLowerCase();
      if ($('mtDup').checked && seen[key]){ fixed++; return; }
      seen[key] = 1; kws.push(k);
    });
    var types = [['mtB', 'Broad', function(k){ return k; }], ['mtP', 'Phrase', function(k){ return '"' + k + '"'; }], ['mtE', 'Exact', function(k){ return '[' + k + ']'; }]].filter(function(t){ return $(t[0]).checked; });
    if (!types.length) iss.push(['bad', 'Tick at least one match type.']);
    var fmt = $('mtFmt').value, L = [];
    if (fmt === 'csv'){
      var camp = v('mtCamp'), ag = v('mtAg');
      L.push('Campaign,Ad group,Keyword,Criterion Type');
      types.forEach(function(t){ kws.forEach(function(k){ L.push([camp, ag, k, t[1]].map(csvCell).join(',')); }); });
      if (!camp || !ag) iss.push(['warn', 'Add a campaign and ad group name so Google Ads Editor knows where to put the keywords.']);
    } else if (fmt === 'mixed'){
      kws.forEach(function(k){ types.forEach(function(t){ L.push(t[2](k)); }); });
    } else {
      types.forEach(function(t, i){ if (i) L.push(''); kws.forEach(function(k){ L.push(t[2](k)); }); });
    }
    if (fixed) iss.push(['warn', fixed + ' line' + (fixed > 1 ? 's were' : ' was') + ' cleaned: old match symbols, plus signs, capitals, invalid symbols or duplicates were removed.']);
    out = L.join('\n');
    $('mtRes').textContent = out || 'Your formatted keywords appear here.';
    $('mtKw').textContent = kws.length; $('mtOut').textContent = L.filter(Boolean).length - (fmt === 'csv' ? 1 : 0); $('mtFix').textContent = fixed; $('mtRej').textContent = rej;
    issues('mtCheck', iss, '<strong>' + kws.length + ' keywords ready</strong> in ' + types.map(function(t){ return t[1].toLowerCase(); }).join(', ') + ' match.');
  }
  $('mtForm').addEventListener('input', run); $('mtForm').addEventListener('change', run);
  $('mtCopy').onclick = function(){ copyText(out, 'toast'); };
  $('mtDl').onclick = function(){ var csv = $('mtFmt').value === 'csv'; download(csv ? 'keywords-ads-editor.csv' : 'keywords.txt', out, csv ? 'text/csv' : 'text/plain'); };
  run();
''',
        content='''
    <h2>What Is a Keyword Match Type Generator?</h2>
    <p>In Google Ads, the way you write a keyword decides which searches it can match. Plain text is broad match, text in quotes is phrase match and text in square brackets is exact match. Typing those symbols around hundreds of keywords by hand is slow and easy to get wrong.</p>
    <p>This keyword match type generator does it for you. Paste a list from any keyword tool and it returns every keyword in the match types you pick, cleaned of symbols Google rejects, duplicates and leftover plus signs from the old broad match modifier.</p>

    <h2>How to Use the Match Type Generator</h2>
    <ol>
      <li><strong>Paste your keywords</strong>, one per line. Existing quotes, brackets and plus signs are fine.</li>
      <li><strong>Tick the match types</strong> you want to build: broad, phrase, exact or all three.</li>
      <li><strong>Keep the clean up options on</strong> to fix capitals, invalid symbols and repeats.</li>
      <li><strong>Pick an output format.</strong> Use a plain list to paste into Google Ads, or the CSV for Google Ads Editor.</li>
      <li><strong>Copy or download</strong> the result and add it to your ad group.</li>
    </ol>

    <h2>Google Ads Match Types Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Match type', 'How to write it', 'Can show for') + '''
      <tbody>
        <tr><td>Broad</td><td><code>running shoes</code></td><td>Searches related to the meaning, even without the words, like "jogging trainers"</td></tr>
        <tr><td>Phrase</td><td><code>"running shoes"</code></td><td>Searches that include the meaning of the phrase, like "buy running shoes online"</td></tr>
        <tr><td>Exact</td><td><code>[running shoes]</code></td><td>Searches with the same meaning or intent, like "shoes for running"</td></tr>
      </tbody>
    </table></div>
    <p>All three types also match close variants such as plurals and misspellings. Google explains each type in its guide to <a href="https://support.google.com/google-ads/answer/7476658" ''' + EXT + '''>adding keywords</a>.</p>

    <h3>Rules the Generator Checks</h3>
    <ul>
      <li>A keyword can have up to 10 words and 80 characters.</li>
      <li>Symbols such as <code>!</code>, <code>@</code>, <code>%</code>, <code>,</code> and brackets inside a keyword are not accepted.</li>
      <li>Plus signs from broad match modifier no longer work, since Google retired it in 2021, so they are removed.</li>
    </ul>

    <h2>Tips for Choosing Match Types</h2>
    <ul>
      <li><strong>Pair broad match with Smart Bidding.</strong> Broad match works best when bids learn from your conversion data.</li>
      <li><strong>Use exact match for your best terms</strong> so you control the bid and the ad for searches you know convert.</li>
      <li><strong>Avoid the same keyword in two ad groups</strong> in the same match type. They compete with each other.</li>
      <li><strong>Review search terms weekly</strong> and add negatives for anything that wastes money.</li>
    </ul>

    <h2>Build Better Keyword Lists</h2>
    <p>Start from strong ideas with <a href="''' + B + '''best-keyword-research-tools-compared/">the best keyword research tools</a>, match intent with <a href="''' + B + '''what-is-search-intent-practical-guide/">our search intent guide</a>, and learn why exact terms help in <a href="''' + B + '''google-ads-quality-score-explained/">Quality Score explained</a>. Next, split your list into themed ad groups with the <a href="''' + T + '''keyword-grouper/">keyword grouper</a>.</p>
''',
        faqs=[
            ("What is the difference between phrase and exact match?", "Phrase match, written in quotes, can show for searches that include the meaning of your keyword plus other words. Exact match, written in square brackets, only shows for searches with the same meaning as your keyword."),
            ("Does broad match modifier still work?", "No. Google stopped broad match modifier in 2021 and folded it into phrase match. Plus signs in keywords are ignored, so this tool removes them."),
            ("How do I import the CSV into Google Ads Editor?", "Download the CSV, open Google Ads Editor, choose Account, then Import, then From file, and select it. Review the changes and click Keep before you post."),
            ("Should I add the same keyword in all three match types?", "Not always. With Smart Bidding many advertisers now use broad and exact only. Adding all three can split data, so test before you roll it out to every ad group."),
        ],
        related=[("Google Ads Quality Score Explained", "google-ads-quality-score-explained"), ("Best Keyword Research Tools Compared", "best-keyword-research-tools-compared"),
                 ("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("What Is Search Intent", "what-is-search-intent-practical-guide")],
    ))

    # ---------- 4. NEGATIVE KEYWORD TOOL ----------
    LISTS = [('jobs', 'Jobs and careers', 'job, jobs, career, careers, hiring, vacancy, vacancies, salary, internship, recruitment', True),
             ('learn', 'Courses and research', 'course, courses, training, tutorial, certification, syllabus, pdf, meaning, definition, wikipedia', True),
             ('used', 'Used and second hand', 'used, second hand, secondhand, refurbished, pre owned', True),
             ('free', 'Free stuff', 'free, freebie, freebies, giveaway, torrent', False),
             ('diy', 'DIY and how to', 'diy, how to, homemade, do it yourself', False),
             ('trouble', 'Complaints and scams', 'complaint, complaints, scam, fraud, lawsuit', False),
             ('media', 'Images and downloads', 'images, pictures, photos, wallpaper, clipart, png, drawing', False)]
    def lck(k, name, words, on):
        return f'<label class="check"><input type="checkbox" class="nkL" value="{k}"' + (' checked' if on else '') + f'> <span>{name} <em style="font-weight:400;color:#666">{words}</em></span></label>'
    TOOLS.append(dict(
        slug='negative-keyword-tool', short='NK', name='Negative Keyword Tool',
        card='Build a clean negative keyword list from ready made lists, then test it against your keywords and real searches.',
        title='Negative Keyword Tool: Build and Test Your List',
        desc='Free negative keyword tool for Google Ads. Add ready made lists, format match types, find negatives that block your own keywords and test real searches.',
        h1='Negative Keyword Tool',
        lead='Build a negative keyword list in the right match types, then test it. The tool shows which searches each negative blocks and warns you when a negative would stop your own keywords from showing.',
        tool='''<section class="tool" aria-label="Negative keyword tool" id="nkForm">
    <div class="card" style="min-width:0">
      <h2>Build Your List</h2>
      <div class="field"><label>Ready Made Lists</label>''' + ''.join(lck(k, n, w, on) for k, n, w, on in LISTS) + '''</div>
      ''' + F('nkCustom', 'Your Own Negatives', 'kids\n"shoe repair"\nformal\nonline\n[running shoes free]', em='one per line, quotes and brackets allowed', tag='textarea', mono=True) + '''
      ''' + F('nkMt', 'Match Type for Plain Words', 'phrase', tag='select', opts=[('broad', 'Negative broad: all words, any order'), ('phrase', 'Negative phrase: words in this order'), ('exact', 'Negative exact: this search only')]) + '''
      ''' + F('nkKw', 'Your Keywords', 'running shoes\n[running shoes for men]\n"buy running shoes online"\ntrail running shoes\nnike running shoes', em='to catch conflicts', tag='textarea', mono=True) + '''
      ''' + F('nkTest', 'Searches to Test', 'running shoes jobs\nrunning shoe repair near me\nbest running shoes for men\nkids running shoes\nhow to clean running shoes\nsecond hand running shoes\nnike running shoes sale\nrunning shoes job\nrunning shoes free delivery', em='one per line, from your search terms report', tag='textarea', mono=True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Negative Keywords</h2>
      <div class="stats">''' + S('nkN', 'Negatives') + S('nkC', 'Conflicts') + S('nkB', 'Searches Blocked') + '''</div>
      <div class="kw-result" id="nkCheck"></div>
      <pre class="code-out" id="nkOut" ''' + ST_(PRE, 'max-height:260px') + '''></pre>
      <div class="actions"><button class="btn dark" id="nkCopy" type="button">Copy Negatives</button><button class="btn" id="nkPl" type="button">Add Missing Plurals</button><button class="btn" id="nkDl" type="button">Download CSV</button><span class="toast" id="toast">Copied!</span></div>
      <h3 style="font-size:16px;margin:18px 0 10px">Search Test</h3>
      <div ''' + SCROLL + '''><table class="rtable"><thead><tr><th>Search</th><th>Result</th><th>Blocked by</th></tr></thead><tbody id="nkBody"></tbody></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var LISTS = {jobs: 'job,jobs,career,careers,hiring,vacancy,vacancies,salary,internship,recruitment', learn: 'course,courses,training,tutorial,certification,syllabus,pdf,meaning,definition,wikipedia',
    used: 'used,second hand,secondhand,refurbished,pre owned', free: 'free,freebie,freebies,giveaway,torrent', diy: 'diy,how to,homemade,do it yourself',
    trouble: 'complaint,complaints,scam,fraud,lawsuit', media: 'images,pictures,photos,wallpaper,clipart,png,drawing'};
  var BADSYM = /[,!@%^()={};~`<>?\\|]/, negs = [], missing = [];
  function norm(s){ return String(s).toLowerCase().replace(/\./g, '').replace(/\s+/g, ' ').trim(); }
  function parse(raw, def){
    var s = raw.trim().replace(/^-\s*/, ''), t = def;
    if (/^\[.*\]$/.test(s)){ t = 'exact'; s = s.slice(1, -1); } else if (/^".*"$/.test(s)){ t = 'phrase'; s = s.slice(1, -1); }
    return {t: t, k: norm(s), raw: raw};
  }
  function blocks(n, search){
    var q = norm(search).split(' '), w = n.k.split(' ');
    if (n.t === 'exact') return q.join(' ') === n.k;
    if (n.t === 'broad') return w.every(function(x){ return q.indexOf(x) > -1; });
    for (var i = 0; i + w.length <= q.length; i++){ if (w.every(function(x, j){ return q[i + j] === x; })) return true; }
    return false;
  }
  function fmt(n){ return n.t === 'exact' ? '[' + n.k + ']' : n.t === 'phrase' ? '"' + n.k + '"' : n.k; }
  function run(){
    var iss = [], seen = {}, def = $('nkMt').value; negs = []; missing = [];
    function addNeg(n, custom){
      if (!n.k) return;
      if (BADSYM.test(n.k)){ iss.push(['bad', c(n.raw) + ' contains a symbol Google does not accept in negative keywords, such as ' + c((n.k.match(BADSYM) || [''])[0]) + '.']); return; }
      if (/\s-\S/.test(n.k)) iss.push(['warn', c(n.raw) + ' has a minus sign inside it. Google ignores the word after it, so put each negative on its own line.']);
      if (/(^|\s)\+/.test(n.k)) iss.push(['warn', c(n.raw) + ' has a plus sign. Google ignores it in negatives.']);
      var key = n.t + '|' + n.k; if (seen[key]) return; seen[key] = 1; n.custom = custom; negs.push(n);
    }
    document.querySelectorAll('.nkL:checked').forEach(function(x){ LISTS[x.value].split(',').forEach(function(w){ addNeg({t: def, k: w, raw: w}, false); }); });
    lines('nkCustom').forEach(function(r){ addNeg(parse(r, def), true); });
    var all = {}; negs.forEach(function(n){ all[n.k] = 1; });
    negs.forEach(function(n){
      if (!n.custom || n.t === 'exact' || / /.test(n.k) || n.k.length < 3) return;
      var alt = /[^s]s$/.test(n.k) ? n.k.slice(0, -1) : /(al|ic|ed|ing|ly|ne|ful|ous|ive|y|s|x|sh|ch)$/.test(n.k) ? '' : n.k + 's';
      if (alt && !all[alt]){ missing.push({t: n.t, k: alt, raw: alt}); all[alt] = 1; }
    });
    if (missing.length) iss.push(['warn', 'Negatives do not match plurals or close variants. Consider adding ' + missing.slice(0, 6).map(function(m){ return c(fmt(m)); }).join(', ') + '.']);
    var conf = 0;
    lines('nkKw').forEach(function(r){
      var k = parse(r, 'broad'); if (!k.k) return;
      negs.forEach(function(n){ if (blocks(n, k.k)){ conf++; iss.push(['bad', 'The negative ' + c(fmt(n)) + ' blocks your keyword ' + c(r) + '. Remove it or make it more specific.']); } });
    });
    if (negs.some(function(n){ return n.k === 'free'; })) iss.push(['warn', 'The negative ' + c('free') + ' also blocks searches like "free delivery". Use phrases like ' + c('"free download"') + ' if you offer free delivery.']);
    var blocked = 0, rows = lines('nkTest').map(function(q){
      var by = negs.filter(function(n){ return blocks(n, q); });
      if (by.length) blocked++;
      return '<tr' + (by.length ? '' : ' class="hit"') + '><td>' + esc(q) + '</td><td style="font-weight:700;color:' + (by.length ? '#d1351f' : '#3d8f12') + '">' + (by.length ? 'Blocked' : 'Ad can show') + '</td><td>' + by.slice(0, 3).map(function(n){ return esc(fmt(n)); }).join(', ') + '</td></tr>';
    });
    $('nkBody').innerHTML = rows.join('') || '<tr><td colspan="3" class="empty">Paste searches to test them.</td></tr>';
    $('nkOut').textContent = negs.map(fmt).join('\n') || 'Your negative keywords appear here.';
    $('nkN').textContent = negs.length; $('nkC').textContent = conf; $('nkB').textContent = blocked;
    $('nkPl').style.display = missing.length ? '' : 'none';
    issues('nkCheck', iss, '<strong>' + negs.length + ' negatives ready</strong> and none of them block your keywords.');
  }
  $('nkForm').addEventListener('input', run); $('nkForm').addEventListener('change', run);
  $('nkCopy').onclick = function(){ copyText(negs.map(fmt).join('\n'), 'toast'); };
  $('nkPl').onclick = function(){ var ta = $('nkCustom'); ta.value = ta.value.replace(/\s*$/, '') + '\n' + missing.map(fmt).join('\n'); run(); };
  $('nkDl').onclick = function(){ var m = {broad: 'Negative Broad', phrase: 'Negative Phrase', exact: 'Negative Exact'};
    download('negative-keywords.csv', 'Keyword,Criterion Type\n' + negs.map(function(n){ return csvCell(n.k) + ',' + m[n.t]; }).join('\n'), 'text/csv'); };
  run();
''',
        content='''
    <h2>What Is a Negative Keyword Tool?</h2>
    <p>Negative keywords stop your ads from showing for searches you do not want, like job seekers clicking a shoe ad or students looking for a free PDF. A good list can save a large share of a search budget. A bad one quietly blocks your best searches.</p>
    <p>This negative keyword tool helps with both sides. It builds a list from common themes and your own terms, writes each one in the right match type, and then tests it. You see exactly which searches get blocked and whether any negative clashes with the keywords you are paying for.</p>

    <h2>How to Use the Negative Keyword Tool</h2>
    <ol>
      <li><strong>Tick the ready made lists</strong> that never fit your business, such as jobs or courses.</li>
      <li><strong>Add your own negatives</strong> from your search terms report. Use quotes for phrase and brackets for exact.</li>
      <li><strong>Choose a match type</strong> for plain words. Phrase is a safe default.</li>
      <li><strong>Paste your keywords</strong> so the tool can flag any negative that would block them.</li>
      <li><strong>Paste real searches</strong> to see which ones your list blocks, then copy the list or download it.</li>
    </ol>

    <h2>How Negative Match Types Work</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Negative', 'Blocks', 'Does not block') + '''
      <tbody>
        <tr><td>Broad: <code>running shoes</code></td><td>Any search with both words in any order, like "shoes for running"</td><td>"running shoe", because plurals are not matched</td></tr>
        <tr><td>Phrase: <code>"running shoes"</code></td><td>Searches with the words in that order, like "blue running shoes"</td><td>"shoes running"</td></tr>
        <tr><td>Exact: <code>[running shoes]</code></td><td>Only the search "running shoes"</td><td>"blue running shoes"</td></tr>
      </tbody>
    </table></div>
    <p>The big difference from normal keywords is that negatives do not match close variants. You have to add plurals, synonyms and other forms yourself, which is why the tool suggests missing plurals. Google explains the rules in <a href="https://support.google.com/google-ads/answer/2453972" ''' + EXT + '''>about negative keywords</a>.</p>

    <h2>Tips for a Safe Negative List</h2>
    <ul>
      <li><strong>Prefer phrases to single words</strong> when a word has two meanings. The negative <code>free</code> also blocks "free delivery".</li>
      <li><strong>Use exact negatives</strong> to stop one wasteful search without losing longer, useful ones.</li>
      <li><strong>Put shared themes in a list.</strong> A shared negative list for jobs or courses can be applied to every campaign.</li>
      <li><strong>Check after every change.</strong> Run your keywords through the conflict check before you upload.</li>
    </ul>

    <h2>Cut Wasted Spend</h2>
    <p>Our full guide to <a href="''' + B + '''google-ads-negative-keywords/">Google Ads negative keywords</a> covers lists and levels in depth, and <a href="''' + B + '''25-google-ads-optimization-tips/">Google Ads optimization tips</a> shows where else to save. Not sure which words waste money? Find them with the <a href="''' + T + '''search-term-ngram-analyzer/">search term ngram analyzer</a>.</p>
''',
        faqs=[
            ("Do negative keywords match plurals and misspellings?", "No. Unlike normal keywords, negatives do not match close variants. If you block job, you also need jobs. Google does handle letter case and common misspellings."),
            ("Which match type should I use for negative keywords?", "Phrase match is a safe default for most negatives. Use exact match to block one specific search, and broad match only when every word on its own is clearly irrelevant."),
            ("Can a negative keyword block my own keyword?", "Yes. If your negative appears inside one of your keywords, that keyword stops showing. The conflict check in this tool finds these clashes before you upload."),
            ("Where do I add the negative keywords?", "In Google Ads open Keywords, then Negative search keywords, and add them to a campaign or ad group. For several campaigns, create a shared negative keyword list in Tools under Shared library."),
        ],
        related=[("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"),
                 ("What Is Search Intent", "what-is-search-intent-practical-guide"), ("Search Campaign vs Performance Max", "search-campaign-vs-performance-max")],
    ))

    # ---------- 5. SEARCH TERM NGRAM ANALYZER ----------
    ST = [('running shoes for men', 120, 2400, 3840, 6), ('buy running shoes online', 95, 1900, 3325, 5), ('nike running shoes', 210, 5200, 7980, 9),
          ('running shoes for women', 88, 2100, 2904, 4), ('running shoes jobs', 14, 900, 560, 0), ('running shoe repair near me', 22, 640, 770, 0),
          ('free running shoes', 31, 1500, 1085, 0), ('running shoes free delivery', 18, 420, 666, 2), ('trail running shoes', 64, 1300, 2560, 3),
          ('best running shoes for flat feet', 41, 980, 1599, 2), ('running shoes for kids', 37, 1100, 1258, 0), ('kids sports shoes', 29, 860, 957, 0),
          ('running shoes size chart', 26, 700, 676, 0), ('how to clean running shoes', 33, 1250, 990, 0), ('running shoes under 3000', 72, 1600, 2160, 4),
          ('asics running shoes', 58, 1200, 2436, 3), ('puma running shoes for men', 49, 1050, 1764, 2), ('second hand running shoes', 12, 380, 420, 0),
          ('running shoes sale', 83, 1700, 2490, 4), ('running shoes meaning', 9, 410, 270, 0), ('running shoes for flat feet', 39, 900, 1404, 1),
          ('nike running shoes for men', 77, 1500, 2849, 4), ('running shoes kids size', 15, 520, 495, 0), ('running coach jobs', 11, 600, 418, 0),
          ('running shoes images', 19, 1300, 380, 0), ('cushioned running shoes', 44, 880, 1584, 2), ('running shoes for heavy runners', 21, 450, 798, 1)]
    ST_TXT = 'Search term\tMatch type\tClicks\tImpr.\tCost\tConversions\n' + '\n'.join(f'{t}\tBroad match\t{cl}\t{im}\t{co:.2f}\t{cv}' for t, cl, im, co, cv in ST)
    TOOLS.append(dict(
        slug='search-term-ngram-analyzer', short='NG', name='Search Term Ngram Analyzer',
        card='Paste a search terms report to find the one, two and three word phrases that waste spend or drive sales.',
        title='Search Term Ngram Analyzer for Google Ads Reports',
        desc='Free ngram analyzer for Google Ads search terms reports. Group spend, clicks and conversions by word and phrase to find wasted spend and new negatives fast.',
        h1='Search Term Ngram Analyzer',
        lead='Paste your Google Ads search terms report and see cost, clicks and conversions grouped by every one, two and three word phrase. Wasteful words jump out, and you can copy them straight into a negative keyword list.',
        tool='''<section class="tool" aria-label="Search term ngram analyzer" id="ngForm">
    <div class="card" style="min-width:0">
      <h2>Search Terms Report</h2>
      ''' + F('ngIn', 'Paste Report', ST_TXT, em='CSV or copied from Google Ads', tag='textarea', mono=True, extra=' style="min-height:260px;white-space:pre;overflow-wrap:normal"') + '''
      ''' + R2(F('ngCpa', 'Target CPA', '800', typ='number', extra=' min="0" step="any"'), F('ngCur', 'Currency Symbol', '₹')) + '''
      ''' + R2(F('ngMin', 'Show Phrases Found In', '2', tag='select', opts=[('1', '1 or more terms'), ('2', '2 or more terms'), ('3', '3 or more terms'), ('5', '5 or more terms')]),
               F('ngSort', 'Sort By', 'cost', tag='select', opts=[('cost', 'Cost'), ('waste', 'Cost with no conversions'), ('clicks', 'Clicks'), ('conv', 'Conversions'), ('cpa', 'Cost per conversion'), ('terms', 'Number of terms')])) + '''
      ''' + CK('ngStop', 'Skip filler words like for, the, and, near') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Ngram Report</h2>
      <div class="stats">''' + S('ngTerms', 'Search Terms') + S('ngCost', 'Total Cost') + S('ngWaste', 'No Conversion Cost') + S('ngFlag', 'Flagged') + '''</div>
      <div class="kw-result" id="ngCheck"></div>
      <div class="tabs" id="ngTabs"><button type="button" class="on" data-n="1">1 Word</button><button type="button" data-n="2">2 Words</button><button type="button" data-n="3">3 Words</button></div>
      <div ''' + SCROLL + '''><table class="rtable" style="font-size:13.5px"><thead><tr><th>Phrase</th><th class="num">Terms</th><th class="num">Clicks</th><th class="num">Cost</th><th class="num">Conv.</th><th class="num">CPA</th><th>Flag</th></tr></thead><tbody id="ngBody"></tbody></table></div>
      <div class="actions"><button class="btn dark" id="ngCopy" type="button">Copy Flagged as Negatives</button><button class="btn" id="ngCsv" type="button">Download CSV</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var N = 1, data = {1: [], 2: [], 3: []}, STOP = {'for':1,'the':1,'and':1,'near':1,'me':1,'to':1,'a':1,'of':1,'in':1,'on':1,'with':1,'online':0,'best':0,'how':0,'is':1,'at':1,'by':1,'my':1,'your':1,'from':1,'under':0};
  function parseRows(txt){
    var first = txt.split(/\r?\n/).find(function(l){ return l.trim(); }) || '', delim = '\t';
    if (txt.indexOf('\t') < 0) delim = (txt.match(/;/g) || []).length > (txt.match(/,/g) || []).length ? ';' : ',';
    var rows = [], row = [], cell = '', q = false;
    for (var i = 0; i < txt.length; i++){
      var ch = txt[i];
      if (q){ if (ch === '"'){ if (txt[i + 1] === '"'){ cell += '"'; i++; } else q = false; } else cell += ch; }
      else if (ch === '"') q = true;
      else if (ch === delim){ row.push(cell); cell = ''; }
      else if (ch === '\n' || ch === '\r'){ if (ch === '\r' && txt[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
      else cell += ch;
    }
    row.push(cell); rows.push(row);
    return rows.filter(function(r){ return r.some(function(x){ return x.trim(); }); });
  }
  function num(s){ s = String(s || '').replace(/[^0-9.\-]/g, ''); var n = parseFloat(s); return isFinite(n) ? n : 0; }
  function money(n){ return v('ngCur') + Math.round(n).toLocaleString('en-IN'); }
  function analyse(){
    var iss = [], rows = parseRows($('ngIn').value), hi = -1;
    for (var i = 0; i < Math.min(rows.length, 15); i++){ if (rows[i].some(function(x){ return /^\s*(search term|search terms|query|search query)\s*$/i.test(x); })){ hi = i; break; } }
    if (hi < 0){ say('ngCheck', 'bad', '<strong>No header row found.</strong> Include the column names, with one called ' + c('Search term') + '.'); $('ngBody').innerHTML = ''; data = {1: [], 2: [], 3: []}; ['ngTerms','ngFlag'].forEach(function(x){ $(x).textContent = 0; }); return; }
    var h = rows[hi].map(function(x){ return x.trim().toLowerCase(); });
    function col(re){ for (var j = 0; j < h.length; j++) if (re.test(h[j])) return j; return -1; }
    var cT = col(/^(search term|search terms|query|search query)$/), cC = col(/^clicks$/), cI = col(/^(impr\.?|impressions)$/), cCo = col(/^cost$/), cV = col(/^(conversions|conv\.)$/);
    if (cCo < 0) iss.push(['warn', 'No ' + c('Cost') + ' column found, so cost and waste show as zero.']);
    if (cV < 0) iss.push(['warn', 'No ' + c('Conversions') + ' column found. Add it to your report to spot waste.']);
    var terms = [];
    rows.slice(hi + 1).forEach(function(r){
      var t = (r[cT] || '').trim(); if (!t || /^total/i.test(t) || t === '--') return;
      terms.push({t: t.toLowerCase(), cl: num(r[cC]), im: num(r[cI]), co: num(r[cCo]), cv: num(r[cV])});
    });
    var stop = $('ngStop').checked, target = num(v('ngCpa')), total = 0, waste = 0;
    terms.forEach(function(x){ total += x.co; if (!x.cv) waste += x.co; });
    [1, 2, 3].forEach(function(n){
      var m = {};
      terms.forEach(function(x){
        var w = x.t.replace(/[^\p{L}\p{N}' ]+/gu, ' ').split(/\s+/).filter(Boolean), done = {};
        for (var i = 0; i + n <= w.length; i++){
          var g = w.slice(i, i + n);
          if (stop && (STOP[g[0]] === 1 || STOP[g[g.length - 1]] === 1)) continue;
          var k = g.join(' '); if (done[k]) continue; done[k] = 1;
          var a = m[k] || (m[k] = {k: k, terms: 0, cl: 0, im: 0, co: 0, cv: 0});
          a.terms++; a.cl += x.cl; a.im += x.im; a.co += x.co; a.cv += x.cv;
        }
      });
      data[n] = Object.keys(m).map(function(k){ var a = m[k]; a.cpa = a.cv ? a.co / a.cv : null;
        a.flag = target > 0 ? (!a.cv && a.co >= target ? 'waste' : a.cv && a.cpa > target * 1.5 ? 'high' : '') : (!a.cv && a.co > 0 ? 'waste' : ''); return a; });
    });
    $('ngTerms').textContent = fmtN(terms.length); $('ngCost').textContent = money(total); $('ngWaste').textContent = money(waste);
    if (!terms.length) iss.push(['bad', 'No search terms found under the header row.']);
    else if (total) iss.push(['warn', Math.round(waste / total * 100) + '% of your spend went on search terms with no conversions. Check the flagged phrases first.']);
    issues('ngCheck', iss, '<strong>' + terms.length + ' search terms analysed.</strong>');
    table();
  }
  function table(){
    var min = +$('ngMin').value, s = $('ngSort').value;
    var list = data[N].filter(function(a){ return a.terms >= min; });
    list.sort(function(a, b){
      if (s === 'waste') return (b.cv ? 0 : b.co) - (a.cv ? 0 : a.co) || b.co - a.co;
      if (s === 'cpa') return (b.cpa === null ? 1e15 : b.cpa) - (a.cpa === null ? 1e15 : a.cpa) || b.co - a.co;
      var key = {cost: 'co', clicks: 'cl', conv: 'cv', terms: 'terms'}[s]; return b[key] - a[key] || b.co - a.co;
    });
    var flagged = data[N].filter(function(a){ return a.flag && a.terms >= min; }).length;
    $('ngFlag').textContent = flagged;
    $('ngBody').innerHTML = list.length ? list.slice(0, 300).map(function(a){
      var f = a.flag === 'waste' ? '<span style="color:#d1351f;font-weight:700">No sales</span>' : a.flag === 'high' ? '<span style="color:#c47a00;font-weight:700">High CPA</span>' : '';
      return '<tr><td>' + esc(a.k) + '</td><td class="num">' + a.terms + '</td><td class="num">' + fmtN(a.cl) + '</td><td class="num">' + money(a.co) + '</td><td class="num">' + (Math.round(a.cv * 100) / 100) + '</td><td class="num">' + (a.cpa === null ? '' : money(a.cpa)) + '</td><td>' + f + '</td></tr>';
    }).join('') : '<tr><td colspan="7" class="empty">No phrases match these settings. Try a lower minimum.</td></tr>';
  }
  document.querySelectorAll('#ngTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#ngTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); N = +b.getAttribute('data-n'); table(); }); });
  $('ngIn').addEventListener('input', analyse); $('ngCpa').addEventListener('input', analyse); $('ngCur').addEventListener('input', analyse); $('ngStop').addEventListener('change', analyse);
  $('ngMin').addEventListener('change', table); $('ngSort').addEventListener('change', table);
  $('ngCopy').onclick = function(){ copyText(data[N].filter(function(a){ return a.flag === 'waste' && a.terms >= +$('ngMin').value; }).map(function(a){ return '"' + a.k + '"'; }).join('\n'), 'toast'); };
  $('ngCsv').onclick = function(){
    var L = ['Phrase,Words,Terms,Clicks,Impressions,Cost,Conversions,CPA,Flag'];
    [1, 2, 3].forEach(function(n){ data[n].forEach(function(a){ L.push([a.k, n, a.terms, a.cl, a.im, a.co.toFixed(2), a.cv, a.cpa === null ? '' : a.cpa.toFixed(2), a.flag === 'waste' ? 'No sales' : a.flag === 'high' ? 'High CPA' : ''].map(csvCell).join(',')); }); });
    download('search-term-ngrams.csv', L.join('\n'), 'text/csv');
  };
  analyse();
''',
        content='''
    <h2>What Is Ngram Analysis in Google Ads?</h2>
    <p>An ngram is a word or a short run of words. A one word ngram is a single word like "jobs", a two word ngram is a pair like "for kids". Ngram analysis splits every search in your report into these pieces and adds up the cost, clicks and conversions for each one.</p>
    <p>Looking at search terms one by one hides patterns, because waste is spread across hundreds of rows that each cost a little. Grouped by ngram, you see that "kids" cost thousands across many searches and never sold anything. That one word becomes one negative keyword that fixes them all.</p>

    <h2>How to Use the Ngram Analyzer</h2>
    <ol>
      <li><strong>Download your search terms report</strong> from Google Ads under Insights and reports, then Search terms. Include clicks, cost and conversions.</li>
      <li><strong>Paste it in.</strong> CSV files and rows copied from the Google Ads table both work. Extra title rows are skipped.</li>
      <li><strong>Enter your target CPA</strong> so the tool can flag phrases that cost more than one sale's worth with no sale.</li>
      <li><strong>Switch between 1, 2 and 3 words</strong> and sort by cost or by cost with no conversions.</li>
      <li><strong>Copy the flagged phrases</strong> as phrase match negatives and review them before you upload.</li>
    </ol>

    <h2>How to Read the Report</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Column', 'What it tells you') + '''
      <tbody>
        <tr><td>Terms</td><td>How many different searches contain the phrase</td></tr>
        <tr><td>Cost and clicks</td><td>The total for every search that contains the phrase</td></tr>
        <tr><td>CPA</td><td>Cost divided by conversions for those searches</td></tr>
        <tr><td>No sales</td><td>The phrase has no conversions and has spent at least your target CPA</td></tr>
        <tr><td>High CPA</td><td>The phrase converts, but at more than 1.5 times your target CPA</td></tr>
      </tbody>
    </table></div>
    <p>Each search counts once per phrase, even if a word repeats. Totals across phrases overlap, because one search contains several ngrams, so compare rows with each other rather than adding them up.</p>

    <h2>Tips for Acting on Ngram Data</h2>
    <ul>
      <li><strong>Use a long date range.</strong> Ninety days or more gives each phrase enough clicks to judge fairly.</li>
      <li><strong>Check before you block.</strong> A word like "kids" is waste for an adult shoe store but gold for a toy shop.</li>
      <li><strong>Look for winners too.</strong> Phrases with a low CPA are ideas for new exact match keywords and ad groups.</li>
      <li><strong>Watch conversion lag.</strong> Recent searches may convert later, so judge the last week with care.</li>
    </ul>

    <h2>Turn Insights Into Savings</h2>
    <p>Learn how to set up lists in <a href="''' + B + '''google-ads-negative-keywords/">Google Ads negative keywords</a>, pick a fair target with <a href="''' + B + '''google-ads-bidding-change-target-cpa/">the target CPA bidding change</a>, and report results with a <a href="''' + B + '''paid-media-reporting-dashboard/">paid media reporting dashboard</a>. Then test your new list in the <a href="''' + T + '''negative-keyword-tool/">negative keyword tool</a>.</p>
''',
        faqs=[
            ("Is my search terms report uploaded anywhere?", "No. The report is read and analysed inside your browser. Costs, search terms and conversions never leave your device."),
            ("What does a flagged phrase mean?", "No sales means the phrase spent at least your target CPA without a single conversion. High CPA means it converts, but at more than one and a half times your target."),
            ("Why do the phrase totals add up to more than my spend?", "One search contains several phrases, so its cost is counted in each of them. That overlap is normal. Compare phrases with each other instead of adding them up."),
            ("Can I use this for Microsoft Ads reports?", "Yes. Any report with a search term column and columns for clicks, cost and conversions works, including Microsoft Advertising exports."),
        ],
        related=[("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("Target CPA Bidding Change", "google-ads-bidding-change-target-cpa"),
                 ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard"), ("Python Keyword Research Automation", "python-keyword-research-automation")],
    ))

    # ---------- 6. TRACKING TEMPLATE GENERATOR ----------
    VT = [('ttMt', 'matchtype', '{matchtype}', 'Match type: e, p or b', True), ('ttNet', 'network', '{network}', 'Network: g Search, s partners, d Display', True),
          ('ttDev', 'device', '{device}', 'Device: m mobile, t tablet, c computer', True), ('ttAg', 'adgroupid', '{adgroupid}', 'Ad group ID', False),
          ('ttTid', 'targetid', '{targetid}', 'Keyword or audience ID', False), ('ttLoc', 'loc_physical_ms', '{loc_physical_ms}', 'Location of the click', False),
          ('ttPl', 'placement', '{placement}', 'Site where a Display ad was clicked', False), ('ttUid', 'utm_id', '{campaignid}', 'GA4 campaign ID', False)]
    def vck(i, k, val, note, on):
        return f'<label class="check"><input id="{i}" type="checkbox" class="ttV" data-k="{k}" data-v="{val}"' + (' checked' if on else '') + f'> <span><code>{k}</code> <em style="font-weight:400;color:#666">{note}</em></span></label>'
    TOOLS.append(dict(
        slug='google-ads-tracking-template-generator', short='TT', name='Google Ads Tracking Template Generator',
        card='Build a final URL suffix or tracking template with UTM tags and ValueTrack parameters, and test a sample click.',
        title='Google Ads Tracking Template Generator With UTMs',
        desc='Free Google Ads tracking template generator. Build a final URL suffix or {lpurl} template with UTMs and ValueTrack parameters, then preview a test click.',
        h1='Google Ads Tracking Template Generator',
        lead='Create the final URL suffix or tracking template that adds UTM tags and ValueTrack parameters to every Google Ads click. Preview the landing page URL a real click would produce and catch mistakes before they break your tracking.',
        tool='''<section class="tool" aria-label="Google Ads tracking template generator" id="ttForm">
    <div class="card" style="min-width:0">
      <h2>Your Tracking</h2>
      ''' + F('ttUrl', 'Final URL', 'https://www.example.in/running-shoes/?colour=blue', em='to test a click', mono=True) + '''
      ''' + F('ttMode', 'Where Will You Paste It?', 'suffix', tag='select', opts=[('suffix', 'Final URL suffix (recommended for UTMs)'), ('template', 'Tracking template with {lpurl}')]) + '''
      ''' + R2(F('ttSrc', 'utm_source', 'google', mono=True), F('ttMed', 'utm_medium', 'cpc', mono=True)) + '''
      ''' + F('ttCamp', 'utm_campaign', '{_campaign}', em='text, ValueTrack or custom parameter', mono=True) + '''
      ''' + R2(F('ttTerm', 'utm_term', '{keyword}', mono=True), F('ttCont', 'utm_content', '{creative}', mono=True)) + '''
      <div class="field"><label>Extra ValueTrack Parameters</label>''' + ''.join(vck(*x) for x in VT) + '''</div>
      ''' + F('ttExtra', 'Custom Parameters', 'season={_season}', em='name=value, one per line', tag='textarea', mono=True, extra=' style="min-height:70px"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Code</h2>
      <div class="kw-result" id="ttCheck"></div>
      <pre class="code-out" id="ttOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="ttCopy" type="button">Copy Code</button><span class="toast" id="toast">Copied!</span></div>
      <h3 style="font-size:16px;margin:20px 0 8px">Test Click Landing Page</h3>
      <pre class="code-out" id="ttTest" ''' + ST_(PRE, 'background:#f6faf1;color:#1d3b0a') + '''></pre>
      <div ''' + ST_(SCROLL, 'margin-top:14px') + '''><table class="rtable"><thead><tr><th>Parameter</th><th>Sample value</th></tr></thead><tbody id="ttBody"></tbody></table></div>
      <div class="tips"><strong>Where to paste it</strong><ul><li>Account level: Admin, Account settings, Tracking</li><li>Campaign level: Campaign settings, Additional settings, Campaign URL options</li><li>The most specific level wins</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var out = '';
  var VT = {campaignid: '21543987654', adgroupid: '163245987321', creative: '702145698321', keyword: 'running shoes', matchtype: 'e', network: 'g', device: 'm',
    targetid: 'kwd-2943817', loc_physical_ms: '1007785', loc_interest_ms: '1007785', placement: '', gclid: 'EAIaIQobChMI', feeditemid: '', extensionid: '',
    devicemodel: '', target: '', random: '8823412', ifmobile: '', ifnotmobile: '', ifsearch: '', ifcontent: '', lpurl: '', unescapedlpurl: '', escapedlpurl: ''};
  function sample(val, custom){
    return val.replace(/\{(_?[A-Za-z0-9_+:\[\]]+)\}/g, function(m, k){
      if (k[0] === '_') return custom[k.slice(1).toLowerCase()] || k.slice(1);
      var base = k.split(':')[0];
      if (/^if(mobile|search)$/.test(base)) return k.split(':').slice(1).join(':').replace(/^\[|\]$/g, '');
      if (/^if(notmobile|content)$/.test(base)) return '';
      return VT[base] !== undefined ? encodeURIComponent(VT[base]) : m;
    });
  }
  function run(){
    var iss = [], P = [], mode = $('ttMode').value, keys = {}, customs = [], custom = {campaign: 'spring_sale', season: 'summer'};
    function add(k, val){ if (!val) return; if (keys[k]) iss.push(['bad', 'The parameter ' + c(k) + ' appears twice. Keep one.']); keys[k] = 1; P.push([k, val]); }
    add('utm_source', v('ttSrc')); add('utm_medium', v('ttMed')); add('utm_campaign', v('ttCamp')); add('utm_term', v('ttTerm')); add('utm_content', v('ttCont'));
    document.querySelectorAll('.ttV:checked').forEach(function(x){ add(x.getAttribute('data-k'), x.getAttribute('data-v')); });
    lines('ttExtra').forEach(function(l){
      var m = l.match(/^([^=\s]+)\s*=\s*(.+)$/);
      if (!m){ iss.push(['bad', c(l) + ' is not in ' + c('name=value') + ' form.']); return; }
      add(m[1], m[2].trim());
    });
    if (!keys.utm_source || !keys.utm_medium) iss.push(['warn', 'Add ' + c('utm_source') + ' and ' + c('utm_medium') + '. Google Analytics needs both to name the traffic source.']);
    P.forEach(function(p){
      if (/\s/.test(p[1])) iss.push(['bad', 'The value of ' + c(p[0]) + ' has a space. Spaces break tracking, so use ' + c(p[1].replace(/\s+/g, '_')) + '.']);
      if (/[^A-Za-z0-9_.\-~]/.test(p[0])) iss.push(['bad', 'The name ' + c(p[0]) + ' should only use letters, numbers and underscores.']);
      (p[1].match(/\{[^}]*\}/g) || []).forEach(function(t){
        var k = t.slice(1, -1);
        if (k[0] === '_'){
          var n = k.slice(1);
          if (!/^[A-Za-z0-9]{1,16}$/.test(n)) iss.push(['bad', 'The custom parameter ' + c(t) + ' needs a name of up to 16 letters and numbers only.']);
          else if (customs.indexOf(n) < 0) customs.push(n);
        } else if (/lpurl/i.test(k)){
          iss.push(['bad', c(t) + ' only works at the start of a tracking template, not inside a parameter value.']);
        } else if (VT[k.split(':')[0]] === undefined){
          iss.push(['bad', c(t) + ' is not a Google Ads ValueTrack parameter. Check the spelling, for example ' + c('{campaignid}') + '.']);
        }
      });
      if (p[0] === 'gclid') iss.push(['warn', 'Leave out ' + c('gclid') + '. Auto tagging adds it to every click for you.']);
    });
    if (/\{keyword\}/.test(P.map(function(p){ return p[1]; }).join(''))) iss.push(['warn', c('{keyword}') + ' is blank for Performance Max, Dynamic Search Ads and AI Max clicks without a keyword.']);
    if (customs.length) iss.push(['warn', 'Set a value for ' + customs.map(function(n){ return c('{_' + n + '}'); }).join(', ') + ' in each campaign or ad group under Campaign URL options. Custom parameters cannot be set at account level, and each level allows up to 8.']);
    if (customs.length > 8) iss.push(['bad', 'You use ' + customs.length + ' custom parameters. Google allows up to 8 per level.']);
    var qs = P.map(function(p){ return p[0] + '=' + p[1]; }).join('&');
    out = mode === 'template' ? '{lpurl}?' + qs : qs;
    var u = null; try { u = new URL(v('ttUrl')); } catch(e){}
    var test = '';
    if (!u || !/^https?:$/.test(u.protocol)) iss.push(['bad', 'Add a full final URL starting with ' + c('https://') + ' to test a click.']);
    else {
      P.forEach(function(p){ if (u.searchParams.has(p[0])) iss.push(['warn', 'Your final URL already has ' + c(p[0]) + '. The landing page would get it twice.']); });
      var base = u.href, hash = '';
      if (u.hash){ hash = u.hash; base = base.slice(0, -hash.length); }
      var tqs = sample(qs, custom);
      test = base + (tqs ? (base.indexOf('?') > -1 ? '&' : '?') + tqs : '') + hash;
    }
    $('ttOut').textContent = out || 'Add at least one parameter.';
    $('ttTest').textContent = test || 'Add a valid final URL to see a sample click.';
    $('ttBody').innerHTML = P.map(function(p){ return '<tr><td><code>' + esc(p[0]) + '</code></td><td>' + esc(decodeURIComponent(sample(p[1], custom)) || '(blank)') + '</td></tr>'; }).join('');
    issues('ttCheck', iss, '<strong>Ready to paste.</strong> Add it as your ' + (mode === 'template' ? 'tracking template' : 'final URL suffix') + ' and Google Ads appends it to every click.');
  }
  $('ttForm').addEventListener('input', run); $('ttForm').addEventListener('change', run);
  $('ttCopy').onclick = function(){ copyText(out, 'toast'); };
  run();
''',
        content='''
    <h2>What Is a Google Ads Tracking Template?</h2>
    <p>Google Ads lets you add tracking information to every click without editing each ad. There are two places to do it. The final URL suffix adds parameters to the end of your landing page URL. The tracking template is a full URL built around <code>{lpurl}</code>, which stands for your final URL, and is mainly used for third party click trackers.</p>
    <p>Google recommends the final URL suffix for anything that should reach your landing page, such as UTM tags for Google Analytics. This generator builds either one, fills in ValueTrack parameters that Google replaces with live click data, and shows you the exact URL a test click would land on.</p>

    <h2>How to Use the Tracking Template Generator</h2>
    <ol>
      <li><strong>Enter a final URL</strong> from one of your ads so you can test a click.</li>
      <li><strong>Choose final URL suffix</strong> unless your tracking platform asks for a full template.</li>
      <li><strong>Set your UTM tags.</strong> The defaults use ValueTrack so campaign, keyword and ad IDs fill in by themselves.</li>
      <li><strong>Tick extra parameters</strong> such as match type and device if your analytics or CRM uses them.</li>
      <li><strong>Copy the code</strong> and paste it at account, campaign or ad group level.</li>
    </ol>

    <h2>Common ValueTrack Parameters</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Parameter', 'Fills in with') + '''
      <tbody>
        <tr><td><code>{campaignid}</code></td><td>The campaign ID</td></tr>
        <tr><td><code>{adgroupid}</code></td><td>The ad group ID</td></tr>
        <tr><td><code>{creative}</code></td><td>The ad ID</td></tr>
        <tr><td><code>{keyword}</code></td><td>The keyword that matched the search, not the search itself</td></tr>
        <tr><td><code>{matchtype}</code></td><td><code>e</code> exact, <code>p</code> phrase or <code>b</code> broad</td></tr>
        <tr><td><code>{network}</code></td><td><code>g</code> Google Search, <code>s</code> search partners, <code>d</code> Display, <code>ytv</code> YouTube, <code>x</code> Performance Max</td></tr>
        <tr><td><code>{device}</code></td><td><code>m</code> mobile, <code>t</code> tablet or <code>c</code> computer</td></tr>
      </tbody>
    </table></div>
    <p>See the full list in Google's guide to <a href="https://support.google.com/google-ads/answer/6305348" ''' + EXT + '''>ValueTrack parameters</a>. Custom parameters such as <code>{_campaign}</code> let you add your own values, like a readable campaign name. Their names can be up to 16 letters and numbers, and you set the value in each campaign.</p>

    <h2>Tips for Reliable Click Tracking</h2>
    <ul>
      <li><strong>Keep auto tagging on.</strong> It adds the click ID that Google Ads and Google Analytics use for conversions. UTMs are extra, not a replacement.</li>
      <li><strong>Never use spaces.</strong> Use underscores in values, because spaces break tracking.</li>
      <li><strong>Test before you save.</strong> Use the Test button in Google Ads and check the landing page loads.</li>
      <li><strong>Allow time.</strong> Changes to tracking templates can take a day or two to show in reports.</li>
    </ul>

    <h2>Track Campaigns With Confidence</h2>
    <p>Learn what each tag does in <a href="''' + B + '''utm-parameters-explained/">UTM parameters explained</a>, improve conversion data with <a href="''' + B + '''enhanced-conversions-explained-setup-benefits/">enhanced conversions</a>, and compare credit models in <a href="''' + B + '''attribution-models-explained-digital-marketers/">attribution models explained</a>. Tagging links for other channels? Use the <a href="''' + ANL + '''utm-builder/">UTM builder</a>.</p>
''',
        faqs=[
            ("Should I use a tracking template or a final URL suffix?", "Use the final URL suffix for UTM tags and any parameters your landing page needs. Use a tracking template only when a third party click tracker must redirect the click."),
            ("Do I need UTMs if Google Ads auto tagging is on?", "Not for Google Analytics 4 linked to Google Ads, which uses the click ID. UTMs still help when other tools, like a CRM or a different analytics platform, need to see the campaign."),
            ("Why is utm_term empty for some clicks?", "The keyword parameter is blank when an ad shows without a keyword, such as in Performance Max, Dynamic Search Ads or AI Max. It also holds your keyword, not the exact search."),
            ("What does {lpurl} mean?", "It stands for the final URL of the ad. Google Ads puts the landing page address there when someone clicks, so your template works for every ad without editing."),
        ],
        related=[("UTM Parameters Explained", "utm-parameters-explained"), ("Enhanced Conversions Explained", "enhanced-conversions-explained-setup-benefits"),
                 ("Attribution Models Explained", "attribution-models-explained-digital-marketers"), ("Performance Max Reporting", "google-ads-performance-max-reporting")],
    ))

    # ---------- 7. KEYWORD GROUPER ----------
    KG = '''running shoes for men\t2400
running shoes for women\t1900
mens running shoes\t1300
womens running shoes\t880
running shoes for women with flat feet\t140
nike running shoes\t3600
nike running shoes for men\t1000
nike running shoes for women\t590
asics running shoes\t1600
asics running shoes for men\t480
puma running shoes\t1300
adidas running shoes\t1900
trail running shoes\t1000
trail running shoes for men\t260
best trail running shoes\t320
running shoes for flat feet\t720
best running shoes for flat feet\t390
cushioned running shoes\t480
running shoes under 2000\t1300
running shoes under 3000\t880
running shoes under 5000\t590
cheap running shoes\t720
running shoes sale\t1000
buy running shoes online\t480
waterproof running shoes\t210
running shoes for kids\t590
kids running shoes\t320
lightweight running shoes\t260'''
    TOOLS.append(dict(
        slug='keyword-grouper', short='KG', name='Keyword Grouper',
        card='Group a long keyword list into tight, themed ad groups by shared words, with search volume totals and a CSV export.',
        title='Keyword Grouper: Free Keyword Grouping Tool',
        desc='Free keyword grouper. Paste a keyword list and group it into themed ad groups by shared words, with volume totals and a Google Ads Editor CSV export.',
        h1='Keyword Grouper',
        lead='Paste a long list of keywords and the grouper sorts them into tight themes by the words they share, like brand, audience or price. Rename nothing by hand: export the groups as ad groups for Google Ads Editor in one click.',
        tool='''<section class="tool" aria-label="Keyword grouper" id="kgForm">
    <div class="card" style="min-width:0">
      <h2>Your Keywords</h2>
      ''' + F('kgIn', 'Keywords', KG, em='one per line, volume optional after a tab or comma', tag='textarea', mono=True, extra=' style="min-height:280px"') + '''
      ''' + R2(F('kgMin', 'Smallest Group', '2', tag='select', opts=[('2', '2 keywords'), ('3', '3 keywords'), ('4', '4 keywords'), ('5', '5 keywords')]),
               F('kgMt', 'Match Type for Export', 'Exact', tag='select', opts=[('Broad', 'Broad'), ('Phrase', 'Phrase'), ('Exact', 'Exact')])) + '''
      ''' + F('kgIgn', 'Words to Ignore', '', em='optional, like your main product', ph='shoes', mono=True) + '''
      ''' + CK('kgCommon', 'Ignore words found in most keywords') + CK('kgStem', 'Treat singular and plural as the same word') + CK('kgStop', 'Ignore filler words like for, with, the') + '''
      ''' + F('kgCamp', 'Campaign Name', 'Search | Running Shoes', em='for the export') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Keyword Groups</h2>
      <div class="stats">''' + S('kgN', 'Keywords') + S('kgG', 'Groups') + S('kgU', 'Ungrouped') + S('kgBig', 'Largest Group') + '''</div>
      <div class="kw-result" id="kgCheck"></div>
      <div id="kgOut" class="outline" style="padding:10px 12px"></div>
      <div class="actions"><button class="btn dark" id="kgCsv" type="button">Download Ads Editor CSV</button><button class="btn" id="kgCopy" type="button">Copy Groups</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var groups = [], STOP = {'for':1,'with':1,'the':1,'and':1,'a':1,'of':1,'in':1,'to':1,'on':1,'near':1,'me':1,'by':1,'at':1,'from':1,'my':1,'is':1,'or':1};
  function stem(w){ return $('kgStem').checked && w.length > 3 && /s$/.test(w) && !/ss$/.test(w) ? w.replace(/(ies)$/, 'y').replace(/s$/, '') : w; }
  function title(s){ return s.split(' ').map(function(w){ return w.charAt(0).toUpperCase() + w.slice(1); }).join(' '); }
  function run(){
    var iss = [], items = [], seen = {}, dups = 0;
    lines('kgIn').forEach(function(l){
      var m = l.match(/^(.*?)[\t,;]\s*([\d,. ]+)\s*$/), k = (m ? m[1] : l).toLowerCase().replace(/^["\[]|["\]]$/g, '').replace(/\s+/g, ' ').trim(), vol = m ? parseFloat(m[2].replace(/[, ]/g, '')) || 0 : 0;
      if (!k) return; if (seen[k]){ dups++; return; } seen[k] = 1;
      var toks = k.replace(/[^\p{L}\p{N}' ]+/gu, ' ').split(' ').filter(Boolean);
      items.push({k: k, vol: vol, w: toks.map(stem), o: toks});
    });
    if (dups) iss.push(['warn', dups + ' duplicate keyword' + (dups > 1 ? 's were' : ' was') + ' removed.']);
    var ign = {}; v('kgIgn').toLowerCase().split(/[\s,]+/).filter(Boolean).forEach(function(w){ ign[stem(w)] = 1; });
    if ($('kgStop').checked) Object.keys(STOP).forEach(function(w){ ign[w] = 1; });
    if ($('kgCommon').checked && items.length >= 6){
      var df = {}; items.forEach(function(it){ var d = {}; it.w.forEach(function(w){ if (!d[w]){ d[w] = 1; df[w] = (df[w] || 0) + 1; } }); });
      var common = Object.keys(df).filter(function(w){ return df[w] / items.length >= 0.5; });
      common.forEach(function(w){ ign[w] = 1; });
      if (common.length) iss.push(['warn', 'Ignored ' + common.map(c).join(', ') + ' because ' + (common.length > 1 ? 'they appear' : 'it appears') + ' in most keywords. Untick the option to group by ' + (common.length > 1 ? 'them' : 'it') + '.']);
    }
    var min = +$('kgMin').value, left = items.slice(); groups = [];
    for (var round = 0; round < 400 && left.length; round++){
      var cnt = {};
      left.forEach(function(it){
        var d = {}, w = it.w;
        for (var n = 1; n <= 2; n++) for (var i = 0; i + n <= w.length; i++){
          var g = w.slice(i, i + n); if (g.some(function(x){ return ign[x]; })) continue;
          var key = g.join(' '); if (d[key]) continue; d[key] = 1;
          var a = cnt[key] || (cnt[key] = {k: key, n: g.length, c: 0, vol: 0}); a.c++; a.vol += it.vol;
        }
      });
      var best = null;
      Object.keys(cnt).forEach(function(k){ var a = cnt[k]; if (a.c < min) return;
        if (!best || a.c > best.c || (a.c === best.c && (a.n > best.n || (a.n === best.n && a.vol > best.vol)))) best = a; });
      if (!best) break;
      var bw = best.k.split(' '), inG = [], rest = [];
      var nm = {};
      left.forEach(function(it){ var hit = -1; for (var i = 0; i + bw.length <= it.w.length; i++){ if (bw.every(function(x, j){ return it.w[i + j] === x; })){ hit = i; break; } }
        if (hit > -1){ inG.push(it); var o = it.o.slice(hit, hit + bw.length).join(' '); nm[o] = (nm[o] || 0) + 1; } else rest.push(it); });
      var nmBest = Object.keys(nm).sort(function(a, b){ return nm[b] - nm[a]; })[0] || best.k;
      groups.push({name: title(nmBest), items: inG}); left = rest;
    }
    groups.sort(function(a, b){ return b.items.length - a.items.length; });
    if (left.length) groups.push({name: 'Other', items: left, other: true});
    var real = groups.filter(function(g){ return !g.other; });
    $('kgN').textContent = items.length; $('kgG').textContent = real.length; $('kgU').textContent = left.length;
    $('kgBig').textContent = real.length ? Math.max.apply(null, real.map(function(g){ return g.items.length; })) : 0;
    var big = real.filter(function(g){ return g.items.length > 20; });
    if (big.length) iss.push(['warn', big.map(function(g){ return c(g.name); }).join(', ') + ' has more than 20 keywords. Consider splitting it so ads stay closely matched.']);
    if (!items.length) iss.push(['bad', 'Paste some keywords to group them.']);
    $('kgOut').innerHTML = groups.map(function(g){
      var vol = g.items.reduce(function(s, it){ return s + it.vol; }, 0);
      return '<div style="padding:8px 0;border-bottom:1px dashed #eee"><div style="display:flex;justify-content:space-between;gap:10px;align-items:baseline"><strong style="font-size:15.5px">' + esc(g.name) + '</strong><small style="color:#6b6b6b;font-weight:700;white-space:nowrap">' + g.items.length + ' keywords' + (vol ? ', ' + fmtN(vol) + ' searches' : '') + '</small></div>' +
        '<div class="chips" style="margin:6px 0 0">' + g.items.map(function(it){ return '<span class="chip" style="font-weight:600">' + esc(it.k) + '</span>'; }).join('') + '</div></div>';
    }).join('') || '<p class="empty">Your groups appear here.</p>';
    issues('kgCheck', iss, '<strong>' + items.length + ' keywords sorted into ' + real.length + ' groups.</strong> Review the names, then export.');
  }
  function fmtKw(k){ var t = $('kgMt').value; return t === 'Exact' ? '[' + k + ']' : t === 'Phrase' ? '"' + k + '"' : k; }
  $('kgForm').addEventListener('input', run); $('kgForm').addEventListener('change', run);
  $('kgCsv').onclick = function(){
    var camp = v('kgCamp'), t = $('kgMt').value, L = ['Campaign,Ad group,Keyword,Criterion Type,Search volume'];
    groups.forEach(function(g){ g.items.forEach(function(it){ L.push([camp, g.name, it.k, t, it.vol || ''].map(csvCell).join(',')); }); });
    download('keyword-groups.csv', L.join('\n'), 'text/csv');
  };
  $('kgCopy').onclick = function(){ copyText(groups.map(function(g){ return g.name + '\n' + g.items.map(function(it){ return fmtKw(it.k); }).join('\n'); }).join('\n\n'), 'toast'); };
  run();
''',
        content='''
    <h2>What Is a Keyword Grouper?</h2>
    <p>Keyword research gives you a long, messy list. To use it in Google Ads you need small groups of closely related keywords, so each ad group can have ads and a landing page that match what people searched. Sorting hundreds of keywords by hand takes hours.</p>
    <p>This keyword grouper does the first pass in seconds. It finds the words and word pairs that keywords share, such as a brand, an audience or a price point, and builds a group around each one. Words that appear in nearly every keyword, like your main product, are skipped so they do not swallow the whole list.</p>

    <h2>How to Use the Keyword Grouper</h2>
    <ol>
      <li><strong>Paste your keywords</strong>, one per line. Add search volume after a tab or comma if you have it.</li>
      <li><strong>Pick the smallest group size.</strong> Keywords that do not fit any group go into Other.</li>
      <li><strong>Add words to ignore</strong> if a group is too broad, for example your product name.</li>
      <li><strong>Review the groups.</strong> Change the options until the themes make sense for your account.</li>
      <li><strong>Download the CSV</strong> and import it into Google Ads Editor, or copy the groups into a sheet.</li>
    </ol>

    <h2>How the Grouping Works</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Step', 'What happens') + '''
      <tbody>
        <tr><td>Clean</td><td>Keywords are lower cased, duplicates and symbols are removed</td></tr>
        <tr><td>Count</td><td>Every word and word pair is counted across the remaining keywords</td></tr>
        <tr><td>Pick</td><td>The most shared theme becomes a group. Pairs beat single words on a tie</td></tr>
        <tr><td>Repeat</td><td>Grouped keywords are removed and the next theme is picked until none are left</td></tr>
      </tbody>
    </table></div>
    <p>Each keyword lands in exactly one group, so you never end up bidding on the same keyword in two ad groups. With singular and plural treated as one word, "mens" and "men" or "shoe" and "shoes" stay together.</p>

    <h2>Tips for Tight Ad Groups</h2>
    <ul>
      <li><strong>Aim for one theme per ad group.</strong> If you cannot write one headline that fits every keyword, split the group.</li>
      <li><strong>Watch the Other group.</strong> It often holds unique long tail keywords worth their own group, or ones to drop.</li>
      <li><strong>Use volume to prioritise.</strong> Start with the groups that have the most searches and a clear landing page.</li>
      <li><strong>Brand and price groups convert differently.</strong> Keeping them apart helps Smart Bidding and makes reports clearer.</li>
    </ul>

    <h2>Plan Your Account Structure</h2>
    <p>Find the right keywords with <a href="''' + B + '''best-keyword-research-tools-compared/">the best keyword research tools</a>, weigh effort and reach in <a href="''' + B + '''search-volume-vs-keyword-difficulty/">search volume vs keyword difficulty</a>, and decide on structure with <a href="''' + B + '''search-campaign-vs-performance-max/">Search vs Performance Max</a>. Then format each group with the <a href="''' + T + '''keyword-match-type-generator/">keyword match type generator</a>.</p>
''',
        faqs=[
            ("How many keywords should an ad group have?", "There is no fixed rule, but most well run accounts keep about 5 to 20 closely related keywords per ad group. What matters is that one set of ads and one landing page fit all of them."),
            ("Why are some keywords in the Other group?", "They do not share a theme with enough other keywords to reach your smallest group size. Lower the minimum, or give the best of them their own ad group."),
            ("Can I group thousands of keywords?", "Yes. Everything runs in your browser, so a few thousand keywords group in a second or two on most computers. Very large lists may take a little longer."),
            ("Does it work for SEO keyword clustering?", "It groups by shared words, which works well for planning pages and topic clusters too. It does not compare live search results, so check that each cluster really shares one intent."),
        ],
        related=[("Best Keyword Research Tools Compared", "best-keyword-research-tools-compared"), ("Search Volume vs Keyword Difficulty", "search-volume-vs-keyword-difficulty"),
                 ("Search Campaign vs Performance Max", "search-campaign-vs-performance-max"), ("How to Build Topic Clusters That Rank", "how-to-build-topic-clusters-that-rank")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'google-ads-tools'; t['updated'] = '2026-11-05'
