"""Batch 5 (2026-11-02): Analytics and Tracking Tools category, 7 tools.
Facts checked 2026-11-02 against: GA4 URL builders help (answer 10917952: 9 UTM parameters, values case sensitive),
GA4 default channel group (answer 9756891: rules and paid medium regex), GA4 event collection limits (answer 9267744:
40 char names, 100 char values, 25 params), GA4 event naming rules (answer 13316687: reserved names and prefixes),
GA4 recommended events reference (currency required if value set, items need item_id or item_name),
consent mode guide on developers.google.com (consent types, region, wait_for_update, ads_data_redaction, url_passthrough),
GA regex help (answer 1034324: full match, case sensitive by default) and Search Console filters (answer 17011165:
RE2, partial match, case insensitive by default)."""
import html as _h

GAH = 'https://support.google.com/analytics/answer/'
A = 'https://brandella.in/tools/analytics-tools/'
B = 'https://brandella.in/'
TH = '<thead><tr style="background:#2b2b2b !important;">'
def th(*cols):
    return TH + ''.join(f'<th style="background:#2b2b2b !important; color:#ffffff !important;">{c}</th>' for c in cols) + '</tr></thead>'

def F(i, label, val='', em='', tag='input', opts=None, ph='', extra='', mono=False):
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
        ctl = f'<input id="{i}"{cls} type="text" autocomplete="off" spellcheck="false" value="{_h.escape(val)}" placeholder="{_h.escape(ph)}"{extra}>'
    return f'<div class="field">{lab}{ctl}</div>'

def R2(a, b): return f'<div class="row2">{a}{b}</div>'
def S(i, label): return f'<div class="stat-box"><b id="{i}">0</b><span>{label}</span></div>'
def CK(i, label, on=True): return f'<label class="check"><input id="{i}" type="checkbox"' + (' checked' if on else '') + f'> <span>{label}</span></label>'
PRE = 'style="display:block;margin-top:0;max-height:520px;overflow:auto;word-break:normal;overflow-wrap:anywhere"'

BASEJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function lines(id){ return String($(id).value).split(/\n/).map(function(s){ return s.trim(); }).filter(Boolean); }
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function issues(id, list, okMsg){
    var bad = list.filter(function(i){ return i[0] === 'bad'; }), warn = list.filter(function(i){ return i[0] === 'warn'; });
    var li = function(a){ return '<ul style="margin:6px 0 0 18px">' + a.map(function(i){ return '<li>' + i[1] + '</li>'; }).join('') + '</ul>'; };
    if (bad.length) say(id, 'bad', '<strong>Fix ' + bad.length + ' issue' + (bad.length > 1 ? 's' : '') + '.</strong>' + li(bad.concat(warn)));
    else if (warn.length) say(id, 'warn', '<strong>Works, with ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') + '.</strong>' + li(warn));
    else say(id, 'ok', okMsg);
  }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
