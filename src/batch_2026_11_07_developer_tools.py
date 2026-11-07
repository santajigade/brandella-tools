"""Batch 10 (2026-11-07): Developer Tools category, first 2 tools.
Facts checked 2026-11-07 against: RFC 8259 (JSON grammar: strings in double quotes only, no comments, no trailing
commas, literals true false null in lowercase, numbers have no leading zeros, plus sign, NaN or Infinity, control
characters in strings must be escaped, object names SHOULD be unique, JSON exchanged between systems MUST be UTF 8),
MDN encodeURIComponent (leaves A to Z a to z 0 to 9 and - _ . ! ~ * ' ( ) unescaped) and encodeURI (also leaves
; / ? : @ & = + $ , # unescaped), RFC 3986 (unreserved set is ALPHA DIGIT - . _ ~, percent encoding uses UTF 8 bytes),
WHATWG URL standard application/x-www-form-urlencoded (space becomes +)."""
import html as _h

T = 'https://brandella.in/tools/developer-tools/'
SC = 'https://brandella.in/tools/schema-generators/'
AN = 'https://brandella.in/tools/analytics-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'
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

def S(i, label): return f'<div class="stat-box"><b id="{i}">0</b><span>{label}</span></div>'
def CK(i, label, on=True): return f'<label class="check"><input id="{i}" type="checkbox"' + (' checked' if on else '') + f'> <span>{label}</span></label>'
PRE = 'style="display:block;margin-top:0;max-height:520px;overflow:auto;word-break:normal;overflow-wrap:anywhere;white-space:pre-wrap"'
SCROLL = 'style="overflow-x:auto;max-height:420px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px;margin-bottom:16px"'

