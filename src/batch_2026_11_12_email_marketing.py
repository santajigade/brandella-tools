"""Batch 15 (2026-11-12): Email Marketing Tools, fourth tool (Email List Cleaner).
Facts checked 2026-11-12 against: Google, Dots don't matter in Gmail addresses (support.google.com/mail/answer/7436150),
and Gmail plus addressing (support.google.com/mail/answer/12096) so dot and plus versions reach one inbox;
Google email sender guidelines (support.google.com/mail/answer/81126): keep spam rate low (below 0.3%), send only to
people who signed up; RFC 2606: example.com, example.net, example.org and the .test, .example, .invalid, .localhost
TLDs are reserved and never receive mail; RFC 5321 section 4.5.3.1: local part at most 64 octets, domain at most 255,
path at most 256 octets (so an address at most 254 characters); MDN input type=email for the browser validation rule.
Search demand: "email list cleaner" and "email list cleaning free" are served by Clearout, Jitbit, DeBounce and others,
mostly with credit limits and an upload step. This tool does syntax, typo, duplicate, disposable and role checks
locally and says plainly it cannot test whether a mailbox exists."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/email-marketing-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

SAMPLE = '''Name, Email, City
Priya Sharma, Priya.Sharma@Gmail.com, Pune
Rahul Verma, rahul.verma@gmial.com, Delhi
priyasharma+offers@gmail.com
"Anita Rao" <anita@yourshop.in>
info@acmetraders.in
rahul.verma@gmail.com
test@mailinator.com
sanjay@@gmail.com
meera.k@outlook.con
neha..joshi@yahoo.co.in
mailto:arjun@rediffmail.com;
someone@example.com
Kiran@Company.co.in
kiran@company.co.in'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='email-list-cleaner', short='EL', name='Email List Cleaner',
        card='Paste a messy email list to remove duplicates, invalid and disposable addresses, fix domain typos and download a clean CSV.',
        title='Email List Cleaner: Remove Duplicates and Bad Emails',
        desc='Free email list cleaner. Remove duplicate, invalid, fake and disposable emails, fix typos like gmial.com and download a clean CSV. Nothing is uploaded.',
        h1='Email List Cleaner',
        lead='Paste emails from a spreadsheet, CRM export or sign up form in any format. The cleaner pulls out every address, fixes common domain typos, removes duplicates, broken addresses and throwaway inboxes, and gives you a clean list to import. Your list never leaves your browser.',
        tool='''<section class="tool" aria-label="Email list cleaner">
    <div class="card" style="min-width:0">
      <h2>Paste Your List</h2>
      ''' + F('elIn', 'Emails, CSV rows or any text', SAMPLE, em='one per line, commas or a whole CSV are fine', tag='textarea', mono=True, extra=' style="min-height:260px"') + '''
      <p style="font-size:14px;margin:0 0 6px"><strong>Cleaning options</strong></p>
      ''' + CK('elTypo', 'Fix common domain typos, such as <code>gmial.com</code> and <code>.con</code>') + '''
      ''' + CK('elGm', 'Treat Gmail dot and plus versions as the same person') + '''
      ''' + CK('elDisp', 'Remove disposable and test addresses') + '''
      ''' + CK('elRole', 'Remove role addresses, such as <code>info@</code> and <code>sales@</code>', False) + '''
      ''' + CK('elSort', 'Sort A to Z', False) + '''
      ''' + F('elFmt', 'Output format', 'line', tag='select', opts=[('line', 'One email per line'), ('comma', 'Comma separated'), ('csv', 'CSV with an email header')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Clean List</h2>
      <div class="stats">''' + S('elFound', 'Found') + S('elClean', 'Clean') + S('elDup', 'Duplicates') + S('elFix', 'Typos fixed') + S('elRem', 'Removed') + '''</div>
      <div class="field"><label for="elOut">Ready to import</label><textarea id="elOut" class="mono" readonly spellcheck="false" style="min-height:200px"></textarea></div>
      <div class="actions" style="margin:0 0 12px"><button class="btn dark" id="elCopy">Copy Clean List</button><button class="btn" id="elDl">Download CSV</button><button class="btn" id="elRep">Download Full Report</button><span class="toast" id="toast">Copied!</span></div>
      <div class="kw-result" id="elNote"></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>What Changed and Why</h2>
      <div style="overflow-x:auto;max-height:420px;overflow-y:auto"><table class="rtable" id="elTbl"></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var FIX = {'gmial.com':'gmail.com','gmai.com':'gmail.com','gmal.com':'gmail.com','gamil.com':'gmail.com','gnail.com':'gmail.com','gmaill.com':'gmail.com','gmail.co':'gmail.com','gmail.cm':'gmail.com','gmail.om':'gmail.com','gmail.cmo':'gmail.com','gmil.com':'gmail.com','gmail':'gmail.com','gmailcom':'gmail.com','gmail.com.com':'gmail.com',
    'yaho.com':'yahoo.com','yahooo.com':'yahoo.com','yhoo.com':'yahoo.com','yahoo.cm':'yahoo.com','yaoo.com':'yahoo.com','yahoo':'yahoo.com','yahoo.co.inn':'yahoo.co.in','yaho.co.in':'yahoo.co.in','yahoo.in':'yahoo.in',
    'hotmial.com':'hotmail.com','hotmal.com':'hotmail.com','hotmil.com':'hotmail.com','hotamil.com':'hotmail.com','hotmail.co':'hotmail.com','hotmail':'hotmail.com',
    'outlok.com':'outlook.com','outllook.com':'outlook.com','outlook.co':'outlook.com','otlook.com':'outlook.com','outlook':'outlook.com',
    'iclod.com':'icloud.com','icoud.com':'icloud.com','icloud.co':'icloud.com','redifmail.com':'rediffmail.com','rediffmail.co':'rediffmail.com','rediffmai.com':'rediffmail.com'};
  var TLDFIX = {con:'com', cmo:'com', ocm:'com', vom:'com', xom:'com', comm:'com', coom:'com', cpm:'com', cim:'com', nett:'net', ogr:'org'};
  var BIG = ['gmail.com','yahoo.com','hotmail.com','outlook.com','icloud.com','rediffmail.com','yahoo.co.in','googlemail.com'];
  var REAL = {'mail.com':1,'gmx.com':1,'ymail.com':1,'email.com':1,'yahoo.co.id':1,'cloud.com':1,'hotmail.fr':1,'hotmail.it':1,'live.com':1,'outlook.in':1,'outlook.fr':1};
  var DISP = ('mailinator.com guerrillamail.com guerrillamail.info guerrillamail.net sharklasers.com grr.la 10minutemail.com 10minutemail.net temp-mail.org temp-mail.io tempmail.com tempmailo.com tempail.com '
    + 'yopmail.com yopmail.net throwawaymail.com trashmail.com trashmail.de getnada.com nada.email dispostable.com maildrop.cc fakeinbox.com mintemail.com mohmal.com emailondeck.com mailnesia.com '
    + 'spamgourmet.com burnermail.io mail.tm moakt.com emailfake.com fakemail.net getairmail.com mailcatch.com mytemp.email tempr.email discard.email inboxkitten.com mailpoof.com spambox.us').split(' ');
  var DS = {}; DISP.forEach(function(d){ DS[d] = 1; });
  var ROLE = {};
  ('info admin administrator support sales contact help office enquiry enquiries inquiry hello team marketing billing accounts accounting careers jobs hr webmaster postmaster hostmaster abuse noreply no-reply donotreply do-not-reply security mail newsletter feedback orders').split(' ').forEach(function(r){ ROLE[r] = 1; });
  var LOCAL = /^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*$/;
  var LABEL = /^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/;
  function dist(a, b){
    if (Math.abs(a.length - b.length) > 1) return 9;
    var d = [], i, j;
    for (i = 0; i <= a.length; i++){ d[i] = [i]; }
    for (j = 0; j <= b.length; j++) d[0][j] = j;
    for (i = 1; i <= a.length; i++) for (j = 1; j <= b.length; j++){
      var cost = a[i - 1] === b[j - 1] ? 0 : 1;
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
    }
    return d[a.length][b.length];
  }
  function fixDomain(d){
    if (FIX[d] && FIX[d] !== d) return FIX[d];
    var p = d.split('.'), t = p[p.length - 1];
    if (p.length > 1 && TLDFIX[t]){ p[p.length - 1] = TLDFIX[t]; var n = p.join('.'); return FIX[n] || n; }
    if (REAL[d] || BIG.indexOf(d) > -1) return '';
    for (var i = 0; i < BIG.length; i++) if (d.length >= 8 && dist(d, BIG[i]) === 1) return BIG[i];
    return '';
  }
  function invalid(e){
    var at = e.lastIndexOf('@');
    if (e.indexOf('@') !== at) return 'More than one @ sign';
    if (at < 1) return 'Nothing before the @ sign';
    var l = e.slice(0, at), d = e.slice(at + 1);
    if (!d) return 'No domain after the @ sign';
    if (l.length > 64) return 'The part before @ is longer than 64 characters';
    if (e.length > 254) return 'Longer than 254 characters';
    if (/\.\./.test(l)) return 'Two dots in a row';
    if (l[0] === '.' || l[l.length - 1] === '.') return 'Starts or ends with a dot before the @';
    if (!LOCAL.test(l)) return 'Has a space or a character email does not allow';
    var p = d.split('.');
    if (p.length < 2) return 'Domain has no ending, such as .com';
    for (var i = 0; i < p.length; i++) if (!LABEL.test(p[i])) return 'The domain is not valid';
    var tld = p[p.length - 1];
    if (!/^([a-z]{2,63}|xn--[a-z0-9-]{1,59})$/.test(tld)) return 'The domain ending is not valid';
    return '';
  }
  function reserved(d){
    var p = d.split('.'), t = p[p.length - 1], two = p.slice(-2).join('.');
    return t === 'test' || t === 'example' || t === 'invalid' || t === 'localhost' || two === 'example.com' || two === 'example.net' || two === 'example.org';
  }
  function key(e){
    var at = e.lastIndexOf('@'), l = e.slice(0, at), d = e.slice(at + 1);
    if ($('elGm').checked && (d === 'gmail.com' || d === 'googlemail.com')){ l = l.split('+')[0].replace(/\./g, ''); d = 'gmail.com'; }
    return l + '@' + d;
  }
  function tokens(raw){
    var out = [];
    raw.split(/[\s,;<>"()\[\]|]+/).forEach(function(t){
      if (t.indexOf('@') < 0) return;
      t = t.replace(/^mailto:/i, '').replace(/[?#].*$/, '').replace(/^['`.:]+|['`.:!]+$/g, '');
      if (t) out.push(t);
    });
    return out;
  }
  var clean = [], report = [];
  function run(){
    var list = tokens($('elIn').value), seen = {}, rows = [], fixed = 0, dup = 0, rem = 0, role = 0;
    clean = []; report = [];
    list.forEach(function(orig){
      var e = orig.toLowerCase(), st = '', note = '', at = e.lastIndexOf('@');
      if ($('elTypo').checked && at > 0 && e.indexOf('@') === at){ var d0 = e.slice(at + 1), f = fixDomain(d0); if (f){ note = 'Typo fixed: ' + d0 + ' to ' + f; e = e.slice(0, at) + '@' + f; fixed++; } }
      var why = invalid(e);
      if (why && note){ fixed--; note = ''; }
      if (!why){
        at = e.lastIndexOf('@'); var l = e.slice(0, at), d = e.slice(at + 1);
        if ($('elDisp').checked && reserved(d)){ st = 'Removed'; why = 'Reserved test domain, never receives mail'; }
        else if ($('elDisp').checked && (DS[d] || DS[d.split('.').slice(-2).join('.')])){ st = 'Removed'; why = 'Disposable inbox that expires'; }
        else {
          var k = key(e);
          if (seen[k]){ st = 'Duplicate'; why = 'Same as ' + seen[k]; dup++; }
          else if (ROLE[l.split('+')[0]]){
            role++;
            if ($('elRole').checked){ st = 'Removed'; why = 'Role address, shared by a team'; }
            else { st = 'Kept'; why = 'Role address, often lower engagement'; seen[k] = e; clean.push(e); }
          }
          else { st = note ? 'Fixed' : 'Clean'; seen[k] = e; clean.push(e); }
        }
      } else st = 'Invalid';
      if (st === 'Removed' || st === 'Invalid') rem++;
      if (note && st !== 'Fixed') why = note + '. ' + why;
      if (note && st === 'Fixed') why = note;
      report.push([orig, e, st, why]);
      if (st !== 'Clean') rows.push('<tr><td class="mono" style="word-break:break-all">' + esc(orig) + '</td><td><strong>' + st + '</strong></td><td>' + esc(why) + '</td></tr>');
    });
    var out = clean.slice(); if ($('elSort').checked) out.sort();
    var fm = $('elFmt').value;
    $('elOut').value = fm === 'comma' ? out.join(', ') : fm === 'csv' ? (out.length ? 'email\n' + out.join('\n') : '') : out.join('\n');
    $('elFound').textContent = fmtN(list.length); $('elClean').textContent = fmtN(clean.length); $('elDup').textContent = fmtN(dup); $('elFix').textContent = fmtN(fixed); $('elRem').textContent = fmtN(rem);
    var shown = rows.slice(0, 500);
    $('elTbl').innerHTML = rows.length ? '<thead><tr><th>Address as pasted</th><th>Result</th><th>Reason</th></tr></thead><tbody>' + shown.join('') + (rows.length > 500 ? '<tr><td colspan="3">Showing the first 500 of ' + fmtN(rows.length) + ' changes. Download the full report to see them all.</td></tr>' : '') + '</tbody>' : '<tbody><tr><td>Nothing to fix. Every address is valid and unique.</td></tr></tbody>';
    if (!list.length){ say('elNote', '', 'Paste a list to clean it. Any line or cell that contains an @ sign is picked up.'); return; }
    var pct = Math.round((list.length - clean.length) / list.length * 100), N = [];
    N.push('<strong>' + fmtN(clean.length) + ' clean address' + (clean.length === 1 ? '' : 'es') + ' from ' + fmtN(list.length) + ' found.</strong> ' + (pct > 0 ? pct + '% of the list was removed or merged.' : 'Nothing was removed.'));
    if (fixed) N.push('Check the ' + fmtN(fixed) + ' typo fix' + (fixed === 1 ? '' : 'es') + ' in the table below before you import.');
    if (role && !$('elRole').checked) N.push(fmtN(role) + ' role address' + (role === 1 ? ' was' : 'es were') + ' kept. Tick the option to remove them for newsletters.');
    N.push('This checks format, typos and duplicates. It cannot test whether a mailbox exists, so remove addresses that bounce after your first send.');
    say('elNote', pct >= 20 ? 'warn' : 'ok', N.join('<br>'));
  }
  function csvq(s){ return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  var tm; $('elIn').addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(run, 150); });
  ['elTypo', 'elGm', 'elDisp', 'elRole', 'elSort', 'elFmt'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('elCopy').addEventListener('click', function(){ run(); copyText($('elOut').value, 'toast'); });
  $('elDl').addEventListener('click', function(){ run(); var o = clean.slice(); if ($('elSort').checked) o.sort(); download('clean-email-list.csv', 'email\n' + o.join('\n') + '\n', 'text/csv'); });
  $('elRep').addEventListener('click', function(){ run(); download('email-list-report.csv', 'original,cleaned,result,reason\n' + report.map(function(r){ return r.map(csvq).join(','); }).join('\n') + '\n', 'text/csv'); });
  run();
''',
        content=f'''
    <h2>What Is an Email List Cleaner?</h2>
    <p>An email list cleaner takes a raw list of addresses and turns it into one you can safely send to. Lists collected from forms, events, spreadsheets and old CRM exports are always messy: the same person appears twice, someone typed <code>gmial.com</code>, a few addresses are broken, and some sign ups used a throwaway inbox to grab a freebie.</p>
    <p>Sending to those addresses costs you money on every campaign and hurts your sender reputation. Bounces and unengaged addresses tell Gmail and Yahoo that you do not manage your list, and the <a href="https://support.google.com/mail/answer/81126" {EXT}>Google email sender guidelines</a> ask you to keep spam complaints low and to send only to people who asked for your mail. Cleaning before every import is the cheapest fix there is.</p>

    <h2>How to Clean Your Email List</h2>
    <ol>
      <li><strong>Paste your list.</strong> Copy a column from Excel or Google Sheets, a whole CSV export, or even an email thread. Anything with an @ sign is picked up, and names and other columns are ignored.</li>
      <li><strong>Choose your options.</strong> Typo fixes, Gmail matching and disposable removal are on by default. Turn on role address removal for newsletters.</li>
      <li><strong>Review the table.</strong> Every change is listed with a reason, so you can check typo fixes before you trust them.</li>
      <li><strong>Copy or download.</strong> Download the clean CSV for your email tool, or the full report to keep a record of what was removed.</li>
    </ol>

    <h2>What the Cleaner Checks</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Check', 'Example', 'What happens')}
      <tbody>
        <tr><td>Format</td><td><code>sanjay@@gmail.com</code></td><td>Removed as invalid: two @ signs, two dots in a row, spaces, no domain ending</td></tr>
        <tr><td>Domain typos</td><td><code>rahul@gmial.com</code></td><td>Fixed to <code>gmail.com</code>, plus endings like <code>.con</code> and <code>.cmo</code></td></tr>
        <tr><td>Duplicates</td><td><code>Kiran@Company.co.in</code></td><td>Matched without caring about capitals, and only the first copy is kept</td></tr>
        <tr><td>Gmail versions</td><td><code>priyasharma+offers@gmail.com</code></td><td>Matched to <code>priya.sharma@gmail.com</code>, because Gmail ignores dots and plus tags</td></tr>
        <tr><td>Disposable inboxes</td><td><code>test@mailinator.com</code></td><td>Removed. These inboxes expire within minutes or hours</td></tr>
        <tr><td>Test domains</td><td><code>someone@example.com</code></td><td>Removed. <a href="https://www.rfc-editor.org/rfc/rfc2606" {EXT}>RFC 2606</a> reserves these, so they never receive mail</td></tr>
        <tr><td>Role addresses</td><td><code>info@acmetraders.in</code></td><td>Flagged, or removed if you choose. Shared inboxes often engage less</td></tr>
      </tbody>
    </table></div>
    <p>Google confirms that <a href="https://support.google.com/mail/answer/7436150" {EXT}>dots do not matter in Gmail addresses</a>, so <code>priya.sharma</code> and <code>priyasharma</code> reach the same inbox. Other providers treat dots as real, so the cleaner only merges Gmail.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Clean before every import,</strong> not once a year. It takes seconds and stops bad addresses spreading into your CRM.</li>
      <li><strong>Keep the report.</strong> If someone asks why they stopped getting mail, the report shows exactly what happened to their address.</li>
      <li><strong>Remove hard bounces after each send.</strong> No browser tool can prove a mailbox exists. Your email platform's bounce list is the final word.</li>
      <li><strong>Drop people who never open.</strong> A valid address that ignores you for six months hurts deliverability too. Send a last check in email, then remove them.</li>
      <li><strong>Fix the source.</strong> If many sign ups come from throwaway inboxes, use double opt in on that form.</li>
    </ul>

    <h2>Keep Your List Healthy</h2>
    <p>A clean list is the base of every good campaign. Plan what you send with our <a href="{B}email-marketing-strategy/">email marketing strategy guide</a>, grow the list the right way with <a href="{B}how-to-generate-high-quality-leads-2026/">how to generate high quality leads</a>, and stop bots filling your forms with <a href="{B}php-contact-form-spam-protection/">contact form spam protection</a>. Then make sure your mail is trusted with the <a href="{T}spf-record-generator/">SPF record generator and checker</a>.</p>
''',
        faqs=[
            ("Does this tool check whether an email address really exists?", "No. Checking a mailbox needs a connection to the mail server, which a browser cannot make and which would mean sending your list somewhere. This cleaner removes everything that can be caught locally: bad format, typos, duplicates, disposable and test addresses. Remove any address that hard bounces after your first send."),
            ("Is my email list uploaded anywhere?", "No. The cleaning runs entirely in your browser with JavaScript. Your list is never sent to a server, so you can safely clean customer data without sharing it with a third party."),
            ("Why are Gmail addresses with dots or a plus treated as duplicates?", "Gmail ignores dots in the part before the @ sign and delivers name+anything to the same inbox. So priya.sharma@gmail.com and priyasharma+offers@gmail.com belong to one person, and sending to both doubles your mail to them. You can turn this off if you need the versions kept apart."),
            ("Should I remove role addresses like info@ and sales@?", "For newsletters and marketing, usually yes. Role addresses are shared by a team, nobody personally signed up, and they tend to open less and complain more. For B2B leads or replies to enquiries they can be fine, which is why the cleaner only flags them unless you tick the option."),
        ],
        related=[("Email Marketing Strategy", "email-marketing-strategy"), ("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026"),
                 ("PHP Contact Form Spam Protection", "php-contact-form-spam-protection"), ("Send Email Code in PHP", "send-email-code-in-php")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'email-marketing-tools'; t['updated'] = '2026-11-12'
