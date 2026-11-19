"""Batch 22 (2026-11-19): Content Writing Tools category, fifth tool (Passive Voice Checker).
Facts checked 2026-11-19: digital.gov plain language guide (digital.gov/guides/plain-language/writing): "Active voice makes
it clear who should do what"; passive sentences combine a form of "to be" with a past participle and often leave out who
acts; passive voice is not the same as past tense; in a few cases passive voice may be appropriate.
Yoast SEO readability analysis (yoast.com/avoid-passive-voice): green bullet when less than 10% of sentences use passive voice.
Search demand: "passive voice checker" is served by Grammarly, ProWritingAid, Originality.ai and many others.
This one runs fully in the browser, highlights every passive phrase (including modal, perfect, progressive and get passives),
shows whether the actor is named with a by phrase, keeps adjective like forms (tired, excited) apart, and gives a % score."""
import json
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
H = 'https://brandella.in/tools/seo-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

IRR = ('arisen awoken borne born beaten begun bent bet bid bitten bled blown broken bred brought built burnt burned burst bought '
       'cast caught chosen clung cost crept cut dealt dug done drawn dreamt drunk driven eaten fallen fed felt fought found fled '
       'flung forbidden forecast forgotten forgiven frozen gotten given ground grown hung heard hidden hit held hurt kept knelt '
       'known laid led leant learnt left lent let lit lost made meant met mistaken misunderstood overcome overtaken overseen '
       'overheard overlooked paid proven put quit read rebuilt redone rewritten rid ridden rung run said seen sought sold sent set '
       'sewn shaken shed shot shown shrunk shut sung sunk slain slung slit spoken sped spent spilt spun split spread sprung '
       'stolen stuck stung struck strung sworn swept swollen taken taught torn told thought thrown thrust trodden understood '
       'undertaken undone upset woken worn woven wed won wound withdrawn withheld written misled mislaid outdone outgrown '
       'oversold overpaid underpaid underwritten foreseen forbidden beset broadcast bound ground spelt spoilt dwelt').split()
# -ed words that are usually adjectives after a be verb: shown in grey, counted only if the box is ticked
ADJ = ('tired interested excited worried pleased bored married scared surprised amazed annoyed ashamed confused delighted '
       'depressed disappointed embarrassed exhausted frightened frustrated satisfied shocked terrified thrilled concerned '
       'convinced determined dedicated devoted involved mixed qualified related relaxed talented experienced skilled '
       'complicated sophisticated advanced detailed limited balanced crowded stressed motivated inspired overwhelmed '
       'prepared supposed').split()
# words ending in ed that are never participles
NOTPP = ('need bed red shed seed feed speed weed deed greed breed indeed exceed proceed succeed embed hundred naked sacred '
         'wicked rugged ragged crooked beloved kindred bred sled fled wed led fed').split()
DATA = json.dumps({'i': IRR, 'a': ADJ, 'n': [w for w in NOTPP if w not in IRR]}, separators=(',', ':'))

