"""Batch 25 (2026-11-22): Business Calculators, second tool (Profit Margin Calculator).
Search demand: "profit margin calculator", "margin calculator" and "margin vs markup calculator" are long
standing high volume calculator queries; Omni Calculator, Calculator.net, Inch Calculator, Sage, Xero, Zoho
and Shopify rank for them. Not covered by any existing tool (the PPC calculators work on ad metrics only).
Facts checked 2026-11-22 (Xero, Zoho, Sage glossaries): margin = profit / selling price, markup = profit / cost,
price for a target margin = cost / (1 - margin), markup = margin / (1 - margin). GST is collected for the
government and is not revenue, so margin is worked out on the price before GST (GST 2.0 rates 5%, 18%, 40%).
Break even ROAS = 1 / margin, matching the break even ROAS calculator.
Runs fully in the browser: three modes (selling price, target margin, markup), optional GST on the price,
quantity totals, highest safe discount, break even ROAS, and a price table for common margins."""
from batch_2026_11_07_developer_tools import F, S, CK, BASEJS, th

T = 'https://brandella.in/tools/business-calculators/'
PP = 'https://brandella.in/tools/ppc-calculators/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='profit-margin-calculator', short='PM', name='Profit Margin Calculator',
        card='Find profit, margin and markup from cost and price, or the price you need for a target margin, with GST handled for you.',
        title='Profit Margin Calculator: Margin, Markup and Price',
        desc='Free profit margin calculator. Get margin and markup from cost and price, or the selling price for a target margin, with GST, discounts and break even ROAS.',
        h1='Profit Margin Calculator',
        lead='Enter what a product costs you and what you sell it for, and see your profit, margin and markup at once. Or set the margin you want and get the right selling price, with GST added correctly.',
        tool='''<section class="tool" aria-label="Profit margin calculator" id="pmForm">
    <div class="card" style="min-width:0">
      <h2>Cost and Price</h2>
      ''' + F('pmCost', 'Cost per unit', '600', em='in rupees, all costs to make or buy one unit', extra=' inputmode="decimal"') + '''
      ''' + F('pmMode', 'I know the', 'price', tag='select', opts=[('price', 'Selling price'), ('margin', 'Margin I want (%)'), ('markup', 'Markup I add (%)')]) + '''
      ''' + F('pmVal', 'Selling price per unit', '1180', em='in rupees', extra=' inputmode="decimal"') + '''
      ''' + F('pmGst', 'GST on the selling price', '18', tag='select', opts=[('0', 'No GST'), ('5', '5%'), ('18', '18%'), ('40', '40%'), ('3', '3%'), ('12', '12% (older invoices)'), ('28', '28% (older invoices)')]) + '''
      <div id="pmIncWrap">''' + CK('pmInc', 'The selling price I entered includes GST', True) + '''</div>
      ''' + F('pmQty', 'Units sold', '100', em='optional, for totals', extra=' inputmode="numeric"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Result</h2>
      <div class="stats">''' + S('pmMargin', 'Margin') + S('pmMarkup', 'Markup') + S('pmProfit', 'Profit per unit') + '''</div>
      <div class="kw-result" id="pmNote"></div>
      <div style="overflow-x:auto" id="pmBreak"></div>
      <div id="pmMore"></div>
      <div class="actions"><button class="btn dark" id="pmCopy">Copy Summary</button><span class="toast" id="toast">Copied!</span></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  function num(s){ s = String(s == null ? '' : s).replace(/[₹,\s]/g, '').replace(/^rs\.?/i, '').replace(/%$/, ''); if (s === '' || !/^\d*\.?\d+$|^\d+\.$/.test(s)) return NaN; return parseFloat(s); }
  function inr(x){ return (x < 0 ? '&minus;' : '') + '₹' + Math.abs(x).toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); }
  function inrT(x){ return (x < 0 ? '-' : '') + '₹' + Math.abs(x).toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2}); }
  function pc(r){ return (r < 0 ? '&minus;' : '') + Math.abs(Math.round(r * 100) / 100) + '%'; }
  function pcT(r){ return (Math.round(r * 100) / 100) + '%'; }
  // Core maths. cost and net price are before GST. Returns profit, margin %, markup % (null if cost is 0).
  function calc(cost, net){
    var p = net - cost;
    return {net: net, profit: p, margin: net > 0 ? p / net * 100 : null, markup: cost > 0 ? p / cost * 100 : null};
  }
  function priceFor(mode, cost, v){ return mode === 'margin' ? cost / (1 - v / 100) : cost * (1 + v / 100); }
  window.__pm = {calc: calc, priceFor: priceFor};

  var LAB = {price: ['Selling price per unit', 'in rupees'], margin: ['Margin I want', 'percent of the selling price before GST'], markup: ['Markup I add', 'percent added on top of cost']};
  var DEF = {price: '1180', margin: '40', markup: '50'};
  var summary = '';
  function setLabel(){
    var m = $('pmMode').value, l = document.querySelector('label[for="pmVal"]');
    l.innerHTML = LAB[m][0] + ' <em>' + LAB[m][1] + '</em>';
    $('pmIncWrap').style.display = m === 'price' && $('pmGst').value !== '0' ? '' : 'none';
  }
  function clear(){ ['pmMargin', 'pmMarkup', 'pmProfit'].forEach(function(i){ $(i).textContent = '…'; }); $('pmBreak').innerHTML = ''; $('pmMore').innerHTML = ''; summary = ''; }

  function run(){
    setLabel();
    var cost = num($('pmCost').value), mode = $('pmMode').value, v = num($('pmVal').value), g = parseFloat($('pmGst').value), qRaw = $('pmQty').value.trim(), qty = qRaw ? num(qRaw) : 0;
    if (!(cost >= 0)) { say('pmNote', 'bad', 'Enter the cost per unit in rupees, for example 600.'); clear(); return; }
    if (!(v >= 0)) { say('pmNote', 'bad', mode === 'price' ? 'Enter the selling price in rupees, for example 1180.' : 'Enter a percentage, for example 40.'); clear(); return; }
    if (mode === 'margin' && v >= 100) { say('pmNote', 'bad', 'A margin must be below 100%. At 100% the cost would have to be zero. If you meant to double your cost, choose Markup and enter 100.'); clear(); return; }
    if (qRaw && !(qty >= 0)) { say('pmNote', 'bad', 'Units sold must be a number, for example 100. Leave it empty to skip totals.'); clear(); return; }
    var net, gross;
    if (mode === 'price') {
      if ($('pmInc').checked && g > 0) { gross = v; net = v * 100 / (100 + g); } else { net = v; gross = v * (1 + g / 100); }
    } else { net = priceFor(mode, cost, v); gross = net * (1 + g / 100); }
    if (mode === 'price' && net === 0) { say('pmNote', 'bad', 'The selling price must be more than zero.'); clear(); return; }
    var x = calc(cost, net);
    $('pmMargin').innerHTML = x.margin === null ? 'n/a' : pc(x.margin);
    $('pmMarkup').innerHTML = x.markup === null ? 'n/a' : pc(x.markup);
    $('pmProfit').innerHTML = inr(x.profit);

    var rows = '<tr><td>Cost per unit</td><td class="num">' + inr(cost) + '</td></tr>' +
      '<tr><td>Selling price before GST</td><td class="num">' + inr(net) + '</td></tr>';
    if (g > 0) rows += '<tr><td>GST at ' + pc(g) + '</td><td class="num">' + inr(gross - net) + '</td></tr><tr><td>Price the customer pays</td><td class="num">' + inr(gross) + '</td></tr>';
    rows += '<tr class="hit"><td>Profit per unit</td><td class="num">' + inr(x.profit) + '</td></tr>';
    if (qty > 0) rows += '<tr><td>Revenue for ' + fmtN(qty) + ' units (before GST)</td><td class="num">' + inr(net * qty) + '</td></tr>' +
      '<tr><td>Total cost for ' + fmtN(qty) + ' units</td><td class="num">' + inr(cost * qty) + '</td></tr>' +
      '<tr class="hit"><td>Total profit for ' + fmtN(qty) + ' units</td><td class="num">' + inr(x.profit * qty) + '</td></tr>';
    $('pmBreak').innerHTML = '<table class="rtable" style="margin-bottom:16px"><tbody>' + rows + '</tbody></table>';

    if (x.profit < 0) say('pmNote', 'bad', 'You lose <strong>' + inr(-x.profit) + '</strong> on every unit. To break even, sell for at least <strong>' + inr(cost) + '</strong> before GST' + (g > 0 ? ' (' + inr(cost * (1 + g / 100)) + ' with GST)' : '') + '.');
    else if (x.profit === 0) say('pmNote', 'warn', 'You break even: the price covers the cost, with no profit left over.');
    else say('pmNote', 'ok', 'You keep <strong>' + inr(x.profit) + '</strong> from every sale, a <strong>' + pc(x.margin) + ' margin</strong>' + (x.markup === null ? '' : ' and a <strong>' + pc(x.markup) + ' markup</strong> on cost') + '.' + (g > 0 ? ' GST of ' + inr(gross - net) + ' goes to the government, so it is left out of your margin.' : ''));

    var more = '';
    if (x.profit > 0) {
      more += '<table class="rtable" style="margin-bottom:16px"><tbody>' +
        '<tr><td>Biggest discount before you make a loss</td><td class="num">' + pc(x.margin) + '</td></tr>' +
        '<tr><td>Break even ROAS (ad revenue needed per ₹1 of ad spend)</td><td class="num">' + (Math.round(net / x.profit * 100) / 100) + '</td></tr>' +
        '<tr><td>Most you can spend on ads per sale and still break even</td><td class="num">' + inr(x.profit) + '</td></tr></tbody></table>';
    }
    var tr = '';
    [10, 20, 25, 30, 40, 50, 60].forEach(function(m){
      var n = priceFor('margin', cost, m), hit = x.margin !== null && Math.abs(x.margin - m) < 0.005;
      tr += '<tr' + (hit ? ' class="hit"' : '') + '><td>' + m + '%</td><td class="num">' + pc(m / (100 - m) * 100) + '</td><td class="num">' + inr(n) + '</td>' + (g > 0 ? '<td class="num">' + inr(n * (1 + g / 100)) + '</td>' : '') + '<td class="num">' + inr(n - cost) + '</td></tr>';
    });
    more += '<h3 style="font-size:16px;margin:4px 0 8px">Price for Common Margins at This Cost</h3><div style="overflow-x:auto"><table class="rtable"><thead><tr><th>Margin</th><th class="num">Markup</th><th class="num">Price before GST</th>' + (g > 0 ? '<th class="num">With GST</th>' : '') + '<th class="num">Profit</th></tr></thead><tbody>' + tr + '</tbody></table></div>';
    $('pmMore').innerHTML = more;

    summary = 'Profit margin calculation\nCost per unit: ' + inrT(cost) + '\nSelling price before GST: ' + inrT(net) +
      (g > 0 ? '\nGST at ' + pcT(g) + ': ' + inrT(gross - net) + '\nPrice with GST: ' + inrT(gross) : '') +
      '\nProfit per unit: ' + inrT(x.profit) + '\nMargin: ' + (x.margin === null ? 'n/a' : pcT(x.margin)) + '\nMarkup: ' + (x.markup === null ? 'n/a' : pcT(x.markup)) +
      (qty > 0 ? '\nTotal profit for ' + fmtN(qty) + ' units: ' + inrT(x.profit * qty) : '');
  }

  $('pmMode').addEventListener('change', function(){ $('pmVal').value = DEF[this.value]; run(); });
  ['pmCost', 'pmVal', 'pmQty'].forEach(function(i){ $(i).addEventListener('input', run); });
  ['pmGst', 'pmInc'].forEach(function(i){ $(i).addEventListener('change', run); });
  $('pmCopy').onclick = function(){ if (summary) copyText(summary, 'toast'); };
  run();
