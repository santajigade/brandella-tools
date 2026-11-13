"""Batch 16 (2026-11-13): Email Marketing Tools, fifth tool (Email Header Analyzer).
Facts checked 2026-11-13 against: Google, Trace an email with its full header (support.google.com/mail/answer/29436):
Gmail More then Show original, Outlook File then Properties (Internet headers), Apple Mail View then Message then
All Headers, Yahoo More then View Raw Message; Google email sender guidelines (support.google.com/mail/answer/81126):
TLS for all senders, From domain aligned with SPF or DKIM domain, one click unsubscribe for marketing mail above 5,000
messages a day, spam rate below 0.3%; RFC 8601 (Authentication-Results: authserv id, method=result, ptype.property);
RFC 5321 section 4.4 (each relay adds a Received trace line at the top, so the newest is first); RFC 8058
(List-Unsubscribe-Post: List-Unsubscribe=One-Click); RFC 6376 (DKIM-Signature d= and s= tags).
Search demand: "email header analyzer" is served by MxToolbox, Google Admin Toolbox Messageheader, PowerDMARC,
Mailmodo and others, which send the headers to a server. This one parses locally and adds marketer checks
(alignment, one click unsubscribe, TLS, slow hops)."""
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/email-marketing-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

SAMPLE = '''Delivered-To: priya.sharma@gmail.com
Received: by 2002:a05:7300:5b14:b0:1a2:3c4d:5e6f with SMTP id k20csp412345dyb;
        Thu, 12 Nov 2026 01:47:09 -0800 (PST)
X-Received: by 2002:a17:90b:4c12:b0:2f1:8e3a:1c2d with SMTP id mz18mr774512pjb.31.1794476829104;
        Thu, 12 Nov 2026 01:47:09 -0800 (PST)
ARC-Seal: i=1; a=rsa-sha256; t=1794476829; cv=none; d=google.com; s=arc-20240605; b=Qm9ndXNTZWFs
ARC-Authentication-Results: i=1; mx.google.com;
       dkim=pass header.i=@acmetraders.in header.s=s1 header.b=Xy12AbCd;
       spf=pass smtp.mailfrom="bounce+a1b2c3@mail.acmetraders.in";
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from=acmetraders.in
Return-Path: <bounce+a1b2c3@mail.acmetraders.in>
Received: from mta1.mail.acmetraders.in (mta1.mail.acmetraders.in. [203.0.113.25])
        by mx.google.com with ESMTPS id 5b1f17b1804b1-47a1c2d3e4fsi123456f9.140.2026.11.12.01.47.08
        for <priya.sharma@gmail.com>
        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 bits=256/256);
        Thu, 12 Nov 2026 01:47:08 -0800 (PST)
Received-SPF: pass (google.com: domain of bounce+a1b2c3@mail.acmetraders.in designates 203.0.113.25 as permitted sender) client-ip=203.0.113.25;
Authentication-Results: mx.google.com;
       dkim=pass header.i=@acmetraders.in header.s=s1 header.b=Xy12AbCd;
       spf=pass (google.com: domain of bounce+a1b2c3@mail.acmetraders.in designates 203.0.113.25 as permitted sender) smtp.mailfrom="bounce+a1b2c3@mail.acmetraders.in";
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from=acmetraders.in
Received: from app2.internal.acmetraders.in (app2.internal.acmetraders.in [10.0.4.12])
        by mta1.mail.acmetraders.in (Postfix) with ESMTP id 4C8F21A0042
        for <priya.sharma@gmail.com>; Thu, 12 Nov 2026 09:46:31 +0000 (UTC)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=acmetraders.in; s=s1;
        t=1794476790; h=from:to:subject:date:message-id:list-unsubscribe:list-unsubscribe-post;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; b=Xy12AbCdEfGh
From: "Acme Traders" <offers@acmetraders.in>
Reply-To: Acme Care <care@acmetraders.in>
To: priya.sharma@gmail.com
Subject: Your Diwali offer: 20% off ends tonight
Date: Thu, 12 Nov 2026 15:16:30 +0530
Message-ID: <20261112094630.4C8F21A0042@mail.acmetraders.in>
List-Unsubscribe: <https://acmetraders.in/unsub?u=a1b2c3>, <mailto:unsub-a1b2c3@mail.acmetraders.in>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="b1"
X-Mailer: Acme Mailer 3.2'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='email-header-analyzer', short='EH', name='Email Header Analyzer',
        card='Paste raw email headers to see SPF, DKIM and DMARC results, alignment, every server hop with delays, and red flags.',
        title='Email Header Analyzer: Check SPF, DKIM, DMARC and Hops',
        desc='Free email header analyzer. Paste full headers to see SPF, DKIM and DMARC results, alignment, delivery hops and delays, and phishing signs. Nothing is uploaded.',
        h1='Email Header Analyzer',
        lead='Paste the full headers of any email to find out why it landed in spam, whether it really came from the sender it claims, and where it was delayed on the way. Everything is read in your browser, so private headers never leave your device.',
        tool='''<section class="tool" aria-label="Email header analyzer">
    <div class="card" style="min-width:0">
      <h2>Paste Email Headers</h2>
      ''' + F('ehIn', 'Full email headers', SAMPLE, em='in Gmail open the email, then More and Show original', tag='textarea', mono=True, extra=' style="min-height:320px"') + '''
      <div class="actions" style="margin:0"><button class="btn dark" id="ehRun">Analyze Headers</button><button class="btn" id="ehClear">Clear</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Verdict</h2>
      <div class="stats">''' + S('ehSpf', 'SPF') + S('ehDkim', 'DKIM') + S('ehDmarc', 'DMARC') + S('ehHops', 'Hops') + S('ehTime', 'Total delay') + '''</div>
      <div class="kw-result" id="ehNote"></div>
      <div style="overflow-x:auto"><table class="rtable" id="ehSum"></table></div>
      <div class="actions" style="margin:12px 0 0"><button class="btn dark" id="ehCopy">Copy Report</button><span class="toast" id="toast">Copied!</span></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Checks</h2>
      <div style="overflow-x:auto"><table class="rtable" id="ehChk"></table></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Delivery Path, Oldest Hop First</h2>
      <div style="overflow-x:auto"><table class="rtable" id="ehPath"></table></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>All Headers</h2>
      ''' + F('ehFind', 'Filter headers', '', ph='such as dkim, received or x-', extra=' autocomplete="off"') + '''
      <div style="overflow-x:auto;max-height:420px;overflow-y:auto"><table class="rtable" id="ehAll"></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var SLD = {co:1, com:1, net:1, org:1, ac:1, gov:1, edu:1, gen:1, firm:1, ind:1, ltd:1, plc:1, me:1, nic:1, res:1};
  function org(d){
    d = (d || '').toLowerCase().replace(/\.$/, '');
    var p = d.split('.'); if (p.length < 3) return d;
    var n = (SLD[p[p.length - 2]] && p[p.length - 1].length === 2) ? 3 : 2;
    return p.slice(-n).join('.');
  }
  function dom(a){ a = (a || '').replace(/^.*</, '').replace(/>.*$/, '').replace(/^"|"$/g, '').trim(); var i = a.lastIndexOf('@'); return (i > -1 ? a.slice(i + 1) : a).toLowerCase().replace(/[>"\s].*$/, ''); }
  function addr(v){ var m = /<([^>]+)>/.exec(v || ''); return (m ? m[1] : (v || '').replace(/\(.*?\)/g, '')).trim(); }
  function noCom(s){ var o = '', d = 0; for (var i = 0; i < s.length; i++){ var ch = s[i]; if (ch === '(') d++; else if (ch === ')' && d) d--; else if (!d) o += ch; } return o; }
  function parse(raw){
    var lines = raw.replace(/\r/g, '').split('\n'), hs = [], cur = null;
    for (var i = 0; i < lines.length; i++){
      var l = lines[i];
      if (!l.trim()){ if (hs.length) break; else continue; }
      if (/^[ \t]/.test(l) && cur){ cur.v += ' ' + l.trim(); continue; }
      var m = /^([!-9;-~]+):\s?(.*)$/.exec(l);
      if (m){ cur = {n: m[1], k: m[1].toLowerCase(), v: m[2].trim()}; hs.push(cur); }
    }
    return hs;
  }
  function get(hs, k){ for (var i = 0; i < hs.length; i++) if (hs[i].k === k) return hs[i].v; return ''; }
  function all(hs, k){ return hs.filter(function(h){ return h.k === k; }).map(function(h){ return h.v; }); }
  function pdate(s){
    s = noCom(s || '').replace(/\s+/g, ' ').trim(); if (!s) return null;
    var t = Date.parse(s); if (!isNaN(t)) return t;
    t = Date.parse(s.replace(/^[A-Za-z]{3},\s*/, '')); return isNaN(t) ? null : t;
  }
  function dur(ms){
    if (ms === null || isNaN(ms)) return 'unknown';
    var neg = ms < 0, s = Math.round(Math.abs(ms) / 1000), o;
    if (s < 60) o = s + ' sec'; else if (s < 3600) o = Math.floor(s / 60) + ' min ' + (s % 60) + ' sec'; else if (s < 86400) o = Math.floor(s / 3600) + ' hr ' + Math.floor(s % 3600 / 60) + ' min'; else o = Math.floor(s / 86400) + ' days ' + Math.floor(s % 86400 / 3600) + ' hr';
    return (neg ? 'minus ' : '') + o;
  }
  function priv(ip){ return /^(10\.|127\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|::1$|f[cd][0-9a-f]{2}:|fe80:)/i.test(ip); }
  function hop(v){
    var semi = v.lastIndexOf(';'), body = semi > -1 ? v.slice(0, semi) : v, date = semi > -1 ? v.slice(semi + 1) : '';
    var t = pdate(date); if (t === null){ body = v; }
    var b = noCom(body).replace(/\s+/g, ' ');
    function part(w){ var m = new RegExp('(?:^|\\s)' + w + '\\s+(\\S+)', 'i').exec(b); return m ? m[1] : ''; }
    var ipm = /\[(?:IPv6:)?([0-9a-f:.]{3,})\]/i.exec(body.split(/\sby\s/i)[0]);
    return {from: part('from').replace(/\.$/, ''), by: part('by').replace(/\.$/, ''), wth: part('with'), ip: ipm ? ipm[1] : '', t: t, tls: /ESMTPS|ESMTPSA|LMTPS|TLS1|TLSv1|version=TLS/i.test(v)};
  }
  function authres(v){
    var s = noCom(v).replace(/\s+/g, ' '), parts = s.split(';'), id = parts.shift().trim().split(' ')[0], r = {id: id, m: []};
    parts.forEach(function(p){
      var m = /^\s*([a-z0-9_-]+)\s*=\s*([a-z]+)(.*)$/i.exec(p); if (!m) return;
      var props = {}, re = /([a-z]+\.[a-z0-9_-]+)\s*=\s*("?)([^\s";]*)\2/gi, x;
      while ((x = re.exec(m[3]))) props[x[1].toLowerCase()] = x[3];
      r.m.push({k: m[1].toLowerCase(), r: m[2].toLowerCase(), p: props});
    });
    return r;
  }
  function tags(v){ var o = {}; v.replace(/\s+/g, '').split(';').forEach(function(p){ var i = p.indexOf('='); if (i > 0) o[p.slice(0, i).toLowerCase()] = p.slice(i + 1); }); return o; }
  var MEAN = {pass: 'Passed', fail: 'Failed', softfail: 'Soft fail', neutral: 'Neutral', none: 'Not set up', temperror: 'Temporary error', permerror: 'Record error', policy: 'Policy', bestguesspass: 'Best guess pass'};
  var report = '';
  function row(st, what, why){ var col = st === 'ok' ? '#1a7f37' : st === 'warn' ? '#9a6700' : '#cf222e', lab = st === 'ok' ? 'Good' : st === 'warn' ? 'Check' : 'Problem'; return {h: '<tr><td style="color:' + col + ';font-weight:700;white-space:nowrap">' + lab + '</td><td><strong>' + what + '</strong></td><td>' + why + '</td></tr>', t: lab + ': ' + what + '. ' + why.replace(/<[^>]+>/g, ''), st: st}; }
  function run(){
    var hs = parse($('ehIn').value);
    ['ehSum', 'ehChk', 'ehPath', 'ehAll'].forEach(function(id){ $(id).innerHTML = ''; });
    ['ehSpf', 'ehDkim', 'ehDmarc'].forEach(function(id){ $(id).textContent = 'none'; });
    $('ehHops').textContent = '0'; $('ehTime').textContent = '0';
    report = '';
    if (!hs.length){ say('ehNote', '', 'Paste the full headers of an email. In Gmail, open the message, click More next to Reply, then Show original, and copy everything.'); return; }
    var from = get(hs, 'from'), fromA = addr(from), fromD = dom(fromA), rp = get(hs, 'return-path'), rpD = dom(addr(rp)), rt = get(hs, 'reply-to');
    var ar = all(hs, 'authentication-results').map(authres), top = ar[0] || {id: '', m: []};
    function meth(k){ for (var i = 0; i < top.m.length; i++) if (top.m[i].k === k) return top.m[i]; return null; }
    var spf = meth('spf'), dmarc = meth('dmarc'), dk = top.m.filter(function(m){ return m.k === 'dkim'; });
    var rspf = get(hs, 'received-spf');
    if (!spf && rspf){ var rm = /^\s*([a-z]+)/i.exec(rspf), mf = /envelope-from=("?)([^\s";]+)\1/i.exec(rspf); spf = {k: 'spf', r: rm ? rm[1].toLowerCase() : 'none', p: {'smtp.mailfrom': mf ? mf[2] : rp}}; }
    var dkPass = dk.filter(function(m){ return m.r === 'pass'; });
    var dkimR = dk.length ? (dkPass.length ? 'pass' : dk[0].r) : 'none';
    var sigs = all(hs, 'dkim-signature').map(tags);
    $('ehSpf').textContent = spf ? spf.r : 'none'; $('ehDkim').textContent = dkimR; $('ehDmarc').textContent = dmarc ? dmarc.r : 'none';
    var recv = all(hs, 'received').map(hop).reverse(), prev = pdate(get(hs, 'date')), first = prev, last = null, maxd = 0, maxi = -1, rows = [];
    recv.forEach(function(h, i){
      var d = (h.t !== null && prev !== null) ? h.t - prev : null;
      if (d !== null && d > maxd){ maxd = d; maxi = i; }
      if (h.t !== null){ prev = h.t; last = h.t; }
      h.d = d;
    });
    recv.forEach(function(h, i){
      rows.push('<tr' + (i === maxi && maxd >= 60000 ? ' style="background:#fff8c5"' : '') + '><td>' + (i + 1) + '</td><td class="mono" style="word-break:break-all">' + esc(h.from || 'not given') + (h.ip ? '<br><small>' + esc(h.ip) + '</small>' : '') + '</td><td class="mono" style="word-break:break-all">' + esc(h.by || 'not given') + '</td><td>' + esc(h.wth || '') + (h.tls ? ' (TLS)' : '') + '</td><td>' + (h.t !== null ? esc(new Date(h.t).toISOString().replace('T', ' ').slice(0, 19)) + ' UTC' : 'no time') + '</td><td>' + (h.d === null ? '' : esc(dur(h.d))) + '</td></tr>');
    });
    $('ehPath').innerHTML = recv.length ? '<thead><tr><th>#</th><th>From</th><th>By</th><th>Protocol</th><th>Time</th><th>Delay</th></tr></thead><tbody>' + rows.join('') + '</tbody>' : '<tbody><tr><td>No Received lines found. Paste the full headers, not only From and Subject.</td></tr></tbody>';
    var total = (first !== null && last !== null) ? last - first : null;
    $('ehHops').textContent = recv.length; $('ehTime').textContent = total === null ? 'unknown' : dur(total);
    var ip = '';
    var cm = /client-ip=([0-9a-f:.]+)/i.exec(rspf); if (cm) ip = cm[1];
    if (!ip && spf && spf.p['smtp.remote-ip']) ip = spf.p['smtp.remote-ip'];
    if (!ip) for (var i = recv.length - 1; i >= 0; i--) if (recv[i].ip && !priv(recv[i].ip)){ ip = recv[i].ip; break; }
    var S1 = [['From', from], ['Reply-To', rt], ['Return-Path', rp], ['To', get(hs, 'to')], ['Subject', get(hs, 'subject')], ['Date', get(hs, 'date')], ['Message-ID', get(hs, 'message-id')], ['Sending IP', ip], ['Checked by', top.id], ['Mailer', get(hs, 'x-mailer') || get(hs, 'user-agent')]];
    $('ehSum').innerHTML = '<tbody>' + S1.filter(function(r){ return r[1]; }).map(function(r){ return '<tr><th style="white-space:nowrap">' + esc(r[0]) + '</th><td style="word-break:break-word">' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody>';
    var C = [];
    if (!ar.length) C.push(row('warn', 'No authentication results', 'There is no ' + c('Authentication-Results') + ' line, so the receiving server did not record SPF, DKIM or DMARC. Copy the headers from the inbox that received the email, not from a draft or the sent folder.'));
    if (spf){
      var sd = dom(spf.p['smtp.mailfrom'] || rp);
      if (spf.r === 'pass') C.push(row('ok', 'SPF ' + MEAN.pass, 'The sending server is allowed to send for ' + c(sd || 'the bounce domain') + '.'));
      else C.push(row(spf.r === 'softfail' || spf.r === 'neutral' || spf.r === 'none' ? 'warn' : 'bad', 'SPF ' + (MEAN[spf.r] || spf.r), (spf.r === 'none' ? 'The domain ' + c(sd) + ' has no SPF record.' : 'The server at ' + c(ip || 'this IP') + ' is not listed in the SPF record of ' + c(sd || 'the bounce domain') + '.') + ' Add the email service to your SPF record.'));
      if (sd && fromD) C.push(org(sd) === org(fromD) ? row('ok', 'SPF aligned', 'The bounce domain ' + c(sd) + ' matches the From domain ' + c(fromD) + '.') : row('warn', 'SPF not aligned', 'The bounce domain ' + c(sd) + ' is different from the From domain ' + c(fromD) + ', so SPF cannot help DMARC pass. That is fine when DKIM is aligned. Otherwise set a custom bounce domain in your email service.'));
    } else if (ar.length) C.push(row('warn', 'SPF not checked', 'The receiver did not record an SPF result.'));
    var dkD = dkPass.map(function(m){ return dom(m.p['header.d'] || m.p['header.i'] || ''); }).filter(Boolean);
    if (!dkD.length && !dk.length) sigs.forEach(function(t){ if (t.d) dkD.push(t.d.toLowerCase()); });
    if (dk.length){
      if (dkPass.length) C.push(row('ok', 'DKIM ' + MEAN.pass, 'Signed by ' + dkD.map(c).join(', ') + ' and not changed on the way.'));
      else if (dkimR === 'none') C.push(row('bad', 'No DKIM signature', 'The receiver found no DKIM signature. Gmail and Yahoo expect bulk mail to be signed with DKIM for your own domain.'));
      else C.push(row('bad', 'DKIM ' + (MEAN[dkimR] || dkimR), 'The signature did not verify. The message may have been changed after signing, or the DKIM public key in DNS does not match.'));
      if (dkPass.length && fromD) C.push(dkD.some(function(d){ return org(d) === org(fromD); }) ? row('ok', 'DKIM aligned', 'A passing signature belongs to the From domain ' + c(fromD) + '.') : row('warn', 'DKIM not aligned', 'The signature is from ' + dkD.map(c).join(', ') + ', not from ' + c(fromD) + '. Set up DKIM for your own domain in your email service.'));
    } else if (sigs.length) C.push(row('warn', 'DKIM signature not verified here', 'A ' + c('DKIM-Signature') + ' is present for ' + sigs.map(function(t){ return c(t.d || '?'); }).join(', ') + ', but there is no receiver result to show whether it passed.'));
    else C.push(row('bad', 'No DKIM signature', 'The email is not signed. Gmail and Yahoo expect bulk mail to be signed with DKIM.'));
    if (dmarc){
      var pol = /p=([a-z]+)/i.exec(v_dm || '');
      if (dmarc.r === 'pass') C.push(row('ok', 'DMARC ' + MEAN.pass, 'The From domain ' + c(dmarc.p['header.from'] || fromD) + ' passed with an aligned SPF or DKIM result.' + (pol ? ' Its policy is ' + c('p=' + pol[1].toLowerCase()) + '.' : '')));
      else if (dmarc.r === 'none') C.push(row('warn', 'DMARC not set up', 'The domain ' + c(dmarc.p['header.from'] || fromD) + ' has no DMARC record. Gmail requires one for bulk senders.'));
      else C.push(row('bad', 'DMARC ' + (MEAN[dmarc.r] || dmarc.r), 'Neither SPF nor DKIM passed for a domain aligned with ' + c(dmarc.p['header.from'] || fromD) + '. This is the most common reason mail goes to spam or is rejected.'));
    } else if (ar.length) C.push(row('warn', 'DMARC not checked', 'The receiver did not record a DMARC result.'));
    var arc = meth('arc'); if (arc) C.push(row(arc.r === 'pass' || arc.r === 'none' ? 'ok' : 'warn', 'ARC ' + (MEAN[arc.r] || arc.r), 'ARC keeps results from earlier servers when an email is forwarded or sent through a mailing list.'));
    var dn = /^\s*"?([^"<]*)"?\s*</.exec(from), dnm = dn && /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i.exec(dn[1]);
    if (dnm && dnm[0].toLowerCase() !== fromA.toLowerCase()) C.push(row('bad', 'Display name shows another address', 'The name shows ' + c(dnm[0]) + ' but the real sender is ' + c(fromA) + '. This is a classic phishing trick.'));
    if (rt && fromD){ var rtD = dom(addr(rt)); if (rtD && org(rtD) !== org(fromD)) C.push(row('warn', 'Reply goes to another domain', 'Replies go to ' + c(rtD) + ', not ' + c(fromD) + '. Normal for some help desks, but a common sign of phishing and invoice fraud.')); else if (rtD) C.push(row('ok', 'Reply address matches', 'Replies go to the same domain as the sender.')); }
    var lu = get(hs, 'list-unsubscribe'), lup = get(hs, 'list-unsubscribe-post');
    if (lu && /List-Unsubscribe=One-Click/i.test(lup) && /<https:/i.test(lu)) C.push(row('ok', 'One click unsubscribe', 'Both ' + c('List-Unsubscribe') + ' with an https link and ' + c('List-Unsubscribe-Post') + ' are present, as Gmail requires for bulk marketing mail.'));
    else if (lu) C.push(row('warn', 'Unsubscribe is not one click', 'There is a ' + c('List-Unsubscribe') + ' header, but ' + (/<https:/i.test(lu) ? 'no ' + c('List-Unsubscribe-Post: List-Unsubscribe=One-Click') : 'no https link') + '. Gmail needs one click unsubscribe for marketing mail above 5,000 messages a day.'));
    else C.push(row('warn', 'No unsubscribe header', 'Fine for personal or transactional email. Newsletters and offers should include ' + c('List-Unsubscribe') + ' and ' + c('List-Unsubscribe-Post') + '.'));
    var ext = recv.filter(function(h){ return h.ip && !priv(h.ip); });
    if (ext.length) C.push(ext.every(function(h){ return h.tls; }) ? row('ok', 'Encrypted with TLS', 'Every hop between public servers used TLS.') : row('warn', 'Not encrypted on every hop', 'At least one hop between public servers did not show TLS. Google asks all senders to use TLS.'));
    if (maxd >= 300000) C.push(row('warn', 'Slow hop', 'Hop ' + (maxi + 1) + ' took ' + dur(maxd) + '. The delay happened at ' + c(recv[maxi].by || 'that server') + '. Queues, greylisting or spam scanning usually cause this.'));
    if (recv.some(function(h){ return h.d !== null && h.d < -60000; })) C.push(row('warn', 'Clock difference', 'One server reports a time before the previous hop. Its clock is wrong, so delays here are approximate.'));
    if (!get(hs, 'message-id')) C.push(row('warn', 'No Message-ID', 'Every email should carry a ' + c('Message-ID') + '. Missing ones look like spam to filters.'));
    $('ehChk').innerHTML = '<thead><tr><th>Status</th><th>Check</th><th>What it means</th></tr></thead><tbody>' + C.map(function(x){ return x.h; }).join('') + '</tbody>';
    var bad = C.filter(function(x){ return x.st === 'bad'; }).length, warn = C.filter(function(x){ return x.st === 'warn'; }).length;
    var head = !ar.length ? 'No authentication results found.' : bad ? bad + ' problem' + (bad === 1 ? '' : 's') + ' found.' : (dmarc && dmarc.r === 'pass') ? 'This email is properly authenticated.' : 'No hard failures, but authentication is incomplete.';
    say('ehNote', bad ? 'bad' : (warn ? 'warn' : 'ok'), '<strong>' + head + '</strong> ' + (warn ? warn + ' item' + (warn === 1 ? '' : 's') + ' to check. ' : '') + 'The email passed through ' + recv.length + ' server' + (recv.length === 1 ? '' : 's') + (total !== null ? ' in ' + dur(total) : '') + '.');
    $('ehAll').setAttribute('data-n', hs.length);
    showAll(hs);
    report = 'Email header report\n' + S1.filter(function(r){ return r[1]; }).map(function(r){ return r[0] + ': ' + r[1]; }).join('\n') + '\n\nSPF: ' + (spf ? spf.r : 'none') + ', DKIM: ' + dkimR + ', DMARC: ' + (dmarc ? dmarc.r : 'none') + '\n\n' + C.map(function(x){ return x.t; }).join('\n') + '\n\nPath:\n' + recv.map(function(h, i){ return (i + 1) + '. ' + (h.from || '?') + (h.ip ? ' [' + h.ip + ']' : '') + ' > ' + (h.by || '?') + (h.d !== null ? ' (' + dur(h.d) + ')' : ''); }).join('\n');
  }
  var v_dm = '';
  var last = [];
  function showAll(hs){
    if (hs) last = hs;
    var q = $('ehFind').value.trim().toLowerCase();
    var f = last.filter(function(h){ return !q || h.k.indexOf(q) > -1 || h.v.toLowerCase().indexOf(q) > -1; });
    $('ehAll').innerHTML = '<thead><tr><th>Header</th><th>Value</th></tr></thead><tbody>' + (f.length ? f.map(function(h){ return '<tr><td class="mono" style="white-space:nowrap;vertical-align:top">' + esc(h.n) + '</td><td class="mono" style="word-break:break-all">' + esc(h.v) + '</td></tr>'; }).join('') : '<tr><td colspan="2">No header matches that filter.</td></tr>') + '</tbody>';
  }
  function go(){ var m = /dmarc=[a-z]+\s*\(([^)]*)\)/i.exec(($('ehIn').value || '').replace(/\s+/g, ' ')); v_dm = m ? m[1] : ''; run(); }
  var tm; $('ehIn').addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(go, 250); });
  $('ehRun').addEventListener('click', go);
  $('ehClear').addEventListener('click', function(){ $('ehIn').value = ''; go(); $('ehIn').focus(); });
  $('ehFind').addEventListener('input', function(){ showAll(); });
  $('ehCopy').addEventListener('click', function(){ go(); copyText(report || 'Paste email headers first.', 'toast'); });
  go();
