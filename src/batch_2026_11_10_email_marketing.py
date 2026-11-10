"""Batch 13 (2026-11-10): Email Marketing Tools category, first 2 tools.
Facts checked 2026-11-10 against: Google Email sender guidelines (support.google.com/mail/answer/81126: subject lines must
not be misleading, no Re: or Fwd: unless a real reply or forward, no emoji used to imitate graphics; all senders need SPF
or DKIM, senders of 5,000+ messages a day need SPF, DKIM and DMARC with the From domain aligned with SPF or DKIM),
Google sender guidelines FAQ (support.google.com/a/answer/14229414: minimum DMARC policy p=none, spam rate under 0.1%,
never 0.3%, one click unsubscribe via List-Unsubscribe headers for marketing mail), RFC 9989 DMARCbis (May 2026, replaces
RFC 7489: pct, rf and ri removed; np, t and psd added; t=y asks receivers to apply the next lower policy; receivers ignore
unknown tags), RFC 9990 aggregate reports and RFC 9991 failure reports (external report address check via
<domain>._report._dmarc.<report domain> TXT "v=DMARC1", unchanged from RFC 7489 section 7.1), RFC 7489 defaults kept
(adkim=r, aspf=r, fo=0, sp falls back to p). Subject line display lengths are industry approximations (phones about 30 to
40 characters, desktop about 60 to 70), so the tool labels them as approximate."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/email-marketing-tools/'
TS = 'https://brandella.in/tools/technical-seo-tools/'
AN = 'https://brandella.in/tools/analytics-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. EMAIL SUBJECT LINE TESTER ----------
    SL_LIST = ('Your Diwali tea box is almost gone\n'
               'FREE!!! Act now and WIN a gift box\n'
               'Re: your order\n'
               '{{first_name}}, 3 new chai blends to try this week ☕\n'
               'Monthly newsletter November edition from Brandella Tea Company with all our latest news\n'
               'Last chance: 20% off ends tonight')
    TOOLS.append(dict(
        slug='email-subject-line-tester', short='SL', name='Email Subject Line Tester',
        card='Score your email subject line and preheader for length, spam words, caps, emoji and mobile cut off, then compare several lines side by side.',
        title='Email Subject Line Tester: Free Score and Spam Check',
        desc='Free email subject line tester. Check length, spam trigger words, caps, emoji and preheader, see how it looks on a phone, and compare up to 20 lines.',
        h1='Email Subject Line Tester',
        lead='Type a subject line and preheader to get an instant score with clear fixes. See where phones cut it off, catch spam trigger words and shouting caps, and paste a list of ideas to pick the strongest one before you send.',
        tool='''<section class="tool" aria-label="Email subject line tester">
    <div class="card" style="min-width:0">
      <h2>Your Email</h2>
      ''' + F('slFrom', 'Sender name', 'Brandella Tea') + '''
      ''' + F('slSub', 'Subject line', '{{first_name}}, your Diwali tea box is almost gone 🎁', em='merge tags such as {{first_name}} are fine') + '''
      ''' + F('slPre', 'Preheader <em>the preview text after the subject</em>', 'Only 40 boxes left. Free delivery across India until Sunday.', tag='textarea', extra=' style="min-height:80px"') + '''
      <div class="stats">''' + S('slScore', 'Score out of 100') + S('slChars', 'Characters') + S('slWords', 'Words') + S('slEmoji', 'Emoji') + '''</div>
      <div class="kw-result" id="slVerdict"></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Inbox Preview</h2>
      <p style="font-size:13px;color:#666;margin:0 0 8px">Phone, approximate cut off</p>
      <div style="border:1px solid #ddd;border-radius:14px;padding:12px 14px;background:#fff;max-width:360px;margin-bottom:16px">
        <div style="display:flex;justify-content:space-between;gap:8px"><strong id="slPmFrom" style="font-size:15px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis"></strong><span style="font-size:12px;color:#888">10:42</span></div>
        <div id="slPmSub" style="font-size:14.5px;font-weight:600;color:#111;overflow-wrap:anywhere"></div>
        <div id="slPmPre" style="font-size:13.5px;color:#666;overflow-wrap:anywhere"></div>
      </div>
      <p style="font-size:13px;color:#666;margin:0 0 8px">Desktop inbox row, approximate cut off</p>
      <div style="border:1px solid #ddd;border-radius:8px;padding:9px 12px;background:#fff;font-size:14px;overflow-wrap:anywhere;margin-bottom:12px"><strong id="slDkFrom"></strong> <span style="color:#bbb">|</span> <strong id="slDkSub"></strong> <span id="slDkPre" style="color:#666"></span></div>
      <p style="font-size:13px;color:#666;margin:0">Each app and screen size cuts text at a slightly different point, so treat these as a guide. Put the words that matter in the first 30 or so characters.</p>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Checks</h2>
      <div style="overflow-x:auto"><table class="rtable" id="slChecks"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="slCopy">Copy Subject Line</button><button class="btn" id="slCopyRep">Copy Report</button></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Compare Subject Lines</h2>
      ''' + F('slList', 'One subject line per line, up to 20', SL_LIST, tag='textarea', extra=' style="min-height:150px"') + '''
      <div class="kw-result" id="slLCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="slLOut"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="slLCopy">Copy Ranking as CSV</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var STRONG = ['100% free','act now','apply now','buy now','call now','click here','click below','congratulations','dear friend','double your','earn money','make money','extra income','cash bonus','free money','free gift','final notice','guaranteed','100% guaranteed','risk free','no cost','no obligation','once in a lifetime','miracle','winner','you won','you have been selected','you are a winner','this is not spam','not spam','urgent','order now','lowest price','best price','cheap','credit card','loan','increase sales','limited time offer','special promotion','exclusive deal','prize','claim now','claim your','instant access','100% off','no catch','offer expires','what are you waiting for'];
  var SOFT = ['free','sale','discount','deal','offer','save','% off','limited time','last chance','hurry','ends tonight','expires','bonus','gift','win','exclusive','only'];
  var ACR = {AI:1,SEO:1,GST:1,ROI:1,USA:1,UK:1,PDF:1,FAQ:1,CEO:1,B2B:1,B2C:1,GA4:1,API:1,UPI:1,EMI:1,IPL:1,PPC:1,CRM:1,NEW:0,SMS:1,OTP:1,PIN:1,ID:1,FYI:1,ASAP:1,HR:1,IT:1,IST:1,TV:1,DIY:1,NFT:1,KYC:1,GPT:1,LLM:1};
  function graphemes(s){ try { if (window.Intl && Intl.Segmenter) return Array.from(new Intl.Segmenter('en', {granularity: 'grapheme'}).segment(s), function(x){ return x.segment; }); } catch (e){} return Array.from(s); }
  var EMO = /\p{Extended_Pictographic}/u;
  function rxw(p){ return new RegExp('(^|[^a-z0-9])' + p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?=$|[^a-z0-9])', 'i'); }
  var RX_S = STRONG.map(function(p){ return [p, rxw(p)]; }), RX_W = SOFT.map(function(p){ return [p, /^%/.test(p) ? /\d\s?% off/i : rxw(p)]; });
  function analyse(sub, pre){
    var s = sub, g = graphemes(s.trim()), n = g.length, emo = g.filter(function(x){ return EMO.test(x); }).length;
    var clean = s.replace(/\{\{[^}]*\}\}|\*\|[^|]*\|\*|%%[^%]*%%|\[[A-Za-z_ ]+\]/g, ' name ');
    var words = (clean.match(/[\p{L}\p{N}][\p{L}\p{N}'’%]*/gu) || []).length, pts = 100, C = [];
    function add(st, name, note, minus){ C.push([st, name, note]); pts -= (minus || 0); }
    if (!s.trim()) return {score: 0, n: 0, words: 0, emo: 0, checks: [['bad', 'Subject line', 'Type a subject line to test it.']]};
    if (n < 15) add('warn', 'Length', n + ' characters is very short. Add a detail that tells readers what is inside.', 15);
    else if (n < 28) add('warn', 'Length', n + ' characters. Short works, but check it says enough to earn the open.', 5);
    else if (n <= 50) add('ok', 'Length', n + ' characters, a strong length that fits most phone inboxes.');
    else if (n <= 60) add('warn', 'Length', n + ' characters. Phones will likely cut the end, so lead with the key words.', 5);
    else if (n <= 78) add('warn', 'Length', n + ' characters is long. Phones show about 30 to 40, desktops about 60 to 70.', 12);
    else add('bad', 'Length', n + ' characters is too long. Most inboxes will hide half of it. Aim for under 50.', 20);
    if (words < 3) add('warn', 'Words', words + ' word' + (words === 1 ? '' : 's') + '. One or two words rarely explain why to open.', 5);
    else if (words > 12) add('warn', 'Words', words + ' words. Cut filler words such as "our", "latest" or "edition".', 8);
    else add('ok', 'Words', words + ' words, easy to scan.');
    var letters = clean.replace(/name/g, '').replace(/[^A-Za-z]/g, '');
    var caps = (clean.match(/\b[A-Z][A-Z0-9]{2,}\b/g) || []).filter(function(w){ return !ACR[w]; });
    if (letters.length > 6 && letters === letters.toUpperCase()) add('bad', 'Capital letters', 'The whole line is in capitals, which reads as shouting and is a classic spam signal.', 25);
    else if (caps.length) add('warn', 'Capital letters', 'Shouting words: ' + caps.map(c).join(', ') + '. Use normal case and let the words do the work.', Math.min(20, caps.length * 8));
    else add('ok', 'Capital letters', 'No shouting words in capitals.');
    var ex = (s.match(/!/g) || []).length, multi = /[!?]{2,}|\${2,}|₹{2,}/.test(s);
    if (multi) add('bad', 'Punctuation', 'Repeated marks such as ' + c((s.match(/[!?]{2,}|\${2,}|₹{2,}/) || [''])[0]) + ' look like spam. Use one at most.', 15);
    else if (ex > 1) add('warn', 'Punctuation', ex + ' exclamation marks. Keep it to one, or none.', 8);
    else add('ok', 'Punctuation', ex ? 'One exclamation mark, which is fine.' : 'Calm punctuation, no exclamation marks.');
    var hs = RX_S.filter(function(r){ return r[1].test(s); }).map(function(r){ return r[0]; });
    var hw = RX_W.filter(function(r){ return r[1].test(s) && !hs.some(function(h){ return h.indexOf(r[0].replace('% ', '')) > -1; }); }).map(function(r){ return r[0]; });
    if (hs.length) add('bad', 'Spam trigger words', 'Strong triggers: ' + hs.map(c).join(', ') + '. These are common in spam and can hurt inbox placement when stacked.', Math.min(24, hs.length * 8));
    if (hw.length) add(hw.length > 2 ? 'warn' : 'ok', 'Promotional words', hw.map(c).join(', ') + (hw.length > 2 ? '. That is a lot for one line. Keep one clear offer.' : '. Fine in moderation for a sale email.'), hw.length > 2 ? 6 : 0);
    if (!hs.length && !hw.length) add('ok', 'Spam trigger words', 'No common spam trigger words found.');
    if (/^\s*(re|fwd?|fw)\s*:/i.test(s)) add('bad', 'Fake reply', 'Starting with ' + c(s.trim().split(':')[0] + ':') + ' when it is not a real reply or forward breaks Google sender guidelines and annoys readers.', 25);
    if (emo > 3) add('warn', 'Emoji', emo + ' emoji. One or two is plenty, and some older inboxes show them as boxes.', 8);
    else if (emo) add('ok', 'Emoji', emo + ' emoji. ' + (EMO.test(g[0]) ? 'It sits at the start, so the first word readers see is a picture. ' : '') + 'Check it still makes sense if the emoji does not show.');
    var tags = s.match(/\{\{[^}]*\}\}|\*\|[^|]*\|\*|%%[^%]*%%/g) || [], broken = /\{\{(?![^}]*\}\})|\*\|(?![^|]*\|\*)|(^|[^{])\{[a-z_ ]+\}(?!\})/i.test(s);
    if (broken) add('bad', 'Merge tag', 'A merge tag looks broken or half typed. Readers would see the raw code. Check the braces or pipes.', 12);
    else if (tags.length) add('ok', 'Personal touch', 'Uses ' + tags.map(c).join(', ') + '. Set a fallback, such as "there", for contacts with no name.');
    if (/\d/.test(s)) C.push(['info', 'Numbers', 'Has a number, which sets a clear expectation.']);
    if (/\?\s*\S{0,3}$/.test(s.trim())) C.push(['info', 'Question', 'Ends with a question, which can spark curiosity.']);
    if (/\s{2,}/.test(s) || s !== s.trim()) add('warn', 'Spacing', 'Has double or extra spaces at the start or end. Tidy it up.', 3);
    var p = (pre || '').trim(), pg = graphemes(p).length;
    if (!p) add('bad', 'Preheader', 'Empty. The inbox will show the first text in your email instead, often "View in browser".', 10);
    else if (/^(view (this|in|it in|online)|having trouble|can'?t see|click here to view|is this email not displaying)/i.test(p)) add('bad', 'Preheader', 'Starts with "' + esc(p.slice(0, 30)) + '". Replace it with a line that adds to the subject.', 10);
    else if (p.toLowerCase() === s.trim().toLowerCase()) add('warn', 'Preheader', 'Repeats the subject. Use it to add a second reason to open.', 8);
    else if (pg < 30) add('warn', 'Preheader', pg + ' characters. Short preheaders can let other email text spill in. Aim for 40 to 110.', 3);
    else if (pg > 140) add('warn', 'Preheader', pg + ' characters. Only the first part will show, so lead with the best bit.', 2);
    else add('ok', 'Preheader', pg + ' characters, a good length that adds to the subject.');
    return {score: Math.max(0, Math.min(100, pts)), n: n, words: words, emo: emo, checks: C, hs: hs.length, hw: hw.length};
  }
  function grade(x){ return x >= 80 ? ['ok', 'Strong'] : x >= 60 ? ['ok', 'Good'] : x >= 40 ? ['warn', 'Needs work'] : ['bad', 'Weak']; }
  function cut(s, n){ var g = graphemes(s); return g.length > n ? g.slice(0, n).join('').replace(/\s+$/, '') + '...' : s; }
  var ICON = {ok: '<span style="color:#2e7d32;font-weight:700">Good</span>', warn: '<span style="color:#b26a00;font-weight:700">Improve</span>', bad: '<span style="color:#c62828;font-weight:700">Fix</span>', info: '<span style="color:#555;font-weight:700">Note</span>'};
  var last;
  function demo(s){ return s.replace(/\{\{\s*first_?name[^}]*\}\}|\*\|FNAME\|\*|%%first_?name%%/gi, 'Priya'); }
  function run(){
    var s = $('slSub').value, p = $('slPre').value, f = $('slFrom').value.trim() || 'Your Brand', r = analyse(s, p), gr = grade(r.score);
    last = r;
    $('slScore').textContent = r.score; $('slChars').textContent = r.n; $('slWords').textContent = r.words; $('slEmoji').textContent = r.emo;
    var fixes = r.checks.filter(function(x){ return x[0] === 'bad' || x[0] === 'warn'; }).length;
    say('slVerdict', gr[0], s.trim() ? '<strong>' + gr[1] + ' subject line (' + r.score + ' of 100).</strong> ' + (fixes ? fixes + ' thing' + (fixes === 1 ? '' : 's') + ' to improve below.' : 'Nothing to fix. Test it against one more idea with a real audience split.') : 'Type a subject line to see its score.');
    $('slChecks').innerHTML = '<thead><tr><th style="width:90px">Result</th><th style="width:170px">Check</th><th>What it means</th></tr></thead><tbody>' + r.checks.map(function(x){ return '<tr><td>' + ICON[x[0]] + '</td><td><strong>' + esc(x[1]) + '</strong></td><td>' + x[2] + '</td></tr>'; }).join('') + '</tbody>';
    var ds = demo(s.trim()), dp = demo(p.trim());
    $('slPmFrom').textContent = f; $('slPmSub').textContent = cut(ds, 38) || '(no subject)'; $('slPmPre').textContent = cut(dp, 85);
    $('slDkFrom').textContent = cut(f, 20); var room = 95 - Math.min(graphemes(ds).length, 95);
    $('slDkSub').textContent = cut(ds, 95) || '(no subject)'; $('slDkPre').textContent = room > 8 && dp ? cut(dp, room) : '';
  }
  var rank = [];
  function runL(){
    var L = $('slList').value.split(/\r?\n/).map(function(x){ return x.trim(); }).filter(Boolean).slice(0, 20);
    rank = L.map(function(x){ var r = analyse(x, 'A preheader that adds detail to this subject line.'); return {s: x, r: r}; }).sort(function(a, b){ return b.r.score - a.r.score; });
    if (!rank.length){ $('slLOut').innerHTML = ''; say('slLCheck', '', 'Paste two or more subject line ideas, one per line.'); return; }
    $('slLOut').innerHTML = '<thead><tr><th class="num">#</th><th>Subject line</th><th class="num">Score</th><th class="num">Chars</th><th>Top issue</th></tr></thead><tbody>' + rank.map(function(o, i){
      var top = o.r.checks.filter(function(x){ return x[0] === 'bad'; })[0] || o.r.checks.filter(function(x){ return x[0] === 'warn'; })[0];
      return '<tr' + (i === 0 ? ' class="hit"' : '') + '><td class="num">' + (i + 1) + '</td><td style="overflow-wrap:anywhere">' + esc(o.s) + '</td><td class="num">' + o.r.score + '</td><td class="num">' + o.r.n + '</td><td>' + (top ? esc(top[1]) : 'None') + '</td></tr>';
    }).join('') + '</tbody>';
    say('slLCheck', 'ok', '<strong>Best scoring: "' + esc(rank[0].s) + '"</strong> (' + rank[0].r.score + ' of 100). The score checks craft, not appeal, so A/B test your top two with real subscribers.');
  }
  function csvq(v){ v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  var t1; ['slSub', 'slPre', 'slFrom'].forEach(function(id){ $(id).addEventListener('input', function(){ clearTimeout(t1); t1 = setTimeout(run, 60); }); });
  var t2; $('slList').addEventListener('input', function(){ clearTimeout(t2); t2 = setTimeout(runL, 120); });
  $('slCopy').addEventListener('click', function(){ if ($('slSub').value.trim()) copyText($('slSub').value.trim(), 'toast'); });
  $('slCopyRep').addEventListener('click', function(){ run(); copyText('Subject: ' + $('slSub').value.trim() + '\nPreheader: ' + $('slPre').value.trim() + '\nScore: ' + last.score + '/100\n' + last.checks.map(function(x){ return '[' + x[0].toUpperCase() + '] ' + x[1] + ': ' + x[2].replace(/<[^>]+>/g, ''); }).join('\n'), 'toast'); });
  $('slLCopy').addEventListener('click', function(){ runL(); if (rank.length) copyText('rank,subject,score,characters\r\n' + rank.map(function(o, i){ return [i + 1, csvq(o.s), o.r.score, o.r.n].join(','); }).join('\r\n'), 'toast'); });
  run(); runL();
''',
        content=f'''
    <h2>What Is an Email Subject Line Tester?</h2>
    <p>An email subject line tester checks the one line that decides whether your email gets opened. It looks at the things readers and spam filters notice first: length, words that sound like spam, shouting capitals, piles of exclamation marks, emoji and the preheader text that sits next to the subject in the inbox.</p>
    <p>This tester gives a score out of 100, explains every issue in plain words and shows roughly where phones and desktop inboxes cut the line off. You can also paste a list of ideas and rank them. Everything runs in your browser, so your campaign never leaves your device.</p>

    <h2>How to Use the Subject Line Tester</h2>
    <ol>
      <li><strong>Enter your sender name, subject line and preheader.</strong> Merge tags such as <code>{{{{first_name}}}}</code> or <code>*|FNAME|*</code> are understood, and the preview shows a sample name.</li>
      <li><strong>Read the score and the checks.</strong> Each row says Good, Improve or Fix, with the reason and a quick way to fix it.</li>
      <li><strong>Look at the inbox preview.</strong> If the key words are hidden on the phone, move them to the front.</li>
      <li><strong>Compare ideas.</strong> Paste up to 20 subject lines, one per line, and the tool ranks them. Copy the ranking to share with your team.</li>
    </ol>

    <h2>What the Tester Checks</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Check', 'Good target', 'Why it matters')}
      <tbody>
        <tr><td>Length</td><td>About 28 to 50 characters</td><td>Phones show roughly 30 to 40 characters and desktops 60 to 70, so long lines lose their ending</td></tr>
        <tr><td>Words</td><td>3 to 12 words</td><td>Short enough to scan in a busy inbox, long enough to say what is inside</td></tr>
        <tr><td>Capitals and punctuation</td><td>Normal case, one exclamation mark at most</td><td>ALL CAPS and <code>!!!</code> read as shouting and are classic spam signals</td></tr>
        <tr><td>Spam trigger words</td><td>None, or one clear offer</td><td>Phrases like "act now" or "risk free" are common in spam. One word rarely sends mail to spam, but stacking them hurts</td></tr>
        <tr><td>Fake Re: or Fwd:</td><td>Only on real replies</td><td>Google says not to start subjects with <code>Re:</code> or <code>Fwd:</code> unless the message really is a reply or forward</td></tr>
        <tr><td>Emoji</td><td>0 to 2</td><td>One emoji can stand out. Many look spammy, and the line must still make sense without them</td></tr>
        <tr><td>Preheader</td><td>About 40 to 110 characters</td><td>An empty preheader lets "View in browser" or menu text show in the inbox instead</td></tr>
      </tbody>
    </table></div>
    <p>The rules on misleading subject lines come straight from the <a href="https://support.google.com/mail/answer/81126" {EXT}>Google email sender guidelines</a>, which also ask bulk senders to keep spam complaints under 0.1%.</p>

    <h2>Practical Tips for Better Open Rates</h2>
    <ul>
      <li><strong>Front load the value.</strong> Put the offer, the deadline or the benefit in the first 30 characters, where every inbox shows it.</li>
      <li><strong>Treat the preheader as line two.</strong> The subject earns attention and the preheader gives a second reason to open. Never repeat the subject.</li>
      <li><strong>Be specific.</strong> "3 new chai blends to try" beats "Our latest newsletter" because readers know what they get.</li>
      <li><strong>Match the email.</strong> A subject that promises something the email does not deliver brings spam complaints, which hurt every future send.</li>
      <li><strong>Test with real people.</strong> No score can predict your audience. Use the score to remove mistakes, then A/B test your top two lines on a small slice of your list.</li>
    </ul>

    <h2>Write Emails People Want to Open</h2>
    <p>Plan the whole program with our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, grow a list worth writing to with <a href="{B}how-to-generate-high-quality-leads-2026/">how to generate high quality leads</a>, and turn opens into sales with <a href="{B}conversion-rate-optimization/">conversion rate optimization</a>. Sending to more than a few thousand people a day? Set up your domain with the <a href="{T}dmarc-record-generator/">DMARC record generator</a> so your mail reaches the inbox at all.</p>
''',
        faqs=[
            ("What is a good length for an email subject line?", "Aim for about 28 to 50 characters, or roughly 4 to 9 words. Phones usually show around 30 to 40 characters and desktop inboxes about 60 to 70, so put the most important words first in case the end is cut off."),
            ("Do spam trigger words really send email to spam?", "Not on their own. Gmail and other providers mostly judge your sender reputation, authentication and how readers react. But piling up phrases like free, act now and guaranteed makes an email look like spam to people and filters, so keep to one clear offer."),
            ("What is a preheader and should I always set one?", "The preheader is the short preview text that inboxes show next to or under the subject line. Yes, always set one. If you leave it empty, the inbox shows the first text in your email, which is often a View in browser link or menu text."),
            ("Can I use emoji in email subject lines?", "Yes, one or two can help a line stand out, especially in busy promotion tabs. Make sure the subject still makes sense if the emoji does not display, and never use emoji to fake buttons or graphics, which Google sender guidelines warn against."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026"),
                 ("Conversion Rate Optimization", "conversion-rate-optimization"), ("Digital Marketing Tips for 2026", "digital-marketing-tips-2026")],
    ))

    # ---------- 2. DMARC RECORD GENERATOR AND CHECKER ----------
    DM_CHECK = 'v=DMARC1; p=quarantine; pct=50; rua=mailto:dmarc@yourshop.in,reports@dmarc.example.net; adkim=s; fo=1'
    POL = [('none', 'none: monitor only, no action'), ('quarantine', 'quarantine: send failing mail to spam'), ('reject', 'reject: block failing mail')]
    TOOLS.append(dict(
        slug='dmarc-record-generator', short='DM', name='DMARC Record Generator and Checker',
        card='Create a valid DMARC TXT record for your domain, or paste an existing one to check every tag against the new RFC 9989 rules.',
        title='DMARC Record Generator and Checker: Free TXT Record',
        desc='Free DMARC record generator and checker. Build the _dmarc TXT record for Gmail and Yahoo sender rules, or paste a record to find errors and old tags.',
        h1='DMARC Record Generator and Checker',
        lead='Choose a policy and a report address to get a ready to paste DMARC TXT record, with the exact host name for your DNS panel. Already have a record? Paste it into the checker to find mistakes, outdated tags and missing protection in seconds.',
        tool='''<section class="tool" aria-label="DMARC record generator">
    <div class="card" style="min-width:0">
      <h2>Build Your DMARC Record</h2>
      ''' + F('dmDom', 'Your domain', 'yourshop.in', em='the domain in your From address', mono=True) + '''
      ''' + F('dmP', 'Policy for mail that fails', 'none', tag='select', opts=POL) + '''
      ''' + F('dmRua', 'Send aggregate reports to', 'dmarc@yourshop.in', em='one or more emails, comma separated', mono=True) + '''
      <div class="row2">''' + F('dmSp', 'Subdomain policy', '', tag='select', opts=[('', 'Same as main policy')] + POL) + F('dmNp', 'Subdomains that do not exist', '', tag='select', opts=[('', 'Same as subdomain policy')] + POL) + '''</div>
      <div class="row2">''' + F('dmAd', 'DKIM alignment', 'r', tag='select', opts=[('r', 'Relaxed (default)'), ('s', 'Strict')]) + F('dmAs', 'SPF alignment', 'r', tag='select', opts=[('r', 'Relaxed (default)'), ('s', 'Strict')]) + '''</div>
      ''' + F('dmRuf', 'Send failure reports to', '', em='optional, few providers send them', mono=True, ph='forensic@yourshop.in') + '''
      <div id="dmFoBox" style="display:none;margin-bottom:10px"><p style="font-size:14px;margin:0 0 6px"><strong>When to send failure reports</strong></p>''' + CK('dmFo0', 'Both SPF and DKIM fail (default)', True) + CK('dmFo1', 'SPF or DKIM fails', False) + CK('dmFoD', 'DKIM fails', False) + CK('dmFoS', 'SPF fails', False) + '''</div>
      ''' + CK('dmT', 'Test mode (<code>t=y</code>): ask receivers to apply one step softer policy while you check reports', False) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your DNS Record</h2>
      <div style="overflow-x:auto"><table class="rtable"><tbody>
        <tr><td style="width:30%"><strong>Type</strong></td><td class="mono">TXT</td></tr>
        <tr><td><strong>Host or Name</strong></td><td class="mono" id="dmHost" style="word-break:break-all"></td></tr>
        <tr><td><strong>Full name</strong></td><td class="mono" id="dmFull" style="word-break:break-all"></td></tr>
        <tr><td><strong>TTL</strong></td><td class="mono">3600 or your panel default</td></tr>
      </tbody></table></div>
      <p style="font-size:14px;margin:14px 0 6px"><strong>Value</strong></p>
      <div class="code-out mono" id="dmRec" style="word-break:break-all;white-space:pre-wrap"></div>
      <div class="actions" style="margin:12px 0"><button class="btn dark" id="dmCopy">Copy Record</button><button class="btn" id="dmCopyHost">Copy Host</button></div>
      <div class="kw-result" id="dmNotes"></div>
      <div id="dmExtBox" style="display:none"><p style="font-size:14px;margin:0 0 6px"><strong>Report address on another domain</strong></p><p style="font-size:14px;margin:0 0 6px">The owner of each report domain below must publish this TXT record, or receivers will not send reports there. Most DMARC report services do this for you.</p><div class="code-out mono" id="dmExt" style="word-break:break-all;white-space:pre-wrap"></div></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Check an Existing DMARC Record</h2>
      ''' + F('dmIn', 'Paste your DMARC record', DM_CHECK, em='quotes and split strings are fine', tag='textarea', mono=True, extra=' style="min-height:80px"') + '''
      <div class="kw-result" id="dmCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="dmTags"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="dmFix">Load Into Generator</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var EM = /^[^\s@,;!]+@([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i;
  var DOM = /^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$/i;
  var SLD = {co:1, com:1, net:1, org:1, gov:1, ac:1, edu:1, gen:1, firm:1, ind:1, res:1, ltd:1, plc:1, me:1, nic:1};
  function org(d){ var p = d.toLowerCase().replace(/\.$/, '').split('.'); if (p.length > 2 && p[p.length - 1].length === 2 && SLD[p[p.length - 2]]) return p.slice(-3).join('.'); return p.slice(-2).join('.'); }
  function cleanDom(v){ return v.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^_dmarc\./, '').replace(/[\/:].*$/, '').replace(/\.$/, ''); }
  function emails(v){ return v.split(/[,;\s]+/).map(function(x){ return x.trim().replace(/^mailto:/i, ''); }).filter(Boolean); }
  var PN = {none: 'monitor only', quarantine: 'send to spam', reject: 'block'};
  var rec = '', host = '';
  function gen(){
    var d = cleanDom($('dmDom').value), p = $('dmP').value, sp = $('dmSp').value, np = $('dmNp').value, rua = emails($('dmRua').value), ruf = emails($('dmRuf').value);
    var N = [], cls = 'ok', bad = [];
    $('dmFoBox').style.display = ruf.length ? '' : 'none';
    if (!d || !DOM.test(d)){ bad.push('Enter a valid domain, such as ' + c('yourshop.in') + '.'); }
    rua.concat(ruf).forEach(function(e){ if (!EM.test(e)) bad.push(c(e) + ' is not a valid email address.'); });
    var t = ['v=DMARC1', 'p=' + p];
    if (sp && sp !== p) t.push('sp=' + sp);
    var spEff = sp || p; if (np && np !== spEff) t.push('np=' + np);
    if (rua.length) t.push('rua=' + rua.map(function(e){ return 'mailto:' + e; }).join(','));
    if (ruf.length) t.push('ruf=' + ruf.map(function(e){ return 'mailto:' + e; }).join(','));
    if ($('dmAd').value === 's') t.push('adkim=s');
    if ($('dmAs').value === 's') t.push('aspf=s');
    if (ruf.length){ var fo = []; if ($('dmFo0').checked) fo.push('0'); if ($('dmFo1').checked) fo.push('1'); if ($('dmFoD').checked) fo.push('d'); if ($('dmFoS').checked) fo.push('s'); if (fo.length && !(fo.length === 1 && fo[0] === '0')) t.push('fo=' + fo.join(':')); }
    if ($('dmT').checked) t.push('t=y');
    rec = t.join('; '); host = '_dmarc' + (d && d.split('.').length > 2 && org(d) !== d ? '.' + d.slice(0, -org(d).length - 1) : '');
    $('dmRec').textContent = rec; $('dmHost').textContent = host; $('dmFull').textContent = '_dmarc.' + (d || 'yourdomain.com');
    if (bad.length){ say('dmNotes', 'bad', '<strong>Fix this first:</strong> ' + bad.join(' ')); $('dmExtBox').style.display = 'none'; return; }
    if (p === 'none'){ cls = 'warn'; N.push('<strong>Monitoring mode.</strong> This meets the Gmail and Yahoo minimum for bulk senders, but it does not stop anyone faking your domain. Read your reports for 2 to 4 weeks, then move to ' + c('quarantine') + '.'); }
    else N.push('<strong>Protection is on:</strong> mail that fails DMARC will be ' + (p === 'reject' ? 'blocked' : 'sent to spam') + (($('dmT').checked) ? ', but test mode asks receivers to treat it one step softer, as ' + c(p === 'reject' ? 'quarantine' : 'none') : '') + '.');
    if (!rua.length){ cls = 'warn'; N.push('No report address, so you will not see who sends mail as your domain. Add one before you tighten the policy.'); }
    if (p !== 'none' && !rua.length) cls = 'bad';
    if ($('dmAd').value === 's' || $('dmAs').value === 's') N.push('Strict alignment needs the exact same domain, so mail sent from a subdomain or some email tools may fail. Relaxed is right for most sites.');
    if (spEff === 'none' && p !== 'none') N.push('Subdomains stay on ' + c('none') + ', so attackers could still fake ' + c('anything.' + d) + '.');
    if ($('dmT').checked && p === 'none') N.push(c('t=y') + ' has no effect with ' + c('p=none') + '.');
    N.push('Add the record in your DNS panel, where your domain is managed, not in your email tool. Changes can take up to a few hours to show.');
    say('dmNotes', cls, N.join('<br>'));
    var me = org(d), ext = rua.concat(ruf).map(function(e){ return e.split('@')[1].toLowerCase(); }).filter(function(x, i, a){ return org(x) !== me && a.indexOf(x) === i; });
    $('dmExtBox').style.display = ext.length ? '' : 'none';
    $('dmExt').textContent = ext.map(function(x){ return 'Host: ' + me + '._report._dmarc.' + x + '\nType: TXT\nValue: v=DMARC1'; }).join('\n\n');
  }
  var INFO = {v: 'Version. Must be exactly DMARC1 and come first.', p: 'Policy for mail that fails DMARC.', sp: 'Policy for subdomains.', np: 'Policy for subdomains that do not exist in DNS (new in RFC 9989).',
    rua: 'Where receivers send daily aggregate reports.', ruf: 'Where receivers send failure reports, if they send them at all.', adkim: 'DKIM alignment: r relaxed, s strict.', aspf: 'SPF alignment: r relaxed, s strict.',
    fo: 'When to send failure reports: 0 all fail, 1 any fails, d DKIM fails, s SPF fails.', t: 'Test mode: y applies one step softer policy, n applies the policy as written.', psd: 'Public suffix flag, only for domain registries. Most sites never need it.',
    pct: 'Removed in RFC 9989 (May 2026). Updated receivers ignore it, so use t=y for a gradual rollout.', ri: 'Removed in RFC 9989. Receivers send reports daily and ignore this tag.', rf: 'Removed in RFC 9989. Failure reports use one format now.'};
  var parsed = null;
  function check(){
    var raw = $('dmIn').value.trim(), E = [], W = [], rows = [];
    parsed = null;
    if (!raw){ $('dmTags').innerHTML = ''; say('dmCheck', '', 'Paste a DMARC record to check it.'); return; }
    var q = raw.match(/"((?:[^"\\]|\\.)*)"/g), s = q ? q.map(function(x){ return x.slice(1, -1); }).join('') : raw.replace(/^.*?\bTXT\b\s*/i, '');
    s = s.replace(/\s+/g, ' ').trim();
    var cnt = (s.match(/v\s*=\s*DMARC1/gi) || []).length;
    if (cnt > 1) E.push('There are ' + cnt + ' DMARC records. A domain must have only one, or receivers ignore them all.');
    var parts = s.split(';').map(function(x){ return x.trim(); }).filter(Boolean), tags = {}, order = [];
    parts.forEach(function(x){
      var m = x.match(/^([A-Za-z]+)\s*=\s*(.*)$/);
      if (!m){ E.push('Cannot read ' + c(x) + '. Each tag needs the form ' + c('name=value') + '.'); return; }
      var k = m[1].toLowerCase(), v = m[2].trim();
      if (tags[k] !== undefined) E.push('The tag ' + c(k) + ' appears twice.');
      tags[k] = v; order.push(k);
    });
    if (order[0] !== 'v') E.push('The record must start with ' + c('v=DMARC1') + '.');
    else if (tags.v !== 'DMARC1') E.push(c('v=' + tags.v) + ' is wrong. It must be exactly ' + c('v=DMARC1') + ', in capitals.');
    var POLS = /^(none|quarantine|reject)$/i;
    if (tags.p === undefined) (tags.rua ? W : E).push('No ' + c('p=') + ' policy. ' + (tags.rua ? 'Under RFC 9989 receivers treat this as ' + c('p=none') + ', but add it so every receiver reads the record.' : 'Without it the record is not valid.'));
    else if (!POLS.test(tags.p)) E.push(c('p=' + tags.p) + ' is not valid. Use none, quarantine or reject.');
    ['sp', 'np'].forEach(function(k){ if (tags[k] !== undefined && !POLS.test(tags[k])) E.push(c(k + '=' + tags[k]) + ' is not valid. Use none, quarantine or reject.'); });
    ['adkim', 'aspf'].forEach(function(k){ if (tags[k] !== undefined && !/^[rs]$/i.test(tags[k])) E.push(c(k + '=' + tags[k]) + ' is not valid. Use r or s.'); });
    if (tags.t !== undefined && !/^[yn]$/i.test(tags.t)) E.push(c('t=' + tags.t) + ' is not valid. Use y or n.');
    if (tags.psd !== undefined && !/^[ynu]$/i.test(tags.psd)) E.push(c('psd=' + tags.psd) + ' is not valid. Use y, n or u.');
    if (tags.fo !== undefined && !/^[01ds](:[01ds])*$/i.test(tags.fo)) E.push(c('fo=' + tags.fo) + ' is not valid. Use 0, 1, d or s, joined with colons.');
    if (tags.fo !== undefined && tags.ruf === undefined) W.push(c('fo') + ' only matters when you also set a ' + c('ruf') + ' address.');
    ['rua', 'ruf'].forEach(function(k){
      if (tags[k] === undefined) return;
      tags[k].split(',').map(function(x){ return x.trim(); }).forEach(function(u){
        if (!/^mailto:/i.test(u)) E.push(c(u) + ' in ' + c(k) + ' must start with ' + c('mailto:') + '.');
        else if (!EM.test(u.replace(/^mailto:/i, '').replace(/!\d+[kmgt]?$/i, ''))) E.push(c(u) + ' is not a valid email address.');
      });
    });
    if (tags.pct !== undefined) W.push(c('pct=' + tags.pct) + ' was removed in RFC 9989 (May 2026), so receivers that follow the new standard ignore it and apply the full policy' + (tags.pct !== '100' ? ', not ' + esc(tags.pct) + '%' : '') + '. Use ' + c('t=y') + ' for a softer test instead.');
    ['ri', 'rf'].forEach(function(k){ if (tags[k] !== undefined) W.push(c(k) + ' was removed in RFC 9989 and can be deleted.'); });
    order.forEach(function(k){ if (!INFO[k]) W.push('Unknown tag ' + c(k) + '. Receivers ignore it, so check for a typo.'); });
    if (!tags.rua) W.push('No ' + c('rua') + ' address, so you get no reports about who sends mail as your domain.');
    var p = (tags.p || 'none').toLowerCase();
    var lvl = p === 'reject' ? 'full protection' : p === 'quarantine' ? 'partial protection, failing mail goes to spam' : 'monitoring only, no protection yet';
    if (/^y$/i.test(tags.t || '') && p !== 'none') lvl += ', softened by test mode';
    rows = order.map(function(k){ return '<tr><td class="mono"><strong>' + esc(k) + '</strong></td><td class="mono" style="word-break:break-all">' + esc(tags[k]) + '</td><td>' + esc(INFO[k] || 'Unknown tag') + '</td></tr>'; });
    $('dmTags').innerHTML = rows.length ? '<thead><tr><th>Tag</th><th>Value</th><th>Meaning</th></tr></thead><tbody>' + rows.join('') + '</tbody>' : '';
    var h = E.length ? '<strong>' + E.length + ' error' + (E.length === 1 ? '' : 's') + ' to fix.</strong> ' : '<strong>Valid DMARC record: ' + lvl + '.</strong> ';
    if (E.length) h += '<br>' + E.join('<br>');
    if (W.length) h += '<br>' + W.map(function(x){ return 'Note: ' + x; }).join('<br>');
    say('dmCheck', E.length ? 'bad' : W.length ? 'warn' : 'ok', h);
    parsed = tags;
  }
  function load(){
    check(); if (!parsed) return; var tg = parsed;
    function set(id, v, ok){ if (v !== undefined && ok.test(v)) $(id).value = v.toLowerCase(); }
    set('dmP', tg.p, /^(none|quarantine|reject)$/i); $('dmSp').value = ''; $('dmNp').value = ''; set('dmSp', tg.sp, /^(none|quarantine|reject)$/i); set('dmNp', tg.np, /^(none|quarantine|reject)$/i);
    $('dmAd').value = /^s$/i.test(tg.adkim || '') ? 's' : 'r'; $('dmAs').value = /^s$/i.test(tg.aspf || '') ? 's' : 'r';
    function em(v){ return (v || '').split(',').map(function(x){ return x.trim().replace(/^mailto:/i, '').replace(/!\d+[kmgt]?$/i, ''); }).filter(Boolean).join(', '); }
    $('dmRua').value = em(tg.rua); $('dmRuf').value = em(tg.ruf); $('dmT').checked = /^y$/i.test(tg.t || '');
    var fo = (tg.fo || '0').toLowerCase().split(':'); $('dmFo0').checked = fo.indexOf('0') > -1; $('dmFo1').checked = fo.indexOf('1') > -1; $('dmFoD').checked = fo.indexOf('d') > -1; $('dmFoS').checked = fo.indexOf('s') > -1;
    var r = $('dmRua').value.split(',')[0]; if (r && r.indexOf('@') > 0 && !$('dmDom').value.trim()) $('dmDom').value = r.split('@')[1];
    gen(); $('dmRec').scrollIntoView({behavior: 'smooth', block: 'center'});
  }
  ['dmDom', 'dmRua', 'dmRuf'].forEach(function(id){ $(id).addEventListener('input', gen); });
  ['dmP', 'dmSp', 'dmNp', 'dmAd', 'dmAs', 'dmFo0', 'dmFo1', 'dmFoD', 'dmFoS', 'dmT'].forEach(function(id){ $(id).addEventListener('change', gen); });
  var tc; $('dmIn').addEventListener('input', function(){ clearTimeout(tc); tc = setTimeout(check, 80); });
  $('dmCopy').addEventListener('click', function(){ gen(); copyText(rec, 'toast'); });
  $('dmCopyHost').addEventListener('click', function(){ gen(); copyText(host, 'toast'); });
  $('dmFix').addEventListener('click', load);
  gen(); check();
''',
        content=f'''
    <h2>What Is a DMARC Record?</h2>
    <p>DMARC is a short TXT record in your domain's DNS that tells Gmail, Yahoo, Outlook and other mailbox providers what to do with email that claims to come from you but fails SPF and DKIM checks. It can let that mail through, send it to spam or block it, and it asks receivers to email you daily reports about who is sending mail with your domain.</p>
    <p>DMARC is no longer optional for marketers. The <a href="https://support.google.com/mail/answer/81126" {EXT}>Google email sender guidelines</a> require it for anyone sending about 5,000 or more messages a day to Gmail, with at least <code>p=none</code> and a From domain that aligns with SPF or DKIM. Yahoo and Microsoft Outlook have similar rules. This generator builds a correct record, and the checker reads an existing one against RFC 9989, the updated DMARC standard published in May 2026.</p>

    <h2>How to Create and Add Your DMARC Record</h2>
    <ol>
      <li><strong>Set up SPF and DKIM first.</strong> DMARC builds on them. Your email platform shows the records to add for both.</li>
      <li><strong>Enter your domain and a report address,</strong> then keep the policy on <code>none</code> for your first record.</li>
      <li><strong>Copy the host and value</strong> into your DNS panel as a new TXT record. In most panels the host is just <code>_dmarc</code>.</li>
      <li><strong>Read the reports for 2 to 4 weeks.</strong> Make sure every tool that sends for you, such as your newsletter, CRM and shop, passes.</li>
      <li><strong>Tighten the policy</strong> to <code>quarantine</code>, then <code>reject</code>. Paste the live record into the checker after each change.</li>
    </ol>

    <h2>DMARC Tags Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Tag', 'Example', 'What it does')}
      <tbody>
        <tr><td><code>v</code></td><td><code>v=DMARC1</code></td><td>Version. Required, and it must come first</td></tr>
        <tr><td><code>p</code></td><td><code>p=quarantine</code></td><td>What to do with failing mail: none, quarantine or reject</td></tr>
        <tr><td><code>rua</code></td><td><code>rua=mailto:dmarc@yourshop.in</code></td><td>Where daily aggregate reports go. Strongly recommended</td></tr>
        <tr><td><code>sp</code> and <code>np</code></td><td><code>sp=reject</code></td><td>Policies for subdomains, and for subdomains that do not exist. They default to <code>p</code></td></tr>
        <tr><td><code>adkim</code> and <code>aspf</code></td><td><code>adkim=s</code></td><td>Relaxed (the default) accepts subdomains of your domain, strict needs an exact match</td></tr>
        <tr><td><code>t</code></td><td><code>t=y</code></td><td>New test mode. Receivers apply the next softer policy, so reject acts like quarantine</td></tr>
        <tr><td><code>pct</code>, <code>ri</code>, <code>rf</code></td><td><code>pct=50</code></td><td>Removed in RFC 9989. Receivers ignore them, so you can delete them</td></tr>
      </tbody>
    </table></div>
    <p>The full tag list is in <a href="https://www.rfc-editor.org/rfc/rfc9989" {EXT}>RFC 9989 on the RFC Editor site</a>. Google's <a href="https://support.google.com/a/answer/14229414" {EXT}>sender guidelines FAQ</a> covers what Gmail checks.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Only one record per domain.</strong> Two DMARC records cancel each other out. Edit the existing one instead of adding another.</li>
      <li><strong>Use a separate mailbox for reports.</strong> Aggregate reports are XML files and busy domains get many a day. A free or paid DMARC report service makes them readable.</li>
      <li><strong>Do not jump to reject.</strong> A newsletter tool or invoice system you forgot about will have its mail blocked. Fix every sender in the reports first.</li>
      <li><strong>Clean up old tags.</strong> If your record still has <code>pct</code>, it no longer softens anything under the new standard. Use <code>t=y</code> for testing instead.</li>
    </ul>

    <h2>Make Sure Your Emails Arrive</h2>
    <p>Authentication gets you to the inbox; good content keeps you there. Read our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, learn about consent and lists in <a href="{B}data-privacy-and-first-party-data/">data privacy and first party data</a>, and if your site sends mail from code, see <a href="{B}send-email-code-in-php/">how to send email in PHP</a>. Then polish your next campaign with the <a href="{T}email-subject-line-tester/">email subject line tester</a>.</p>
''',
        faqs=[
            ("What is the best DMARC policy to start with?", "Start with p=none and a rua report address. It changes nothing for your mail but shows you every service sending as your domain. After 2 to 4 weeks of clean reports, move to p=quarantine and then to p=reject for full protection."),
            ("Where do I add the DMARC record?", "Add it as a TXT record in the DNS settings where your domain is managed, such as your domain registrar, hosting panel or Cloudflare. Most panels want the host as _dmarc, and they add your domain for you. It is not added inside your email marketing tool."),
            ("Is DMARC required to send email to Gmail?", "Google requires DMARC for anyone sending about 5,000 or more messages a day to Gmail accounts, with a policy of at least p=none and a From domain aligned with SPF or DKIM. Smaller senders need SPF or DKIM, but DMARC is still strongly recommended."),
            ("What changed in DMARC with RFC 9989?", "RFC 9989, published in May 2026, replaced the original DMARC standard. It removed the pct, ri and rf tags, added np for subdomains that do not exist, t for test mode and psd for domain registries. Existing records keep working, and receivers simply ignore the removed tags."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("Send Email Code in PHP", "send-email-code-in-php"),
                 ("Data Privacy and First Party Data", "data-privacy-and-first-party-data"), ("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'email-marketing-tools'; t['updated'] = '2026-11-10'