SAMPLE = ('Our new pricing page was launched last week. It was designed by the marketing team, and every headline was tested '
          'with real users. Visitors are now shown three plans instead of five. We are excited about the early results.\n\n'
          'Sign ups grew by 18 percent in the first seven days, and fewer support tickets were opened. Mistakes were made in the '
          'first version, so the checkout form has been rewritten. Next month, the page will be translated into Hindi and Marathi.\n\n'
          'Our sales team got paid a bonus for the launch, and the whole project is being reviewed by the leadership team on Friday. '
          'Customers love the simpler layout.')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='passive-voice-checker', short='PV', name='Passive Voice Checker',
        card='Find and highlight every passive sentence, see who is missing as the actor, and get your passive voice percentage.',
        title='Passive Voice Checker: Find Passive Sentences Free',
        desc='Free passive voice checker. Paste your text to highlight every passive sentence, see your passive percentage and get tips to rewrite it in active voice.',
        h1='Passive Voice Checker',
        lead='Paste your draft to highlight every passive sentence, see what share of your text is passive, and find out who is missing as the actor, so you can rewrite it in clear, active voice.',
        tool='''<section class="tool" aria-label="Passive voice checker">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('pvIn', 'Text to check', SAMPLE, em='a blog post, AI draft, email or page copy', tag='textarea', extra=' style="min-height:300px"') + '''
      ''' + CK('pvGet', 'Count get passives, such as <em>got paid</em>', True) + '''
      ''' + CK('pvAdj', 'Count adjective like forms, such as <em>is excited</em>', False) + '''
      ''' + F('pvGoal', 'Target', '10', tag='select', opts=[('5', 'Under 5% passive (strict)'), ('10', 'Under 10% passive (common guideline)'), ('20', 'Under 20% passive (technical or legal text)')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('pvPct', 'Passive sentences') + S('pvNum', 'Passive / total') + S('pvPh', 'Passive phrases') + S('pvNo', 'No actor named') + '''</div>
      <div class="kw-result" id="pvVerdict"></div>
      <div id="pvOut" style="max-height:380px;overflow:auto;white-space:pre-wrap;overflow-wrap:break-word;font-size:15px;line-height:1.75;background:#fff;color:#222;border:1px solid #ddd;border-radius:10px;padding:14px"></div>
      <div class="actions"><button class="btn dark" id="pvCopy">Copy Passive Sentences</button><span class="toast" id="toast">Copied!</span></div>
      <p style="font-size:13px;color:#666;margin:8px 0 0"><mark style="background:#ffd27a">Orange</mark> is a passive phrase. <mark style="background:#e8e8e8">Grey</mark> looks passive but usually works as an adjective.</p>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Every Passive Sentence</h2>
      <div style="overflow-x:auto;max-height:460px;overflow-y:auto"><table class="rtable" id="pvList"></table></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  var D = ''' + DATA + r''';
  var IRR = new Set(D.i), ADJ = new Set(D.a), NOT = new Set(D.n);
  var BE = new Set(['am','is','are','was','were','be','been','being',"isn't","aren't","wasn't","weren't","i'm","you're","we're","they're","ain't"]);
  var GET = new Set(['get','gets','got','gotten','getting']);
  var AUX = new Set(['has','have','had','will','would','can','could','may','might','must','should','shall',"won't","wouldn't","can't","couldn't","shouldn't","hasn't","haven't","hadn't","mustn't",'to','not','never']);
  var ADV = new Set(['not','never','also','often','always','already','just','still','now','then','all','both','each','usually','sometimes','rarely','seldom','being','soon','even','further','first','again','once','largely','mostly','widely','well','no','longer','too']);
  var GOOD = new Set(['agreed','freed','decreed','guaranteed','refereed','disagreed','used','owed','sued','awed','axed','aged','eyed','dyed','tied','died']);
  var ABBR = new Set(['mr','mrs','ms','dr','st','vs','etc','eg','ie','no','prof','inc','ltd','jr','sr','fig','approx']);
  var last = [];
  function isPP(w){
    if (IRR.has(w)) return true;
    if (NOT.has(w)) return false;
    if (/eed$/.test(w)) return GOOD.has(w);
    if (w.length <= 4) return GOOD.has(w);
    return /[a-z]ed$/.test(w);
  }
  function isAdv(w){ return ADV.has(w) || (w.length > 3 && /ly$/.test(w)); }
  function sentences(text){
    var out = [], start = 0, i = 0, n = text.length;
    while (i < n){
      var ch = text[i];
      if (ch === '\n'){ if (text.slice(start, i).trim()) out.push([start, i]); start = i + 1; i++; continue; }
      if (ch === '.' || ch === '!' || ch === '?'){
        var j = i; while (j + 1 < n && /[.!?"'”’)\]]/.test(text[j + 1])) j++;
        if (j + 1 >= n || /\s/.test(text[j + 1])){
          var k = j + 1; while (k < n && text[k] === ' ') k++;
          var wm = /([A-Za-z]+)\.?$/.exec(text.slice(start, i).replace(/\./g, '')), pw = wm ? wm[1].toLowerCase() : '';
          var nextOk = k >= n || /[A-Z0-9"'“‘(\n]/.test(text[k]);
          if (ch === '.' && (ABBR.has(pw) || (pw.length === 1 && /[A-Z]/.test(wm[1])))) nextOk = false;
          if (/\d$/.test(text.slice(start, i)) && k < n && /\d/.test(text[k])) nextOk = false;
          if (nextOk){ out.push([start, j + 1]); start = j + 1; i = j + 1; continue; }
        }
      }
      i++;
    }
    if (text.slice(start).trim()) out.push([start, n]);
    return out.map(function(s){ var a = s[0], b = s[1]; while (a < b && /\s/.test(text[a])) a++; return [a, b]; });
  }
  function analyse(text, useGet, useAdj){
    var sents = sentences(text), res = [];
    sents.forEach(function(s){
      var seg = text.slice(s[0], s[1]), toks = [], m, re = /[A-Za-z]+(?:['’][A-Za-z]+)?/g;
      while ((m = re.exec(seg))) toks.push({w: m[0].toLowerCase().replace(/’/g, "'"), raw: m[0], a: s[0] + m.index, b: s[0] + m.index + m[0].length});
      var hits = [];
      for (var t = 0; t < toks.length; t++){
        var w = toks[t].w, isBe = BE.has(w), isGet = useGet && GET.has(w);
        if (!isBe && !isGet) continue;
        var u = t + 1, gap = 0;
        while (u < toks.length && gap < 2 && isAdv(toks[u].w) && !isPP(toks[u].w)) { u++; gap++; }
        if (u < toks.length && toks[u].w === 'being' && isBe){ u++; }
        if (u >= toks.length) continue;
        var pp = toks[u].w;
        if (!isPP(pp)) continue;
        if (isGet && (pp === 'done' || pp === 'lost' || pp === 'used')) continue;
        if (pp === 'supposed' && toks[u + 1] && toks[u + 1].w === 'to') continue;
        if (BE.has(pp) || pp === 'got' || pp === 'gotten') continue;
        var adj = ADJ.has(pp);
        var st = t; while (st > 0 && AUX.has(toks[st - 1].w) && toks[st - 1].w !== 'to' && toks[st - 1].w !== 'not' && toks[st - 1].w !== 'never' && /^\s+$/.test(text.slice(toks[st - 1].b, toks[st].a))) st--;
        var actor = '';
        for (var v = u + 1; v < toks.length && v <= u + 4; v++){
          if (/[,;:.!?]/.test(text.slice(toks[v - 1].b, toks[v].a))) break;
          if (toks[v].w === 'by'){
            var parts = [];
            for (var x = v + 1; x < toks.length && parts.length < 5; x++){
              if (x > v + 1 && /[,;:.!?()]/.test(text.slice(toks[x - 1].b, toks[x].a))) break;
              if (/^(and|but|or|on|in|at|for|with|so|because|while|after|before|last|next|this)$/.test(toks[x].w) && parts.length) break;
              parts.push(toks[x].raw);
            }
            actor = parts.join(' '); break;
          }
        }
        hits.push({a: toks[st].a, b: toks[u].b, ph: text.slice(toks[st].a, toks[u].b), adj: adj, count: !adj || useAdj, actor: actor, pp: pp, get: isGet});
        t = u;
      }
      res.push({a: s[0], b: s[1], text: seg.trim(), hits: hits, passive: hits.some(function(h){ return h.count; })});
    });
    return res;
  }
  function run(){
    var text = $('pvIn').value, res = analyse(text, $('pvGet').checked, $('pvAdj').checked), goal = +$('pvGoal').value;
    var total = res.length, pas = res.filter(function(r){ return r.passive; }), phrases = 0, noActor = 0, marks = [];
    res.forEach(function(r){ r.hits.forEach(function(h){ marks.push(h); if (h.count){ phrases++; if (!h.actor) noActor++; } }); });
    var pct = total ? Math.round(pas.length / total * 100) : 0;
    $('pvPct').textContent = pct + '%'; $('pvNum').textContent = pas.length + ' / ' + total; $('pvPh').textContent = phrases; $('pvNo').textContent = noActor;
    var html = '', pos = 0;
    marks.sort(function(x, y){ return x.a - y.a; }).forEach(function(h){
      if (h.a < pos) return;
      html += esc(text.slice(pos, h.a));
      var bg = h.count && !h.adj ? '#ffd27a' : '#e8e8e8';
      var tip = h.adj ? 'Usually an adjective, so not counted unless you tick the box' : h.actor ? 'Passive. Actor: ' + h.actor : 'Passive. Nobody is named as the actor';
      html += '<mark title="' + esc(tip) + '" style="background:' + bg + ';padding:0 2px;border-radius:3px">' + esc(text.slice(h.a, h.b)) + '</mark>';
      pos = h.b;
    });
    html += esc(text.slice(pos));
    $('pvOut').innerHTML = text.trim() ? html : '<span style="color:#888">Your highlighted text will appear here.</span>';
    if (!text.trim()) say('pvVerdict', '', 'Paste some text to check it.');
    else if (!pas.length) say('pvVerdict', 'ok', '<strong>No passive voice found.</strong> Every sentence is in active voice.');
    else if (pct < goal) say('pvVerdict', 'ok', '<strong>Good.</strong> ' + pct + '% of your sentences use passive voice, under your ' + goal + '% target.');
    else if (pct < goal * 2) say('pvVerdict', 'warn', '<strong>A little high.</strong> ' + pct + '% of your sentences use passive voice. Rewrite about ' + Math.max(1, Math.ceil(pas.length - (goal / 100) * total + 0.0001)) + ' of them to get under ' + goal + '%.');
    else say('pvVerdict', 'bad', '<strong>Too much passive voice.</strong> ' + pct + '% of your sentences are passive. Rewrite about ' + Math.max(1, Math.ceil(pas.length - (goal / 100) * total + 0.0001)) + ' of them to get under ' + goal + '%, starting with those that name no actor.');
    last = pas.map(function(r){ return r.text; });
    var rows = [];
    pas.forEach(function(r, i){
      r.hits.filter(function(h){ return h.count; }).forEach(function(h, j){
        var tip = h.actor ? 'Start with the actor: <strong>' + esc(h.actor) + '</strong> then the verb.' : h.get ? 'Say who did it, or use a plain verb, such as <em>was paid</em> to <em>we paid</em>.' : 'Name who does it and make them the subject.';
        rows.push('<tr><td class="num">' + (j ? '' : (i + 1)) + '</td><td><strong>' + esc(h.ph) + '</strong></td><td>' + (h.actor ? esc(h.actor) : '<span style="color:#b3541e">Not named</span>') + '</td><td>' + tip + '</td><td style="min-width:240px">' + (j ? '' : esc(r.text)) + '</td></tr>');
      });
    });
    $('pvList').innerHTML = rows.length ? '<thead><tr><th class="num">#</th><th>Passive phrase</th><th>Actor</th><th>How to make it active</th><th>Sentence</th></tr></thead><tbody>' + rows.join('') + '</tbody>' : '<tbody><tr><td>No passive sentences found.</td></tr></tbody>';
  }
  $('pvIn').addEventListener('input', run);
  ['pvGet', 'pvAdj', 'pvGoal'].forEach(function(i){ $(i).addEventListener('change', run); });
  $('pvCopy').onclick = function(){ copyText(last.length ? last.join('\n') : 'No passive sentences found.', 'toast'); };
  window.__pvAnalyse = analyse;
  run();
''',
        content=f'''
    <h2>What Is a Passive Voice Checker?</h2>
    <p>A passive voice checker finds sentences where the thing being acted on comes first and the one doing the action is moved to the end, or left out. "The report was written by Priya" is passive. "Priya wrote the report" is active.</p>
    <p>Passive sentences are not wrong, but too many make writing slow, vague and hard to scan. The <a href="https://digital.gov/guides/plain-language/writing" {EXT}>US government plain language guide</a> puts it simply: active voice makes it clear who should do what. That matters for readers, for conversions, and for AI answers that quote clear, direct sentences.</p>
    <p>This tool highlights every passive phrase, tells you whether the actor is named, and shows what share of your sentences is passive. AI drafts lean on passive voice a lot, so it is a quick check before you publish.</p>

    <h2>How to Use the Checker</h2>
    <ol>
      <li><strong>Paste your text</strong> into the box. A sample is already there so you can see how it works.</li>
      <li><strong>Read the score.</strong> The result shows your passive percentage and how many sentences to rewrite to hit your target.</li>
      <li><strong>Check the highlights.</strong> Orange phrases are passive. Hover over one to see who the actor is.</li>
      <li><strong>Work through the table.</strong> Each row shows the phrase, the actor and a tip to make it active.</li>
      <li><strong>Edit and repeat.</strong> Rewrite in the box and the score updates as you type.</li>
    </ol>

    <h2>What the Checker Finds</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Type', 'Example', 'Active version')}
      <tbody>
        <tr><td>Simple passive</td><td>The page was launched last week.</td><td>We launched the page last week.</td></tr>
        <tr><td>Passive with an actor</td><td>It was designed by the marketing team.</td><td>The marketing team designed it.</td></tr>
        <tr><td>Perfect passive</td><td>The form has been rewritten.</td><td>Our developer has rewritten the form.</td></tr>
        <tr><td>Modal or future passive</td><td>The page will be translated.</td><td>Our editors will translate the page.</td></tr>
        <tr><td>Progressive passive</td><td>The project is being reviewed.</td><td>The leadership team is reviewing the project.</td></tr>
        <tr><td>Get passive</td><td>The team got paid a bonus.</td><td>We paid the team a bonus.</td></tr>
        <tr><td>Adjective like form (not counted)</td><td>We are excited about the results.</td><td>Usually fine as it is.</td></tr>
      </tbody>
    </table></div>
    <p>A passive sentence is a form of <code>be</code> (or <code>get</code>) followed by a past participle, such as <code>was written</code>. Past tense alone is not passive: "We launched the page" is active.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Aim for under 1 in 10.</strong> <a href="https://yoast.com/avoid-passive-voice/" {EXT}>Yoast SEO</a> gives a green light when fewer than 10% of sentences are passive, a fair target for blogs and web pages.</li>
      <li><strong>Fix the ones with no actor first.</strong> "Mistakes were made" hides who is responsible, and readers notice.</li>
      <li><strong>Keep passive when the actor does not matter.</strong> "The site was built in 2019" or "Your order has been shipped" read well as they are.</li>
      <li><strong>Watch AI drafts.</strong> ChatGPT and other tools often write "it is recommended that" or "can be used to". Turn them into direct advice.</li>
    </ul>

    <h2>Write Clear, Active Content</h2>
    <p>Active voice is one habit of clear writing. Learn more in <a href="{B}10-easy-tips-for-effective-content-writing/">10 easy tips for effective content writing</a>, <a href="{B}25-content-writing-mistakes/">25 content writing mistakes</a> and <a href="{B}how-to-write-seo-friendly-blog/">how to write an SEO friendly blog</a>. Then check sentence length and grade level with the <a href="{H}readability-score-checker/">readability score checker</a>, or remove the ChatGPT tone with the <a href="{T}ai-words-checker/">AI words checker</a>.</p>
''',
        faqs=[
            ("How do I check if a sentence is passive?", "Look for a form of be, such as is, was, were or has been, followed by a past participle, such as written or launched. If the one doing the action comes after the verb with by, or is missing, the sentence is passive. Paste your text into the checker to find them all at once."),
            ("Is passive voice bad for SEO?", "Google does not penalise passive voice. It matters because readers find active sentences easier to follow, and easy to read pages keep visitors longer. Tools like Yoast SEO suggest keeping passive voice under 10% of sentences."),
            ("When is passive voice the right choice?", "Use it when the actor is unknown, obvious or not important, such as your order has been shipped, or when you want to keep the focus on the thing acted on, as in scientific methods and some legal text."),
            ("Why does the checker skip words like excited or tired?", "In sentences like we are excited, the word works as an adjective that describes a feeling, not an action done to someone. Most editors do not count these as passive. Tick the box if your style guide counts them."),
        ],
        related=[("10 Easy Tips for Effective Content Writing", "10-easy-tips-for-effective-content-writing"), ("25 Content Writing Mistakes", "25-content-writing-mistakes"),
                 ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("AI Search Optimization Checklist", "ai-search-optimization-checklist-25")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-19'