''',
        content=f'''
    <h2>What Is an Email Header Analyzer?</h2>
    <p>Every email carries a hidden block of headers above the message. They record who sent it, every server it passed through, the time at each step, and whether the receiving mailbox trusted it. Reading them by hand is slow, because the lines are long, out of order and full of codes.</p>
    <p>This email header analyzer turns that block into a clear report. You see the SPF, DKIM and DMARC results, whether they line up with the From address, the full delivery path with the delay at each hop, and warning signs such as a reply address on another domain. Use it when your own campaign lands in spam, when a customer says your email never arrived, or when a message looks like phishing.</p>
    <p>Many header tools send what you paste to their server. Headers contain names, addresses and internal server details, so this one reads them only in your browser.</p>

    <h2>How to Analyze Email Headers</h2>
    <ol>
      <li><strong>Copy the full headers.</strong> Use the steps in the table below. Copy everything, not only the From and Subject lines.</li>
      <li><strong>Paste them in the box.</strong> The report updates as you paste. The sample shows a well set up marketing email.</li>
      <li><strong>Read the verdict and checks.</strong> Problems are shown first in plain words, with what to fix.</li>
      <li><strong>Look at the delivery path.</strong> The slowest hop is highlighted, so you know which server held the email.</li>
      <li><strong>Copy the report</strong> to share it with your developer or email service support team.</li>
    </ol>

    <h2>How to Find Email Headers</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Email app', 'Steps')}
      <tbody>
        <tr><td>Gmail</td><td>Open the email, click More next to Reply, then Show original. Click Copy to clipboard.</td></tr>
        <tr><td>Outlook</td><td>Open the email, click File, then Properties. Copy the Internet headers box.</td></tr>
        <tr><td>Apple Mail</td><td>Open the email, then View, Message, All Headers.</td></tr>
        <tr><td>Yahoo Mail</td><td>Open the email, click More, then View Raw Message.</td></tr>
      </tbody>
    </table></div>
    <p>These steps come from Google's guide to <a href="https://support.google.com/mail/answer/29436" {EXT}>tracing an email with its full header</a>.</p>

    <h2>What the Results Mean</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Check', 'What it tells you')}
      <tbody>
        <tr><td>SPF</td><td>Whether the sending server is listed in the SPF record of the bounce domain in <code>Return-Path</code>.</td></tr>
        <tr><td>DKIM</td><td>Whether the message carries a valid signature, and which domain signed it with the <code>d=</code> tag.</td></tr>
        <tr><td>DMARC</td><td>Whether SPF or DKIM passed for a domain that matches the visible From address. This is the result Gmail and Yahoo care about most.</td></tr>
        <tr><td>Alignment</td><td>Whether the SPF or DKIM domain shares the same main domain as From, such as <code>mail.yourshop.in</code> and <code>yourshop.in</code>.</td></tr>
        <tr><td>Delivery path</td><td>Each <code>Received</code> line, read from the bottom up, oldest first. Each server adds its line at the top.</td></tr>
        <tr><td>One click unsubscribe</td><td>Whether <code>List-Unsubscribe</code> and <code>List-Unsubscribe-Post</code> are present for marketing mail.</td></tr>
      </tbody>
    </table></div>
    <p>The <a href="https://support.google.com/mail/answer/81126" {EXT}>Google email sender guidelines</a> ask every sender to use TLS, and senders of more than 5,000 messages a day to Gmail to pass DMARC with an aligned From domain and to support one click unsubscribe.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Test your own campaigns.</strong> Send one to a Gmail and an Outlook address you own, then paste both headers here before you send to the full list.</li>
      <li><strong>Read the top result.</strong> Forwarded mail can carry several authentication results. The top one was added by the final inbox, so that is the one the analyzer uses.</li>
      <li><strong>DMARC fail with SPF pass?</strong> Your email service is using its own bounce domain. Set up DKIM for your domain in the service so DMARC can pass.</li>
      <li><strong>Long delay at one hop?</strong> Look at the server named in the By column. Delays inside your own systems point to a queue; delays at the receiver often mean greylisting or spam scanning.</li>
      <li><strong>Suspicious email?</strong> A DMARC fail, a reply address on another domain, or a display name showing a different address are all reasons not to click anything.</li>
    </ul>

    <h2>Fix What the Headers Show</h2>
    <p>Most problems trace back to DNS. Build a correct record with the <a href="{T}spf-record-generator/">SPF record generator and checker</a> and the <a href="{T}dmarc-record-generator/">DMARC record generator</a>. Then plan better campaigns with our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, and if your site sends mail itself, see <a href="{B}send-email-code-in-php/">send email code in PHP</a> and <a href="{B}php-contact-form-spam-protection/">contact form spam protection</a>.</p>
''',
        faqs=[
            ("Is it safe to paste email headers here?", "Yes. The analyzer runs entirely in your browser with JavaScript. Headers are never uploaded or stored, which matters because they contain names, email addresses and internal server details."),
            ("Why does my email pass SPF but fail DMARC?", "DMARC needs SPF or DKIM to pass for a domain that matches your From address. Email services often send with their own bounce domain, so SPF passes for their domain, not yours. Set up DKIM for your own domain in the service, or a custom bounce domain, and DMARC will pass."),
            ("Which Received line is the first hop?", "The bottom one. Every server adds its Received line to the top of the headers, so the oldest hop is at the bottom and the final inbox is at the top. The analyzer reverses them and shows the oldest hop first, with the delay between each step."),
            ("Can headers prove who really sent an email?", "They show which servers handled it and whether the sending domain authenticated it. A DMARC pass means the From domain approved the message. Lines added before the first trusted server can be faked, so trust the results added by your own inbox, at the top."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("Send Email Code in PHP", "send-email-code-in-php"),
                 ("PHP Contact Form Spam Protection", "php-contact-form-spam-protection"), ("How Hosting Affects SEO", "how-hosting-affects-seo")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'email-marketing-tools'; t['updated'] = '2026-11-13'
