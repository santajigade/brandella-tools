"""Batch 23 (2026-11-20): Content Writing Tools category, sixth tool (Remove Line Breaks).
Search demand (Semrush US, Nov 2026): "remove line breaks" 2,400/mo KD 20, "line break remover" 720 KD 4,
"remove line breaks online" 170, "remove line breaks from text" 140. Established tool sites rank for it.
Not covered by any existing tool: AI Text Cleaner only tidies blank lines, it does not join wrapped lines.
Facts checked 2026-11-20: MDN Glossary CRLF (developer.mozilla.org/en-US/docs/Glossary/CRLF): Windows uses CR LF,
Linux and Unix use LF, classic Mac OS used CR.
Runs fully in the browser: keeps paragraphs and list items, rejoins words split by a hyphen at the end of a line
(PDF copies), handles CR LF, CR, LF and Unicode line separators, replace mode for comma lists or <br>."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
AI = 'https://brandella.in/tools/ai-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

SAMPLE = ('Search engines and AI assistants now read the same pages you\n'
          'publish, so clean text matters more than ever. When you copy\n'
          'from a PDF, an email or a chat window, every line often ends\n'
          'with a hard break, and long words get split with a hyp-\n'
          'hen at the edge of the page.\n'
          '\n'
          'That makes the text messy to paste into WordPress, Google\n'
          'Docs or an AI prompt. Fix it in three steps:\n'
          '1. Paste the text into the box.\n'
          '2. Pick how to handle the line breaks.\n'
          '3. Copy the clean result.\n'
          '\n'
          'Everything runs in your browser, so nothing you paste is\n'
          'uploaded anywhere.')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='remove-line-breaks', short='LR', name='Remove Line Breaks',
        card='Fix text copied from PDFs, emails and AI chats: join wrapped lines, keep paragraphs and lists, or turn lines into a comma list.',
        title='Remove Line Breaks: Free Online Line Break Remover',
        desc='Free line break remover. Fix text copied from a PDF, email or ChatGPT: join broken lines, keep paragraphs and lists, or replace line breaks with commas.',
        h1='Remove Line Breaks',
        lead='Paste text copied from a PDF, email, chat window or website and get clean, flowing paragraphs. Keep your paragraphs and lists, rejoin split words, or turn every line into a comma separated list.',
        tool='''<section class="tool" aria-label="Remove line breaks">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('lrIn', 'Text with unwanted line breaks', SAMPLE, em='from a PDF, email, AI chat or web page', tag='textarea', extra=' style="min-height:300px"') + '''
      ''' + F('lrMode', 'What to do with line breaks', 'para', tag='select', opts=[
            ('para', 'Keep paragraphs, join wrapped lines'),
            ('all', 'Remove all line breaks (one block of text)'),
            ('blank', 'Remove empty lines only'),
            ('rep', 'Replace each line break with my text')]) + '''
      <div id="lrRepWrap">''' + F('lrRep', 'Replace line breaks with', ', ', em='for example a comma, a space or &lt;br&gt;') + '''</div>
      ''' + CK('lrHy', 'Rejoin words split by a hyphen at the end of a line') + '''
      ''' + CK('lrList', 'Keep list items on their own lines') + '''
      ''' + CK('lrSp', 'Collapse repeated spaces and tabs') + '''
      ''' + CK('lrTrim', 'Trim spaces at the start and end of each line') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Clean Text</h2>
      <div class="stats">''' + S('lrBefore', 'Line breaks before') + S('lrAfter', 'Line breaks after') + S('lrWords', 'Words') + S('lrChars', 'Characters') + '''</div>
      <textarea id="lrOut" aria-label="Clean text" spellcheck="false" style="min-height:300px"></textarea>
      <div class="actions"><button class="btn dark" id="lrCopy">Copy Clean Text</button><button class="btn" id="lrDl">Download .txt</button><button class="btn" id="lrClear">Clear</button><span class="toast" id="toast">Copied!</span></div>
      <div class="kw-result" id="lrNote"></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  var LIST = /^\s*(?:[\u2022\u25AA\u25E6\u25CF\u2023*+>-]|\d{1,3}[.)]|[a-zA-Z][.)]|\(\d{1,3}\)|\([a-zA-Z]\))\s+/;
  function joinTwo(a, b, hy){
    if (hy){
      if (/\u00AD$/.test(a)) return a.slice(0, -1) + b;
      if (/[A-Za-z]-$/.test(a) && /^[a-z]/.test(b)) return a.slice(0, -1) + b;
    }
    if (!a) return b; if (!b) return a;
    return /\s$/.test(a) || /^\s/.test(b) ? a + b : a + ' ' + b;
  }
  function clean(text, o){
    text = text.replace(/\u2029/g, '\n\n').replace(/\r\n?|[\u2028\u0085\u000B\u000C]/g, '\n');
    var before = (text.match(/\n/g) || []).length;
    var lines = text.split('\n').map(function(l){
      if (o.sp) l = l.replace(/[ \t\u00A0]+/g, ' ');
      if (o.trim) l = l.replace(/^[ \t\u00A0]+|[ \t\u00A0]+$/g, '');
      return l;
    });
    var isBlank = function(l){ return !/\S/.test(l); }, out;
    if (o.mode === 'blank'){
      out = lines.filter(function(l){ return !isBlank(l); }).join('\n');
    } else if (o.mode === 'rep'){
      var rep = o.rep.replace(/\\n/g, '\n').replace(/\\t/g, '\t');
      var parts = [], cur = null;
      lines.forEach(function(l){
        if (isBlank(l)) { if (cur !== null) { parts.push(cur); cur = null; } return; }
        if (cur !== null && o.hy && (/\u00AD$/.test(cur) || (/[A-Za-z]-$/.test(cur) && /^[a-z]/.test(l.trim())))) cur = joinTwo(cur, l.trim(), true);
        else { if (cur !== null) parts.push(cur); cur = l; }
      });
      if (cur !== null) parts.push(cur);
      out = parts.join(rep);
    } else {
      var paras = [], block = [];
      lines.forEach(function(l){
        if (isBlank(l)) { if (block.length) { paras.push(block); block = []; } }
        else block.push(l);
      });
      if (block.length) paras.push(block);
      var done = paras.map(function(p){
        var res = [], cur = '';
        p.forEach(function(l, i){
          if (i === 0) { cur = l; return; }
          if (o.mode === 'para' && o.list && LIST.test(l)) { res.push(cur); cur = l; return; }
          cur = joinTwo(cur, l, o.hy);
        });
        res.push(cur);
        return res.join('\n');
      });
      if (o.mode === 'all') {
        out = done.reduce(function(a, b){ return joinTwo(a, b, false); }, '');
      } else out = done.join('\n\n');
      if (o.sp) out = out.replace(/ {2,}/g, ' ');
    }
    return { text: out, before: before, after: (out.match(/\n/g) || []).length };
  }
  function opts(){ return { mode: $('lrMode').value, rep: $('lrRep').value, hy: $('lrHy').checked, list: $('lrList').checked, sp: $('lrSp').checked, trim: $('lrTrim').checked }; }
  function run(){
    var o = opts(), r = clean($('lrIn').value, o);
    $('lrRepWrap').style.display = o.mode === 'rep' ? '' : 'none';
    $('lrList').closest('label').style.opacity = o.mode === 'para' ? 1 : .5;
    $('lrOut').value = r.text;
    $('lrBefore').textContent = fmtN(r.before); $('lrAfter').textContent = fmtN(r.after);
    var w = r.text.trim() ? r.text.trim().split(/\s+/).length : 0;
    $('lrWords').textContent = fmtN(w); $('lrChars').textContent = fmtN(r.text.length);
    if (!$('lrIn').value.trim()) say('lrNote', '', 'Paste some text on the left to clean it.');
    else if (r.before === r.after && o.mode !== 'rep') say('lrNote', 'ok', '<strong>Nothing to remove.</strong> This text has no line breaks that need fixing with these settings.');
    else say('lrNote', 'ok', '<strong>Done.</strong> Removed ' + fmtN(Math.max(0, r.before - r.after)) + ' line breaks. Copy the clean text or download it as a file.');
  }
  $('lrIn').addEventListener('input', run); $('lrRep').addEventListener('input', run);
  ['lrMode', 'lrHy', 'lrList', 'lrSp', 'lrTrim'].forEach(function(i){ $(i).addEventListener('change', run); });
  $('lrCopy').onclick = function(){ copyText($('lrOut').value, 'toast'); };
  $('lrDl').onclick = function(){ download('clean-text.txt', $('lrOut').value); };
  $('lrClear').onclick = function(){ $('lrIn').value = ''; run(); $('lrIn').focus(); };
  window.__lrClean = clean;
  run();
''',
        content=f'''
    <h2>What Does a Line Break Remover Do?</h2>
    <p>When you copy text from a PDF, an email, a chat window or some web pages, each line often ends with a hard line break. Paste it into WordPress, Google Docs, a form or an AI prompt and the sentences break in odd places, words are split in half, and lists run together.</p>
    <p>This tool removes the line breaks you do not want and keeps the ones you do. By default it joins wrapped lines into flowing paragraphs, keeps the blank line between paragraphs, keeps numbered and bulleted list items on their own lines, and rejoins words that were split with a hyphen at the edge of the page.</p>
    <p>It also handles every kind of line ending. Windows uses a carriage return plus a line feed (<code>\\r\\n</code>), while Linux and macOS use a line feed alone (<code>\\n</code>), as the <a href="https://developer.mozilla.org/en-US/docs/Glossary/CRLF" {EXT}>MDN glossary on CRLF</a> explains. Text copied between systems often mixes them, and this tool treats them all the same.</p>

    <h2>How to Remove Line Breaks</h2>
    <ol>
      <li><strong>Paste your text</strong> into the box on the left. A sample copied from a PDF is already there.</li>
      <li><strong>Pick a mode.</strong> Keep paragraphs for articles, remove all breaks for one block of text, remove empty lines only, or replace each break with your own text.</li>
      <li><strong>Set the options.</strong> Rejoin split words, keep list items, collapse extra spaces and trim each line.</li>
      <li><strong>Check the result.</strong> The clean text updates as you type, with a count of line breaks before and after.</li>
      <li><strong>Copy or download</strong> the clean text and paste it where you need it.</li>
    </ol>

    <h2>The Four Modes Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Mode', 'What it does', 'Best for')}
      <tbody>
        <tr><td>Keep paragraphs</td><td>Joins wrapped lines, keeps blank lines between paragraphs and list items on their own lines</td><td>Text from PDFs, ebooks, old emails and scanned documents</td></tr>
        <tr><td>Remove all line breaks</td><td>Turns everything into one continuous block of text</td><td>Meta descriptions, form fields, spreadsheet cells and ad copy</td></tr>
        <tr><td>Remove empty lines only</td><td>Deletes blank lines and keeps every other line as it is</td><td>Code, lists and AI answers with too much spacing</td></tr>
        <tr><td>Replace with my text</td><td>Puts your text, such as a comma or <code>&lt;br&gt;</code>, where each line break was</td><td>Turning a column of keywords or emails into a comma separated list</td></tr>
      </tbody>
    </table></div>
    <p>In replace mode you can type <code>\\n</code> for a new line or <code>\\t</code> for a tab, for example <code>,\\n</code> to add a comma at the end of every line.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Check rejoined words.</strong> A word that really has a hyphen, such as <code>well-known</code>, can lose it if the line broke right after the hyphen. Turn the option off for text full of such words.</li>
      <li><strong>Clean prompts before you paste.</strong> Wrapped lines waste tokens and can confuse AI models about where a sentence ends. Paste clean paragraphs into ChatGPT, Claude or Gemini instead.</li>
      <li><strong>Keep lists as lists.</strong> Lines that start with a number, a letter, a bullet or a star stay on their own line, so steps and checklists survive.</li>
      <li><strong>Your text stays private.</strong> Everything runs in your browser. Nothing you paste is uploaded or saved.</li>
    </ul>

    <h2>Clean Text, Better Content</h2>
    <p>Clean formatting is the first step of good writing. Learn more in <a href="{B}10-easy-tips-for-effective-content-writing/">10 easy tips for effective content writing</a>, write better AI prompts with <a href="{B}prompt-engineering-marketing-professionals/">prompt engineering for marketing professionals</a>, and avoid <a href="{B}25-content-writing-mistakes/">25 common content writing mistakes</a>. If your text came from ChatGPT, also strip hidden characters and Markdown symbols with the <a href="{AI}ai-text-cleaner/">AI text cleaner</a>.</p>
''',
        faqs=[
            ("How do I remove line breaks from text copied from a PDF?", "Paste the text into the tool and keep the default mode, Keep paragraphs. It joins the wrapped lines into full sentences, keeps the gap between paragraphs, and rejoins words split with a hyphen at the end of a line. Then copy the clean text."),
            ("Will it remove the spaces between my paragraphs?", "Not in Keep paragraphs mode. A blank line between two blocks of text is treated as a paragraph break and kept. Choose Remove all line breaks if you want one continuous block of text."),
            ("How do I turn a list into comma separated values?", "Choose Replace each line break with my text and type a comma and a space in the box. Each line becomes one item in a single comma separated line, and empty lines are skipped."),
            ("Is my text uploaded anywhere?", "No. The tool runs entirely in your browser with JavaScript. Nothing you paste is sent to a server or stored, so it is safe for private emails and documents."),
        ],
        related=[("10 Easy Tips for Effective Content Writing", "10-easy-tips-for-effective-content-writing"), ("Prompt Engineering for Marketing Professionals", "prompt-engineering-marketing-professionals"),
                 ("25 Content Writing Mistakes", "25-content-writing-mistakes"), ("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-20'
