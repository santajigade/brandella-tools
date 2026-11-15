"""Batch 18 (2026-11-15): Content Writing Tools category, first tool (Headline Analyzer).
Facts checked 2026-11-15 against: Google Search Central, Influencing your title links
(developers.google.com/search/docs/appearance/title-link): no limit on <title> length, but title links are truncated
to fit the device width; Google may use the first visible <h1> as the title link; avoid keyword stuffing ("no reason
to have the same words or phrases appear multiple times") and boilerplate. Google, Creating helpful, reliable,
people first content (developers.google.com/search/docs/fundamentals/creating-helpful-content): "Does the main heading
or page title provide a descriptive, helpful summary of the content?" and "avoid exaggerating or being shocking in
nature?". Google Discover docs: avoid clickbait, misleading or exaggerated details in preview content and withholding
crucial information; avoid sensationalism. The 600 px desktop title width (20px Arial) matches the existing SERP
Snippet Preview tool and is labelled as approximate. Word balance targets (common, uncommon, emotional, power) are
editorial guidelines, labelled as such, not Google rules.
Search demand: "headline analyzer" is served by CoSchedule (now Headline Studio, account needed), AIOSEO, WPBeginner,
MonsterInsights, LanderLab, RightBlogger, ryrob and others. This one adds a Google title width check, clickbait checks
based on Google's own guidance, focus keyword checks and a ranked comparison of up to 20 headlines, with no signup."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
SEO = 'https://brandella.in/tools/seo-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

HL_LIST = ('11 Proven Ways to Write Headlines People Love to Click\n'
           "You Won't Believe These SHOCKING Headline Tricks!!!\n"
           'Headlines\n'
           'Why Your Blog Posts Get No Clicks and How to Fix It Today\n'
           'Some Things You Should Know About Writing Good Headlines\n'
           'The Complete Beginner Guide to Writing Headlines for SEO, Social Media, Email Newsletters and AI Search Answers')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='headline-analyzer', short='HA', name='Headline Analyzer',
        card='Score any blog headline or title for length, word balance, power and emotional words, clickbait and Google cut off, then rank several ideas.',
        title='Headline Analyzer: Free Headline Score and Checker',
        desc='Free headline analyzer. Score your blog title for length, power and emotional words, clickbait and Google cut off, check your keyword and rank 20 ideas.',
        h1='Headline Analyzer',
        lead='Type a headline to get an instant score out of 100 with clear fixes. See its word balance, where Google will cut it off, whether it reads like clickbait, and paste a list of ideas to pick the strongest one before you publish.',
        tool='''<section class="tool" aria-label="Headline analyzer">
    <div class="card" style="min-width:0">
      <h2>Your Headline</h2>
      ''' + F('haIn', 'Headline or title', 'How to Write Headlines People Love to Click (Without Clickbait)', em='a blog title, page title, video title or post headline') + '''
      ''' + F('haKw', 'Focus keyword', 'write headlines', em='optional, the phrase you want to rank for') + '''
      <div class="stats">''' + S('haScore', 'Score out of 100') + S('haWords', 'Words') + S('haChars', 'Characters') + S('haPx', 'Pixels of 600') + '''</div>
      <div class="kw-result" id="haVerdict"></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="haCopy">Copy Headline</button><button class="btn" id="haRep">Copy Report</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Word Balance</h2>
      <div id="haBal"></div>
      <p style="font-size:13px;color:#666;margin:6px 0 14px">Targets are editorial guidelines from headline research, not fixed rules. A strong headline mixes plain words with a few specific, vivid ones.</p>
      <h2 style="margin-top:4px">How It Looks</h2>
      <p style="font-size:13px;color:#666;margin:0 0 6px">Google desktop result, approximate cut off at 600 pixels</p>
      <div style="border:1px solid #ddd;border-radius:10px;padding:12px 14px;background:#fff;font-family:Arial,sans-serif;margin-bottom:14px"><div style="font-size:12px;color:#4d5156">yourblog.com</div><div id="haSerp" style="font-size:20px;line-height:1.3;color:#1a0dab;overflow-wrap:anywhere"></div></div>
      <p style="font-size:13px;color:#666;margin:0 0 6px">What a skimming reader takes in: the first and last three words</p>
      <div class="chips" id="haSkim"></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Checks</h2>
      <div style="overflow-x:auto"><table class="rtable" id="haChecks"></table></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Compare Headlines</h2>
      ''' + F('haList', 'One headline per line, up to 20', HL_LIST, tag='textarea', extra=' style="min-height:150px"') + '''
      <div class="kw-result" id="haLCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="haLOut"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="haLCopy">Copy Ranking as CSV</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function set(s){ var o = {}; s.split(' ').forEach(function(w){ if (w) o[w] = 1; }); return o; }
  var COMMON = set('a about above after again all also am an and any are as at be because been before being between both but by can come could day did do does doing down during each even every few first for from get gets getting give go going good got had has have having he her here him his how i if in into is it its just know like look make makes many me more most much my need needs new no nor not now of off on once one only or other our out over own people really right same say see she should so some such take than that the their them then there these they thing think this those through time to too two under until up us use used using very want was way ways we well were what when where which while who whom why will with without work would year years you your yours');
  var POWER = set('best proven ultimate complete essential secret secrets guaranteed effortless effortlessly powerful remarkable effective easy easily simple simply quick quickly fast faster instant instantly smart smarter stop never always today finally exclusive insider expert experts hidden boost double triple save grow win master unlock discover reveal revealed critical crucial vital must worst warning dangerous mistake mistakes avoid lazy beginner beginners hack hacks trick tricks truth honest actually free bonus breakthrough fix stunning brilliant genius definitive practical surprising unusual rare limited urgent new step steps checklist template blueprint formula framework strategy strategies results instant massive tiny little known overlooked underrated forgotten myth myths');
  var POS = set('love loved loves happy happier happiest joy joyful hope hopeful dream dreams proud confident inspiring inspired heartwarming beautiful delightful exciting thrilling calm peaceful brave bold success successful win wins winning rich wealthy healthy trust amazing awesome wonderful fantastic incredible perfect better best easy fun favorite favourite glad grateful lucky relief relaxed safe smart strong');
  var NEG = set('hate hated fear afraid sad angry anger worry worried stress stressed struggle struggling pain painful embarrassing awkward scary terrifying regret lonely frustrating frustrated annoying guilty shame ashamed failure fail failing broke lose losing lost miss missing ugly worst wrong bad terrible horrible awful dangerous danger warning mistake mistakes problem problems crisis disaster panic hurt killing waste wasted wasting ruin ruined trap toxic myth myths lies');
  var EMOX = set('crazy wild surprising surprised secret secrets dare desire curious curiosity heart soul obsessed jealous furious nervous excited thrill');
  var VAGUE = set('things thing stuff very really various certain basically literally nice somehow');
  var CLICK = [/you\s+(won'?t|will\s+not|wont)\s+believe/i, /(blow|blew)\s+your\s+mind/i, /mind\s*blowing/i, /what\s+happen(s|ed)\s+next/i, /this\s+one\s+(weird\s+|simple\s+)?trick/i, /(doctors|experts)\s+hate/i, /\bshocking\b/i, /jaw\s*dropping/i, /gone\s+wrong/i, /you\s+(need|have)\s+to\s+see/i, /number\s+\d+\s+will/i, /\binsane\b/i, /\bomg\b/i, /\bmust\s+see\b/i, /\bnobody\s+(is\s+)?talking\s+about\b/i, /\bwill\s+shock\s+you\b/i];
  var VERBS = set('get stop make start use try learn build write boost grow avoid fix create find turn discover master improve increase double save plan choose read watch join meet');
  var ACR = {AI:1,SEO:1,GST:1,ROI:1,USA:1,UK:1,PDF:1,FAQ:1,CEO:1,B2B:1,B2C:1,GA4:1,API:1,UPI:1,PPC:1,CRM:1,SMS:1,HTML:1,CSS:1,URL:1,GPT:1,LLM:1,AEO:1,GEO:1,SERP:1,CTR:1,KPI:1,SaaS:1,DIY:1,FAQS:1,UX:1,UI:1,IT:1,HR:1,TV:1,PR:1,USB:1,NASA:1};
  function stem(w, S){ if (S[w]) return true; if (/s$/.test(w) && S[w.slice(0, -1)]) return true; if (/es$/.test(w) && S[w.slice(0, -2)]) return true; return false; }
  function words(s){ return (s.match(/[\p{L}\p{N}][\p{L}\p{N}'’]*/gu) || []); }
  var cv = document.createElement('canvas').getContext('2d');
  function px(t){ cv.font = '20px Arial'; return Math.round(cv.measureText(t).width); }
  function serpCut(t){
    if (px(t) <= 600) return {text: t, cut: false};
    var w = t.split(/\s+/), out = '';
    for (var i = 0; i < w.length; i++){ var nx = out ? out + ' ' + w[i] : w[i]; if (px(nx + ' ...') > 600) break; out = nx; }
    if (!out){ out = t; while (out.length && px(out + '...') > 600) out = out.slice(0, -1); return {text: out + '...', cut: true}; }
    return {text: out + ' ...', cut: true};
  }
  function htype(s, ws){
    var l = s.trim().toLowerCase(), f = (ws[0] || '').toLowerCase();
    if (/^\d+\s/.test(l) || /\b\d+\s+(ways|tips|reasons|ideas|examples|things|steps|mistakes|tools|lessons|facts|questions|rules|signs|secrets|hacks|tricks|strategies|places|books|apps)\b/.test(l)) return 'List';
    if (/^how\s+(to|i|we|you|a|an|the|this|my|our)\b/.test(l)) return 'How to';
    if (/\?\s*$/.test(l) || /^(what|when|where|who|which|can|should|is|are|do|does|will|would|could|did|has|have)\b/.test(l)) return 'Question';
    if (/^why\b/.test(l)) return 'Why explainer';
    if (/\bvs\.?\b|\bversus\b/.test(l)) return 'Comparison';
    if (/\b(guide|tutorial|explained|handbook|introduction)\b/.test(l)) return 'Guide';
    if (/\breview(s|ed)?\b/.test(l)) return 'Review';
    if (VERBS[f]) return 'Command';
    return 'General';
  }
  function analyse(s, kw){
    s = (s || '').replace(/\s+/g, ' ').trim(); kw = (kw || '').replace(/\s+/g, ' ').trim().toLowerCase();
    if (!s) return {score: 0, words: 0, chars: 0, px: 0, type: '', checks: [['bad', 'Headline', 'Type a headline to analyze it.']], bal: null};
    var ws = words(s), lw = ws.map(function(w){ return w.toLowerCase().replace(/['’]s$/, '').replace(/’/g, "'"); }), n = ws.length;
    var cm = 0, pw = [], em = [], pos = 0, neg = 0;
    lw.forEach(function(w){
      var isP = stem(w, POWER), isE = stem(w, POS) || stem(w, NEG) || stem(w, EMOX);
      if (stem(w, POS)) pos++; if (stem(w, NEG)) neg++;
      if (isP) pw.push(w); if (isE) em.push(w);
      if (!isP && !isE && stem(w, COMMON)) cm++;
    });
    var unc = lw.filter(function(w){ return !stem(w, COMMON) && !stem(w, POWER) && !stem(w, POS) && !stem(w, NEG) && !stem(w, EMOX); }).length;
    var pct = function(x){ return n ? Math.round(x * 100 / n) : 0; };
    var bal = {common: pct(cm), uncommon: pct(unc), emotional: pct(em.length), power: pw.length};
    var pts = 100, C = [];
    function add(st, name, note, minus){ C.push([st, name, note]); pts -= (minus || 0); }
    var chars = Array.from(s).length, width = px(s), type = htype(s, ws);
    if (n < 4) add('bad', 'Length', n + ' word' + (n === 1 ? '' : 's') + ' is too short to tell readers what they get. Most strong headlines use 6 to 13 words.', 40);
    else if (n < 6) add('warn', 'Length', n + ' words. Short can work, but add a detail such as who it is for or what they will get.', 8);
    else if (n <= 13) add('ok', 'Length', n + ' words, a strong length that is easy to scan.');
    else if (n <= 16) add('warn', 'Length', n + ' words is getting long. Cut words that do not add meaning.', 6);
    else add('bad', 'Length', n + ' words is too long. Readers and search results will lose the end. Aim for 6 to 13.', 20);
    if (width > 600) add('warn', 'Google title width', 'About ' + width + ' pixels, wider than the roughly 600 pixels Google shows on desktop, so the end will be cut. Fine for an on page heading, but shorten the title tag.', 8);
    else add('ok', 'Google title width', 'About ' + width + ' pixels, so it should show in full in Google on desktop.');
    if (bal.common < 15 && n >= 4) add('warn', 'Common words', bal.common + '% common words. Headlines with almost no plain words can read stiff. Aim for about 20 to 30%.', 4);
    else if (bal.common > 60) add('warn', 'Common words', bal.common + '% common words. It reads flat. Swap a few plain words for specific ones.', 10);
    else add('ok', 'Common words', bal.common + '% common words, which keeps it easy to read.');
    if (n >= 4 && bal.uncommon < 10) add('warn', 'Uncommon words', bal.uncommon + '% uncommon words. Add a specific word, such as a topic, a tool or a result, so it stands out.', 6);
    else add('ok', 'Uncommon words', bal.uncommon + '% uncommon words, which makes it specific.');
    if (!em.length) add('warn', 'Emotional words', 'None found. One word that names a feeling, such as love, fear, proud or struggle, makes people care.', 6);
    else if (bal.emotional > 30) add('warn', 'Emotional words', bal.emotional + '% emotional words (' + em.map(c).join(', ') + '). That much can feel like hype. Keep one or two.', 4);
    else add('ok', 'Emotional words', em.map(c).join(', ') + '. A good touch of feeling.');
    if (!pw.length) add('warn', 'Power words', 'None found. A word like proven, simple, mistakes or checklist promises a clear payoff.', 8);
    else if (pw.length > 3) add('warn', 'Power words', pw.length + ' power words (' + pw.map(c).join(', ') + '). Stacking them sounds salesy. Keep the strongest one or two.', 5);
    else add('ok', 'Power words', pw.map(c).join(', ') + '. These make the promise clear.');
    var cb = CLICK.filter(function(r){ return r.test(s); }).map(function(r){ return (s.match(r) || [''])[0]; });
    if (cb.length) add('bad', 'Clickbait', 'Phrases like ' + cb.map(c).join(', ') + ' read as clickbait. Google asks that titles avoid exaggerating or being shocking, and readers who feel tricked leave fast.', Math.min(40, cb.length * 25));
    else add('ok', 'Clickbait', 'No clickbait phrases found.');
    var letters = s.replace(/[^A-Za-z]/g, ''), caps = (s.match(/\b[A-Z][A-Z0-9]{2,}\b/g) || []).filter(function(w){ return !ACR[w]; });
    if (letters.length > 8 && letters === letters.toUpperCase()) add('bad', 'Capital letters', 'The whole headline is in capitals, which reads as shouting.', 18);
    else if (caps.length) add('warn', 'Capital letters', 'Shouting words: ' + caps.map(c).join(', ') + '. Use title case or sentence case instead.', Math.min(15, caps.length * 7));
    var ex = (s.match(/!/g) || []).length;
    if (/[!?]{2,}/.test(s)) add('bad', 'Punctuation', 'Repeated marks such as ' + c((s.match(/[!?]{2,}/) || [''])[0]) + ' look like spam. Use one at most.', 12);
    else if (ex) add('warn', 'Punctuation', 'Exclamation marks rarely help a headline. Let the words carry the energy.', 4);
    var vg = lw.filter(function(w){ return VAGUE[w]; });
    if (vg.length) add('warn', 'Vague words', vg.map(c).join(', ') + '. Replace with something concrete, such as a number, a name or a result.', Math.min(12, vg.length * 6));
    var rep = {}, dup = [];
    lw.forEach(function(w){ if (!stem(w, COMMON) && w.length > 2){ rep[w] = (rep[w] || 0) + 1; if (rep[w] === 2) dup.push(w); } });
    if (dup.length) add('warn', 'Repeated words', dup.map(c).join(', ') + ' appear more than once. Google advises against repeating the same words in a title.', 5);
    if (kw){
      var L = s.toLowerCase(), at = L.indexOf(kw), cnt = at < 0 ? 0 : L.split(kw).length - 1;
      if (at < 0){
        var kws = words(kw).map(function(w){ return w.toLowerCase(); }), hit = kws.filter(function(w){ return lw.indexOf(w) > -1 || lw.some(function(x){ return x.indexOf(w) === 0 || w.indexOf(x) === 0 && x.length > 3; }); });
        if (kws.length > 1 && hit.length === kws.length) add('warn', 'Focus keyword', 'All the words of ' + c(kw) + ' are there, but not as one phrase. Use the exact phrase if it still reads naturally.', 4);
        else add('bad', 'Focus keyword', c(kw) + ' is not in the headline. Add it so readers and search engines see the page matches what they searched.', 14);
      }
      else if (cnt > 1) add('warn', 'Focus keyword', c(kw) + ' appears ' + cnt + ' times. Once is enough, more looks like keyword stuffing.', 8);
      else if (at > L.length / 2) add('warn', 'Focus keyword', c(kw) + ' is in the second half. Move it closer to the start, where readers and search results notice it first.', 4);
      else add('ok', 'Focus keyword', c(kw) + ' appears once, near the start. Well placed.');
    }
    var yr = new Date().getFullYear(), ys = (s.match(/\b(19|20)\d{2}\b/g) || []).map(Number);
    var old = ys.filter(function(y){ return y >= 2010 && y < yr; });
    if (old.length) add('warn', 'Year', c(String(old[0])) + ' makes the headline look out of date. Update the year, and the content with it, or remove it.', 6);
    else if (ys.indexOf(yr) > -1) C.push(['info', 'Year', 'Includes ' + yr + ', which signals fresh content. Remember to update it next year.']);
    C.push(['info', 'Headline type', type + (type === 'General' ? '. Lists, how to guides and questions tend to set clearer expectations. Try one as an alternative.' : '. A clear format that tells readers what they will get.')]);
    if (/\d/.test(s)) C.push(['info', 'Numbers', 'Has a number, which makes the promise specific.']);
    if (/[\[(][^\])]+[\])]/.test(s)) C.push(['info', 'Brackets', 'Has a bracketed extra, such as a format or bonus, which can help it stand out.']);
    if (type === 'Question' || type === 'How to' || type === 'Comparison' || /^what\s+is\b/i.test(s)) C.push(['info', 'AI search fit', 'This mirrors how people ask search engines and AI assistants. Answer it clearly in the first paragraph so the answer is easy to quote.']);
    var sent = pos > neg ? 'Positive' : neg > pos ? 'Negative' : 'Neutral';
    C.push(['info', 'Sentiment', sent + (sent === 'Neutral' ? '. Fine for clear, factual headlines.' : sent === 'Negative' ? '. Warnings and mistakes can pull attention, but make sure the page offers a fix.' : '. Upbeat headlines tend to suit guides and how to content.')]);
    return {score: Math.max(0, Math.min(100, pts)), words: n, chars: chars, px: width, type: type, checks: C, bal: bal, ws: ws, sent: sent};
  }
  function grade(x){ return x >= 80 ? ['ok', 'Strong'] : x >= 60 ? ['ok', 'Good'] : x >= 40 ? ['warn', 'Needs work'] : ['bad', 'Weak']; }
  var ICON = {ok: '<span style="color:#2e7d32;font-weight:700">Good</span>', warn: '<span style="color:#b26a00;font-weight:700">Improve</span>', bad: '<span style="color:#c62828;font-weight:700">Fix</span>', info: '<span style="color:#555;font-weight:700">Note</span>'};
  function bar(label, val, shown, lo, hi, max, target){
    var ok = val >= lo && val <= hi, w = Math.min(100, Math.round(val * 100 / max));
    return '<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;font-size:14px"><strong>' + label + '</strong><span>' + shown + ' <em style="color:#777;font-style:normal">target ' + target + '</em></span></div>' +
      '<div style="height:9px;background:#eee;border-radius:6px;overflow:hidden"><div style="height:100%;width:' + w + '%;background:' + (ok ? '#6cbf2a' : '#e0a02a') + '"></div></div></div>';
  }
  var last = null;
  function run(){
    var s = $('haIn').value, r = analyse(s, $('haKw').value), gr = grade(r.score); last = r;
    $('haScore').textContent = r.score; $('haWords').textContent = r.words; $('haChars').textContent = r.chars; $('haPx').textContent = r.px;
    var fixes = r.checks.filter(function(x){ return x[0] === 'bad' || x[0] === 'warn'; }).length;
    say('haVerdict', gr[0], s.trim() ? '<strong>' + gr[1] + ' headline (' + r.score + ' of 100).</strong> ' + r.type + ' headline. ' + (fixes ? fixes + ' thing' + (fixes === 1 ? '' : 's') + ' to improve below.' : 'Nothing to fix. Compare it with one or two other ideas below.') : 'Type a headline to see its score.');
    $('haChecks').innerHTML = '<thead><tr><th style="width:90px">Result</th><th style="width:170px">Check</th><th>What it means</th></tr></thead><tbody>' + r.checks.map(function(x){ return '<tr><td>' + ICON[x[0]] + '</td><td><strong>' + esc(x[1]) + '</strong></td><td>' + x[2] + '</td></tr>'; }).join('') + '</tbody>';
    if (r.bal){
      var b = r.bal;
      $('haBal').innerHTML = bar('Common words', b.common, b.common + '%', 15, 60, 100, '20 to 30%') + bar('Uncommon words', b.uncommon, b.uncommon + '%', 10, 100, 100, '10 to 20%') + bar('Emotional words', b.emotional, b.emotional + '%', 1, 30, 100, '10 to 15%') + bar('Power words', b.power, b.power, 1, 3, 5, '1 or 2');
      var sc = serpCut(s.replace(/\s+/g, ' ').trim());
      $('haSerp').textContent = sc.text;
      var w = r.ws, first = w.slice(0, 3).join(' '), lastw = w.length > 3 ? w.slice(-3).join(' ') : '';
      $('haSkim').innerHTML = '<span class="chip">' + esc(first) + '</span>' + (lastw ? '<span class="chip">' + esc(lastw) + '</span>' : '');
    } else { $('haBal').innerHTML = ''; $('haSerp').textContent = ''; $('haSkim').innerHTML = ''; }
  }
  var ranked = [];
  function runList(){
    var lines = $('haList').value.split(/\n/).map(function(x){ return x.replace(/\s+/g, ' ').trim(); }).filter(Boolean), kw = $('haKw').value, extra = 0;
    if (lines.length > 20){ extra = lines.length - 20; lines = lines.slice(0, 20); }
    ranked = lines.map(function(l){ var r = analyse(l, kw); return {h: l, r: r, top: (r.checks.filter(function(x){ return x[0] === 'bad'; })[0] || r.checks.filter(function(x){ return x[0] === 'warn'; })[0] || ['ok', '', 'No issues found.'])}; })
      .sort(function(a, b){ return b.r.score - a.r.score; });
    if (!ranked.length){ say('haLCheck', '', 'Paste a few headline ideas, one per line, to rank them.'); $('haLOut').innerHTML = ''; return; }
    say('haLCheck', 'ok', '<strong>Best idea:</strong> ' + esc(ranked[0].h) + ' (' + ranked[0].r.score + ' of 100).' + (extra ? ' Only the first 20 lines were checked.' : ''));
    $('haLOut').innerHTML = '<thead><tr><th>#</th><th>Headline</th><th>Score</th><th>Type</th><th>Words</th><th>Main thing to fix</th></tr></thead><tbody>' + ranked.map(function(x, i){
      var t = x.top; return '<tr><td>' + (i + 1) + '</td><td>' + esc(x.h) + '</td><td><strong>' + x.r.score + '</strong></td><td>' + esc(x.r.type) + '</td><td>' + x.r.words + '</td><td>' + (t[1] ? '<strong>' + esc(t[1]) + ':</strong> ' : '') + t[2] + '</td></tr>'; }).join('') + '</tbody>';
  }
  function plain(h){ return String(h).replace(/<[^>]+>/g, ''); }
  function q(v){ v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  $('haIn').addEventListener('input', run);
  $('haKw').addEventListener('input', function(){ run(); runList(); });
  $('haList').addEventListener('input', runList);
  $('haCopy').onclick = function(){ var s = $('haIn').value.trim(); if (s) copyText(s, 'toast'); };
  $('haRep').onclick = function(){ if (!last || !last.words) return; copyText('Headline: ' + $('haIn').value.trim() + '\nScore: ' + last.score + ' of 100 (' + last.type + ')\n\n' + last.checks.map(function(x){ return x[0].toUpperCase() + ' ' + x[1] + ': ' + plain(x[2]); }).join('\n'), 'toast'); };
  $('haLCopy').onclick = function(){ if (!ranked.length) return; copyText('Rank,Headline,Score,Type,Words,Main thing to fix\n' + ranked.map(function(x, i){ return [i + 1, q(x.h), x.r.score, x.r.type, x.r.words, q(plain(x.top[2]))].join(','); }).join('\n'), 'toast'); };
  run(); runList();
''',
        content=f'''
    <h2>What Is a Headline Analyzer?</h2>
    <p>A headline analyzer reads your title the way a busy reader and a search engine would, then scores it. It checks length, the mix of plain and vivid words, whether it sounds like clickbait, and where Google will cut it off. You get a score out of 100 and a short list of fixes, so you can improve a headline in a minute instead of guessing.</p>
    <p>Your headline decides whether anyone reads the rest. It is the blue link in Google, the bold line on social media, and often the text an AI assistant shows when it cites your page. Google itself asks whether <q>the main heading or page title provide a descriptive, helpful summary of the content</q> in its guide to <a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" {EXT}>creating helpful content</a>.</p>

    <h2>How to Use the Headline Analyzer</h2>
    <ol>
      <li><strong>Type your headline</strong> in the first box. The score and checks update as you type.</li>
      <li><strong>Add your focus keyword</strong> if the page should rank for a phrase. The tool checks that it appears once, near the start.</li>
      <li><strong>Work through the checks.</strong> Fix anything marked Fix first, then the Improve items.</li>
      <li><strong>Look at the Google preview</strong> to see if the end of your title gets cut off.</li>
      <li><strong>Paste several ideas</strong> into Compare Headlines to rank them, then copy the ranking as a CSV for your team.</li>
    </ol>

    <h2>What the Score Checks</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Check', 'What a strong headline does')}
      <tbody>
        <tr><td>Length</td><td>Uses about 6 to 13 words. Long enough to make a clear promise, short enough to scan.</td></tr>
        <tr><td>Google title width</td><td>Fits in roughly 600 pixels, so the whole title shows on desktop. Google cuts longer titles to fit the screen.</td></tr>
        <tr><td>Word balance</td><td>Mixes common words for flow, uncommon words for detail, one emotional word and one or two power words.</td></tr>
        <tr><td>Clickbait</td><td>Promises only what the page delivers, without phrases like <q>you won't believe</q> or <q>shocking</q>.</td></tr>
        <tr><td>Focus keyword</td><td>Uses the search phrase once, close to the start, without repeating it.</td></tr>
        <tr><td>Caps and punctuation</td><td>Uses normal case and no repeated marks, so it never looks like spam.</td></tr>
        <tr><td>Type</td><td>Follows a clear format, such as a list, a how to, a question or a comparison.</td></tr>
      </tbody>
    </table></div>
    <p>The length and keyword rules follow Google's guide to <a href="https://developers.google.com/search/docs/appearance/title-link" {EXT}>title links</a>, which says titles are cut to fit the device width and that repeating the same words adds nothing. The word balance targets are editorial guidelines, not fixed rules.</p>

    <h2>Practical Tips for Better Headlines</h2>
    <ul>
      <li><strong>Write ten, keep one.</strong> Your first idea is rarely your best. Paste them all into the comparison and test the top two with real readers.</li>
      <li><strong>Be specific.</strong> <q>7 email mistakes that cost you sales</q> beats <q>some things about email</q>. Numbers, names and results build trust.</li>
      <li><strong>Lead with what matters.</strong> Readers and search results notice the first few words most, so put the topic there.</li>
      <li><strong>Match the search.</strong> Questions and how to headlines mirror what people type into Google and ask AI assistants. Answer the question in your first paragraph.</li>
      <li><strong>Keep the title tag and H1 close.</strong> Google may use your main heading as the title link, so make both describe the same page.</li>
    </ul>

    <h2>Keep Improving Your Content</h2>
    <p>A strong headline works best on a strong page. Read our guide to <a href="{B}title-tag-optimization/">title tag optimization</a>, avoid the traps in <a href="{B}25-content-writing-mistakes/">25 content writing mistakes</a>, and learn <a href="{B}ai-overviews-clicks-how-to-get-cited-2026/">how to get cited in AI Overviews</a>. When your headline is ready, see the full search result with the <a href="{SEO}serp-snippet-preview/">SERP snippet preview</a> and format it with the <a href="{SEO}title-case-converter/">title case converter</a>.</p>
''',
        faqs=[
            ("What is a good headline score?", "Aim for 70 or higher. A score of 80 or more means the headline has a clear length, a good word mix and no clickbait or keyword problems. A lower score is not a failure, it simply shows the quickest fixes, so use it as a guide and trust real reader data when you have it."),
            ("How long should a headline be?", "Most strong headlines use 6 to 13 words. For the title tag that shows in Google, stay within roughly 600 pixels, which is usually 50 to 60 characters. Google has no fixed length limit, but it cuts longer titles to fit the screen."),
            ("What are power words and emotional words?", "Power words make a clear promise or create urgency, such as proven, simple, mistakes or checklist. Emotional words name a feeling, such as love, fear, proud or struggle. One of each usually helps. Stacking many of them makes a headline sound like an advert."),
            ("Is my headline sent anywhere?", "No. The analyzer runs entirely in your browser. Headlines and keywords you type are never uploaded, stored or shared, so it is safe for unpublished work and client projects."),
        ],
        related=[("Title Tag Optimization", "title-tag-optimization"), ("25 Content Writing Mistakes", "25-content-writing-mistakes"),
                 ("10 Easy Tips for Effective Content Writing", "10-easy-tips-for-effective-content-writing"), ("How to Get Cited in AI Overviews", "ai-overviews-clicks-how-to-get-cited-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-15'
