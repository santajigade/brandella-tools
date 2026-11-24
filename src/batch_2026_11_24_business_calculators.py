"""Batch 27 (2026-11-24): Business Calculators, fourth tool (Customer Lifetime Value Calculator).
Search demand: "customer lifetime value calculator", "clv calculator", "ltv calculator" and "ltv cac ratio
calculator" are long standing marketing calculator queries; HubSpot, Shopify, Martech Zone, Geckoboard,
Chargebee and Wall Street Prep rank for them. Not a duplicate: the CPA and ROAS calculators work on one
order, not the full customer relationship.
Facts checked 2026-11-24 (HubSpot, Shopify, Chargebee, Wall Street Prep, CFI): repeat purchase CLV =
average order value x purchases per year x years retained x gross margin; subscription CLV = monthly revenue
per customer x gross margin / monthly churn, with average lifetime = 1 / churn; LTV:CAC of about 3:1 is the
common healthy benchmark, below 1:1 loses money, well above 5:1 can mean under investing in growth;
CAC payback months = CAC / monthly gross profit per customer.
Runs fully in the browser: two models (repeat purchases, subscription), profit and revenue CLV, LTV:CAC with
a verdict, highest CAC for 3:1, payback months, and a table of what each lever adds to lifetime value."""
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/business-calculators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='customer-lifetime-value-calculator', short='CLV', name='Customer Lifetime Value Calculator',
        card='Work out what a customer is worth over time, your LTV to CAC ratio, the most you can pay to win a customer and your payback months.',
        title='Customer Lifetime Value Calculator: CLV and LTV:CAC',
        desc='Free customer lifetime value calculator. Find CLV for repeat buyers or subscriptions, your LTV:CAC ratio, the highest safe CAC and your CAC payback months.',
        h1='Customer Lifetime Value Calculator',
        lead='Find out how much profit a customer brings you over the whole relationship, not just the first order. Compare it with what you pay to win that customer and see how much you can safely spend on ads.',
        tool='''<section class="tool" aria-label="Customer lifetime value calculator" id="clvForm">
    <div class="card" style="min-width:0">
      <div class="tabs" id="clvTabs" role="tablist"><button type="button" data-t="rep" class="on">Repeat Purchases</button><button type="button" data-t="sub">Subscription</button></div>
      <div id="clvRep">
        <h2>Your Customers</h2>
        ''' + F('clvAov', 'Average order value', '1200', em='in rupees, before GST', extra=' inputmode="decimal"') + '''
        ''' + F('clvFreq', 'Orders per customer per year', '4', extra=' inputmode="decimal"') + '''
        ''' + F('clvYears', 'Years a customer keeps buying', '3', extra=' inputmode="decimal"') + '''
      </div>
      <div id="clvSub" style="display:none">
        <h2>Your Subscribers</h2>
        ''' + F('clvArpu', 'Monthly revenue per customer', '999', em='in rupees, before GST', extra=' inputmode="decimal"') + '''
        ''' + F('clvChurn', 'Monthly churn rate', '4', em='percent of customers who cancel each month', extra=' inputmode="decimal"') + '''
      </div>
      ''' + F('clvMargin', 'Gross margin', '40', em='percent you keep after product and delivery costs', extra=' inputmode="decimal"') + '''
      ''' + F('clvCac', 'Cost to win a customer (CAC)', '1500', em='optional, ad and sales spend per new customer', extra=' inputmode="decimal"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('clvProfit', 'Lifetime value (profit)') + S('clvRev', 'Lifetime revenue') + S('clvRatio', 'LTV:CAC ratio') + '''</div>
      <div class="kw-result" id="clvNote"></div>
      <div style="overflow-x:auto" id="clvBreak"></div>
      <div id="clvMore"></div>
      <div class="actions"><button class="btn dark" id="clvCopy">Copy Summary</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  function num(s){ s = String(s == null ? '' : s).replace(/[₹,%\s]/g, '').replace(/^rs\.?/i, ''); if (s === '' || !/^\d*\.?\d+$|^\d+\.$/.test(s)) return NaN; return parseFloat(s); }
  function inr(x){ return (x < 0 ? '&minus;' : '') + '₹' + Math.abs(Math.round(x)).toLocaleString('en-IN'); }
  function inrT(x){ return (x < 0 ? '-' : '') + '₹' + Math.abs(Math.round(x)).toLocaleString('en-IN'); }
  function r1(x){ return Math.round(x * 10) / 10; }
  function r2(x){ return Math.round(x * 100) / 100; }
  function rt(x){ return (x < 1 ? r2(x) : r1(x)) + ':1'; }
  // Core maths. m = gross margin as a fraction. Returns lifetime revenue, profit CLV, lifetime months and monthly gross profit.
  function rep(aov, freq, years, m){ var rev = aov * freq * years; return {rev: rev, clv: rev * m, months: years * 12, mgp: aov * freq / 12 * m}; }
  function sub(arpu, churn, m){ var months = 1 / churn; return {rev: arpu * months, clv: arpu * m / churn, months: months, mgp: arpu * m}; }
  window.__clv = {rep: rep, sub: sub};

  var mode = 'rep', summary = '';
  $('clvTabs').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    mode = b.getAttribute('data-t');
    $('clvTabs').querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x === b); });
    $('clvRep').style.display = mode === 'rep' ? '' : 'none';
    $('clvSub').style.display = mode === 'sub' ? '' : 'none';
    run();
  });
  function clear(){ ['clvProfit', 'clvRev', 'clvRatio'].forEach(function(i){ $(i).textContent = '…'; }); $('clvBreak').innerHTML = ''; $('clvMore').innerHTML = ''; summary = ''; }
  function bad(msg){ say('clvNote', 'bad', msg); clear(); }

  function run(){
    var mp = num($('clvMargin').value), cr = $('clvCac').value.trim(), cac = cr ? num(cr) : 0, x, inputs, levers = [];
    if (!(mp > 0 && mp <= 100)) return bad('Enter your gross margin as a percent between 1 and 100, for example 40.');
    if (!(cac >= 0)) return bad('CAC must be a number in rupees, for example 1500. Leave it empty to skip it.');
    var m = mp / 100;
    if (mode === 'rep') {
      var aov = num($('clvAov').value), freq = num($('clvFreq').value), yrs = num($('clvYears').value);
      if (!(aov > 0)) return bad('Enter your average order value in rupees, for example 1200.');
      if (!(freq > 0)) return bad('Enter how many orders a customer places in a year, for example 4. Use 1 for one order a year.');
      if (!(yrs > 0)) return bad('Enter how many years a customer keeps buying, for example 3. Use 0.5 for six months.');
      x = rep(aov, freq, yrs, m);
      inputs = [['Average order value', inr(aov), 'Average order value: ' + inrT(aov)], ['Orders per year', r2(freq), 'Orders per year: ' + r2(freq)], ['Years retained', r2(yrs), 'Years retained: ' + r2(yrs)]];
      levers = [['Order value up 10%', rep(aov * 1.1, freq, yrs, m)], ['One more order a year', rep(aov, freq + 1, yrs, m)], ['Customers stay 1 year longer', rep(aov, freq, yrs + 1, m)]];
      if (mp <= 95) levers.push(['Gross margin up 5 points', rep(aov, freq, yrs, m + 0.05)]);
    } else {
      var arpu = num($('clvArpu').value), ch = num($('clvChurn').value);
      if (!(arpu > 0)) return bad('Enter the monthly revenue per customer in rupees, for example 999.');
      if (!(ch > 0 && ch <= 100)) return bad('Enter your monthly churn as a percent above 0 and up to 100, for example 4. If 4 of every 100 customers cancel each month, enter 4.');
      x = sub(arpu, ch / 100, m);
      inputs = [['Monthly revenue per customer', inr(arpu), 'Monthly revenue per customer: ' + inrT(arpu)], ['Monthly churn', r2(ch) + '%', 'Monthly churn: ' + r2(ch) + '%']];
      levers = [['Price up 10%', sub(arpu * 1.1, ch / 100, m)]];
      if (ch > 1) levers.push(['Churn down 1 point', sub(arpu, (ch - 1) / 100, m)]);
      levers.push(['Churn cut in half', sub(arpu, ch / 2 / 100, m)]);
      if (mp <= 95) levers.push(['Gross margin up 5 points', sub(arpu, ch / 100, m + 0.05)]);
    }
    $('clvProfit').innerHTML = inr(x.clv);
    $('clvRev').innerHTML = inr(x.rev);
    var ratio = cac > 0 ? x.clv / cac : null, pay = cac > 0 ? Math.ceil(cac / x.mgp - 1e-9) : null;
    $('clvRatio').textContent = ratio === null ? 'add CAC' : rt(ratio);

    var rows = inputs.map(function(i){ return '<tr><td>' + i[0] + '</td><td class="num">' + i[1] + '</td></tr>'; }).join('') +
      '<tr><td>Gross margin</td><td class="num">' + r2(mp) + '%</td></tr>' +
      '<tr><td>Average customer lifetime</td><td class="num">' + r1(x.months) + ' months</td></tr>' +
      '<tr><td>Gross profit per customer per month</td><td class="num">' + inr(x.mgp) + '</td></tr>' +
      '<tr><td>Lifetime revenue per customer</td><td class="num">' + inr(x.rev) + '</td></tr>' +
      '<tr class="hit"><td>Customer lifetime value (profit)</td><td class="num">' + inr(x.clv) + '</td></tr>';
    if (cac > 0) rows += '<tr><td>Cost to win a customer</td><td class="num">' + inr(cac) + '</td></tr>' +
      '<tr class="hit"><td>LTV:CAC ratio</td><td class="num">' + rt(ratio) + '</td></tr>' +
      '<tr><td>Profit per customer after CAC</td><td class="num">' + inr(x.clv - cac) + '</td></tr>' +
      '<tr><td>Months to earn back CAC</td><td class="num">' + pay + '</td></tr>';
    rows += '<tr><td>Highest CAC for a 3:1 ratio</td><td class="num">' + inr(x.clv / 3) + '</td></tr>' +
      '<tr><td>Break even CAC (1:1)</td><td class="num">' + inr(x.clv) + '</td></tr>';
    $('clvBreak').innerHTML = '<table class="rtable" style="margin-bottom:16px"><tbody>' + rows + '</tbody></table>';

    var note = 'Each customer brings you about <strong>' + inr(x.clv) + '</strong> in gross profit over ' + r1(x.months) + ' months, from ' + inr(x.rev) + ' in sales.', cls = 'ok';
    if (ratio === null) { cls = ''; note += ' Add your cost to win a customer to see your LTV:CAC ratio. To keep a healthy 3:1 ratio, spend no more than <strong>' + inr(x.clv / 3) + '</strong> per new customer.'; }
    else if (ratio < 1) { cls = 'bad'; note += ' You pay ' + inr(cac) + ' to win each customer, so you <strong>lose ' + inr(cac - x.clv) + '</strong> on every one. Cut CAC below ' + inr(x.clv) + ' or raise lifetime value before you scale ads.'; }
    else if (ratio < 3) { cls = 'warn'; note += ' At <strong>' + rt(ratio) + '</strong> you make money, but the margin is thin once salaries and rent are paid. Aim for 3:1, which means a CAC of about ' + inr(x.clv / 3) + '.'; }
    else if (ratio <= 5) note += ' At <strong>' + rt(ratio) + '</strong> your customer economics are healthy. You earn back the ' + inr(cac) + ' CAC in about ' + pay + ' month' + (pay === 1 ? '' : 's') + '.';
    else note += ' At <strong>' + rt(ratio) + '</strong> each customer is very profitable. You could likely spend up to ' + inr(x.clv / 3) + ' per customer to grow faster and still keep 3:1.';
    if (pay !== null && ratio >= 1 && pay > x.months) { cls = 'bad'; note += ' But it takes ' + pay + ' months to earn back the CAC, longer than the average customer stays, so the cash comes back too slowly.'; }
    else if (pay !== null && ratio >= 1 && pay > 12) { if (cls === 'ok') cls = 'warn'; note += ' Payback takes ' + pay + ' months, so you need enough cash to fund growth until it comes back.'; }
    say('clvNote', cls, note);

    var lr = levers.map(function(l){ var d = l[1].clv - x.clv; return '<tr><td>' + l[0] + '</td><td class="num">' + inr(l[1].clv) + '</td><td class="num">+' + inr(d) + ' (+' + r1(d / x.clv * 100) + '%)</td></tr>'; }).join('');
    $('clvMore').innerHTML = '<h3 style="font-size:16px;margin:4px 0 8px">What Raises Your Lifetime Value Most</h3><div style="overflow-x:auto"><table class="rtable" style="margin-bottom:16px"><thead><tr><th>Change</th><th class="num">New CLV</th><th class="num">Gain</th></tr></thead><tbody>' + lr + '</tbody></table></div>';

    summary = 'Customer lifetime value (' + (mode === 'rep' ? 'repeat purchases' : 'subscription') + ')\n' + inputs.map(function(i){ return i[2]; }).join('\n') +
      '\nGross margin: ' + r2(mp) + '%\nAverage lifetime: ' + r1(x.months) + ' months\nLifetime revenue: ' + inrT(x.rev) + '\nLifetime value (profit): ' + inrT(x.clv) +
      (cac > 0 ? '\nCAC: ' + inrT(cac) + '\nLTV:CAC ratio: ' + rt(ratio) + '\nCAC payback: ' + pay + ' months' : '') + '\nHighest CAC for 3:1: ' + inrT(x.clv / 3);
  }

  ['clvAov', 'clvFreq', 'clvYears', 'clvArpu', 'clvChurn', 'clvMargin', 'clvCac'].forEach(function(i){ $(i).addEventListener('input', run); });
  $('clvCopy').onclick = function(){ if (summary) copyText(summary, 'toast'); };
  run();
