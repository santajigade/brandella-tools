"""Batch 11 (2026-11-08): Developer Tools category, tools 3 and 4.
Facts checked 2026-11-08 against: RFC 4648 (section 4 base64 alphabet A to Z a to z 0 to 9 + / with = padding,
section 5 base64url uses - and _ instead of + and /), RFC 2045 (MIME base64 lines at most 76 characters),
RFC 7515 and RFC 7519 (JWT parts are base64url without padding, joined by dots; iat, exp, nbf are NumericDate
seconds since 1970 UTC), MDN btoa (throws InvalidCharacterError for characters outside Latin 1, so text is
encoded as UTF 8 bytes first), MDN data URLs (data:[<media-type>][;base64],<data>), Myers 1986 O(ND) diff
algorithm (shortest edit script, the basis of git diff and GNU diff), GNU unified diff format (--- +++ @@ hunks)."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, PRE, th

T = 'https://brandella.in/tools/developer-tools/'
AI = 'https://brandella.in/tools/ai-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 3. DIFF CHECKER ----------
    DC_A = ('Organic green tea, hand picked in Assam.\n'
            'Each box has 100 tea bags.\n'
            'Price: Rs 349 with free delivery on orders above Rs 499.\n'
            'Brew for 3 minutes in water at 80 degrees.\n'
            'Store in a cool, dry place.\n'
            'Best before 12 months from packing.')
    DC_B = ('Organic green tea, hand picked in the hills of Assam.\n'
            'Each box has 100 tea bags.\n'
            'Price: Rs 399 with free delivery on orders above Rs 499.\n'
            'Brew for 2 to 3 minutes in water at 80 degrees.\n'
            'Store in a cool, dry place.\n'
            'Rich in antioxidants and naturally low in caffeine.\n'
            'Best before 18 months from packing.')
    TOOLS.append(dict(
        slug='diff-checker', short='DC', name='Diff Checker',
        card='Compare two texts or code files and see every added, removed and changed line and word, side by side.',
        title='Diff Checker: Compare Two Texts and Find Differences',
        desc='Free diff checker. Compare two texts, code files or AI rewrites and see every added, removed and changed word, side by side or inline, with a unified diff.',
        h1='Diff Checker: Compare Text Online',
        lead='Paste two versions of any text, code or config file and see exactly what changed. Added lines are green, removed lines are red, and the changed words inside each line are highlighted, so nothing slips past you.',
        tool='''<style>
.dfv{border:1px solid #e6e6e6;border-radius:10px;overflow:auto;max-height:560px;margin-bottom:12px;background:#fff}
.dft{border-collapse:collapse;width:100%;font:13px/1.55 Consolas,Monaco,monospace}
.dft.sbs{min-width:620px;table-layout:fixed}
.dft td{padding:1px 8px;vertical-align:top;white-space:pre-wrap;overflow-wrap:anywhere;word-break:normal}
.dft td.ln{color:#999;text-align:right;user-select:none;width:38px;white-space:nowrap;background:#fafafa;border-right:1px solid #eee}
.dft td.sg{width:14px;color:#777;user-select:none;padding:1px 2px}
.dft .del{background:#fdecea}.dft .add{background:#eaf7e0}.dft .emp{background:#f6f6f6}
.dft del,.dfw del{background:#f5b7ae;text-decoration:none;border-radius:2px}
.dft ins,.dfw ins{background:#b9e59a;text-decoration:none;border-radius:2px}
.dft tr.skip td{background:#f2f6fb;color:#5b6b80;text-align:center;font-family:inherit;padding:4px}
.dfw{padding:12px 14px;font:14px/1.7 Consolas,Monaco,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.dfw del{color:#8a1c0e;text-decoration:line-through}.dfw ins{color:#1f5c07}
</style>
<section class="tool" aria-label="Diff checker" id="dcForm">
    <div class="card full" style="min-width:0">
      <h2>Your Two Versions</h2>
      <div class="row2">''' + F('dcA', 'Original text', DC_A, em='the old version', tag='textarea', mono=True, extra=' style="min-height:200px"') + F('dcB', 'Changed text', DC_B, em='the new version', tag='textarea', mono=True, extra=' style="min-height:200px"') + '''</div>
      <div class="row2">''' + F('dcMode', 'Compare by', 'line', tag='select', opts=[('line', 'Lines, with changed words highlighted'), ('word', 'Words, as flowing text'), ('char', 'Characters, for tiny edits')]) + F('dcView', 'Show as', 'auto', tag='select', opts=[('auto', 'Side by side on wide screens'), ('sbs', 'Side by side'), ('inline', 'Inline, one column')]) + '''</div>
      <div style="margin:0 0 12px">''' + CK('dcCase', 'Ignore upper and lower case', False) + CK('dcSpace', 'Ignore extra spaces and indents', False) + CK('dcOnly', 'Show only changes, with 2 lines of context', False) + '''</div>
      <div class="actions" style="margin:0 0 6px"><button type="button" class="btn btn-sm" id="dcSwap">Swap Sides</button><button type="button" class="btn btn-sm" id="dcClear">Clear Both</button></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Differences</h2>
      <div class="stats">''' + S('dcAdd', 'Added') + S('dcDel', 'Removed') + S('dcChg', 'Changed Lines') + S('dcSim', 'Similarity') + '''</div>
      <div class="kw-result" id="dcCheck"></div>
      <div class="dfv" id="dcOut"></div>
      <div class="actions"><button class="btn dark" id="dcCopy">Copy Unified Diff</button><button class="btn" id="dcDl">Download .diff</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function myers(a, b, limit){
    var n = a.length, m = b.length, pre = 0, suf = 0, ops = [], k, x, y, d;
    while (pre < n && pre < m && a[pre] === b[pre]) pre++;
    while (suf < n - pre && suf < m - pre && a[n - 1 - suf] === b[m - 1 - suf]) suf++;
    var A = a.slice(pre, n - suf), Bb = b.slice(pre, m - suf), N = A.length, M = Bb.length, max = N + M, off = max + 1;
    var mid = [], cut = false;
    if (N === 0 || M === 0){ for (x = 0; x < N; x++) mid.push(['-', pre + x]); for (y = 0; y < M; y++) mid.push(['+', pre + y]); }
    else {
      var v = new Int32Array(2 * max + 3), trace = [], D = -1;
      outer: for (d = 0; d <= max; d++){
        if (d > limit){ cut = true; break; }
        trace.push(v.slice(off - d, off + d + 1));
        for (k = -d; k <= d; k += 2){
          x = (k === -d || (k !== d && v[off + k - 1] < v[off + k + 1])) ? v[off + k + 1] : v[off + k - 1] + 1;
          y = x - k;
          while (x < N && y < M && A[x] === Bb[y]){ x++; y++; }
          v[off + k] = x;
          if (x >= N && y >= M){ D = d; break outer; }
        }
      }
      if (cut){ for (x = 0; x < N; x++) mid.push(['-', pre + x]); for (y = 0; y < M; y++) mid.push(['+', pre + y]); }
      else {
        x = N; y = M;
        for (d = D; d > 0; d--){
          var vv = trace[d]; k = x - y;
          var pk = (k === -d || (k !== d && vv[k - 1 + d] < vv[k + 1 + d])) ? k + 1 : k - 1;
          var px = vv[pk + d], py = px - pk;
          while (x > px && y > py){ mid.push(['=', pre + x - 1, pre + y - 1]); x--; y--; }
          if (x === px) mid.push(['+', pre + y - 1]); else mid.push(['-', pre + x - 1]);
          x = px; y = py;
        }
        while (x > 0 && y > 0){ mid.push(['=', pre + x - 1, pre + y - 1]); x--; y--; }
        mid.reverse();
      }
    }
    for (x = 0; x < pre; x++) ops.push(['=', x, x]);
    ops = ops.concat(mid);
    for (x = 0; x < suf; x++) ops.push(['=', n - suf + x, m - suf + x]);
    // within a change block, list removals before additions
    var outOps = [], i = 0;
    while (i < ops.length){
      if (ops[i][0] === '='){ outOps.push(ops[i]); i++; continue; }
      var dels = [], adds = [];
      while (i < ops.length && ops[i][0] !== '='){ (ops[i][0] === '-' ? dels : adds).push(ops[i]); i++; }
      outOps = outOps.concat(dels, adds);
    }
    return {ops: outOps, cut: cut};
  }
  function wtok(s){ return s.match(/\s+|[A-Za-z0-9_À-￿]+|[^\sA-Za-z0-9_À-￿]/g) || []; }
  function keyer(){
    var ic = $('dcCase').checked, is = $('dcSpace').checked;
    return function(s){ if (is) s = s.replace(/\s+/g, ' ').trim(); if (ic) s = s.toLowerCase(); return s; };
  }
  function inner(a, b, kf){
    var ta = wtok(a), tb = wtok(b), r = myers(ta.map(kf), tb.map(kf), 400), L = '', R = '', same = 0;
    if (r.cut) return null;
    r.ops.forEach(function(o){
      if (o[0] === '='){ L += esc(ta[o[1]]); R += esc(tb[o[2]]); if (/\S/.test(ta[o[1]])) same += ta[o[1]].length; }
      else if (o[0] === '-') L += '<del>' + esc(ta[o[1]]) + '</del>';
      else R += '<ins>' + esc(tb[o[1]]) + '</ins>';
    });
    var tot = Math.max(a.replace(/\s/g, '').length, b.replace(/\s/g, '').length, 1);
    return same / tot >= 0.3 ? [L.replace(/<\/del><del>/g, ''), R.replace(/<\/ins><ins>/g, '')] : null;
  }
  function split(s){ var l = s.replace(/\r\n?/g, '\n').split('\n'); if (l.length > 1 && l[l.length - 1] === '') l.pop(); return s === '' ? [] : l; }
  function unified(la, lb, ops){
    var out = ['--- original', '+++ changed'], C = 3, n = ops.length, ab = [], bb = [], ca0 = 0, cb0 = 0, idx = [];
    ops.forEach(function(o, j){ ab.push(ca0); bb.push(cb0); if (o[0] !== '+') ca0++; if (o[0] !== '-') cb0++; if (o[0] !== '=') idx.push(j); });
    if (!idx.length) return '';
    var groups = [], s = idx[0], e = idx[0];
    for (var q = 1; q < idx.length; q++){ if (idx[q] - e <= 2 * C) e = idx[q]; else { groups.push([s, e]); s = e = idx[q]; } }
    groups.push([s, e]);
    groups.forEach(function(g){
      var a0 = Math.max(0, g[0] - C), a1 = Math.min(n - 1, g[1] + C), body = [], ca = 0, cb = 0;
      for (var j = a0; j <= a1; j++){
        var o = ops[j];
        if (o[0] === '='){ body.push(' ' + la[o[1]]); ca++; cb++; }
        else if (o[0] === '-'){ body.push('-' + la[o[1]]); ca++; }
        else { body.push('+' + lb[o[1]]); cb++; }
      }
      var sa = ca ? ab[a0] + 1 : ab[a0], sb = cb ? bb[a0] + 1 : bb[a0];
      out.push('@@ -' + sa + (ca === 1 ? '' : ',' + ca) + ' +' + sb + (cb === 1 ? '' : ',' + cb) + ' @@');
      out = out.concat(body);
    });
    return out.join('\n') + '\n';
  }
  var patch = '';
  function run(){
    var a = $('dcA').value, b = $('dcB').value, kf = keyer(), mode = $('dcMode').value;
    var view = $('dcView').value; if (view === 'auto') view = window.innerWidth >= 760 ? 'sbs' : 'inline';
    var la = split(a), lb = split(b), lr = myers(la.map(kf), lb.map(kf), 3000), ops = lr.ops;
    patch = unified(la, lb, ops);
    if (!a && !b){ $('dcOut').innerHTML = '<p class="empty" style="padding:12px">Paste two versions above to compare them.</p>'; ['dcAdd', 'dcDel', 'dcChg'].forEach(function(id){ $(id).textContent = '0'; }); $('dcSim').textContent = '0%'; say('dcCheck', '', 'Paste the original text on the left and the changed text on the right.'); return; }
    var added = 0, removed = 0, changed = 0, i = 0;
    var blocks = [];
    while (i < ops.length){
      if (ops[i][0] === '='){ blocks.push({t: '=', a: ops[i][1], b: ops[i][2]}); i++; continue; }
      var d = [], ad = [];
      while (i < ops.length && ops[i][0] === '-'){ d.push(ops[i][1]); i++; }
      while (i < ops.length && ops[i][0] === '+'){ ad.push(ops[i][1]); i++; }
      blocks.push({t: 'c', d: d, ad: ad});
    }
    var wa = wtok(a).filter(function(t){ return /\S/.test(t); }), wb = wtok(b).filter(function(t){ return /\S/.test(t); });
    var wr = myers(wa.map(kf), wb.map(kf), 4000), wsame = 0, wadd = 0, wdel = 0;
    wr.ops.forEach(function(o){ if (o[0] === '=') wsame++; else if (o[0] === '+') wadd++; else wdel++; });
    var sim = wa.length + wb.length ? Math.round(200 * wsame / (wa.length + wb.length)) : 100;
    var h = '';
    if (mode === 'line'){
      var rows = [];
      blocks.forEach(function(bk){
        if (bk.t === '='){ rows.push({t: '=', a: bk.a, b: bk.b}); return; }
        var ap = 0, D = bk.d, AD = bk.ad;
        D.forEach(function(x){
          var hit = -1, hl = null;
          for (var y = ap; y < Math.min(AD.length, ap + 60); y++){ hl = inner(la[x], lb[AD[y]], kf); if (hl){ hit = y; break; } }
          if (hit < 0){ rows.push({t: 'c', a: x, b: null}); removed++; return; }
          for (; ap < hit; ap++){ rows.push({t: 'c', a: null, b: AD[ap]}); added++; }
          rows.push({t: 'c', a: x, b: AD[hit], hl: hl}); changed++; ap = hit + 1;
        });
        for (; ap < AD.length; ap++){ rows.push({t: 'c', a: null, b: AD[ap]}); added++; }
      });
      var show = rows.map(function(){ return true; });
      if ($('dcOnly').checked){
        show = rows.map(function(r, j){ for (var q = Math.max(0, j - 2); q <= Math.min(rows.length - 1, j + 2); q++) if (rows[q].t === 'c') return true; return false; });
      }
      var sbs = view === 'sbs', body = '', skip = 0;
      function flush(){ if (skip){ body += '<tr class="skip"><td colspan="' + (sbs ? 6 : 4) + '">' + skip + ' unchanged line' + (skip === 1 ? '' : 's') + ' hidden</td></tr>'; skip = 0; } }
      rows.forEach(function(r, j){
        if (!show[j]){ skip++; return; }
        flush();
        var ta = r.a !== null ? la[r.a] : '', tb = r.b !== null ? lb[r.b] : '';
        var ha = r.hl ? r.hl[0] : esc(ta), hb = r.hl ? r.hl[1] : esc(tb);
        if (sbs){
          if (r.t === '=') body += '<tr><td class="ln">' + (r.a + 1) + '</td><td class="sg"></td><td>' + esc(ta) + '</td><td class="ln">' + (r.b + 1) + '</td><td class="sg"></td><td>' + esc(tb) + '</td></tr>';
          else body += '<tr>' + (r.a !== null ? '<td class="ln">' + (r.a + 1) + '</td><td class="sg del">−</td><td class="del">' + ha + '</td>' : '<td class="ln"></td><td class="sg emp"></td><td class="emp"></td>')
            + (r.b !== null ? '<td class="ln">' + (r.b + 1) + '</td><td class="sg add">+</td><td class="add">' + hb + '</td>' : '<td class="ln"></td><td class="sg emp"></td><td class="emp"></td>') + '</tr>';
        } else {
          if (r.t === '=') body += '<tr><td class="ln">' + (r.a + 1) + '</td><td class="ln">' + (r.b + 1) + '</td><td class="sg"></td><td>' + esc(ta) + '</td></tr>';
          else {
            if (r.a !== null) body += '<tr class="del"><td class="ln">' + (r.a + 1) + '</td><td class="ln"></td><td class="sg">−</td><td>' + ha + '</td></tr>';
            if (r.b !== null) body += '<tr class="add"><td class="ln"></td><td class="ln">' + (r.b + 1) + '</td><td class="sg">+</td><td>' + hb + '</td></tr>';
          }
        }
      });
      flush();
      h = '<table class="dft' + (sbs ? ' sbs' : '') + '">' + (sbs ? '<colgroup><col style="width:42px"><col style="width:16px"><col><col style="width:42px"><col style="width:16px"><col></colgroup>' : '') + '<tbody>' + body + '</tbody></table>';
      $('dcAdd').textContent = fmtN(added) + ' line' + (added === 1 ? '' : 's'); $('dcDel').textContent = fmtN(removed) + ' line' + (removed === 1 ? '' : 's'); $('dcChg').textContent = fmtN(changed);
    } else {
      var ta2 = mode === 'char' ? Array.from(a) : wtok(a), tb2 = mode === 'char' ? Array.from(b) : wtok(b);
      var big = mode === 'char' && ta2.length + tb2.length > 60000;
      var r2 = big ? {ops: [], cut: true} : myers(ta2.map(kf), tb2.map(kf), 6000), out = '', ca = 0, cd = 0;
      if (r2.cut){ out = '<em>These texts are too long or too different to compare by ' + (mode === 'char' ? 'character' : 'word') + '. Choose Lines instead.</em>'; }
      else r2.ops.forEach(function(o){
        if (o[0] === '=') out += esc(ta2[o[1]]);
        else if (o[0] === '-'){ out += '<del>' + esc(ta2[o[1]]) + '</del>'; if (/\S/.test(ta2[o[1]])) cd++; }
        else { out += '<ins>' + esc(tb2[o[1]]) + '</ins>'; if (/\S/.test(tb2[o[1]])) ca++; }
      });
      h = '<div class="dfw">' + out.replace(/<\/del><del>/g, '').replace(/<\/ins><ins>/g, '') + '</div>';
      var unit = mode === 'char' ? ' char' : ' word';
      $('dcAdd').textContent = fmtN(ca) + unit + (ca === 1 ? '' : 's'); $('dcDel').textContent = fmtN(cd) + unit + (cd === 1 ? '' : 's');
      blocks.forEach(function(bk){ if (bk.t === 'c') changed += Math.max(bk.d.length, bk.ad.length); });
      $('dcChg').textContent = fmtN(changed);
    }
    $('dcSim').textContent = sim + '%';
    $('dcOut').innerHTML = h;
    var opts = ($('dcCase').checked || $('dcSpace').checked) ? ' (ignoring ' + [$('dcCase').checked ? 'case' : '', $('dcSpace').checked ? 'extra spaces' : ''].filter(Boolean).join(' and ') + ')' : '';
    if (!patch) say('dcCheck', 'ok', '<strong>The two versions are identical' + opts + '.</strong> There is nothing to change.');
    else say('dcCheck', 'warn', '<strong>' + sim + '% similar' + opts + '.</strong> ' + fmtN(wadd) + ' word' + (wadd === 1 ? '' : 's') + ' added and ' + fmtN(wdel) + ' removed across ' + fmtN(la.length) + ' original and ' + fmtN(lb.length) + ' changed lines.' + (lr.cut ? ' The files are very different, so the line view shows them as fully replaced.' : ''));
  }
  var tm; ['dcA', 'dcB'].forEach(function(id){ $(id).addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(run, ($('dcA').value.length + $('dcB').value.length) > 100000 ? 400 : 80); }); });
  ['dcMode', 'dcView', 'dcCase', 'dcSpace', 'dcOnly'].forEach(function(id){ $(id).addEventListener('change', run); });
  window.addEventListener('resize', function(){ if ($('dcView').value === 'auto'){ clearTimeout(tm); tm = setTimeout(run, 150); } });
  $('dcSwap').addEventListener('click', function(){ var t = $('dcA').value; $('dcA').value = $('dcB').value; $('dcB').value = t; run(); });
  $('dcClear').addEventListener('click', function(){ $('dcA').value = ''; $('dcB').value = ''; run(); $('dcA').focus(); });
  $('dcCopy').addEventListener('click', function(){ run(); if (patch) copyText(patch, 'toast'); else say('dcCheck', 'ok', '<strong>No differences to copy.</strong> The two versions are identical.'); });
  $('dcDl').addEventListener('click', function(){ run(); if (patch) download('changes.diff', patch, 'text/x-diff'); });
  run();
''',
        content=f'''
    <h2>What Is a Diff Checker?</h2>
    <p>A diff checker compares two versions of a text and shows exactly what changed between them. It is the same idea programmers use in Git, where every commit is shown as lines added and lines removed, but it works on anything you can paste: articles, product descriptions, contracts, code, robots.txt files, prompts or JSON.</p>
    <p>This tool uses the Myers diff algorithm, the same method behind <code>git diff</code>, so it finds the smallest set of changes that turns one version into the other. Inside each changed line it also highlights the exact words that differ, which saves you from reading two long lines side by side. It is especially handy for checking what an AI tool really changed when you asked it to edit or rewrite your text. Everything runs in your browser, so private drafts never leave your device.</p>

    <h2>How to Use the Diff Checker</h2>
    <ol>
      <li><strong>Paste the original</strong> into the left box and the <strong>changed version</strong> into the right box.</li>
      <li><strong>Read the result.</strong> Red lines were removed, green lines were added, and the darker highlight marks the exact words that changed.</li>
      <li><strong>Choose how to compare.</strong> Lines suits code and lists, Words suits paragraphs of prose, and Characters suits short strings such as URLs or IDs.</li>
      <li><strong>Turn on options</strong> to ignore case or extra spaces, or to show only the changes in a long file.</li>
      <li><strong>Copy the unified diff</strong> to share the changes with a developer, or paste it into a ticket or pull request.</li>
    </ol>

    <h2>Which Compare Mode Should You Use?</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Mode', 'Best for', 'What you see')}
      <tbody>
        <tr><td>Lines</td><td>Code, config files, CSV rows, lists, robots.txt</td><td>Each line marked as same, added or removed, with changed words highlighted</td></tr>
        <tr><td>Words</td><td>Articles, emails, AI rewrites, legal text</td><td>The text as one flowing piece, with removed words struck in red and new words in green</td></tr>
        <tr><td>Characters</td><td>URLs, product codes, titles, single sentences</td><td>Every single letter that was added or removed</td></tr>
      </tbody>
    </table></div>
    <p>The similarity score compares the words in both versions. 100% means the words are the same, and a low score means most of the text was rewritten. The unified diff uses the standard <code>---</code>, <code>+++</code> and <code>@@</code> format with 3 lines of context, which <code>git apply</code> and the <a href="https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html" {EXT}>GNU patch tools</a> understand.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Check AI edits before you publish.</strong> Ask an AI tool to fix grammar, then compare its answer with your draft. You will see at once if it quietly changed a price, a name or a claim.</li>
      <li><strong>Review content refreshes.</strong> Compare the old and new versions of an article to confirm the key facts, headings and internal links you wanted are still there.</li>
      <li><strong>Ignore spaces for code.</strong> Tick the spaces option when only the indentation changed, so the real edits stand out.</li>
      <li><strong>Use Show only changes for long files.</strong> Unchanged parts fold away and you can jump straight to the lines that matter.</li>
    </ul>

    <h2>Keep Your Content in Shape</h2>
    <p>Updating old pages? Read <a href="{B}how-to-refresh-old-content-without-losing-rankings/">how to refresh old content without losing rankings</a> and follow <a href="{B}google-ai-content-guidelines-2026/">Google's AI content guidelines</a> when you edit with AI. Cleaning up text that came from ChatGPT first? Run it through the <a href="{AI}ai-text-cleaner/">AI text cleaner</a>, and compare two JSON files after formatting them with the <a href="{T}json-formatter/">JSON formatter</a>.</p>
''',
        faqs=[
            ("How do I compare two texts for differences?", "Paste the first version into the left box and the second into the right box. The diff checker shows removed lines in red, added lines in green and highlights the exact changed words inside each line. You can switch to word or character mode for prose and short strings."),
            ("Can I see what ChatGPT changed in my text?", "Yes. Paste your original draft on the left and the AI edited version on the right, then choose Words. Every removed and added word is highlighted, so you can spot changed facts, numbers or tone before you publish."),
            ("What is a unified diff?", "It is the standard text format for changes, used by Git and patch tools. Lines starting with a minus were removed, lines starting with a plus were added, and each block starts with an @@ line showing where it sits in both files."),
            ("Is my text uploaded anywhere?", "No. The comparison runs entirely in your browser. Nothing you paste is sent to a server or stored, so it is safe for private documents and code."),
        ],
        related=[("How to Refresh Old Content Without Losing Rankings", "how-to-refresh-old-content-without-losing-rankings"), ("Content Audit Explained", "content-audit-explained-improve-rankings"),
                 ("Google AI Content Guidelines 2026", "google-ai-content-guidelines-2026"), ("Content Decay Explained", "content-decay-explained-why-rankings-drop")],
    ))

    # ---------- 4. BASE64 ENCODER AND DECODER ----------
    B64_SAMPLE = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEwMjQiLCJuYW1lIjoiUHJpeWEgU2hhcm1hIiwiZW1haWwiOiJwcml5YUBleGFtcGxlLmNvbSIsInJvbGUiOiJlZGl0b3IiLCJpYXQiOjE3OTM4MzY4MDAsImV4cCI6MTc5MzkyMzIwMH0.Xk3vQ9mZb2LwT7rN1cYpH8sJdF4gA6eU0oRtV5iKqWE'
    TOOLS.append(dict(
        slug='base64-encoder-decoder', short='B64', name='Base64 Encoder and Decoder',
        card='Encode and decode Base64 and base64url, read JWT tokens, and turn images into data URIs, with full UTF 8 support.',
        title='Base64 Encoder and Decoder: Decode, Encode and JWT',
        desc='Free Base64 encoder and decoder with UTF 8 support. Decode base64url and JWT tokens, preview images, and convert files to Base64 data URIs for HTML and CSS.',
        h1='Base64 Encoder and Decoder',
        lead='Decode any Base64 string into readable text, an image or a file, or encode text and files to Base64. JWT tokens are split into header and payload with readable dates, and images become ready to paste data URIs.',
        tool='''<section class="tool" aria-label="Base64 encoder and decoder" id="b6Form">
    <div class="card" style="min-width:0">
      <h2>Input</h2>
      <div class="tabs" id="b6Tabs"><button type="button" data-m="dec" class="on">Decode</button><button type="button" data-m="enc">Encode Text</button><button type="button" data-m="file">File to Base64</button></div>
      <div id="b6TextBox">''' + F('b6In', 'Base64, JWT or data URI', B64_SAMPLE, em='spaces and line breaks are ignored', tag='textarea', mono=True, extra=' style="min-height:190px"') + '''</div>
      <div id="b6FileBox" style="display:none"><div class="field"><label for="b6File">Choose a file <em>image, font, PDF or any file, it stays on your device</em></label><input id="b6File" type="file"></div><p class="empty" id="b6FileInfo" style="padding:4px 0 10px">No file chosen yet.</p></div>
      <div id="b6EncOpts" style="display:none">''' + CK('b6Url', 'URL safe (base64url: <code>-</code> and <code>_</code> instead of <code>+</code> and <code>/</code>)', False) + CK('b6Pad', 'Keep <code>=</code> padding at the end', True) + CK('b6Wrap', 'Break lines every 76 characters, as in email (MIME)', False) + '''</div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('b6InSize', 'Input') + S('b6OutSize', 'Output') + S('b6Type', 'Detected') + '''</div>
      <div class="kw-result" id="b6Check"></div>
      <div id="b6Extra"></div>
      <pre class="code-out" id="b6Out" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="b6Copy">Copy Result</button><button class="btn" id="b6Dl">Download</button><button class="btn" id="b6Swap">Use Result as Input</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var mode = 'dec', last = '', lastBytes = null, lastName = 'decoded.bin', lastMime = 'application/octet-stream', fileBytes = null, fileName = '', fileMime = '';
  function toB64(u8){ var s = '', CH = 0x8000; for (var i = 0; i < u8.length; i += CH) s += String.fromCharCode.apply(null, u8.subarray(i, i + CH)); return btoa(s); }
  function fromB64(s){ var bin = atob(s), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; }
  function enc(u8){
    var s = toB64(u8);
    if ($('b6Url').checked) s = s.replace(/\+/g, '-').replace(/\//g, '_');
    if (!$('b6Pad').checked) s = s.replace(/=+$/, '');
    if ($('b6Wrap').checked) s = s.replace(/(.{76})(?=.)/g, '$1\n');
    return s;
  }
  function clean(raw){
    var s = raw.trim(), info = {dataMime: ''};
    var m = s.match(/^data:([^;,]*)((?:;[^;,]*)*?);base64,/i);
    if (m){ info.dataMime = m[1] || 'text/plain'; s = s.slice(m[0].length); }
    s = s.replace(/\s+/g, '');
    try { if (/%[0-9A-Fa-f]{2}/.test(s)){ s = decodeURIComponent(s); info.pct = true; } } catch (e){}
    info.url = /[-_]/.test(s); info.std = /[+\/]/.test(s);
    var bad = s.search(/[^A-Za-z0-9+\/=_-]/);
    if (bad >= 0) return {err: 'The character ' + JSON.stringify(s[bad]) + ' at position ' + (bad + 1) + ' is not part of Base64. Base64 only uses A to Z, a to z, 0 to 9, + and / (or - and _ in the URL safe version), with = at the end.'};
    var eq = s.indexOf('=');
    if (eq >= 0 && /[^=]/.test(s.slice(eq))) return {err: 'An = sign appears in the middle, at position ' + (eq + 1) + '. Padding is only allowed at the very end. This often means two Base64 strings were joined together.'};
    var body = s.replace(/=+$/, '');
    if (body.length % 4 === 1) return {err: 'The length does not work for Base64 (' + body.length + ' characters, one too many or a few missing). Part of the string was probably cut off when it was copied.'};
    info.padFixed = (s.length % 4 !== 0);
    body = body.replace(/-/g, '+').replace(/_/g, '/');
    while (body.length % 4) body += '=';
    info.b64 = body; return info;
  }
  var SIG = [[[0x89, 0x50, 0x4E, 0x47], 'image/png', 'PNG image', 'png'], [[0xFF, 0xD8, 0xFF], 'image/jpeg', 'JPEG image', 'jpg'], [[0x47, 0x49, 0x46, 0x38], 'image/gif', 'GIF image', 'gif'],
    [[0x25, 0x50, 0x44, 0x46], 'application/pdf', 'PDF', 'pdf'], [[0x50, 0x4B, 0x03, 0x04], 'application/zip', 'ZIP or Office file', 'zip'], [[0x1F, 0x8B], 'application/gzip', 'Gzip file', 'gz'],
    [[0x77, 0x4F, 0x46, 0x32], 'font/woff2', 'WOFF2 font', 'woff2'], [[0x77, 0x4F, 0x46, 0x46], 'font/woff', 'WOFF font', 'woff'], [[0x00, 0x00, 0x01, 0x00], 'image/x-icon', 'ICO icon', 'ico']];
  function sniff(u){
    if (u.length > 11 && u[0] === 0x52 && u[1] === 0x49 && u[2] === 0x46 && u[3] === 0x46 && u[8] === 0x57 && u[9] === 0x45 && u[10] === 0x42 && u[11] === 0x50) return ['image/webp', 'WebP image', 'webp'];
    if (u.length > 11 && u[4] === 0x66 && u[5] === 0x74 && u[6] === 0x79 && u[7] === 0x70 && String.fromCharCode(u[8], u[9], u[10], u[11]) === 'avif') return ['image/avif', 'AVIF image', 'avif'];
    for (var i = 0; i < SIG.length; i++){ var s = SIG[i][0], ok = u.length >= s.length; for (var j = 0; ok && j < s.length; j++) if (u[j] !== s[j]) ok = false; if (ok) return SIG[i].slice(1); }
    return null;
  }
  function utf8(u){ try { var t = new TextDecoder('utf-8', {fatal: true}).decode(u); var ctl = (t.match(/[\u0000-\u0008\u000e-\u001f\u007f]/g) || []).length; return ctl > Math.max(2, t.length / 50) ? null : t; } catch (e){ return null; } }
  function hex(u){ var o = []; for (var i = 0; i < Math.min(u.length, 48); i++) o.push(('0' + u[i].toString(16)).slice(-2)); return o.join(' ').replace(/((?:\S\S ){16})/g, '$1\n').trim() + (u.length > 48 ? ' ...' : ''); }
  function claimRow(k, v){
    var note = '';
    if ((k === 'exp' || k === 'iat' || k === 'nbf' || k === 'auth_time') && typeof v === 'number'){
      var d = new Date(v * 1000), now = Date.now(), diff = Math.round((v * 1000 - now) / 60000), rel = Math.abs(diff) < 120 ? Math.abs(diff) + ' minutes' : Math.abs(diff) < 2880 ? Math.round(Math.abs(diff) / 60) + ' hours' : Math.round(Math.abs(diff) / 1440) + ' days';
      note = d.toUTCString().replace('GMT', 'UTC') + ' (' + (diff >= 0 ? 'in ' + rel : rel + ' ago') + ')';
      if (k === 'exp') note += diff < 0 ? ' <strong style="color:#c0321a">Expired</strong>' : ' <strong style="color:#2f7a0c">Still valid</strong>';
      if (k === 'nbf' && diff > 0) note += ' <strong style="color:#c47a00">Not valid yet</strong>';
    }
    var N = {iss: 'Issuer', sub: 'Subject (user)', aud: 'Audience', exp: 'Expires', nbf: 'Not before', iat: 'Issued at', jti: 'Token ID', alg: 'Algorithm', typ: 'Type', kid: 'Key ID'};
    return '<tr><td><code>' + esc(k) + '</code>' + (N[k] ? '<br><small>' + N[k] + '</small>' : '') + '</td><td style="word-break:break-all">' + esc(typeof v === 'string' ? v : JSON.stringify(v)) + (note ? '<br><small>' + note + '</small>' : '') + '</td></tr>';
  }
  function jwt(s){
    var p = s.trim().split('.');
    if (p.length !== 3 || !/^[A-Za-z0-9_-]+$/.test(p[0]) || !/^[A-Za-z0-9_-]+$/.test(p[1]) || !/^[A-Za-z0-9_-]*$/.test(p[2])) return null;
    try {
      var h = JSON.parse(utf8(fromB64(clean(p[0]).b64))), pl = JSON.parse(utf8(fromB64(clean(p[1]).b64)));
      if (!h || typeof h !== 'object' || !h.alg) return null;
      return {h: h, p: pl, sig: p[2]};
    } catch (e){ return null; }
  }
  function setStats(a, b, t){ $('b6InSize').textContent = a; $('b6OutSize').textContent = b; $('b6Type').textContent = t; }
  function run(){
    $('b6Extra').innerHTML = ''; lastBytes = null; last = '';
    if (mode === 'file'){
      if (!fileBytes){ $('b6Out').textContent = ''; setStats('0 B', '0 B', 'None'); say('b6Check', '', 'Choose a file to turn it into Base64 and a data URI.'); return ''; }
      var b = enc(fileBytes), mime = fileMime || (sniff(fileBytes) || ['application/octet-stream'])[0], plain = toB64(fileBytes), uri = 'data:' + mime + ';base64,' + plain;
      last = b;
      $('b6Out').textContent = b;
      setStats(fmtB(fileBytes.length), fmtB(b.length), (sniff(fileBytes) || [0, mime.split('/')[1] || 'File'])[1]);
      var img = /^image\//.test(mime);
      var snippets = [['Data URI', uri]];
      if (img){ snippets.push(['HTML img tag', '<img src="' + uri + '" alt="" width="" height="">']); snippets.push(['CSS background', 'background-image: url("' + uri + '");']); }
      $('b6Extra').innerHTML = (img ? '<p style="margin:0 0 10px"><img src="' + uri + '" alt="Preview of the chosen image" style="max-width:100%;max-height:180px;border:1px solid #e6e6e6;border-radius:8px;background:#fff"></p>' : '')
        + snippets.map(function(s, i){ return '<div class="field"><label>' + s[0] + ' <button type="button" class="btn btn-sm" data-cp="' + i + '" style="margin-left:6px">Copy</button></label><textarea readonly class="mono" spellcheck="false" style="min-height:64px">' + esc(s[1].length > 4000 ? s[1].slice(0, 4000) + '...' : s[1]) + '</textarea></div>'; }).join('');
      $('b6Extra').querySelectorAll('[data-cp]').forEach(function(btn){ btn.addEventListener('click', function(){ copyText(snippets[+btn.getAttribute('data-cp')][1], 'toast'); }); });
      var grow = Math.round((plain.length / fileBytes.length - 1) * 100);
      say('b6Check', fileBytes.length > 10240 ? 'warn' : 'ok', '<strong>Encoded ' + esc(fileName) + '.</strong> Base64 is ' + grow + '% larger than the file.' + (fileBytes.length > 10240 ? ' For files over about 10 KB a normal file link is usually faster, because the browser can cache it. Inline Base64 works best for small icons and logos.' : ''));
      return last;
    }
    var raw = $('b6In').value;
    if (!raw.trim()){ $('b6Out').textContent = ''; setStats('0 B', '0 B', 'None'); say('b6Check', '', mode === 'enc' ? 'Type or paste text to encode it.' : 'Paste a Base64 string, a JWT token or a data URI to decode it.'); return ''; }
    if (mode === 'enc'){
      var u = new TextEncoder().encode(raw);
      last = enc(u); $('b6Out').textContent = last;
      setStats(fmtB(u.length), fmtB(last.length), /[^\x00-\x7f]/.test(raw) ? 'UTF 8 text' : 'Text');
      say('b6Check', 'ok', '<strong>Encoded ' + fmtN(u.length) + ' bytes into ' + fmtN(last.replace(/\n/g, '').length) + ' Base64 characters.</strong>' + (/[^\x00-\xff]/.test(raw) ? ' Your text has characters such as ₹ or Indian scripts, so it was encoded as UTF 8. Plain <code>btoa()</code> would fail on this text.' : '') + ($('b6Url').checked ? ' URL safe, ready for links, file names and JWT parts.' : ''));
      return last;
    }
    var j = jwt(raw);
    if (j){
      last = JSON.stringify(j.p, null, 2); $('b6Out').textContent = last;
      setStats(fmtB(raw.trim().length), fmtB(last.length), 'JWT token');
      var rows = Object.keys(j.h).map(function(k){ return claimRow(k, j.h[k]); }).join(''), prow = Object.keys(j.p).map(function(k){ return claimRow(k, j.p[k]); }).join('');
      $('b6Extra').innerHTML = '<div style="overflow-x:auto;margin-bottom:12px"><table class="rtable"><thead><tr><th colspan="2">Header</th></tr></thead><tbody>' + rows + '</tbody><thead><tr><th colspan="2">Payload</th></tr></thead><tbody>' + prow + '</tbody></table></div>';
      var expd = typeof j.p.exp === 'number' && j.p.exp * 1000 < Date.now();
      say('b6Check', expd || j.h.alg === 'none' ? 'warn' : 'ok', '<strong>This is a JWT token signed with ' + esc(String(j.h.alg)) + '.</strong> The payload is shown below as JSON.' + (expd ? ' It has expired, so a server will reject it.' : '') + (j.h.alg === 'none' ? ' It uses <code>alg: none</code>, which means it is not signed at all and must never be trusted.' : '') + ' Decoding does not check the signature, and anyone can read a JWT, so never put passwords or secrets inside one.');
      return last;
    }
    var c = clean(raw);
    if (c.err){ $('b6Out').textContent = ''; setStats(fmtB(raw.length), '0 B', 'Invalid'); say('b6Check', 'bad', '<strong>Not valid Base64.</strong> ' + esc(c.err)); return ''; }
    var u8 = fromB64(c.b64), sn = sniff(u8), txt = sn ? null : utf8(u8), notes = [];
    if (c.url) notes.push('It uses the URL safe alphabet (base64url).');
    if (c.padFixed) notes.push('The = padding at the end was missing, so it was added.');
    if (c.pct) notes.push('It was also URL encoded, so the %XX codes were decoded first.');
    if (c.url && c.std) notes.push('It mixes both alphabets (+ / and - _), which usually means it was edited by hand.');
    if (txt !== null && !c.dataMime || (txt !== null && /^text\/|json|xml|svg/.test(c.dataMime))){
      var t2 = txt;
      try { var pj = JSON.parse(t2); if (pj && typeof pj === 'object'){ t2 = JSON.stringify(pj, null, 2); notes.push('The text is JSON, so it was formatted.'); } } catch (e){}
      last = t2; $('b6Out').textContent = t2; lastBytes = u8; lastName = 'decoded.txt'; lastMime = 'text/plain';
      setStats(fmtB(raw.length), fmtB(u8.length), /JSON/.test(notes.join()) ? 'JSON' : /^\s*<svg/i.test(txt) ? 'SVG image' : 'Text');
      if (/^\s*<svg/i.test(txt)) $('b6Extra').innerHTML = '<p style="margin:0 0 10px"><img src="data:image/svg+xml;base64,' + c.b64 + '" alt="Preview of the decoded SVG" style="max-width:100%;max-height:180px;border:1px solid #e6e6e6;border-radius:8px;background:#fff"></p>';
      say('b6Check', c.url && c.std ? 'warn' : 'ok', '<strong>Decoded ' + fmtN(u8.length) + ' bytes of UTF 8 text.</strong> ' + notes.join(' '));
      return last;
    }
    var mime = sn ? sn[0] : (c.dataMime || 'application/octet-stream'), label = sn ? sn[1] : 'Binary file', ext = sn ? sn[2] : 'bin';
    lastBytes = u8; lastMime = mime; lastName = 'decoded.' + ext;
    last = hex(u8); $('b6Out').textContent = last;
    setStats(fmtB(raw.length), fmtB(u8.length), label);
    if (/^image\//.test(mime)) $('b6Extra').innerHTML = '<p style="margin:0 0 10px"><img src="data:' + mime + ';base64,' + c.b64 + '" alt="Preview of the decoded image" style="max-width:100%;max-height:220px;border:1px solid #e6e6e6;border-radius:8px;background:#fff"></p>';
    say('b6Check', 'ok', '<strong>Decoded a ' + esc(label) + ' of ' + fmtB(u8.length) + '.</strong> It is not readable text, so the first bytes are shown in hex below. Press Download to save the file. ' + notes.join(' '));
    return last;
  }
  $('b6Tabs').querySelectorAll('button').forEach(function(btn){
    btn.addEventListener('click', function(){
      $('b6Tabs').querySelectorAll('button').forEach(function(x){ x.classList.remove('on'); });
      btn.classList.add('on'); mode = btn.getAttribute('data-m');
      $('b6TextBox').style.display = mode === 'file' ? 'none' : '';
      $('b6FileBox').style.display = mode === 'file' ? '' : 'none';
      $('b6EncOpts').style.display = mode === 'dec' ? 'none' : '';
      $('b6Swap').style.display = mode === 'file' ? 'none' : '';
      document.querySelector('label[for="b6In"]').firstChild.textContent = mode === 'enc' ? 'Text to encode ' : 'Base64, JWT or data URI ';
      run();
    });
  });
  $('b6File').addEventListener('change', function(){
    var f = this.files && this.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function(){ fileBytes = new Uint8Array(r.result); fileName = f.name; fileMime = f.type; $('b6FileInfo').textContent = f.name + ', ' + fmtB(f.size); run(); };
    r.readAsArrayBuffer(f);
  });
  var tm; $('b6In').addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(run, 60); });
  ['b6Url', 'b6Pad', 'b6Wrap'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('b6Copy').addEventListener('click', function(){ var o = run(); if (o) copyText(o, 'toast'); });
  $('b6Dl').addEventListener('click', function(){
    run();
    if (lastBytes){ var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([lastBytes], {type: lastMime})); a.download = lastName; document.body.appendChild(a); a.click(); document.body.removeChild(a); }
    else if (last) download(mode === 'dec' ? 'decoded.json' : 'base64.txt', last, mode === 'dec' ? 'application/json' : 'text/plain');
  });
  $('b6Swap').addEventListener('click', function(){
    if (!last || mode === 'file') return;
    var target = mode === 'enc' ? 'dec' : 'enc', val = mode === 'dec' && lastBytes && !utf8(lastBytes) ? null : last;
    if (val === null) return;
    $('b6In').value = val; $('b6Tabs').querySelector('[data-m="' + target + '"]').click();
  });
  run();
''',
        content=f'''
    <h2>What Is Base64?</h2>
    <p>Base64 is a way to write any data, including images, files and text in any language, using only 64 safe characters: <code>A</code> to <code>Z</code>, <code>a</code> to <code>z</code>, <code>0</code> to <code>9</code>, <code>+</code> and <code>/</code>, with <code>=</code> as padding at the end. It is defined in <a href="https://www.rfc-editor.org/rfc/rfc4648" {EXT}>RFC 4648</a>. Every 3 bytes become 4 characters, so Base64 is about 33% larger than the original.</p>
    <p>You meet it everywhere: in email attachments, data URIs that put small images straight into HTML or CSS, API keys and basic auth headers, and JWT login tokens. This tool decodes all of these, encodes text and files, and runs entirely in your browser, so tokens and files never leave your device.</p>

    <h2>How to Use the Base64 Tool</h2>
    <ol>
      <li><strong>To decode,</strong> paste a Base64 string, a JWT token or a full <code>data:</code> URI. The tool works out what it is and shows text, formatted JSON, an image preview or a file you can download.</li>
      <li><strong>To encode text,</strong> open Encode Text and type. Choose URL safe for links and tokens, and line breaks for email.</li>
      <li><strong>To encode a file,</strong> open File to Base64 and pick an image, font or PDF. You get plain Base64, a data URI and, for images, a ready <code>&lt;img&gt;</code> tag and CSS line.</li>
      <li><strong>Copy or download</strong> the result, or press Use Result as Input to go the other way.</li>
    </ol>

    <h2>Base64 Variants Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Variant', 'Characters', 'Where it is used')}
      <tbody>
        <tr><td>Standard Base64</td><td><code>A to Z a to z 0 to 9 + /</code> and <code>=</code></td><td>Email attachments, data URIs, most APIs</td></tr>
        <tr><td>base64url</td><td><code>-</code> and <code>_</code> in place of <code>+</code> and <code>/</code>, padding often left out</td><td>JWT tokens, URLs, file names</td></tr>
        <tr><td>MIME</td><td>Standard, with a line break every 76 characters</td><td>Email bodies and attachments</td></tr>
        <tr><td>Data URI</td><td><code>data:image/png;base64,</code> followed by the data</td><td>Small images and fonts inside HTML or CSS</td></tr>
      </tbody>
    </table></div>
    <p>The decoder accepts all of these, adds missing padding, and handles text in Hindi, Marathi or any other script as UTF 8. The browser function <a href="https://developer.mozilla.org/en-US/docs/Web/API/Window/btoa" {EXT}>btoa()</a> on its own fails on such characters, which is a common cause of broken encoders.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Base64 is not encryption.</strong> Anyone can decode it in a second, so never use it to hide passwords or personal data.</li>
      <li><strong>Read JWTs safely.</strong> The decoder shows who a token belongs to and when it expires, but it does not check the signature. Only your server can confirm a token is genuine.</li>
      <li><strong>Inline only small images.</strong> A data URI saves a request, but it adds about a third to the size and cannot be cached on its own. Keep it for icons and logos under about 10 KB.</li>
      <li><strong>Fix broken strings fast.</strong> If decoding fails, the tool shows the exact bad character or tells you the string was cut off when copied.</li>
    </ul>

    <h2>Work Smarter With Data and Images</h2>
    <p>See how image weight affects speed in <a href="{B}optimize-images-for-seo-without-losing-quality/">how to optimize images without losing quality</a> and <a href="{B}webp-vs-avif-image-format-seo/">WebP vs AVIF</a>, and learn how tokens protect logins in <a href="{B}php-authentication-system/">building a PHP authentication system</a>. Decoded a JSON payload? Tidy it up in the <a href="{T}json-formatter/">JSON formatter and validator</a>.</p>
''',
        faqs=[
            ("How do I decode a Base64 string?", "Paste it into the Decode box. The tool removes spaces and line breaks, accepts the URL safe version, adds missing padding and shows the result as text, formatted JSON, an image preview or a file to download."),
            ("How do I decode a JWT token?", "Paste the whole token, the three parts joined by dots. The tool decodes the header and payload, which are base64url, and shows each claim in a table with the issued and expiry times as readable dates. It does not verify the signature."),
            ("How do I convert an image to Base64?", "Open File to Base64 and choose the image. You get the plain Base64 text, a full data URI, an img tag and a CSS background line you can copy. The image never leaves your device."),
            ("Is Base64 encoding secure?", "No. Base64 only changes how data is written, it does not hide it. Anyone can decode it, so use real encryption or hashing for passwords and private data."),
        ],
        related=[("Optimize Images for SEO Without Losing Quality", "optimize-images-for-seo-without-losing-quality"), ("WebP vs AVIF Image Format", "webp-vs-avif-image-format-seo"),
                 ("PHP Authentication System", "php-authentication-system"), ("REST API in PHP Without a Framework", "rest-api-in-php-without-a-framework")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'developer-tools'; t['updated'] = '2026-11-08'