''',
        content=f'''
    <h2>What Is a Profit Margin Calculator?</h2>
    <p>A profit margin calculator shows how much of each sale you actually keep. You enter what a product or service costs you and what you charge for it, and it tells you your profit in rupees, your margin as a share of the price, and your markup as a share of the cost.</p>
    <p>It also works the other way round. Pick the margin you want, say 40%, and it gives you the selling price that delivers it. That is the step most people get wrong, because adding 40% to your cost does not give you a 40% margin.</p>
    <p>Built for Indian sellers, it handles GST for you. GST is money you collect for the government, not income, so the calculator takes it out of the price before working out your margin, and shows the final price your customer pays at 5%, 18% or 40%.</p>

    <h2>How to Use the Profit Margin Calculator</h2>
    <ol>
      <li><strong>Enter your cost per unit.</strong> Include everything it takes to make or buy one unit: purchase price, packing, shipping and platform fees.</li>
      <li><strong>Choose what you know.</strong> Pick Selling price to check a price you already use, Margin I want to find a new price, or Markup I add if you price by adding a percentage to cost.</li>
      <li><strong>Enter the price or percentage.</strong> A sample is filled in: a ₹600 product sold for ₹1,180 including 18% GST.</li>
      <li><strong>Set the GST rate</strong> and say whether your price already includes it.</li>
      <li><strong>Add units sold</strong> to see total revenue, cost and profit.</li>
      <li><strong>Read the result</strong>, then copy the summary for your price list or a client.</li>
    </ol>

    <h2>Margin and Markup Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Figure', 'Formula', 'Example: cost ₹600, price ₹1,000')}
      <tbody>
        <tr><td>Profit</td><td>Price &minus; cost</td><td>₹400</td></tr>
        <tr><td>Margin</td><td>Profit &divide; price &times; 100</td><td>40%</td></tr>
        <tr><td>Markup</td><td>Profit &divide; cost &times; 100</td><td>66.67%</td></tr>
        <tr><td>Price for a target margin</td><td>Cost &divide; (1 &minus; margin)</td><td>₹600 &divide; 0.6 = ₹1,000</td></tr>
        <tr><td>Markup from margin</td><td>Margin &divide; (1 &minus; margin)</td><td>0.4 &divide; 0.6 = 66.67%</td></tr>
        <tr><td>Break even ROAS</td><td>1 &divide; margin</td><td>1 &divide; 0.4 = 2.5</td></tr>
      </tbody>
    </table></div>
    <p>Margin can never reach 100%, but markup has no ceiling. A 100% markup, doubling your cost, gives a 50% margin. You can check these definitions in the <a href="https://www.xero.com/us/glossary/margin-vs-markup/" {EXT}>Xero guide to margin and markup</a>.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Price from margin, not markup.</strong> If you want a 30% margin on a ₹700 cost, the price is ₹1,000, not ₹910.</li>
      <li><strong>Know your discount limit.</strong> Your margin is the biggest percentage discount you can give before you sell at a loss. At a 25% margin, a 30% off sale loses money on every unit.</li>
      <li><strong>Count every cost.</strong> Marketplace commission, payment gateway fees, packaging and returns all come out of your margin. Leave them out and your real margin is lower than it looks.</li>
      <li><strong>Keep GST out of your figures.</strong> Report revenue and margin on the price before GST, as your accounts and GA4 should.</li>
      <li><strong>Link margin to ad spend.</strong> Your break even ROAS is one divided by your margin. At a 40% margin, ads must bring back ₹2.50 for every rupee spent just to break even.</li>
      <li><strong>Your figures stay private.</strong> Everything runs in your browser. Nothing you enter is uploaded or saved.</li>
    </ul>

    <h2>Margins and Your Marketing</h2>
    <p>Margin decides how hard your ads can push. If you bid on conversion value, feed real profit into your bidding, as explained in <a href="{B}value-based-bidding-google-ads-explained/">value based bidding in Google Ads</a>, and send clean revenue without tax using our <a href="{B}ga4-ecommerce-events-examples/">GA4 ecommerce events examples</a>. Raising your conversion rate is often the cheapest way to lift profit, so see our guide to <a href="{B}conversion-rate-optimization/">conversion rate optimization</a>. Need the tax figures for an invoice? Use the <a href="{T}gst-calculator/">GST calculator</a>, then check your ad targets with the <a href="{PP}break-even-roas-calculator/">break even ROAS calculator</a>.</p>