''',
        content=f'''
    <h2>What Is Customer Lifetime Value?</h2>
    <p>Customer lifetime value, often shortened to CLV or LTV, is the total profit you can expect from one customer over the whole time they buy from you. A customer who spends ₹1,200 today and comes back four times a year for three years is worth far more than that first order.</p>
    <p>Knowing this number changes how you market. If you only look at the first sale, a ₹1,500 cost per customer looks like a loss. Once you see the full lifetime value, you know whether that spend pays back, how much more you could spend, and which lever grows profit fastest.</p>
    <p>This calculator works for both kinds of business: shops and services where people buy again and again, and subscriptions where people pay every month until they cancel.</p>

    <h2>How to Use the Customer Lifetime Value Calculator</h2>
    <ol>
      <li><strong>Pick your model.</strong> Choose Repeat Purchases for ecommerce, restaurants, salons and most services. Choose Subscription for SaaS, memberships and monthly plans.</li>
      <li><strong>Enter your customer numbers.</strong> For repeat purchases, add your average order value, orders per year and how many years a customer keeps buying. For subscriptions, add monthly revenue per customer and monthly churn.</li>
      <li><strong>Enter your gross margin</strong>, the percent you keep after product, delivery and payment costs. Lifetime value is measured in profit, not sales.</li>
      <li><strong>Add your cost to win a customer</strong>, your total ad and sales spend divided by new customers in the same period.</li>
      <li><strong>Read the verdict and the levers table</strong> to see your LTV:CAC ratio, payback months and which change would add the most value. Then copy the summary.</li>
    </ol>

    <h2>Customer Lifetime Value Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Figure', 'Formula', 'Example')}
      <tbody>
        <tr><td>Lifetime revenue (repeat)</td><td>Order value &times; orders per year &times; years</td><td>₹1,200 &times; 4 &times; 3 = ₹14,400</td></tr>
        <tr><td>Lifetime value (repeat)</td><td>Lifetime revenue &times; gross margin</td><td>₹14,400 &times; 40% = ₹5,760</td></tr>
        <tr><td>Average lifetime (subscription)</td><td>1 &divide; monthly churn</td><td>1 &divide; 4% = 25 months</td></tr>
        <tr><td>Lifetime value (subscription)</td><td>Monthly revenue &times; gross margin &divide; churn</td><td>₹999 &times; 40% &divide; 4% = ₹9,990</td></tr>
        <tr><td>LTV:CAC ratio</td><td>Lifetime value &divide; CAC</td><td>₹5,760 &divide; ₹1,500 = 3.8:1</td></tr>
        <tr><td>CAC payback</td><td>CAC &divide; monthly gross profit per customer</td><td>₹1,500 &divide; ₹160 = 10 months</td></tr>
      </tbody>
    </table></div>
    <p>These are the standard formulas used by finance and growth teams, as explained in <a href="https://blog.hubspot.com/service/how-to-calculate-customer-lifetime-value" {EXT}>HubSpot's guide to calculating customer lifetime value</a>. A ratio near 3:1 is the most common benchmark for healthy growth.</p>

    <h2>What Is a Good LTV:CAC Ratio?</h2>
    <ul>
      <li><strong>Below 1:1.</strong> You lose money on every new customer. Fix this before you spend more on ads.</li>
      <li><strong>1:1 to 3:1.</strong> Profitable on paper, but thin once rent, salaries and returns are paid.</li>
      <li><strong>3:1 to 5:1.</strong> Healthy. Each customer pays back their cost and funds growth.</li>
      <li><strong>Above 5:1.</strong> Very profitable, but you may be spending too little to grow. Test a higher budget.</li>
    </ul>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Use real data, not hopes.</strong> Take order value and repeat rate from your store or CRM for the last 12 months. For new businesses, keep years retained modest, such as 1 or 2.</li>
      <li><strong>Retention is usually the biggest lever.</strong> Check the levers table. Keeping customers one more year often adds more than a price rise.</li>
      <li><strong>Watch payback as well as the ratio.</strong> A 4:1 ratio that takes 20 months to pay back can still leave you short of cash.</li>
      <li><strong>Leave GST out.</strong> Enter prices before GST, since GST is not your income.</li>
      <li><strong>Your figures stay private.</strong> Everything runs in your browser and nothing is uploaded or saved.</li>
    </ul>

    <h2>Lifetime Value and Your Marketing</h2>
    <p>Lifetime value tells you how much you can bid for a customer, and which channels deserve credit. See <a href="{B}marketing-attribution-first-last-data-driven/">marketing attribution models explained</a> to judge channels fairly, and read our <a href="{B}email-marketing-strategy/">email marketing strategy</a> guide for the cheapest way to win repeat orders. If you bid on value in Google Ads, <a href="{B}value-based-bidding-google-ads-explained/">value based bidding explained</a> shows how to feed it better numbers. Then check how many sales you need each month with the <a href="{T}break-even-calculator/">break even calculator</a>, and set your ad targets with the <a href="{PP}cpa-calculator/">CPA calculator</a>.</p>
