"""Batch 24 (2026-11-21): Business Calculators category, first tool (GST Calculator).
Search demand: "gst calculator" is one of the most searched calculator queries in India; ClearTax, Tally,
Razorpay, Bajaj Finserv, Vyapar and others rank for it. Not covered by any existing tool.
Facts checked 2026-11-21: GST 2.0 (56th GST Council, effective 22 September 2025): main slabs 5% and 18%,
special 40% rate for sin and luxury goods, 12% and 28% slabs removed for most items; 3% gold and silver,
0.25% rough precious stones unchanged. Intra state supply = CGST + SGST (or UTGST) split equally,
inter state = IGST. Digital ads billed in India (Google Ads, Meta) carry 18% GST.
Runs fully in the browser: add or remove GST, CGST/SGST/IGST split, rate comparison, multi item invoice with
rate wise tax summary, round off, amount in words (Indian numbering) and CSV download."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/business-calculators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

RATES = ['0', '0.25', '3', '5', '18', '40', '12', '28']
CHIPS = ''.join(f'<button type="button" class="btn btn-sm{" dark" if r == "18" else ""}" data-r="{r}">{r}%</button>' for r in RATES)


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='gst-calculator', short='GST', name='GST Calculator',
        card='Add or remove GST at any rate, split it into CGST, SGST or IGST, and total a full invoice with a rate wise tax summary.',
        title='GST Calculator: Add or Remove GST, CGST, SGST, IGST',
        desc='Free GST calculator for India with the new 5%, 18% and 40% rates. Add or remove GST, split CGST, SGST and IGST, and total a multi item invoice.',
        h1='GST Calculator',
        lead='Work out GST on any price in seconds. Add GST to a base price or take it out of a total, see the CGST, SGST or IGST split, and total a full invoice with several items and rates.',
        tool='''<section class="tool" aria-label="GST calculator" id="gsForm">
    <div class="card" style="min-width:0">
      <div class="tabs" id="gsTabs" role="tablist"><button type="button" data-t="quick" class="on">Quick Calculator</button><button type="button" data-t="inv">Invoice With Items</button></div>
      <div id="gsQuick">
        <h2>Price and Rate</h2>
        ''' + F('gsAmt', 'Amount', '11800', em='in rupees', extra=' inputmode="decimal"') + '''
        ''' + F('gsMode', 'This amount is', 'inc', tag='select', opts=[('exc', 'Before GST (add GST to it)'), ('inc', 'Including GST (take GST out of it)')]) + '''
        <div class="field"><label>GST Rate</label><div class="chips" id="gsChips" style="margin-bottom:8px">''' + CHIPS + '''</div>
        <input id="gsCustom" type="text" inputmode="decimal" autocomplete="off" placeholder="Other rate, for example 7.5" aria-label="Other GST rate in percent"></div>
        <p style="font-size:13.5px;color:#666;margin-top:0">5% and 18% are the main rates since 22 September 2025, and 40% is for sin and luxury goods. Use 12% or 28% only for older invoices.</p>
      </div>
      <div id="gsInvWrap" style="display:none">
        <h2>Invoice Items</h2>
        <div style="overflow-x:auto;margin-bottom:10px"><table class="rtable" id="gsItems" style="min-width:520px"><thead><tr><th>Item</th><th class="num">Qty</th><th class="num">Price per unit</th><th class="num">GST %</th><th></th></tr></thead><tbody></tbody></table></div>
        <div class="actions" style="margin:0 0 14px"><button type="button" class="btn btn-sm" id="gsAdd">Add Item</button><button type="button" class="btn btn-sm" id="gsReset">Clear Items</button></div>
        ''' + CK('gsInc', 'Prices already include GST', False) + '''
        ''' + CK('gsRound', 'Round the invoice total to the nearest rupee', True) + '''
      </div>
      ''' + F('gsSup', 'Where is it supplied?', 'intra', tag='select', opts=[('intra', 'Within the same state (CGST and SGST)'), ('ut', 'Within a union territory (CGST and UTGST)'), ('inter', 'To another state or abroad (IGST)')]) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('gsBase', 'Before GST') + S('gsTax', 'GST') + S('gsTotal', 'Total') + '''</div>
      <div class="kw-result" id="gsNote"></div>
      <div style="overflow-x:auto" id="gsBreak"></div>
      <div id="gsMore"></div>
      <div class="actions"><button class="btn dark" id="gsCopy">Copy Summary</button><button class="btn" id="gsDl" style="display:none">Download CSV</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  var R2 = function(x){ return Math.round((x + Number.EPSILON) * 100) / 100; };
  function num(s){ s = String(s == null ? '' : s).replace(/[₹,\s]/g, '').replace(/^rs\.?/i, ''); if (s === '' || !/^\d*\.?\d+$|^\d+\.$/.test(s)) return NaN; return parseFloat(s); }
  function inr(x){ return '₹' + Number(x).toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); }
  function pc(r){ return (Math.round(r * 1000) / 1000) + '%'; }
  var LBL = {intra: ['CGST', 'SGST'], ut: ['CGST', 'UTGST'], inter: ['IGST']};
  // One line: amount = qty x price. Returns taxable value, tax parts and total, rounded to paise.
  function line(amt, r, inc, sup){
    amt = R2(amt);
    var base, parts;
    if (inc){
      base = R2(amt * 100 / (100 + r));
      var tax = R2(amt - base);
      if (sup === 'inter') parts = [tax];
      else { var h = R2(tax / 2); parts = [h, R2(tax - h)]; }
    } else {
      base = amt;
      if (sup === 'inter') parts = [R2(base * r / 100)];
      else { var h2 = R2(base * r / 200); parts = [h2, h2]; }
    }
    var t = R2(parts.reduce(function(a, b){ return a + b; }, 0));
    return {base: base, parts: parts, tax: t, total: R2(base + t)};
  }
  var ONES = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
  var TENS = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];
  function w2(n){ return n < 20 ? ONES[n] : TENS[Math.floor(n / 10)] + (n % 10 ? ' ' + ONES[n % 10] : ''); }
  function w3(n){ return (n >= 100 ? ONES[Math.floor(n / 100)] + ' Hundred' + (n % 100 ? ' ' : '') : '') + (n % 100 ? w2(n % 100) : ''); }
  function words(n){
    if (n === 0) return 'Zero';
    var out = [], cr = Math.floor(n / 10000000), rest = n % 10000000;
    if (cr) out.push((cr >= 1000 ? words(cr) : w3(cr)) + ' Crore');
    var l = Math.floor(rest / 100000), th = Math.floor(rest / 1000) % 100, h = rest % 1000;
    if (l) out.push(w2(l) + ' Lakh'); if (th) out.push(w2(th) + ' Thousand'); if (h) out.push(w3(h));
    return out.join(' ');
  }
  function inWords(x){
    var p = Math.round(x * 100), r = Math.floor(p / 100), ps = p % 100;
    return 'Rupees ' + words(r) + (ps ? ' and ' + w2(ps) + ' Paise' : '') + ' Only';
  }
  window.__gst = {line: line, inWords: inWords};

  var tab = 'quick', rate = 18, summary = '', csv = '';
  var SAMPLE = [['SEO retainer, November', 1, 25000, 18], ['Google Ads management fee', 1, 15000, 18], ['Team offsite hotel room, per night', 2, 6500, 5]];
  function rowHtml(d){
    var o = ['0', '0.25', '3', '5', '18', '40', '12', '28'].map(function(r){ return '<option value="' + r + '"' + (String(d[3]) === r ? ' selected' : '') + '>' + r + '%</option>'; }).join('');
    return '<tr><td><input type="text" aria-label="Item name" value="' + esc(d[0]) + '" style="min-width:150px"></td>' +
      '<td><input type="text" inputmode="decimal" aria-label="Quantity" value="' + esc(String(d[1])) + '" style="width:64px;text-align:right"></td>' +
      '<td><input type="text" inputmode="decimal" aria-label="Price per unit" value="' + esc(String(d[2])) + '" style="width:110px;text-align:right"></td>' +
      '<td><select aria-label="GST rate">' + o + '</select></td>' +
      '<td><button type="button" class="btn btn-sm" aria-label="Remove item" data-del="1">&times;</button></td></tr>';
  }
  function addRow(d){ $('gsItems').tBodies[0].insertAdjacentHTML('beforeend', rowHtml(d || ['', 1, '', 18])); }
  SAMPLE.forEach(addRow);
  $('gsItems').querySelectorAll('input,select').forEach(function(e){ e.style.border = '1px solid #cfcfcf'; e.style.borderRadius = '6px'; e.style.padding = '6px 8px'; e.style.font = 'inherit'; e.style.fontSize = '14px'; });
  function styleNew(){ var tr = $('gsItems').tBodies[0].lastElementChild; if (tr) tr.querySelectorAll('input,select').forEach(function(e){ e.style.border = '1px solid #cfcfcf'; e.style.borderRadius = '6px'; e.style.padding = '6px 8px'; e.style.font = 'inherit'; e.style.fontSize = '14px'; }); }

  function curRate(){ var c = num($('gsCustom').value); return $('gsCustom').value.trim() ? c : rate; }

  function quick(){
    var amt = num($('gsAmt').value), r = curRate(), sup = $('gsSup').value, inc = $('gsMode').value === 'inc', L = LBL[sup];
    $('gsDl').style.display = 'none';
    if (!(amt >= 0)) { say('gsNote', 'bad', 'Enter an amount in rupees, for example 11800.'); clear(); return; }
    if (!(r >= 0) || r > 100) { say('gsNote', 'bad', 'Enter a GST rate between 0 and 100 percent.'); clear(); return; }
    var x = line(amt, r, inc, sup);
    $('gsBase').textContent = inr(x.base); $('gsTax').textContent = inr(x.tax); $('gsTotal').textContent = inr(x.total);
    var rows = '<tr><td>Amount before GST (taxable value)</td><td class="num">' + inr(x.base) + '</td></tr>';
    L.forEach(function(n, i){ rows += '<tr><td>' + n + ' at ' + pc(L.length > 1 ? r / 2 : r) + '</td><td class="num">' + inr(x.parts[i]) + '</td></tr>'; });
    rows += '<tr class="hit"><td>Total including GST</td><td class="num">' + inr(x.total) + '</td></tr>';
    $('gsBreak').innerHTML = '<table class="rtable" style="margin-bottom:16px"><tbody>' + rows + '</tbody></table>';
    say('gsNote', 'ok', inc ? '<strong>' + inr(amt) + '</strong> includes <strong>' + inr(x.tax) + '</strong> of GST at ' + pc(r) + '. The price before GST is <strong>' + inr(x.base) + '</strong>.'
                           : 'Adding ' + pc(r) + ' GST to <strong>' + inr(amt) + '</strong> gives <strong>' + inr(x.total) + '</strong>, of which <strong>' + inr(x.tax) + '</strong> is GST.');
    var cmp = '';
    [0, 5, 18, 40].concat([3, 12, 28]).forEach(function(rr){
      var y = line(amt, rr, inc, sup);
      cmp += '<tr' + (rr === r ? ' class="hit"' : '') + '><td>' + pc(rr) + '</td><td class="num">' + inr(y.base) + '</td><td class="num">' + inr(y.tax) + '</td><td class="num">' + inr(y.total) + '</td></tr>';
    });
    $('gsMore').innerHTML = '<h3 style="font-size:16px;margin:4px 0 8px">Same Amount at Every Rate</h3><div style="overflow-x:auto"><table class="rtable"><thead><tr><th>Rate</th><th class="num">Before GST</th><th class="num">GST</th><th class="num">Total</th></tr></thead><tbody>' + cmp + '</tbody></table></div>';
    summary = 'GST calculation at ' + pc(r) + '\nAmount before GST: ' + inr(x.base) + '\n' + L.map(function(n, i){ return n + ' at ' + pc(L.length > 1 ? r / 2 : r) + ': ' + inr(x.parts[i]); }).join('\n') + '\nTotal GST: ' + inr(x.tax) + '\nTotal including GST: ' + inr(x.total);
  }
  function clear(){ ['gsBase', 'gsTax', 'gsTotal'].forEach(function(i){ $(i).textContent = '…'; }); $('gsBreak').innerHTML = ''; $('gsMore').innerHTML = ''; summary = ''; }
  function q(s){ s = String(s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }

  function invoice(){
    var sup = $('gsSup').value, inc = $('gsInc').checked, L = LBL[sup], items = [], bad = 0;
    $('gsItems').tBodies[0].querySelectorAll('tr').forEach(function(tr, k){
      var f = tr.querySelectorAll('input,select'), qn = num(f[1].value), p = num(f[2].value), r = parseFloat(f[3].value);
      var blank = !f[0].value.trim() && !f[2].value.trim();
      f[1].style.borderColor = qn > 0 || blank ? '#cfcfcf' : '#d1351f'; f[2].style.borderColor = p >= 0 || blank ? '#cfcfcf' : '#d1351f';
      if (blank) return;
      if (!(qn > 0) || !(p >= 0)) { bad++; return; }
      var x = line(qn * p, r, inc, sup); x.name = f[0].value.trim() || 'Item ' + (k + 1); x.qty = qn; x.rate = r; items.push(x);
    });
    if (!items.length) { say('gsNote', bad ? 'bad' : '', bad ? 'Check the highlighted quantity and price boxes. Use numbers only.' : 'Add at least one item with a quantity and a price.'); clear(); $('gsDl').style.display = 'none'; return; }
    var base = 0, tax = 0, sums = {}, parts = L.map(function(){ return 0; });
    var rows = items.map(function(x){
      base = R2(base + x.base); tax = R2(tax + x.tax); x.parts.forEach(function(v, i){ parts[i] = R2(parts[i] + v); });
      var s = sums[x.rate] || (sums[x.rate] = {base: 0, parts: L.map(function(){ return 0; }), tax: 0});
      s.base = R2(s.base + x.base); s.tax = R2(s.tax + x.tax); x.parts.forEach(function(v, i){ s.parts[i] = R2(s.parts[i] + v); });
      return '<tr><td>' + esc(x.name) + '<br><small style="color:#666">' + fmtN(x.qty) + ' at ' + pc(x.rate) + '</small></td><td class="num">' + inr(x.base) + '</td><td class="num">' + inr(x.tax) + '</td><td class="num">' + inr(x.total) + '</td></tr>';
    }).join('');
    var total = R2(base + tax), round = $('gsRound').checked ? R2(Math.round(total) - total) : 0, grand = R2(total + round);
    $('gsBase').textContent = inr(base); $('gsTax').textContent = inr(tax); $('gsTotal').textContent = inr(grand);
    var foot = '<tr><td>Taxable value</td><td class="num" colspan="3">' + inr(base) + '</td></tr>';
    L.forEach(function(n, i){ foot += '<tr><td>' + n + '</td><td class="num" colspan="3">' + inr(parts[i]) + '</td></tr>'; });
    if (round) foot += '<tr><td>Round off</td><td class="num" colspan="3">' + (round > 0 ? '+' : '&minus;') + inr(Math.abs(round)) + '</td></tr>';
    foot += '<tr class="hit"><td>Invoice total</td><td class="num" colspan="3">' + inr(grand) + '</td></tr>';
    $('gsBreak').innerHTML = '<table class="rtable" style="margin-bottom:16px;min-width:420px"><thead><tr><th>Item</th><th class="num">Taxable</th><th class="num">GST</th><th class="num">Total</th></tr></thead><tbody>' + rows + foot + '</tbody></table>';
    var keys = Object.keys(sums).map(parseFloat).sort(function(a, b){ return a - b; });
    var srows = keys.map(function(k){ var s = sums[k]; return '<tr><td>' + pc(k) + '</td><td class="num">' + inr(s.base) + '</td>' + s.parts.map(function(v){ return '<td class="num">' + inr(v) + '</td>'; }).join('') + '<td class="num">' + inr(s.tax) + '</td></tr>'; }).join('');
    $('gsMore').innerHTML = '<h3 style="font-size:16px;margin:4px 0 8px">Tax Summary by Rate</h3><div style="overflow-x:auto"><table class="rtable" style="min-width:420px"><thead><tr><th>Rate</th><th class="num">Taxable</th>' + L.map(function(n){ return '<th class="num">' + n + '</th>'; }).join('') + '<th class="num">Total GST</th></tr></thead><tbody>' + srows + '</tbody></table></div>' +
      '<p style="font-size:14px;margin:12px 0 0"><strong>Amount in words:</strong> <span id="gsWords">' + inWords(grand) + '</span></p>';
    say('gsNote', bad ? 'warn' : 'ok', (bad ? '<strong>' + bad + ' item' + (bad > 1 ? 's' : '') + ' skipped.</strong> Fix the highlighted boxes. ' : '') + items.length + ' item' + (items.length > 1 ? 's' : '') + ', ' + (inc ? 'prices include GST' : 'GST added on top') + '. Total GST is <strong>' + inr(tax) + '</strong> and the invoice total is <strong>' + inr(grand) + '</strong>.');
    summary = items.map(function(x){ return x.name + ' (' + fmtN(x.qty) + ' at ' + pc(x.rate) + '): taxable ' + inr(x.base) + ', GST ' + inr(x.tax) + ', total ' + inr(x.total); }).join('\n') +
      '\n\nTaxable value: ' + inr(base) + '\n' + L.map(function(n, i){ return n + ': ' + inr(parts[i]); }).join('\n') + (round ? '\nRound off: ' + (round > 0 ? '+' : '') + round.toFixed(2) : '') + '\nInvoice total: ' + inr(grand) + '\n' + inWords(grand);
    var head = ['Item', 'Quantity', 'GST rate %', 'Taxable value'].concat(L, ['Total GST', 'Line total']);
    csv = [head.join(',')].concat(items.map(function(x){ return [q(x.name), x.qty, x.rate, x.base.toFixed(2)].concat(x.parts.map(function(v){ return v.toFixed(2); }), [x.tax.toFixed(2), x.total.toFixed(2)]).join(','); }))
      .concat([['Total', '', '', base.toFixed(2)].concat(parts.map(function(v){ return v.toFixed(2); }), [tax.toFixed(2), total.toFixed(2)]).join(',')])
      .concat(round ? ['Round off,,,,' + L.map(function(){ return ''; }).join(',') + ',,' + round.toFixed(2)] : [])
      .concat(['Invoice total,,,,' + L.map(function(){ return ''; }).join(',') + ',,' + grand.toFixed(2)]).join('\n');
    $('gsDl').style.display = '';
  }
  function run(){ if (tab === 'quick') quick(); else invoice(); }

  $('gsChips').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    rate = parseFloat(b.getAttribute('data-r')); $('gsCustom').value = '';
    $('gsChips').querySelectorAll('button').forEach(function(x){ x.classList.toggle('dark', x === b); });
    run();
  });
  $('gsCustom').addEventListener('input', function(){
    var on = this.value.trim() !== '';
    $('gsChips').querySelectorAll('button').forEach(function(x){ x.classList.toggle('dark', !on && parseFloat(x.getAttribute('data-r')) === rate); });
    run();
  });
  $('gsTabs').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    tab = b.getAttribute('data-t');
    $('gsTabs').querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x === b); });
    $('gsQuick').style.display = tab === 'quick' ? '' : 'none'; $('gsInvWrap').style.display = tab === 'inv' ? '' : 'none';
    run();
  });
  ['gsAmt'].forEach(function(i){ $(i).addEventListener('input', run); });
  ['gsMode', 'gsSup', 'gsInc', 'gsRound'].forEach(function(i){ $(i).addEventListener('change', run); });
  $('gsItems').addEventListener('input', run); $('gsItems').addEventListener('change', run);
  $('gsItems').addEventListener('click', function(e){ var b = e.target.closest('[data-del]'); if (!b) return; b.closest('tr').remove(); run(); });
  $('gsAdd').onclick = function(){ addRow(); styleNew(); $('gsItems').tBodies[0].lastElementChild.querySelector('input').focus(); run(); };
  $('gsReset').onclick = function(){ $('gsItems').tBodies[0].innerHTML = ''; addRow(); styleNew(); run(); };
  $('gsCopy').onclick = function(){ if (summary) copyText(summary, 'toast'); };
  $('gsDl').onclick = function(){ if (csv) download('gst-invoice.csv', '﻿' + csv, 'text/csv'); };
  run();
''',
        content=f'''
    <h2>What Is a GST Calculator?</h2>
    <p>A GST calculator works out the Goods and Services Tax on a price in India. It answers the two questions every shop owner, freelancer, agency and buyer asks each day: how much will this cost once GST is added, and how much of this bill is GST?</p>
    <p>This one does both, and more. Add GST to a base price, or take it out of a price that already includes it. See the tax split into CGST and SGST for a sale within your state, or IGST for a sale to another state. Switch to the invoice tab to total several items at different rates, with a tax summary for each rate, a round off line and the amount in words, ready to copy into your bill.</p>
    <p>It is updated for GST 2.0, the new rate structure that started on 22 September 2025. Most goods and services now fall under two main rates, 5% and 18%, with a special 40% rate for sin and luxury goods. You can check the official rate lists on the <a href="https://gstcouncil.gov.in/" {EXT}>GST Council website</a> and the <a href="https://cbic-gst.gov.in/gst-goods-services-rates.html" {EXT}>CBIC GST rates page</a>.</p>

    <h2>How to Use the GST Calculator</h2>
    <ol>
      <li><strong>Enter the amount</strong> in rupees. A sample of ₹11,800 is already filled in.</li>
      <li><strong>Say what the amount is.</strong> Choose Before GST to add tax on top, or Including GST to find the tax hidden inside a total.</li>
      <li><strong>Pick the GST rate.</strong> Tap 5%, 18%, 40% or another rate, or type your own.</li>
      <li><strong>Choose where it is supplied.</strong> Within your state gives CGST and SGST, another state gives IGST.</li>
      <li><strong>Read the result.</strong> You get the price before GST, the GST amount, the total, and the same amount at every rate.</li>
      <li><strong>Billing several items?</strong> Open Invoice With Items, enter each item, quantity, price and rate, then copy the summary or download a CSV file.</li>
    </ol>

    <h2>GST Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('You know', 'Formula', 'Example at 18%')}
      <tbody>
        <tr><td>Price before GST</td><td>GST = price &times; rate &divide; 100, total = price + GST</td><td>₹10,000 + ₹1,800 = ₹11,800</td></tr>
        <tr><td>Price including GST</td><td>Price before GST = total &times; 100 &divide; (100 + rate), GST = total &minus; that price</td><td>₹11,800 &times; 100 &divide; 118 = ₹10,000, GST ₹1,800</td></tr>
        <tr><td>Sale within the same state</td><td>CGST = SGST = GST &divide; 2</td><td>₹900 CGST at 9% and ₹900 SGST at 9%</td></tr>
        <tr><td>Sale to another state</td><td>IGST = full GST</td><td>₹1,800 IGST at 18%</td></tr>
      </tbody>
    </table></div>
    <p>A common mistake is to remove GST by taking 18% off the total. That gives ₹9,676 from ₹11,800, which is wrong. Always divide by 1.18, as the calculator does.</p>

    <h2>GST Rates After 22 September 2025</h2>
    <ul>
      <li><strong>0%:</strong> exempt and nil rated items such as fresh food and many daily essentials.</li>
      <li><strong>5%:</strong> the merit rate for everyday goods and many services.</li>
      <li><strong>18%:</strong> the standard rate for most goods and services, including digital advertising, software, agency and consulting fees.</li>
      <li><strong>40%:</strong> the special rate for sin and luxury goods.</li>
      <li><strong>3% and 0.25%:</strong> special rates for gold and silver, and for rough precious stones.</li>
      <li><strong>12% and 28%:</strong> removed for most items in GST 2.0. Keep them only to check invoices dated before the change.</li>
    </ul>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Budget ads with GST.</strong> Google Ads and Meta ads billed in India add 18% GST to your spend, so a ₹50,000 budget becomes a ₹59,000 bill. Registered businesses can usually claim that GST back as input tax credit.</li>
      <li><strong>Check the place of supply.</strong> Charging CGST and SGST when the sale should carry IGST is a frequent invoice error that delays your buyer's input tax credit.</li>
      <li><strong>Round only the final total.</strong> Work out tax on each line in paise, then round the invoice total and show the difference as a round off line, as the invoice tab does.</li>
      <li><strong>Confirm the rate for your HSN or SAC code.</strong> Rates depend on the exact product or service, so check the official list before you bill.</li>
      <li><strong>Your figures stay private.</strong> Everything runs in your browser. Nothing you enter is uploaded or saved.</li>
    </ul>

    <h2>GST and Your Marketing Numbers</h2>
    <p>Tax changes how you judge campaign results. When you report revenue, keep GST out of it, and send the tax in the <code>tax</code> field of your purchase event, as shown in our <a href="{B}ga4-ecommerce-events-examples/">GA4 ecommerce events examples</a>. Plan monthly ad spend with GST included using our guide to the <a href="{B}google-ads-budget-pacing-update-2026/">Google Ads budget pacing update</a>, and keep your reports clean with a <a href="{B}paid-media-reporting-dashboard/">paid media reporting dashboard</a>. Then use the <a href="{PP}break-even-roas-calculator/">break even ROAS calculator</a> to see the return your ads need after tax and costs.</p>
''',
        faqs=[
            ("How do I calculate GST from a total amount?", "Divide the total by 1 plus the rate. For 18% GST, divide by 1.18: ₹11,800 divided by 1.18 is ₹10,000, so the GST is ₹1,800. In the calculator, choose Including GST and it does this for you."),
            ("When do I charge CGST and SGST, and when IGST?", "Charge CGST and SGST, split equally, when the supplier and the place of supply are in the same state. Charge IGST when the place of supply is in another state or the sale is an export. In a union territory without its own legislature, UTGST takes the place of SGST."),
            ("What are the GST rates in India now?", "Since 22 September 2025, most goods and services are taxed at 5% or 18%, with a special 40% rate for sin and luxury goods and 0% for exempt items. Gold and silver stay at 3%. The old 12% and 28% slabs were removed for most items."),
            ("Is GST charged on Google Ads and Facebook ads?", "Yes. Online advertising billed to an Indian account carries 18% GST, added on top of your ad spend. If your business is registered for GST, you can usually claim it back as input tax credit using the GSTIN on your ad account."),
        ],
        related=[("GA4 Ecommerce Events Examples", "ga4-ecommerce-events-examples"), ("Google Ads Budget Pacing Update 2026", "google-ads-budget-pacing-update-2026"),
                 ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard"), ("Digital Marketing Tips 2026", "digital-marketing-tips-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'business-calculators'; t['updated'] = '2026-11-21'
