"""Batch 14 (2026-11-11): Email Marketing Tools, third tool (SPF Record Generator and Checker).
Facts checked 2026-11-11 against: RFC 7208 (rfc-editor.org/rfc/rfc7208): section 4.6.4 only include, a, mx, ptr, exists
and redirect cause DNS lookups, more than 10 gives permerror, each mx may resolve at most 10 hosts, void lookups SHOULD
be limited to 2; sections 3.2 and 4.5 more than one v=spf1 record gives permerror; section 3.3 strings of one TXT record
are joined without spaces, 255 octets per string; section 3.4 keep the answer within 512 octets; section 5.5 ptr SHOULD
NOT be published; section 6 redirect and exp at most once each, redirect ignored when all is present; section 4.6.2
qualifiers + - ~ ? (pass, fail, softfail, neutral), default +; section 5.6 ip4 defaults to /32, ip6 to /128; section
4.7 no match and no redirect gives neutral; section 3.1 only TXT, type 99 discontinued. Unknown mechanisms give
permerror, unknown modifiers are ignored (section 6).
Provider values: Google Workspace include:_spf.google.com, Google recommends ~all and says up to 10 include tags
(knowledge.workspace.google.com set up SPF); Microsoft 365 include:spf.protection.outlook.com with -all, ip4 ip6 all
do not count as lookups, nested includes add lookups (learn.microsoft.com email-authentication-spf-configure);
Hostinger Email include:_spf.mail.hostinger.com ~all (hostinger.com/support/1583673); Brevo include:spf.brevo.com,
merged example v=spf1 include:_spf.google.com include:spf.brevo.com mx ~all (help.brevo.com 4414335084434);
Zoho Mail include:zoho.com, India data centre include:zoho.in (the tool tells users to confirm in their admin console)."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/email-marketing-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    SP_CHECK = ('"v=spf1 include:_spf.google.com ~all"\n'
                '"v=spf1 include:spf.brevo.com mx ptr ip4:203.0.113.25 ~all"')
    SERV = [('spG', 'Google Workspace', '_spf.google.com', True), ('spM', 'Microsoft 365', 'spf.protection.outlook.com', False),
            ('spZ', 'Zoho Mail', 'zoho.com', False), ('spZi', 'Zoho Mail India data centre', 'zoho.in', False),
            ('spH', 'Hostinger Email', '_spf.mail.hostinger.com', False), ('spB', 'Brevo', 'spf.brevo.com', True)]
    serv_html = ''.join(CK(i, f'{n} <code>include:{v}</code>', on) for i, n, v, on in SERV)
    serv_js = ', '.join(f"['{i}', '{v}']" for i, n, v, on in SERV)

    TOOLS.append(dict(
        slug='spf-record-generator', short='SP', name='SPF Record Generator and Checker',
        card='Build one valid SPF TXT record for all your email senders, or paste records to count DNS lookups, find errors and merge duplicates.',
        title='SPF Record Generator and Checker: Free TXT Record',
        desc='Free SPF record generator and checker. Combine Google, Microsoft 365, Zoho and Brevo into one TXT record, count DNS lookups and merge duplicate SPF records.',
        h1='SPF Record Generator and Checker',
        lead='Tick the services that send email for your domain to get one ready to paste SPF record, with a live count of DNS lookups. Already have records? Paste them into the checker to catch errors, the 10 lookup limit and duplicate records, then merge them into one in a click.',
        tool='''<section class="tool" aria-label="SPF record generator">
    <div class="card" style="min-width:0">
      <h2>Build Your SPF Record</h2>
      ''' + F('spDom', 'Your domain', 'yourshop.in', em='the domain in your From address', mono=True) + '''
      <p style="font-size:14px;margin:0 0 6px"><strong>Services that send email for you</strong></p>
      ''' + serv_html + '''
      ''' + CK('spMx', 'Your own mail servers (<code>mx</code>)', False) + CK('spA', 'Your website server (<code>a</code>)', False) + '''
      ''' + F('spIp4', 'IPv4 addresses or ranges', '203.0.113.25', em='comma separated, such as 203.0.113.0/24', mono=True) + '''
      ''' + F('spIp6', 'IPv6 addresses or ranges', '', em='optional', mono=True, ph='2001:db8::/32') + '''
      ''' + F('spInc', 'Other include domains', '', em='from your email tool, comma separated', mono=True, ph='sendgrid.net, amazonses.com') + '''
      ''' + F('spAll', 'Mail from any other server', '~all', tag='select', opts=[('~all', '~all soft fail: mark as suspicious (Google default)'), ('-all', '-all fail: reject (Microsoft default)'), ('?all', '?all neutral: testing only')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your DNS Record</h2>
      <div class="stats">''' + S('spLk', 'DNS lookups of 10') + S('spLen', 'Characters') + S('spN', 'Senders') + '''</div>
      <div style="overflow-x:auto"><table class="rtable"><tbody>
        <tr><td style="width:30%"><strong>Type</strong></td><td class="mono">TXT</td></tr>
        <tr><td><strong>Host or Name</strong></td><td class="mono" id="spHost" style="word-break:break-all"></td></tr>
        <tr><td><strong>Full name</strong></td><td class="mono" id="spFull" style="word-break:break-all"></td></tr>
        <tr><td><strong>TTL</strong></td><td class="mono">3600 or your panel default</td></tr>
      </tbody></table></div>
      <p style="font-size:14px;margin:14px 0 6px"><strong>Value</strong></p>
      <div class="code-out mono" id="spRec" style="word-break:break-all;white-space:pre-wrap"></div>
      <div id="spSplitBox" style="display:none"><p style="font-size:14px;margin:12px 0 6px"><strong>Split version for panels that limit each string to 255 characters</strong></p><div class="code-out mono" id="spSplit" style="word-break:break-all;white-space:pre-wrap"></div></div>
      <div class="actions" style="margin:12px 0"><button class="btn dark" id="spCopy">Copy Record</button><button class="btn" id="spCopyHost">Copy Host</button></div>
      <div class="kw-result" id="spNotes"></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Check or Merge Existing SPF Records</h2>
      ''' + F('spIn', 'Paste your SPF record, or all TXT records of your domain', SP_CHECK, em='one record per line, quotes are fine', tag='textarea', mono=True, extra=' style="min-height:90px"') + '''
      <div class="kw-result" id="spCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="spTerms"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="spMerge">Merge Into One Record</button><button class="btn" id="spCopyIn">Copy Checked Record</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var SERV = [''' + serv_js + r'''];
  var DOM = /^([a-z0-9_]([a-z0-9_-]{0,61}[a-z0-9_])?\.)+[a-z]{2,63}\.?$/i;
  var SLD = {co:1, com:1, net:1, org:1, gov:1, ac:1, edu:1, gen:1, firm:1, ind:1, res:1, ltd:1, plc:1, me:1, nic:1};
  function org(d){ var p = d.toLowerCase().replace(/\.$/, '').split('.'); if (p.length > 2 && p[p.length - 1].length === 2 && SLD[p[p.length - 2]]) return p.slice(-3).join('.'); return p.slice(-2).join('.'); }
  function cleanDom(v){ return v.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/[\/:].*$/, '').replace(/\.$/, ''); }
  function list(v){ return v.split(/[,;\s]+/).map(function(x){ return x.trim(); }).filter(Boolean); }
  function isDom(d){ return d.indexOf('%') > -1 ? /^[^\s]+$/.test(d) : DOM.test(d); }
  function ip4(x){ var m = x.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?:\/(\d{1,2}))?$/); if (!m) return false; for (var i = 1; i < 5; i++) if (+m[i] > 255) return false; return m[5] === undefined || +m[5] <= 32; }
  function ip6(x){ var m = x.match(/^([0-9a-f:.]+)(?:\/(\d{1,3}))?$/i); if (!m || m[1].indexOf(':') < 0) return false; if (m[2] !== undefined && +m[2] > 128) return false; try { new URL('http://[' + m[1] + ']/'); return true; } catch (e) { return false; } }
  function split255(s){ if (s.length <= 255) return null; var out = [], r = s; while (r.length > 255){ var cut = r.lastIndexOf(' ', 254); if (cut < 1) cut = 254; out.push(r.slice(0, cut + 1)); r = r.slice(cut + 1); } out.push(r); return out.map(function(x){ return '"' + x + '"'; }).join(' '); }
  var LK = {include: 1, a: 1, mx: 1, ptr: 1, exists: 1, redirect: 1};
  var rec = '', host = '';
  function gen(){
    var d = cleanDom($('spDom').value), bad = [], N = [], cls = 'ok', inc = [], t = ['v=spf1'], lk = 0, n = 0;
    if (!d || !DOM.test(d)) bad.push('Enter a valid domain, such as ' + c('yourshop.in') + '.');
    list($('spIp4').value).forEach(function(x){ x = x.replace(/^ip4:/i, ''); if (!ip4(x)) bad.push(c(x) + ' is not a valid IPv4 address or range.'); else { t.push('ip4:' + x); n++; } });
    list($('spIp6').value).forEach(function(x){ x = x.replace(/^ip6:/i, ''); if (!ip6(x)) bad.push(c(x) + ' is not a valid IPv6 address or range.'); else { t.push('ip6:' + x); n++; } });
    if ($('spA').checked){ t.push('a'); lk++; n++; }
    if ($('spMx').checked){ t.push('mx'); lk++; n++; }
    SERV.forEach(function(s){ if ($(s[0]).checked) inc.push(s[1]); });
    list($('spInc').value).forEach(function(x){ x = x.toLowerCase().replace(/^include:/, ''); if (!isDom(x)) bad.push(c(x) + ' is not a valid include domain.'); else inc.push(x); });
    inc = inc.filter(function(x, i, a){ return a.indexOf(x) === i; });
    inc.forEach(function(x){ t.push('include:' + x); lk++; n++; });
    var all = n ? $('spAll').value : '-all';
    t.push(all); rec = t.join(' ');
    host = d && d.split('.').length > 2 && org(d) !== d ? d.slice(0, -org(d).length - 1) : '@';
    $('spRec').textContent = rec; $('spHost').textContent = host; $('spFull').textContent = d || 'yourdomain.com';
    $('spLk').textContent = lk; $('spLen').textContent = rec.length; $('spN').textContent = n;
    var sp = split255(rec); $('spSplitBox').style.display = sp ? '' : 'none'; if (sp) $('spSplit').textContent = sp;
    if (bad.length){ say('spNotes', 'bad', '<strong>Fix this first:</strong> ' + bad.join(' ')); return; }
    if (!n){ say('spNotes', 'warn', '<strong>No senders selected.</strong> This record, ' + c('v=spf1 -all') + ', says the domain sends no email at all. That is right for a domain you never send from, and it stops others faking it. Tick a service if you do send email.'); return; }
    if (lk > 10){ cls = 'bad'; N.push('<strong>Too many lookups:</strong> ' + lk + ' of 10. Receivers will return a permanent error and SPF fails for every email. Remove services you no longer use, or replace some with their IP ranges.'); }
    else if (inc.length) { N.push('<strong>' + lk + ' direct lookups of 10.</strong> Each ' + c('include') + ' also brings the lookups inside that service\'s own record, so the real total is higher. Keep the direct count low, and check the live record with a DNS lookup tool after publishing.'); if (lk >= 7) cls = 'warn'; }
    else N.push('<strong>' + lk + ' DNS lookups of 10.</strong> IP addresses and ' + c('all') + ' cost no lookups.');
    if (all === '~all') N.push(c('~all') + ' marks mail from unlisted servers as suspicious. Google recommends it, and it is the safe choice while you check that every sender is listed.');
    if (all === '-all') N.push(c('-all') + ' tells receivers to reject mail from unlisted servers. Microsoft recommends it. Use it once you are sure every sender is listed.');
    if (all === '?all'){ cls = cls === 'bad' ? cls : 'warn'; N.push(c('?all') + ' gives no protection at all. Use it only for a short test.'); }
    if ($('spZ').checked && $('spZi').checked) N.push('You ticked both Zoho options. Most accounts need only one: check the value in your Zoho admin console.');
    if (sp) N.push('The record is longer than 255 characters. Many DNS panels split it for you; if yours shows an error, paste the split version.');
    N.push('Add this as one TXT record where your domain is managed. If an SPF record already exists, replace it: a domain may have only one.' + (host !== '@' ? ' This record covers ' + c(d) + ' only, not the main domain.' : ''));
    say('spNotes', cls, N.join('<br>'));
  }
  var MEAN = {all: 'Matches every other server', include: 'Uses the SPF record of another domain', a: 'The servers in the A or AAAA record', mx: 'The mail servers in the MX record',
    ptr: 'Reverse DNS match. Slow and not recommended', ip4: 'An IPv4 address or range', ip6: 'An IPv6 address or range', exists: 'Passes if the domain has an A record', redirect: 'Use another domain\'s record instead', exp: 'Text shown when mail fails'};
  var QN = {'+': 'pass', '-': 'fail', '~': 'soft fail', '?': 'neutral'};
  function extract(raw){
    var recs = [], other = 0;
    raw.split(/\r?\n/).forEach(function(line){
      line = line.trim(); if (!line) return;
      var q = line.match(/"((?:[^"\\]|\\.)*)"/g), s;
      if (q) s = q.map(function(x){ return x.slice(1, -1); }).join(''); else s = line.replace(/^.*?\bTXT\b\s*/i, '');
      s = s.replace(/\s+/g, ' ').trim();
      if (/^v=spf1(\s|$)/i.test(s)) recs.push({s: s, q: q}); else if (/^v=spf/i.test(s)) recs.push({s: s, q: q}); else if (recs.length && !/=/.test(s.split(' ')[0]) && !q) recs[recs.length - 1].s += ' ' + s; else other++;
    });
    return {recs: recs, other: other};
  }
  function parse(s){
    var terms = s.split(' ').slice(1), out = [];
    terms.forEach(function(x){
      if (!x) return;
      var m = x.match(/^([a-z][a-z0-9_.-]*)=(.*)$/i);
      if (m){ out.push({raw: x, mod: true, name: m[1].toLowerCase(), val: m[2]}); return; }
      var q = '+', y = x; if ('+-~?'.indexOf(y[0]) > -1){ q = y[0]; y = y.slice(1); }
      var mm = y.match(/^([a-z0-9]+)(?:[:\/](.*))?$/i), name = mm ? mm[1].toLowerCase() : y.toLowerCase(), val = mm && mm[2] !== undefined ? y.slice(mm[1].length) : '';
      out.push({raw: x, mod: false, q: q, name: name, val: val});
    });
    return out;
  }
  var checked = '', lastRecs = [];
  function check(){
    var raw = $('spIn').value.trim(), E = [], W = [], rows = [];
    $('spMerge').style.display = 'none'; checked = ''; lastRecs = [];
    if (!raw){ $('spTerms').innerHTML = ''; say('spCheck', '', 'Paste an SPF record to check it.'); return; }
    var ex = extract(raw), recs = ex.recs;
    if (!recs.length){ $('spTerms').innerHTML = ''; say('spCheck', 'bad', '<strong>No SPF record found.</strong> An SPF record is a TXT record that starts with ' + c('v=spf1') + '.' + (ex.other ? ' The ' + ex.other + ' other TXT line' + (ex.other === 1 ? ' you pasted is' : 's you pasted are') + ' not SPF, for example a site verification code.' : '')); return; }
    recs.forEach(function(r){ if (!/^v=spf1(\s|$)/i.test(r.s)) E.push(c(r.s.split(' ')[0]) + ' is not a valid version. It must be exactly ' + c('v=spf1') + '.'); });
    lastRecs = recs.filter(function(r){ return /^v=spf1(\s|$)/i.test(r.s); });
    if (lastRecs.length > 1){ E.push('<strong>' + lastRecs.length + ' SPF records found.</strong> A domain may have only one. With more, every receiver returns a permanent error and SPF fails for all your email. Click <strong>Merge Into One Record</strong> below.'); $('spMerge').style.display = ''; }
    var r = lastRecs[0] || recs[0]; checked = r.s;
    if (r.q) r.q.forEach(function(x){ if (x.length - 2 > 255) E.push('One quoted string is ' + (x.length - 2) + ' characters. Each string in a TXT record can hold 255 at most, so split it.'); });
    if (!r.q && r.s.length > 255) W.push('The record is ' + r.s.length + ' characters. Each DNS string holds 255, so it must be published as two or more strings. Most panels do this for you.');
    if (r.s.length > 450) W.push('The record is long. RFC 7208 asks to keep the whole DNS answer within 512 bytes, so remove senders you no longer use.');
    var T = parse(r.s), lk = 0, seen = {}, allAt = -1, red = 0, exp = 0, allQ = '';
    T.forEach(function(t, i){
      var note = MEAN[t.name] || '', cost = 0, bad = '';
      if (seen[t.raw.toLowerCase()]) W.push(c(t.raw) + ' appears twice. Remove the copy, it wastes a lookup.');
      seen[t.raw.toLowerCase()] = 1;
      if (allAt > -1 && !t.mod){ W.push(c(t.raw) + ' comes after ' + c('all') + ', so receivers never read it.'); }
      if (t.mod){
        if (t.name === 'redirect'){ red++; cost = 1; if (!isDom(t.val)) bad = 'Needs a valid domain.'; }
        else if (t.name === 'exp'){ exp++; if (!isDom(t.val)) bad = 'Needs a valid domain.'; }
        else { note = 'Unknown modifier. Receivers ignore it'; W.push('Unknown modifier ' + c(t.raw) + '. Receivers ignore it, so check for a typo.'); }
      } else {
        var v = t.val, arg = v.replace(/^:/, '');
        if (t.name === 'all'){ if (v) bad = c('all') + ' takes no value.'; if (allAt < 0){ allAt = i; allQ = t.q; } else W.push('There is more than one ' + c('all') + '.'); }
        else if (t.name === 'include' || t.name === 'exists'){ cost = 1; if (v[0] !== ':' || !isDom(arg)) bad = c(t.name) + ' needs a domain, such as ' + c(t.name + ':_spf.example.com') + '.'; }
        else if (t.name === 'a' || t.name === 'mx'){ cost = 1; var dm = v.match(/^(?::([^\/]+))?(\/\d{1,2})?(\/\/\d{1,3})?$/); if (!dm || (dm[1] && !isDom(dm[1]))) bad = c(t.raw) + ' is not valid. Use ' + c(t.name) + ', ' + c(t.name + ':example.com') + ' or ' + c(t.name + '/24') + '.'; }
        else if (t.name === 'ptr'){ cost = 1; W.push(c('ptr') + ' should not be used (RFC 7208 section 5.5). It is slow, and some receivers ignore it. Replace it with ' + c('ip4') + ' or ' + c('a') + '.'); if (v && (v[0] !== ':' || !isDom(arg))) bad = 'Needs a valid domain.'; }
        else if (t.name === 'ip4'){ if (v[0] !== ':' || !ip4(arg)) bad = c(t.raw) + ' is not a valid IPv4 address or range.'; else { var pf = arg.split('/')[1]; if (pf !== undefined && +pf < 16) W.push(c(t.raw) + ' allows ' + Math.pow(2, 32 - pf).toLocaleString('en-IN') + ' addresses. Check that the range is not too wide.'); } }
        else if (t.name === 'ip6'){ if (v[0] !== ':' || !ip6(arg)) bad = c(t.raw) + ' is not a valid IPv6 address or range.'; }
        else { note = 'Unknown mechanism'; bad = 'Unknown mechanism ' + c(t.raw) + '. Receivers return a permanent error, so SPF fails.' + (/^(inc|incl|inlcude|includ|inculde)/i.test(t.name) ? ' Did you mean ' + c('include') + '?' : '') + (/^ip[46]$/i.test(t.name) ? '' : ''); }
        if (!bad && t.q === '+' && t.raw[0] === '+' && t.name !== 'all') W.push('The ' + c('+') + ' before ' + c(t.raw.slice(1)) + ' is the default and can be dropped.');
      }
      if (bad) E.push(bad);
      lk += cost;
      rows.push('<tr><td class="mono" style="word-break:break-all"><strong>' + esc(t.raw) + '</strong></td><td>' + (t.mod ? 'modifier' : esc(QN[t.q])) + '</td><td>' + (cost ? cost : '0') + '</td><td>' + (bad ? '<strong>Error.</strong> ' : '') + esc(note) + '</td></tr>');
    });
    if (allAt > -1 && allQ === '+') E.push(c('+all') + ' lets every server on the internet send as your domain. Change it to ' + c('~all') + ' or ' + c('-all') + '.');
    if (red > 1) E.push(c('redirect') + ' appears more than once, which is a permanent error.');
    if (exp > 1) E.push(c('exp') + ' appears more than once, which is a permanent error.');
    if (red && allAt > -1){ lk -= red; rows = rows.map(function(x){ return /^<tr><td class="mono" style="word-break:break-all"><strong>redirect=/i.test(x) ? x.replace('<td>1</td>', '<td>0</td>') : x; }); }
    if (red && allAt > -1) W.push(c('redirect') + ' is ignored because the record also has ' + c('all') + '.');
    if (allAt < 0 && !red) W.push('No ' + c('all') + ' at the end, so mail from unlisted servers gets a neutral result. Add ' + c('~all') + ' or ' + c('-all') + '.');
    if (allQ === '?') W.push(c('?all') + ' gives no protection. Switch to ' + c('~all') + ' or ' + c('-all') + ' when testing is done.');
    if (lk > 10) E.push('<strong>' + lk + ' DNS lookups.</strong> The limit is 10, so SPF fails with a permanent error. Remove unused senders or swap some for IP ranges.');
    else if (lk >= 8) W.push(lk + ' direct lookups is close to the limit of 10, and lookups inside each ' + c('include') + ' count too.');
    $('spTerms').innerHTML = rows.length ? '<thead><tr><th>Term</th><th>Result if matched</th><th>Lookups</th><th>Meaning</th></tr></thead><tbody>' + rows.join('') + '</tbody>' : '';
    var lvl = allQ === '-' ? 'unlisted servers fail' : allQ === '~' ? 'unlisted servers soft fail' : allQ === '?' ? 'no protection' : red ? 'policy comes from the redirect domain' : 'no ending, so unlisted servers are neutral';
    var h = E.length ? '<strong>' + E.length + ' error' + (E.length === 1 ? '' : 's') + ' to fix.</strong> ' : '<strong>Valid SPF record: ' + lk + ' direct lookup' + (lk === 1 ? '' : 's') + ' of 10, ' + lvl + '.</strong> ';
    if (lastRecs.length > 1) h += 'Checking the first record below. ';
    if (E.length) h += '<br>' + E.join('<br>');
    if (W.length) h += '<br>' + W.map(function(x){ return 'Note: ' + x; }).join('<br>');
    say('spCheck', E.length ? 'bad' : W.length ? 'warn' : 'ok', h);
  }
  function merge(){
    if (lastRecs.length < 2) return;
    var ips = [], mech = [], incs = [], ends = [], seen = {}, exp = '';
    lastRecs.forEach(function(r){
      parse(r.s).forEach(function(t){
        var k = t.raw.toLowerCase().replace(/^\+/, '');
        if (t.mod){ if (t.name === 'redirect') k = 'include:' + t.val.toLowerCase(); else if (t.name === 'exp'){ exp = exp || t.raw; return; } else return; }
        else if (t.name === 'all'){ ends.push(t.q); return; }
        else if (t.name === 'ptr') return;
        if (seen[k]) return; seen[k] = 1;
        if (/^ip[46]:/.test(k)) ips.push(k); else if (/^include:/.test(k)) incs.push(k); else mech.push(k);
      });
    });
    var end = ends.length && ends.every(function(q){ return q === '-'; }) ? '-all' : '~all';
    var out = ['v=spf1'].concat(ips, mech, incs, [end]); if (exp) out.push(exp);
    $('spIn').value = out.join(' '); check();
    say('spCheck', $('spCheck').className.indexOf('bad') > -1 ? 'bad' : 'ok', '<strong>Merged into one record.</strong> Delete the old SPF records in your DNS panel and add this one in their place. Duplicates and ' + c('ptr') + ' were removed, and ' + c(end) + ' was kept as the ending.' + '<br>' + $('spCheck').innerHTML);
    $('spIn').scrollIntoView({behavior: 'smooth', block: 'center'});
  }
  ['spDom', 'spIp4', 'spIp6', 'spInc'].forEach(function(id){ $(id).addEventListener('input', gen); });
  SERV.map(function(s){ return s[0]; }).concat(['spMx', 'spA', 'spAll']).forEach(function(id){ $(id).addEventListener('change', gen); });
  var tc; $('spIn').addEventListener('input', function(){ clearTimeout(tc); tc = setTimeout(check, 80); });
  $('spCopy').addEventListener('click', function(){ gen(); copyText(rec, 'toast'); });
  $('spCopyHost').addEventListener('click', function(){ gen(); copyText(host, 'toast'); });
  $('spCopyIn').addEventListener('click', function(){ check(); if (checked) copyText(checked, 'toast'); });
  $('spMerge').addEventListener('click', merge);
  gen(); check();
''',
        content=f'''
    <h2>What Is an SPF Record?</h2>
    <p>SPF, short for Sender Policy Framework, is a TXT record in your domain's DNS that lists the servers allowed to send email for your domain. When Gmail, Yahoo or Outlook receives a message, it checks the sending server against this list. If the server is not on it, the mail can be marked as spam or rejected.</p>
    <p>SPF is now a basic requirement. The <a href="https://support.google.com/mail/answer/81126" {EXT}>Google email sender guidelines</a> ask every sender to set up SPF or DKIM, and bulk senders need SPF, DKIM and DMARC together. The hard part is that most businesses send from several places, such as Google Workspace for staff, Brevo for newsletters and a website server for order emails, and all of them must sit in one record. This generator builds that one record, and the checker finds the mistakes that silently break SPF.</p>

    <h2>How to Create and Add Your SPF Record</h2>
    <ol>
      <li><strong>List every service that sends email</strong> with your domain in the From address: your mailbox provider, newsletter tool, CRM, shop and website.</li>
      <li><strong>Tick those services</strong> or paste the include value each one gives you in its domain setup page. Add fixed server IP addresses if you have them.</li>
      <li><strong>Start with <code>~all</code>,</strong> then copy the record and the host. For the main domain the host is <code>@</code>.</li>
      <li><strong>Replace any existing SPF record</strong> in your DNS panel. Never add a second one next to it.</li>
      <li><strong>Paste the live record into the checker</strong> after a few hours to confirm it is valid and under the lookup limit.</li>
    </ol>

    <h2>SPF Mechanisms Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Term', 'Example', 'Lookups', 'What it does')}
      <tbody>
        <tr><td><code>ip4</code> and <code>ip6</code></td><td><code>ip4:203.0.113.25</code></td><td>0</td><td>Allows one address or a range. A single IPv4 address means <code>/32</code></td></tr>
        <tr><td><code>include</code></td><td><code>include:_spf.google.com</code></td><td>1 plus nested</td><td>Allows every server in another domain's SPF record</td></tr>
        <tr><td><code>a</code> and <code>mx</code></td><td><code>mx</code></td><td>1</td><td>Allows the servers your domain's A or MX records point to</td></tr>
        <tr><td><code>exists</code> and <code>redirect</code></td><td><code>redirect=_spf.example.com</code></td><td>1</td><td>Advanced checks, and handing the whole policy to another domain</td></tr>
        <tr><td><code>ptr</code></td><td><code>ptr</code></td><td>1</td><td>Reverse DNS match. RFC 7208 says not to use it</td></tr>
        <tr><td><code>~all</code>, <code>-all</code></td><td><code>~all</code></td><td>0</td><td>Ending for every other server: soft fail or fail</td></tr>
      </tbody>
    </table></div>
    <p>The rules come from <a href="https://www.rfc-editor.org/rfc/rfc7208" {EXT}>RFC 7208</a>, the SPF standard. Microsoft explains the lookup count well in its <a href="https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure" {EXT}>SPF setup guide</a>.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>One record only.</strong> Two records starting with <code>v=spf1</code> make SPF fail for every email. This is the most common SPF mistake, and the checker merges them for you.</li>
      <li><strong>Watch the 10 lookup limit.</strong> Every <code>include</code>, <code>a</code> and <code>mx</code> costs a lookup, and so does every include inside those records. Remove tools you stopped using.</li>
      <li><strong>Soft fail or fail?</strong> Google recommends <code>~all</code> and Microsoft recommends <code>-all</code>. With a DMARC policy in place, both protect you, and <code>~all</code> is safer while you are still finding senders.</li>
      <li><strong>Subdomains need their own record.</strong> The record on your main domain does not cover <code>news.yourshop.in</code>.</li>
      <li><strong>Some tools need no include.</strong> Many newsletter platforms send from their own bounce domain and only ask for DKIM. Follow your tool's setup page rather than guessing.</li>
    </ul>

    <h2>Finish Your Email Setup</h2>
    <p>SPF works best with DKIM and DMARC. Plan your sending with our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, and if your website sends mail from code, read <a href="{B}send-email-code-in-php/">how to send email in PHP</a> and <a href="{B}php-contact-form-spam-protection/">contact form spam protection in PHP</a>. Then publish a policy for failing mail with the <a href="{T}dmarc-record-generator/">DMARC record generator and checker</a>.</p>
''',
        faqs=[
            ("Can a domain have two SPF records?", "No. A domain may have only one TXT record that starts with v=spf1. With two or more, receivers return a permanent error and SPF fails for all your mail. Combine every include and IP address into a single record instead."),
            ("What is the SPF 10 DNS lookup limit?", "RFC 7208 allows at most 10 DNS lookups while checking SPF. Every include, a, mx, ptr and exists term and the redirect modifier costs one, and includes inside included records count too. IP addresses and all cost nothing. Going over 10 makes SPF fail."),
            ("Should I use ~all or -all?", "~all (soft fail) asks receivers to treat unlisted senders as suspicious, and Google recommends it. -all (fail) asks them to reject such mail, and Microsoft recommends it. Start with ~all, and move to -all once you are sure every sender is listed."),
            ("Where do I add the SPF record?", "Add it as a TXT record in the DNS settings where your domain is managed, such as your registrar, hosting panel or Cloudflare. Use @ as the host for the main domain. If an SPF record is already there, edit it instead of adding a new one."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("Send Email Code in PHP", "send-email-code-in-php"),
                 ("PHP Contact Form Spam Protection", "php-contact-form-spam-protection"), ("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'email-marketing-tools'; t['updated'] = '2026-11-11'
