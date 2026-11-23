"""Batch 26 (2026-11-23): Business Calculators, third tool (Break Even Calculator).
Search demand: "break even calculator" and "break even point calculator" are long standing high volume
calculator queries; Omni Calculator, Calculator.net, Pearson, Xero, Sage and FreshBooks rank for them.
Not a duplicate: the PPC break even ROAS calculator works on ad return only, not fixed costs and units.
Facts checked 2026-11-23 (Xero, Sage, AccountingCoach, OpenStax Principles of Accounting 3.2):
break even units = fixed costs / (price - variable cost per unit); break even revenue = fixed costs /
contribution margin ratio; units for a target profit = (fixed costs + target profit) / contribution per unit;
margin of safety = (expected sales - break even sales) / expected sales.
Runs fully in the browser: ad cost per sale as an extra variable cost, margin of safety, profit at expected
sales, units for a target profit, payback months for a one time investment, and price and volume tables."""
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/business-calculators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='break-even-calculator', short='BEP', name='Break Even Calculator',
        card='Find how many units and how much revenue you need each month to cover your costs, including ad spend per sale.',
        title='Break Even Calculator: Units, Revenue and Profit',
        desc='Free break even calculator. Find the units and sales you need to cover fixed costs, with ad cost per sale, margin of safety, target profit and payback time.',
        h1='Break Even Calculator',
        lead='Enter your monthly fixed costs, your price and what each sale costs you, and see exactly how many units you must sell to stop losing money. Add your ad cost per sale to see the true picture for a business that grows with ads.',
        tool='''<section class="tool" aria-label="Break even calculator" id="beForm">
    <div class="card" style="min-width:0">
      <h2>Your Costs and Price</h2>
      ''' + F('beFixed', 'Fixed costs per month', '150000', em='in rupees: rent, salaries, software, EMIs', extra=' inputmode="decimal"') + '''
      ''' + F('bePrice', 'Selling price per unit', '1000', em='in rupees, before GST', extra=' inputmode="decimal"') + '''
      ''' + F('beVar', 'Variable cost per unit', '550', em='product, packing, shipping, payment and marketplace fees', extra=' inputmode="decimal"') + '''
      ''' + F('beAds', 'Ad cost per sale', '150', em='optional, your cost per acquisition', extra=' inputmode="decimal"') + '''
      ''' + F('beExp', 'Units you expect to sell per month', '650', em='optional, for profit and margin of safety', extra=' inputmode="decimal"') + '''
      ''' + F('beTarget', 'Monthly profit you want', '60000', em='optional, in rupees', extra=' inputmode="decimal"') + '''
      ''' + F('beInvest', 'One time investment to recover', '300000', em='optional: setup, stock, equipment', extra=' inputmode="decimal"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('beUnits', 'Break even units a month') + S('beRev', 'Break even sales a month') + S('beCm', 'Contribution per unit') + '''</div>
      <div class="kw-result" id="beNote"></div>
      <div style="overflow-x:auto" id="beBreak"></div>
      <div id="beMore"></div>
      <div class="actions"><button class="btn dark" id="beCopy">Copy Summary</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  function num(s){ s = String(s == null ? '' : s).replace(/[₹,\s]/g, '').replace(/^rs\.?/i, ''); if (s === '' || !/^\d*\.?\d+$|^\d+\.$/.test(s)) return NaN; return parseFloat(s); }
  function inr(x, d){ d = d == null ? 0 : d; return (x < 0 ? '&minus;' : '') + '₹' + Math.abs(x).toLocaleString('en-IN', {minimumFractionDigits: d, maximumFractionDigits: d}); }
  function inrT(x){ return (x < 0 ? '-' : '') + '₹' + Math.abs(x).toLocaleString('en-IN', {maximumFractionDigits: 0}); }
  function pc(r){ return (r < 0 ? '&minus;' : '') + Math.abs(Math.round(r * 100) / 100) + '%'; }
  function pcT(r){ return (Math.round(r * 100) / 100) + '%'; }
  // Core maths. Returns contribution per unit, ratio, exact and whole break even units, break even revenue.
  function calc(fixed, price, varc){
    var cm = price - varc;
    if (!(cm > 0)) return {cm: cm, ratio: price > 0 ? cm / price : null, exact: null, units: null, rev: null};
    var exact = fixed / cm, units = Math.ceil(exact - 1e-9);
    return {cm: cm, ratio: cm / price, exact: exact, units: units, rev: fixed / (cm / price)};
  }
  function unitsFor(fixed, cm, profit){ return Math.ceil((fixed + profit) / cm - 1e-9); }
  window.__be = {calc: calc, unitsFor: unitsFor};

  var summary = '';
  function opt(id){ var r = $(id).value.trim(); return r ? num(r) : 0; }
  function clear(){ ['beUnits', 'beRev', 'beCm'].forEach(function(i){ $(i).textContent = '…'; }); $('beBreak').innerHTML = ''; $('beMore').innerHTML = ''; summary = ''; }

  function run(){
    var fixed = num($('beFixed').value), price = num($('bePrice').value), v = num($('beVar').value), ads = opt('beAds'), exp = opt('beExp'), tgt = opt('beTarget'), inv = opt('beInvest');
    if (!(fixed >= 0)) { say('beNote', 'bad', 'Enter your fixed costs per month in rupees, for example 150000.'); clear(); return; }
    if (!(price > 0)) { say('beNote', 'bad', 'Enter a selling price above zero, for example 1000.'); clear(); return; }
    if (!(v >= 0)) { say('beNote', 'bad', 'Enter the variable cost per unit in rupees, for example 550. Use 0 if there is none.'); clear(); return; }
    var bad = [['beAds', ads, 'Ad cost per sale'], ['beExp', exp, 'Units you expect to sell'], ['beTarget', tgt, 'Monthly profit you want'], ['beInvest', inv, 'One time investment']].filter(function(x){ return !(x[1] >= 0); });
    if (bad.length) { say('beNote', 'bad', bad[0][2] + ' must be a number, for example 100. Leave it empty to skip it.'); clear(); return; }
    var varc = v + ads, x = calc(fixed, price, varc);
    if (x.units === null) {
      say('beNote', 'bad', 'Each sale costs you ' + inr(varc, 2) + (ads > 0 ? ' including ads' : '') + ' but brings in only ' + inr(price, 2) + ', so every extra sale adds to your loss. You can never break even at this price. Raise the price above ' + inr(varc, 2) + (ads > 0 ? ' or bring your ad cost per sale down' : '') + '.');
      clear(); $('beCm').innerHTML = inr(x.cm, 2); return;
    }
    $('beUnits').textContent = fmtN(x.units);
    $('beRev').innerHTML = inr(x.rev);
    $('beCm').innerHTML = inr(x.cm, 2);

    var rows = '<tr><td>Selling price per unit</td><td class="num">' + inr(price, 2) + '</td></tr>' +
      '<tr><td>Variable cost per unit</td><td class="num">' + inr(v, 2) + '</td></tr>' +
      (ads > 0 ? '<tr><td>Ad cost per sale</td><td class="num">' + inr(ads, 2) + '</td></tr>' : '') +
      '<tr><td>Contribution per unit</td><td class="num">' + inr(x.cm, 2) + '</td></tr>' +
      '<tr><td>Contribution margin</td><td class="num">' + pc(x.ratio * 100) + '</td></tr>' +
      '<tr class="hit"><td>Break even units per month</td><td class="num">' + fmtN(x.units) + '</td></tr>' +
      '<tr><td>That is about this many a day</td><td class="num">' + fmtN(Math.ceil(x.units / 30)) + '</td></tr>' +
      '<tr class="hit"><td>Break even sales per month (before GST)</td><td class="num">' + inr(x.rev) + '</td></tr>';
    var profit = null, mos = null;
    if (exp > 0) {
      profit = exp * x.cm - fixed; mos = (exp - x.exact) / exp * 100;
      rows += '<tr><td>Profit at ' + fmtN(exp) + ' units a month</td><td class="num">' + inr(profit) + '</td></tr>' +
        '<tr><td>Margin of safety</td><td class="num">' + pc(mos) + '</td></tr>';
    }
    var tu = null;
    if (tgt > 0) { tu = unitsFor(fixed, x.cm, tgt); rows += '<tr><td>Units for ' + inr(tgt) + ' profit a month</td><td class="num">' + fmtN(tu) + '</td></tr><tr><td>Sales for that profit (before GST)</td><td class="num">' + inr(tu * price) + '</td></tr>'; }
    var pay = null;
    if (inv > 0 && profit !== null && profit > 0) { pay = Math.ceil(inv / profit - 1e-9); rows += '<tr><td>Months to recover ' + inr(inv) + '</td><td class="num">' + fmtN(pay) + '</td></tr>'; }
    $('beBreak').innerHTML = '<table class="rtable" style="margin-bottom:16px"><tbody>' + rows + '</tbody></table>';

    var note = 'You need to sell <strong>' + fmtN(x.units) + ' units</strong>, or <strong>' + inr(x.rev) + '</strong> in sales, every month to cover your costs. Each sale adds <strong>' + inr(x.cm, 2) + '</strong> towards fixed costs, then profit.';
    var cls = 'ok';
    if (profit !== null) {
      if (profit < 0) { cls = 'bad'; note += ' At ' + fmtN(exp) + ' units you lose <strong>' + inr(-profit) + '</strong> a month. You are ' + fmtN(x.units - exp) + ' units short.'; }
      else if (mos < 10) { cls = 'warn'; note += ' At ' + fmtN(exp) + ' units you make ' + inr(profit) + ', but a drop of just ' + pc(mos) + ' in sales wipes that out.'; }
      else note += ' At ' + fmtN(exp) + ' units you make <strong>' + inr(profit) + '</strong> a month, and sales can fall ' + pc(mos) + ' before you make a loss.';
    }
    if (inv > 0 && profit !== null && !(profit > 0)) note += ' You cannot recover the ' + inr(inv) + ' investment until you make a profit each month.';
    else if (pay !== null) note += ' You earn back the ' + inr(inv) + ' investment in about <strong>' + fmtN(pay) + ' month' + (pay === 1 ? '' : 's') + '</strong>.';
    if (inv > 0 && profit === null) note += ' Add the units you expect to sell to see how long the investment takes to recover.';
    say('beNote', cls, note);

    // Profit at different volumes around break even
    var vr = '';
    [0.5, 0.75, 1, 1.25, 1.5, 2].forEach(function(f){
      var u = f === 1 ? x.units : Math.round(x.units * f), p = u * x.cm - fixed;
      vr += '<tr' + (f === 1 ? ' class="hit"' : '') + '><td class="num">' + fmtN(u) + '</td><td class="num">' + inr(u * price) + '</td><td class="num">' + inr(p) + '</td></tr>';
    });
    var more = '<h3 style="font-size:16px;margin:4px 0 8px">Profit at Different Sales Levels</h3><div style="overflow-x:auto"><table class="rtable" style="margin-bottom:16px"><thead><tr><th class="num">Units a month</th><th class="num">Sales</th><th class="num">Profit or loss</th></tr></thead><tbody>' + vr + '</tbody></table></div>';
    // Break even at different prices
    var pr = '';
    [-10, -5, 0, 5, 10].forEach(function(d){
      var p2 = price * (1 + d / 100), y = calc(fixed, p2, varc);
      pr += '<tr' + (d === 0 ? ' class="hit"' : '') + '><td>' + (d === 0 ? 'Current price' : (d > 0 ? '+' : '&minus;') + Math.abs(d) + '% price') + '</td><td class="num">' + inr(p2, 2) + '</td><td class="num">' + (y.units === null ? 'never' : fmtN(y.units)) + '</td></tr>';
    });
    more += '<h3 style="font-size:16px;margin:4px 0 8px">Break Even Units if You Change the Price</h3><div style="overflow-x:auto"><table class="rtable"><thead><tr><th>Price change</th><th class="num">Price</th><th class="num">Break even units</th></tr></thead><tbody>' + pr + '</tbody></table></div>';
    $('beMore').innerHTML = more;

    summary = 'Break even calculation\nFixed costs per month: ' + inrT(fixed) + '\nSelling price per unit: ' + inrT(price) + '\nVariable cost per unit: ' + inrT(v) +
      (ads > 0 ? '\nAd cost per sale: ' + inrT(ads) : '') + '\nContribution per unit: ' + inrT(x.cm) + ' (' + pcT(x.ratio * 100) + ')' +
      '\nBreak even units per month: ' + fmtN(x.units) + '\nBreak even sales per month: ' + inrT(x.rev) +
      (profit !== null ? '\nProfit at ' + fmtN(exp) + ' units: ' + inrT(profit) + '\nMargin of safety: ' + pcT(mos) : '') +
      (tu !== null ? '\nUnits for ' + inrT(tgt) + ' profit: ' + fmtN(tu) : '') +
      (pay !== null ? '\nMonths to recover ' + inrT(inv) + ': ' + fmtN(pay) : '');
  }

  ['beFixed', 'bePrice', 'beVar', 'beAds', 'beExp', 'beTarget', 'beInvest'].forEach(function(i){ $(i).addEventListener('input', run); });
  $('beCopy').onclick = function(){ if (summary) copyText(summary, 'toast'); };
  run();
''',
        content=f'''
    <h2>What Is a Break Even Calculator?</h2>
    <p>A break even calculator tells you the point where your business stops losing money. It is the number of units, or the amount of sales, you need each month so that what you earn covers everything you spend. Every sale after that point is profit.</p>
    <p>The idea is simple. Some costs stay the same however much you sell, like rent, salaries and software. Others rise with every sale, like stock, packing, shipping and payment fees. The gap between your price and those per sale costs is your contribution, and you need enough contributions to pay for the fixed costs.</p>
    <p>This calculator adds one thing most others leave out: your ad cost per sale. If you grow with Google or Meta ads, every order also carries an acquisition cost, and leaving it out makes your break even point look far easier to reach than it is.</p>

    <h2>How to Use the Break Even Calculator</h2>
    <ol>
      <li><strong>Enter your fixed costs per month.</strong> Add up rent, salaries, software, loan EMIs and anything else you pay whether you sell or not.</li>
      <li><strong>Enter your selling price per unit</strong> before GST, since GST is not your income.</li>
      <li><strong>Enter your variable cost per unit.</strong> Include product cost, packing, shipping, payment gateway charges and marketplace commission.</li>
      <li><strong>Add your ad cost per sale</strong> if you pay for ads. Your CPA from Google Ads or Meta is the number to use.</li>
      <li><strong>Add the units you expect to sell</strong>, a target profit and any one time investment to see profit, margin of safety and payback time.</li>
      <li><strong>Read the tables</strong> to see how profit changes with volume, and how a small price change moves your break even point. Then copy the summary.</li>
    </ol>

    <h2>Break Even Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Figure', 'Formula', 'Example')}
      <tbody>
        <tr><td>Contribution per unit</td><td>Price &minus; variable cost &minus; ad cost per sale</td><td>₹1,000 &minus; ₹550 &minus; ₹150 = ₹300</td></tr>
        <tr><td>Contribution margin</td><td>Contribution &divide; price</td><td>₹300 &divide; ₹1,000 = 30%</td></tr>
        <tr><td>Break even units</td><td>Fixed costs &divide; contribution per unit</td><td>₹1,50,000 &divide; ₹300 = 500</td></tr>
        <tr><td>Break even sales</td><td>Fixed costs &divide; contribution margin</td><td>₹1,50,000 &divide; 0.3 = ₹5,00,000</td></tr>
        <tr><td>Units for a target profit</td><td>(Fixed costs + profit) &divide; contribution</td><td>(₹1,50,000 + ₹60,000) &divide; ₹300 = 700</td></tr>
        <tr><td>Margin of safety</td><td>(Expected units &minus; break even units) &divide; expected units</td><td>(650 &minus; 500) &divide; 650 = 23.08%</td></tr>
      </tbody>
    </table></div>
    <p>These are the standard cost volume profit formulas taught in accounting, as set out in the <a href="https://www.xero.com/us/glossary/break-even-point-formula/" {EXT}>Xero guide to the break even point formula</a>. Break even units are rounded up, because you cannot sell part of a unit.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Small price moves matter a lot.</strong> In the sample, a 10% price rise cuts the units you need from 500 to 375. Check the price table before you run a discount.</li>
      <li><strong>Watch your ad cost per sale.</strong> If your CPA rises from ₹150 to ₹250, contribution falls to ₹200 and you need 750 units instead of 500.</li>
      <li><strong>Keep a margin of safety.</strong> Below 10%, one slow month puts you in the red. Aim for 20% or more.</li>
      <li><strong>Be honest with fixed costs.</strong> Include your own salary if you need one. A business that only breaks even without paying you is not really breaking even.</li>
      <li><strong>Use averages for many products.</strong> If you sell a range, use your average order value as the price and the average cost per order as the variable cost.</li>
      <li><strong>Your figures stay private.</strong> Everything runs in your browser. Nothing you enter is uploaded or saved.</li>
    </ul>

    <h2>Break Even and Your Marketing</h2>
    <p>Your break even point shows how much room your ads have. To bring the cost per sale down, start with our <a href="{B}25-google-ads-optimization-tips/">Google Ads optimization tips</a>, and if you bid on value, read <a href="{B}value-based-bidding-google-ads-explained/">value based bidding in Google Ads explained</a>. Selling more to the same visitors lowers your break even point too, so see our guide to <a href="{B}conversion-rate-optimization/">conversion rate optimization</a>. To set the price itself, use the <a href="{T}profit-margin-calculator/">profit margin calculator</a>, and check your ad targets with the <a href="{PP}cpa-calculator/">CPA calculator</a>.</p>
''',
        faqs=[
            ("How do I calculate my break even point?", "Subtract your variable cost per unit from your selling price to get your contribution per unit. Then divide your monthly fixed costs by that number. With ₹1,50,000 fixed costs, a ₹1,000 price and ₹700 of costs per sale, you need ₹1,50,000 divided by ₹300, which is 500 units a month."),
            ("Should I count ad spend as a fixed or variable cost?", "If you pay a fairly steady cost for each order, such as your CPA in Google Ads or Meta, treat it as a variable cost and enter it as ad cost per sale. If you spend a fixed monthly amount on branding or retainers whatever you sell, add it to fixed costs instead."),
            ("What is margin of safety?", "Margin of safety is how far your sales can fall before you make a loss. If you expect to sell 650 units and break even at 500, your margin of safety is 150 units, or about 23%. The higher it is, the safer your business is in a slow month."),
            ("Why does the calculator say I can never break even?", "That happens when each sale costs you as much as or more than you charge for it, once product costs and ad cost per sale are added. Selling more then only makes the loss bigger. You need to raise your price, cut costs per unit, or lower your ad cost per sale."),
        ],
        related=[("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"), ("Value Based Bidding in Google Ads Explained", "value-based-bidding-google-ads-explained"),
                 ("Conversion Rate Optimization", "conversion-rate-optimization"), ("How to Generate High Quality Leads in 2026", "how-to-generate-high-quality-leads-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'business-calculators'; t['updated'] = '2026-11-23'
