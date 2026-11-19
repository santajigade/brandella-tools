"""Batch 2 (2026-10-28): 7 more SEO tools. Completes the SEO Tools category (12 tools)."""

def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 6. READABILITY SCORE CHECKER ----------
    TOOLS.append(dict(
        slug='readability-score-checker', short='RS', name='Readability Score Checker',
        card='Get a Flesch reading ease score and grade level, plus long sentences and passive voice flagged.',
        title='Readability Score Checker: Free Flesch Reading Ease Test',
        desc='Free readability score checker. Get your Flesch reading ease score and grade level, and find long sentences, passive voice and complex words.',
        h1='Readability Score Checker',
        lead='Paste your content to get a Flesch reading ease score, a grade level, and a list of the exact sentences that make your writing harder to read.',
        tool=r'''<section class="tool" aria-label="Readability score checker">
    <div class="card">
      <h2>Paste Your Content</h2>
      <div class="field">
        <label for="rsText">Text <em id="rsChars">0 words</em></label>
        <textarea id="rsText" class="big">Readability matters because people skim. Short sentences and familiar words help readers find answers fast. When a page is easy to read, visitors stay longer and understand more.

The optimization of content readability is frequently overlooked by writers who are focused primarily on the inclusion of keywords, which results in paragraphs that are technically comprehensive but are considerably more difficult for the average visitor to process and remember. Mistakes were made in many drafts.

Read your draft out loud. If you run out of breath, the sentence is too long.</textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn" id="rsClear">Clear</button>
      </div>
      <div class="tips"><strong>Targets for web content</strong><ul>
        <li>Reading ease of 60 or higher</li><li>Grade level 8 or lower</li><li>Average sentence under 20 words</li><li>Passive voice in under 10% of sentences</li></ul></div>
    </div>

    <div class="card">
      <h2>Readability Results</h2>
      <div class="stats">
        <div class="stat-box"><b id="rsScore">0</b><span>Reading Ease</span></div>
        <div class="stat-box"><b id="rsGrade">0</b><span>Grade Level</span></div>
        <div class="stat-box"><b id="rsAvg">0</b><span>Words per Sentence</span></div>
        <div class="stat-box"><b id="rsComplex">0%</b><span>Complex Words</span></div>
      </div>
      <div class="kw-result" id="rsVerdict">Paste text to see its readability.</div>
      <div class="chips" id="rsChips"></div>
      <div id="rsLong"></div>
    </div>
  </section>''',
        js=r'''
  function syl(w){
    w = w.toLowerCase().replace(/[^a-z]/g,'');
    if (!w) return 0; if (w.length <= 3) return 1;
    w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');
    var m = w.match(/[aeiouy]{1,2}/g); return m ? m.length : 1;
  }
  var PASSIVE = /\b(am|is|are|was|were|be|been|being|get|gets|got)\s+(\w+ly\s+)?(\w+ed|\w+en|made|done|built|written|known|seen|given|taken|found|sent|kept|held|left|paid|put|set|told|thought|brought|bought|caught|taught|sold|shown|chosen)\b/i;
  function label(s){
    if (s >= 90) return ['Very easy','ok']; if (s >= 80) return ['Easy','ok']; if (s >= 70) return ['Fairly easy','ok'];
    if (s >= 60) return ['Plain English','ok']; if (s >= 50) return ['Fairly difficult','warn']; if (s >= 30) return ['Difficult','bad']; return ['Very difficult','bad'];
  }
  function run(){
    var txt = $('rsText').value.replace(/\s+/g,' ').trim();
    var sents = (txt.match(/[^.!?]+[.!?]*/g) || []).map(function(s){ return s.trim(); }).filter(function(s){ return /[a-z0-9]/i.test(s); });
    var words = txt.match(/[A-Za-z0-9']+/g) || [];
    $('rsChars').textContent = words.length + ' words';
    if (!words.length){
      ['rsScore','rsGrade','rsAvg'].forEach(function(id){ $(id).textContent='0'; }); $('rsComplex').textContent='0%';
      $('rsVerdict').className='kw-result'; $('rsVerdict').textContent='Paste text to see its readability.'; $('rsChips').innerHTML=''; $('rsLong').innerHTML=''; return;
    }
    var sylls = 0, complex = 0, adverbs = 0;
    words.forEach(function(w){ var s = syl(w); sylls += s; if (s >= 3) complex++; if (/ly$/i.test(w) && w.length > 4) adverbs++; });
    var wps = words.length / Math.max(1, sents.length), spw = sylls / words.length;
    var ease = Math.max(0, Math.min(100, 206.835 - 1.015*wps - 84.6*spw));
    var grade = Math.max(0, 0.39*wps + 11.8*spw - 15.59);
    $('rsScore').textContent = ease.toFixed(0);
    $('rsGrade').textContent = grade.toFixed(1);
    $('rsAvg').textContent = wps.toFixed(1);
    $('rsComplex').textContent = (complex/words.length*100).toFixed(0) + '%';
    var l = label(ease);
    $('rsVerdict').className = 'kw-result ' + l[1];
    $('rsVerdict').innerHTML = '<strong>' + l[0] + '.</strong> ' + (ease >= 60 ? 'Most adults can read this comfortably.' : 'Try shorter sentences and simpler words to reach 60 or higher.');
    var longS = sents.filter(function(s){ return (s.match(/[A-Za-z0-9']+/g)||[]).length > 20; });
    var passS = sents.filter(function(s){ return PASSIVE.test(s); });
    $('rsChips').innerHTML = '<span class="chip">Sentences: ' + sents.length + '</span><span class="chip">Long sentences: ' + longS.length + '</span><span class="chip">Passive: ' + passS.length + '</span><span class="chip">Adverbs: ' + adverbs + '</span>';
    var html = '';
    if (longS.length) html += '<div class="tips" style="border-left-color:#f0a020;background:#fff6e5"><strong>Long sentences (over 20 words)</strong><ul>' + longS.map(function(s){ return '<li>' + esc(s) + ' <em style="color:#c47a00">(' + (s.match(/[A-Za-z0-9']+/g)||[]).length + ' words)</em></li>'; }).join('') + '</ul></div>';
    if (passS.length) html += '<div class="tips" style="border-left-color:#e0442c;background:#fdecea"><strong>Possible passive voice</strong><ul>' + passS.map(function(s){ return '<li>' + esc(s).replace(PASSIVE, function(m){ return '<strong>' + m + '</strong>'; }) + '</li>'; }).join('') + '</ul></div>';
    if (!html) html = '<div class="tips"><strong>No long sentences or passive voice found.</strong></div>';
    $('rsLong').innerHTML = html;
  }
  $('rsText').addEventListener('input', run);
  $('rsClear').onclick = function(){ $('rsText').value=''; run(); $('rsText').focus(); };
  run();
''',
        content=r'''
    <h2>What Is a Readability Score?</h2>
    <p>A readability score estimates how easy a piece of text is to read, based on sentence length and word length.</p>
    <p>This readability score checker uses the Flesch reading ease formula, one of the most widely used tests, along with the Flesch Kincaid grade level.</p>

    <h2>How to Read Your Score</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Reading Ease</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Meaning</th></tr></thead>
      <tbody>
        <tr><td>90 to 100</td><td>Very easy, understood by an 11 year old</td></tr>
        <tr><td>70 to 89</td><td>Easy to fairly easy, ideal for most blogs</td></tr>
        <tr><td>60 to 69</td><td>Plain English, a good target for web content</td></tr>
        <tr><td>30 to 59</td><td>Difficult, closer to academic writing</td></tr>
        <tr><td>0 to 29</td><td>Very difficult, best kept for specialist readers</td></tr>
      </tbody>
    </table>
    <p>The grade level shows roughly how many years of schooling a reader needs. For general web content, aim for grade 8 or below.</p>

    <h2>How to Use This Tool</h2>
    <ol>
      <li><strong>Paste your draft.</strong> Plain text works best. Remove menus or footer text if you copied a whole page.</li>
      <li><strong>Check the score and grade.</strong> The verdict tells you whether the text is comfortable for most readers.</li>
      <li><strong>Fix the flagged sentences.</strong> Long sentences and possible passive voice are listed so you can edit them directly.</li>
    </ol>

    <h2>Does Readability Affect SEO?</h2>
    <p>Google does not use a readability formula as a ranking factor. But clear writing helps people find answers quickly, and pages that satisfy readers tend to perform better over time.</p>
    <p>Easy to read content is also easier for AI assistants to quote accurately, which matters more as answers appear directly in search.</p>

    <h2>Quick Ways to Improve Readability</h2>
    <ul>
      <li>Split long sentences into two.</li>
      <li>Swap long words for short, common ones.</li>
      <li>Use active voice: "We updated the guide" instead of "The guide was updated".</li>
      <li>Keep paragraphs to one or two sentences on the web.</li>
      <li>Use subheadings and lists so readers can scan.</li>
    </ul>
    <p>For more, read our guides on <a href="https://brandella.in/10-easy-tips-for-effective-content-writing/">effective content writing</a> and <a href="https://brandella.in/25-content-writing-mistakes/">common content writing mistakes</a>. You can also count words and reading time with our <a href="https://brandella.in/tools/seo-tools/word-character-counter/">word and character counter</a>.</p>
''',
        faqs=[
            ("What is a good Flesch reading ease score?", "For most websites, a score of 60 or higher is a good target. Scores between 60 and 70 read as plain English, and anything above 70 is easy for most adults."),
            ("How is the Flesch reading ease score calculated?", "It uses average sentence length and average syllables per word: 206.835 minus 1.015 times words per sentence, minus 84.6 times syllables per word. Shorter sentences and shorter words raise the score."),
            ("Is the passive voice detection exact?", "It is an estimate based on common patterns such as a form of 'to be' followed by a past participle. Treat flagged sentences as suggestions to review, not definite errors."),
            ("Does this readability score checker store my text?", "No. It runs entirely in your browser, so your text is never uploaded or saved."),
        ],
        related=[("Effective Content Writing Tips", "10-easy-tips-for-effective-content-writing"), ("25 Content Writing Mistakes", "25-content-writing-mistakes"),
                 ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("E E A T Explained", "eeat-experience-expertise-authority-trust")],
    ))

    # ---------- 7. KEYWORD COMBINER ----------
    TOOLS.append(dict(
        slug='keyword-combiner', short='KC', name='Keyword Combiner',
        card='Mix up to three keyword lists into every combination, with broad, phrase and exact match output.',
        title='Keyword Combiner: Free Keyword Mixer for SEO and Google Ads',
        desc='Free keyword combiner. Mix up to three keyword lists into every combination and export as broad, phrase or exact match for Google Ads.',
        h1='Keyword Combiner',
        lead='Combine up to three keyword lists into every possible variation in seconds, ready for keyword research or Google Ads with match types applied.',
        tool=r'''<section class="tool" aria-label="Keyword combiner">
    <div class="card">
      <h2>Enter Keyword Lists</h2>
      <div class="row2">
        <div class="field">
          <label for="kcA">List 1 <em>one per line</em></label>
          <textarea id="kcA">buy
best
cheap</textarea>
        </div>
        <div class="field">
          <label for="kcB">List 2</label>
          <textarea id="kcB">running shoes
trail shoes</textarea>
        </div>
      </div>
      <div class="field">
        <label for="kcC">List 3 <em>optional</em></label>
        <textarea id="kcC" style="min-height:70px">online
in pune</textarea>
      </div>
      <label class="check"><input id="kcPairs" type="checkbox" checked> Also include two list combinations (1+2, 1+3, 2+3)</label>
      <p style="font-weight:700;font-size:14.5px;margin:12px 0 6px">Match types</p>
      <label class="check"><input id="kcBroad" type="checkbox" checked> Broad (keyword)</label>
      <label class="check"><input id="kcPhrase" type="checkbox"> Phrase ("keyword")</label>
      <label class="check"><input id="kcExact" type="checkbox"> Exact ([keyword])</label>
    </div>

    <div class="card">
      <h2>Combined Keywords <span id="kcCount" style="color:#3d8f12"></span></h2>
      <div class="field">
        <textarea id="kcOut" class="big mono" readonly></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="kcCopy">Copy All</button>
        <button class="btn" id="kcCsv">Download CSV</button>
        <button class="btn" id="kcClear">Clear</button>
        <span class="toast" id="toast">Copied!</span>
      </div>
    </div>
  </section>''',
        js=r'''
  function list(id){ var seen = {}; return $(id).value.split('\n').map(function(x){ return x.trim().replace(/\s+/g,' '); }).filter(function(x){ if (!x || seen[x.toLowerCase()]) return false; seen[x.toLowerCase()] = 1; return true; }); }
  function cross(a, b){ var o = []; a.forEach(function(x){ b.forEach(function(y){ o.push(x + ' ' + y); }); }); return o; }
  var result = [];
  function run(){
    var A = list('kcA'), B = list('kcB'), C = list('kcC'), combos = [];
    var lists = [A, B, C].filter(function(l){ return l.length; });
    if (lists.length >= 2) combos = lists.slice(1).reduce(function(acc, l){ return cross(acc, l); }, lists[0]);
    if ($('kcPairs').checked && A.length && B.length && C.length){ combos = combos.concat(cross(A,B), cross(A,C), cross(B,C)); }
    var seen = {}; combos = combos.filter(function(k){ var l = k.toLowerCase(); if (seen[l]) return false; seen[l] = 1; return true; });
    result = [];
    combos.forEach(function(k){
      if ($('kcBroad').checked) result.push(k);
      if ($('kcPhrase').checked) result.push('"' + k + '"');
      if ($('kcExact').checked) result.push('[' + k + ']');
    });
    $('kcOut').value = result.join('\n');
    $('kcCount').textContent = result.length ? '(' + result.length + ')' : '';
  }
  ['kcA','kcB','kcC'].forEach(function(id){ $(id).addEventListener('input', run); });
  ['kcPairs','kcBroad','kcPhrase','kcExact'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('kcCopy').onclick = function(){ copyText(result.join('\n'), 'toast'); };
  $('kcCsv').onclick = function(){
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob(['Keyword\n' + result.map(function(k){ return '"' + k.replace(/"/g,'""') + '"'; }).join('\n')], {type:'text/csv'}));
    a.download = 'keyword-combinations.csv'; a.click();
  };
  $('kcClear').onclick = function(){ ['kcA','kcB','kcC'].forEach(function(id){ $(id).value=''; }); run(); $('kcA').focus(); };
  run();
''',
        content=r'''
    <h2>What Is a Keyword Combiner?</h2>
    <p>A keyword combiner, sometimes called a keyword mixer, takes two or three lists of words and joins them into every possible combination.</p>
    <p>Instead of typing out "buy running shoes", "best running shoes", "cheap trail shoes" and dozens more by hand, you enter each part once and get the full list instantly.</p>

    <h2>How to Use This Keyword Combiner</h2>
    <ol>
      <li><strong>List 1:</strong> modifiers such as buy, best, cheap, or review.</li>
      <li><strong>List 2:</strong> your core products or services.</li>
      <li><strong>List 3 (optional):</strong> locations or qualifiers like online, near me, or a city name.</li>
      <li><strong>Choose match types</strong> if you are building a Google Ads campaign, then copy or download the list.</li>
    </ol>
    <p>Duplicates are removed automatically, and the counter shows exactly how many keywords you will get.</p>

    <h2>Using It for Google Ads</h2>
    <p>Google Ads uses three keyword match types:</p>
    <ul>
      <li><strong>Broad match</strong> (no symbols) reaches the widest range of related searches.</li>
      <li><strong>Phrase match</strong> ("in quotes") shows ads for searches that include the meaning of your phrase.</li>
      <li><strong>Exact match</strong> ([in brackets]) targets searches with the same meaning as the keyword.</li>
    </ul>
    <p>Tick the match types you need and paste the output straight into Google Ads Editor or the keyword planner. Pair it with a solid list of <a href="https://brandella.in/google-ads-negative-keywords/">Google Ads negative keywords</a> so the extra coverage does not waste budget.</p>

    <h2>Using It for SEO Research</h2>
    <p>Combined keywords are not a final keyword list. They are seeds. Paste them into a keyword research tool to check search volume and difficulty, then keep only the terms people actually search for.</p>
    <p>Our guide to <a href="https://brandella.in/search-volume-vs-keyword-difficulty/">search volume vs keyword difficulty</a> explains how to choose between them. When your list gets messy, clean it with the <a href="https://brandella.in/tools/seo-tools/duplicate-line-remover/">duplicate line and keyword cleaner</a>.</p>
''',
        faqs=[
            ("How many keyword combinations can I create?", "There is no fixed limit. The keyword combiner runs in your browser, so it comfortably handles thousands of combinations. Very large lists may take a moment to display."),
            ("What is the difference between broad, phrase and exact match?", "Broad match reaches the widest range of related searches, phrase match requires the meaning of your phrase, and exact match targets searches with the same meaning as the keyword."),
            ("Should I use every combination in my campaign?", "No. Use the list as a starting point, then check search volume and remove combinations nobody searches for or that do not fit your offer."),
            ("Is this keyword combiner free?", "Yes. It is completely free, needs no signup, and nothing you enter is uploaded."),
        ],
        related=[("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("Search Volume vs Keyword Difficulty", "search-volume-vs-keyword-difficulty"),
                 ("Best Keyword Research Tools Compared", "best-keyword-research-tools-compared"), ("Python Keyword Research Automation", "python-keyword-research-automation")],
    ))

    # ---------- 8. ALT TEXT CHECKER ----------
    TOOLS.append(dict(
        slug='alt-text-checker', short='AT', name='Alt Text Checker',
        card='Paste page HTML to find images with missing, empty, too long or filename style alt text.',
        title='Alt Text Checker: Find Missing and Weak Image Alt Text',
        desc='Free alt text checker. Paste page HTML to find images with missing, empty, too long or filename style alt text, for better image SEO.',
        h1='Alt Text Checker',
        lead='Paste your page HTML and instantly see every image, its alt text, and which ones are missing, empty, too long or just a file name.',
        tool=r'''<section class="tool" aria-label="Alt text checker">
    <div class="card">
      <h2>Paste Page HTML</h2>
      <div class="field">
        <label for="atText">HTML Source <em id="atChars">0 chars</em></label>
        <textarea id="atText" class="big mono" placeholder="Paste the full HTML of your page here..."></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="atSample">Load Sample</button>
        <button class="btn" id="atClear">Clear</button>
      </div>
      <div class="tips"><strong>Good alt text</strong><ul>
        <li>Describes what the image shows</li><li>Usually under 125 characters</li><li>Uses empty alt only for decorative images</li><li>Includes a keyword only when it fits naturally</li></ul></div>
    </div>

    <div class="card">
      <h2>Image Report</h2>
      <div class="chips" id="atChips"></div>
      <div class="kw-result" id="atSummary">Paste HTML to check image alt text.</div>
      <div id="atTable"></div>
    </div>
  </section>''',
        js=r'''
  var SAMPLE = '<img src="/uploads/team-photo.jpg" alt="Brandella team at the Pune office">\n<img src="/uploads/IMG_4021.jpg">\n<img src="/uploads/divider.png" alt="">\n<img src="/uploads/chart.png" alt="chart.png">\n<img src="/uploads/seo.jpg" alt="Image of SEO">\n<img src="/uploads/hero.webp" alt="A marketer reviewing a Google Search Console performance report on a laptop, with charts showing clicks, impressions and average position over the last three months">';
  function fname(src){ if (!src) return '(no src)'; var s = src.split('?')[0].split('#')[0]; return s.substring(s.lastIndexOf('/') + 1) || s; }
  function check(img){
    var has = img.hasAttribute('alt'), alt = (img.getAttribute('alt') || '').trim(), out = [];
    if (!has) return [['bad','Missing alt attribute']];
    if (!alt) return [['warn','Empty alt (fine only for decorative images)']];
    if (alt.length > 125) out.push(['warn','Long (' + alt.length + ' chars)']);
    if (/\.(jpe?g|png|gif|webp|avif|svg)$/i.test(alt) || /^(img|dsc|image|photo|screenshot)[\s_]?\d+/i.test(alt) || /_/.test(alt)) out.push(['bad','Looks like a file name']);
    if (/^(image|picture|photo|graphic) of\b/i.test(alt)) out.push(['warn','Starts with "image of"']);
    if (alt.split(/\s+/).length < 2 && alt.length < 12) out.push(['warn','Very short']);
    return out.length ? out : [['ok','Good']];
  }
  function run(){
    var raw = $('atText').value; $('atChars').textContent = raw.length + ' chars';
    var imgs = Array.prototype.slice.call(new DOMParser().parseFromString(raw, 'text/html').querySelectorAll('img'));
    var box = $('atSummary');
    if (!raw.trim()){ box.className='kw-result'; box.textContent='Paste HTML to check image alt text.'; $('atChips').innerHTML=''; $('atTable').innerHTML=''; return; }
    if (!imgs.length){ box.className='kw-result warn'; box.textContent='No images found in this HTML.'; $('atChips').innerHTML=''; $('atTable').innerHTML=''; return; }
    var res = imgs.map(check), counts = {missing:0, empty:0, issues:0, good:0}, altSeen = {};
    var rows = imgs.map(function(img, i){
      var alt = (img.getAttribute('alt') || '').trim(), r = res[i];
      if (alt && altSeen[alt.toLowerCase()]) r = r.filter(function(x){ return x[0] !== 'ok'; }).concat([['warn','Duplicate alt text']]);
      if (alt) altSeen[alt.toLowerCase()] = 1;
      res[i] = r;
      if (!img.hasAttribute('alt')) counts.missing++; else if (!alt) counts.empty++; else if (r[0][0] === 'ok') counts.good++; else counts.issues++;
      var color = r.some(function(x){ return x[0]==='bad'; }) ? '#d1351f' : (r[0][0]==='ok' ? '#3d8f12' : '#c47a00');
      return '<tr><td>' + (i+1) + '</td><td style="word-break:break-all">' + esc(fname(img.getAttribute('src'))) + '</td><td>' + (img.hasAttribute('alt') ? (alt ? esc(alt) : '<em style="color:#999">(empty)</em>') : '<em style="color:#999">(none)</em>') + '</td><td style="color:' + color + ';font-weight:700;font-size:13px">' + r.map(function(x){ return esc(x[1]); }).join('<br>') + '</td></tr>';
    });
    $('atChips').innerHTML = '<span class="chip">Images: ' + imgs.length + '</span><span class="chip">Good: ' + counts.good + '</span><span class="chip">Missing: ' + counts.missing + '</span><span class="chip">Empty: ' + counts.empty + '</span><span class="chip">Needs work: ' + counts.issues + '</span>';
    var problems = counts.missing + counts.issues;
    box.className = 'kw-result ' + (counts.missing ? 'bad' : (problems || counts.empty ? 'warn' : 'ok'));
    box.innerHTML = problems ? '<strong>' + problems + ' image' + (problems===1?'':'s') + ' need attention.</strong> ' + (counts.empty ? counts.empty + ' empty alt values are fine only if those images are decorative.' : '') : '<strong>Looks good.</strong> Every image has descriptive alt text.' + (counts.empty ? ' Check the ' + counts.empty + ' empty alt values are decorative.' : '');
    $('atTable').innerHTML = '<div style="overflow-x:auto"><table class="rtable"><thead><tr><th>#</th><th>Image</th><th>Alt Text</th><th>Status</th></tr></thead><tbody>' + rows.join('') + '</tbody></table></div>';
  }
  $('atText').addEventListener('input', run);
  $('atSample').onclick = function(){ $('atText').value = SAMPLE; run(); };
  $('atClear').onclick = function(){ $('atText').value=''; run(); $('atText').focus(); };
  $('atText').value = SAMPLE; run();
''',
        content=r'''
    <h2>What Is Alt Text?</h2>
    <p>Alt text is the short description inside an image's <code>alt</code> attribute. Screen readers read it aloud, browsers show it when an image fails to load, and search engines use it to understand what the image shows.</p>
    <p>Good alt text makes your pages more accessible and helps your images appear in Google Images.</p>

    <h2>How to Use This Alt Text Checker</h2>
    <ol>
      <li><strong>Copy your page HTML.</strong> In Chrome press Ctrl + U, then select all and copy. Pasting just your article HTML also works.</li>
      <li><strong>Paste it into the box.</strong> Every image is listed with its file name and alt text.</li>
      <li><strong>Fix anything marked red or orange.</strong> The status column explains exactly what is wrong.</li>
    </ol>

    <h2>What the Checker Flags</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Issue</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Why It Matters</th></tr></thead>
      <tbody>
        <tr><td>Missing alt attribute</td><td>Screen readers may read out the file name instead</td></tr>
        <tr><td>Empty alt</td><td>Correct for decorative images, a problem for meaningful ones</td></tr>
        <tr><td>File name as alt</td><td>"IMG_4021.jpg" tells nobody what the image shows</td></tr>
        <tr><td>Starts with "image of"</td><td>Screen readers already announce it as an image</td></tr>
        <tr><td>Over 125 characters</td><td>Hard to listen to, and often keyword stuffed</td></tr>
        <tr><td>Duplicate alt text</td><td>Different images usually deserve different descriptions</td></tr>
      </tbody>
    </table>

    <h2>How to Write Better Alt Text</h2>
    <ul>
      <li>Describe the image as you would to someone on the phone.</li>
      <li>Be specific: "Bar chart of monthly organic traffic rising from 2,000 to 9,000" beats "chart".</li>
      <li>Use a keyword only when it genuinely describes the image.</li>
      <li>Leave alt empty for purely decorative images like dividers and background shapes.</li>
    </ul>
    <p>For the full picture on image SEO, read <a href="https://brandella.in/optimize-images-for-seo-without-losing-quality/">how to optimize images for SEO</a>, <a href="https://brandella.in/lazy-loading-images-explained-lcp-seo/">lazy loading images explained</a>, and <a href="https://brandella.in/webp-vs-avif-image-format-seo/">WebP vs AVIF</a>. To check headings on the same page, try the <a href="https://brandella.in/tools/seo-tools/heading-structure-checker/">heading structure checker</a>.</p>
''',
        faqs=[
            ("Does alt text help SEO?", "Yes. Google uses alt text, along with the page content and file name, to understand images. Descriptive alt text helps images rank in Google Images and makes the page more accessible."),
            ("How long should alt text be?", "Keep it concise, usually under 125 characters. Describe what matters in the image without stuffing keywords."),
            ("When should alt text be empty?", "Use an empty alt attribute for purely decorative images such as dividers, spacers or background shapes, so screen readers skip them."),
            ("Does this alt text checker upload my HTML?", "No. The alt text checker works entirely in your browser and never uploads or stores what you paste."),
        ],
        related=[("Optimize Images for SEO", "optimize-images-for-seo-without-losing-quality"), ("Lazy Loading Images Explained", "lazy-loading-images-explained-lcp-seo"),
                 ("WebP vs AVIF for SEO", "webp-vs-avif-image-format-seo"), ("HTML Semantic Elements Explained", "html-semantic-elements-explained")],
    ))

    # ---------- 9. INTERNAL LINK CHECKER ----------
    TOOLS.append(dict(
        slug='internal-link-checker', short='IL', name='Internal Link Checker',
        card='List every link on a page, split internal from external, and flag generic or empty anchor text.',
        title='Internal Link Checker: Free Anchor Text and Link Analyzer',
        desc='Free internal link checker. Paste page HTML to list every internal and external link, and flag generic anchors, empty anchors and nofollow issues.',
        h1='Internal Link Checker',
        lead='Paste a page\'s HTML to see every internal and external link, the anchor text used, and which links need attention.',
        tool=r'''<section class="tool" aria-label="Internal link checker">
    <div class="card" style="min-width:0">
      <h2>Paste Page HTML</h2>
      <div class="field">
        <label for="ilDomain">Your Domain</label>
        <input id="ilDomain" type="text" value="brandella.in">
      </div>
      <div class="field">
        <label for="ilText">HTML Source <em id="ilChars">0 chars</em></label>
        <textarea id="ilText" class="big mono" placeholder="Paste the full HTML of your page here..."></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="ilSample">Load Sample</button>
        <button class="btn" id="ilClear">Clear</button>
      </div>
      <div class="tips"><strong>Tip</strong><ul><li>Paste only the article HTML to skip menu and footer links.</li></ul></div>
    </div>

    <div class="card" style="min-width:0">
      <h2>Link Report</h2>
      <div class="stats">
        <div class="stat-box"><b id="ilTotal">0</b><span>Links</span></div>
        <div class="stat-box"><b id="ilInt">0</b><span>Internal</span></div>
        <div class="stat-box"><b id="ilExt">0</b><span>External</span></div>
        <div class="stat-box"><b id="ilIss">0</b><span>Issues</span></div>
      </div>
      <div class="tabs" role="tablist" id="ilTabs">
        <button class="on" data-f="all">All</button>
        <button data-f="internal">Internal</button>
        <button data-f="external">External</button>
        <button data-f="issues">Issues</button>
      </div>
      <div id="ilTable"></div>
    </div>
  </section>''',
        js=r'''
  var SAMPLE = '<p>Start with our <a href="/what-is-seo/">beginner guide to SEO</a>, then learn about <a href="https://brandella.in/internal-linking-best-practices-seo-rankings/">internal linking best practices</a>.</p>\n<p>For more details <a href="/link-equity-explained/">click here</a>.</p>\n<p>Google explains this in <a href="https://developers.google.com/search/docs" target="_blank">its documentation</a>.</p>\n<p><a href="/title-tag-optimization/" rel="nofollow">Title tag optimization</a></p>\n<p><a href="/what-is-seo/"><img src="seo.png"></a> <a href="#faq">Jump to FAQ</a> <a href="mailto:hello@brandella.in">Email us</a></p>\n<p><a href="http://brandella.in/old-page/">read more</a></p>';
  var GENERIC = /^(click here|here|read more|more|learn more|this|this link|link|go|continue|details|more info|this page|website)$/i;
  var data = [], filter = 'all';
  function host(h){ return h.replace(/^www\./,'').toLowerCase(); }
  function run(){
    var raw = $('ilText').value; $('ilChars').textContent = raw.length + ' chars';
    var dom = host($('ilDomain').value.trim().replace(/^https?:\/\//,'').replace(/\/.*$/,'') || 'example.com');
    var doc = new DOMParser().parseFromString(raw, 'text/html'), counts = {};
    data = Array.prototype.slice.call(doc.querySelectorAll('a[href]')).map(function(a){
      var href = a.getAttribute('href').trim(), type, url = href, issues = [];
      var text = a.textContent.replace(/\s+/g,' ').trim();
      if (!text){ var im = a.querySelector('img'); text = im && im.getAttribute('alt') ? '[image: ' + im.getAttribute('alt') + ']' : ''; }
      if (/^#/.test(href)) type = 'anchor';
      else if (/^(mailto|tel|sms):/i.test(href)) type = 'contact';
      else if (/^javascript:/i.test(href)) type = 'script';
      else {
        try { var u = new URL(href, 'https://' + dom + '/'); url = u.href; type = host(u.hostname) === dom ? 'internal' : 'external';
          if (u.protocol === 'http:') issues.push('Uses http, not https'); } catch(e){ type = 'external'; issues.push('Invalid URL'); }
      }
      var rel = (a.getAttribute('rel') || '').toLowerCase();
      if (!text) issues.push('Empty anchor text');
      else if (GENERIC.test(text)) issues.push('Generic anchor text');
      if (type === 'internal' && /nofollow/.test(rel)) issues.push('Nofollow on an internal link');
      if (type === 'external' && a.getAttribute('target') === '_blank' && !/noopener|noreferrer/.test(rel)) issues.push('New tab without rel noopener');
      counts[url] = (counts[url] || 0) + 1;
      return { text: text, url: url, type: type, rel: rel, issues: issues };
    });
    data.forEach(function(d){ d.times = counts[d.url]; });
    $('ilTotal').textContent = data.length;
    $('ilInt').textContent = data.filter(function(d){ return d.type==='internal'; }).length;
    $('ilExt').textContent = data.filter(function(d){ return d.type==='external'; }).length;
    $('ilIss').textContent = data.filter(function(d){ return d.issues.length; }).length;
    table();
  }
  function table(){
    var rows = data.filter(function(d){ return filter==='all' || (filter==='issues' ? d.issues.length : d.type===filter); });
    if (!$('ilText').value.trim()){ $('ilTable').innerHTML = '<p class="empty">Paste HTML to list its links.</p>'; return; }
    if (!rows.length){ $('ilTable').innerHTML = '<p class="empty">No links in this view.</p>'; return; }
    $('ilTable').innerHTML = '<div style="overflow-x:auto;max-height:520px"><table class="rtable"><thead><tr><th>Anchor Text</th><th>URL</th><th>Type</th><th>Notes</th></tr></thead><tbody>' + rows.map(function(d){
      return '<tr><td>' + (d.text ? esc(d.text) : '<em style="color:#999">(empty)</em>') + '</td><td style="word-break:break-all;font-size:13px">' + esc(d.url) + (d.times > 1 ? ' <span class="chip" style="padding:1px 7px;font-size:11px">x' + d.times + '</span>' : '') + '</td><td>' + d.type + (d.rel ? '<br><small style="color:#777">' + esc(d.rel) + '</small>' : '') + '</td><td style="color:' + (d.issues.length ? '#d1351f' : '#3d8f12') + ';font-weight:700;font-size:13px">' + (d.issues.length ? d.issues.map(esc).join('<br>') : 'OK') + '</td></tr>';
    }).join('') + '</tbody></table></div>';
  }
  document.querySelectorAll('#ilTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#ilTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); filter = b.getAttribute('data-f'); table(); }); });
  $('ilText').addEventListener('input', run); $('ilDomain').addEventListener('input', run);
  $('ilSample').onclick = function(){ $('ilText').value = SAMPLE; run(); };
  $('ilClear').onclick = function(){ $('ilText').value=''; run(); $('ilText').focus(); };
  $('ilText').value = SAMPLE; run();
''',
        content=r'''
    <h2>Why Internal Links Matter</h2>
    <p>Internal links connect your pages together. They help Google discover new content, understand how topics relate, and pass authority from strong pages to newer ones.</p>
    <p>They also guide readers to the next useful page, which keeps them on your site longer.</p>

    <h2>How to Use This Internal Link Checker</h2>
    <ol>
      <li><strong>Enter your domain</strong> so the tool can tell internal links from external ones. Relative links like <code>/about/</code> count as internal.</li>
      <li><strong>Paste the HTML.</strong> Use the full page source, or just the article to ignore menus and footers.</li>
      <li><strong>Review the report.</strong> Switch between All, Internal, External and Issues to focus on what needs fixing.</li>
    </ol>

    <h2>What the Checker Flags</h2>
    <ul>
      <li><strong>Generic anchor text</strong> like "click here" or "read more", which tells search engines nothing about the target page.</li>
      <li><strong>Empty anchors</strong>, usually linked images with no alt text.</li>
      <li><strong>Nofollow on internal links</strong>, which stops your own pages from sharing authority.</li>
      <li><strong>Links using http</strong> instead of https, which add an extra redirect.</li>
      <li><strong>External links opening in a new tab</strong> without <code>rel="noopener"</code>.</li>
      <li><strong>Repeated URLs</strong>, marked with a count so you can spot pages linked many times.</li>
    </ul>

    <h2>Internal Linking Best Practices</h2>
    <ul>
      <li>Use descriptive anchor text that matches the topic of the target page.</li>
      <li>Link from strong, well ranked pages to the pages you want to grow.</li>
      <li>Add three to five relevant in body links per article rather than long link lists.</li>
      <li>Fix or update links to redirected pages so they point to the final URL.</li>
    </ul>
    <p>Read more in our guides to <a href="https://brandella.in/internal-linking-best-practices-seo-rankings/">internal linking best practices</a>, <a href="https://brandella.in/anchor-text-optimization-best-practices/">anchor text optimization</a>, and <a href="https://brandella.in/link-equity-explained/">link equity</a>. To check images on the same page, use the <a href="https://brandella.in/tools/seo-tools/alt-text-checker/">alt text checker</a>.</p>
''',
        faqs=[
            ("What is an internal link?", "An internal link points from one page on your website to another page on the same domain. Links to other websites are external links."),
            ("Why is 'click here' bad anchor text?", "It gives search engines and screen reader users no clue about the page being linked. Descriptive anchors like 'internal linking best practices' explain the destination."),
            ("Does the internal link checker crawl my website?", "No. It analyses only the HTML you paste, entirely in your browser. To check a whole site, run this on each key page or use a crawler like Screaming Frog."),
            ("Should internal links be nofollow?", "Almost never. Nofollow on internal links stops authority flowing between your own pages. Keep internal links followed unless the target is something like a login page."),
        ],
        related=[("Internal Linking Best Practices", "internal-linking-best-practices-seo-rankings"), ("Anchor Text Optimization", "anchor-text-optimization-best-practices"),
                 ("Link Equity Explained", "link-equity-explained"), ("Nofollow vs Dofollow Links", "nofollow-vs-dofollow-links")],
    ))

    # ---------- 10. WORD AND CHARACTER COUNTER ----------
    TOOLS.append(dict(
        slug='word-character-counter', short='WC', name='Word and Character Counter',
        card='Count words, characters, sentences and reading time, and check limits for titles, ads and social posts.',
        title='Word and Character Counter: Free Live Word Count Tool',
        desc='Free word and character counter. Count words, characters, sentences, paragraphs and reading time, and check limits for SEO titles and social posts.',
        h1='Word and Character Counter',
        lead='Count words, characters, sentences and reading time as you type, and check your text against limits for SEO titles, ads and social posts.',
        tool=r'''<section class="tool" aria-label="Word and character counter">
    <div class="card">
      <h2>Type or Paste Text</h2>
      <div class="field">
        <textarea id="wcText" class="big" style="min-height:300px" aria-label="Text to count">A word counter helps you hit the right length for every piece of content. Blog posts, meta descriptions, ad headlines and social posts all have different limits.

Paste your text here and watch the numbers update as you type.</textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn" id="wcClear">Clear</button>
        <button class="btn" id="wcSpace">Remove Extra Spaces</button>
      </div>
    </div>

    <div class="card">
      <h2>Counts</h2>
      <div class="stats">
        <div class="stat-box"><b id="wcWords">0</b><span>Words</span></div>
        <div class="stat-box"><b id="wcChars">0</b><span>Characters</span></div>
        <div class="stat-box"><b id="wcNoSp">0</b><span>No Spaces</span></div>
        <div class="stat-box"><b id="wcSent">0</b><span>Sentences</span></div>
        <div class="stat-box"><b id="wcPara">0</b><span>Paragraphs</span></div>
        <div class="stat-box"><b id="wcRead">0s</b><span>Reading Time</span></div>
        <div class="stat-box"><b id="wcSpeak">0s</b><span>Speaking Time</span></div>
        <div class="stat-box"><b id="wcAvg">0</b><span>Avg Word Length</span></div>
      </div>
      <h3 style="font-size:16px;margin:4px 0 8px">Character Limits</h3>
      <div id="wcLimits"></div>
      <h3 style="font-size:16px;margin:16px 0 8px">Top Words</h3>
      <div id="wcTop"></div>
    </div>
  </section>''',
        js=STOP_JS + r'''
  var LIMITS = [['SEO title',60],['Meta description',160],['Google Ads headline',30],['Google Ads description',90],['X (Twitter) post',280],['LinkedIn post',3000],['Instagram caption',2200]];
  function dur(sec){ sec = Math.round(sec); if (sec < 60) return sec + 's'; var m = Math.floor(sec/60), s = sec % 60; return m + 'm' + (s ? ' ' + s + 's' : ''); }
  function run(){
    var t = $('wcText').value, words = t.match(/[A-Za-z0-9À-ɏ]+(?:['’][A-Za-z]+)?/g) || [], n = words.length;
    $('wcWords').textContent = n.toLocaleString();
    $('wcChars').textContent = t.length.toLocaleString();
    $('wcNoSp').textContent = t.replace(/\s/g,'').length.toLocaleString();
    $('wcSent').textContent = (t.match(/[^.!?]+[.!?]+(\s|$)/g) || (t.trim() ? [1] : [])).length;
    $('wcPara').textContent = t.split(/\n\s*\n/).filter(function(p){ return p.trim(); }).length;
    $('wcRead').textContent = dur(n / 200 * 60);
    $('wcSpeak').textContent = dur(n / 130 * 60);
    $('wcAvg').textContent = n ? (words.join('').length / n).toFixed(1) : 0;
    var len = t.trim().length;
    $('wcLimits').innerHTML = '<table class="rtable"><tbody>' + LIMITS.map(function(l){
      var ok = len <= l[1];
      return '<tr><td>' + l[0] + '</td><td class="num">' + len + ' / ' + l[1] + '</td><td class="num" style="font-weight:700;color:' + (ok ? '#3d8f12' : '#d1351f') + '">' + (ok ? 'Fits' : 'Over by ' + (len - l[1])) + '</td></tr>';
    }).join('') + '</tbody></table>';
    var m = {}; words.forEach(function(w){ w = w.toLowerCase(); if (!STOP.has(w) && w.length > 2 && !/^\d+$/.test(w)) m[w] = (m[w]||0) + 1; });
    var top = Object.keys(m).map(function(k){ return [k, m[k]]; }).sort(function(a,b){ return b[1]-a[1]; }).slice(0,8);
    $('wcTop').innerHTML = top.length ? '<div class="chips">' + top.map(function(x){ return '<span class="chip">' + esc(x[0]) + ' &times; ' + x[1] + '</span>'; }).join('') + '</div>' : '<p class="empty">Start typing to see your most used words.</p>';
  }
  $('wcText').addEventListener('input', run);
  $('wcClear').onclick = function(){ $('wcText').value=''; run(); $('wcText').focus(); };
  $('wcSpace').onclick = function(){ $('wcText').value = $('wcText').value.replace(/[ \t]+/g,' ').replace(/ *\n */g,'\n').replace(/\n{3,}/g,'\n\n').trim(); run(); };
  run();
''',
        content=r'''
    <h2>A Word Counter Built for Marketers</h2>
    <p>This word and character counter does more than count words. It shows reading time, speaking time and your most used words, and checks your text against the limits that matter in SEO and advertising.</p>
    <p>Everything updates live as you type, and nothing you write leaves your browser.</p>

    <h2>What It Counts</h2>
    <ul>
      <li><strong>Words and characters</strong>, with and without spaces.</li>
      <li><strong>Sentences and paragraphs</strong>, where a blank line starts a new paragraph.</li>
      <li><strong>Reading time</strong> at 200 words per minute, a common average for online reading.</li>
      <li><strong>Speaking time</strong> at 130 words per minute, useful for videos, podcasts and presentations.</li>
      <li><strong>Top words</strong>, ignoring common filler words, so you can spot repetition.</li>
    </ul>

    <h2>Common Length Limits</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Where</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Limit</th></tr></thead>
      <tbody>
        <tr><td>SEO title</td><td>About 60 characters</td></tr>
        <tr><td>Meta description</td><td>About 160 characters</td></tr>
        <tr><td>Google Ads headline</td><td>30 characters</td></tr>
        <tr><td>Google Ads description</td><td>90 characters</td></tr>
        <tr><td>X post</td><td>280 characters (standard accounts)</td></tr>
        <tr><td>Instagram caption</td><td>2,200 characters</td></tr>
        <tr><td>LinkedIn post</td><td>3,000 characters</td></tr>
      </tbody>
    </table>
    <p>Search titles are actually cut by pixel width, not characters. For an exact check, use our <a href="https://brandella.in/tools/seo-tools/serp-snippet-preview/">SERP snippet preview</a>.</p>

    <h2>How Long Should a Blog Post Be?</h2>
    <p>There is no ideal word count for ranking. The right length is whatever fully answers the searcher's question without padding.</p>
    <p>Look at the pages already ranking for your keyword to judge the depth needed, then focus on covering the topic better rather than simply writing more. Our guide on <a href="https://brandella.in/how-to-write-seo-friendly-blog/">writing an SEO friendly blog</a> goes into detail, and you can plan lengths ahead with a <a href="https://brandella.in/content-calendar-planning/">content calendar</a>.</p>
''',
        faqs=[
            ("How is reading time calculated?", "Reading time divides the word count by 200 words per minute, a common average for reading on screen. Speaking time uses 130 words per minute."),
            ("Does the character count include spaces?", "The main character count includes spaces and line breaks. The 'No Spaces' box shows the count without any whitespace."),
            ("Is word count a Google ranking factor?", "No. Google has said word count is not a ranking factor. Length matters only as far as it helps you fully answer the search."),
            ("Is my text saved anywhere?", "No. The word and character counter runs entirely in your browser and does not save or upload your text."),
        ],
        related=[("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("Reading Time Calculator for Blog Posts", "reading-time-calculator-blog-posts"),
                 ("Title Tag Optimization", "title-tag-optimization"), ("Content Calendar Planning", "content-calendar-planning")],
    ))

    # ---------- 11. TITLE CASE CONVERTER ----------
    TOOLS.append(dict(
        slug='title-case-converter', short='CC', name='Title Case Converter',
        card='Convert headlines to title case, sentence case, uppercase or lowercase, keeping acronyms intact.',
        title='Title Case Converter: Free Headline Capitalization Tool',
        desc='Free title case converter. Turn headlines into title case, sentence case, uppercase or lowercase instantly, while keeping acronyms like SEO intact.',
        h1='Title Case Converter',
        lead='Paste a headline or a list of titles and convert them to title case, sentence case, uppercase or lowercase in one click.',
        tool=r'''<section class="tool" aria-label="Title case converter">
    <div class="card">
      <h2>Enter Text</h2>
      <div class="field">
        <label for="ccIn">Text <em>one or more lines</em></label>
        <textarea id="ccIn" class="big">how to improve your website's SEO in 30 days
the complete guide to google ads for beginners
WHY CONTENT MARKETING STILL WORKS: a practical look</textarea>
      </div>
      <div class="tabs" role="tablist" id="ccTabs" style="flex-wrap:wrap">
        <button class="on" data-m="title">Title Case</button>
        <button data-m="sentence">Sentence case</button>
        <button data-m="caps">Capitalize Each</button>
        <button data-m="upper">UPPERCASE</button>
        <button data-m="lower">lowercase</button>
      </div>
      <label class="check"><input id="ccAcr" type="checkbox" checked> Keep acronyms (SEO, PPC, AI) in capitals</label>
    </div>

    <div class="card">
      <h2>Result</h2>
      <div class="field">
        <textarea id="ccOut" class="big" readonly aria-label="Converted text"></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="ccCopy">Copy Result</button>
        <button class="btn" id="ccClear">Clear</button>
        <span class="toast" id="toast">Copied!</span>
      </div>
      <div class="tips"><strong>Title case rules used</strong><ul>
        <li>Capitalize the first and last word</li><li>Capitalize all main words</li><li>Lowercase short words like a, the, and, of, to, in</li><li>Capitalize the word after a colon</li></ul></div>
    </div>
  </section>''',
        js=r'''
  var SMALL = new Set('a an the and but or nor for so yet at by in of on to up as via vs per off out'.split(' '));
  var mode = 'title';
  function isAcr(w){ var b = w.replace(/[^A-Za-z0-9&]/g,''); if (b.length > 4 && !KNOWN.has(b.toUpperCase())) return false; return b.length >= 2 && b.length <= 6 && /[A-Z]/.test(b) && b === b.toUpperCase() && /^[A-Z0-9&]+s?$/.test(b); }
  function cap(w){ return w.toLowerCase().replace(/(^[^a-z0-9]*|[\/])([a-z])/g, function(m, p, c){ return p + c.toUpperCase(); }); }
  var KNOWN = new Set('SEO SEM PPC AI ML GA4 GTM URL URLS HTML CSS JS API APIS CTA CTR ROI ROAS CPC CPA CPM KPI KPIS B2B B2C UX UI USA UK EU FAQ FAQS PDF CRM CMS SERP SERPS AEO GEO LLM LLMS SMS USB IT HR PR TV'.split(' '));
  function convertLine(line){
    var letters = line.replace(/[^A-Za-z]/g,''), shouting = letters.length > 8 && (letters.replace(/[^A-Z]/g,'').length / letters.length) > 0.6;
    var acr = $('ccAcr').checked, parts = line.split(/(\s+)/), idx = [];
    parts.forEach(function(p, i){ if (p.trim()) idx.push(i); });
    var first = idx[0], last = idx[idx.length - 1], after = true;
    return parts.map(function(w, i){
      if (!w.trim()) return w;
      var out, keep = acr && isAcr(w) && (!shouting || KNOWN.has(w.replace(/[^A-Za-z0-9]/g,'').toUpperCase())), bare = w.toLowerCase().replace(/[^a-z']/g,'');
      if (mode === 'upper') out = w.toUpperCase();
      else if (mode === 'lower') out = keep ? w : w.toLowerCase();
      else if (keep) out = w;
      else if (mode === 'caps') out = cap(w);
      else if (mode === 'title') out = (i !== first && i !== last && !after && SMALL.has(bare)) ? w.toLowerCase() : cap(w);
      else out = after ? cap(w) : (/^i$/i.test(bare) ? 'I' : w.toLowerCase());
      after = mode === 'sentence' ? /[.!?:]["')\]]*$/.test(w) : /[:?!]["')\]]*$/.test(w);
      return out;
    }).join('');
  }
  function run(){ $('ccOut').value = $('ccIn').value.split('\n').map(convertLine).join('\n'); }
  document.querySelectorAll('#ccTabs button').forEach(function(b){ b.addEventListener('click', function(){
    document.querySelectorAll('#ccTabs button').forEach(function(x){ x.classList.remove('on'); }); b.classList.add('on'); mode = b.getAttribute('data-m'); run(); }); });
  $('ccIn').addEventListener('input', run); $('ccAcr').addEventListener('change', run);
  $('ccCopy').onclick = function(){ copyText($('ccOut').value, 'toast'); };
  $('ccClear').onclick = function(){ $('ccIn').value=''; run(); $('ccIn').focus(); };
  run();
''',
        content=r'''
    <h2>What Is Title Case?</h2>
    <p>Title case capitalizes the main words in a headline while keeping short words like "a", "the" and "of" in lowercase. It is the standard style for book titles, news headlines and many blog post titles.</p>
    <p>Sentence case, by contrast, capitalizes only the first word and proper nouns, just like a normal sentence. Both are correct. What matters is using one style consistently across your site.</p>

    <h2>How to Use This Title Case Converter</h2>
    <ol>
      <li><strong>Paste your text.</strong> One headline or a whole list, one per line.</li>
      <li><strong>Pick a style.</strong> Title Case, Sentence case, Capitalize Each Word, UPPERCASE or lowercase.</li>
      <li><strong>Copy the result</strong> into your CMS, ad platform or spreadsheet.</li>
    </ol>
    <p>Acronyms such as SEO, PPC, AI and GA4 stay in capitals by default, so "how to improve your SEO" becomes "How to Improve Your SEO", not "Seo".</p>

    <h2>The Five Styles Explained</h2>
    <table class="lim">
      <thead><tr style="background:#2b2b2b !important;"><th style="background:#2b2b2b !important; color:#ffffff !important;">Style</th><th style="background:#2b2b2b !important; color:#ffffff !important;">Example</th></tr></thead>
      <tbody>
        <tr><td>Title Case</td><td>The Complete Guide to Google Ads for Beginners</td></tr>
        <tr><td>Sentence case</td><td>The complete guide to Google Ads for beginners</td></tr>
        <tr><td>Capitalize Each Word</td><td>The Complete Guide To Google Ads For Beginners</td></tr>
        <tr><td>UPPERCASE</td><td>THE COMPLETE GUIDE TO GOOGLE ADS FOR BEGINNERS</td></tr>
        <tr><td>lowercase</td><td>the complete guide to google ads for beginners</td></tr>
      </tbody>
    </table>
    <p>Sentence case cannot know which words are names, so check proper nouns like brand names after converting.</p>

    <h2>Does Capitalization Affect SEO?</h2>
    <p>No. Google treats uppercase and lowercase the same for ranking. Capitalization does affect how your result looks, though, and a clean, consistent title can earn more clicks.</p>
    <p>Avoid writing whole titles in capitals. They are harder to read and can look like spam. For more, see <a href="https://brandella.in/title-tag-optimization/">title tag optimization</a> and <a href="https://brandella.in/html-heading-structure-best-practices/">heading structure best practices</a>, and preview your title with the <a href="https://brandella.in/tools/seo-tools/serp-snippet-preview/">SERP snippet preview</a>.</p>
''',
        faqs=[
            ("Which words stay lowercase in title case?", "Short articles, conjunctions and prepositions such as a, an, the, and, but, or, for, at, by, in, of, on and to stay lowercase, unless they are the first word, the last word, or follow a colon."),
            ("Should I use title case or sentence case for blog titles?", "Either works. Title case feels more traditional, while sentence case reads more naturally and is popular with modern brands. Pick one and use it consistently."),
            ("Will the converter change acronyms like SEO?", "Not by default. Words written in capitals, such as SEO, PPC or GA4, are kept as they are. Untick the acronym option to convert them too."),
            ("Can I convert many headlines at once?", "Yes. Paste one headline per line and the title case converter processes each line separately."),
        ],
        related=[("Title Tag Optimization", "title-tag-optimization"), ("HTML Heading Structure Best Practices", "html-heading-structure-best-practices"),
                 ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("6 Tips on How to Build Articles", "6-tips-how-to-build-articles")],
    ))

    # ---------- 12. DUPLICATE LINE AND KEYWORD CLEANER ----------
    TOOLS.append(dict(
        slug='duplicate-line-remover', short='DL', name='Duplicate Line and Keyword Cleaner',
        card='Remove duplicate lines from keyword lists, trim spaces, drop blanks and sort A to Z in one click.',
        title='Duplicate Line Remover: Free Keyword List Cleaner',
        desc='Free duplicate line remover and keyword list cleaner. Remove duplicates, trim spaces, delete blank lines, lowercase and sort lists instantly.',
        h1='Duplicate Line and Keyword Cleaner',
        lead='Paste any list, such as keywords, URLs or emails, and remove duplicates, blank lines and extra spaces, then sort it the way you need.',
        tool=r'''<section class="tool" aria-label="Duplicate line remover">
    <div class="card">
      <h2>Paste Your List</h2>
      <div class="field">
        <label for="dlIn">List <em id="dlInCount">0 lines</em></label>
        <textarea id="dlIn" class="big">seo tools
SEO Tools
  keyword research

backlink checker
keyword   research
seo tools
rank tracker
backlink checker</textarea>
      </div>
      <label class="check"><input id="dlCase" type="checkbox" checked> Ignore case when finding duplicates</label>
      <label class="check"><input id="dlTrim" type="checkbox" checked> Trim and collapse extra spaces</label>
      <label class="check"><input id="dlBlank" type="checkbox" checked> Remove blank lines</label>
      <label class="check"><input id="dlLower" type="checkbox"> Convert to lowercase</label>
      <div class="field" style="margin-top:10px">
        <label for="dlSort">Sort</label>
        <select id="dlSort"><option value="none">Keep original order</option><option value="az">A to Z</option><option value="za">Z to A</option><option value="len">Shortest first</option><option value="lenr">Longest first</option></select>
      </div>
    </div>

    <div class="card">
      <h2>Clean List</h2>
      <div class="stats">
        <div class="stat-box"><b id="dlA">0</b><span>Lines In</span></div>
        <div class="stat-box"><b id="dlB">0</b><span>Lines Out</span></div>
        <div class="stat-box"><b id="dlC">0</b><span>Removed</span></div>
      </div>
      <div class="field">
        <textarea id="dlOut" class="big" readonly aria-label="Clean list"></textarea>
      </div>
      <div class="actions" style="margin-top:0">
        <button class="btn dark" id="dlCopy">Copy List</button>
        <button class="btn" id="dlDown">Download TXT</button>
        <button class="btn" id="dlClear">Clear</button>
        <span class="toast" id="toast">Copied!</span>
      </div>
    </div>
  </section>''',
        js=r'''
  function run(){
    var lines = $('dlIn').value.split(/\r?\n/), seen = {}, out = [];
    $('dlInCount').textContent = lines.filter(function(l){ return l.trim(); }).length + ' lines';
    lines.forEach(function(l){
      if ($('dlTrim').checked) l = l.trim().replace(/\s+/g,' ');
      if ($('dlLower').checked) l = l.toLowerCase();
      if (!l.trim() && $('dlBlank').checked) return;
      var key = $('dlCase').checked ? l.trim().toLowerCase() : l;
      if (l.trim() && seen[key]) return;
      seen[key] = 1; out.push(l);
    });
    var s = $('dlSort').value;
    if (s === 'az') out.sort(function(a,b){ return a.localeCompare(b, undefined, {sensitivity:'base'}); });
    if (s === 'za') out.sort(function(a,b){ return b.localeCompare(a, undefined, {sensitivity:'base'}); });
    if (s === 'len') out.sort(function(a,b){ return a.length - b.length; });
    if (s === 'lenr') out.sort(function(a,b){ return b.length - a.length; });
    $('dlOut').value = out.join('\n');
    $('dlA').textContent = lines.length; $('dlB').textContent = out.length; $('dlC').textContent = lines.length - out.length;
  }
  $('dlIn').addEventListener('input', run);
  ['dlCase','dlTrim','dlBlank','dlLower','dlSort'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('dlCopy').onclick = function(){ copyText($('dlOut').value, 'toast'); };
  $('dlDown').onclick = function(){ var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([$('dlOut').value], {type:'text/plain'})); a.download = 'clean-list.txt'; a.click(); };
  $('dlClear').onclick = function(){ $('dlIn').value=''; run(); $('dlIn').focus(); };
  run();
''',
        content=r'''
    <h2>Why Clean Your Keyword Lists?</h2>
    <p>Keyword lists grow messy fast. Exports from different tools overlap, the same phrase appears with different capitals, and stray spaces make identical keywords look different.</p>
    <p>A clean list saves time in research, avoids duplicate keywords in Google Ads, and gives you accurate counts when planning content.</p>

    <h2>How to Use This Duplicate Line Remover</h2>
    <ol>
      <li><strong>Paste your list</strong> with one item per line. It works for keywords, URLs, emails, product names or any other list.</li>
      <li><strong>Choose your options.</strong> By default it ignores case, trims spaces and removes blank lines.</li>
      <li><strong>Sort if needed,</strong> alphabetically or by length.</li>
      <li><strong>Copy or download</strong> the clean list.</li>
    </ol>
    <p>The counters show how many lines went in, how many came out, and how many were removed.</p>

    <h2>What Each Option Does</h2>
    <ul>
      <li><strong>Ignore case</strong> treats "SEO Tools" and "seo tools" as the same item and keeps the first one.</li>
      <li><strong>Trim and collapse spaces</strong> removes spaces at the start and end, and turns double spaces into single ones.</li>
      <li><strong>Remove blank lines</strong> deletes empty rows.</li>
      <li><strong>Convert to lowercase</strong> makes the whole list consistent, which suits keyword research and URL lists.</li>
      <li><strong>Sort</strong> orders the list A to Z, Z to A, or by length, which is handy for spotting long tail keywords.</li>
    </ul>

    <h2>Where It Helps</h2>
    <p>Use it after merging exports from several keyword tools, before uploading keywords or negative keywords to Google Ads, or when combining URL lists for a content audit.</p>
    <p>It pairs well with our <a href="https://brandella.in/tools/seo-tools/keyword-combiner/">keyword combiner</a>. For strategy, read <a href="https://brandella.in/google-ads-negative-keywords/">Google Ads negative keywords</a> and <a href="https://brandella.in/content-audit-explained-improve-rankings/">content audits explained</a>.</p>
''',
        faqs=[
            ("How do I remove duplicate keywords from a list?", "Paste the list with one keyword per line. The tool removes duplicates instantly, and with 'ignore case' on, it also catches the same keyword written with different capitals."),
            ("Which duplicate is kept?", "The first time an item appears is kept, and later repeats are removed. Your original order stays the same unless you choose a sort option."),
            ("Is there a limit on list size?", "No fixed limit. Because the tool runs in your browser, it handles tens of thousands of lines comfortably on most computers."),
            ("Is my list uploaded?", "No. The duplicate line remover works entirely in your browser. Nothing is uploaded or stored."),
        ],
        related=[("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("Best Keyword Research Tools Compared", "best-keyword-research-tools-compared"),
                 ("Python Keyword Research Automation", "python-keyword-research-automation"), ("Content Audit Explained", "content-audit-explained-improve-rankings")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'seo-tools'; t['updated'] = '2026-10-28'
