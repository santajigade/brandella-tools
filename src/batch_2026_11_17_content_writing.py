"""Batch 20 (2026-11-17): Content Writing Tools category, third tool (Text Similarity Checker).
Facts checked 2026-11-17 against: Google Search Central spam policies (developers.google.com/search/docs/essentials/spam-policies):
scraped content includes sites that copy content from other sites, modify it only slightly (for example by substituting
synonyms or using automated techniques) and republish it; scaled content abuse covers many pages made mainly to
manipulate rankings, however they are made. Google Search Central guidance on generative AI content: using AI is fine
when the result is helpful and original. Google's Dan Nguyen (Search Office Hours, reported by Plagiarism Today) said
sites that use AI to plagiarize and modify content violate the spam rules.
Search demand: "compare two texts for plagiarism", "text similarity checker", "text compare" are served by
Copyleaks Text Compare, Originality.ai Text Compare, PlagAware and dcode. This one is free with no word limit, shows
matching passages side by side, a copied share for each text, word overlap, and runs fully in the browser.
It does not search the web: it compares the two texts you paste."""
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
DV = 'https://brandella.in/tools/developer-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

SI_A = ('Composting at home is one of the easiest ways to cut kitchen waste. Fruit peels, vegetable scraps, tea leaves and '
        'coffee grounds can all go into the bin, along with dry leaves and shredded cardboard. The trick is to keep a good '
        'balance between green and brown material, so the pile stays moist but never smells.\n\n'
        'Turn the pile once a week to let air in. In warm weather, finished compost can be ready in as little as eight weeks. '
        'Dark, crumbly compost that smells like soil is a sign that it is ready to use in your garden or pots.')
