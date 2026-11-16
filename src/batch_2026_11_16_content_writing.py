"""Batch 19 (2026-11-16): Content Writing Tools category, second tool (AI Words Checker).
Facts checked 2026-11-16 against: GPTZero, "10 Phrases Most Overused by AI" (Oct 2024, gptzero.me/news/most-common-ai-vocabulary):
"play a significant role in shaping" about 182x, "today's fast paced world" 107x, "notable works include" 120x,
"aims to" 50x, showcasing 20x, aligns 16x, surpassing 12x more often in AI text than human text; GPTZero notes a flagged
phrase does not prove a text is AI written. Kobak et al., "Delving into LLM assisted writing in biomedical publications
through excess vocabulary" (arXiv 2406.07016, Science Advances 2025): at least 13.5% of 2024 PubMed abstracts were
processed with LLMs, detected through excess style words such as delves, showcasing and underscores.
Google Search Central, guidance on using generative AI content (developers.google.com/search/docs/fundamentals/using-gen-ai-content):
using AI is not against Google's rules; content made mainly to manipulate rankings is spam; accuracy and quality matter.
Search demand: "ai words checker", "ai words detector", "chatgpt words list" are served by saijogeorge.com AI words
detector, AmpiFire ABBA, wildandfreetools and GPTZero's vocabulary scan. This one adds one click plain English swaps,
chatbot leftover and long dash checks, sentence rhythm, a custom banned word list, and runs fully in the browser.
It is deliberately NOT presented as an AI detector."""
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
AIT = 'https://brandella.in/tools/ai-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