''',
        faqs=[
            ("What is the difference between margin and markup?", "Both use the same profit, but divide it by different numbers. Margin is profit divided by the selling price, and markup is profit divided by the cost. A product that costs ₹600 and sells for ₹1,000 has a 40% margin and a 66.67% markup."),
            ("How do I find the selling price for a 30% margin?", "Divide your cost by 1 minus the margin. For a 30% margin on a ₹700 cost, that is ₹700 divided by 0.7, which is ₹1,000. Choose Margin I want in the calculator, enter 30, and it does this for you, with GST added on top if you need it."),
            ("Should I include GST when working out my profit margin?", "No. GST is collected on behalf of the government and passed on, so it is not your income. Work out margin on the price before GST. If your price includes 18% GST, divide it by 1.18 first, which the calculator does when you tick the includes GST box."),
            ("What is a good profit margin?", "It depends on your industry. Grocery and electronics resellers often work on thin margins, while software, services and own brand products can run far higher. Compare against businesses like yours, and make sure your margin covers your ad costs, returns and overheads."),
        ],
        related=[("Value Based Bidding in Google Ads Explained", "value-based-bidding-google-ads-explained"), ("GA4 Ecommerce Events Examples", "ga4-ecommerce-events-examples"),
                 ("Conversion Rate Optimization", "conversion-rate-optimization"), ("Digital Marketing Tips 2026", "digital-marketing-tips-2026")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'business-calculators'; t['updated'] = '2026-11-22'