'''

UTMJS = r'''
  function norm(s, low, sp){
    s = String(s).trim(); if (low) s = s.toLowerCase();
    if (sp === '_') s = s.replace(/\s+/g, '_'); else if (sp === '-') s = s.replace(/\s+/g, '-');
    return s;
  }
  function enc(s){ return encodeURIComponent(s).replace(/%2F/gi, '/').replace(/%3A/gi, ':'); }
  function fixUrl(u){ u = String(u).trim(); if (u && !/^[a-z][a-z0-9+.\-]*:\/\//i.test(u)) u = 'https://' + u.replace(/^\/+/, ''); return u; }
  function validUrl(u){ try { var x = new URL(u); return /^https?:$/.test(x.protocol) && /\./.test(x.hostname); } catch(e){ return false; } }
  function tag(base, pairs){
    var hash = '', i = base.indexOf('#'); if (i > -1){ hash = base.slice(i); base = base.slice(0, i); }
    var q = '', j = base.indexOf('?'); if (j > -1){ q = base.slice(j + 1); base = base.slice(0, j); }
    var kept = q.split('&').filter(function(p){ return p && !/^utm_/i.test(p.split('=')[0]); });
    var add = pairs.filter(function(p){ return p[1] !== ''; }).map(function(p){ return p[0] + '=' + enc(p[1]); });
    var all = kept.concat(add);
    return base + (all.length ? '?' + all.join('&') : '') + hash;
  }
  var SE = ['google','bing','yahoo','duckduckgo','baidu','yandex','ecosia','naver','seznam'];
  var SO = ['facebook','fb','instagram','ig','linkedin','lnkd.in','twitter','t.co','pinterest','reddit','quora','snapchat','tiktok','tumblr'];
  var VI = ['youtube','vimeo','twitch','dailymotion'];
  function channel(src, med, camp){
    var s = src.toLowerCase(), m = med.toLowerCase(), cp = camp.toLowerCase();
    var sn = s.replace(/^(www\.|m\.|l\.|lm\.)/, '').replace(/\.(com|co\.in|co\.uk|in|net|org)$/, '');
    var paid = /^(.*cp.*|ppc|retargeting|paid.*)$/.test(m), shop = /^(.*(([^a-df-z]|^)shop|shopping).*)$/.test(cp);
    var se = SE.indexOf(sn) > -1, so = SO.indexOf(sn) > -1, vi = VI.indexOf(sn) > -1, em = /^(email|e-mail|e_mail|e mail)$/;
    if (!s && !m) return 'Direct';
    if (cp.indexOf('cross-network') > -1) return 'Cross network';
    if (shop && paid) return 'Paid Shopping';
    if (se && paid) return 'Paid Search';
    if (so && paid) return 'Paid Social';
    if (vi && paid) return 'Paid Video';
    if (['display','banner','expandable','interstitial','cpm'].indexOf(m) > -1) return 'Display';
    if (paid) return 'Paid Other';
    if (shop) return 'Organic Shopping';
    if (so || ['social','social-network','social-media','sm','social network','social media'].indexOf(m) > -1) return 'Organic Social';
    if (vi || /video/.test(m)) return 'Organic Video';
    if (se || m === 'organic') return 'Organic Search';
    if (['referral','app','link'].indexOf(m) > -1) return 'Referral';
    if (em.test(s) || em.test(m)) return 'Email';
    if (m === 'affiliate') return 'Affiliates';
    if (m === 'audio') return 'Audio';
    if (s === 'sms' || m === 'sms') return 'SMS';
    if (/push$/.test(m) || /mobile|notification/.test(m) || s === 'firebase') return 'Mobile Push';
    return 'Unassigned';
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. UTM BUILDER ----------
    presets = [('google|cpc', 'Google Ads'), ('facebook|paid_social', 'Meta Ads'), ('instagram|social', 'Instagram Post'),
               ('linkedin|social', 'LinkedIn Post'), ('newsletter|email', 'Newsletter'), ('whatsapp|social', 'WhatsApp'),
               ('youtube|video', 'YouTube Video'), ('qr_code|print', 'Print QR Code')]
    pbtn = ''.join(f'<button type="button" class="btn btn-sm" data-p="{k}">{t}</button>' for k, t in presets)
    TOOLS.append(dict(
        slug='utm-builder', short='UB', name='UTM Builder',
        card='Build clean campaign URLs with all nine GA4 UTM parameters and see which channel the visit will land in.',
        title='UTM Builder: Free Campaign URL Builder for GA4',
        desc='Free UTM builder for GA4. Add source, medium, campaign and all nine UTM parameters, fix case and spaces, and preview the GA4 channel your link lands in.',
        h1='UTM Builder',
        lead='Fill in your landing page and campaign details to get a clean tracking link. The builder fixes case and spaces, keeps your existing parameters, and shows which GA4 channel the visit will be counted under.',
        tool='''<section class="tool" aria-label="UTM builder" id="ubForm">
    <div class="card" style="min-width:0">
      <h2>Campaign Details</h2>
      ''' + F('ubUrl', 'Website URL', 'https://www.example.com/shoes/running?color=blue', em='landing page', mono=True) + '''
      <p style="font-size:13.5px;color:#666;margin:-8px 0 8px">Quick fill source and medium:</p>
      <div class="chips" id="ubPresets">''' + pbtn + '''</div>
      ''' + R2(F('ubSrc', 'Campaign Source', 'facebook', em='utm_source *', ph='google, newsletter'), F('ubMed', 'Campaign Medium', 'paid_social', em='utm_medium *', ph='cpc, email, social')) + '''
      ''' + R2(F('ubCamp', 'Campaign Name', 'Diwali Sale 2026', em='utm_campaign *', ph='spring_sale'), F('ubId', 'Campaign ID', '', em='utm_id', ph='abc.123')) + '''
      ''' + R2(F('ubTerm', 'Campaign Term', '', em='utm_term', ph='running shoes'), F('ubCont', 'Campaign Content', 'carousel v1', em='utm_content', ph='blue_button')) + '''
      ''' + R2(F('ubPlat', 'Source Platform', '', em='utm_source_platform', ph='Search Ads 360'), F('ubFmt', 'Creative Format', '', em='utm_creative_format', ph='video')) + '''
      ''' + F('ubTac', 'Marketing Tactic', '', em='utm_marketing_tactic', ph='remarketing, prospecting') + '''
      ''' + CK('ubLow', 'Convert values to lowercase (recommended)') + '''
      ''' + F('ubSp', 'Replace Spaces With', '_', tag='select', opts=[('_', 'Underscore _'), ('-', 'Hyphen -'), ('', 'Keep spaces (encoded as %20)')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Tracking Link</h2>
      <pre class="code-out" id="ubOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="ubCopy">Copy Link</button><span class="toast" id="toast">Copied!</span></div>
      <div class="stats" style="margin-top:16px">''' + S('ubCh', 'Likely GA4 Channel') + S('ubN', 'UTM Parameters') + S('ubLen', 'URL Length') + '''</div>
      <div class="kw-result" id="ubCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="ubTable"></table></div>
      <div class="tips"><strong>Good to know</strong><ul><li>Source, medium and campaign should always be set</li><li>GA4 treats <code>Facebook</code> and <code>facebook</code> as two different sources</li><li>Never add UTM tags to links inside your own site</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + UTMJS + r'''
  var F = [['utm_source','ubSrc'],['utm_medium','ubMed'],['utm_campaign','ubCamp'],['utm_id','ubId'],['utm_term','ubTerm'],['utm_content','ubCont'],['utm_source_platform','ubPlat'],['utm_creative_format','ubFmt'],['utm_marketing_tactic','ubTac']];
  function run(){
    var low = $('ubLow').checked, sp = $('ubSp').value, raw = v('ubUrl'), url = fixUrl(raw), iss = [];
    var pairs = F.map(function(f){ return [f[0], norm($(f[1]).value, low, sp)]; });
    var get = function(k){ return pairs.filter(function(p){ return p[0] === k; })[0][1]; };
    if (!raw){ $('ubOut').textContent = 'Enter your landing page URL to build a link.'; say('ubCheck', 'bad', 'Enter the page you want to send people to.'); $('ubTable').innerHTML = ''; ['ubCh','ubN','ubLen'].forEach(function(i){ $(i).textContent = '…'; }); return; }
    if (raw !== url) iss.push(['warn', 'Added ' + c('https://') + ' to the start of your URL.']);
    if (!validUrl(url)) iss.push(['bad', 'The website URL does not look valid. Use a full address like ' + c('https://www.example.com/page') + '.']);
    ['utm_source','utm_medium','utm_campaign'].forEach(function(k){ if (!get(k)) iss.push(['bad', c(k) + ' is empty. GA4 will show (not set) for it.']); });
    if (/[?&]utm_/i.test(raw)) iss.push(['warn', 'Your URL already had UTM tags. They were replaced with the new ones.']);
    if (/[?&](gclid|gbraid|wbraid|dclid)=/i.test(raw)) iss.push(['warn', 'Your URL contains a Google Ads click ID. Remove it, as it belongs to one past click only.']);
    pairs.forEach(function(p){
      var orig = $(F.filter(function(f){ return f[0] === p[0]; })[0][1]).value.trim();
      if (!low && /[A-Z]/.test(p[1])) iss.push(['warn', c(p[0]) + ' has capital letters. Values are case sensitive in GA4, so pick one style and stick to it.']);
      if (sp === '' && /\s/.test(orig)) iss.push(['warn', c(p[0]) + ' has spaces, which become ' + c('%20') + ' in the link.']);
      if (/[&#?=]/.test(orig)) iss.push(['warn', c(p[0]) + ' contains ' + c('& # ? =') + '. They are encoded safely, but plain words are easier to read in reports.']);
    });
    var ch = channel(get('utm_source'), get('utm_medium'), get('utm_campaign'));
    if (ch === 'Unassigned') iss.push(['warn', 'This source and medium do not match any GA4 default channel rule, so the traffic will show as Unassigned. Use a standard medium like ' + c('cpc') + ', ' + c('email') + ', ' + c('social') + ' or ' + c('referral') + ', or create a custom channel group.']);
    var out = validUrl(url) ? tag(url, pairs) : '';
    $('ubOut').textContent = out || 'Fix the URL to see your link.';
    var n = pairs.filter(function(p){ return p[1]; }).length;
    $('ubCh').textContent = ch; $('ubN').textContent = n + ' of 9'; $('ubLen').textContent = out ? out.length : '…';
    if (out.length > 2000) iss.push(['warn', 'The link is over 2,000 characters. Shorten some values.']);
    issues('ubCheck', iss, '<strong>Ready to use.</strong> Source, medium and campaign are set and the link is clean.');
    $('ubTable').innerHTML = '<thead><tr><th>Parameter</th><th>Value in link</th></tr></thead><tbody>' + pairs.filter(function(p){ return p[1]; }).map(function(p){ return '<tr><td><code>' + p[0] + '</code></td><td style="word-break:break-all">' + esc(enc(p[1])) + '</td></tr>'; }).join('') + '</tbody>';
  }
  $('ubPresets').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    var p = b.getAttribute('data-p').split('|'); $('ubSrc').value = p[0]; $('ubMed').value = p[1]; run();
  });
  $('ubForm').addEventListener('input', run); $('ubForm').addEventListener('change', run);
  $('ubCopy').onclick = function(){ if ($('ubOut').textContent.indexOf('http') === 0) copyText($('ubOut').textContent, 'toast'); };
  run();
''',
        content='''
    <h2>What Is a UTM Builder?</h2>
    <p>A UTM builder adds tracking tags to the end of a link so Google Analytics 4 can tell where a visitor came from. Without them, a click from your newsletter or an Instagram story often shows up as Direct or Referral, and you cannot tell which campaign worked.</p>
    <p>This builder supports all nine UTM parameters listed in Google's <a href="''' + GAH + '''10917952" target="_blank" rel="noopener">URL builder guide for GA4</a>, cleans up your values as you type, and predicts the default channel the visit will be counted under using the rules in the <a href="''' + GAH + '''9756891" target="_blank" rel="noopener">GA4 default channel group</a>.</p>

    <h2>How to Use the UTM Builder</h2>
    <ol>
      <li><strong>Paste the landing page URL.</strong> Existing parameters such as a product colour are kept, and old UTM tags are replaced.</li>
      <li><strong>Pick a quick fill button</strong> or type your own source and medium.</li>
      <li><strong>Name the campaign</strong> in a way your whole team will reuse, for example <code>diwali_sale_2026</code>.</li>
      <li><strong>Add content or term</strong> if you want to compare two ads, buttons or keywords inside the same campaign.</li>
      <li><strong>Check the channel and warnings</strong>, then copy the link into your ad, email or post.</li>
    </ol>

    <h2>The Nine UTM Parameters in GA4</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Parameter', 'What it means', 'Example') + '''
      <tbody>
        <tr><td><code>utm_source</code></td><td>Where the visit came from. Always set it.</td><td>google, newsletter</td></tr>
        <tr><td><code>utm_medium</code></td><td>The type of traffic. Always set it.</td><td>cpc, email, social</td></tr>
        <tr><td><code>utm_campaign</code></td><td>The campaign, product or promo. Always set it.</td><td>spring_sale</td></tr>
        <tr><td><code>utm_id</code></td><td>Campaign ID, used to join data you import into GA4</td><td>abc.123</td></tr>
        <tr><td><code>utm_term</code></td><td>Paid keyword</td><td>running shoes</td></tr>
        <tr><td><code>utm_content</code></td><td>Tells apart two links or creatives in one campaign</td><td>top_banner</td></tr>
        <tr><td><code>utm_source_platform</code></td><td>The platform that sent the traffic, such as a buying tool</td><td>Search Ads 360</td></tr>
        <tr><td><code>utm_creative_format</code></td><td>Type of creative. Not yet shown in GA4 reports.</td><td>video, native</td></tr>
        <tr><td><code>utm_marketing_tactic</code></td><td>Targeting used. Not yet shown in GA4 reports.</td><td>remarketing</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Clean Campaign Data</h2>
    <ul>
      <li><strong>Use lowercase everywhere.</strong> GA4 values are case sensitive, so <code>Email</code> and <code>email</code> split your data into two rows.</li>
      <li><strong>Match the medium to a channel.</strong> Paid traffic needs a medium like <code>cpc</code>, <code>ppc</code> or one starting with <code>paid</code>. Organic posts should use <code>social</code>. Mediums like <code>print</code> land in Unassigned unless you build a custom channel group.</li>
      <li><strong>Keep a naming sheet.</strong> Agree on source and campaign names once and reuse them for every link.</li>
      <li><strong>Skip Google Ads if auto tagging is on.</strong> GA4 reads the Google Ads click ID, so manual tags are rarely needed there.</li>
      <li><strong>Never tag internal links.</strong> A UTM tag on a link inside your own site starts a new session and wipes out the real source.</li>
    </ul>

    <h2>Learn More About Campaign Tracking</h2>
    <p>Read <a href="''' + B + '''utm-parameters-explained/">UTM parameters explained</a> for a deeper guide, see how campaign data feeds <a href="''' + B + '''attribution-models-explained-digital-marketers/">attribution models</a>, and learn the basics in <a href="''' + B + '''google-analytics-4-metrics-explained-beginners/">GA4 metrics explained</a>. Tagging many links at once? Use the <a href="''' + A + '''bulk-utm-builder/">bulk UTM builder</a>.</p>
''',
        faqs=[
            ("Which UTM parameters are required?", "Google recommends always setting utm_source, utm_medium and utm_campaign. GA4 still records a visit without them, but reports show (not set) for any parameter you leave out."),
            ("Are UTM parameters case sensitive?", "Yes. GA4 treats utm_source=Facebook and utm_source=facebook as two different sources. Using lowercase for every value is the easiest way to keep reports clean."),
            ("Why does my traffic show as Unassigned in GA4?", "Your source and medium did not match any default channel rule. For example a medium of print or qr does not fit a channel. Use a standard medium such as cpc, email, social or referral, or set up a custom channel group."),
            ("Is my campaign data sent anywhere?", "No. This UTM builder runs entirely in your browser. The links you build are never uploaded or stored."),
        ],
        related=[("UTM Parameters Explained", "utm-parameters-explained"), ("GA4 Metrics Explained for Beginners", "google-analytics-4-metrics-explained-beginners"),
                 ("Attribution Models Explained", "attribution-models-explained-digital-marketers"), ("Email Marketing Strategy", "email-marketing-strategy")],
    ))

    # ---------- 2. BULK UTM BUILDER ----------
    TOOLS.append(dict(
        slug='bulk-utm-builder', short='BU', name='Bulk UTM Builder',
        card='Tag many landing pages for many sources at once and download every link as a CSV.',
        title='Bulk UTM Builder: Create Many UTM Links at Once',
        desc='Free bulk UTM builder. Paste many URLs, list your sources and mediums, and get every tagged link in one table you can copy or download as a CSV file.',
        h1='Bulk UTM Builder',
        lead='Paste your landing pages and the places you will share them. Get a tagged link for every combination in one table, ready to copy or download as a spreadsheet.',
        tool='''<section class="tool" aria-label="Bulk UTM builder" id="buForm">
    <div class="card" style="min-width:0">
      <h2>Pages and Sources</h2>
      ''' + F('buUrls', 'Landing Page URLs', 'https://www.example.com/\nhttps://www.example.com/pricing/\nhttps://www.example.com/blog/ga4-guide/', em='one per line', tag='textarea', mono=True) + '''
      ''' + F('buSrc', 'Source and Medium', 'facebook, paid_social\ninstagram, social\nnewsletter, email\nlinkedin, social', em='source, medium per line', tag='textarea', mono=True) + '''
      ''' + R2(F('buCamp', 'Campaign Name', 'winter launch', em='utm_campaign'), F('buCont', 'Campaign Content', '', em='optional', ph='use {source} or {n}')) + '''
      ''' + R2(F('buTerm', 'Campaign Term', '', em='optional'), F('buId', 'Campaign ID', '', em='optional')) + '''
      ''' + CK('buLow', 'Convert values to lowercase and spaces to underscores') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Tagged Links</h2>
      <div class="stats">''' + S('buN', 'Links Built') + S('buP', 'Pages') + S('buS', 'Sources') + '''</div>
      <div class="kw-result" id="buCheck"></div>
      <div class="actions" style="margin:0 0 14px"><button class="btn dark" id="buCopy">Copy All Links</button><button class="btn" id="buCsv">Download CSV</button><span class="toast" id="toast">Copied!</span></div>
      <div style="overflow:auto;max-height:520px"><table class="rtable" id="buTable" style="font-size:13.5px"></table></div>
    </div>
  </section>''',
        js=BASEJS + UTMJS + r'''
  var rows = [];
  function run(){
    var low = $('buLow').checked, sp = low ? '_' : '', iss = [];
    var urls = lines('buUrls'), srcs = lines('buSrc').map(function(l){ var p = l.split(/[,\t|]/); return [norm(p[0] || '', low, sp), norm(p[1] || '', low, sp)]; });
    var camp = norm(v('buCamp'), low, sp), cont = v('buCont'), term = norm(v('buTerm'), low, sp), id = norm(v('buId'), low, sp);
    rows = [];
    var badU = 0, n = 0;
    urls.forEach(function(u){
      var fu = fixUrl(u); if (!validUrl(fu)){ badU++; return; }
      srcs.forEach(function(s){
        n++; if (rows.length >= 1000) return;
        var ct = norm(cont.replace(/\{source\}/g, s[0]).replace(/\{n\}/g, n), low, sp);
        rows.push({url: fu, src: s[0], med: s[1], link: tag(fu, [['utm_source', s[0]], ['utm_medium', s[1]], ['utm_campaign', camp], ['utm_id', id], ['utm_term', term], ['utm_content', ct]]), ch: channel(s[0], s[1], camp)});
      });
    });
    $('buN').textContent = rows.length; $('buP').textContent = urls.length - badU; $('buS').textContent = srcs.length;
    if (!urls.length) iss.push(['bad', 'Add at least one landing page URL.']);
    if (!srcs.length) iss.push(['bad', 'Add at least one line like ' + c('facebook, paid_social') + '.']);
    if (!camp) iss.push(['bad', 'Add a campaign name.']);
    if (badU) iss.push(['bad', badU + ' URL' + (badU > 1 ? 's do' : ' does') + ' not look valid and ' + (badU > 1 ? 'were' : 'was') + ' skipped.']);
    srcs.forEach(function(s){ if (!s[1]) iss.push(['bad', 'Source ' + c(s[0] || '(empty)') + ' has no medium. Write it as ' + c('source, medium') + '.']); });
    var un = {}; rows.forEach(function(r){ if (r.ch === 'Unassigned' && r.med) un[r.src + ' / ' + r.med] = 1; });
    Object.keys(un).forEach(function(k){ iss.push(['warn', c(k) + ' will show as Unassigned in GA4. Try a standard medium such as ' + c('social') + ', ' + c('email') + ' or ' + c('cpc') + '.']); });
    if (n > 1000) iss.push(['warn', 'Showing the first 1,000 of ' + n + ' links. Split your list to get the rest.']);
    issues('buCheck', iss, '<strong>' + rows.length + ' links ready.</strong> Copy them or download the CSV for your campaign sheet.');
    $('buTable').innerHTML = '<thead><tr><th>Page</th><th>Source</th><th>Medium</th><th>Channel</th><th>Tagged Link</th></tr></thead><tbody>' +
      rows.map(function(r){ return '<tr><td style="word-break:break-all;min-width:120px">' + esc(r.url.replace(/^https?:\/\//, '')) + '</td><td>' + esc(r.src) + '</td><td>' + esc(r.med) + '</td><td>' + r.ch + '</td><td class="mono" style="word-break:break-all;min-width:220px">' + esc(r.link) + '</td></tr>'; }).join('') + '</tbody>';
  }
  function csvCell(s){ s = String(s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  $('buForm').addEventListener('input', run); $('buForm').addEventListener('change', run);
  $('buCopy').onclick = function(){ if (rows.length) copyText(rows.map(function(r){ return r.link; }).join('\n'), 'toast'); };
  $('buCsv').onclick = function(){
    if (!rows.length) return;
    var csv = 'Landing page,Source,Medium,Likely GA4 channel,Tagged link\n' + rows.map(function(r){ return [r.url, r.src, r.med, r.ch, r.link].map(csvCell).join(','); }).join('\n');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(['﻿' + csv], {type: 'text/csv;charset=utf-8'}));
    a.download = 'utm-links.csv'; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };
  run();
''',
        content='''
    <h2>What Is a Bulk UTM Builder?</h2>
    <p>A bulk UTM builder creates many tracking links in one go. Instead of building each link by hand, you list your landing pages and every place you will share them, and the tool creates a tagged link for every combination.</p>
    <p>Three pages shared on four channels means twelve links. Building those by hand invites typos like <code>Facebook</code> in one link and <code>facebook</code> in another, which GA4 counts as two different sources. A bulk builder applies the same rules to every link, so your reports stay clean.</p>

    <h2>How to Use the Bulk UTM Builder</h2>
    <ol>
      <li><strong>Paste your landing pages</strong>, one URL per line. Links without <code>https://</code> are fixed for you.</li>
      <li><strong>List each source and medium</strong> on its own line, separated by a comma, such as <code>newsletter, email</code>.</li>
      <li><strong>Add the campaign name</strong> and any optional term, content or ID values.</li>
      <li><strong>Use placeholders in content</strong>: <code>{source}</code> inserts the source and <code>{n}</code> inserts a running number, so each link gets a unique content value.</li>
      <li><strong>Copy all links or download the CSV</strong> and paste it into your campaign planning sheet.</li>
    </ol>

    <h2>Common Source and Medium Pairs</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Where you share', 'Source', 'Medium', 'GA4 channel') + '''
      <tbody>
        <tr><td>Meta paid ads</td><td><code>facebook</code></td><td><code>paid_social</code></td><td>Paid Social</td></tr>
        <tr><td>Organic Instagram post</td><td><code>instagram</code></td><td><code>social</code></td><td>Organic Social</td></tr>
        <tr><td>Email newsletter</td><td><code>newsletter</code></td><td><code>email</code></td><td>Email</td></tr>
        <tr><td>Microsoft Ads</td><td><code>bing</code></td><td><code>cpc</code></td><td>Paid Search</td></tr>
        <tr><td>Partner website</td><td><code>partner_name</code></td><td><code>referral</code></td><td>Referral</td></tr>
        <tr><td>Affiliate link</td><td><code>affiliate_name</code></td><td><code>affiliate</code></td><td>Affiliates</td></tr>
        <tr><td>Text message</td><td><code>sms</code></td><td><code>sms</code></td><td>SMS</td></tr>
      </tbody>
    </table></div>
    <p>The channel column follows the <a href="''' + GAH + '''9756891" target="_blank" rel="noopener">GA4 default channel group rules</a>. GA4 matches sources against its own list of known sites, so the channel shown in the table is a close guide rather than a promise.</p>

    <h2>Tips for Tagging at Scale</h2>
    <ul>
      <li><strong>Keep one master sheet.</strong> Download the CSV for every campaign so you always know which link went where.</li>
      <li><strong>Lowercase everything.</strong> Leave the lowercase option on unless your team has a different standard.</li>
      <li><strong>Use content for creatives.</strong> When one source gets several ads or buttons, give each a different content value.</li>
      <li><strong>Shorten links for print and SMS.</strong> Long tagged links are fine in ads and emails but look messy in a text message.</li>
    </ul>

    <h2>Related Guides</h2>
    <p>Learn how each tag works in <a href="''' + B + '''utm-parameters-explained/">UTM parameters explained</a>, plan your sends with our <a href="''' + B + '''email-marketing-strategy/">email marketing strategy</a> guide, and report results with a <a href="''' + B + '''paid-media-reporting-dashboard/">paid media reporting dashboard</a>. Need just one link with every GA4 field? Use the <a href="''' + A + '''utm-builder/">UTM builder</a>.</p>
''',
        faqs=[
            ("How many links can I build at once?", "The table shows up to 1,000 links at a time, which covers almost any campaign. If you need more, split your list of pages into smaller groups."),
            ("Can I open the CSV in Excel or Google Sheets?", "Yes. The file uses standard comma separated values with UTF 8 encoding, so it opens cleanly in Excel, Google Sheets and Numbers."),
            ("Does the tool keep existing URL parameters?", "Yes. Parameters already on your landing page, such as a product filter, are kept. Only old UTM tags are replaced so you never end up with two sources in one link."),
            ("Are my URLs uploaded anywhere?", "No. Everything happens in your browser, including the CSV download. Nothing is sent to a server."),
        ],
        related=[("UTM Parameters Explained", "utm-parameters-explained"), ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard"),
                 ("Email Marketing Strategy", "email-marketing-strategy"), ("Customer Journey Mapping", "customer-journey-mapping-digital-marketing")],
    ))

    # ---------- 3. UTM PARAMETER REMOVER ----------
    TOOLS.append(dict(
        slug='utm-parameter-remover', short='UR', name='UTM Parameter Remover',
        card='Strip UTM tags, click IDs and other tracking codes from links while keeping the parameters that matter.',
        title='UTM Parameter Remover: Clean Tracking From URLs',
        desc='Free UTM parameter remover. Strip utm tags, gclid, fbclid, msclkid and other tracking codes from one or many URLs while keeping useful parameters.',
        h1='UTM Parameter Remover',
        lead='Paste one link or a whole list. The tool strips UTM tags, ad click IDs and email tracking codes, keeps every other parameter, and shows exactly what was removed.',
        tool='''<section class="tool" aria-label="UTM parameter remover" id="rmForm">
    <div class="card" style="min-width:0">
      <h2>Links to Clean</h2>
      ''' + F('rmIn', 'URLs', 'https://www.example.com/shoes/?color=blue&utm_source=facebook&utm_medium=paid_social&fbclid=IwAR2xYz\nhttps://shop.example.in/p/123?gclid=Cj0KCQjw&size=9&utm_campaign=diwali\nhttps://www.example.com/blog/?mc_cid=a1b2c3&mc_eid=d4e5f6#comments\nhttps://youtu.be/dQw4w9WgXcQ?si=AbC123xyz', em='one per line', tag='textarea', mono=True, extra=' style="min-height:170px"') + '''
      <p style="font-weight:700;font-size:14.5px;margin-bottom:8px">Remove</p>
      ''' + CK('rmUtm', 'UTM tags (<code>utm_source</code>, <code>utm_medium</code> and every other <code>utm_</code> tag)') + '''
      ''' + CK('rmAds', 'Ad click IDs (<code>gclid</code>, <code>fbclid</code>, <code>msclkid</code>, <code>ttclid</code> and more)') + '''
      ''' + CK('rmMail', 'Email tracking (<code>mc_cid</code>, <code>mc_eid</code>, <code>_hsenc</code>, <code>mkt_tok</code>)') + '''
      ''' + CK('rmGa', 'Analytics linker codes (<code>_ga</code>, <code>_gl</code>)') + '''
      ''' + CK('rmSoc', 'Share codes (<code>igshid</code>, <code>igsh</code>, <code>si</code>, <code>ref_src</code>)') + '''
      ''' + F('rmCustom', 'Also Remove', '', em='your own names, comma separated', ph='ref, aff_id', mono=True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Clean Links</h2>
      <div class="stats">''' + S('rmN', 'Links') + S('rmC', 'Links Cleaned') + S('rmR', 'Codes Removed') + '''</div>
      <pre class="code-out" id="rmOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="rmCopy">Copy Clean Links</button><span class="toast" id="toast">Copied!</span></div>
      <p style="font-weight:700;font-size:14.5px;margin:18px 0 8px">Removed</p>
      <div class="chips" id="rmChips"></div>
      <div class="kw-result" id="rmCheck"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var G = {
    rmAds: ['gclid','gclsrc','gbraid','wbraid','dclid','gad_source','gad_campaignid','msclkid','fbclid','ttclid','twclid','li_fat_id','yclid','epik','sccid','srsltid'],
    rmMail: ['mc_cid','mc_eid','_hsenc','_hsmi','mkt_tok','oly_anon_id','oly_enc_id','vero_id','vero_conv'],
    rmGa: ['_ga','_gl','_gac'],
    rmSoc: ['igshid','igsh','si','ref_src','ref_url']
  };
  var last = [];
  function dec(s){ try { return decodeURIComponent(s.replace(/\+/g, ' ')); } catch(e){ return s; } }
  function run(){
    var custom = v('rmCustom').toLowerCase().split(/[,\s]+/).filter(Boolean), rm = {}, n = 0, cleaned = 0, total = 0, bad = 0;
    var kill = function(k){
      k = k.toLowerCase();
      if ($('rmUtm').checked && /^utm_/.test(k)) return true;
      for (var g in G) if ($(g).checked && G[g].indexOf(k) > -1) return true;
      return custom.indexOf(k) > -1;
    };
    last = lines('rmIn').map(function(u){
      n++;
      var hash = '', i = u.indexOf('#'); if (i > -1){ hash = u.slice(i); u = u.slice(0, i); }
      var j = u.indexOf('?'); if (j < 0) return u + hash;
      var base = u.slice(0, j), parts = u.slice(j + 1).split('&').filter(Boolean), keep = [], gone = 0;
      parts.forEach(function(p){
        var k = dec(p.split('=')[0]);
        if (kill(k)){ gone++; rm[k.toLowerCase()] = (rm[k.toLowerCase()] || 0) + 1; } else keep.push(p);
      });
      if (!/^[a-z][a-z0-9+.\-]*:\/\//i.test(base) && !/^www\./i.test(base)) bad++;
      if (gone){ cleaned++; total += gone; }
      return base + (keep.length ? '?' + keep.join('&') : '') + hash;
    });
    $('rmN').textContent = n; $('rmC').textContent = cleaned; $('rmR').textContent = total;
    $('rmOut').textContent = last.length ? last.join('\n') : 'Paste one or more links on the left.';
    var keys = Object.keys(rm).sort();
    $('rmChips').innerHTML = keys.length ? keys.map(function(k){ return '<span class="chip"><code>' + esc(k) + '</code> ' + rm[k] + '</span>'; }).join('') : '<span class="chip zero">Nothing removed</span>';
    if (!n) say('rmCheck', 'warn', 'Paste at least one link.');
    else if (bad) say('rmCheck', 'warn', bad + ' line' + (bad > 1 ? 's do' : ' does') + ' not start with ' + c('https://') + '. They were still cleaned, but check they are real links.');
    else if (!total) say('rmCheck', 'ok', 'These links are already clean. No tracking codes from the groups you picked were found.');
    else say('rmCheck', 'ok', '<strong>Done.</strong> Removed ' + total + ' tracking code' + (total > 1 ? 's' : '') + ' from ' + cleaned + ' of ' + n + ' link' + (n > 1 ? 's' : '') + '. Other parameters and page anchors were kept.');
  }
  $('rmForm').addEventListener('input', run); $('rmForm').addEventListener('change', run);
  $('rmCopy').onclick = function(){ if (last.length) copyText(last.join('\n'), 'toast'); };
  run();
''',
        content='''
    <h2>What Does a UTM Parameter Remover Do?</h2>
    <p>Links copied from ads, emails and social apps often carry tracking codes at the end, such as <code>utm_source</code>, <code>fbclid</code> or <code>gclid</code>. They make links long and ugly, they can pass old campaign data to the next person who clicks, and they can split one page into many URLs in your reports.</p>
    <p>This tool removes those codes and keeps everything else. A product filter like <code>?color=blue</code> or a page anchor like <code>#reviews</code> stays exactly as it was, so the clean link still opens the same content.</p>

    <h2>How to Use It</h2>
    <ol>
      <li><strong>Paste your links</strong>, one per line. You can paste a single link or hundreds.</li>
      <li><strong>Choose what to remove.</strong> UTM tags and ad click IDs are on by default. Turn groups on or off to suit the job.</li>
      <li><strong>Add your own names</strong> if your site uses other tracking parameters, such as <code>ref</code> or <code>aff_id</code>.</li>
      <li><strong>Copy the clean links</strong> and check the Removed list to see exactly what was stripped.</li>
    </ol>

    <h2>Tracking Codes This Tool Removes</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Code', 'Added by') + '''
      <tbody>
        <tr><td><code>utm_source</code>, <code>utm_medium</code>, <code>utm_campaign</code> and other <code>utm_</code> tags</td><td>Manual campaign tagging for Google Analytics and most other tools</td></tr>
        <tr><td><code>gclid</code>, <code>gbraid</code>, <code>wbraid</code>, <code>dclid</code>, <code>gad_source</code></td><td>Google Ads and Google Marketing Platform auto tagging</td></tr>
        <tr><td><code>srsltid</code></td><td>Google Merchant Center links in search results</td></tr>
        <tr><td><code>fbclid</code></td><td>Facebook and Instagram outbound links</td></tr>
        <tr><td><code>msclkid</code></td><td>Microsoft Advertising auto tagging</td></tr>
        <tr><td><code>ttclid</code>, <code>twclid</code>, <code>li_fat_id</code></td><td>TikTok, X and LinkedIn ads</td></tr>
        <tr><td><code>mc_cid</code>, <code>mc_eid</code>, <code>_hsenc</code>, <code>mkt_tok</code></td><td>Mailchimp, HubSpot and Marketo emails</td></tr>
        <tr><td><code>_gl</code>, <code>_ga</code></td><td>Google Analytics cross domain linking</td></tr>
      </tbody>
    </table></div>

    <h2>When to Remove Tracking Codes</h2>
    <ul>
      <li><strong>Before sharing a link.</strong> If you forward a link with someone else's UTM tags, your visit gets credited to their campaign.</li>
      <li><strong>Before adding a link to your site or sitemap.</strong> Tracking codes create duplicate URLs. Link to the clean version and let your <a href="''' + B + '''canonical-tag-implementation-guide/">canonical tag</a> handle the rest.</li>
      <li><strong>When cleaning report exports.</strong> Strip codes from landing page lists so the same page is counted once.</li>
      <li><strong>Do not strip codes from live ads.</strong> Removing <code>gclid</code> or UTM tags from the final URL of an ad breaks the tracking you pay for.</li>
    </ul>

    <h2>Related Reading</h2>
    <p>See how query strings affect search in <a href="''' + B + '''url-parameters-explained-do-they-hurt-seo/">URL parameters explained</a>, and learn when GA4 needs the <code>_gl</code> code in our <a href="''' + B + '''cross-domain-tracking-ga4-setup-guide/">cross domain tracking guide</a>. To add fresh, consistent tags to a clean link, use the <a href="''' + A + '''utm-builder/">UTM builder</a>.</p>
''',
        faqs=[
            ("Will removing UTM tags break the link?", "No. UTM tags and click IDs only carry tracking data. The page they point to loads the same without them. This tool keeps all other parameters, so filters and IDs that the page needs are left in place."),
            ("What is fbclid?", "fbclid is a click ID that Facebook and Instagram add to outbound links. It helps Meta match visits to ad clicks. It is safe to remove when you share or save a link."),
            ("Should I remove gclid from my Google Ads URLs?", "No. Google Ads adds gclid automatically when auto tagging is on, and GA4 and Google Ads conversion tracking rely on it. Only remove it from links you copy and share elsewhere."),
            ("Are the links I paste stored?", "No. The cleaning happens entirely in your browser and nothing is sent to a server."),
        ],
        related=[("URL Parameters Explained", "url-parameters-explained-do-they-hurt-seo"), ("Cross Domain Tracking in GA4", "cross-domain-tracking-ga4-setup-guide"),
                 ("Canonical Tag Implementation Guide", "canonical-tag-implementation-guide"), ("Referral Spam Explained", "referral-spam-explained-keep-analytics-clean")],
    ))

    # ---------- 4. GA4 EVENT CODE GENERATOR ----------
    ev = [('generate_lead', 'generate_lead (lead form)'), ('sign_up', 'sign_up'), ('login', 'login'), ('search', 'search'), ('share', 'share'),
          ('select_content', 'select_content'), ('add_to_cart', 'add_to_cart'), ('begin_checkout', 'begin_checkout'), ('purchase', 'purchase'), ('custom', 'Custom event')]
    TOOLS.append(dict(
        slug='ga4-event-generator', short='GE', name='GA4 Event Code Generator',
        card='Write GA4 event code for gtag.js or the GTM data layer, checked against Google naming rules and limits.',
        title='GA4 Event Code Generator: gtag and dataLayer Code',
        desc='Free GA4 event code generator. Build gtag.js or GTM dataLayer.push code for recommended or custom events, checked against GA4 naming rules and limits.',
        h1='GA4 Event Code Generator',
        lead='Choose a recommended event or name your own, add parameters, and get ready to paste gtag.js or Google Tag Manager data layer code. Every name and value is checked against GA4 rules as you type.',
        tool='''<section class="tool" aria-label="GA4 event code generator" id="geForm">
    <div class="card" style="min-width:0">
      <h2>Your Event</h2>
      ''' + R2(F('gePreset', 'Start From', 'generate_lead', tag='select', opts=ev), F('geName', 'Event Name', 'generate_lead', mono=True)) + '''
      ''' + F('geParams', 'Event Parameters', 'currency = INR\nvalue = 500\nform_name = contact_page', em='name = value per line', tag='textarea', mono=True) + '''
      ''' + F('geItems', 'Items', '', em='id | name | price | quantity', tag='textarea', mono=True, ph='SKU_123 | Running Shoes | 2499 | 1') + '''
      ''' + R2(F('geFmt', 'Code Type', 'gtag', tag='select', opts=[('gtag', 'gtag.js'), ('dl', 'GTM dataLayer.push')]),
               F('geTrig', 'When to Send', 'now', tag='select', opts=[('now', 'Right away'), ('click', 'On click of an element'), ('submit', 'On form submit')])) + '''
      ''' + F('geSel', 'CSS Selector', '#contact-form', em='for click or submit', mono=True) + '''
      ''' + CK('geWrap', 'Wrap in a <code>&lt;script&gt;</code> tag') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Event Code</h2>
      <div class="kw-result" id="geCheck"></div>
      <pre class="code-out" id="geCode" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="geCopy">Copy Code</button><span class="toast" id="toast">Copied!</span></div>
      <div class="stats" style="margin-top:16px">''' + S('geNp', 'Parameters') + S('geNl', 'Name Length') + S('geNi', 'Items') + '''</div>
      <div class="tips"><strong>Before you publish</strong><ul><li>gtag code needs the Google tag already on the page</li><li>dataLayer code needs a GA4 Event tag in GTM with a matching Custom Event trigger</li><li>Check the event in GA4 DebugView before you rely on it</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var P = {
    generate_lead: ['currency = INR\nvalue = 500\nform_name = contact_page', ''],
    sign_up: ['method = Google', ''], login: ['method = Google', ''], search: ['search_term = running shoes', ''],
    share: ['method = WhatsApp\ncontent_type = article\nitem_id = ga4-guide', ''],
    select_content: ['content_type = product\ncontent_id = SKU_123', ''],
    add_to_cart: ['currency = INR\nvalue = 2499', 'SKU_123 | Running Shoes | 2499 | 1'],
    begin_checkout: ['currency = INR\nvalue = 3298\ncoupon = WINTER10', 'SKU_123 | Running Shoes | 2499 | 1\nSKU_456 | Sports Socks | 799 | 1'],
    purchase: ['transaction_id = T_10045\ncurrency = INR\nvalue = 3298\ntax = 503\nshipping = 0', 'SKU_123 | Running Shoes | 2499 | 1\nSKU_456 | Sports Socks | 799 | 1'],
    custom: ['button_text = Download Price List\npage_section = hero', '']
  };
  var NEED_ITEMS = ['add_to_cart','begin_checkout','purchase','add_to_wishlist','view_item','view_cart','remove_from_cart','add_payment_info','add_shipping_info','refund','view_item_list','select_item'];
  var RES_EV = ['ad_impression','app_remove','app_store_refund','app_store_subscription_cancel','app_store_subscription_renew','click','error','file_download','first_open','first_visit','form_start','form_submit','in_app_purchase','page_view','scroll','session_start','user_engagement','view_complete','video_progress','video_start','view_search_results'];
  var RES_P = ['cid','customer_id','customerid','dclid','gclid','session_id','sessionid','sfmc_id','sid','srsltid','uid','user_id','userid'];
  var LONG = {page_title: 300, page_referrer: 420, page_location: 1000};
  function lit(k, s){
    if (/^(true|false)$/i.test(s)) return s.toLowerCase();
    if (!/_id$/.test(k) && k !== 'coupon' && /^-?(0|[1-9]\d*)(\.\d+)?$/.test(s)) return s;
    return "'" + s.replace(/\\/g, '\\\\').replace(/'/g, "\\'") + "'";
  }
  function run(){
    var name = v('geName'), iss = [], params = [], seen = {};
    if (!name) iss.push(['bad', 'Enter an event name.']);
    else {
      if (!/^\p{L}[\p{L}\p{N}_]*$/u.test(name)) iss.push(['bad', 'Event names must start with a letter and use only letters, numbers and underscores. No spaces.']);
      if (name.length > 40) iss.push(['bad', 'Event name is ' + name.length + ' characters. GA4 allows 40.']);
      if (RES_EV.indexOf(name) > -1) iss.push(['bad', c(name) + ' is reserved or collected automatically by GA4. Pick a different name.']);
      if (/^(firebase_|ga_|google_|gtag\.)/i.test(name)) iss.push(['bad', 'Event names cannot start with ' + c('firebase_') + ', ' + c('ga_') + ', ' + c('google_') + ' or ' + c('gtag.') + '.']);
      if (/[A-Z]/.test(name)) iss.push(['warn', 'Names are case sensitive. Google uses lowercase with underscores, so ' + c(name.toLowerCase()) + ' is safer.']);
    }
    lines('geParams').forEach(function(l){
      var m = l.match(/^([^=:]+)[=:](.*)$/);
      if (!m){ iss.push(['bad', 'Could not read ' + c(l) + '. Write each parameter as ' + c('name = value') + '.']); return; }
      var k = m[1].trim(), val = m[2].trim();
      if (seen[k]){ iss.push(['warn', c(k) + ' is listed twice. The last value is used.']); params = params.filter(function(p){ return p[0] !== k; }); }
      seen[k] = 1; params.push([k, val]);
      if (!/^\p{L}[\p{L}\p{N}_]*$/u.test(k)) iss.push(['bad', 'Parameter ' + c(k) + ' must start with a letter and use only letters, numbers and underscores.']);
      if (/^(_|firebase_|ga_|google_|gtag\.)/i.test(k)) iss.push(['bad', 'Parameter ' + c(k) + ' uses a reserved prefix.']);
      if (RES_P.indexOf(k.toLowerCase()) > -1) iss.push(['warn', c(k) + ' is a reserved name and cannot be used as a custom dimension.']);
      if (k.length > 40) iss.push(['bad', 'Parameter ' + c(k) + ' is ' + k.length + ' characters. GA4 allows 40.']);
      var lim = LONG[k] || 100;
      if (val.length > lim) iss.push(['warn', c(k) + ' value is ' + val.length + ' characters. GA4 keeps only the first ' + lim + '.']);
      if (!val) iss.push(['warn', c(k) + ' has no value.']);
    });
    var items = lines('geItems').map(function(l){
      var p = l.split('|').map(function(s){ return s.trim(); }), it = [];
      if (p[0]) it.push(['item_id', "'" + p[0].replace(/'/g, "\\'") + "'"]);
      if (p[1]) it.push(['item_name', "'" + p[1].replace(/'/g, "\\'") + "'"]);
      if (p[2]){ var pr = parseFloat(p[2].replace(/,/g, '')); if (isFinite(pr)) it.push(['price', String(pr)]); else iss.push(['bad', 'Item price ' + c(p[2]) + ' must be a number.']); }
      if (p[3]){ var q = parseInt(p[3], 10); if (q > 0) it.push(['quantity', String(q)]); else iss.push(['bad', 'Item quantity ' + c(p[3]) + ' must be a whole number above zero.']); }
      if (!p[0] && !p[1]) iss.push(['bad', 'Each item needs an ID or a name.']);
      return it;
    });
    var total = params.length + (items.length ? 1 : 0);
    if (total > 25) iss.push(['bad', 'This event has ' + total + ' parameters. GA4 accepts 25 per event.']);
    if (seen.value && !seen.currency) iss.push(['bad', 'Add ' + c('currency') + '. GA4 needs it whenever you send ' + c('value') + '.']);
    params.forEach(function(p){ if (p[0] === 'currency' && !/^[A-Z]{3}$/.test(p[1])) iss.push(['warn', 'Currency should be a three letter ISO code in capitals, such as ' + c('INR') + ' or ' + c('USD') + '.']); if (p[0] === 'value' && !/^-?\d+(\.\d+)?$/.test(p[1])) iss.push(['bad', c('value') + ' must be a plain number with no currency symbol or commas.']); });
    if (NEED_ITEMS.indexOf(name) > -1 && !items.length) iss.push(['bad', c(name) + ' needs at least one item.']);
    if (name === 'purchase' && !seen.transaction_id) iss.push(['bad', c('purchase') + ' needs a ' + c('transaction_id') + ' so GA4 can remove duplicate purchases.']);
    if (name === 'search' && !seen.search_term) iss.push(['bad', c('search') + ' needs a ' + c('search_term') + '.']);
    var fmt = v('geFmt'), ind = '    ', body, code;
    var plist = params.map(function(p){ return [p[0], lit(p[0], p[1])]; });
    var itemsStr = items.length ? 'x' : '';
    var itemsAt = function(pad){ return '[\n' + items.map(function(it){ return pad + '  { ' + it.map(function(x){ return x[0] + ': ' + x[1]; }).join(', ') + ' }'; }).join(',\n') + '\n' + pad + ']'; };
    var objLines = function(pad){ var a = plist.map(function(p){ return pad + p[0] + ': ' + p[1]; }); if (items.length) a.push(pad + 'items: ' + itemsAt(pad)); return a.join(',\n'); };
    if (fmt === 'gtag'){
      body = "gtag('event', '" + name + "'" + (plist.length || itemsStr ? ', {\n' + objLines('  ') + '\n})' : ')') + ';';
    } else if (itemsStr){
      body = 'window.dataLayer = window.dataLayer || [];\ndataLayer.push({ ecommerce: null });\ndataLayer.push({\n  event: \'' + name + '\',\n  ecommerce: {\n' + objLines('    ') + '\n  }\n});';
    } else {
      body = 'window.dataLayer = window.dataLayer || [];\ndataLayer.push({\n  event: \'' + name + "'" + (plist.length ? ',\n' + objLines('  ') : '') + '\n});';
    }
    var trig = v('geTrig'), sel = v('geSel').replace(/'/g, "\\'");
    var indent = function(s, n){ return s.split('\n').map(function(l){ return new Array(n + 1).join(' ') + l; }).join('\n'); };
    if (trig !== 'now'){
      if (!sel) iss.push(['bad', 'Enter a CSS selector such as ' + c('#contact-form') + ' or ' + c('.buy-button') + '.']);
      else { try { document.querySelector(sel.replace(/\\'/g, "'")); } catch(e){ iss.push(['bad', c(v('geSel')) + ' is not a valid CSS selector.']); } }
      code = "document.addEventListener('" + trig + "', function (e) {\n  if (!e.target.closest || !e.target.closest('" + sel + "')) return;\n" + indent(body, 2) + '\n});';
    } else code = body;
    if ($('geWrap').checked) code = '<script>\n' + indent(code, 2) + '\n<\/script>';
    $('geCode').textContent = code;
    $('geNp').textContent = total + ' / 25'; $('geNl').textContent = name.length + ' / 40'; $('geNi').textContent = items.length;
    issues('geCheck', iss, '<strong>Valid.</strong> The event name and parameters follow GA4 naming rules and limits.');
  }
  $('gePreset').onchange = function(){
    var k = this.value, p = P[k]; $('geName').value = k === 'custom' ? 'download_price_list' : k; $('geParams').value = p[0]; $('geItems').value = p[1];
    if (k === 'custom'){ $('geTrig').value = 'click'; $('geSel').value = '.price-list-button'; }
    run();
  };
  $('geForm').addEventListener('input', run); $('geForm').addEventListener('change', function(e){ if (e.target.id !== 'gePreset') run(); });
  $('geCopy').onclick = function(){ copyText($('geCode').textContent, 'toast'); };
  run();
''',
        content='''
    <h2>What Is a GA4 Event Code Generator?</h2>
    <p>Everything Google Analytics 4 records is an event. Page views and scrolls are collected for you, but leads, sign ups, purchases and button clicks usually need a few lines of code. This generator writes that code for you, either as a <code>gtag()</code> call for sites using the Google tag, or as a <code>dataLayer.push()</code> for sites using Google Tag Manager.</p>
    <p>Small mistakes break events quietly. A space in a name, a value sent as text with a currency symbol, or a missing <code>currency</code> can mean GA4 drops the data or shows zero revenue. The checker flags these problems as you type, using Google's <a href="''' + GAH + '''13316687" target="_blank" rel="noopener">event naming rules</a> and <a href="''' + GAH + '''9267744" target="_blank" rel="noopener">event collection limits</a>.</p>

    <h2>How to Use the Generator</h2>
    <ol>
      <li><strong>Pick a recommended event</strong> such as <code>generate_lead</code> or <code>purchase</code>, or choose Custom event and type your own name.</li>
      <li><strong>Edit the parameters</strong>, one per line, as <code>name = value</code>. Numbers are sent as numbers, and IDs stay as text.</li>
      <li><strong>Add items</strong> for ecommerce events, one product per line, as <code>id | name | price | quantity</code>.</li>
      <li><strong>Choose gtag.js or dataLayer</strong> and when the event should fire: right away, on a click, or on a form submit.</li>
      <li><strong>Copy the code</strong> into your page, then confirm the event arrives in GA4 DebugView.</li>
    </ol>

    <h2>GA4 Event Rules and Limits</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Rule', 'Limit') + '''
      <tbody>
        <tr><td>Event name length</td><td>40 characters</td></tr>
        <tr><td>Parameter name length</td><td>40 characters</td></tr>
        <tr><td>Parameter value length</td><td>100 characters (<code>page_title</code> 300, <code>page_referrer</code> 420, <code>page_location</code> 1,000)</td></tr>
        <tr><td>Parameters per event</td><td>25</td></tr>
        <tr><td>Allowed characters</td><td>Letters, numbers and underscores, starting with a letter</td></tr>
        <tr><td>Reserved prefixes</td><td><code>_</code>, <code>firebase_</code>, <code>ga_</code>, <code>google_</code>, <code>gtag.</code></td></tr>
        <tr><td>Value and currency</td><td>If you send <code>value</code>, also send a three letter <code>currency</code></td></tr>
        <tr><td>Items</td><td>Each item needs <code>item_id</code> or <code>item_name</code></td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Reliable Event Tracking</h2>
    <ul>
      <li><strong>Use recommended events first.</strong> Names like <code>generate_lead</code> and <code>purchase</code> unlock built in reports. See the full list in Google's <a href="https://developers.google.com/analytics/devguides/collection/ga4/reference/events" target="_blank" rel="noopener">recommended events reference</a>.</li>
      <li><strong>Keep names lowercase.</strong> Names are case sensitive, so <code>Sign_Up</code> and <code>sign_up</code> are two separate events.</li>
      <li><strong>Register custom parameters.</strong> To see a custom parameter in reports, create a custom dimension for it in GA4 Admin.</li>
      <li><strong>Mark key events.</strong> Sending an event does not make it a conversion. Mark it as a key event in GA4 once it shows up.</li>
      <li><strong>Clear old ecommerce data in GTM.</strong> The <code>ecommerce: null</code> push stops items from one event leaking into the next.</li>
    </ul>

    <h2>Go Further With GA4 Events</h2>
    <p>Follow our step by step guide to <a href="''' + B + '''ga4-custom-event-tracking-google-tag-manager/">GA4 custom event tracking in Google Tag Manager</a>, copy full examples from <a href="''' + B + '''ga4-ecommerce-events-examples/">GA4 ecommerce events examples</a>, and learn the <a href="''' + B + '''ga4-events-vs-conversions-difference/">difference between events and conversions</a>. Testing a filter on your new event names? Try the <a href="''' + A + '''ga4-regex-tester/">GA4 regex tester</a>.</p>
''',
        faqs=[
            ("Should I use gtag.js or dataLayer code?", "Use gtag.js code if your site loads the Google tag directly. Use dataLayer.push code if you manage tags in Google Tag Manager, then create a GA4 Event tag with a Custom Event trigger that matches the event name."),
            ("Why is my event not showing in GA4 reports?", "Standard reports can take up to a day to update. Check DebugView or the Realtime report first. If the event is missing there, look for a name with spaces or capitals, a reserved name, or code that runs before the Google tag loads."),
            ("Do I need to send currency with value?", "Yes. Google's reference says currency is required whenever you set value. Without it, revenue and value metrics are not calculated correctly."),
            ("Is my event data uploaded?", "No. The code is generated in your browser and nothing you type is sent to a server."),
        ],
        related=[("GA4 Custom Event Tracking With GTM", "ga4-custom-event-tracking-google-tag-manager"), ("GA4 Ecommerce Events Examples", "ga4-ecommerce-events-examples"),
                 ("GTM Data Layer Explained", "gtm-data-layer-explained"), ("Track Button Clicks in GA4", "track-button-clicks-ga4")],
    ))

    # ---------- 5. CONSENT MODE V2 GENERATOR ----------
    EEA = 'AT, BE, BG, HR, CY, CZ, DK, EE, FI, FR, DE, GR, HU, IE, IT, LV, LT, LU, MT, NL, PL, PT, RO, SK, SI, ES, SE, IS, LI, NO, GB, CH'
    types = [('ad_storage', 'denied'), ('analytics_storage', 'denied'), ('ad_user_data', 'denied'), ('ad_personalization', 'denied'),
             ('functionality_storage', 'granted'), ('personalization_storage', 'denied'), ('security_storage', 'granted')]
    GD = [('denied', 'Denied'), ('granted', 'Granted')]
    tsel = ''.join(R2(F('cm_' + types[i][0], f'<code>{types[i][0]}</code>', types[i][1], tag='select', opts=GD),
                      F('cm_' + types[i + 1][0], f'<code>{types[i + 1][0]}</code>', types[i + 1][1], tag='select', opts=GD) if i + 1 < len(types) else '')
                   for i in range(0, len(types), 2))
    TOOLS.append(dict(
        slug='consent-mode-v2-generator', short='CM', name='Consent Mode v2 Generator',
        card='Generate Google consent mode v2 default and update code with regions, wait time and privacy settings.',
        title='Consent Mode v2 Generator: Google Consent Code',
        desc='Free Google consent mode v2 generator. Create gtag consent default and update code with ad_user_data, ad_personalization, regions and wait_for_update.',
        h1='Consent Mode v2 Generator',
        lead='Choose your default consent settings and where they apply. Get the consent default code for every page, plus the update code your cookie banner runs when a visitor accepts or rejects.',
        tool='''<section class="tool" aria-label="Consent mode v2 generator" id="cmForm">
    <div class="card" style="min-width:0">
      <h2>Default Consent Settings</h2>
      ''' + F('cmScope', 'Where Do These Defaults Apply?', 'regions', tag='select', opts=[('regions', 'Only in the regions below'), ('all', 'Everywhere')]) + '''
      ''' + F('cmRegions', 'Regions', EEA, em='country codes, comma separated', tag='textarea', mono=True, extra=' style="min-height:80px"') + '''
      <div class="actions" style="margin:-8px 0 16px"><button type="button" class="btn btn-sm" id="cmEea">EEA, UK and Switzerland</button><button type="button" class="btn btn-sm" id="cmUs">US states with privacy laws</button></div>
      ''' + F('cmElse', 'Everywhere Else', 'granted', tag='select', opts=[('granted', 'Grant all consent types'), ('same', 'Use the same defaults'), ('none', 'No default (leave it out)')]) + '''
      ''' + tsel + '''
      ''' + R2(F('cmWait', 'Wait for Update', '500', em='milliseconds'), F('cmId', 'Google Tag ID', 'G-ABC123XYZ9', em='optional', mono=True)) + '''
      ''' + CK('cmRed', 'Redact ads data when <code>ad_storage</code> is denied (<code>ads_data_redaction</code>)') + '''
      ''' + CK('cmPass', 'Pass ad click info through URLs (<code>url_passthrough</code>)', False) + '''
      ''' + CK('cmTag', 'Include the Google tag snippet after the consent code') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>1. Consent Default Code</h2>
      <div class="kw-result" id="cmCheck"></div>
      <p style="font-size:13.5px;color:#666;margin-bottom:8px">Paste into the <code>&lt;head&gt;</code> of every page, above your Google tag or Tag Manager snippet.</p>
      <pre class="code-out" id="cmCode" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="cmCopy">Copy Default Code</button><span class="toast" id="toast">Copied!</span></div>
      <h2 style="margin-top:26px">2. Consent Update Code</h2>
      <p style="font-size:13.5px;color:#666;margin-bottom:8px">Call these functions from your banner buttons, and again on later visits once you know the saved choice.</p>
      <pre class="code-out" id="cmUpd" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="cmCopy2">Copy Update Code</button><span class="toast" id="toast2">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var T = ['ad_storage','analytics_storage','ad_user_data','ad_personalization','functionality_storage','personalization_storage','security_storage'];
  var EEA = "''' + EEA + r'''";
  var US = 'US-CA, US-CO, US-CT, US-VA, US-UT, US-TX, US-OR, US-MT, US-DE, US-IA, US-NE, US-NH, US-NJ, US-TN, US-MN, US-MD, US-IN, US-KY, US-RI';
  function obj(map, extra, pad){
    var a = [];
    T.forEach(function(t){ a.push(pad + "'" + t + "': '" + map[t] + "'"); });
    (extra || []).forEach(function(x){ a.push(pad + x); });
    return '{\n' + a.join(',\n') + '\n' + pad.slice(2) + '}';
  }
  function run(){
    var iss = [], d = {}, scope = v('cmScope'), els = v('cmElse'), wait = v('cmWait'), id = v('cmId');
    T.forEach(function(t){ d[t] = $('cm_' + t).value; });
    $('cmRegions').disabled = scope !== 'regions'; $('cmElse').disabled = scope !== 'regions';
    var regs = v('cmRegions').toUpperCase().split(/[\s,;]+/).filter(Boolean), badR = regs.filter(function(r){ return !/^[A-Z]{2}(-[A-Z0-9]{1,3})?$/.test(r); });
    var uniq = regs.filter(function(r, i){ return regs.indexOf(r) === i; });
    if (scope === 'regions'){
      if (!regs.length) iss.push(['bad', 'Add at least one region code, or choose Everywhere.']);
      if (badR.length) iss.push(['bad', 'These region codes look wrong: ' + badR.slice(0, 6).map(c).join(', ') + '. Use two letter country codes like ' + c('DE') + ', or country and region like ' + c('US-CA') + '.']);
      if (els === 'none') iss.push(['warn', 'Without a default for other places, tags elsewhere run as if consent were granted. That is fine only if you are sure no consent banner is needed there.']);
    }
    var w = parseInt(wait, 10);
    if (wait && !(/^\d+$/.test(wait))) iss.push(['bad', c('wait_for_update') + ' must be a whole number of milliseconds, such as 500.']);
    else if (w > 2000) iss.push(['warn', 'A wait over 2,000 ms delays every tag on the page. Most banners need 500 ms or less.']);
    if (id && !/^(G|AW|GT|DC)-[A-Z0-9]{4,}$/i.test(id)) iss.push(['warn', c(id) + ' does not look like a Google tag ID. It usually starts with ' + c('G-') + ' or ' + c('AW-') + '.']);
    if (d.ad_storage === 'granted' && d.ad_user_data === 'denied') iss.push(['warn', c('ad_storage') + ' is granted but ' + c('ad_user_data') + ' is denied. Check that this matches what your banner asks.']);
    if (d.security_storage === 'denied') iss.push(['warn', c('security_storage') + ' covers fraud prevention and logins. It is normally granted.']);
    if (Object.keys(d).every(function(k){ return d[k] === 'granted'; }) && (scope === 'all')) iss.push(['warn', 'Every type is granted by default everywhere. Consent mode is meant to start as denied where consent is required.']);
    var extra = [];
    if (wait && /^\d+$/.test(wait)) extra.push("'wait_for_update': " + w);
    var L = ['<script>', '  window.dataLayer = window.dataLayer || [];', '  function gtag(){dataLayer.push(arguments);}', ''];
    if (scope === 'regions'){
      L.push('  // Defaults for visitors in these regions');
      L.push("  gtag('consent', 'default', " + obj(d, extra.concat(["'region': [" + uniq.map(function(r){ return "'" + r + "'"; }).join(', ') + ']']), '    ') + ');');
      if (els !== 'none'){
        var g = {}; T.forEach(function(t){ g[t] = els === 'granted' ? 'granted' : d[t]; });
        L.push('', '  // Defaults for everyone else');
        L.push("  gtag('consent', 'default', " + obj(g, els === 'same' ? extra : [], '    ') + ');');
      }
    } else L.push("  gtag('consent', 'default', " + obj(d, extra, '    ') + ');');
    if ($('cmRed').checked) L.push('', "  gtag('set', 'ads_data_redaction', true);");
    if ($('cmPass').checked) L.push(($('cmRed').checked ? '' : '\n') + "  gtag('set', 'url_passthrough', true);");
    L.push('<\/script>');
    if ($('cmTag').checked){
      if (!id) iss.push(['warn', 'Add your Google tag ID to include the Google tag snippet.']);
      else L.push('', '<!-- Google tag (gtag.js) -->', '<script async src="https://www.googletagmanager.com/gtag/js?id=' + id.toUpperCase() + '"><\/script>', '<script>', "  gtag('js', new Date());", "  gtag('config', '" + id.toUpperCase() + "');", '<\/script>');
    }
    $('cmCode').textContent = L.join('\n');
    var all = function(s){ var m = {}; T.forEach(function(t){ m[t] = s; }); m.security_storage = 'granted'; return m; };
    var up = all('granted'), dn = all('denied');
    $('cmUpd').textContent = '<script>\n  function consentAcceptAll() {\n    gtag(\'consent\', \'update\', ' + obj(up, [], '      ') + ');\n  }\n\n  function consentRejectAll() {\n    gtag(\'consent\', \'update\', ' + obj(dn, [], '      ') + ');\n  }\n<\/script>';
    issues('cmCheck', iss, '<strong>Ready.</strong> Defaults are set for all seven consent types' + (scope === 'regions' ? ' in ' + uniq.length + ' region' + (uniq.length > 1 ? 's' : '') : '') + '.');
  }
  $('cmEea').onclick = function(){ $('cmRegions').value = EEA; $('cmScope').value = 'regions'; run(); };
  $('cmUs').onclick = function(){ $('cmRegions').value = US; $('cmScope').value = 'regions'; run(); };
  $('cmForm').addEventListener('input', run); $('cmForm').addEventListener('change', run);
  $('cmCopy').onclick = function(){ copyText($('cmCode').textContent, 'toast'); };
  $('cmCopy2').onclick = function(){ copyText($('cmUpd').textContent, 'toast2'); };
  run();
''',
        content='''
    <h2>What Is Google Consent Mode v2?</h2>
    <p>Consent mode tells Google tags what a visitor has agreed to. When a visitor says no to cookies, tags stop setting advertising and analytics cookies but can still send basic, cookieless signals. Google then uses those signals to model the conversions and visits you would otherwise lose.</p>
    <p>Version 2 added two consent types, <code>ad_user_data</code> and <code>ad_personalization</code>. Google requires them for advertisers who want to keep audience and measurement features for visitors in the European Economic Area. The code this tool writes follows Google's <a href="https://developers.google.com/tag-platform/security/guides/consent" target="_blank" rel="noopener">consent mode setup guide for websites</a>.</p>

    <h2>How to Use the Generator</h2>
    <ol>
      <li><strong>Choose where the defaults apply.</strong> Most sites deny by default in the EEA, UK and Switzerland and grant elsewhere.</li>
      <li><strong>Set each consent type.</strong> Advertising and analytics start as denied. Security storage normally stays granted.</li>
      <li><strong>Keep a short wait.</strong> <code>wait_for_update</code> gives your cookie banner time to load a saved choice before tags fire. 500 ms suits most banners.</li>
      <li><strong>Paste the default code</strong> into the head of every page, above the Google tag or Tag Manager container.</li>
      <li><strong>Connect the update code</strong> to your banner's Accept and Reject buttons, and run it again on each page view once the choice is saved.</li>
    </ol>

    <h2>The Seven Consent Types</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Consent type', 'What it controls') + '''
      <tbody>
        <tr><td><code>ad_storage</code></td><td>Cookies and storage used for advertising</td></tr>
        <tr><td><code>analytics_storage</code></td><td>Cookies used for analytics, such as visit length</td></tr>
        <tr><td><code>ad_user_data</code></td><td>Sending user data to Google for advertising (new in v2)</td></tr>
        <tr><td><code>ad_personalization</code></td><td>Personalized advertising such as remarketing (new in v2)</td></tr>
        <tr><td><code>functionality_storage</code></td><td>Storage that makes the site work, such as language settings</td></tr>
        <tr><td><code>personalization_storage</code></td><td>Storage for personal features such as recommendations</td></tr>
        <tr><td><code>security_storage</code></td><td>Storage for security, logins and fraud prevention</td></tr>
      </tbody>
    </table></div>

    <h2>Basic or Advanced Consent Mode?</h2>
    <p>In <strong>basic</strong> mode, Google tags do not load at all until the visitor accepts, so nothing is sent before consent. In <strong>advanced</strong> mode, tags load straight away with consent denied and send cookieless pings, which gives Google more data to model with. The default code from this tool works for both. For basic mode, your consent platform also blocks the tags until the visitor accepts.</p>
    <ul>
      <li><strong>Order matters.</strong> The default command must run before any <code>config</code> or <code>event</code> command, or the defaults are ignored.</li>
      <li><strong>Region specific defaults win.</strong> A default with a <code>region</code> list overrides the general default for visitors in those places.</li>
      <li><strong>Test with Tag Assistant.</strong> Check that consent shows as denied on load and changes to granted after you accept.</li>
    </ul>

    <h2>Learn More</h2>
    <p>Read <a href="''' + B + '''consent-mode-v2-explained-website-owners/">consent mode v2 explained for website owners</a>, see why <a href="''' + B + '''data-privacy-and-first-party-data/">first party data and privacy</a> matter more each year, and consider <a href="''' + B + '''what-is-server-side-tagging-guide/">server side tagging</a> for more control. Ready to send events once consent is in place? Use the <a href="''' + A + '''ga4-event-generator/">GA4 event code generator</a>.</p>
''',
        faqs=[
            ("Where do I put the consent mode code?", "Put the default code in the head of every page, above the Google tag or Google Tag Manager snippet. It must run before any config or event command so the defaults apply to the very first hit."),
            ("Does this replace a cookie banner?", "No. Consent mode only passes the visitor's choice to Google tags. You still need a cookie banner or consent management platform to ask for consent and call the update code."),
            ("What does wait_for_update do?", "It tells Google tags to wait a set number of milliseconds for an update command before sending data. This gives your banner time to load a choice the visitor made on an earlier visit."),
            ("Is anything I enter uploaded?", "No. The code is built in your browser and nothing you type is sent to a server."),
        ],
        related=[("Consent Mode v2 Explained", "consent-mode-v2-explained-website-owners"), ("Data Privacy and First Party Data", "data-privacy-and-first-party-data"),
                 ("What Is Server Side Tagging", "what-is-server-side-tagging-guide"), ("Enhanced Conversions Setup in GTM", "enhanced-conversions-setup-gtm")],
    ))

    # ---------- 6. GA4 REGEX TESTER ----------
    TOOLS.append(dict(
        slug='ga4-regex-tester', short='RX', name='GA4 Regex Tester',
        card='Test regular expressions for GA4 and Search Console filters, with full and partial match modes.',
        title='GA4 Regex Tester: Test Regex for Analytics and GSC',
        desc='Free regex tester for Google Analytics 4 and Search Console. Test full or partial matches, catch RE2 errors, and turn a list of pages into a ready regex.',
        h1='GA4 Regex Tester',
        lead='Paste a regular expression and the values you want to filter. See which ones match exactly the way GA4 or Search Console would, spot syntax that Google does not support, and build a regex from a simple list.',
        tool='''<section class="tool" aria-label="GA4 regex tester" id="rxForm">
    <div class="card" style="min-width:0">
      <h2>Your Regex</h2>
      ''' + F('rxMode', 'Test As', 'ga4full', tag='select', opts=[('ga4full', 'GA4 matches regex (full match)'), ('ga4part', 'GA4 partially matches regex'), ('gsc', 'Search Console custom regex (partial, ignores case)')]) + '''
      ''' + F('rxRe', 'Regular Expression', '/blog/(seo|ppc|analytics)/.*', mono=True) + '''
      ''' + CK('rxCase', 'Ignore case', False) + '''
      ''' + F('rxTest', 'Values to Test', '/blog/seo/title-tags/\n/blog/ppc/roas-guide/\n/blog/social/instagram-tips/\n/Blog/SEO/old-url/\n/shop/seo-book/\n/blog/analytics/', em='one per line', tag='textarea', mono=True, extra=' style="min-height:150px"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Results</h2>
      <div class="stats">''' + S('rxM', 'Match') + S('rxN', 'No Match') + S('rxL', 'Regex Length') + '''</div>
      <div class="kw-result" id="rxCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="rxTable"></table></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Build a Regex From a List</h2>
      ''' + F('rxList', 'Pages, Keywords or Values', '/pricing/\n/contact-us/\n/thank-you.html', em='one per line', tag='textarea', mono=True, extra=' style="min-height:100px"') + '''
      ''' + F('rxHow', 'Match Type', 'exact', tag='select', opts=[('exact', 'Exactly one of these'), ('contains', 'Contains any of these'), ('starts', 'Starts with any of these')]) + '''
      <pre class="code-out" id="rxBuilt" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="rxCopy">Copy Regex</button><button class="btn" id="rxUse">Test This Regex</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var userCase = false;
  function run(){
    var mode = v('rxMode'), raw = $('rxRe').value.trim(), ci = $('rxCase').checked, iss = [];
    var cb = $('rxCase');
    if (mode === 'gsc'){ if (!cb.disabled) userCase = cb.checked; ci = true; cb.checked = true; cb.disabled = true; }
    else if (cb.disabled){ cb.disabled = false; cb.checked = userCase; ci = userCase; }
    var re = raw, m = re.match(/^\(\?(-?)i\)/);
    if (m){ ci = m[1] !== '-'; re = re.slice(m[0].length); if (mode !== 'gsc') iss.push(['warn', 'GA4 does not document the ' + c(m[0]) + ' flag. Use the Ignore case box or a pattern like ' + c('[Ss]eo') + ' instead.']); }
    if (/\(\?[=!]/.test(re)) iss.push(['bad', 'Lookaheads like ' + c('(?=') + ' and ' + c('(?!') + ' are not supported by RE2, the regex engine Google uses.']);
    if (/\(\?<[=!]/.test(re)) iss.push(['bad', 'Lookbehinds like ' + c('(?<=') + ' are not supported by RE2.']);
    if (/\\[1-9]/.test(re)) iss.push(['bad', 'Backreferences like ' + c('\\1') + ' are not supported by RE2.']);
    if (/\(\?>/.test(re)) iss.push(['bad', 'Atomic groups ' + c('(?>') + ' are not supported by RE2.']);
    if (/\(\?[a-z\-]*i[a-z\-]*\)/i.test(re)) iss.push(['warn', 'Inline flags in the middle of a regex cannot be tested here.']);
    if (/^\s|\s$/.test(raw)) iss.push(['warn', 'Your regex starts or ends with a space, which must also be in the value to match.']);
    if (/\|\||^\||\|$|\(\|/.test(re)) iss.push(['warn', 'There is an empty alternative such as ' + c('||') + '. It matches empty text and can match everything in partial mode.']);
    if (mode === 'ga4full' && /^\^/.test(re) && /\$$/.test(re)) iss.push(['warn', 'In full match mode ' + c('^') + ' and ' + c('$') + ' are not needed, though they do no harm.']);
    if (mode !== 'ga4full' && /\.\*$/.test(re)) iss.push(['warn', 'A trailing ' + c('.*') + ' is not needed in partial match mode.']);
    $('rxL').textContent = raw.length;
    var rx = null;
    try { rx = new RegExp(mode === 'ga4full' ? '^(?:' + re + ')$' : re, ci ? 'i' : ''); }
    catch(e){ iss.push(['bad', 'This is not a valid regex: ' + esc(e.message.replace(/^Invalid regular expression: /, '')) + '.']); }
    var vals = String($('rxTest').value).split('\n').filter(function(s){ return s !== ''; }), mc = 0;
    var rows = vals.map(function(s){
      if (!rx) return '<tr><td class="mono">' + esc(s) + '</td><td>…</td></tr>';
      var r = rx.exec(s), ok = !!r;
      if (ok) mc++;
      var shown = esc(s);
      if (ok && mode !== 'ga4full' && r[0] !== '') shown = esc(s.slice(0, r.index)) + '<mark style="background:#d8f3c1">' + esc(r[0]) + '</mark>' + esc(s.slice(r.index + r[0].length));
      return '<tr' + (ok ? ' class="hit"' : '') + '><td class="mono" style="word-break:break-all">' + shown + '</td><td>' + (ok ? 'Match' : 'No match') + '</td></tr>';
    });
    $('rxM').textContent = rx ? mc : '…'; $('rxN').textContent = rx ? vals.length - mc : '…';
    $('rxTable').innerHTML = '<thead><tr><th>Value</th><th>Result</th></tr></thead><tbody>' + rows.join('') + '</tbody>';
    var label = {ga4full: 'GA4 matches regex', ga4part: 'GA4 partially matches regex', gsc: 'Search Console'}[mode];
    issues('rxCheck', iss, '<strong>' + mc + ' of ' + vals.length + ' values match</strong> using ' + label + (ci ? ', ignoring case.' : ', case sensitive.'));
    build();
  }
  function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function build(){
    var items = lines('rxList'), how = v('rxHow'), out = '';
    items = items.filter(function(s, i){ return items.indexOf(s) === i; });
    if (items.length){
      var alt = items.map(escRe).join('|'), g = items.length > 1 ? '(' + alt + ')' : alt;
      out = how === 'exact' ? '^' + g + '$' : how === 'starts' ? '^' + g : alt;
    }
    $('rxBuilt').textContent = out || 'Add some values above.';
  }
  $('rxForm').addEventListener('input', run); $('rxForm').addEventListener('change', run);
  $('rxCopy').onclick = function(){ var t = $('rxBuilt').textContent; if (lines('rxList').length) copyText(t, 'toast'); };
  $('rxUse').onclick = function(){
    if (!lines('rxList').length) return;
    $('rxRe').value = $('rxBuilt').textContent; $('rxMode').value = v('rxHow') === 'exact' ? 'ga4full' : 'ga4part';
    $('rxTest').value = lines('rxList').join('\n') + '\n/some/other/page/'; run(); $('rxRe').scrollIntoView({behavior: 'smooth', block: 'center'});
  };
  run();
''',
        content='''
    <h2>Why Use a Regex Tester for GA4?</h2>
    <p>Regular expressions let you filter many pages, campaigns or search queries with one rule. They power GA4 report filters, audiences, custom channel groups and the Search Console performance report. The catch is that each tool reads them a little differently, and a regex that works in a code editor can quietly fail in Google's tools.</p>
    <p>This tester copies Google's behaviour. GA4 <strong>matches regex</strong> is a full match and case sensitive by default, as explained in Google's <a href="''' + GAH + '''1034324" target="_blank" rel="noopener">regular expressions help page</a>. Search Console uses RE2, matches anywhere in the text and ignores case unless you start with <code>(?-i)</code>, according to its <a href="https://support.google.com/webmasters/answer/17011165" target="_blank" rel="noopener">filtering documentation</a>.</p>

    <h2>How to Use the Tester</h2>
    <ol>
      <li><strong>Choose where the regex will be used</strong>: GA4 full match, GA4 partial match, or Search Console.</li>
      <li><strong>Type your regex</strong> and paste the values you want to check, one per line. Real page paths or queries from a report work best.</li>
      <li><strong>Read the results.</strong> Matching rows are highlighted, and in partial mode the matching part is marked.</li>
      <li><strong>Fix any warnings</strong>, such as lookaheads that Google's RE2 engine does not support.</li>
      <li><strong>Use the list builder</strong> to turn a plain list of pages or keywords into a safe, escaped regex.</li>
    </ol>

    <h2>Regex Cheat Sheet for Analytics</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Pattern', 'Meaning', 'Example') + '''
      <tbody>
        <tr><td><code>|</code></td><td>Or</td><td><code>seo|ppc</code></td></tr>
        <tr><td><code>.*</code></td><td>Anything, any length</td><td><code>/blog/.*</code></td></tr>
        <tr><td><code>^</code> and <code>$</code></td><td>Start and end of the value</td><td><code>^/blog/$</code></td></tr>
        <tr><td><code>( )</code></td><td>Group options together</td><td><code>/(en|hi)/pricing/</code></td></tr>
        <tr><td><code>\\.</code></td><td>A real dot, not any character</td><td><code>thank\\.html</code></td></tr>
        <tr><td><code>[0-9]+</code></td><td>One or more digits</td><td><code>/p/[0-9]+</code></td></tr>
        <tr><td><code>?</code></td><td>The item before it is optional</td><td><code>colou?r</code></td></tr>
        <tr><td><code>(?i)</code></td><td>Ignore case (Search Console style)</td><td><code>(?i)brandella</code></td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Google Regex Filters</h2>
    <ul>
      <li><strong>Mind full match in GA4.</strong> With matches regex, <code>/blog/</code> only matches that exact page. Add <code>.*</code> or switch to partially matches regex to catch every blog post.</li>
      <li><strong>Escape dots and question marks</strong> in URLs. The list builder does this for you.</li>
      <li><strong>Avoid lookaheads.</strong> RE2 has no lookarounds or backreferences. Use the does not match option instead.</li>
      <li><strong>Watch capitals.</strong> GA4 is case sensitive, so <code>/Blog/</code> and <code>/blog/</code> are different values.</li>
    </ul>

    <h2>Put Your Regex to Work</h2>
    <p>Use regex to separate brand searches with the <a href="''' + B + '''branded-queries-filter-in-search-console/">branded queries filter in Search Console</a>, dig into the <a href="''' + B + '''search-console-performance-report/">Search Console performance report</a>, and clean data as shown in <a href="''' + B + '''how-to-detect-filter-bot-traffic-ga4/">how to detect and filter bot traffic in GA4</a>. Want clean campaign values to filter on? Build them with the <a href="''' + A + '''utm-builder/">UTM builder</a>.</p>
''',
        faqs=[
            ("What regex syntax does GA4 use?", "Google Analytics and Search Console use Google's RE2 syntax. It supports the common patterns like |, .*, ^, $, groups and character classes, but not lookaheads, lookbehinds or backreferences."),
            ("What is the difference between matches regex and partially matches regex in GA4?", "Matches regex must match the whole value. Partially matches regex passes if any part of the value matches. For example, seo fully matches only the value seo, but partially matches /blog/seo/tips/."),
            ("Is Search Console regex case sensitive?", "No. Search Console regex ignores case by default. Start your expression with (?-i) to make it case sensitive."),
            ("Is my data sent anywhere?", "No. All testing runs in your browser and nothing you paste is uploaded."),
        ],
        related=[("Branded Queries Filter in Search Console", "branded-queries-filter-in-search-console"), ("Search Console Performance Report", "search-console-performance-report"),
                 ("Detect and Filter Bot Traffic in GA4", "how-to-detect-filter-bot-traffic-ga4"), ("Python and Pandas SEO Reporting", "python-and-pandas-seo-reporting")],
    ))

    # ---------- 7. A/B TEST SAMPLE SIZE CALCULATOR ----------
    TOOLS.append(dict(
        slug='ab-test-sample-size-calculator', short='AB', name='A/B Test Sample Size Calculator',
        card='Find how many visitors and how many days your A/B test needs before you can trust the result.',
        title='A/B Test Sample Size Calculator and Test Duration',
        desc='Free A/B test sample size calculator. Enter your conversion rate and the lift you want to detect to get visitors per variant and how many days to run the test.',
        h1='A/B Test Sample Size Calculator',
        lead='Enter your current conversion rate and the smallest improvement worth finding. See how many visitors each version needs and how long the test must run before the result means something.',
        tool='''<section class="tool" aria-label="A/B test sample size calculator" id="abForm">
    <div class="card" style="min-width:0">
      <h2>Your Test</h2>
      ''' + R2(F('abBase', 'Current Conversion Rate', '3', em='%', extra=' inputmode="decimal"'), F('abMde', 'Smallest Lift to Detect', '15', em='minimum detectable effect', extra=' inputmode="decimal"')) + '''
      ''' + F('abType', 'Lift Is', 'rel', tag='select', opts=[('rel', 'Relative, % of the current rate'), ('abs', 'Absolute, percentage points')]) + '''
      ''' + R2(F('abSig', 'Significance Level', '95', tag='select', opts=[('90', '90%'), ('95', '95% (standard)'), ('99', '99%')]),
               F('abPow', 'Statistical Power', '80', tag='select', opts=[('80', '80% (standard)'), ('90', '90%')])) + '''
      ''' + R2(F('abVar', 'Number of Versions', '2', tag='select', opts=[('2', '2 (A and B)'), ('3', '3'), ('4', '4'), ('5', '5')]),
               F('abDaily', 'Daily Visitors to the Page', '4000', extra=' inputmode="numeric"')) + '''
      ''' + F('abShare', 'Share of Traffic in the Test', '100', em='%', extra=' inputmode="decimal"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Sample Size Needed</h2>
      <div class="stats">''' + S('abPer', 'Visitors per Version') + S('abTot', 'Total Visitors') + S('abDays', 'Days to Run') + S('abConv', 'Conversions per Version') + '''</div>
      <div class="kw-result" id="abCheck"></div>
      <div class="actions"><button class="btn dark" id="abCopy">Copy Results</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Good to know</strong><ul><li>Decide the sample size before the test starts and do not stop early</li><li>Run for whole weeks so weekday and weekend visitors are both counted</li></ul></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Sample Size for Other Lifts</h2>
      <div style="overflow-x:auto"><table class="rtable" id="abTable"></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function n(id){ var s = v(id).replace(/[,\s%]/g, ''); return /^\d*\.?\d+$/.test(s) ? parseFloat(s) : NaN; }
  function fmt(x){ return isFinite(x) ? new Intl.NumberFormat('en-IN').format(Math.round(x)) : '…'; }
  function zq(p){
    var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.3577518672690, -30.66479806614716, 2.506628277459239],
        b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572],
        cc = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783],
        d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416], q, r;
    if (p < 0.02425){ q = Math.sqrt(-2 * Math.log(p)); return (((((cc[0]*q+cc[1])*q+cc[2])*q+cc[3])*q+cc[4])*q+cc[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1); }
    if (p > 1 - 0.02425){ q = Math.sqrt(-2 * Math.log(1 - p)); return -(((((cc[0]*q+cc[1])*q+cc[2])*q+cc[3])*q+cc[4])*q+cc[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1); }
    q = p - 0.5; r = q * q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);
  }
  function size(p1, p2, alpha, power){
    var za = zq(1 - alpha / 2), zb = zq(power), pb = (p1 + p2) / 2;
    var x = za * Math.sqrt(2 * pb * (1 - pb)) + zb * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2));
    return Math.ceil(x * x / ((p2 - p1) * (p2 - p1)));
  }
  var res = '';
  function run(){
    var base = n('abBase'), mde = n('abMde'), type = v('abType'), sig = +v('abSig'), pow = +v('abPow'), k = +v('abVar'), daily = n('abDaily'), share = n('abShare');
    if (!isFinite(share)) share = 100;
    var alpha = 1 - sig / 100, p1 = base / 100, p2 = type === 'rel' ? p1 * (1 + mde / 100) : p1 + mde / 100;
    var ids = ['abPer','abTot','abDays','abConv'];
    if (!(base > 0 && base < 100)){ ids.forEach(function(i){ $(i).textContent = '…'; }); say('abCheck', 'bad', 'Enter your current conversion rate as a percent between 0 and 100, for example 3.'); $('abTable').innerHTML = ''; return; }
    if (!(mde > 0)){ ids.forEach(function(i){ $(i).textContent = '…'; }); say('abCheck', 'bad', 'Enter the smallest lift you want to detect, for example 10 for a 10% relative lift.'); $('abTable').innerHTML = ''; return; }
    if (!(p2 < 1)){ ids.forEach(function(i){ $(i).textContent = '…'; }); say('abCheck', 'bad', 'That lift would push the conversion rate to 100% or more. Use a smaller lift.'); $('abTable').innerHTML = ''; return; }
    if (!(share > 0 && share <= 100)){ ids.forEach(function(i){ $(i).textContent = '…'; }); say('abCheck', 'bad', 'Share of traffic must be between 1 and 100.'); return; }
    var per = size(p1, p2, alpha, pow / 100), tot = per * k, perDay = daily > 0 ? daily * share / 100 : NaN, days = Math.ceil(tot / perDay);
    $('abPer').textContent = fmt(per); $('abTot').textContent = fmt(tot); $('abDays').textContent = isFinite(days) ? fmt(days) : 'Add traffic'; $('abConv').textContent = fmt(per * p1);
    var h = 'To spot a change from <strong>' + (+(p1 * 100).toFixed(3)) + '%</strong> to <strong>' + (+(p2 * 100).toFixed(3)) + '%</strong> with ' + sig + '% significance and ' + pow + '% power, each version needs <strong>' + fmt(per) + ' visitors</strong>.';
    var cls = 'ok';
    if (isFinite(days)){
      var wk = Math.ceil(days / 7);
      h += ' At ' + fmt(perDay) + ' visitors a day in the test, that takes about <strong>' + fmt(days) + ' days</strong>. Round up to ' + wk + ' full week' + (wk > 1 ? 's' : '') + '.';
      if (days > 56){ cls = 'warn'; h += ' That is a long test. Consider testing a bolder change, a page with more traffic, or a step closer to the conversion.'; }
      else if (days < 7){ h += ' Even if you reach the sample sooner, run it for at least one full week.'; }
    }
    if (k > 2) h += ' With ' + k + ' versions, each one is compared with the control, so the chance of a false winner rises. Treat close results with care.';
    say('abCheck', cls, h);
    res = ['Current conversion rate: ' + base + '%', 'Lift to detect: ' + mde + (type === 'rel' ? '% relative' : ' points absolute'), 'Visitors per version: ' + fmt(per), 'Total visitors: ' + fmt(tot), 'Days to run: ' + (isFinite(days) ? fmt(days) : 'n/a')].join('\n');
    var lifts = type === 'rel' ? [5, 10, 15, 20, 25, 30, 40, 50] : [0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 3];
    $('abTable').innerHTML = '<thead><tr><th>Lift</th><th class="num">New Rate</th><th class="num">Per Version</th><th class="num">Total</th><th class="num">Days</th></tr></thead><tbody>' +
      lifts.map(function(L){
        var q = type === 'rel' ? p1 * (1 + L / 100) : p1 + L / 100; if (q >= 1) return '';
        var s = size(p1, q, alpha, pow / 100), t = s * k, dd = Math.ceil(t / perDay);
        return '<tr' + (L === mde ? ' class="hit"' : '') + '><td>' + L + (type === 'rel' ? '%' : ' pts') + '</td><td class="num">' + (+(q * 100).toFixed(3)) + '%</td><td class="num">' + fmt(s) + '</td><td class="num">' + fmt(t) + '</td><td class="num">' + (isFinite(dd) ? fmt(dd) : '…') + '</td></tr>';
      }).join('') + '</tbody>';
  }
  $('abForm').addEventListener('input', run); $('abForm').addEventListener('change', run);
  $('abCopy').onclick = function(){ if (res) copyText(res, 'toast'); };
  run();
''',
        content='''
    <h2>What Is an A/B Test Sample Size Calculator?</h2>
    <p>An A/B test shows two versions of a page, ad or email to different visitors and compares how many convert. The hard part is knowing when to stop. Stop too early and a lucky streak looks like a winner. This calculator tells you how many visitors each version needs before the difference you see is likely to be real.</p>
    <p>It uses the standard sample size formula for comparing two conversion rates with a two sided test. You choose the significance level, which controls false winners, and the power, which controls how often a real improvement is caught.</p>

    <h2>How to Use the Calculator</h2>
    <ol>
      <li><strong>Enter your current conversion rate</strong> from GA4 or your testing tool, for the exact page and goal you will test.</li>
      <li><strong>Set the smallest lift worth finding.</strong> A 15% relative lift on a 3% rate means detecting a move to 3.45%.</li>
      <li><strong>Keep 95% significance and 80% power</strong> unless you have a reason to change them. These are the common defaults.</li>
      <li><strong>Add your daily visitors</strong> and the share of traffic in the test to see how many days the test needs.</li>
      <li><strong>Check the table</strong> to see how much faster a test finishes when you aim for a bigger lift.</li>
    </ol>

    <h2>What Each Setting Means</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Setting', 'What it controls', 'Typical value') + '''
      <tbody>
        <tr><td>Baseline conversion rate</td><td>How often visitors convert today</td><td>From your reports</td></tr>
        <tr><td>Minimum detectable effect</td><td>The smallest change the test can reliably find</td><td>10% to 20% relative</td></tr>
        <tr><td>Significance level</td><td>How sure you want to be that a winner is not luck</td><td>95%</td></tr>
        <tr><td>Statistical power</td><td>The chance of catching a real improvement of that size</td><td>80%</td></tr>
        <tr><td>Number of versions</td><td>Each extra version needs its own full sample</td><td>2</td></tr>
      </tbody>
    </table></div>
    <p>The formula is n = (z<sub>α/2</sub> × √(2p̄(1 − p̄)) + z<sub>β</sub> × √(p₁(1 − p₁) + p₂(1 − p₂)))² ÷ (p₂ − p₁)², where p₁ is the current rate, p₂ the rate you want to detect, and p̄ their average.</p>

    <h2>Tips for Trustworthy A/B Tests</h2>
    <ul>
      <li><strong>Fix the sample size first.</strong> Checking results every day and stopping when one version leads is the most common way to get a false winner.</li>
      <li><strong>Run whole weeks.</strong> People behave differently on weekends, so cover at least one full week, ideally two.</li>
      <li><strong>Test bold changes on small sites.</strong> Low traffic pages can only detect big lifts in a sensible time.</li>
      <li><strong>Track one main goal.</strong> Pick the conversion you care about before you start and judge the test on that.</li>
    </ul>

    <h2>Keep Improving</h2>
    <p>Find ideas worth testing in our guide to <a href="''' + B + '''conversion-rate-optimization/">conversion rate optimization</a>, apply the same thinking to ads with <a href="''' + B + '''ppc-ad-copy-testing/">PPC ad copy testing</a>, and make sure your goal is tracked correctly using <a href="''' + B + '''ga4-events-vs-conversions-difference/">GA4 events vs conversions</a>. Testing ad clickthrough rates instead? The <a href="https://brandella.in/tools/ppc-calculators/ctr-calculator/">CTR calculator</a> checks whether one ad really beats another, and you can track each version cleanly with the <a href="''' + A + '''utm-builder/">UTM builder</a>.</p>
''',
        faqs=[
            ("How many visitors do I need for an A/B test?", "It depends on your conversion rate and the lift you want to detect. A page converting at 3% needs about 24,000 visitors per version to detect a 15% relative lift at 95% significance and 80% power. Bigger lifts and higher conversion rates need far fewer."),
            ("What is a minimum detectable effect?", "It is the smallest improvement your test can reliably find. If the real lift is smaller than this, the test will usually end without a clear winner. Smaller effects need much larger samples."),
            ("Can I stop the test once it reaches significance?", "Not safely. Significance moves up and down as data comes in, so stopping at the first good reading inflates false winners. Decide the sample size up front and let the test reach it."),
            ("Is my data stored?", "No. The calculator runs entirely in your browser and nothing you enter is sent anywhere."),
        ],
        related=[("Conversion Rate Optimization", "conversion-rate-optimization"), ("PPC Ad Copy Testing", "ppc-ad-copy-testing"),
                 ("GA4 Events vs Conversions", "ga4-events-vs-conversions-difference"), ("Customer Journey Mapping", "customer-journey-mapping-digital-marketing")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'analytics-tools'; t['updated'] = '2026-11-02'