AW_TEXT = ('Certainly! Here’s a blog intro for your bakery.\n\n'
           'In today’s fast-paced world, finding the perfect birthday cake can feel overwhelming. Whether you’re a busy parent '
           'or a party planner, our bakery is a testament to the power of fresh ingredients — and it shows. Let’s delve into '
           'what makes us different.\n\n'
           'It’s important to note that every cake is meticulously crafted by hand. Our bakers leverage decades of experience to '
           'create a seamless blend of tradition and innovation. Moreover, our robust menu plays a crucial role in helping customers '
           'navigate the vibrant landscape of celebration desserts.\n\n'
           'It’s not just about cake, it’s about memories. Ready to elevate your next party? Look no further.\n\n'
           'I hope this helps!')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='ai-words-checker', short='AW', name='AI Words Checker',
        card='Find the words and phrases AI overuses, such as delve, testament and seamless, and swap them for plain English in one click.',
        title='AI Words Checker: Find Overused ChatGPT Words',
        desc='Free AI words checker. Highlight words and phrases ChatGPT overuses, like delve and testament, chatbot leftovers and long dashes, then fix them in one click.',
        h1='AI Words Checker',
        lead='Paste a draft to highlight the words, stock phrases and habits that make writing sound like ChatGPT. Each one comes with plain alternatives, and many can be fixed in one click, so your text reads like a person wrote it.',
        tool='''<section class="tool" aria-label="AI words checker">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('awIn', 'Paste your draft', AW_TEXT, em='a blog post, email, product page or AI answer', tag='textarea', extra=' style="min-height:300px"') + '''
      ''' + F('awOwn', 'Your own words to avoid', 'unparalleled, nestled', em='optional, separated by commas, such as words from your style guide') + '''
      <div class="actions" style="margin:0 0 6px"><button class="btn dark" id="awCopy">Copy Text</button><button class="btn" id="awUndo" disabled>Undo Last Fix</button><button class="btn" id="awRep">Copy Report</button><span class="toast" id="toast">Copied!</span></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('awWords', 'Words') + S('awHits', 'Flags') + S('awRate', 'Per 100 words') + S('awDash', 'Long dashes') + '''</div>
      <div class="kw-result" id="awVerdict"></div>
      <p style="font-size:13px;color:#666;margin:10px 0 6px"><span style="background:#ffe0e0;padding:1px 5px;border-radius:4px">Chatbot leftover</span> <span style="background:#ffeccc;padding:1px 5px;border-radius:4px">Stock phrase</span> <span style="background:#fff6b3;padding:1px 5px;border-radius:4px">AI word</span> <span style="background:#dcecff;padding:1px 5px;border-radius:4px">Your list</span></p>
      <pre class="code-out" id="awView" style="display:block;margin-top:0;max-height:420px;overflow:auto;white-space:pre-wrap;word-break:normal;overflow-wrap:break-word;font-family:inherit;font-size:15px;line-height:1.7;background:#fff;color:#222;border:1px solid #ddd"></pre>
    </div>
    <div class="card full" style="min-width:0">
      <h2>What to Change</h2>
      <p style="font-size:13px;color:#666;margin:0 0 8px">Click a green button to replace every match in your text. Read the sentence afterwards, and use Undo if it does not fit.</p>
      <div style="overflow-x:auto"><table class="rtable" id="awOut"></table></div>
      <div class="kw-result" id="awStyle" style="margin-top:12px"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var A = "['’]";
  // [label, kind c=chatbot p=phrase w=word, regex, suggestions, fixes {matched lower: replacement}]
  var L = [
    ['Certainly!', 'c', '\\b(certainly|absolutely|sure|of course)!\\s*', 'delete it', {'*': ''}],
    ['Great question', 'c', '\\bgreat question[.!,]?\\s*', 'delete it', {'*': ''}],
    ['Here is a ...', 'c', '(?:^|(?<=\\n)|(?<=[!.] ))\\s*here' + A + 's (a|an|the|your) [^.:\\n]{0,60}(for you|you asked|version|draft|rewrite|revised|polished|requested|blog|post|article|intro|email|caption|description|summary|outline)[^.:\\n]{0,40}[:.]\\s*', 'delete the line before you publish', {'*': ''}],
    ['I hope this helps', 'c', '\\bi hope (this|that) helps[.!]?\\s*', 'delete it', {'*': ''}],
    ['Let me know if ...', 'c', '\\blet me know if [^.!\\n]*[.!]?\\s*', 'delete it', {'*': ''}],
    ['Feel free to ...', 'c', '\\bfeel free to\\b', 'you can', {'*': 'you can'}],
    ['As an AI', 'c', '\\bas an ai( language model)?\\b,?\\s*', 'delete it', {'*': ''}],
    ['I’d be happy to', 'c', '\\bi' + A + 'd be (happy|glad) to\\b', 'delete it, or I can', null],
    ["In today's fast paced world", 'p', '\\bin today' + A + 's (fast[ -]paced|digital|modern|ever[ -](changing|evolving)) (world|age|landscape|era)\\b,?\\s*', 'delete it and start with your point', {'*': ''}],
    ["It's important to note that", 'p', '\\bit' + A + 's (important|worth) (to note|noting|to remember|mentioning) that\\s*', 'delete it', {'*': ''}],
    ['Plays a crucial role', 'p', '\\bplay(s|ed|ing)? an? (crucial|pivotal|significant|vital|key|critical|major|important) role( in( shaping)?)?', 'matters for, helps, shapes', null],
    ['A testament to', 'p', '\\b(is |stands as )?a testament to\\b', 'shows, proves', {'a testament to': 'proof of', 'is a testament to': 'shows', 'stands as a testament to': 'shows'}],
    ["Let's dive in", 'p', '\\blet' + A + 's (dive|delve|jump) (in|into|deeper)\\b', 'let us start, here is how', {'*': 'let us look at'}],
    ['Dive into / deep dive', 'p', '\\b(a )?deep dive( into)?\\b|\\bdive (deep )?into\\b', 'look at, explain, a close look at', null],
    ['In the realm of', 'p', '\\bin the (realm|world|landscape) of\\b', 'in', {'*': 'in'}],
    ['Navigate the complexities', 'p', '\\bnavigat(e|es|ing) the (complexities|intricacies|challenges|nuances) of\\b', 'handle, deal with', null],
    ['When it comes to', 'p', '\\bwhen it comes to\\b', 'for, with', {'*': 'for'}],
    ['At the end of the day', 'p', '\\bat the end of the day\\b,?\\s*', 'in the end, or delete it', {'*': ''}],
    ['In conclusion', 'p', '\\b(in conclusion|in summary|to sum up|all in all|ultimately),\\s*', 'delete it, the last paragraph is the conclusion', {'*': ''}],
    ["Whether you're a X or a Y", 'p', '\\bwhether you' + A + 're an? [^,.]{1,40} or an? [^,.]{1,40}', 'name the one reader you are writing for', null],
    ["It's not just X, it's Y", 'p', '\\b(it|this|that)' + A + 's not (just|only) (about )?[^,.;]{1,40}[,;]\\s*(it|this|that)' + A + 's\\b|\\bisn' + A + 't just [^,.;]{1,40}[,;]\\s*it' + A + 's\\b', 'say the main point once', null],
    ['Not only ... but also', 'p', '\\bnot only\\b[^.]{1,60}\\bbut also\\b', 'and, as well as', null],
    ['Look no further', 'p', '\\blook no further\\b[.!]?\\s*', 'delete it', {'*': ''}],
    ['Unlock the potential', 'p', '\\bunlock(ing)? (the|your) (full )?(potential|power) of\\b', 'get more from, use', {'*': 'get more from'}],
    ['Harness the power of', 'p', '\\bharness(ing)? the power of\\b', 'use', {'*': 'use'}],
    ['Take it to the next level', 'p', '\\btake (it|your [a-z]+|things) to the next level\\b', 'improve it, grow it', null],
    ['Stay ahead of the curve', 'p', '\\bstay ahead of the curve\\b', 'stay ahead, keep up', {'*': 'stay ahead'}],
    ['Embark on a journey', 'p', '\\bembark(s|ed|ing)? on (a|an|your|this) [a-z ]{0,20}journey\\b', 'start', null],
    ['Game changer', 'p', '\\bgame[ -]?changer(s)?\\b|\\bgame[ -]changing\\b', 'a big change, describe the actual result', null],
    ['Ever evolving', 'p', '\\bever[ -](evolving|changing)\\b', 'changing', {'*': 'changing'}],
    ['A wide range of', 'p', '\\ba (wide|vast|broad|diverse) (range|array|variety) of\\b', 'many, lots of', {'*': 'many'}],
    ['Serves as / stands as', 'p', '\\b(serves|stands) as\\b', 'is', {'*': 'is'}],
    ['Aims to', 'p', '\\baims to\\b', 'wants to, tries to, will', null],
    ['Delve', 'w', '\\bdelv(e|es|ed|ing)( into)?\\b', 'explore, look at, dig into', {delve: 'explore', delves: 'explores', delved: 'explored', delving: 'exploring', 'delve into': 'explore', 'delves into': 'explores', 'delved into': 'explored', 'delving into': 'exploring'}],
    ['Testament', 'w', '\\btestament\\b', 'proof, sign', null],
    ['Tapestry', 'w', '\\b(rich )?tapestr(y|ies)\\b', 'mix, range', null],
    ['Underscore', 'w', '\\bunderscor(e|es|ed|ing)\\b', 'shows, highlights', {underscore: 'show', underscores: 'shows', underscored: 'showed', underscoring: 'showing'}],
    ['Pivotal', 'w', '\\bpivotal\\b', 'key, important', {'*': 'key'}],
    ['Crucial', 'w', '\\bcrucial(ly)?\\b', 'key, important', {crucial: 'key', crucially: 'importantly'}],
    ['Realm', 'w', '\\brealms?\\b', 'area, field', {realm: 'area', realms: 'areas'}],
    ['Landscape', 'w', '\\blandscapes?\\b', 'market, field, scene', null],
    ['Showcase', 'w', '\\bshowcas(e|es|ed|ing)\\b', 'show, display', {showcase: 'show', showcases: 'shows', showcased: 'showed', showcasing: 'showing'}],
    ['Seamless', 'w', '\\bseamless(ly)?\\b', 'smooth, easy', {seamless: 'smooth', seamlessly: 'smoothly'}],
    ['Robust', 'w', '\\brobust\\b', 'strong, solid', {'*': 'strong'}],
    ['Leverage', 'w', '\\bleverag(e|es|ed|ing)\\b', 'use', {leverage: 'use', leverages: 'uses', leveraged: 'used', leveraging: 'using'}],
    ['Utilize', 'w', '\\butili[sz](e|es|ed|ing)\\b', 'use', {utilize: 'use', utilizes: 'uses', utilized: 'used', utilizing: 'using', utilise: 'use', utilises: 'uses', utilised: 'used', utilising: 'using'}],
    ['Navigate', 'w', '\\bnavigat(e|es|ed|ing)\\b', 'handle, deal with, find your way', null],
    ['Foster', 'w', '\\bfoster(s|ed|ing)?\\b', 'build, encourage', {foster: 'build', fosters: 'builds', fostered: 'built', fostering: 'building'}],
    ['Embark', 'w', '\\bembark(s|ed|ing)?\\b', 'start, begin', null],
    ['Elevate', 'w', '\\belevat(e|es|ed|ing)\\b', 'improve, raise', {elevate: 'improve', elevates: 'improves', elevated: 'improved', elevating: 'improving'}],
    ['Unleash', 'w', '\\bunleash(es|ed|ing)?\\b', 'release, use', null],
    ['Harness', 'w', '\\bharness(es|ed|ing)?\\b', 'use', {harness: 'use', harnesses: 'uses', harnessed: 'used', harnessing: 'using'}],
    ['Meticulous', 'w', '\\bmeticulous(ly)?\\b', 'careful, carefully', {meticulous: 'careful', meticulously: 'carefully'}],
    ['Intricate', 'w', '\\bintricate(ly)?\\b|\\bintricacies\\b', 'detailed, complex, details', null],
    ['Multifaceted', 'w', '\\bmulti[ -]?faceted\\b', 'complex, varied', {'*': 'varied'}],
    ['Vibrant', 'w', '\\bvibrant\\b', 'lively, bright', {'*': 'lively'}],
    ['Bustling', 'w', '\\bbustling\\b', 'busy', {'*': 'busy'}],
    ['Paramount', 'w', '\\bparamount\\b', 'most important', null],
    ['Comprehensive', 'w', '\\bcomprehensive\\b', 'full, complete', {'*': 'complete'}],
    ['Moreover / Furthermore', 'w', '\\b(moreover|furthermore|additionally)\\b,?', 'delete it, or use also', {'*': ''}],
    ['Notably', 'w', '\\bnotably\\b', 'especially', {'*': 'especially'}],
    ['Myriad / plethora', 'w', '\\b(a )?(myriad|plethora)( of)?\\b', 'many, lots of', {'*': 'many'}],
    ['Nuanced', 'w', '\\bnuanced?\\b', 'subtle, detailed', null],
    ['Holistic', 'w', '\\bholistic(ally)?\\b', 'whole, complete', null],
    ['Transformative', 'w', '\\btransformative\\b', 'major, big', {'*': 'major'}],
    ['Cutting edge', 'w', '\\bcutting[ -]edge\\b|\\bstate[ -]of[ -]the[ -]art\\b', 'new, modern, latest', {'*': 'modern'}],
    ['Streamline', 'w', '\\bstreamlin(e|es|ed|ing)\\b', 'simplify, speed up', {streamline: 'simplify', streamlines: 'simplifies', streamlined: 'simpler', streamlining: 'simplifying'}],
    ['Revolutionize', 'w', '\\brevolutioni[sz](e|es|ed|ing)\\b', 'change, improve', null],
    ['Bolster', 'w', '\\bbolster(s|ed|ing)?\\b', 'support, strengthen', {bolster: 'support', bolsters: 'supports', bolstered: 'supported', bolstering: 'supporting'}],
    ['Resonate', 'w', '\\bresonat(e|es|ed|ing)\\b', 'connect, appeal', null],
    ['Empower', 'w', '\\bempower(s|ed|ing)?\\b', 'help, let', null],
    ['Facilitate', 'w', '\\bfacilitat(e|es|ed|ing)\\b', 'help, make easier', {facilitate: 'help', facilitates: 'helps', facilitated: 'helped', facilitating: 'helping'}],
    ['Enhance', 'w', '\\benhanc(e|es|ed|ing)\\b', 'improve', {enhance: 'improve', enhances: 'improves', enhanced: 'improved', enhancing: 'improving'}],
    ['Endeavor', 'w', '\\bendeavou?rs?\\b', 'effort, try', null],
    ['Invaluable', 'w', '\\binvaluable\\b', 'very useful', {'*': 'very useful'}],
    ['Captivating', 'w', '\\bcaptivat(e|es|ed|ing)\\b', 'interesting, gripping', null],
    ['Commendable', 'w', '\\bcommendable\\b', 'good, impressive', {'*': 'impressive'}],
    ['Synergy', 'w', '\\bsynerg(y|ies)\\b', 'teamwork, working together', null],
    ['Beacon', 'w', '\\bbeacons?\\b', 'example, guide', null],
    ['Treasure trove', 'w', '\\btreasure troves?\\b', 'collection, source', {'treasure trove': 'collection'}],
    ['Aligns', 'w', '\\balign(s|ed|ing)? with\\b', 'fits, matches', {'aligns with': 'fits', 'align with': 'fit', 'aligned with': 'matched', 'aligning with': 'matching'}],
    ['Surpassing', 'w', '\\bsurpass(es|ed|ing)?\\b', 'beat, pass', null]
  ];
  var KIND = {c: ['Chatbot leftover', '#ffe0e0', 3], p: ['Stock phrase', '#ffeccc', 2], w: ['AI word', '#fff6b3', 1], u: ['Your list', '#dcecff', 1]};
  var RX = L.map(function(e){ return new RegExp(e[2], 'gi'); });
  function own(){
    return $('awOwn').value.split(/[,\n]/).map(function(x){ return x.trim(); }).filter(function(x){ return x.length > 1; }).slice(0, 50);
  }
  function rxEsc(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function entries(){
    var E = L.map(function(e, i){ return {l: e[0], k: e[1], rx: RX[i], s: e[3], f: e[4]}; });
    var seen = {};
    own().forEach(function(w){
      var lw = w.toLowerCase(); if (seen[lw]) return; seen[lw] = 1;
      if (E.some(function(e){ e.rx.lastIndex = 0; var m = e.rx.exec(w); return m && m[0].trim().toLowerCase() === lw; })) return;
      E.push({l: w, k: 'u', rx: new RegExp('\\b' + rxEsc(w) + '\\b', 'gi'), s: 'from your own list', f: null});
    });
    return E;
  }
  function find(t){
    var E = entries(), M = [];
    E.forEach(function(e, ei){ e.rx.lastIndex = 0; var m; while ((m = e.rx.exec(t))){ if (!m[0].length){ e.rx.lastIndex++; continue; } M.push({a: m.index, b: m.index + m[0].length, e: ei, t: m[0]}); } });
    var pr = {c: 0, u: 1, p: 2, w: 3};
    M.sort(function(x, y){ return x.a - y.a || pr[E[x.e].k] - pr[E[y.e].k] || (y.b - y.a) - (x.b - x.a); });
    var out = [], end = -1;
    M.forEach(function(m){ if (m.a >= end){ out.push(m); end = m.b; } });
    return {E: E, M: out};
  }
  function wc(t){ return (t.match(/[\p{L}\p{N}][\p{L}\p{N}'’]*/gu) || []).length; }
  function sentences(t){ return t.replace(/\n+/g, '. ').split(/(?<=[.!?])\s+/).map(function(s){ return s.trim(); }).filter(function(s){ return wc(s) > 2; }); }
  var last = null, undo = [];
  function fixFor(e, txt){
    if (!e.f) return null;
    var k = txt.toLowerCase().replace(/’/g, "'").replace(/[,!.:\s]+$/, '');
    if (k in e.f) return e.f[k];
    if ('*' in e.f) return e.f['*'];
    return null;
  }
  function matchCase(src, rep){
    if (!rep) return rep;
    if (src === src.toUpperCase() && /[A-Z]{2}/.test(src)) return rep.toUpperCase();
    if (/^[A-Z]/.test(src)) return rep.charAt(0).toUpperCase() + rep.slice(1);
    return rep;
  }
  function applyFix(ei){
    var t = $('awIn').value, r = find(t), e = r.E[ei], ms = r.M.filter(function(m){ return m.e === ei; });
    if (!ms.length) return;
    undo.push(t); if (undo.length > 30) undo.shift();
    var out = '', pos = 0;
    ms.forEach(function(m){
      var rep = fixFor(e, m.t); if (rep === null){ return; }
      var before = out + t.slice(pos, m.a);
      if (rep === ''){
        var startOfSentence = /(^|[.!?:]\s*|\n\s*)$/.test(before);
        out = before; pos = m.b;
        if (startOfSentence){
          var rest = t.slice(pos);
          var lead = rest.match(/^\s*/)[0]; pos += lead.length;
          if (/^[a-z]/.test(t.charAt(pos))){ out += t.charAt(pos).toUpperCase(); pos++; }
        } else if (/ $/.test(out) && /^[ ,.]/.test(t.slice(pos))) { out = out.replace(/ +$/, ''); if (!/^[,.]/.test(t.slice(pos))) out += ' '; }
      } else {
        var core = m.t.replace(/[,\s]+$/, ''), trail = m.t.slice(core.length);
        out = before + matchCase(core, rep) + trail; pos = m.b;
      }
    });
    out += t.slice(pos);
    out = out.replace(/[ \t]{2,}/g, ' ').replace(/\n{3,}/g, '\n\n').replace(/^\s+/, '');
    $('awIn').value = out; $('awUndo').disabled = false; run();
  }
  function run(){
    var t = $('awIn').value, r = find(t), E = r.E, M = r.M, n = wc(t);
    var dashes = (t.match(/[—–]|\s--\s/g) || []).length;
    var pts = 0; M.forEach(function(m){ pts += KIND[E[m.e].k][2]; }); pts += dashes;
    var rate = n ? Math.round(pts * 1000 / n) / 10 : 0;
    $('awWords').textContent = fmtN(n); $('awHits').textContent = M.length + dashes; $('awRate').textContent = rate; $('awDash').textContent = dashes;
    var view = '', p = 0;
    M.forEach(function(m){ var k = KIND[E[m.e].k]; view += esc(t.slice(p, m.a)) + '<mark title="' + esc(k[0] + ': try ' + E[m.e].s) + '" style="background:' + k[1] + ';color:inherit;border-radius:3px;padding:0 2px">' + esc(m.t.replace(/\s+$/, '')) + '</mark>' + esc((m.t.match(/\s+$/) || [''])[0]); p = m.b; });
    view += esc(t.slice(p));
    view = view.replace(/[—–]/g, '<mark title="Long dash" style="background:#e8dcff;color:inherit;border-radius:3px;padding:0 2px">$&</mark>');
    $('awView').innerHTML = view || 'Your highlighted text will show here.';
    var cnt = {}; M.forEach(function(m){ var x = cnt[m.e] || (cnt[m.e] = {n: 0, ex: m.t.trim()}); x.n++; });
    var rows = Object.keys(cnt).map(Number).sort(function(a, b){ var ka = KIND[E[a].k][2], kb = KIND[E[b].k][2]; return kb - ka || cnt[b].n - cnt[a].n; });
    last = {n: n, hits: M.length + dashes, rate: rate, dashes: dashes, rows: rows.map(function(i){ return [KIND[E[i].k][0], cnt[i].ex, cnt[i].n, E[i].s]; })};
    if (!t.trim()){ say('awVerdict', '', 'Paste some text to check it.'); $('awOut').innerHTML = ''; say('awStyle', '', ''); return; }
    var lvl = rate < 1 ? ['ok', 'Reads natural.', 'Very few AI style words. Give it a final read for facts and tone.'] : rate < 3 ? ['warn', 'Some AI style.', 'A few words and phrases readers link with AI. Swap the ones below that do not sound like you.'] : ['bad', 'Heavy AI style.', 'Many words and phrases that readers link with ChatGPT. Rewrite the flagged parts in your own words before you publish.'];
    say('awVerdict', lvl[0], '<strong>' + lvl[1] + '</strong> ' + lvl[2] + ' This is a style check, not an AI detector.');
    $('awOut').innerHTML = rows.length ? '<thead><tr><th>Type</th><th>Found</th><th>Times</th><th>Try instead</th><th>Fix</th></tr></thead><tbody>' + rows.map(function(i){
      var e = E[i], x = cnt[i], rep = fixFor(e, x.ex), btn = rep === null ? '<span style="color:#777">Rewrite by hand</span>' : '<button class="btn btn-sm dark" data-fix="' + i + '">' + (rep === '' ? 'Remove' : 'Use ' + esc(rep)) + '</button>';
      return '<tr><td><span style="background:' + KIND[e.k][1] + ';padding:1px 6px;border-radius:4px;white-space:nowrap">' + KIND[e.k][0] + '</span></td><td><strong>' + esc(x.ex) + '</strong></td><td>' + x.n + '</td><td>' + esc(e.s) + '</td><td>' + btn + '</td></tr>'; }).join('') + '</tbody>'
      : '<tbody><tr><td>No AI style words or phrases found.</td></tr></tbody>';
    var S = sentences(t), notes = [];
    if (dashes) notes.push('<strong>Long dashes:</strong> ' + dashes + ' found. AI tools use them a lot. A comma, a full stop or brackets usually reads more natural.');
    if (S.length >= 5){
      var ls = S.map(wc), mean = ls.reduce(function(a, b){ return a + b; }, 0) / ls.length, sd = Math.sqrt(ls.reduce(function(a, b){ return a + (b - mean) * (b - mean); }, 0) / ls.length), cv = sd / mean;
      notes.push('<strong>Sentence rhythm:</strong> average ' + Math.round(mean) + ' words, ' + (cv < 0.35 ? 'and most sentences are a similar length, which can sound flat and machine made. Mix in a few short ones.' : 'with a healthy mix of short and long sentences.'));
    }
    var starts = S.filter(function(s){ return /^(moreover|furthermore|additionally|however|overall|ultimately|in addition)\b/i.test(s); }).length;
    if (starts >= 2) notes.push('<strong>Sentence openers:</strong> ' + starts + ' sentences start with words like Moreover or Additionally. Most can simply be deleted.');
    say('awStyle', notes.length ? 'warn' : 'ok', notes.length ? notes.join('<br>') : 'No long dashes or repeated sentence openers found.');
  }
  $('awOut').addEventListener('click', function(ev){ var b = ev.target.closest('[data-fix]'); if (b) applyFix(+b.getAttribute('data-fix')); });
  $('awIn').addEventListener('input', run); $('awOwn').addEventListener('input', run);
  $('awUndo').onclick = function(){ if (!undo.length) return; $('awIn').value = undo.pop(); this.disabled = !undo.length; run(); };
  $('awCopy').onclick = function(){ var s = $('awIn').value.trim(); if (s) copyText(s, 'toast'); };
  $('awRep').onclick = function(){ if (!last || !last.n) return; copyText('AI words check\nWords: ' + last.n + '\nFlags: ' + last.hits + ' (' + last.rate + ' per 100 words)\nLong dashes: ' + last.dashes + '\n\n' + last.rows.map(function(r){ return r[0] + ': "' + r[1] + '" x' + r[2] + ', try ' + r[3]; }).join('\n'), 'toast'); };
  run();
''',
        content=f'''
    <h2>What Is an AI Words Checker?</h2>
    <p>An AI words checker scans your text for the words and phrases that AI writing tools use far more often than people do. Think <q>delve</q>, <q>a testament to</q>, <q>seamless</q> and <q>in today's fast paced world</q>. It highlights each one, explains what to use instead, and lets you swap many of them for plain English in one click.</p>
    <p>These patterns are measurable. A study of more than 15 million PubMed abstracts by Kobak and colleagues, <a href="https://arxiv.org/abs/2406.07016" {EXT}>published in Science Advances</a>, found a sudden jump in style words such as <q>delves</q>, <q>showcasing</q> and <q>underscores</q> after ChatGPT arrived, and estimated that at least 13.5% of 2024 abstracts were processed with AI. GPTZero found phrases like <q>today's fast paced world</q> appear over 100 times more often in AI text than in human writing.</p>

    <h2>How to Use the AI Words Checker</h2>
    <ol>
      <li><strong>Paste your draft</strong> into the box. Highlights and counts update as you type.</li>
      <li><strong>Add your own words</strong> to avoid, such as banned terms from your brand style guide.</li>
      <li><strong>Read the highlights.</strong> Hover over any one to see a plainer option.</li>
      <li><strong>Fix the list.</strong> Click a green button to replace every match, or rewrite by hand where the tool says so. Use Undo if a swap does not fit.</li>
      <li><strong>Copy your text</strong> or copy the report to share with a writer or client.</li>
    </ol>

    <h2>What the Checker Looks For</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Type', 'Examples', 'Why it matters')}
      <tbody>
        <tr><td>Chatbot leftovers</td><td>Certainly!, I hope this helps, let me know if</td><td>Lines meant for the chat, not the page. Always delete them.</td></tr>
        <tr><td>Stock phrases</td><td>plays a crucial role, it's not just X it's Y, look no further</td><td>Fillers that say little and make every AI text sound the same.</td></tr>
        <tr><td>AI words</td><td>delve, tapestry, leverage, robust, vibrant, elevate</td><td>Fine on their own, but a cluster of them is a clear tell.</td></tr>
        <tr><td>Long dashes</td><td>dashes used to join two thoughts</td><td>AI tools use them heavily. A comma or full stop often reads better.</td></tr>
        <tr><td>Sentence rhythm</td><td>many sentences of the same length</td><td>Even rhythm sounds flat. People mix short and long sentences.</td></tr>
      </tbody>
    </table></div>
    <p>The score is flags per 100 words, weighted so chatbot leftovers count most. Under 1 reads natural, 1 to 3 has some AI style, and over 3 needs a rewrite.</p>

    <h2>Is This an AI Detector?</h2>
    <p>No, and that is on purpose. People use these words too, and a flag never proves a text was written by AI. Treat the results as editing suggestions. Google says in its <a href="https://developers.google.com/search/docs/fundamentals/using-gen-ai-content" {EXT}>guidance on generative AI content</a> that using AI is fine, as long as the content is accurate, original and made to help people rather than to game rankings.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Cut before you swap.</strong> Many flagged phrases can simply be deleted, and the sentence gets better.</li>
      <li><strong>Add what AI cannot.</strong> Real numbers, your own examples and a clear opinion make text feel human far more than any word swap.</li>
      <li><strong>Read it out loud.</strong> If you would never say a word to a friend, replace it.</li>
      <li><strong>Prompt better.</strong> Ask the AI to write in plain English and avoid the words on your list, then check the result here.</li>
    </ul>

    <h2>Write Content People Trust</h2>
    <p>Learn what Google expects in our guide to <a href="{B}google-ai-content-guidelines-2026/">Google's AI content guidelines</a>, avoid the traps in <a href="{B}25-content-writing-mistakes/">25 content writing mistakes</a>, and follow our <a href="{B}10-easy-tips-for-effective-content-writing/">easy tips for effective content writing</a>. Then pick a strong title with the <a href="{T}headline-analyzer/">headline analyzer</a>, and remove hidden characters and Markdown with the <a href="{AIT}ai-text-cleaner/">AI text cleaner</a>.</p>
''',
        faqs=[
            ("What words does ChatGPT use too much?", "Common ones include delve, testament, tapestry, underscore, pivotal, seamless, robust, leverage, vibrant and elevate, plus phrases such as in today's fast paced world, plays a crucial role and it's important to note. Research on millions of scientific abstracts and AI text samples shows these words became far more common after ChatGPT launched."),
            ("Can this tool tell if text was written by AI?", "No. It is a style checker, not a detector. People use these words too, so a flag only means a phrase sounds like AI writing. No tool can prove who wrote a text, and AI detectors often make mistakes on human writing."),
            ("Does Google penalize AI written content?", "Not for using AI. Google says appropriate use of AI is not against its guidelines. What matters is that the content is helpful, accurate and original. Content made mainly to manipulate rankings is treated as spam, however it was written."),
            ("Is my text uploaded anywhere?", "No. The checker runs entirely in your browser. Your text and word list are never sent to us, to an AI model or to anyone else, so it is safe for client work and unpublished drafts."),
        ],
        related=[("Google AI Content Guidelines 2026", "google-ai-content-guidelines-2026"), ("25 Content Writing Mistakes", "25-content-writing-mistakes"),
                 ("10 Easy Tips for Effective Content Writing", "10-easy-tips-for-effective-content-writing"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-16'
