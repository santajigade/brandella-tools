"""Batch 17 (2026-11-14): Email Marketing Tools, sixth tool (DKIM Record Generator and Checker).
Facts checked 2026-11-14 against: RFC 6376 section 3.6.1 (key record tags v h k n p s t; v= must be DKIM1 and first;
p= required, empty value means revoked; k default rsa; s default *; t=y testing, verifiers MUST NOT treat testing mode
signatures differently from unsigned mail; t=s means i= must equal d=), section 3.2 (tag names are case sensitive,
duplicate tags make the list invalid, unknown tags are ignored), section 3.6.2.1 (record lives at
selector._domainkey.domain); RFC 8301 (rfc-editor.org/rfc/rfc8301): signers MUST use RSA keys of at least 1024 bits,
SHOULD use 2048, verifiers MUST validate 1024 to 4096, keys under 1024 are not valid, rsa-sha1 MUST NOT be used;
RFC 8463 (k=ed25519, 32 byte public key); Google email sender guidelines (support.google.com/mail/answer/81126):
personal Gmail needs a DKIM key of 1024 bits or longer, 2048 recommended if the DNS provider supports it; Amazon SES
BYODKIM (docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-authentication-dkim-bring-your-own.html): RSA 1024 to
2048 bits, PKCS #1 or PKCS #8, header lines and line breaks removed when pasted.
Search demand: "dkim record generator" and "dkim generator" are served by PowerDMARC, MailSlurp, ZeroBounce, SmartReach,
Salesforge, CaptainDNS and others. Most create the private key on their server. This one creates it with the browser's
Web Crypto API, so the private key never leaves the device, and adds a paste based record checker with key size."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/email-marketing-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

CHECK = ('s1._domainkey.yourshop.in. 3600 IN TXT "v=DKIM1; k=rsa; t=y; " "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChRIzjXmN4VhTfHHQ6AXlOxCRkzL/580epK3cfA6GFdAvBc276sYN4D6ePVVri1jQ/2AqjCFjLir4romIGsHwzotRLtGHK6cO0UJlYEVCz2sdmorgbpy/TfsM4wT43vi9HYASYEkjCeAYYr0mRZ25EWT9nnOddNdOwyywhn7H7KQIDAQAB"')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='dkim-record-generator', short='DK', name='DKIM Record Generator and Checker',
        card='Create a DKIM key pair and the TXT record for your DNS right in your browser, or paste a record to check its tags and key size.',
        title='DKIM Record Generator and Checker: Free Key Pair',
        desc='Free DKIM record generator. Create a 2048 bit key pair and TXT record in your browser, or check an existing DKIM record and key size. Keys stay on your device.',
        h1='DKIM Record Generator and Checker',
        lead='Pick a selector and key size to get a fresh DKIM private key and the matching TXT record, with the exact host name for your DNS panel. The keys are created by your own browser, so the private key is never sent anywhere. Already have a record? Paste it into the checker below.',
        tool='''<section class="tool" aria-label="DKIM record generator">
    <div class="card" style="min-width:0">
      <h2>Create a DKIM Key</h2>
      ''' + F('dkDom', 'Your domain', 'yourshop.in', em='the domain that signs the email', mono=True) + '''
      ''' + F('dkSel', 'Selector', 's1', em='any short name, such as s1 or mail2026', mono=True) + '''
      <div class="row2">''' + F('dkBits', 'Key size', '2048', tag='select', opts=[('2048', '2048 bit (recommended)'), ('1024', '1024 bit (short DNS records)'), ('4096', '4096 bit (very long record)')]) + F('dkFmt', 'Private key format', 'p8', tag='select', opts=[('p8', 'PKCS #8 (BEGIN PRIVATE KEY)'), ('p1', 'PKCS #1 (BEGIN RSA PRIVATE KEY)')]) + '''</div>
      ''' + CK('dkT', 'Test mode (<code>t=y</code>): tell receivers you are still testing DKIM', False) + '''
      <div class="actions" style="margin:6px 0 12px"><button class="btn dark" id="dkGen">Generate New Keys</button></div>
      <p style="font-size:14px;margin:0 0 6px"><strong>Private key</strong> <em>keep it secret, it goes on your mail server only</em></p>
      <textarea id="dkPriv" class="mono" readonly spellcheck="false" aria-label="Private key" style="min-height:180px;width:100%"></textarea>
      <div class="actions" style="margin:10px 0 0"><button class="btn dark" id="dkCopyPriv">Copy Private Key</button><button class="btn" id="dkDl">Download Key File</button><button class="btn" id="dkOne">Copy as One Line</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Your DNS Record</h2>
      <div style="overflow-x:auto"><table class="rtable"><tbody>
        <tr><td style="width:30%"><strong>Type</strong></td><td class="mono">TXT</td></tr>
        <tr><td><strong>Host or Name</strong></td><td class="mono" id="dkHost" style="word-break:break-all"></td></tr>
        <tr><td><strong>Full name</strong></td><td class="mono" id="dkFull" style="word-break:break-all"></td></tr>
        <tr><td><strong>TTL</strong></td><td class="mono">3600 or your panel default</td></tr>
      </tbody></table></div>
      <p style="font-size:14px;margin:14px 0 6px"><strong>Value</strong> <em id="dkLen"></em></p>
      <div class="code-out mono" id="dkRec" style="word-break:break-all;white-space:pre-wrap"></div>
      <div class="actions" style="margin:12px 0"><button class="btn dark" id="dkCopy">Copy Record</button><button class="btn" id="dkCopyHost">Copy Host</button><button class="btn" id="dkCopySplit">Copy Split Version</button></div>
      <div class="kw-result" id="dkNotes"></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Check an Existing DKIM Record</h2>
      ''' + F('dkIn', 'Paste your DKIM record', CHECK, em='a zone file line, quotes and split strings are fine', tag='textarea', mono=True, extra=' style="min-height:100px"') + '''
      <div class="stats">''' + S('dkcType', 'Key type') + S('dkcBits', 'Key size') + S('dkcTags', 'Tags') + S('dkcIss', 'Problems') + '''</div>
      <div class="kw-result" id="dkCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="dkTags"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="dkRep">Copy Report</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var DOM = /^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$/i;
  var SEL = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$/i;
  var SLD = {co:1, com:1, net:1, org:1, gov:1, ac:1, edu:1, gen:1, firm:1, ind:1, res:1, ltd:1, plc:1, me:1, nic:1};
  function org(d){ var p = d.split('.'); if (p.length > 2 && p[p.length - 1].length === 2 && SLD[p[p.length - 2]]) return p.slice(-3).join('.'); return p.slice(-2).join('.'); }
  function cleanDom(v){ return v.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/[\/:].*$/, '').replace(/\.$/, ''); }
  function b64(buf){ var b = new Uint8Array(buf), s = ''; for (var i = 0; i < b.length; i++) s += String.fromCharCode(b[i]); return btoa(s); }
  function pem(label, u8){ return '-----BEGIN ' + label + '-----\n' + b64(u8).match(/.{1,64}/g).join('\n') + '\n-----END ' + label + '-----\n'; }
  function tlv(b, i){
    if (i + 2 > b.length) throw new Error('short');
    var t = b[i], l = b[i + 1], h = 2;
    if (l & 0x80){ var n = l & 0x7f; if (n < 1 || n > 4) throw new Error('len'); l = 0; for (var k = 0; k < n; k++) l = l * 256 + b[i + 2 + k]; h = 2 + n; }
    if (i + h + l > b.length) throw new Error('short');
    return {t: t, s: i + h, e: i + h + l};
  }
  function pkcs1(p8){ var top = tlv(p8, 0), v = tlv(p8, top.s), alg = tlv(p8, v.e), os = tlv(p8, alg.e); return p8.slice(os.s, os.e); }
  function split255(s){ return (s.match(/.{1,255}/g) || ['']).map(function(x){ return '"' + x + '"'; }).join(' '); }

  var keys = null, rec = '', host = '', full = '';
  function privText(){ if (!keys) return ''; return $('dkFmt').value === 'p1' ? pem('RSA PRIVATE KEY', pkcs1(keys.p8)) : pem('PRIVATE KEY', keys.p8); }
  function gen(){
    if (!window.crypto || !crypto.subtle){ say('dkNotes', 'bad', 'Your browser cannot create keys on this page. Open it over https in a current version of Chrome, Edge, Firefox or Safari.'); return; }
    var bits = +$('dkBits').value; $('dkGen').disabled = true; keys = null;
    $('dkPriv').value = 'Creating a ' + bits + ' bit key...'; $('dkRec').textContent = ''; say('dkNotes', '', 'Creating your key pair in this browser' + (bits === 4096 ? '. A 4096 bit key can take a few seconds.' : '.'));
    crypto.subtle.generateKey({name: 'RSASSA-PKCS1-v1_5', modulusLength: bits, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256'}, true, ['sign', 'verify'])
      .then(function(kp){ return Promise.all([crypto.subtle.exportKey('spki', kp.publicKey), crypto.subtle.exportKey('pkcs8', kp.privateKey)]); })
      .then(function(r){ keys = {pub: b64(r[0]), p8: new Uint8Array(r[1]), bits: bits}; $('dkGen').disabled = false; render(); })
      .catch(function(){ $('dkGen').disabled = false; $('dkPriv').value = ''; say('dkNotes', 'bad', 'The browser could not create the key. Try again, or pick 2048 bit.'); });
  }
  function render(){
    var d = cleanDom($('dkDom').value), sel = $('dkSel').value.trim().toLowerCase().replace(/\._domainkey.*$/, ''), bad = [];
    if (!d || !DOM.test(d)) bad.push('Enter a valid domain, such as ' + c('yourshop.in') + '.');
    if (!sel || !SEL.test(sel)) bad.push('The selector can use letters, numbers and dots only, such as ' + c('s1') + ' or ' + c('mail2026') + '.');
    var od = d && DOM.test(d) ? org(d) : d;
    full = (sel || 'selector') + '._domainkey.' + (d || 'yourdomain.com');
    host = (sel || 'selector') + '._domainkey' + (d && od !== d ? '.' + d.slice(0, -od.length - 1) : '');
    $('dkHost').textContent = host; $('dkFull').textContent = full;
    if (!keys){ return; }
    $('dkPriv').value = privText();
    var t = ['v=DKIM1', 'k=rsa']; if ($('dkT').checked) t.push('t=y'); t.push('p=' + keys.pub);
    rec = t.join('; ');
    $('dkRec').textContent = rec; $('dkLen').textContent = rec.length + ' characters' + (rec.length > 255 ? ', longer than one 255 character string' : '');
    $('dkCopySplit').style.display = rec.length > 255 ? '' : 'none';
    if (bad.length){ say('dkNotes', 'bad', '<strong>Fix this first:</strong> ' + bad.join(' ')); return; }
    var N = [], cls = 'ok';
    if (keys.bits === 2048) N.push('<strong>Good choice.</strong> 2048 bit is the size Google recommends and the size RFC 8301 asks signers to use.');
    else if (keys.bits === 1024){ cls = 'warn'; N.push('<strong>1024 bit is the minimum</strong> Gmail accepts. Use it only if your DNS panel cannot save a long record, and move to 2048 bit when you can.'); }
    else { cls = 'warn'; N.push('<strong>4096 bit keys make a very long record.</strong> Receivers must support up to 4096 bit, but some DNS panels cannot save it and Amazon SES accepts at most 2048 bit.'); }
    if (rec.length > 255) N.push('Most DNS panels accept the long value as is. If yours shows an error, or you edit a zone file, use the split version, which breaks it into quoted strings of 255 characters that receivers join back together.');
    if ($('dkT').checked) N.push('Test mode is on. Receivers treat your signed mail like unsigned mail, so remove ' + c('t=y') + ' as soon as signing works.');
    N.push('<strong>Save the private key now.</strong> It was made in this browser and is not stored anywhere. Install it on your mail server with selector ' + c(sel) + ' and domain ' + c(d) + ', then add the TXT record in your DNS panel.');
    say('dkNotes', cls, N.join('<br>'));
  }

  var INFO = {v: 'Version. Optional, but if present it must be DKIM1 and come first.', k: 'Key type: rsa (the default) or ed25519.', p: 'The public key in base64. Required. An empty value means the key is revoked.',
    h: 'Hash algorithms this key may be used with. Leave it out to allow all.', s: 'Service type: * (the default) or email.', t: 'Flags: y means testing, s means the i= domain must exactly match d=.', n: 'Notes for people. Receivers ignore it.',
    g: 'Removed in RFC 6376. Receivers ignore it.'};
  var rows = [], verdict = '';
  function check(){
    var raw = $('dkIn').value, v = raw.trim(), info = [];
    var nm = v.match(/([a-z0-9][a-z0-9.\-]*)\._domainkey\.([a-z0-9.\-]+[a-z])\.?/i);
    var q = v.match(/"((?:[^"\\]|\\.)*)"/g);
    if (q) v = q.map(function(x){ return x.slice(1, -1).replace(/\\(.)/g, '$1'); }).join('');
    else v = v.replace(/^[^=]*?\bTXT\s+/i, '');
    v = v.trim();
    rows = []; var E = 0, W = 0, seen = {}, tags = {}, type = 'rsa', bits = '';
    function add(tag, val, st, msg){ rows.push([tag, val, st, msg]); if (st === 'bad') E++; else if (st === 'warn') W++; }
    if (!v){ ['dkcType', 'dkcBits', 'dkcTags', 'dkcIss'].forEach(function(i){ $(i).textContent = '0'; }); say('dkCheck', '', 'Paste a DKIM TXT record to check it.'); $('dkTags').innerHTML = ''; verdict = ''; return; }
    var parts = v.split(';').map(function(x){ return x.trim(); }).filter(Boolean);
    parts.forEach(function(p, i){
      var eq = p.indexOf('=');
      if (eq < 1){ add(p, '', 'bad', 'Not a tag. Each part must look like ' + c('name=value') + ', separated by semicolons.'); return; }
      var n = p.slice(0, eq).trim(), val = p.slice(eq + 1).trim();
      if (seen[n]){ add(n, val, 'bad', 'This tag appears twice. Receivers then reject the whole record.'); return; }
      seen[n] = 1; tags[n] = val;
      if (n === 'v'){ if (val !== 'DKIM1') add(n, val, 'bad', 'Must be exactly ' + c('DKIM1') + ', or the record is thrown away.'); else if (i !== 0) add(n, val, 'bad', 'The version tag must come first in the record.'); else add(n, val, 'ok', INFO.v); }
      else if (n === 'k'){ type = val.toLowerCase(); if (val === 'rsa') add(n, val, 'ok', INFO.k); else if (val === 'ed25519') add(n, val, 'warn', 'Ed25519 key (RFC 8463). Valid, but not every receiver checks it yet, so also sign with an RSA key under another selector.'); else add(n, val, 'bad', 'Unknown key type. Use ' + c('rsa') + ' or ' + c('ed25519') + '.'); }
      else if (n === 'h'){ var hs = val.split(':').map(function(x){ return x.trim(); }); if (hs.indexOf('sha256') >= 0) add(n, val, hs.indexOf('sha1') >= 0 ? 'warn' : 'ok', hs.indexOf('sha1') >= 0 ? 'SHA1 is historic under RFC 8301 and must not be used. Keep only ' + c('sha256') + '.' : INFO.h); else add(n, val, 'bad', 'Only allows ' + c(val) + '. Signatures must use ' + c('sha256') + ', so this key cannot verify any valid signature. Remove the tag or set ' + c('h=sha256') + '.'); }
      else if (n === 's'){ var ss = val.split(':').map(function(x){ return x.trim(); }); if (ss.indexOf('*') >= 0 || ss.indexOf('email') >= 0) add(n, val, 'ok', INFO.s); else add(n, val, 'bad', 'This key is not allowed for email. Remove the tag or use ' + c('s=email') + '.'); }
      else if (n === 't'){ var fl = val.split(':').map(function(x){ return x.trim(); }); if (fl.indexOf('y') >= 0) add(n, val, 'warn', 'Testing mode. Receivers treat your signed mail like unsigned mail, so DKIM gives you no benefit. Remove ' + c('y') + ' once signing works.'); else if (fl.indexOf('s') >= 0) add(n, val, 'ok', 'Strict: mail must be signed with the exact domain, not a subdomain.'); else add(n, val, 'ok', INFO.t); }
      else if (n === 'p'){ /* checked below */ }
      else if (INFO[n]) add(n, val, n === 'g' ? 'warn' : 'ok', INFO[n]);
      else if (INFO[n.toLowerCase()]) add(n, val, 'bad', 'Tag names are case sensitive. Write ' + c(n.toLowerCase()) + ' in lower case, or receivers ignore it.');
      else add(n, val, 'warn', 'Unknown tag. Receivers ignore it.');
    });
    if (!('p' in tags)){ add('p', '', 'bad', 'Missing. Every DKIM record needs the public key in ' + c('p=') + '.'); }
    else {
      var pv = tags.p.replace(/\s+/g, ''), pshow = pv.length > 40 ? pv.slice(0, 20) + '...' + pv.slice(-12) : pv;
      if (pv === '') add('p', '(empty)', 'bad', 'Empty, which means this key is revoked. Mail signed with this selector fails DKIM.');
      else if (/BEGIN|END/.test(tags.p)) add('p', pshow, 'bad', 'Contains PEM header lines. Paste only the base64 text between them, with no line breaks.');
      else if (!/^[A-Za-z0-9+\/]+={0,2}$/.test(pv) || pv.length % 4 === 1) add('p', pshow, 'bad', 'Not valid base64. Check for missing characters or stray quotes after joining the strings.');
      else {
        var bin; try { bin = atob(pv); } catch (e) { bin = null; }
        if (bin === null) add('p', pshow, 'bad', 'Not valid base64.');
        else {
          var u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
          if (type === 'ed25519'){ if (u.length === 32){ bits = '256'; add('p', pshow, 'ok', 'A 32 byte Ed25519 public key.'); } else add('p', pshow, 'bad', 'An Ed25519 key must be exactly 32 bytes, this one is ' + u.length + '.'); }
          else {
            var r = null; try { r = rsa(u); } catch (e) { r = null; }
            if (!r) add('p', pshow, 'bad', 'This is not a readable RSA public key. It may be cut short.');
            else if (r.err) add('p', pshow, 'bad', r.err);
            else {
              bits = String(r.bits);
              var msg = r.bits + ' bit RSA key, exponent ' + r.exp + '.';
              if (r.bits < 1024) add('p', pshow, 'bad', msg + ' Keys under 1024 bit are not valid under RFC 8301 and Gmail rejects them. Create a 2048 bit key.');
              else if (r.bits < 2048) add('p', pshow, 'warn', msg + ' This meets the Gmail minimum, but Google recommends 2048 bit. Plan a new key.');
              else if (r.bits > 4096) add('p', pshow, 'warn', msg + ' Receivers only have to support keys up to 4096 bit.');
              else add('p', pshow, 'ok', msg + ' A strong key size.');
              if (r.form === 'pkcs1') add('p', 'format', 'warn', 'The key is in the bare RSAPublicKey form. Most systems publish the SubjectPublicKeyInfo form, which some receivers require.');
            }
          }
        }
      }
    }
    if (!('v' in tags)) add('v', '(missing)', 'info', 'Optional, but adding ' + c('v=DKIM1') + ' at the start is recommended.');
    if (v.length > 255 && !q) info.push('This record is ' + v.length + ' characters. If your DNS panel refuses it, split it into quoted strings of up to 255 characters.');
    if (nm) info.push('Selector ' + c(nm[1].toLowerCase()) + ' on domain ' + c(nm[2].toLowerCase()) + '.');
    $('dkcType').textContent = ('k' in tags) ? tags.k : 'rsa'; $('dkcBits').textContent = bits || 'n/a'; $('dkcTags').textContent = Object.keys(tags).length; $('dkcIss').textContent = E + W;
    var cls = E ? 'bad' : W ? 'warn' : 'ok';
    verdict = E ? E + ' error' + (E === 1 ? '' : 's') + ': this record will not work as it is.' : W ? 'The record works, with ' + W + ' thing' + (W === 1 ? '' : 's') + ' to improve.' : 'This DKIM record looks valid.';
    say('dkCheck', cls, '<strong>' + verdict + '</strong>' + (info.length ? '<br>' + info.join('<br>') : ''));
    var lab = {ok: 'OK', warn: 'Improve', bad: 'Error', info: 'Note'};
    $('dkTags').innerHTML = '<thead><tr><th>Tag</th><th>Value</th><th>Status</th><th>What it means</th></tr></thead><tbody>' + rows.map(function(x){
      return '<tr><td class="mono">' + esc(x[0]) + '</td><td class="mono" style="word-break:break-all">' + esc(x[1]) + '</td><td>' + lab[x[2]] + '</td><td>' + x[3] + '</td></tr>'; }).join('') + '</tbody>';
  }
  function rsa(b){
    var top = tlv(b, 0); if (top.t !== 0x30) return null;
    var f = tlv(b, top.s), n, e, form = 'spki';
    if (f.t === 0x30){
      var oid = tlv(b, f.s), h = ''; for (var i = oid.s; i < oid.e; i++) h += ('0' + b[i].toString(16)).slice(-2);
      if (h === '2b6570') return {err: 'This is an Ed25519 key in SubjectPublicKeyInfo form. Set ' + c('k=ed25519') + ' and publish only the raw 32 byte key.'};
      if (h !== '2a864886f70d010101') return {err: 'This is not an RSA key. Check that you copied the public key, not a certificate.'};
      var bs = tlv(b, f.e); if (bs.t !== 0x03) return null;
      var rs = tlv(b, bs.s + 1); if (rs.t !== 0x30) return null;
      n = tlv(b, rs.s); e = tlv(b, n.e);
    } else if (f.t === 0x02){ form = 'pkcs1'; n = f; e = tlv(b, n.e); }
    else return null;
    if (n.t !== 0x02 || e.t !== 0x02) return null;
    var s = n.s; while (s < n.e && b[s] === 0) s++;
    if (s >= n.e) return null;
    var hi = 7; while (hi > 0 && !(b[s] & (1 << hi))) hi--;
    var exp = 0; for (var j = e.s; j < e.e; j++) exp = exp * 256 + b[j];
    return {bits: (n.e - s - 1) * 8 + hi + 1, exp: exp, form: form};
  }

  $('dkGen').onclick = gen;
  $('dkBits').addEventListener('change', gen);
  ['dkDom', 'dkSel'].forEach(function(i){ $(i).addEventListener('input', render); });
  ['dkFmt', 'dkT'].forEach(function(i){ $(i).addEventListener('change', render); });
  $('dkCopy').onclick = function(){ if (rec) copyText(rec, 'toast'); };
  $('dkCopyHost').onclick = function(){ copyText(host, 'toast'); };
  $('dkCopySplit').onclick = function(){ if (rec) copyText(split255(rec), 'toast'); };
  $('dkCopyPriv').onclick = function(){ if (keys) copyText(privText(), 'toast'); };
  $('dkOne').onclick = function(){ if (keys) copyText(privText().split('\n').filter(function(l){ return l && l.indexOf('-----') !== 0; }).join(''), 'toast'); };
  $('dkDl').onclick = function(){ if (keys) download(($('dkSel').value.trim() || 'dkim') + '.private', privText(), 'application/x-pem-file'); };
  $('dkIn').addEventListener('input', check);
  $('dkRep').onclick = function(){ if (!verdict) return; copyText('DKIM record check\n' + verdict + '\n\n' + rows.map(function(x){ return x[0] + ' = ' + x[1] + '\n  ' + x[2].toUpperCase() + ': ' + x[3].replace(/<[^>]+>/g, ''); }).join('\n'), 'toast'); };
  render(); check(); gen();
''',
        content=f'''
    <h2>What Is a DKIM Record?</h2>
    <p>DKIM, short for DomainKeys Identified Mail, lets your mail server add a digital signature to every email it sends. The signature is made with a private key that stays on your server. Receivers like Gmail and Outlook then look up the matching public key in your DNS, in a TXT record at <code>selector._domainkey.yourdomain.com</code>, and check that the email really came from you and was not changed on the way.</p>
    <p>This generator creates both keys with the Web Crypto API that is built into your browser. Many online DKIM generators make the private key on their own server, which means someone else has seen it. Here it never leaves your device.</p>

    <h2>How to Set Up DKIM With This Tool</h2>
    <ol>
      <li><strong>Enter your domain and a selector.</strong> The selector is just a label, so you can run several keys side by side, such as <code>s1</code> now and <code>s2</code> when you rotate.</li>
      <li><strong>Keep 2048 bit</strong> unless your DNS panel refuses long records.</li>
      <li><strong>Save the private key.</strong> Copy or download it and install it in your mail server or sending service with the same selector and domain.</li>
      <li><strong>Add the TXT record</strong> in your DNS panel using the host name shown. Changes can take up to a few hours to appear.</li>
      <li><strong>Send a test email</strong> to a Gmail address and check that DKIM shows as pass in the full headers.</li>
    </ol>
    <p><strong>Using Google Workspace, Microsoft 365, Mailchimp, Brevo or a similar service?</strong> They create the DKIM key for you. Use the record they give you and paste it into the checker above. This generator is for your own mail server, such as Postfix with OpenDKIM, or services that let you bring your own key, like <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-authentication-dkim-bring-your-own.html" {EXT}>Amazon SES</a>. For SES, use 1024 or 2048 bit and the Copy as One Line button.</p>

    <h2>DKIM Record Tags Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Tag', 'What it does')}
      <tbody>
        <tr><td><code>v=DKIM1</code></td><td>Version. Optional, but when used it must be the first tag.</td></tr>
        <tr><td><code>k=rsa</code></td><td>Key type. RSA is the default and works everywhere. <code>ed25519</code> is newer and not checked by every receiver.</td></tr>
        <tr><td><code>p=</code></td><td>The public key in base64. Required. An empty <code>p=</code> revokes the key.</td></tr>
        <tr><td><code>t=y</code></td><td>Testing mode. Receivers treat your mail as if it had no signature, so remove it after testing.</td></tr>
        <tr><td><code>t=s</code></td><td>Strict mode. Mail signed for a subdomain does not match this key.</td></tr>
        <tr><td><code>h=</code> and <code>s=</code></td><td>Limit the hash and service. Most records leave them out.</td></tr>
      </tbody>
    </table></div>
    <p>These rules come from <a href="https://www.rfc-editor.org/rfc/rfc6376" {EXT}>RFC 6376</a> and the key size update in <a href="https://www.rfc-editor.org/rfc/rfc8301" {EXT}>RFC 8301</a>, which says signers must use at least 1024 bit RSA keys and should use 2048 bit.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Rotate keys once or twice a year.</strong> Publish a new selector, switch your server to it, and keep the old record for a week so mail in transit still verifies.</li>
      <li><strong>Long record errors?</strong> Some DNS panels limit one string to 255 characters. Use the split version, which receivers join back together.</li>
      <li><strong>Never email the private key.</strong> Anyone who has it can sign mail as your domain.</li>
      <li><strong>DKIM alone is not enough.</strong> Gmail and Yahoo want bulk senders to have SPF, DKIM and DMARC together, with the DKIM domain matching your From address.</li>
    </ul>

    <h2>Finish Your Email Authentication</h2>
    <p>With DKIM in place, add the other two records with the <a href="{T}spf-record-generator/">SPF record generator</a> and the <a href="{T}dmarc-record-generator/">DMARC record generator</a>, then confirm all three pass with the <a href="{T}email-header-analyzer/">email header analyzer</a>. For the bigger picture, read our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, and if your website sends its own mail, see <a href="{B}send-email-code-in-php/">send email code in PHP</a> and <a href="{B}how-hosting-affects-seo/">how hosting affects SEO</a>.</p>
''',
        faqs=[
            ("Is it safe to create a DKIM private key in the browser?", "Yes. The key is made by your browser's built in Web Crypto API, the same code browsers use for secure connections. Nothing is uploaded or stored, so copy or download the private key before you close the page."),
            ("Should I use a 1024 or 2048 bit DKIM key?", "Use 2048 bit. Google recommends it and RFC 8301 asks signers to use it. 1024 bit is the minimum Gmail accepts, so only use it if your DNS provider cannot save the longer record."),
            ("What is a DKIM selector?", "A short name that tells receivers which key to look up, so the record lives at selector._domainkey.yourdomain.com. You can pick any name. Using a new selector for each key makes rotation easy, because old and new keys can live side by side."),
            ("Why does my DKIM check fail after adding the record?", "Common causes are a DNS change that has not spread yet, a host name with the domain added twice, a key that was cut short or split wrongly, or a selector that does not match the one your server signs with. Paste the record into the checker above to see which part is wrong."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("Send Email Code in PHP", "send-email-code-in-php"),
                 ("PHP Contact Form Spam Protection", "php-contact-form-spam-protection"), ("How Hosting Affects SEO", "how-hosting-affects-seo")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'email-marketing-tools'; t['updated'] = '2026-11-14'