SI_B = ('Home composting is one of the easiest ways to cut kitchen waste. You can add fruit peels, vegetable scraps, tea leaves and '
        'coffee grounds, along with dry leaves and shredded cardboard. The key is to keep a good balance between green and brown '
        'material so the heap stays damp without any bad smell.\n\n'
        'Mix the heap every week so air can get in. When the weather is warm, finished compost can be ready in as little as eight weeks. '
        'If it looks dark and crumbly and smells like fresh earth, it is ready for your plants.')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='text-similarity-checker', short='SI', name='Text Similarity Checker',
        card='Compare two texts to see how much was copied, with every matching passage highlighted side by side.',
        title='Text Similarity Checker: Compare Two Texts for Plagiarism',
        desc='Free text similarity checker. Paste two texts to see the copied share, word overlap and every matching passage highlighted side by side. No word limit.',
        h1='Text Similarity Checker',
        lead='Paste an original and a second text to see how much of it was copied. Every shared passage is highlighted in both texts, with a copied share, word overlap and the longest match, so you can tell a real rewrite from a light reword.',
        tool='''<section class="tool" aria-label="Text similarity checker">
    <div class="card" style="min-width:0">
      <h2>Original Text</h2>
      ''' + F('siA', 'Source or first text', SI_A, em='the article, page or essay you compare against', tag='textarea', extra=' style="min-height:240px"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Text to Check</h2>
      ''' + F('siB', 'Rewrite or second text', SI_B, em='an AI rewrite, guest post, student essay or competitor page', tag='textarea', extra=' style="min-height:240px"') + '''
    </div>
    <div class="card full" style="min-width:0">
      <div class="row2">
        ''' + F('siN', 'Shortest match to count', '5', em='in words', tag='select', opts=[('3', '3 words (strict)'), ('4', '4 words'), ('5', '5 words (recommended)'), ('6', '6 words'), ('8', '8 words (loose)')]) + '''
        <div class="field"><label>Actions</label><div class="actions" style="margin:0"><button class="btn" id="siSwap">Swap Texts</button><button class="btn dark" id="siRep">Copy Report</button><span class="toast" id="toast">Copied!</span></div></div>
      </div>
      <div class="stats">''' + S('siCopy', 'Copied in text to check') + S('siUsed', 'Original reused') + S('siOver', 'Word overlap') + S('siLong', 'Longest match, words') + '''</div>
      <div class="kw-result" id="siVerdict"></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Original, Matches Marked</h2>
      <pre class="code-out" id="siViewA" style="display:block;margin-top:0;max-height:420px;overflow:auto;white-space:pre-wrap;word-break:normal;overflow-wrap:break-word;font-family:inherit;font-size:15px;line-height:1.7;background:#fff;color:#222;border:1px solid #ddd"></pre>
    </div>
    <div class="card" style="min-width:0">
      <h2>Text to Check, Matches Marked</h2>
      <pre class="code-out" id="siViewB" style="display:block;margin-top:0;max-height:420px;overflow:auto;white-space:pre-wrap;word-break:normal;overflow-wrap:break-word;font-family:inherit;font-size:15px;line-height:1.7;background:#fff;color:#222;border:1px solid #ddd"></pre>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Matching Passages</h2>
      <p style="font-size:13px;color:#666;margin:0 0 8px">Longest first. Click a row to jump to that passage in both texts.</p>
      <div style="overflow-x:auto;max-height:420px;overflow-y:auto"><table class="rtable" id="siOut"></table></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  var RE = /[\p{L}\p{N}]+(?:['’][\p{L}\p{N}]+)*/gu, last = null;
  function toks(s){ var out = [], m; RE.lastIndex = 0; while ((m = RE.exec(s))) out.push({w: m[0].toLowerCase().replace(/’/g, "'"), s: m.index, e: m.index + m[0].length}); return out; }
  function pct(a, b){ return b ? Math.round(a * 1000 / b) / 10 : 0; }
  function view(text, T, M){
    var out = '', pos = 0, open = 0;
    for (var k = 0; k < T.length; k++){
      var id = M[k];
      if (open && id !== open){ out += '</mark>'; open = 0; }
      out += esc(text.slice(pos, T[k].s));
      if (id && !open){ out += '<mark data-m="' + id + '" title="Match ' + id + '" style="background:' + (id % 2 ? '#fff1a8' : '#ffd9a8') + ';padding:0 1px;border-radius:3px">'; open = id; }
      out += esc(text.slice(T[k].s, T[k].e)); pos = T[k].e;
    }
    if (open) out += '</mark>';
    return out + esc(text.slice(pos));
  }
  function run(){
    var a = $('siA').value, b = $('siB').value, n = +$('siN').value;
    var A = toks(a), Bt = toks(b), mA = new Int32Array(A.length), mB = new Int32Array(Bt.length), P = [];
    if (!A.length || !Bt.length){
      say('siVerdict', '', 'Paste text in both boxes to compare them.');
      ['siCopy', 'siUsed', 'siOver'].forEach(function(i){ $(i).textContent = '0%'; }); $('siLong').textContent = '0';
      $('siViewA').innerHTML = esc(a); $('siViewB').innerHTML = esc(b); $('siOut').innerHTML = ''; last = null; return;
    }
    if (A.length < n || Bt.length < n){
      say('siVerdict', 'warn', 'Each text needs at least ' + n + ' words to find matches. Add more text or pick a shorter match length.');
      ['siCopy', 'siUsed', 'siOver'].forEach(function(i){ $(i).textContent = '0%'; }); $('siLong').textContent = '0';
      $('siViewA').innerHTML = esc(a); $('siViewB').innerHTML = esc(b); $('siOut').innerHTML = ''; last = null; return;
    }
    var aw = A.map(function(t){ return t.w; }), bw = Bt.map(function(t){ return t.w; }), idx = new Map();
    for (var j = 0; j + n <= aw.length; j++){ var key = aw.slice(j, j + n).join(' '); var l = idx.get(key); if (l){ if (l.length < 300) l.push(j); } else idx.set(key, [j]); }
    var i = 0;
    while (i + n <= bw.length){
      var cand = idx.get(bw.slice(i, i + n).join(' ')), best = 0, bj = -1;
      if (cand) cand.forEach(function(j){ var L = n; while (i + L < bw.length && j + L < aw.length && bw[i + L] === aw[j + L]) L++; if (L > best){ best = L; bj = j; } });
      if (best){
        var id = P.length + 1;
        for (var k = 0; k < best; k++){ mB[i + k] = id; if (!mA[bj + k]) mA[bj + k] = id; }
        P.push({id: id, len: best, text: b.slice(Bt[i].s, Bt[i + best - 1].e)});
        i += best;
      } else i++;
    }
    var cB = 0, cA = 0; mB.forEach(function(v){ if (v) cB++; }); mA.forEach(function(v){ if (v) cA++; });
    function bag(ws){ var s = new Set(); ws.forEach(function(w){ if (!STOP.has(w) && w.length > 1 && !/^\d+$/.test(w)) s.add(w); }); return s; }
    var sa = bag(aw), sb = bag(bw), inter = 0; sb.forEach(function(w){ if (sa.has(w)) inter++; });
    var uni = sa.size + sb.size - inter, over = pct(inter, uni), copy = pct(cB, Bt.length), used = pct(cA, A.length);
    var longest = P.reduce(function(m, p){ return Math.max(m, p.len); }, 0);
    $('siCopy').textContent = copy + '%'; $('siUsed').textContent = used + '%'; $('siOver').textContent = over + '%'; $('siLong').textContent = longest;
    var v = copy < 10 ? ['ok', 'Original.', 'Very little text is shared. Short matches like names and common phrases are normal.']
      : copy < 30 ? ['warn', 'Some copying.', 'A few passages are copied word for word. Rewrite them, or quote and credit the source.']
      : copy < 60 ? ['bad', 'Heavily copied.', 'Large parts are copied or only lightly reworded. This reads as a reword, not a new piece.']
      : ['bad', 'Near copy.', 'Most of the text matches the original. Treat it as a duplicate.'];
    var note = (copy < 30 && over >= 60) ? ' Word overlap is high though, so the ideas and wording follow the original closely. Check it is a real rewrite and not a synonym swap.' : '';
    say('siVerdict', v[0], '<strong>' + v[1] + '</strong> ' + esc(fmtN(cB)) + ' of ' + esc(fmtN(Bt.length)) + ' words in the text to check sit inside matching passages of ' + n + ' or more words. ' + v[2] + note);
    $('siViewA').innerHTML = view(a, A, mA); $('siViewB').innerHTML = view(b, Bt, mB);
    var S = P.slice().sort(function(x, y){ return y.len - x.len || x.id - y.id; });
    $('siOut').innerHTML = S.length ? '<thead><tr><th>Match</th><th>Words</th><th>Passage</th></tr></thead><tbody>' + S.slice(0, 200).map(function(p){
      return '<tr data-go="' + p.id + '" style="cursor:pointer"><td>' + p.id + '</td><td>' + p.len + '</td><td>' + esc(p.text) + '</td></tr>'; }).join('') + '</tbody>'
      + (S.length > 200 ? '<tbody><tr><td colspan="3">Showing the 200 longest of ' + S.length + ' passages.</td></tr></tbody>' : '')
      : '<tbody><tr><td>No matching passages of ' + n + ' or more words.</td></tr></tbody>';
    last = {copy: copy, used: used, over: over, longest: longest, n: n, words: Bt.length, P: S};
  }
  function go(id){
    ['siViewA', 'siViewB'].forEach(function(v){
      var box = $(v), m = box.querySelector('mark[data-m="' + id + '"]');
      if (!m) return;
      box.scrollTop = m.offsetTop - box.offsetTop - 40;
      m.style.outline = '2px solid #e0442c'; setTimeout(function(){ m.style.outline = ''; }, 1500);
    });
  }
  $('siOut').addEventListener('click', function(ev){ var r = ev.target.closest('[data-go]'); if (r) go(r.getAttribute('data-go')); });
  ['siA', 'siB'].forEach(function(i){ $(i).addEventListener('input', run); });
  $('siN').addEventListener('change', run);
  $('siSwap').onclick = function(){ var t = $('siA').value; $('siA').value = $('siB').value; $('siB').value = t; run(); };
  $('siRep').onclick = function(){ if (!last) return; copyText('Text similarity check (matches of ' + last.n + '+ words)\nCopied in text to check: ' + last.copy + '%\nOriginal reused: ' + last.used + '%\nWord overlap: ' + last.over + '%\nLongest match: ' + last.longest + ' words\n\n' + last.P.slice(0, 50).map(function(p){ return '[' + p.len + ' words] ' + p.text; }).join('\n'), 'toast'); };
  run();
''',
        content=f'''
    <h2>What Is a Text Similarity Checker?</h2>
    <p>A text similarity checker compares two pieces of text and shows how much of the second one was copied from the first. It finds every passage the two texts share word for word, highlights it in both, and turns the result into a simple copied share.</p>
    <p>It is the quickest way to answer questions like these: did the AI rewrite really change my source, or just swap a few words? Did a guest writer copy my article? How close is a competitor page to mine? Is this essay too close to the reading it was based on?</p>
    <p>Unlike a web plagiarism checker, it does not search the internet. You paste both texts, so it works on drafts, private documents and pages that are not online yet, with no word limit.</p>

    <h2>How to Use the Text Similarity Checker</h2>
    <ol>
      <li><strong>Paste the original</strong> in the first box, such as your source article or the page you suspect was copied.</li>
      <li><strong>Paste the text to check</strong> in the second box, such as the AI rewrite, guest post or competitor copy.</li>
      <li><strong>Pick the shortest match.</strong> Five words is a good default. Three words is strict and catches more, eight words only flags long copied runs.</li>
      <li><strong>Read the scores and highlights.</strong> Matching passages are marked in both texts. Click a row in the table to jump to it.</li>
      <li><strong>Copy the report</strong> to share the numbers and the longest passages with a writer, client or teacher.</li>
    </ol>

    <h2>What the Numbers Mean</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Score', 'What it measures', 'How to read it')}
      <tbody>
        <tr><td>Copied in text to check</td><td>Share of words in the second text that sit inside a matching passage</td><td>The main score. Under 10% is original, 10 to 30% has some copying, over 30% is a reword.</td></tr>
        <tr><td>Original reused</td><td>Share of the original that appears in the second text</td><td>High when a short text lifts most of a long one, even if the copied share looks small.</td></tr>
        <tr><td>Word overlap</td><td>Shared meaningful words, ignoring words like the and of</td><td>High overlap with few long matches often means a synonym swap that kept the same ideas and order.</td></tr>
        <tr><td>Longest match</td><td>The longest run of identical words</td><td>A run of 20 or more words is almost never a coincidence.</td></tr>
      </tbody>
    </table></div>
    <p>Matching ignores capital letters, punctuation and line breaks, so a copied sentence still counts after small edits around it. The bands above are guides, not rules. Quotes, names, product specs and legal text will always match, and that is fine when they are credited.</p>

    <h2>Why Copied and Lightly Reworded Text Matters</h2>
    <p>Google's <a href="https://developers.google.com/search/docs/essentials/spam-policies" {EXT}>spam policies</a> list scraped content as spam, including pages that copy content from other sites and change it only slightly, for example by swapping synonyms or using automated tools. Google's <a href="https://developers.google.com/search/docs/fundamentals/using-gen-ai-content" {EXT}>guidance on AI content</a> says using AI is fine when the result is helpful and original. So an AI rewrite that keeps most of the source is a risk, not a shortcut.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Rewrite from notes, not from the page.</strong> Close the source, write from your own outline, then check here. The copied share drops fast.</li>
      <li><strong>Add what the source lacks.</strong> Your own example, numbers or opinion makes the page original in a way no word swap can.</li>
      <li><strong>Quote on purpose.</strong> When you need the exact words, use quote marks and link the source.</li>
      <li><strong>Check your own pages too.</strong> Two of your pages with a high score compete with each other. Merge them or point one to the other with a canonical tag.</li>
    </ul>

    <h2>Keep Your Content Original</h2>
    <p>Learn what Google expects in our guide to <a href="{B}google-ai-content-guidelines-2026/">Google's AI content guidelines</a>, reuse your own work the right way with <a href="{B}repurpose-blog-content-maximum-reach/">how to repurpose blog content</a>, and handle duplicate pages with <a href="{B}what-is-canonical-tag/">what is a canonical tag</a>. Then strip the ChatGPT tone from your rewrite with the <a href="{T}ai-words-checker/">AI words checker</a>, or see every single edit line by line in the <a href="{DV}diff-checker/">diff checker</a>.</p>
''',
        faqs=[
            ("How do I check if two texts are plagiarized?", "Paste the original in the first box and the text you suspect in the second. The checker finds every passage of five or more identical words, highlights them in both texts and shows what share of the second text was copied. Over 30% usually means it is a reword rather than an original piece."),
            ("Does this tool search the internet for copies?", "No. It compares only the two texts you paste. That makes it useful for private drafts and AI rewrites, but to find copies of your page across the web you need a web search or a paid plagiarism checker."),
            ("Can it catch AI paraphrasing or synonym swaps?", "Partly. Light rewrites keep many runs of identical words, which show up as matches. When a tool swaps nearly every word, the copied share falls, but word overlap stays high. A low copied share with high overlap is a sign to read the text side by side."),
            ("Is my text uploaded anywhere?", "No. The comparison runs entirely in your browser. Neither text is sent to us, to an AI model or to anyone else, so it is safe for client work, unpublished drafts and student papers."),
        ],
        related=[("Google AI Content Guidelines 2026", "google-ai-content-guidelines-2026"), ("What Is a Canonical Tag", "what-is-canonical-tag"),
                 ("Repurpose Blog Content for Maximum Reach", "repurpose-blog-content-maximum-reach"), ("25 Content Writing Mistakes", "25-content-writing-mistakes")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-17'