BASEJS = r'''
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
  function fmtN(n){ return Number(n).toLocaleString('en-IN'); }
  function bytes(s){ return new Blob([s]).size; }
  function fmtB(n){ return n < 1024 ? n + ' B' : n < 1048576 ? (n / 1024).toFixed(1) + ' KB' : (n / 1048576).toFixed(2) + ' MB'; }
  function download(name, text, type){
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: (type || 'text/plain') + ';charset=utf-8'}));
    a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. JSON FORMATTER AND VALIDATOR ----------
    JF_SAMPLE = 'Here is the JSON you asked for:\n```json\n{"@context":"https://schema.org","@type":"Product","name":"Organic Green Tea, 100 Bags","sku":"GT-100","gtin13":"8901234567890","image":["https://example.com/img/green-tea.jpg"],"offers":{"@type":"Offer","price":"349.00","priceCurrency":"INR","availability":"https://schema.org/InStock",},"aggregateRating":{"@type":"AggregateRating","ratingValue":4.6,"reviewCount":128},\'inStockOnline\': True}\n```'
    TOOLS.append(dict(
        slug='json-formatter', short='JF', name='JSON Formatter and Validator',
        card='Format, validate, minify and repair JSON, with the exact line of every error and fixes for broken AI output.',
        title='JSON Formatter and Validator: Beautify and Fix JSON',
        desc='Free JSON formatter and validator. Beautify or minify JSON, find the exact line and column of errors, and repair trailing commas and broken AI output.',
        h1='JSON Formatter and Validator',
        lead='Paste any JSON to beautify it, check it against the official standard and see exactly where it breaks. Broken JSON from ChatGPT, APIs or config files is repaired in one step, without changing your data.',
        tool='''<section class="tool" aria-label="JSON formatter and validator" id="jfForm">
    <div class="card" style="min-width:0">
      <h2>Your JSON</h2>
      ''' + F('jfIn', 'Paste JSON', JF_SAMPLE, em='from an API, a file, schema markup or an AI chat', tag='textarea', mono=True, extra=' style="min-height:320px"') + '''
      <div class="row2">''' + F('jfInd', 'Indent', '2', tag='select', opts=[('2', '2 spaces'), ('4', '4 spaces'), ('tab', 'Tabs'), ('0', 'Minify (one line)')]) + '''<div class="field"><label>Options</label>''' + CK('jfSort', 'Sort keys A to Z', False) + CK('jfAscii', 'Escape non English characters', False) + '''</div></div>
      <div class="actions" style="margin:0 0 6px"><button type="button" class="btn btn-sm" id="jfUse">Replace Input With Result</button><button type="button" class="btn btn-sm" id="jfClear">Clear</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('jfKeys', 'Keys') + S('jfDepth', 'Max Depth') + S('jfSize', 'Size') + '''</div>
      <div class="kw-result" id="jfCheck"></div>
      <pre class="code-out" id="jfOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="jfCopy">Copy JSON</button><button class="btn" id="jfDl">Download .json</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function JP(src, lenient){
    var i = 0, fixes = [], dups = [], n = src.length;
    function fix(m){ if (fixes.indexOf(m) < 0) fixes.push(m); }
    function lc(p){ var pre = src.slice(0, p).split('\n'); return {line: pre.length, col: pre[pre.length - 1].length + 1}; }
    function fail(m, p){ var e = new Error(m); e.pos = p === undefined ? i : p; throw e; }
    function ws(){
      for (;;){
        while (i < n && /[ \t\n\r]/.test(src[i])) i++;
        if (i < n && /[\u00a0\u200b\ufeff\u2028\u2029]/.test(src[i])){ if (!lenient) fail('Hidden or non standard space character (' + 'U+' + src.charCodeAt(i).toString(16).toUpperCase() + '). JSON only allows normal spaces, tabs and line breaks here.'); fix('Removed hidden space characters'); i++; continue; }
        if (src[i] === '/' && (src[i + 1] === '/' || src[i + 1] === '*')){
          if (!lenient) fail('Comments are not allowed in JSON.');
          if (src[i + 1] === '/'){ while (i < n && src[i] !== '\n') i++; }
          else { var e = src.indexOf('*/', i + 2); i = e < 0 ? n : e + 2; }
          fix('Removed comments'); continue;
        }
        break;
      }
    }
    var Q = {'"': '"', "'": "'", '\u201c': '\u201d', '\u201d': '\u201d', '\u2018': '\u2019', '\u2019': '\u2019'};
    function str(){
      var open = src[i], close = Q[open], out = '', st = i;
      if (open !== '"'){ if (!lenient) fail(open === "'" ? 'Strings and keys must use double quotes, not single quotes.' : 'Curly or smart quotes are not valid in JSON. Use straight double quotes.'); fix(open === "'" ? 'Changed single quotes to double quotes' : 'Changed curly quotes to straight quotes'); }
      i++;
      for (;;){
        if (i >= n) fail('This string is never closed. Add the missing closing quote.', st);
        var ch = src[i];
        if (ch === close || (close !== '"' && close !== "'" && (ch === '\u201c' || ch === '\u201d') && close === '\u201d')){ i++; return out; }
        if (ch === '\\'){
          var e = src[i + 1];
          if (e === 'u'){ var hx = src.substr(i + 2, 4); if (!/^[0-9a-fA-F]{4}$/.test(hx)) fail('Bad unicode escape. Use \\u followed by 4 hex digits.'); out += String.fromCharCode(parseInt(hx, 16)); i += 6; continue; }
          var m = {'"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t'};
          if (e in m){ out += m[e]; i += 2; continue; }
          if (lenient && e === "'"){ out += "'"; i += 2; fix('Fixed invalid escape characters'); continue; }
          if (!lenient) fail('Invalid escape \\' + (e || '') + ' inside a string. Allowed escapes are \\" \\\\ \\/ \\b \\f \\n \\r \\t and \\u.');
          out += e; i += 2; fix('Fixed invalid escape characters'); continue;
        }
        if (ch.charCodeAt(0) < 32){ if (!lenient) fail('Unescaped line break or control character inside a string. Write it as \\n or \\t.'); fix('Escaped raw line breaks inside strings'); out += ch; i++; continue; }
        out += ch; i++;
      }
    }
    function num(){
      var st = i, m = src.slice(i).match(/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?/);
      if (!m) fail('Unexpected character ' + JSON.stringify(src[i]) + '.');
      var raw = m[0]; i += raw.length;
      if (/^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$/.test(raw)) return {t: 'n', v: raw};
      if (!lenient) fail('Invalid number ' + raw + '. JSON numbers cannot have a plus sign, leading zeros or a dot at the start or end.', st);
      fix('Fixed number formats');
      return {t: 'n', v: String(Number(raw))};
    }
    function word(){
      var m = src.slice(i).match(/^[A-Za-z_$][\w$]*/);
      if (!m) return null;
      var w = m[0], map = {'true': true, 'false': false, 'null': null};
      if (w in map){ i += w.length; return {t: 'l', v: w}; }
      var L = {True: 'true', False: 'false', None: 'null', TRUE: 'true', FALSE: 'false', NULL: 'null', Null: 'null', undefined: 'null', NaN: 'null', Infinity: 'null'};
      if (w in L){ if (!lenient) fail(w + ' is not valid JSON. Use lowercase true, false or null.'); i += w.length; fix('Changed ' + w + ' to ' + L[w]); return {t: 'l', v: L[w]}; }
      return null;
    }
    function val(depth){
      ws(); if (i >= n) fail('The JSON ends too early. Something is missing at the end.');
      var ch = src[i];
      if (ch === '{') return obj(depth + 1);
      if (ch === '[') return arr(depth + 1);
      if (ch in Q) return {t: 's', v: str()};
      if (/[-+\d.]/.test(ch)) return num();
      var w = word(); if (w) return w;
      fail('Unexpected character ' + JSON.stringify(ch) + '. A value must be a string, number, object, array, true, false or null.');
    }
    function sep(close, what){
      ws();
      if (src[i] === ','){ var p = i; i++; ws();
        if (src[i] === close){ if (!lenient) fail('Trailing comma before ' + close + '. Remove the last comma.', p); fix('Removed trailing commas'); return false; }
        if (src[i] === ','){ if (!lenient) fail('Two commas in a row.', i); while (src[i] === ','){ i++; ws(); } fix('Removed extra commas'); if (src[i] === close) return false; }
        return true; }
      if (src[i] === close) return false;
      if (i >= n) fail('Missing ' + close + ' at the end. The ' + what + ' is never closed.');
      if (lenient && (src[i] in Q || /[\w{\[\-]/.test(src[i]))){ fix('Added missing commas'); return true; }
      fail('Expected a comma or ' + close + ' here.');
    }
    function obj(depth){
      var o = {t: 'o', k: [], v: [], d: depth}, seen = {}; i++; ws();
      if (src[i] === '}'){ i++; return o; }
      for (;;){
        ws(); var key, kp = i;
        if (src[i] in Q) key = str();
        else { var m = src.slice(i).match(/^[A-Za-z_$@][\w$@\-]*/);
          if (!m) fail(src[i] === '}' ? 'Trailing comma before }.' : 'Expected a key in double quotes.');
          if (!lenient) fail('Keys must be in double quotes, like "' + m[0] + '".'); key = m[0]; i += m[0].length; fix('Added quotes around keys'); }
        ws(); if (src[i] !== ':'){ if (lenient && src[i] === '='){ fix('Changed = to :'); } else fail('Expected a colon after the key "' + key + '".'); }
        i++;
        if (Object.prototype.hasOwnProperty.call(seen, key)) dups.push([key, lc(kp).line]);
        seen[key] = 1;
        o.k.push(key); o.v.push(val(depth));
        if (!sep('}', 'object')) break;
      }
      i++; return o;
    }
    function arr(depth){
      var a = {t: 'a', v: [], d: depth}; i++; ws();
      if (src[i] === ']'){ i++; return a; }
      for (;;){ ws(); a.v.push(val(depth)); if (!sep(']', 'array')) break; }
      i++; return a;
    }
    try {
      ws(); if (i >= n) fail('There is no JSON here yet.');
      var root = val(0); ws();
      if (i < n){ if (!lenient) fail('Extra text after the end of the JSON. Only one value is allowed.'); fix('Removed extra text after the JSON'); }
      return {ok: true, v: root, fixes: fixes, dups: dups};
    } catch (e){ var p = lc(e.pos); return {ok: false, msg: e.message, pos: e.pos, line: p.line, col: p.col}; }
  }
  function unwrap(s){
    var f = [], t = s, m = t.match(/```[ \t]*(?:json5?|javascript|js)?[ \t]*\r?\n([\s\S]*?)```/i);
    if (m){ t = m[1]; f.push('Removed the Markdown code fence'); }
    var a = t.search(/[\[{]/), ob = t.lastIndexOf('}'), cb = t.lastIndexOf(']'), z = Math.max(ob, cb);
    if (a > 0 && /\S/.test(t.slice(0, a)) && !/^\s*["\d\-tfn]/.test(t)){ t = t.slice(a); z -= a; f.push('Removed text before the JSON'); }
    if (a >= 0 && z >= 0 && /[A-Za-z]/.test(t.slice(z + 1))){ t = t.slice(0, z + 1); f.push('Removed text after the JSON'); }
    return {t: t, f: f};
  }
  function ser(x, ind, lvl, sort, ascii){
    var q = function(s){ var j = JSON.stringify(s); return ascii ? j.replace(/[\u007f-\uffff]/g, function(ch){ return '\\u' + ('000' + ch.charCodeAt(0).toString(16)).slice(-4); }) : j; };
    if (x.t === 's') return q(x.v);
    if (x.t === 'n' || x.t === 'l') return String(x.v);
    var nl = ind ? '\n' : '', pad = ind ? new Array(lvl + 2).join(ind) : '', pad0 = ind ? new Array(lvl + 1).join(ind) : '', colon = ind ? ': ' : ':';
    if (x.t === 'a'){ if (!x.v.length) return '[]'; return '[' + nl + x.v.map(function(y){ return pad + ser(y, ind, lvl + 1, sort, ascii); }).join(',' + nl) + nl + pad0 + ']'; }
    if (!x.k.length) return '{}';
    var idx = x.k.map(function(_, j){ return j; });
    if (sort) idx.sort(function(a, b){ return x.k[a] < x.k[b] ? -1 : x.k[a] > x.k[b] ? 1 : 0; });
    return '{' + nl + idx.map(function(j){ return pad + q(x.k[j]) + colon + ser(x.v[j], ind, lvl + 1, sort, ascii); }).join(',' + nl) + nl + pad0 + '}';
  }
  function walk(x, s){ if (x.t === 'o'){ s.keys += x.k.length; s.depth = Math.max(s.depth, x.d); x.v.forEach(function(y){ walk(y, s); }); } else if (x.t === 'a'){ s.depth = Math.max(s.depth, x.d); x.v.forEach(function(y){ walk(y, s); }); } return s; }
  var last = '';
  function run(){
    var raw = $('jfIn').value, iv = $('jfInd').value, ind = iv === 'tab' ? '\t' : iv === '0' ? '' : new Array(+iv + 1).join(' ');
    if (!raw.trim()){ last = ''; $('jfOut').textContent = ''; $('jfKeys').textContent = '0'; $('jfDepth').textContent = '0'; $('jfSize').textContent = '0 B'; say('jfCheck', '', 'Paste JSON on the left to format and validate it.'); return ''; }
    var strict = JP(raw, false), res = strict, fixes = [];
    if (!strict.ok){
      var u = unwrap(raw), len = JP(u.t, true);
      if (len.ok){ res = len; fixes = u.f.concat(len.fixes); }
    }
    if (!res.ok){
      last = '';
      var lines = raw.split('\n'), L = strict.line, from = Math.max(0, L - 3), snip = [];
      for (var k = from; k < Math.min(lines.length, L + 1); k++){
        var t = lines[k].length > 160 ? lines[k].slice(Math.max(0, (k === L - 1 ? strict.col : 1) - 80), Math.max(0, (k === L - 1 ? strict.col : 1) - 80) + 160) : lines[k];
        snip.push(String(k + 1).padStart(4, ' ') + ' | ' + t);
        if (k === L - 1){ var off = lines[k].length > 160 ? Math.min(strict.col - 1, 79) : strict.col - 1; snip.push('       ' + new Array(off + 1).join(' ') + '^'); }
      }
      $('jfOut').textContent = snip.join('\n');
      $('jfKeys').textContent = '0'; $('jfDepth').textContent = '0'; $('jfSize').textContent = fmtB(bytes(raw));
      say('jfCheck', 'bad', '<strong>Invalid JSON at line ' + strict.line + ', column ' + strict.col + '.</strong> ' + esc(strict.msg) + ' The marker below points to the spot.');
      return '';
    }
    var out = ser(res.v, ind, 0, $('jfSort').checked, $('jfAscii').checked), st = walk(res.v, {keys: 0, depth: 0});
    last = out;
    $('jfOut').textContent = out;
    $('jfKeys').textContent = fmtN(st.keys); $('jfDepth').textContent = st.depth; $('jfSize').textContent = fmtB(bytes(out));
    var dup = res.dups.length ? '<li>Duplicate key ' + res.dups.slice(0, 5).map(function(d){ return c(d[0]) + ' on line ' + d[1]; }).join(', ') + (res.dups.length > 5 ? ' and ' + (res.dups.length - 5) + ' more' : '') + '. Most parsers keep only the last value, so check which one you meant.</li>' : '';
    if (!strict.ok){
      say('jfCheck', 'warn', '<strong>Your input was not valid JSON (line ' + strict.line + ', column ' + strict.col + ': ' + esc(strict.msg) + ') so it was repaired.</strong><ul style="margin:6px 0 0 18px">' + fixes.map(function(f){ return '<li>' + esc(f) + '</li>'; }).join('') + dup + '</ul>The result below is valid JSON. Check it, then copy it or press Replace Input With Result.');
    } else if (dup){
      say('jfCheck', 'warn', '<strong>Valid JSON, with a warning.</strong><ul style="margin:6px 0 0 18px">' + dup + '</ul>');
    } else {
      var kind = res.v.t === 'o' ? 'an object' : res.v.t === 'a' ? 'an array of ' + res.v.v.length + ' item' + (res.v.v.length === 1 ? '' : 's') : 'a single value';
      say('jfCheck', 'ok', '<strong>Valid JSON.</strong> The top level is ' + kind + (st.keys ? ', with ' + fmtN(st.keys) + ' key' + (st.keys === 1 ? '' : 's') + ' in total' : '') + '. Minified it is ' + fmtB(bytes(ser(res.v, '', 0, false, false))) + '.');
    }
    return out;
  }
  var tm; $('jfIn').addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(run, $('jfIn').value.length > 200000 ? 400 : 60); });
  ['jfInd', 'jfSort', 'jfAscii'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('jfUse').addEventListener('click', function(){ if (run()){ $('jfIn').value = last; run(); } });
  $('jfClear').addEventListener('click', function(){ $('jfIn').value = ''; run(); $('jfIn').focus(); });
  $('jfCopy').addEventListener('click', function(){ var o = run(); if (o) copyText(o, 'toast'); });
  $('jfDl').addEventListener('click', function(){ var o = run(); if (o) download('data.json', o, 'application/json'); });
  run();
''',
        content=f'''
    <h2>What Is a JSON Formatter and Validator?</h2>
    <p>JSON is the plain text format that APIs, apps, schema markup, Google Tag Manager and AI tools use to pass data around. It is easy for machines to read, but a single missing quote or extra comma breaks the whole thing, and long JSON on one line is almost impossible for people to read.</p>
    <p>This tool does three jobs at once. It <strong>formats</strong> JSON with clean indentation, <strong>validates</strong> it against the official <a href="https://www.rfc-editor.org/rfc/rfc8259" {EXT}>JSON standard (RFC 8259)</a> and points to the exact line and column of any error, and <strong>repairs</strong> the most common problems, such as the broken JSON that ChatGPT and other AI tools often return. Everything runs in your browser, so private data never leaves your device.</p>

    <h2>How to Use the JSON Formatter</h2>
    <ol>
      <li><strong>Paste your JSON</strong> into the box. You can paste a whole AI answer, including the code fence and the text around it.</li>
      <li><strong>Read the check.</strong> Green means valid. Red shows the line, column and a marker under the problem. Amber means the tool repaired it and lists every fix.</li>
      <li><strong>Pick an indent</strong> of 2 spaces, 4 spaces or tabs, or choose Minify to put it all on one line for production.</li>
      <li><strong>Tick Sort keys</strong> to order keys A to Z, which makes two versions easy to compare.</li>
      <li><strong>Copy or download</strong> the result, or press Replace Input With Result to keep working on the fixed version.</li>
    </ol>

    <h2>Common JSON Errors and What the Tool Does</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Problem', 'Example', 'What happens')}
      <tbody>
        <tr><td>Trailing comma</td><td><code>{{"a": 1,}}</code></td><td>Flagged, then removed</td></tr>
        <tr><td>Single or curly quotes</td><td><code>{{'name': 'Tea'}}</code></td><td>Changed to straight double quotes</td></tr>
        <tr><td>Keys without quotes</td><td><code>{{name: "Tea"}}</code></td><td>Quotes added around the key</td></tr>
        <tr><td>Python style values</td><td><code>True</code>, <code>False</code>, <code>None</code></td><td>Changed to <code>true</code>, <code>false</code>, <code>null</code></td></tr>
        <tr><td>Comments</td><td><code>// note</code> or <code>/* note */</code></td><td>Removed, since JSON has no comments</td></tr>
        <tr><td>Code fence and chat text</td><td><code>```json</code> with text around it</td><td>Only the JSON is kept</td></tr>
        <tr><td>Missing bracket or quote</td><td><code>{{"a": [1, 2}}</code></td><td>Exact line and column shown so you can fix it</td></tr>
        <tr><td>Duplicate keys</td><td><code>{{"id": 1, "id": 2}}</code></td><td>Warning, as most parsers keep only the last one</td></tr>
      </tbody>
    </table></div>
    <p>Repairs never guess at your data. Numbers are kept exactly as written, so long IDs and prices do not lose digits the way they can in some online formatters.</p>

    <h2>Tips for Working With JSON</h2>
    <ul>
      <li><strong>Ask AI tools for JSON only.</strong> Add "Return only valid JSON, no extra text" to your prompt. If it still adds a comment or a trailing comma, paste it here.</li>
      <li><strong>Minify for production, format for people.</strong> Minified JSON is smaller to send, while formatted JSON is easier to review in a pull request.</li>
      <li><strong>Validate schema markup before testing it.</strong> A syntax error stops Google from reading your JSON LD at all, so fix syntax here first, then run Google's Rich Results Test.</li>
      <li><strong>Save files as UTF 8.</strong> The standard requires it when JSON moves between systems, and it keeps accents and Indian scripts intact.</li>
    </ul>

    <h2>Put Your JSON to Work</h2>
    <p>Add structured data with <a href="{B}how-to-add-schema-markup-json-ld/">how to add schema markup with JSON LD</a>, push clean events with <a href="{B}gtm-data-layer-explained/">the GTM data layer explained</a>, or return JSON from your own backend with <a href="{B}rest-api-in-php-without-a-framework/">a REST API in PHP without a framework</a>. Need to send JSON inside a link? Encode it with the <a href="{T}url-encoder-decoder/">URL encoder and decoder</a>.</p>
''',
        faqs=[
            ("Why is my JSON invalid when it looks fine?", "The usual causes are a trailing comma after the last item, single or curly quotes, a missing comma between items, or an unescaped line break inside a string. The validator shows the exact line and column, with a marker under the character that breaks it."),
            ("How do I fix broken JSON from ChatGPT?", "Paste the whole answer here, including the code fence. The tool strips the text around it, removes comments and trailing commas, fixes quotes and Python style True, False and None, then shows valid JSON with a list of every change it made."),
            ("Does formatting change my data?", "No. Only spaces and line breaks change. Keys stay in the same order unless you tick Sort keys, and numbers are kept exactly as written, so long IDs keep every digit."),
            ("Is it safe to paste private JSON here?", "Yes. The formatter runs entirely in your browser. Nothing you paste is uploaded, logged or stored, so API responses, tokens and customer data stay on your device."),
        ],
        related=[("How to Add Schema Markup With JSON LD", "how-to-add-schema-markup-json-ld"), ("GTM Data Layer Explained", "gtm-data-layer-explained"),
                 ("REST API in PHP Without a Framework", "rest-api-in-php-without-a-framework"), ("Build an AI Chatbot With the OpenAI API", "build-ai-chatbot-openai-api")],
    ))

    # ---------- 2. URL ENCODER AND DECODER ----------
    UE_SAMPLE = 'https://www.example.com/go?url=https%3A%2F%2Fbrandella.in%2Ftools%2F%3Futm_source%3Dnewsletter%26utm_medium%3Demail%26utm_campaign%3Ddiwali%2520sale&ref=email+footer'
    TOOLS.append(dict(
        slug='url-encoder-decoder', short='UE', name='URL Encoder and Decoder',
        card='Encode or decode URLs and query strings, unwrap double encoding and see every parameter in a clean table.',
        title='URL Encoder and Decoder: Percent Encode Online Free',
        desc='Free URL encoder and decoder. Percent encode or decode text, links and query strings, fix double encoding and see every URL parameter in a clear table.',
        h1='URL Encoder and Decoder',
        lead='Turn messy links full of %20 and %3A back into readable text, or safely encode text for a URL. Double encoded tracking links are unwrapped, and every parameter is laid out in a table so you can check it.',
        tool='''<section class="tool" aria-label="URL encoder and decoder" id="ueForm">
    <div class="card" style="min-width:0">
      <h2>Input</h2>
      <div class="tabs" id="ueTabs"><button type="button" data-m="dec" class="on">Decode</button><button type="button" data-m="enc">Encode</button></div>
      ''' + F('ueIn', 'Text or URL', UE_SAMPLE, em='one per line for bulk', tag='textarea', mono=True, extra=' style="min-height:170px"') + '''
      <div id="ueEncOpts" style="display:none">''' + F('ueType', 'Encode as', 'comp', tag='select', opts=[('comp', 'Parameter value (encodeURIComponent)'), ('url', 'Full URL (keeps : / ? & =)'), ('form', 'Form data (spaces as +)')]) + CK('ueStrict', "Strict RFC 3986 (also encode ! ' ( ) *)", False) + '''</div>
      <div id="ueDecOpts">''' + CK('uePlus', 'Treat + as a space', True) + CK('ueAll', 'Decode every layer (fixes double encoding)', True) + '''</div>
      ''' + CK('ueLines', 'Process each line separately', True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('ueLayers', 'Layers Decoded') + S('ueParams', 'URL Parameters') + S('ueChars', 'Characters') + '''</div>
      <div class="kw-result" id="ueCheck"></div>
      <pre class="code-out" id="ueOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="ueCopy">Copy Result</button><button class="btn" id="ueSwap">Use Result as Input</button><span class="toast" id="toast">Copied!</span></div>
      <div id="ueBreak"></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var mode = 'dec';
  function dec1(s, plus){
    var bad = 0; if (plus) s = s.replace(/\+/g, ' ');
    var out = s.replace(/(%[0-9A-Fa-f]{2})+/g, function(run){
      try { return decodeURIComponent(run); }
      catch (e){
        var bs = run.match(/%[0-9A-Fa-f]{2}/g).map(function(h){ return parseInt(h.slice(1), 16); });
        try { return new TextDecoder('utf-8', {fatal: true}).decode(new Uint8Array(bs)); } catch (e2){ bad++; return new TextDecoder('utf-8').decode(new Uint8Array(bs)); }
      }
    });
    return {s: out, bad: bad};
  }
  function decode(s, plus, all){
    var layers = 0, bad = 0, cur = s;
    for (var k = 0; k < 6; k++){
      if (!/%[0-9A-Fa-f]{2}/.test(cur) && !(k === 0 && plus && /\+/.test(cur))) break;
      var r = dec1(cur, plus && k === 0); bad += r.bad;
      if (r.s === cur) break;
      cur = r.s; layers++;
      if (!all) break;
    }
    return {s: cur, layers: layers, bad: bad, left: /%[0-9A-Fa-f]{2}/.test(cur)};
  }
  function strictify(s){ return s.replace(/[!'()*]/g, function(ch){ return '%' + ch.charCodeAt(0).toString(16).toUpperCase(); }); }
  function encode(s, type, strict){
    var out;
    try {
      if (type === 'url') out = s.split(/(%[0-9A-Fa-f]{2})/).map(function(p, j){ return j % 2 ? p : encodeURI(p); }).join('');
      else { out = encodeURIComponent(s); if (type === 'form') out = out.replace(/%20/g, '+'); }
    } catch (e){ out = encodeURIComponent(s.replace(/[\ud800-\udfff]/g, '\ufffd')); }
    return strict ? strictify(out) : out;
  }
  function breakdown(txt){
    var m = txt.match(/https?:\/\/[^\s<>"]+/); if (!m) return {h: '', n: 0, warn: []};
    var u; try { u = new URL(m[0]); } catch (e){ return {h: '', n: 0, warn: []}; }
    var rows = [], warn = [], seen = {}, n = 0;
    rows.push(['Protocol', u.protocol.replace(':', '')]); rows.push(['Host', u.host]);
    var path; try { path = decodeURIComponent(u.pathname); } catch (e){ path = u.pathname; }
    rows.push(['Path', path || '/']);
    var q = u.search.slice(1).split('&').filter(Boolean), ps = '';
    q.forEach(function(pair){
      var eq = pair.indexOf('='), k = eq < 0 ? pair : pair.slice(0, eq), val = eq < 0 ? '' : pair.slice(eq + 1);
      var dk = decode(k, true, true).s, dv = decode(val, true, true);
      n++;
      if (seen[dk]) warn.push('The parameter ' + c(dk) + ' appears more than once.'); seen[dk] = 1;
      var dbl = val.match(/%25[0-9A-Fa-f]{2}/);
      if (dbl) warn.push('The value of ' + c(dk) + ' contains double encoded characters such as ' + c(dbl[0]) + '. Encode each part only once so analytics and redirects read it correctly.');
      if (/^utm_/i.test(dk) && /[A-Z]/.test(dv.s)) warn.push(c(dk) + ' contains capital letters. GA4 treats Email and email as different values.');
      var inner = /^https?:\/\//i.test(dv.s) ? ' <em>(a URL inside a URL)</em>' : '';
      ps += '<tr><td><code>' + esc(dk) + '</code></td><td style="overflow-wrap:anywhere">' + esc(dv.s) + inner + '</td></tr>';
    });
    if (u.hash) rows.push(['Fragment', u.hash.slice(1)]);
    var h = '<h3 style="font-size:16px;margin:16px 0 10px">URL Breakdown</h3><div ' + 'style="overflow-x:auto;border:1px solid #e6e6e6;border-radius:10px;margin-bottom:12px"' + '><table class="rtable"><tbody>' + rows.map(function(r){ return '<tr><th style="width:110px">' + r[0] + '</th><td style="overflow-wrap:anywhere">' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table></div>';
    if (n) h += '<div style="overflow-x:auto;max-height:360px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px"><table class="rtable"><thead><tr><th>Parameter</th><th>Decoded value</th></tr></thead><tbody>' + ps + '</tbody></table></div>';
    return {h: h, n: n, warn: warn};
  }
  var last = '';
  function run(){
    var raw = $('ueIn').value, lines = $('ueLines').checked ? raw.split(/\r?\n/) : [raw], out = [], layers = 0, bad = 0, left = 0;
    $('ueEncOpts').style.display = mode === 'enc' ? '' : 'none'; $('ueDecOpts').style.display = mode === 'dec' ? '' : 'none';
    if (!raw.trim()){ last = ''; $('ueOut').textContent = ''; $('ueBreak').innerHTML = ''; ['ueLayers', 'ueParams', 'ueChars'].forEach(function(i){ $(i).textContent = '0'; }); say('ueCheck', '', 'Paste a link or some text to ' + (mode === 'dec' ? 'decode' : 'encode') + ' it.'); return ''; }
    lines.forEach(function(l){
      if (mode === 'dec'){ var r = decode(l, $('uePlus').checked, $('ueAll').checked); out.push(r.s); layers = Math.max(layers, r.layers); bad += r.bad; if (r.left) left++; }
      else out.push(l === '' ? '' : encode(l, $('ueType').value, $('ueStrict').checked));
    });
    last = out.join($('ueLines').checked ? '\n' : '');
    $('ueOut').textContent = last;
    $('ueChars').textContent = fmtN(last.length); $('ueLayers').textContent = mode === 'dec' ? layers : 0;
    var b = breakdown(mode === 'dec' ? raw : last); $('ueParams').textContent = b.n; $('ueBreak').innerHTML = b.h;
    var notes = b.warn.slice();
    if (mode === 'dec'){
      if (bad) notes.unshift('Some percent codes do not form valid UTF 8 characters, so they show as \ufffd. The original text was probably encoded with an old character set.');
      if (left) notes.push('Some percent codes are still left. Tick Decode every layer to unwrap them.');
      if (/%(?![0-9A-Fa-f]{2})/.test(raw)) notes.push('A lone % sign was found that is not followed by two hex digits. It was kept as it is.');
    } else if ($('ueType').value === 'comp' && /^https?:\/\//i.test(raw.trim()) && !$('ueLines').checked){
      notes.push('You are encoding a whole URL as a parameter value. That is right for a redirect or share link, but choose Full URL if you only want to make the link itself safe.');
    }
    var head = mode === 'dec' ? (layers ? '<strong>Decoded ' + (layers > 1 ? layers + ' layers of encoding' : 'the text') + '.</strong>' : '<strong>Nothing to decode.</strong> The text has no percent codes.')
      : '<strong>Encoded ' + (lines.length > 1 ? lines.filter(function(l){ return l; }).length + ' lines' : 'your text') + '.</strong> It is safe to use ' + ($('ueType').value === 'url' ? 'as a link.' : $('ueType').value === 'form' ? 'in form data or a query string.' : 'as a query parameter value.');
    say('ueCheck', notes.length ? 'warn' : 'ok', head + (notes.length ? '<ul style="margin:6px 0 0 18px">' + notes.map(function(x){ return '<li>' + x + '</li>'; }).join('') + '</ul>' : ''));
    return last;
  }
  $('ueTabs').querySelectorAll('button').forEach(function(btn){
    btn.addEventListener('click', function(){
      $('ueTabs').querySelectorAll('button').forEach(function(x){ x.classList.remove('on'); });
      btn.classList.add('on'); mode = btn.getAttribute('data-m'); run();
    });
  });
  $('ueForm').addEventListener('input', run); $('ueForm').addEventListener('change', run);
  $('ueCopy').addEventListener('click', function(){ var o = run(); if (o) copyText(o, 'toast'); });
  $('ueSwap').addEventListener('click', function(){ if (last){ $('ueIn').value = last; run(); } });
  run();
''',
        content=f'''
    <h2>What Is URL Encoding?</h2>
    <p>URLs can only contain a small set of characters. Spaces, accents, emoji and symbols such as <code>&amp;</code>, <code>?</code> and <code>#</code> have to be written as a percent sign plus two hex digits. A space becomes <code>%20</code>, a colon becomes <code>%3A</code> and the rupee sign becomes <code>%E2%82%B9</code>. This is called percent encoding, and it is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986#section-2.1" {EXT}>RFC 3986</a>.</p>
    <p>Decoding does the reverse and turns an unreadable link back into plain text. This tool does both, line by line, and also lays out every part of a URL in a table. It is built for the jobs marketers and developers face every week: checking tracking links, building redirect and share links, and fixing links that were encoded twice.</p>

    <h2>How to Use the URL Encoder and Decoder</h2>
    <ol>
      <li><strong>Choose Decode or Encode</strong> at the top of the input box.</li>
      <li><strong>Paste a link or text.</strong> Put several on separate lines to process them all at once.</li>
      <li><strong>When decoding,</strong> keep Decode every layer ticked to unwrap links that were encoded two or three times, such as <code>%2520</code>.</li>
      <li><strong>When encoding,</strong> pick what the text is for: a parameter value, a full URL, or form data.</li>
      <li><strong>Check the URL breakdown</strong> under the result, then copy it or use it as the new input.</li>
    </ol>

    <h2>Which Encoding Should You Use?</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Option', 'Use it for', 'What stays as is')}
      <tbody>
        <tr><td>Parameter value</td><td>A value after <code>=</code>, such as a URL inside <code>?url=</code> or a campaign name</td><td>Letters, digits and <code>- _ . ! ~ * ' ( )</code></td></tr>
        <tr><td>Full URL</td><td>Making a whole link with spaces or accents safe to share</td><td>Also <code>: / ? # &amp; = + , ; @ $</code>, and existing <code>%XX</code> codes</td></tr>
        <tr><td>Form data</td><td>Text sent like an HTML form, <code>application/x-www-form-urlencoded</code></td><td>Same as parameter value, but spaces become <code>+</code></td></tr>
        <tr><td>Strict RFC 3986</td><td>Signed API requests and systems that reject <code>! ' ( ) *</code></td><td>Only letters, digits and <code>- _ . ~</code></td></tr>
      </tbody>
    </table></div>
    <p>The parameter and full URL options match the browser functions <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent" {EXT}>encodeURIComponent</a> and <code>encodeURI</code>, so the result is exactly what JavaScript would produce. Text is encoded as UTF 8, which is what every modern browser and server expects.</p>

    <h2>Tips for Clean Links</h2>
    <ul>
      <li><strong>Encode once, at the end.</strong> Double encoding, where <code>%20</code> turns into <code>%2520</code>, is the most common reason UTM values look broken in GA4.</li>
      <li><strong>Encode the inner URL in redirects.</strong> When a link carries another link, such as <code>?url=https://...</code>, encode the inner URL as a parameter value, or its own <code>&amp;</code> parts will be read as parameters of the outer link.</li>
      <li><strong>Keep UTM values lowercase.</strong> The breakdown warns you, because analytics treats <code>Email</code> and <code>email</code> as two sources.</li>
      <li><strong>Prefer hyphens or underscores to spaces in slugs.</strong> A clean slug needs no encoding at all and is easier to read and share.</li>
    </ul>

    <h2>Build Better URLs</h2>
    <p>Learn how query strings affect crawling in <a href="{B}url-parameters-explained-do-they-hurt-seo/">URL parameters explained</a>, tag campaigns properly with <a href="{B}utm-parameters-explained/">UTM parameters explained</a>, and plan readable paths with <a href="{B}url-structure-for-ai-seo/">URL structure for AI SEO</a>. Building a campaign link from scratch? Use the <a href="{AN}utm-builder/">UTM builder</a>, and check any JSON payload with the <a href="{T}json-formatter/">JSON formatter and validator</a>.</p>
''',
        faqs=[
            ("What does %20 mean in a URL?", "%20 is the encoded form of a space. Every special character in a URL is written as a percent sign and two hex digits, so %3A is a colon, %2F is a slash and %26 is an ampersand. Decoding turns them back into normal characters."),
            ("What is double encoding and how do I fix it?", "Double encoding happens when already encoded text is encoded again, so %20 becomes %2520. Paste the link here with Decode every layer ticked and the tool unwraps all layers and tells you how many there were."),
            ("Should a space be %20 or +?", "In the path of a URL a space must be %20. In a query string or form data, + is also read as a space by most servers. Use the Form data option if a system expects +, and %20 everywhere else."),
            ("What is the difference between encodeURI and encodeURIComponent?", "encodeURI keeps the characters that give a URL its structure, such as : / ? & and =, so it is for whole links. encodeURIComponent encodes those too, so it is for a single value placed inside a link, such as a redirect target."),
        ],
        related=[("URL Parameters Explained", "url-parameters-explained-do-they-hurt-seo"), ("UTM Parameters Explained", "utm-parameters-explained"),
                 ("URL Structure for AI SEO", "url-structure-for-ai-seo"), ("Generate SEO Friendly URLs in PHP", "generate-seo-friendly-urls-php")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'developer-tools'; t['updated'] = '2026-11-07'