''',
        faqs=[
            ("How do I calculate customer lifetime value?", "Multiply your average order value by the number of orders a customer places each year and by the number of years they stay. That gives lifetime revenue. Multiply it by your gross margin to get lifetime value in profit. For example, ₹1,200 times 4 orders times 3 years is ₹14,400, and at a 40% margin that is ₹5,760."),
            ("How do I calculate CLV for a subscription business?", "Divide your monthly gross profit per customer by your monthly churn rate. If customers pay ₹999 a month, you keep 40%, and 4% cancel each month, the average customer stays 25 months and is worth ₹999 times 0.4 divided by 0.04, which is ₹9,990."),
            ("What is a good LTV to CAC ratio?", "About 3:1 is the common benchmark, meaning a customer brings three times what you paid to win them. Below 1:1 you lose money on each customer. Well above 5:1 usually means you could spend more on marketing to grow faster."),
            ("Should CLV use revenue or profit?", "Use profit. Revenue makes every customer look more valuable than they are, because it ignores product, delivery and payment costs. This calculator shows both, but the LTV:CAC ratio and the highest safe CAC are based on gross profit."),
        ],
        related=[("Marketing Attribution: First, Last and Data Driven", "marketing-attribution-first-last-data-driven"), ("Email Marketing Strategy", "email-marketing-strategy"),
                 ("Value Based Bidding in Google Ads Explained", "value-based-bidding-google-ads-explained"), ("Customer Journey Mapping in Digital Marketing", "customer-journey-mapping-digital-marketing")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'business-calculators'; t['updated'] = '2026-11-24'
