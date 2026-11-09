"""Batch 12 (2026-11-09): Developer Tools category, tools 5 and 6.
Facts checked 2026-11-09 against: POSIX / Unix time (seconds since 1970-01-01 00:00:00 UTC, leap seconds not counted),
Year 2038 limit of a signed 32 bit time_t (2147483647 = 2038-01-19 03:14:07 UTC), MDN Date (JavaScript time values are
milliseconds since the epoch, range plus or minus 8.64e15 ms), Google Analytics BigQuery export schema (event_timestamp is
in microseconds, UTC), Go time.UnixNano (nanoseconds), Excel and Google Sheets serial dates (=A1/86400+DATE(1970,1,1)),
RFC 4180 (CSV: fields with commas, quotes or line breaks are wrapped in double quotes, a quote inside is doubled, CRLF
line breaks, optional header row), jsonlines.org (one valid JSON value per line, UTF 8, \\n separator), OpenAI Batch API
(input is a .jsonl file, one request per line), BigQuery loads newline delimited JSON, MDN Number.MAX_SAFE_INTEGER
(9007199254740991, larger integers lose precision), OWASP CSV injection (cells starting with = + - @ tab or CR)."""
import json
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, PRE, th

T = 'https://brandella.in/tools/developer-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

ZONES = [('local', 'Your device time zone'), ('UTC', 'UTC'), ('Asia/Kolkata', 'India (IST, UTC+5:30)'), ('America/New_York', 'New York'),
         ('America/Los_Angeles', 'Los Angeles'), ('Europe/London', 'London'), ('Europe/Berlin', 'Berlin, Paris'), ('Asia/Dubai', 'Dubai'),
         ('Asia/Singapore', 'Singapore'), ('Asia/Tokyo', 'Tokyo'), ('Australia/Sydney', 'Sydney')]


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 5. UNIX TIMESTAMP CONVERTER ----------
    UX_BATCH = ('2026-11-09 server log: login user_1024 at 1794220200\n'
                'GA4 BigQuery event_timestamp 1794220200123456\n'
                'JavaScript Date.now() 1794220212345\n'
                'JWT exp claim 1794306600\n'
                'Go UnixNano 1794220200000000000\n'
                'This line has no timestamp')
    TOOLS.append(dict(
        slug='unix-timestamp-converter', short='UX', name='Unix Timestamp Converter',
        card='Convert Unix epoch time to a readable date in any time zone and back, with seconds, milliseconds and microseconds detected for you.',
        title='Unix Timestamp Converter: Epoch to Date and Back',
        desc='Free Unix timestamp converter. Turn epoch time in seconds, milliseconds or microseconds into a date in IST, UTC or any zone, and convert dates back.',
        h1='Unix Timestamp Converter',
        lead='Paste any Unix timestamp to see the exact date and time in UTC, India time or your own time zone. The tool works out whether it is in seconds, milliseconds, microseconds or nanoseconds, converts dates back into timestamps, and reads many timestamps from logs at once.',
        tool='''<section class="tool" aria-label="Unix timestamp converter" id="uxForm">
    <div class="card full" style="min-width:0">
      <h2>Current Unix Time</h2>
      <div class="stats">''' + S('uxNowS', 'Seconds') + S('uxNowMs', 'Milliseconds') + '''</div>
      <div class="kw-result" id="uxNowIso" style="margin-bottom:10px">Loading the current time...</div>
      <div class="actions"><button type="button" class="btn btn-sm" id="uxCopyNowS">Copy Seconds</button><button type="button" class="btn btn-sm" id="uxCopyNowMs">Copy Milliseconds</button><button type="button" class="btn btn-sm" id="uxUseNow">Convert Now</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Timestamp to Date</h2>
      ''' + F('uxIn', 'Unix timestamp or date', '1794220200', em='any unit, or an ISO date', mono=True) + '''
      <div class="row2">''' + F('uxUnit', 'Unit', 'auto', tag='select', opts=[('auto', 'Detect automatically'), ('s', 'Seconds'), ('ms', 'Milliseconds'), ('us', 'Microseconds'), ('ns', 'Nanoseconds')]) + F('uxZone', 'Show in time zone', 'Asia/Kolkata', tag='select', opts=ZONES) + '''</div>
      <div class="kw-result" id="uxCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="uxOut"></table></div>
      <div class="actions" style="margin-top:12px"><button class="btn dark" id="uxCopyIso">Copy ISO 8601</button><button class="btn" id="uxCopyAll">Copy All</button></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Date to Timestamp</h2>
      <div class="row2"><div class="field"><label for="uxDate">Date</label><input id="uxDate" type="date" value="2026-11-09"></div><div class="field"><label for="uxTime">Time <em>24 hour</em></label><input id="uxTime" type="time" step="1" value="16:00:00"></div></div>
      ''' + F('uxDZone', 'This date and time is in', 'Asia/Kolkata', tag='select', opts=ZONES) + '''
      <div class="stats">''' + S('uxDs', 'Seconds') + S('uxDms', 'Milliseconds') + '''</div>
      <div class="kw-result" id="uxDCheck"></div>
      <div class="actions"><button type="button" class="btn dark" id="uxCopyDs">Copy Seconds</button><button type="button" class="btn" id="uxCopyDms">Copy Milliseconds</button><button type="button" class="btn" id="uxDNow">Set to Now</button></div>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Convert Many Timestamps</h2>
      ''' + F('uxBatch', 'Paste log lines, CSV rows or a list', UX_BATCH, em='the first timestamp on each line is converted, in the time zone chosen above', tag='textarea', mono=True, extra=' style="min-height:150px"') + '''
      <div class="kw-result" id="uxBCheck"></div>
      <div style="overflow-x:auto;max-height:420px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px;margin-bottom:12px"><table class="rtable" id="uxBOut"></table></div>
      <div class="actions"><button class="btn dark" id="uxBCopy">Copy as CSV</button><button class="btn" id="uxBDl">Download CSV</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var UNITS = {s: ['Seconds', 1000000000n], ms: ['Milliseconds', 1000000n], us: ['Microseconds', 1000n], ns: ['Nanoseconds', 1n]};
  var ZL = {}; Array.prototype.forEach.call($('uxZone').options, function(o){ ZL[o.value] = o.textContent; });
  var MINMS = -62135596800000, MAXMS = 253402300799999;
  function pad(n, l){ n = String(Math.abs(n)); while (n.length < (l || 2)) n = '0' + n; return n; }
  function zid(z){ if (z !== 'local') return z; try { return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC'; } catch (e){ return 'UTC'; } }
  function utc(y, mo, d, h, mi, s){ var t = new Date(Date.UTC(2000, mo - 1, d, h, mi, s)); t.setUTCFullYear(y, mo - 1, d); return t.getTime(); }
  var FC = {};
  function parts(ms, tz){
    var f = FC[tz] || (FC[tz] = new Intl.DateTimeFormat('en-US', {timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', weekday: 'long'}));
    var o = {}; f.formatToParts(new Date(ms)).forEach(function(p){ o[p.type] = p.value; });
    return {y: +o.year, mo: +o.month, d: +o.day, h: (+o.hour) % 24, mi: +o.minute, s: +o.second, wd: o.weekday};
  }
  function offMin(ms, tz){ var p = parts(ms, tz); return Math.round((utc(p.y, p.mo, p.d, p.h, p.mi, p.s) - Math.floor(ms / 1000) * 1000) / 60000); }
  function offStr(m){ return (m < 0 ? '-' : '+') + pad(Math.floor(Math.abs(m) / 60)) + ':' + pad(Math.abs(m) % 60); }
  function frac(ms, sub, u){ var f = pad(((ms % 1000) + 1000) % 1000, 3) + pad(sub, 6); var L = u === 'ms' ? 3 : u === 'us' ? 6 : u === 'ns' ? 9 : (f.replace(/0+$/, '').length ? Math.ceil(f.replace(/0+$/, '').length / 3) * 3 : 0); return L ? '.' + f.slice(0, L) : ''; }
  function isoIn(ms, tz, fr){ var p = parts(ms, tz), o = offMin(ms, tz); return pad(p.y, 4) + '-' + pad(p.mo) + '-' + pad(p.d) + 'T' + pad(p.h) + ':' + pad(p.mi) + ':' + pad(p.s) + fr + (o === 0 && tz === 'UTC' ? 'Z' : offStr(o)); }
  function human(ms, tz){
    var p = parts(ms, tz), o = offMin(ms, tz), M = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return p.wd + ', ' + p.d + ' ' + M[p.mo - 1] + ' ' + p.y + ', ' + pad(p.h) + ':' + pad(p.mi) + ':' + pad(p.s) + ' (UTC' + (o ? offStr(o) : '') + ')';
  }
  function rel(ms){
    var d = (ms - Date.now()) / 1000, a = Math.abs(d), U = [['year', 31557600], ['month', 2629800], ['week', 604800], ['day', 86400], ['hour', 3600], ['minute', 60], ['second', 1]];
    if (a < 1) return 'right now';
    for (var i = 0; i < U.length; i++) if (a >= U[i][1] || i === U.length - 1){ var n = Math.round(a / U[i][1]); var w = n + ' ' + U[i][0] + (n === 1 ? '' : 's'); return d > 0 ? 'in ' + w : w + ' ago'; }
  }
  function weekInfo(ms, tz){
    var p = parts(ms, tz), day0 = utc(p.y, p.mo, p.d, 0, 0, 0), doy = Math.round((day0 - utc(p.y, 1, 1, 0, 0, 0)) / 86400000) + 1;
    var dt = new Date(day0), wd = (dt.getUTCDay() + 6) % 7; dt.setUTCDate(dt.getUTCDate() - wd + 3);
    var fy = dt.getUTCFullYear(), w1 = new Date(utc(fy, 1, 4, 0, 0, 0)); var wk = 1 + Math.round(((dt - w1) / 86400000 - 3 + ((w1.getUTCDay() + 6) % 7)) / 7);
    return 'Day ' + doy + ' of ' + p.y + ', ISO week ' + wk + (fy !== p.y ? ' of ' + fy : '');
  }
  function readTs(raw, unit){
    var s = raw.trim().replace(/[,_\s]/g, '');
    if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
    var neg = s[0] === '-', ip = s.replace('-', '').split('.')[0], fp = s.split('.')[1] || '', L = ip.replace(/^0+/, '').length, u = unit, guessed = false;
    if (u === 'auto'){ u = L <= 11 ? 's' : L <= 14 ? 'ms' : L <= 17 ? 'us' : 'ns'; guessed = true; }
    var F = UNITS[u][1], fd = String(F).length - 1;
    var ns = BigInt(ip) * F + (fd ? BigInt((fp + '000000000').slice(0, fd)) : 0n);
    if (neg) ns = -ns;
    var q = ns / 1000000n; if (ns < 0n && q * 1000000n !== ns) q -= 1n;
    return {u: u, guessed: guessed, digits: L, ns: ns, ms: Number(q), sub: Number(ns - q * 1000000n), neg: neg};
  }
  function bigFix(ns, F){ var neg = ns < 0n, a = neg ? -ns : ns, w = a / F, r = a % F, fd = String(F).length - 1, f = fd ? pad(Number(r), fd).replace(/0+$/, '') : ''; return (neg ? '-' : '') + w.toString() + (f ? '.' + f : ''); }
  var lastIso = '', lastAll = '';
  function run(){
    var raw = $('uxIn').value, z = $('uxZone').value, tz = zid(z), t = readTs(raw, $('uxUnit').value), notes = [], cls = 'ok';
    if (!raw.trim()){ $('uxOut').innerHTML = ''; lastIso = lastAll = ''; say('uxCheck', '', 'Paste a Unix timestamp, or a date to see its timestamp.'); return; }
    if (!t){
      var pm = Date.parse(raw.trim());
      if (isNaN(pm)){ $('uxOut').innerHTML = ''; lastIso = lastAll = ''; say('uxCheck', 'bad', '<strong>This is not a timestamp or a date the tool can read.</strong> Use digits only, such as ' + c('1794220200') + ', or an ISO date such as ' + c('2026-11-09T16:00:00+05:30') + '.'); return; }
      t = {u: 'date', ms: pm, sub: 0, ns: BigInt(pm) * 1000000n};
      notes.push('Read as a date. Its Unix timestamp is <strong>' + c(bigFix(t.ns, 1000000000n).split('.')[0]) + '</strong> in seconds.' + (/[zZ]|[+-]\d\d:?\d\d$/.test(raw.trim()) || !/\d:\d/.test(raw) ? '' : ' It has no time zone, so your device time zone was used.'));
    }
    if (t.ms < MINMS || t.ms > MAXMS){ $('uxOut').innerHTML = ''; lastIso = lastAll = ''; say('uxCheck', 'bad', '<strong>This timestamp is outside the years 1 to 9999.</strong> ' + (t.u === 's' && !t.guessed ? 'It is probably in milliseconds or microseconds, so set the unit to Detect automatically.' : 'Check that no digits were added or lost when it was copied.')); return; }
    if (t.u !== 'date'){
      if (t.guessed) notes.push('Read as <strong>' + UNITS[t.u][0].toLowerCase() + '</strong> because it has ' + t.digits + ' digits.');
      var y = new Date(t.ms).getUTCFullYear();
      var au = readTs(raw, 'auto').u;
      if (!t.guessed && au !== t.u){ cls = 'warn'; notes.push('It has ' + t.digits + ' digits, which usually means ' + UNITS[au][0].toLowerCase() + ', not ' + UNITS[t.u][0].toLowerCase() + '. If the year ' + y + ' looks wrong, set the unit to Detect automatically.'); }
      if (t.neg) notes.push('It is negative, so the date is before 1 January 1970.');
      if (t.ms > 2147483647000){ notes.push('This is after 19 January 2038, 03:14:07 UTC, the largest time a signed 32 bit integer can hold. Old systems that store time that way will overflow.'); }
    }
    var fr = frac(t.ms, t.sub, t.u === 'date' ? 's' : t.u), iso = new Date(t.ms).toISOString().replace(/\.\d{3}Z$/, fr + 'Z');
    var rows = [['UTC', human(t.ms, 'UTC')], [ZL[z] + (z === 'local' ? ' (' + tz + ')' : ''), human(t.ms, tz)], ['ISO 8601 in UTC', iso], ['ISO 8601 with offset', isoIn(t.ms, tz, fr)],
      ['HTTP date (RFC 9110)', new Date(t.ms).toUTCString()], ['Relative', rel(t.ms)], ['Calendar', weekInfo(t.ms, tz)],
      ['Seconds', bigFix(t.ns, 1000000000n)], ['Milliseconds', bigFix(t.ns, 1000000n)], ['Microseconds', bigFix(t.ns, 1000n)], ['Nanoseconds', t.ns.toString()]];
    if (z === 'UTC') rows.splice(1, 1);
    $('uxOut').innerHTML = '<tbody>' + rows.map(function(r){ return '<tr><td style="width:38%"><strong>' + esc(r[0]) + '</strong></td><td class="mono" style="word-break:break-all">' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody>';
    lastIso = iso; lastAll = rows.map(function(r){ return r[0] + ': ' + r[1]; }).join('\n');
    say('uxCheck', cls, '<strong>' + esc(human(t.ms, tz)) + '</strong><br>' + notes.join(' '));
  }
  function zonedToMs(y, mo, d, h, mi, s, tz){
    var g = utc(y, mo, d, h, mi, s), o1 = offMin(g, tz), t = g - o1 * 60000, o2 = offMin(t, tz);
    if (o2 !== o1){ var t2 = g - o2 * 60000; t = offMin(t2, tz) === o2 ? t2 : g - o1 * 60000; }
    return t;
  }
  var dS = '', dMs = '';
  function runD(){
    var dv = $('uxDate').value, tv = $('uxTime').value || '00:00:00', z = $('uxDZone').value, tz = zid(z);
    var dm = dv.match(/^(\d{4,})-(\d\d)-(\d\d)$/), tm = tv.match(/^(\d\d):(\d\d)(?::(\d\d))?/);
    if (!dm || !tm){ $('uxDs').textContent = $('uxDms').textContent = '0'; dS = dMs = ''; say('uxDCheck', '', 'Pick a date and a time to get the Unix timestamp.'); return; }
    var ms = zonedToMs(+dm[1], +dm[2], +dm[3], +tm[1], +tm[2], +(tm[3] || 0), tz), p = parts(ms, tz);
    dS = String(Math.floor(ms / 1000)); dMs = String(ms);
    $('uxDs').textContent = dS; $('uxDms').textContent = dMs;
    var shift = (p.h !== +tm[1] || p.mi !== +tm[2]) ? ' That time does not exist in this zone because the clocks move forward for daylight saving, so the nearest real time was used.' : '';
    say('uxDCheck', shift ? 'warn' : 'ok', '<strong>' + esc(human(ms, tz)) + '</strong> is ' + c(new Date(ms).toISOString().replace('.000Z', 'Z')) + ' in UTC.' + shift);
  }
  var bRows = [];
  function runB(){
    var lines = $('uxBatch').value.split(/\r?\n/), z = $('uxZone').value, tz = zid(z), found = 0, h = '';
    bRows = [['Line', 'Timestamp', 'Unit', 'UTC (ISO 8601)', ZL[z].replace(/ \(.*/, '') + ' time']];
    lines.forEach(function(l, i){
      if (!l.trim()) return;
      var m = l.match(/(?:^|[^\d.])(-?\d{9,19}(?:\.\d+)?)(?![\d])/), t = m ? readTs(m[1], 'auto') : null;
      if (t && t.ms >= MINMS && t.ms <= MAXMS){
        found++;
        var fr = frac(t.ms, t.sub, t.u), r = [i + 1, m[1], UNITS[t.u][0], new Date(t.ms).toISOString().replace(/\.\d{3}Z$/, fr + 'Z'), isoIn(t.ms, tz, fr).replace('T', ' ')];
        bRows.push(r);
        h += '<tr><td class="num">' + r[0] + '</td><td class="mono">' + esc(r[1]) + '</td><td>' + r[2] + '</td><td class="mono">' + esc(r[3]) + '</td><td class="mono">' + esc(r[4]) + '</td></tr>';
      } else h += '<tr><td class="num">' + (i + 1) + '</td><td colspan="4" style="color:#777">No timestamp found in: ' + esc(l.length > 60 ? l.slice(0, 60) + '...' : l) + '</td></tr>';
    });
    $('uxBOut').innerHTML = h ? '<thead><tr>' + bRows[0].map(function(x, j){ return '<th' + (j ? '' : ' class="num"') + '>' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>' + h + '</tbody>' : '';
    say('uxBCheck', found ? 'ok' : '', found ? '<strong>Converted ' + found + ' timestamp' + (found === 1 ? '' : 's') + '.</strong> Each unit was detected from the number of digits.' : 'Paste lines that contain Unix timestamps of 9 to 19 digits.');
  }
  function csv(){ return bRows.length > 1 ? bRows.map(function(r){ return r.map(function(v){ v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(','); }).join('\r\n') + '\r\n' : ''; }
  function tick(){ var n = Date.now(); $('uxNowS').textContent = Math.floor(n / 1000); $('uxNowMs').textContent = n; $('uxNowIso').innerHTML = 'Right now it is ' + c(new Date(n).toISOString().replace(/\.\d{3}Z/, 'Z')) + ' in UTC, which is ' + esc(human(n, zid($('uxZone').value))) + ' in ' + esc(ZL[$('uxZone').value]) + '.'; }
  var tmr; $('uxIn').addEventListener('input', function(){ clearTimeout(tmr); tmr = setTimeout(run, 60); });
  $('uxUnit').addEventListener('change', run);
  $('uxZone').addEventListener('change', function(){ run(); runB(); tick(); });
  ['uxDate', 'uxTime'].forEach(function(id){ $(id).addEventListener('input', runD); $(id).addEventListener('change', runD); });
  $('uxDZone').addEventListener('change', runD);
  var tb; $('uxBatch').addEventListener('input', function(){ clearTimeout(tb); tb = setTimeout(runB, 120); });
  $('uxCopyNowS').addEventListener('click', function(){ copyText(String(Math.floor(Date.now() / 1000)), 'toast'); });
  $('uxCopyNowMs').addEventListener('click', function(){ copyText(String(Date.now()), 'toast'); });
  $('uxUseNow').addEventListener('click', function(){ $('uxIn').value = Math.floor(Date.now() / 1000); $('uxUnit').value = 'auto'; run(); });
  $('uxCopyIso').addEventListener('click', function(){ run(); if (lastIso) copyText(lastIso, 'toast'); });
  $('uxCopyAll').addEventListener('click', function(){ run(); if (lastAll) copyText(lastAll, 'toast'); });
  $('uxCopyDs').addEventListener('click', function(){ runD(); if (dS) copyText(dS, 'toast'); });
  $('uxCopyDms').addEventListener('click', function(){ runD(); if (dMs) copyText(dMs, 'toast'); });
  $('uxDNow').addEventListener('click', function(){ var p = parts(Date.now(), zid($('uxDZone').value)); $('uxDate').value = pad(p.y, 4) + '-' + pad(p.mo) + '-' + pad(p.d); $('uxTime').value = pad(p.h) + ':' + pad(p.mi) + ':' + pad(p.s); runD(); });
  $('uxBCopy').addEventListener('click', function(){ runB(); var t = csv(); if (t) copyText(t, 'toast'); });
  $('uxBDl').addEventListener('click', function(){ runB(); var t = csv(); if (t) download('timestamps.csv', t, 'text/csv'); });
  tick(); setInterval(tick, 1000); run(); runD(); runB();
''',
        content=f'''
    <h2>What Is a Unix Timestamp?</h2>
    <p>A Unix timestamp, also called epoch time or POSIX time, is the number of seconds that have passed since 1 January 1970 at 00:00:00 UTC. That moment is called the Unix epoch. Because it is just one number with no time zone, servers, databases, APIs and analytics tools use it everywhere to store dates.</p>
    <p>The catch is that people cannot read it, and different systems use different units. PHP and most server logs count seconds, JavaScript counts milliseconds, and the Google Analytics export to BigQuery stores <code>event_timestamp</code> in microseconds. This converter detects the unit from the number of digits, shows the date in UTC and your chosen time zone, and runs entirely in your browser.</p>

    <h2>How to Use the Unix Timestamp Converter</h2>
    <ol>
      <li><strong>Paste a timestamp</strong> into Timestamp to Date. The unit is detected for you, or you can set it by hand.</li>
      <li><strong>Pick a time zone,</strong> such as India (IST) or New York. You see the date in UTC and in that zone, plus ISO 8601, the HTTP date format and how long ago it was.</li>
      <li><strong>Go the other way</strong> with Date to Timestamp. Choose a date, a time and the zone it belongs to, then copy the seconds or milliseconds.</li>
      <li><strong>Convert a whole log</strong> by pasting lines into Convert Many Timestamps. The first timestamp on each line is converted, and you can download the result as a CSV.</li>
    </ol>

    <h2>How Many Digits? Seconds, Milliseconds and More</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Digits today', 'Unit', 'Where you see it')}
      <tbody>
        <tr><td>10</td><td>Seconds</td><td>PHP <code>time()</code>, Unix and server logs, JWT <code>exp</code> and <code>iat</code> claims, most APIs</td></tr>
        <tr><td>13</td><td>Milliseconds</td><td>JavaScript <code>Date.now()</code>, Java, many tracking and ad platform exports</td></tr>
        <tr><td>16</td><td>Microseconds</td><td>GA4 BigQuery <code>event_timestamp</code>, some database and Python tools</td></tr>
        <tr><td>19</td><td>Nanoseconds</td><td>Go <code>UnixNano()</code>, InfluxDB and other monitoring tools</td></tr>
      </tbody>
    </table></div>
    <p>JavaScript dates work in milliseconds, as explained in the <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date" {EXT}>MDN Date reference</a>, while the <a href="https://support.google.com/analytics/answer/7029846" {EXT}>GA4 BigQuery export schema</a> lists event times in microseconds, UTC.</p>

    <h2>Get the Current Timestamp in Code</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Language or tool', 'Code')}
      <tbody>
        <tr><td>JavaScript</td><td><code>Math.floor(Date.now() / 1000)</code></td></tr>
        <tr><td>Python</td><td><code>int(time.time())</code></td></tr>
        <tr><td>PHP</td><td><code>time()</code></td></tr>
        <tr><td>MySQL</td><td><code>SELECT UNIX_TIMESTAMP();</code></td></tr>
        <tr><td>Linux or Mac terminal</td><td><code>date +%s</code></td></tr>
        <tr><td>Excel or Google Sheets</td><td><code>=A1/86400+DATE(1970,1,1)</code> turns seconds in A1 into a date</td></tr>
      </tbody>
    </table></div>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Store UTC, show local.</strong> Keep timestamps in UTC in your database and only convert to IST or another zone when you display them.</li>
      <li><strong>A date in 1970 means the wrong unit.</strong> If seconds are read as milliseconds you land in January 1970, and the reverse gives a year far in the future.</li>
      <li><strong>Watch out for 2038.</strong> Systems that store time as a signed 32 bit number stop at 19 January 2038, 03:14:07 UTC. The tool warns you when a date is past that point.</li>
      <li><strong>Check AI written code.</strong> AI assistants often mix up seconds and milliseconds. Paste the value your code produces here to confirm it is the date you expect.</li>
    </ul>

    <h2>Work With Time in Your Projects</h2>
    <p>Scheduling scripts? Read <a href="{B}php-cron-jobs/">how to set up PHP cron jobs</a>, then learn to read crawl times in <a href="{B}python-log-file-analysis-googlebot-crawl-behavior/">Python log file analysis for Googlebot</a> and keep errors traceable with <a href="{B}php-error-logging-and-monitoring/">PHP error logging and monitoring</a>. Checking when a login token expires? Paste it into the <a href="{T}base64-encoder-decoder/">Base64 and JWT decoder</a>.</p>
''',
        faqs=[
            ("What is a Unix timestamp?", "It is the number of seconds since 1 January 1970 at 00:00:00 UTC, called the Unix epoch. It has no time zone, so the same timestamp means the same moment everywhere. Some systems count milliseconds or microseconds instead of seconds."),
            ("How do I convert a Unix timestamp to a date in Excel or Google Sheets?", "Use =A1/86400+DATE(1970,1,1) and format the cell as a date and time. The result is in UTC. For India time add 5.5/24, and if the timestamp is in milliseconds divide by 86400000 instead of 86400."),
            ("Why does my timestamp show a date in 1970 or thousands of years from now?", "The unit is wrong. A millisecond value read as seconds lands far in the future, and a seconds value read as milliseconds lands in January 1970. Count the digits: 10 is seconds, 13 is milliseconds and 16 is microseconds."),
            ("What is the Year 2038 problem?", "Systems that store Unix time as a signed 32 bit integer can only count up to 2147483647, which is 19 January 2038 at 03:14:07 UTC. After that the number overflows. Modern systems use 64 bit time, which lasts for billions of years."),
        ],
        related=[("PHP Cron Jobs", "php-cron-jobs"), ("Python Log File Analysis for Googlebot", "python-log-file-analysis-googlebot-crawl-behavior"),
                 ("PHP Error Logging and Monitoring", "php-error-logging-and-monitoring"), ("Search Console Data Pulls With Python", "google-search-console-data-pulls-with-python")],
    ))

    # ---------- 6. CSV TO JSON CONVERTER ----------
    CJ_CSV = ('order_id,product,price,qty,paid,city,coupon\n'
              '00981,"Organic Green Tea, 100 Bags",349.00,2,true,Pune,\n'
              '00982,"Masala Chai ""Strong"" Blend",299,1,false,Mumbai,DIWALI10\n'
              '00983,Tulsi Honey Infusion,425.50,3,TRUE,"New Delhi",\n'
              '00984,"Gift Box\nwith 4 teas",1199,1,true,Bengaluru,FESTIVE')
    CJ_JSON = ('{\n  "status": "ok",\n  "results": [\n'
               '    {"id": 101, "page": "/blog/what-is-seo/", "clicks": 412, "ctr": 0.054, "author": {"name": "Priya", "team": "SEO"}, "tags": ["seo", "basics"]},\n'
               '    {"id": 102, "page": "/blog/utm-guide/", "clicks": 268, "ctr": 0.031, "author": {"name": "Rahul", "team": "Analytics"}, "tags": ["ga4"]},\n'
               '    {"id": 103, "page": "/tools/", "clicks": 95, "ctr": 0.022, "author": {"name": "Asha", "team": "Content"}, "tags": [], "note": "Has a comma, and \\"quotes\\""}\n'
               '  ]\n}')
    TOOLS.append(dict(
        slug='csv-to-json-converter', short='CJ', name='CSV to JSON Converter',
        card='Convert CSV to JSON or JSON Lines, and JSON back to an Excel ready CSV, with quotes, nested data and big IDs handled correctly.',
        title='CSV to JSON Converter: Convert CSV and JSON Both Ways',
        desc='Free CSV to JSON converter. Turn CSV or Excel exports into JSON, JSON Lines for AI batch files, or nested objects, and convert JSON back to CSV for Excel.',
        h1='CSV to JSON Converter',
        lead='Paste or upload a CSV and get clean JSON in a second, as an array of objects, JSON Lines or nested data. Switch to JSON to CSV to flatten API responses into a spreadsheet that opens properly in Excel. Quotes, commas inside fields and long IDs are all handled the right way.',
        tool='''<section class="tool" aria-label="CSV to JSON converter" id="cjForm">
    <div class="card" style="min-width:0">
      <h2>Input</h2>
      <div class="tabs" id="cjTabs"><button type="button" data-m="c2j" class="on">CSV to JSON</button><button type="button" data-m="j2c">JSON to CSV</button></div>
      ''' + F('cjIn', 'CSV data', CJ_CSV, em='paste, or choose a file below', tag='textarea', mono=True, extra=' style="min-height:210px"') + '''
      <div class="field"><label for="cjFile">Or open a file <em>.csv, .tsv, .txt, .json or .jsonl, it stays on your device</em></label><input id="cjFile" type="file" accept=".csv,.tsv,.txt,.json,.jsonl,.ndjson,text/csv,application/json"></div>
      <div id="cjC2J">
        <div class="row2">''' + F('cjDelim', 'Delimiter', 'auto', tag='select', opts=[('auto', 'Detect automatically'), (',', 'Comma ,'), (';', 'Semicolon ;'), ('\\t', 'Tab'), ('|', 'Pipe |')]) + F('cjFmt', 'Output format', 'objects', tag='select', opts=[('objects', 'Array of objects'), ('jsonl', 'JSON Lines (.jsonl)'), ('arrays', 'Array of arrays'), ('keyed', 'Object keyed by first column')]) + '''</div>
        <div class="row2">''' + F('cjIndent', 'Indent', '2', tag='select', opts=[('2', '2 spaces'), ('4', '4 spaces'), ('t', 'Tabs'), ('0', 'Minified, one line')]) + '''<div></div></div>
        <div style="margin:0 0 8px">''' + CK('cjHead', 'First row is the header', True) + CK('cjTypes', 'Turn numbers and true or false into real values (leading zeros and long IDs stay text)', True) + CK('cjNest', 'Make nested objects from dotted headers such as <code>author.name</code>', False) + CK('cjTrim', 'Trim spaces around values', True) + CK('cjSkip', 'Skip empty rows', True) + '''</div>
      </div>
      <div id="cjJ2C" style="display:none">
        <div class="row2">''' + F('cjOutDelim', 'Delimiter', ',', tag='select', opts=[(',', 'Comma ,'), (';', 'Semicolon ; for European Excel'), ('\\t', 'Tab'), ('|', 'Pipe |')]) + '<div></div></div>' + '''
        <div style="margin:0 0 8px">''' + CK('cjFlat', 'Flatten nested objects into columns such as <code>author.name</code>', True) + CK('cjBom', 'Add a byte order mark to the download so Excel shows ₹ and Indian scripts correctly', True) + CK('cjSafe', 'Protect against spreadsheet formulas (cells starting with = + @)', False) + CK('cjQuote', 'Wrap every value in quotes', False) + '''</div>
      </div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('cjRows', 'Rows') + S('cjCols', 'Columns') + S('cjInSize', 'Input') + S('cjOutSize', 'Output') + '''</div>
      <div class="kw-result" id="cjCheck"></div>
      <div id="cjPrev" style="overflow-x:auto;max-height:260px;overflow-y:auto;border:1px solid #e6e6e6;border-radius:10px;margin-bottom:12px"></div>
      <pre class="code-out" id="cjOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="cjCopy">Copy Result</button><button class="btn" id="cjDl">Download</button><button class="btn" id="cjSwap">Use Result as Input</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var mode = 'c2j', out = '', SAMPLES = {c2j: $('cjIn').value, j2c: ''' + json.dumps(CJ_JSON) + r'''};
  var DN = {',': 'comma', ';': 'semicolon', '\t': 'tab', '|': 'pipe'};
  function dval(v){ return v === '\\t' ? '\t' : v; }
  function parseCSV(text, d, limit){
    var rows = [], lines = [], row = [], f = '', i = 0, q = false, n = text.length, line = 1, start = 1, qs = 0, ch;
    while (i < n){
      ch = text[i];
      if (q){
        if (ch === '"'){ if (text[i + 1] === '"'){ f += '"'; i += 2; continue; } q = false; i++; continue; }
        if (ch === '\n') line++;
        f += ch; i++; continue;
      }
      if (ch === '"' && f.trim() === ''){ f = ''; q = true; qs = line; i++; continue; }
      if (ch === d){ row.push(f); f = ''; i++; continue; }
      if (ch === '\r' || ch === '\n'){
        row.push(f); rows.push(row); lines.push(start); row = []; f = '';
        if (ch === '\r' && text[i + 1] === '\n') i++;
        i++; line++; start = line;
        if (limit && rows.length >= limit) return {rows: rows, lines: lines};
        continue;
      }
      f += ch; i++;
    }
    if (q) return {err: 'A quoted value that starts on line ' + qs + ' is never closed. Add the missing closing " mark, or check for a stray quote on that line.'};
    if (f !== '' || row.length){ row.push(f); rows.push(row); lines.push(start); }
    return {rows: rows, lines: lines};
  }
  function detect(text){
    var best = ',', bs = -1;
    [',', ';', '\t', '|'].forEach(function(d){
      var r = parseCSV(text.slice(0, 30000), d, 25); if (r.err || !r.rows.length) return;
      var rs = r.rows.length > 2 ? r.rows.slice(0, -1) : r.rows, c0 = rs[0].length;
      if (c0 < 2) return;
      var same = rs.filter(function(x){ return x.length === c0; }).length / rs.length, s = same * 100 + c0;
      if (s > bs){ bs = s; best = d; }
    });
    return best;
  }
  function conv(v, types){
    if (!types) return v;
    if (/^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$/.test(v)){ var x = Number(v); if (isFinite(x) && (/[.eE]/.test(v) || Number.isSafeInteger(x))) return x; return v; }
    var l = v.toLowerCase(); if (l === 'true') return true; if (l === 'false') return false; if (l === 'null') return null;
    return v;
  }
  function setPath(o, key){
    var p = key.split('.'); if (p.some(function(x){ return x === ''; })) return false;
    var cur = o;
    for (var i = 0; i < p.length - 1; i++){
      if (cur[p[i]] === undefined) cur[p[i]] = {};
      else if (typeof cur[p[i]] !== 'object' || cur[p[i]] === null || Array.isArray(cur[p[i]])) return false;
      cur = cur[p[i]];
    }
    if (cur[p[p.length - 1]] !== undefined && typeof cur[p[p.length - 1]] === 'object') return false;
    return {o: cur, k: p[p.length - 1]};
  }
  function preview(head, rows){
    if (!rows.length){ $('cjPrev').innerHTML = ''; $('cjPrev').style.display = 'none'; return; }
    $('cjPrev').style.display = '';
    var hs = head.slice(0, 12);
    $('cjPrev').innerHTML = '<table class="rtable"><thead><tr>' + hs.map(function(h){ return '<th>' + esc(h) + '</th>'; }).join('') + (head.length > 12 ? '<th>+' + (head.length - 12) + ' more</th>' : '') + '</tr></thead><tbody>'
      + rows.slice(0, 8).map(function(r){ return '<tr>' + hs.map(function(h, j){ var v = r[j]; return '<td style="white-space:nowrap;max-width:280px;overflow:hidden;text-overflow:ellipsis">' + esc(v === undefined || v === null ? '' : String(v)).replace(/\n/g, ' ') + '</td>'; }).join('') + (head.length > 12 ? '<td></td>' : '') + '</tr>'; }).join('')
      + (rows.length > 8 ? '<tr><td colspan="' + (hs.length + (head.length > 12 ? 1 : 0)) + '" style="color:#777">Showing 8 of ' + fmtN(rows.length) + ' rows</td></tr>' : '') + '</tbody></table>';
  }
  function stats(r, cn, inS, outS){ $('cjRows').textContent = fmtN(r); $('cjCols').textContent = fmtN(cn); $('cjInSize').textContent = fmtB(inS); $('cjOutSize').textContent = fmtB(outS); }
  function fail(msg){ out = ''; $('cjOut').textContent = ''; preview([], []); stats(0, 0, bytes($('cjIn').value), 0); say('cjCheck', 'bad', msg); }
  function c2j(text){
    text = text.replace(/^\uFEFF/, '');
    var dsel = $('cjDelim').value, d = dsel === 'auto' ? detect(text) : dval(dsel), p = parseCSV(text, d), notes = [];
    if (p.err) return fail('<strong>The CSV could not be read.</strong> ' + esc(p.err));
    var trim = $('cjTrim').checked, types = $('cjTypes').checked, rows = [], lines = [];
    p.rows.forEach(function(r, i){
      if (trim) r = r.map(function(v){ return v.trim(); });
      if ($('cjSkip').checked && r.every(function(v){ return v === ''; })) return;
      rows.push(r); lines.push(p.lines[i]);
    });
    if (!rows.length) return fail('<strong>No rows found.</strong> Paste CSV data with one record per line.');
    var head = [], body = rows, hasHead = $('cjHead').checked;
    if (hasHead){ head = rows[0].slice(); body = rows.slice(1); lines = lines.slice(1); }
    var width = Math.max.apply(null, rows.map(function(r){ return r.length; })), seen = {}, renamed = 0;
    for (var j = 0; j < width; j++){
      var h = head[j] || ''; if (!h) h = 'column_' + (j + 1);
      if (seen[h]){ var k = 2; while (seen[h + '_' + k]) k++; h = h + '_' + k; renamed++; }
      seen[h] = 1; head[j] = h;
    }
    var odd = [], w0 = hasHead ? rows[0].length : (body[0] || []).length;
    body.forEach(function(r, i){ if (r.length !== w0) odd.push(lines[i]); });
    var fmt = $('cjFmt').value, ind = $('cjIndent').value, sp = ind === 't' ? '\t' : +ind, nest = $('cjNest').checked, flatKeys = 0, kept = 0;
    function cell(v){ var x = conv(v, types); if (types && typeof x === 'string' && /^-?\d+(\.\d+)?$/.test(x) && x !== '') kept++; return x; }
    var objs = body.map(function(r){
      var o = {};
      head.forEach(function(h, j){
        var v = cell(r[j] === undefined ? '' : r[j]);
        if (nest && h.indexOf('.') > 0){ var t = setPath(o, h); if (t){ t.o[t.k] = v; return; } flatKeys++; }
        o[h] = v;
      });
      return o;
    });
    var data;
    if (fmt === 'arrays'){ data = body.map(function(r){ return head.map(function(h, j){ return cell(r[j] === undefined ? '' : r[j]); }); }); if (hasHead) data.unshift(head); }
    else if (fmt === 'keyed'){
      data = {}; var dup = 0;
      objs.forEach(function(o, i){ var key = String(body[i][0] === undefined ? '' : body[i][0]); if (data.hasOwnProperty(key)) dup++; data[key] = o; });
      if (dup) notes.push(dup + ' row' + (dup === 1 ? ' has' : 's have') + ' a first column value that repeats, so later rows replaced earlier ones.');
    } else data = objs;
    out = fmt === 'jsonl' ? objs.map(function(o){ return JSON.stringify(o); }).join('\n') + (objs.length ? '\n' : '') : JSON.stringify(data, null, sp);
    $('cjOut').textContent = out.length > 200000 ? out.slice(0, 200000) + '\n... preview cut at 200 KB, copy or download for the full result' : out;
    preview(head, body.map(function(r){ return head.map(function(h, j){ return r[j]; }); }));
    stats(body.length, head.length, bytes(text), bytes(out));
    if (dsel === 'auto') notes.unshift('Delimiter detected: ' + DN[d] + '.');
    if (odd.length) notes.push(odd.length + ' row' + (odd.length === 1 ? '' : 's') + ' (line ' + odd.slice(0, 5).join(', ') + (odd.length > 5 ? ' and more' : '') + ') ' + (odd.length === 1 ? 'has' : 'have') + ' a different number of values than the header. Missing values were left empty.');
    if (renamed) notes.push(renamed + ' repeated or empty column name' + (renamed === 1 ? ' was' : 's were') + ' renamed so no data is lost.');
    if (kept) notes.push(fmtN(kept) + ' value' + (kept === 1 ? '' : 's') + ' with leading zeros or more than 15 digits stayed as text, so IDs, PIN codes and phone numbers are not changed.');
    if (flatKeys) notes.push('Some dotted headers clash with other columns, so they were kept as flat keys.');
    if (fmt === 'jsonl') notes.push('Each line is one JSON object, the format used by AI batch and fine tuning files and by BigQuery imports.');
    say('cjCheck', odd.length ? 'warn' : 'ok', '<strong>Converted ' + fmtN(body.length) + ' row' + (body.length === 1 ? '' : 's') + ' and ' + head.length + ' column' + (head.length === 1 ? '' : 's') + ' to ' + (fmt === 'jsonl' ? 'JSON Lines' : 'JSON') + '.</strong> ' + notes.join(' '));
  }
  function parseJ(t){
    t = t.replace(/^\uFEFF/, '').trim();
    try { return {v: JSON.parse(t)}; } catch (e){
      var ls = t.split(/\r?\n/).filter(function(l){ return l.trim(); }), first = null;
      if (ls.length > 1){ try { first = JSON.parse(ls[0]); } catch (e3){} }
      if (first !== null && typeof first === 'object'){
        var arr = [];
        for (var i = 0; i < ls.length; i++){ try { arr.push(JSON.parse(ls[i])); } catch (e2){ return {err: 'This looks like JSON Lines, but line ' + (i + 1) + ' is not valid JSON: ' + e2.message}; } }
        return {v: arr, jsonl: true};
      }
      return {err: e.message};
    }
  }
  function isObj(x){ return x !== null && typeof x === 'object' && !Array.isArray(x); }
  function flatten(o, pre, acc, flat){
    Object.keys(o).forEach(function(k){
      var v = o[k], key = pre + k;
      if (isObj(v) && flat && Object.keys(v).length) flatten(v, key + '.', acc, flat);
      else if (Array.isArray(v)) acc[key] = flat && v.every(function(x){ return x === null || typeof x !== 'object'; }) ? v.map(function(x){ return x === null ? '' : String(x); }).join('; ') : (v.length ? JSON.stringify(v) : '');
      else if (isObj(v)) acc[key] = Object.keys(v).length ? JSON.stringify(v) : '';
      else acc[key] = v;
    });
    return acc;
  }
  function j2c(text){
    var p = parseJ(text), notes = [];
    if (p.err) return fail('<strong>The JSON is not valid.</strong> ' + esc(p.err) + ' Fix it in the <a href="https://brandella.in/tools/developer-tools/json-formatter/">JSON formatter</a>, which points to the exact error.');
    var v = p.v, rows, from = '';
    if (Array.isArray(v)) rows = v;
    else if (isObj(v)){
      var ks = Object.keys(v);
      for (var i = 0; i < ks.length; i++){ var a = v[ks[i]]; if (Array.isArray(a) && a.length && a.every(isObj)){ rows = a; from = ks[i]; break; } }
      if (!rows) rows = [v];
    } else rows = [v];
    var d = dval($('cjOutDelim').value), flat = $('cjFlat').checked, safe = $('cjSafe').checked, qa = $('cjQuote').checked, head = [], seen = {}, recs, raw = false;
    if (rows.length && rows.every(Array.isArray)){ raw = true; recs = rows; var w = Math.max.apply(null, rows.map(function(r){ return r.length; })); for (var j = 0; j < w; j++) head.push(String(j + 1)); }
    else {
      recs = rows.map(function(r){ return isObj(r) ? flatten(r, '', {}, flat) : {value: r}; });
      recs.forEach(function(r){ Object.keys(r).forEach(function(k){ if (!seen[k]){ seen[k] = 1; head.push(k); } }); });
    }
    var guarded = 0;
    function cell(x){
      var s = x === null || x === undefined ? '' : (typeof x === 'object' ? JSON.stringify(x) : String(x));
      if (safe && typeof x === 'string' && /^[=+\-@\t\r]/.test(s) && !/^[+-]?\d+(\.\d+)?$/.test(s)){ s = "'" + s; guarded++; }
      return (qa || s.indexOf(d) >= 0 || /["\r\n]/.test(s) || /^\s|\s$/.test(s)) ? '"' + s.replace(/"/g, '""') + '"' : s;
    }
    var grid = raw ? recs : recs.map(function(r){ return head.map(function(h){ return r[h]; }); });
    var lines = raw ? [] : [head.map(cell).join(d)];
    grid.forEach(function(r){ lines.push(r.map(cell).join(d)); });
    out = lines.join('\r\n') + '\r\n';
    $('cjOut').textContent = out.length > 200000 ? out.slice(0, 200000) + '\n... preview cut at 200 KB, copy or download for the full result' : out;
    preview(head, grid);
    stats(grid.length, head.length, bytes(text), bytes(out));
    if (p.jsonl) notes.push('Read as JSON Lines, one record per line.');
    if (from) notes.push('The records were found in the ' + c(from) + ' list of the response.');
    if (raw) notes.push('The input is a list of lists, so each inner list became one row with no header.');
    if (flat) notes.push('Nested objects became dotted columns, and simple lists were joined with semicolons.');
    if (guarded) notes.push(guarded + ' cell' + (guarded === 1 ? ' was' : 's were') + ' prefixed with an apostrophe so Excel will not run ' + (guarded === 1 ? 'it' : 'them') + ' as a formula.');
    say('cjCheck', 'ok', '<strong>Converted ' + fmtN(grid.length) + ' record' + (grid.length === 1 ? '' : 's') + ' into ' + head.length + ' CSV column' + (head.length === 1 ? '' : 's') + '.</strong> ' + notes.join(' '));
  }
  function run(){
    var t = $('cjIn').value;
    if (!t.trim()){ out = ''; $('cjOut').textContent = ''; preview([], []); stats(0, 0, 0, 0); say('cjCheck', '', mode === 'c2j' ? 'Paste CSV data or open a CSV file to convert it to JSON.' : 'Paste JSON or JSON Lines to convert it to CSV.'); return; }
    if (mode === 'c2j') c2j(t); else j2c(t);
  }
  function setMode(m, keep){
    if (!keep && $('cjIn').value === SAMPLES[mode]) $('cjIn').value = SAMPLES[m];
    mode = m;
    $('cjTabs').querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x.getAttribute('data-m') === m); });
    $('cjC2J').style.display = m === 'c2j' ? '' : 'none'; $('cjJ2C').style.display = m === 'j2c' ? '' : 'none';
    document.querySelector('label[for="cjIn"]').firstChild.textContent = m === 'c2j' ? 'CSV data ' : 'JSON or JSON Lines ';
    run();
  }
  $('cjTabs').querySelectorAll('button').forEach(function(b){ b.addEventListener('click', function(){ setMode(b.getAttribute('data-m')); }); });
  var tm; $('cjIn').addEventListener('input', function(){ clearTimeout(tm); tm = setTimeout(run, $('cjIn').value.length > 200000 ? 400 : 80); });
  ['cjDelim', 'cjFmt', 'cjIndent', 'cjHead', 'cjTypes', 'cjNest', 'cjTrim', 'cjSkip', 'cjOutDelim', 'cjFlat', 'cjBom', 'cjSafe', 'cjQuote'].forEach(function(id){ $(id).addEventListener('change', run); });
  $('cjFile').addEventListener('change', function(){
    var f = this.files && this.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function(){ $('cjIn').value = r.result; var js = /\.(json|jsonl|ndjson)$/i.test(f.name) || /^\s*[\[{]/.test(r.result); setMode(js ? 'j2c' : 'c2j', true); if (/\.tsv$/i.test(f.name) && !js){ $('cjDelim').value = '\\t'; run(); } };
    r.readAsText(f);
  });
  $('cjCopy').addEventListener('click', function(){ run(); if (out) copyText(out, 'toast'); });
  $('cjDl').addEventListener('click', function(){
    run(); if (!out) return;
    if (mode === 'j2c') download('data.csv', ($('cjBom').checked ? '\uFEFF' : '') + out, 'text/csv');
    else download($('cjFmt').value === 'jsonl' ? 'data.jsonl' : 'data.json', out, $('cjFmt').value === 'jsonl' ? 'application/jsonl' : 'application/json');
  });
  $('cjSwap').addEventListener('click', function(){
    run(); if (!out) return;
    var next = mode === 'c2j' ? 'j2c' : 'c2j';
    $('cjIn').value = out; if (next === 'c2j') $('cjDelim').value = 'auto';
    setMode(next, true);
  });
  run();
''',
        content=f'''
    <h2>What Is a CSV to JSON Converter?</h2>
    <p>CSV is the format spreadsheets, Search Console, Google Ads and almost every CRM export. JSON is the format APIs, JavaScript, databases and AI tools expect. A CSV to JSON converter turns each spreadsheet row into a JSON object, using the header row for the keys, so you can feed your data into code, a website or an AI workflow without writing a script.</p>
    <p>This tool works both ways. It follows <a href="https://www.rfc-editor.org/rfc/rfc4180" {EXT}>RFC 4180</a>, the CSV standard, so commas, quotes and even line breaks inside a field are read correctly. It also turns JSON from an API back into a CSV that opens cleanly in Excel or Google Sheets. Everything runs in your browser, so customer lists and sales data never leave your device.</p>

    <h2>How to Use the CSV to JSON Converter</h2>
    <ol>
      <li><strong>Paste your CSV</strong> or open a file. The delimiter, whether comma, semicolon, tab or pipe, is detected for you.</li>
      <li><strong>Pick an output format,</strong> such as an array of objects for code or JSON Lines for AI batch files and BigQuery.</li>
      <li><strong>Check the preview table</strong> to confirm the columns lined up, and read any notes about rows with missing values.</li>
      <li><strong>Copy or download</strong> the JSON. To go back, open JSON to CSV, paste an API response and download a CSV for Excel.</li>
    </ol>

    <h2>Which Output Format Should You Choose?</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Format', 'Looks like', 'Best for')}
      <tbody>
        <tr><td>Array of objects</td><td><code>[{{"name": "Priya", "city": "Pune"}}]</code></td><td>APIs, JavaScript, website data, most code</td></tr>
        <tr><td>JSON Lines</td><td>One object per line, no outer brackets</td><td>AI batch and fine tuning files, BigQuery imports, logs and very large data</td></tr>
        <tr><td>Array of arrays</td><td><code>[["name", "city"], ["Priya", "Pune"]]</code></td><td>Charts, tables and the smallest possible file</td></tr>
        <tr><td>Keyed object</td><td><code>{{"00981": {{...}}}}</code></td><td>Quick lookups by an ID or SKU in the first column</td></tr>
      </tbody>
    </table></div>
    <p><a href="https://jsonlines.org/" {EXT}>JSON Lines</a> puts one complete JSON value on each line. Tools such as the OpenAI Batch API and BigQuery read it line by line, which is why it is the usual format for large AI and analytics jobs.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>IDs stay safe.</strong> Values with leading zeros, such as <code>00981</code>, and numbers longer than JavaScript can hold exactly stay as text, so order IDs, PIN codes and phone numbers are never changed.</li>
      <li><strong>European Excel uses semicolons.</strong> If a CSV from a colleague abroad shows everything in one column, the tool still detects the semicolon. Choose semicolon when you export for them too.</li>
      <li><strong>Keep the byte order mark on</strong> when you download a CSV for Excel. Without it Excel can show ₹ and Hindi or Marathi text as garbled characters.</li>
      <li><strong>Protect shared exports.</strong> Turn on formula protection when the data came from users, such as form entries, so a cell like <code>=HYPERLINK(...)</code> cannot run in someone's spreadsheet.</li>
    </ul>

    <h2>Put Your Data to Work</h2>
    <p>Want to go further with exports? Read <a href="{B}python-and-pandas-seo-reporting/">Python and pandas for SEO reporting</a>, learn <a href="{B}google-search-console-data-pulls-with-python/">how to pull Search Console data with Python</a>, or serve your JSON with <a href="{B}rest-api-in-php-without-a-framework/">a simple REST API in PHP</a>. Need to read or fix the JSON first? Open it in the <a href="{T}json-formatter/">JSON formatter and validator</a>.</p>
''',
        faqs=[
            ("How do I convert a CSV file to JSON?", "Paste the CSV or open the file, keep First row is the header ticked, and the tool turns every row into a JSON object with the header names as keys. Choose the output format and indent, then copy the JSON or download it as a file."),
            ("How do I convert JSON to CSV for Excel?", "Open JSON to CSV and paste your JSON, an API response or JSON Lines. Nested objects become columns such as author.name, and the download includes a byte order mark so Excel shows every character correctly. Choose semicolon if your Excel uses European settings."),
            ("Why are some numbers kept as text in the JSON?", "Numbers with leading zeros, such as 00981, would lose the zeros, and whole numbers above 9007199254740991 would lose digits in JavaScript. The tool keeps them as text so IDs, PIN codes and phone numbers stay exactly as they were."),
            ("What is JSON Lines and when should I use it?", "JSON Lines, also called JSONL or NDJSON, puts one JSON object on each line with no surrounding brackets. Use it for AI batch and fine tuning files, BigQuery imports and very large exports, because tools can read it one line at a time."),
        ],
        related=[("Python and Pandas SEO Reporting", "python-and-pandas-seo-reporting"), ("Search Console Data Pulls With Python", "google-search-console-data-pulls-with-python"),
                 ("REST API in PHP Without a Framework", "rest-api-in-php-without-a-framework"), ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'developer-tools'; t['updated'] = '2026-11-09'
