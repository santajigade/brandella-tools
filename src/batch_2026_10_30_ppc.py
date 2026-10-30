"""Batch 4 (2026-10-30): PPC Calculators category, 7 calculators.
Formulas follow Google Ads Help definitions (checked 2026-10-30): CTR = clicks / impressions (answer 2615875),
avg CPC = cost / clicks (14074), avg CPA = cost / conversions (6396841), target ROAS % = value / spend x 100 (6268637),
monthly charging limit = 30.4 x average daily budget and daily spend up to 2x (1704424), CPM per 1,000 impressions (6310)."""

GA = 'https://support.google.com/google-ads/answer/'
P = 'https://brandella.in/tools/ppc-calculators/'
B = 'https://brandella.in/'
TH = '<thead><tr style="background:#2b2b2b !important;">'
def th(*cols):
    return TH + ''.join(f'<th style="background:#2b2b2b !important; color:#ffffff !important;">{c}</th>' for c in cols) + '</tr></thead>'

def F(i, label, val='', em='', tag='input', opts=None, wid='', ph=''):
    lab = f'<label for="{i}">{label}' + (f' <em>{em}</em>' if em else '') + '</label>'
    if tag == 'select':
        o = ''
        for x in opts:
            v, t = (x, x) if isinstance(x, str) else x
            o += f'<option value="{v}"' + (' selected' if v == val else '') + f'>{t}</option>'
        ctl = f'<select id="{i}">{o}</select>'
    else:
        ctl = f'<input id="{i}" type="text" inputmode="decimal" autocomplete="off" value="{val}" placeholder="{ph}">'
    return f'<div class="field"' + (f' id="{wid}"' if wid else '') + f'>{lab}{ctl}</div>'

def R2(a, b): return f'<div class="row2">{a}{b}</div>'

CURS = [('INR', 'INR ₹'), ('USD', 'USD $'), ('EUR', 'EUR €'), ('GBP', 'GBP £'), ('AUD', 'AUD $'), ('CAD', 'CAD $'), ('AED', 'AED'), ('SGD', 'SGD $')]
def CUR(P_): return F(P_ + 'Cur', 'Currency', 'INR', tag='select', opts=CURS)

def S(i, label): return f'<div class="stat-box"><b id="{i}">0</b><span>{label}</span></div>'

def RES(P_, title, stats, tips):
    return f'''<div class="card" id="{P_}Res" style="min-width:0">
      <h2>{title}</h2>
      <div class="stats">{''.join(S(i, l) for i, l in stats)}</div>
      <div class="kw-result" id="{P_}Verdict"></div>
      <div class="actions"><button class="btn dark" id="{P_}Copy">Copy Results</button><span class="toast" id="toast">Copied!</span></div>
      <div class="tips"><strong>Good to know</strong><ul>{tips}</ul></div>
    </div>'''

def EXTRA(title, inputs, stats, vid, after=''):
    return f'''<div class="card full" style="min-width:0">
      <h2>{title}</h2>
      {inputs}
      <div class="stats">{''.join(S(i, l) for i, l in stats)}</div>
      <div class="kw-result" id="{vid}"></div>{after}
    </div>'''

CJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function n(id){ var s = v(id).replace(/[,\s]/g,'').replace(/^[₹$€£]/,'').replace(/%$/,''); return /^\d*\.?\d+$/.test(s) ? parseFloat(s) : NaN; }
  function n0(id){ var x = n(id); return isFinite(x) ? x : 0; }
  function loc(c){ return c === 'INR' ? 'en-IN' : 'en-US'; }
  function money(x, c){
    if (!isFinite(x)) return '…';
    var a = Math.abs(x), r2 = Math.round(a * 100) / 100, dec = a < 100 && r2 % 1 !== 0 ? 2 : 0;
    try { return new Intl.NumberFormat(loc(c), {style:'currency', currency:c, minimumFractionDigits:dec, maximumFractionDigits:dec}).format(x); }
    catch(e){ return c + ' ' + x.toFixed(dec); }
  }
  function num(x, d, c){ return isFinite(x) ? new Intl.NumberFormat(loc(c || 'USD'), {maximumFractionDigits: d || 0}).format(x) : '…'; }
  function pct(x, d){ return isFinite(x) ? num(x, d === undefined ? 2 : d) + '%' : '…'; }
  function plain(x, d){ return isFinite(x) ? String(+x.toFixed(d === undefined ? 4 : d)) : ''; }
  function set(id, t){ $(id).textContent = t; }
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function wire(P, run){
    var f = $(P + 'Form'); f.addEventListener('input', run); f.addEventListener('change', run);
    $(P + 'Copy').onclick = function(){
      var out = [];
      f.querySelectorAll('.card').forEach(function(card){
        card.querySelectorAll('.stat-box').forEach(function(b){ out.push(b.querySelector('span').textContent + ': ' + b.querySelector('b').textContent); });
        card.querySelectorAll('.kw-result').forEach(function(k){ if (k.textContent.trim()) out.push(k.textContent.trim()); });
      });
      copyText(out.join('\n'), 'toast');
    };
    run();
  }
  function solveMode(ids, target){
    ids.forEach(function(id){ var e = $(id); e.readOnly = (id === target); e.style.background = id === target ? '#f3f8ee' : ''; e.style.fontWeight = id === target ? '700' : ''; });
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. ROAS CALCULATOR ----------
    TOOLS.append(dict(
        slug='roas-calculator', short='RO', name='ROAS Calculator',
        card='Work out return on ad spend, profit after ads and the revenue you need to hit a target ROAS.',
        title='ROAS Calculator: Free Return on Ad Spend Calculator',
        desc='Free ROAS calculator. Enter ad spend and revenue to get ROAS as a ratio and percent, profit after ads, ROI and the revenue needed for your target ROAS.',
        h1='ROAS Calculator',
        lead='Enter what you spent on ads and the revenue they brought in. See your return on ad spend, whether you actually made a profit, and what a target ROAS means in real money.',
        tool='''<section class="tool" aria-label="ROAS calculator" id="roForm">
    <div class="card" style="min-width:0">
      <h2>Your Campaign Numbers</h2>
      ''' + CUR('ro') + '''
      ''' + R2(F('roSpend', 'Ad Spend', '50000'), F('roRev', 'Revenue From Ads', '215000', em='conversion value')) + '''
      ''' + F('roMargin', 'Gross Profit Margin', '40', em='% optional') + '''
      <p style="font-size:13.5px;color:#666">Margin is the share of each sale you keep after product and delivery costs. Add it to see real profit.</p>
    </div>
    ''' + RES('ro', 'Your ROAS', [('roX', 'ROAS'), ('roPct', 'ROAS Percent'), ('roBe', 'Break Even ROAS'), ('roProfit', 'Profit After Ads'), ('roRoi', 'Return on Ad Spend Profit')],
              '<li>Google Ads target ROAS is set as a percent, so 4x equals 400%</li><li>ROAS uses revenue, not profit, so always check it against your margin</li>') + '''
    ''' + EXTRA('Target ROAS Planner', R2(F('roTarget', 'Target ROAS', '400', em='% like Google Ads'), F('roPlan', 'Planned Ad Spend', '100000')) + F('roGoal', 'Revenue Goal', '600000', em='optional'),
                [('roNeed', 'Revenue Needed'), ('roMax', 'Max Spend for Goal'), ('roTp', 'Profit at Target')], 'roPlanV') + '''
  </section>''',
        js=CJS + r'''
  function run(){
    var c = v('roCur'), s = n('roSpend'), r = n('roRev'), m = n('roMargin'), ok = s > 0 && r >= 0;
    var roas = ok ? r / s : NaN, hasM = m > 0 && m <= 100;
    set('roX', isFinite(roas) ? num(roas, 2) + 'x' : '…');
    set('roPct', isFinite(roas) ? num(roas * 100, 0) + '%' : '…');
    var be = hasM ? 100 / m : NaN, profit = hasM && ok ? r * m / 100 - s : NaN;
    set('roBe', hasM ? num(be, 2) + 'x' : 'Add margin');
    set('roProfit', isFinite(profit) ? money(profit, c) : 'Add margin');
    set('roRoi', isFinite(profit) ? num(profit / s * 100, 0) + '%' : 'Add margin');
    if (!ok) say('roVerdict', 'bad', 'Enter an ad spend above zero and the revenue those ads brought in.');
    else if (v('roMargin') && !hasM) say('roVerdict', 'warn', 'Profit margin must be a number between 1 and 100.');
    else if (!hasM) say('roVerdict', '', 'Your ROAS is <strong>' + num(roas, 2) + 'x</strong>. Every ' + money(1, c) + ' of ad spend brought in ' + money(roas, c) + ' of revenue. Add your profit margin to see if that is profitable.');
    else if (profit >= 0) say('roVerdict', 'ok', '<strong>Profitable.</strong> Your ROAS of ' + num(roas, 2) + 'x is above your break even ROAS of ' + num(be, 2) + 'x, so these ads made ' + money(profit, c) + ' of gross profit after ad costs.');
    else say('roVerdict', 'bad', '<strong>Losing money.</strong> Your ROAS of ' + num(roas, 2) + 'x is below your break even ROAS of ' + num(be, 2) + 'x. After ad costs these ads lost ' + money(-profit, c) + '.');
    var t = n('roTarget'), ps = n('roPlan'), g = n('roGoal');
    var need = t > 0 && ps > 0 ? ps * t / 100 : NaN, mx = t > 0 && g > 0 ? g * 100 / t : NaN;
    var tp = hasM && t > 0 && ps > 0 ? ps * t / 100 * m / 100 - ps : NaN;
    set('roNeed', money(need, c)); set('roMax', g > 0 ? money(mx, c) : 'Add a goal'); set('roTp', hasM ? money(tp, c) : 'Add margin');
    if (!(t > 0)) say('roPlanV', 'warn', 'Enter a target ROAS as a percent, for example 400 for 4x.');
    else if (!(ps > 0)) say('roPlanV', 'warn', 'Enter the ad spend you plan to use.');
    else {
      var h = 'At a ' + num(t, 0) + '% target ROAS (' + num(t / 100, 2) + 'x), spending ' + money(ps, c) + ' must bring in ' + money(need, c) + ' in revenue.';
      if (g > 0) h += ' To reach ' + money(g, c) + ' in revenue you can spend up to ' + money(mx, c) + '.';
      if (hasM) h += tp >= 0 ? ' At your margin that leaves ' + money(tp, c) + ' of profit.' : ' At your margin that target still loses ' + money(-tp, c) + ', so aim for at least ' + num(be * 100, 0) + '%.';
      say('roPlanV', hasM && tp < 0 ? 'warn' : 'ok', h);
    }
  }
  wire('ro', run);
''',
        content='''
    <h2>What Is ROAS?</h2>
    <p>ROAS stands for return on ad spend. It tells you how much revenue your ads brought in for every unit of money you spent on them. If you spend ₹10,000 and the ads drive ₹40,000 in sales, your ROAS is 4, usually written as 4x or 400%.</p>
    <p>The formula is simple: <strong>ROAS = revenue from ads ÷ ad spend</strong>. Google Ads calls this conversion value per cost, and its <a href="''' + GA + '''6268637" target="_blank" rel="noopener">Target ROAS bidding guide</a> multiplies it by 100 to give a percent. That is why a target of 400% in Google Ads means 4x.</p>

    <h2>How to Use the ROAS Calculator</h2>
    <ol>
      <li><strong>Pick your currency</strong> and enter your total ad spend for the period.</li>
      <li><strong>Enter the revenue from those ads.</strong> In Google Ads this is the conversion value column. In Meta Ads Manager it is purchase conversion value.</li>
      <li><strong>Add your gross profit margin</strong> to see your break even ROAS and the real profit left after ad costs.</li>
      <li><strong>Use the planner</strong> to turn a target ROAS into the revenue you need, or the most you can spend to reach a revenue goal.</li>
    </ol>

    <h2>ROAS Formulas Used</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Result', 'Formula') + '''
      <tbody>
        <tr><td>ROAS</td><td>Revenue ÷ ad spend</td></tr>
        <tr><td>ROAS percent</td><td>Revenue ÷ ad spend × 100</td></tr>
        <tr><td>Break even ROAS</td><td>1 ÷ profit margin, so a 40% margin needs 2.5x</td></tr>
        <tr><td>Profit after ads</td><td>Revenue × margin minus ad spend</td></tr>
        <tr><td>Revenue needed</td><td>Planned spend × target ROAS</td></tr>
        <tr><td>Max spend for a goal</td><td>Revenue goal ÷ target ROAS</td></tr>
      </tbody>
    </table></div>

    <h2>What Is a Good ROAS?</h2>
    <p>There is no single good number. A ROAS of 3x is great for a store with a 60% margin and a loss for a store with a 25% margin. The right question is whether your ROAS is above your break even point. Work that out first, then set targets above it.</p>
    <ul>
      <li><strong>Low margin products</strong> such as electronics need a much higher ROAS than high margin products like cosmetics or digital goods.</li>
      <li><strong>Repeat buyers change the maths.</strong> If customers come back, a first order ROAS slightly under break even can still pay off over time.</li>
      <li><strong>Check attribution.</strong> Platforms often credit themselves for the same sale, so compare ad platform revenue with your own sales data.</li>
      <li><strong>Raise targets slowly.</strong> Jumping a Google Ads target ROAS too far at once can choke traffic.</li>
    </ul>

    <h2>Improve Your ROAS</h2>
    <p>To push ROAS up, cut wasted clicks with <a href="''' + B + '''google-ads-negative-keywords/">negative keywords</a>, send real sale values with <a href="''' + B + '''value-based-bidding-google-ads-explained/">value based bidding</a>, and read our <a href="''' + B + '''25-google-ads-optimization-tips/">Google Ads optimization tips</a>. To find the exact ROAS you must beat, use the <a href="''' + P + '''break-even-roas-calculator/">break even ROAS calculator</a>.</p>
''',
        faqs=[
            ("How do I calculate ROAS?", "Divide the revenue your ads generated by what you spent on those ads. For example, ₹2,15,000 in revenue from ₹50,000 of spend is a ROAS of 4.3x, or 430%."),
            ("What is the difference between ROAS and ROI?", "ROAS compares revenue with ad spend only. ROI looks at profit, so it subtracts product costs and ad spend first. A campaign can have a healthy looking ROAS and still lose money if margins are thin."),
            ("Why does Google Ads show ROAS as a percent?", "Google Ads multiplies conversion value per cost by 100. So a target ROAS of 500% means you want 5 in sales for every 1 you spend on ads."),
            ("Is my campaign data sent anywhere?", "No. This ROAS calculator runs entirely in your browser. Nothing you type is uploaded or stored."),
        ],
        related=[("Value Based Bidding Explained", "value-based-bidding-google-ads-explained"), ("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"),
                 ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard"), ("Attribution Models Explained", "attribution-models-explained-digital-marketers")],
    ))

    # ---------- 2. BREAK EVEN ROAS CALCULATOR ----------
    TOOLS.append(dict(
        slug='break-even-roas-calculator', short='BE', name='Break Even ROAS Calculator',
        card='Find the minimum ROAS and maximum CPA you can afford from your price, costs and fees.',
        title='Break Even ROAS Calculator: Find Your Minimum ROAS',
        desc='Free break even ROAS calculator. Enter price, product cost, shipping and fees to find your minimum ROAS, break even CPA and the target ROAS for real profit.',
        h1='Break Even ROAS Calculator',
        lead='Enter your selling price and costs per order. Get the lowest ROAS your ads can run at without losing money, plus the target ROAS you need for the profit you want.',
        tool='''<section class="tool" aria-label="Break even ROAS calculator" id="beForm">
    <div class="card" style="min-width:0">
      <h2>Price and Costs per Order</h2>
      ''' + CUR('be') + '''
      ''' + R2(F('bePrice', 'Average Order Value', '1999', em='selling price'), F('beCogs', 'Product Cost', '700', em='per order')) + '''
      ''' + R2(F('beShip', 'Shipping and Packing', '120', em='per order'), F('beFee', 'Payment and Platform Fees', '2', em='% of price')) + '''
      ''' + R2(F('beOther', 'Other Costs per Order', '50', em='returns, COD'), F('beTarget', 'Profit You Want', '10', em='% of revenue')) + '''
    </div>
    ''' + RES('be', 'Your Break Even Point', [('beProfit', 'Profit per Order Before Ads'), ('beMargin', 'Margin'), ('beRoas', 'Break Even ROAS'), ('beRoasP', 'Break Even ROAS %'), ('beCpa', 'Break Even CPA'), ('beT', 'Target ROAS'), ('beTc', 'Target CPA')],
              '<li>Below break even ROAS, every sale from ads loses money</li><li>Use the target ROAS percent directly in Google Ads bidding</li>') + '''
    <div class="card full" style="min-width:0">
      <h2>Profit at Different ROAS Levels</h2>
      <p style="font-size:14px;color:#666;margin-bottom:10px" id="beNote"></p>
      <div style="overflow-x:auto"><table class="rtable" id="beTable"></table></div>
    </div>
  </section>''',
        js=CJS + r'''
  function run(){
    var c = v('beCur'), p = n('bePrice'), cg = n0('beCogs'), sh = n0('beShip'), f = n0('beFee'), o = n0('beOther'), t = n0('beTarget');
    var ids = ['beProfit','beMargin','beRoas','beRoasP','beCpa','beT','beTc'];
    if (!(p > 0)){ ids.forEach(function(i){ set(i, '…'); }); say('beVerdict', 'bad', 'Enter your average order value, the price a customer pays per order.'); $('beTable').innerHTML = ''; return; }
    var fees = p * f / 100, pr = p - cg - sh - fees - o, mg = pr / p;
    set('beProfit', money(pr, c)); set('beMargin', pct(mg * 100, 1));
    if (pr <= 0){
      ['beRoas','beRoasP','beCpa','beT','beTc'].forEach(function(i){ set(i, 'None'); });
      say('beVerdict', 'bad', '<strong>Each order loses ' + money(-pr, c) + ' before any ad spend.</strong> No ROAS can make this profitable. Raise the price or cut costs first.');
      $('beTable').innerHTML = ''; $('beNote').textContent = ''; return;
    }
    var be = 1 / mg, tm = mg - t / 100;
    set('beRoas', num(be, 2) + 'x'); set('beRoasP', num(be * 100, 0) + '%'); set('beCpa', money(pr, c));
    if (t > 0 && tm <= 0){ set('beT', 'Not possible'); set('beTc', 'Not possible'); }
    else { set('beT', num(1 / tm, 2) + 'x'); set('beTc', money(pr - p * t / 100, c)); }
    var h = 'You keep ' + money(pr, c) + ' from each ' + money(p, c) + ' order, a ' + pct(mg * 100, 1) + ' margin. Your ads must earn at least <strong>' + num(be, 2) + 'x ROAS</strong> (' + num(be * 100, 0) + '% in Google Ads) and cost no more than ' + money(pr, c) + ' per sale to break even.';
    if (t > 0) h += tm > 0 ? ' For a ' + num(t, 1) + '% profit, aim for <strong>' + num(1 / tm, 2) + 'x</strong> (' + num(100 / tm, 0) + '%).' : ' A ' + num(t, 1) + '% profit is not possible at this margin, because it is higher than the margin itself.';
    say('beVerdict', t > 0 && tm <= 0 ? 'warn' : 'ok', h);
    var sp = 1000, levels = [1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8], hit = false;
    var rows = levels.map(function(r){
      var rev = sp * r, prof = rev * mg - sp, cls = '';
      if (!hit && prof >= 0){ cls = ' class="hit"'; hit = true; }
      return '<tr' + cls + '><td>' + num(r, 1) + 'x (' + num(r * 100, 0) + '%)</td><td class="num">' + money(rev, c) + '</td><td class="num">' + money(prof, c) + '</td><td class="num">' + pct(prof / rev * 100, 1) + '</td></tr>';
    });
    $('beNote').textContent = 'For every ' + money(sp, c) + ' of ad spend at your margin. The highlighted row is the first level that makes a profit.';
    $('beTable').innerHTML = '<thead><tr><th>ROAS</th><th class="num">Revenue</th><th class="num">Profit or Loss</th><th class="num">Net Margin</th></tr></thead><tbody>' + rows.join('') + '</tbody>';
  }
  wire('be', run);
''',
        content='''
    <h2>What Is Break Even ROAS?</h2>
    <p>Break even ROAS is the return on ad spend where your ads pay for themselves and nothing more. Above it, every sale from ads adds profit. Below it, every sale loses money once you pay for the product, delivery, fees and the ad.</p>
    <p>The formula is <strong>break even ROAS = 1 ÷ profit margin</strong>, where profit margin is the share of the selling price left after all the costs of one order, before ads. A 50% margin means you break even at 2x ROAS. A 25% margin means you need 4x.</p>

    <h2>How to Use This Calculator</h2>
    <ol>
      <li><strong>Enter your average order value.</strong> This is what a customer pays, after discounts.</li>
      <li><strong>Add product cost per order</strong>, including the cost of goods and any packaging or labels.</li>
      <li><strong>Add shipping, payment fees and other costs</strong> such as returns, cash on delivery charges or marketplace commission.</li>
      <li><strong>Enter the profit you want</strong> as a percent of revenue to get a target ROAS that leaves real money in the bank.</li>
      <li><strong>Read the table</strong> to see what each ROAS level means for profit per ₹1,000 of ad spend.</li>
    </ol>

    <h2>What Each Result Means</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Result', 'Formula', 'Use it for') + '''
      <tbody>
        <tr><td>Profit per order</td><td>Price minus all order costs</td><td>Your budget for winning one sale</td></tr>
        <tr><td>Break even ROAS</td><td>Price ÷ profit per order</td><td>The lowest ROAS you can accept</td></tr>
        <tr><td>Break even CPA</td><td>Profit per order</td><td>The most you can pay for one sale</td></tr>
        <tr><td>Target ROAS</td><td>1 ÷ (margin minus desired profit)</td><td>Your Google Ads or Meta goal</td></tr>
        <tr><td>Target CPA</td><td>Profit per order minus desired profit</td><td>Cost per purchase goals</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Using Break Even ROAS</h2>
    <ul>
      <li><strong>Count every cost.</strong> Forgetting returns or payment fees is the most common reason a "profitable" campaign loses money.</li>
      <li><strong>Use real order values.</strong> Take the average from your store reports, not the list price of your best seller.</li>
      <li><strong>Set Google Ads targets as a percent.</strong> A break even ROAS of 1.84x becomes 184% in <a href="''' + GA + '''6268637" target="_blank" rel="noopener">Target ROAS bidding</a>.</li>
      <li><strong>Think about lifetime value.</strong> If customers reorder, you can sometimes accept a first order ROAS near break even to grow faster.</li>
    </ul>

    <h2>Next Steps</h2>
    <p>Once you know your floor, check live results with the <a href="''' + P + '''roas-calculator/">ROAS calculator</a>. Learn how bidding works in <a href="''' + B + '''how-to-optimize-performance-max-campaign-step-by-step/">our Performance Max optimization guide</a> and <a href="''' + B + '''value-based-bidding-google-ads-explained/">value based bidding explained</a>, and track true order values with <a href="''' + B + '''ga4-ecommerce-events-examples/">GA4 ecommerce events</a>.</p>
''',
        faqs=[
            ("How do I calculate break even ROAS?", "Divide 1 by your profit margin before ads. If you keep 40% of each sale after product, shipping and fees, your break even ROAS is 1 ÷ 0.40 = 2.5x, or 250%."),
            ("Should I include shipping and fees?", "Yes. Include every cost that comes with one order: product, packing, shipping, payment fees, marketplace commission and an allowance for returns. Leaving any out makes your break even ROAS look lower than it really is."),
            ("What is the difference between break even ROAS and target ROAS?", "Break even ROAS is where you make zero profit. Target ROAS is higher, set so that you also keep the profit margin you want after ad costs."),
            ("Is my pricing data private?", "Yes. The break even ROAS calculator runs entirely in your browser. Your prices and costs are never uploaded."),
        ],
        related=[("Value Based Bidding Explained", "value-based-bidding-google-ads-explained"), ("Optimize Performance Max Step by Step", "how-to-optimize-performance-max-campaign-step-by-step"),
                 ("Meta Advantage Plus Campaigns", "meta-advantage-plus-campaigns"), ("GA4 Ecommerce Events Examples", "ga4-ecommerce-events-examples")],
    ))

    # ---------- 3. CPA CALCULATOR ----------
    TOOLS.append(dict(
        slug='cpa-calculator', short='CPA', name='CPA Calculator',
        card='Calculate cost per acquisition and the most you can afford to pay for a sale or lead.',
        title='CPA Calculator: Cost per Acquisition and Max CPA',
        desc='Free CPA calculator. Find your cost per acquisition, conversion rate and CPC, then work out the maximum CPA you can afford for each sale or lead.',
        h1='CPA Calculator',
        lead='Find out what each sale or lead really costs you, and compare it with the most you can afford to pay before a conversion stops being profitable.',
        tool='''<section class="tool" aria-label="CPA calculator" id="cpForm">
    <div class="card" style="min-width:0">
      <h2>Your Campaign Numbers</h2>
      ''' + CUR('cp') + '''
      ''' + R2(F('cpSpend', 'Ad Spend', '75000'), F('cpConv', 'Conversions', '150', em='sales or leads')) + '''
      ''' + F('cpClicks', 'Clicks', '3000', em='optional') + '''
    </div>
    ''' + RES('cp', 'Your Cost per Acquisition', [('cpCpa', 'CPA'), ('cpCr', 'Conversion Rate'), ('cpCpc', 'Average CPC')],
              '<li>Google Ads shows this as Cost / conv.</li><li>Leads and sales need separate CPA goals</li>') + '''
    ''' + EXTRA('Max CPA You Can Afford', R2(F('cpValue', 'Value per Conversion', '2500', em='order value'), F('cpMargin', 'Profit Margin', '45', em='%')) + F('cpClose', 'Leads That Become Customers', '100', em='% use 100 for online sales'),
                [('cpMax', 'Max CPA'), ('cpGap', 'Profit per Conversion'), ('cpTot', 'Total Profit After Ads')], 'cpMaxV') + '''
  </section>''',
        js=CJS + r'''
  function run(){
    var c = v('cpCur'), s = n('cpSpend'), cv = n('cpConv'), cl = n('cpClicks');
    var cpa = s >= 0 && cv > 0 ? s / cv : NaN, cr = cl > 0 && cv >= 0 ? cv / cl * 100 : NaN, cpc = cl > 0 && s >= 0 ? s / cl : NaN;
    set('cpCpa', money(cpa, c)); set('cpCr', cl > 0 ? pct(cr) : 'Add clicks'); set('cpCpc', cl > 0 ? money(cpc, c) : 'Add clicks');
    if (!(s >= 0) || !v('cpSpend')) say('cpVerdict', 'bad', 'Enter your total ad spend.');
    else if (!(cv > 0)) say('cpVerdict', 'warn', 'No conversions yet. You have spent ' + money(s, c) + ' without a conversion, so CPA cannot be calculated.');
    else if (cl > 0 && cv > cl) say('cpVerdict', 'warn', 'You have more conversions than clicks. That can happen when one click leads to several conversions, but check your conversion settings.');
    else say('cpVerdict', '', 'You paid <strong>' + money(cpa, c) + '</strong> for each of your ' + num(cv, 2, c) + ' conversions' + (cl > 0 ? ', from a ' + pct(cr) + ' conversion rate at ' + money(cpc, c) + ' per click.' : '.'));
    var val = n('cpValue'), m = n('cpMargin'), cls = n('cpClose');
    if (!isFinite(cls)) cls = 100;
    if (!(val > 0) || !(m > 0 && m <= 100) || !(cls > 0 && cls <= 100)){
      ['cpMax','cpGap','cpTot'].forEach(function(i){ set(i, '…'); });
      say('cpMaxV', 'warn', 'Enter the value of one conversion, your profit margin from 1 to 100, and the share of leads that become customers.'); return;
    }
    var mx = val * m / 100 * cls / 100, gap = mx - cpa;
    set('cpMax', money(mx, c)); set('cpGap', money(gap, c)); set('cpTot', isFinite(gap) ? money(gap * cv, c) : '…');
    if (!isFinite(cpa)) say('cpMaxV', '', 'You can pay up to <strong>' + money(mx, c) + '</strong> per conversion before you start losing money.');
    else if (gap >= 0) say('cpMaxV', 'ok', '<strong>Profitable.</strong> Your CPA of ' + money(cpa, c) + ' is under your max CPA of ' + money(mx, c) + ', leaving ' + money(gap, c) + ' profit per conversion. You have room to bid higher for more volume.');
    else say('cpMaxV', 'bad', '<strong>Too expensive.</strong> Your CPA of ' + money(cpa, c) + ' is ' + money(-gap, c) + ' above your max CPA of ' + money(mx, c) + '. Improve the conversion rate or cut costly keywords and placements.');
  }
  wire('cp', run);
''',
        content='''
    <h2>What Is CPA?</h2>
    <p>CPA means cost per acquisition, also called cost per action or cost per conversion. It is the average amount you pay in ads to get one result, such as a sale, a lead form, a sign up or a call.</p>
    <p>The formula is <strong>CPA = ad spend ÷ conversions</strong>. Google Ads defines <a href="''' + GA + '''6396841" target="_blank" rel="noopener">average CPA</a> the same way: total cost divided by the number of conversions. Spend ₹75,000 for 150 leads and your CPA is ₹500.</p>

    <h2>How to Use the CPA Calculator</h2>
    <ol>
      <li><strong>Enter your ad spend</strong> for a period, such as last month.</li>
      <li><strong>Enter conversions</strong> for the same period. Count only the action you care about.</li>
      <li><strong>Add clicks</strong> if you also want your conversion rate and average CPC.</li>
      <li><strong>Fill in the max CPA section</strong> with the value of one conversion, your margin and, for leads, how many become paying customers.</li>
      <li><strong>Compare the two numbers.</strong> If your CPA is under your max CPA, the campaign makes money.</li>
    </ol>

    <h2>CPA Formulas Explained</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Metric', 'Formula', 'Example') + '''
      <tbody>
        <tr><td>CPA</td><td>Spend ÷ conversions</td><td>₹75,000 ÷ 150 = ₹500</td></tr>
        <tr><td>Conversion rate</td><td>Conversions ÷ clicks × 100</td><td>150 ÷ 3,000 = 5%</td></tr>
        <tr><td>Average CPC</td><td>Spend ÷ clicks</td><td>₹75,000 ÷ 3,000 = ₹25</td></tr>
        <tr><td>Max CPA</td><td>Value × margin × lead close rate</td><td>₹2,500 × 45% × 100% = ₹1,125</td></tr>
      </tbody>
    </table></div>

    <h2>Tips to Lower Your CPA</h2>
    <ul>
      <li><strong>Fix the landing page first.</strong> Doubling your conversion rate halves your CPA without touching bids.</li>
      <li><strong>Cut wasted spend.</strong> Search terms that never convert push CPA up. Add them as negatives.</li>
      <li><strong>Set CPA goals per conversion type.</strong> A newsletter sign up and a purchase should never share one target.</li>
      <li><strong>Be careful with Target CPA bidding.</strong> Start your target near your recent CPA and move it in small steps, as Google suggests in its <a href="''' + GA + '''6268632" target="_blank" rel="noopener">Target CPA guide</a>.</li>
      <li><strong>Lead businesses must track quality.</strong> A cheap lead that never buys is worth nothing, so use the close rate field honestly.</li>
    </ul>

    <h2>Learn More</h2>
    <p>Read about <a href="''' + B + '''google-ads-bidding-change-target-cpa/">the Google Ads Target CPA bidding change</a>, improve results with <a href="''' + B + '''conversion-rate-optimization/">conversion rate optimization</a>, and grow lead volume with <a href="''' + B + '''how-to-generate-high-quality-leads-2026/">our lead generation guide</a>. Planning a new campaign? Turn your CPA into a budget with the <a href="''' + P + '''ppc-budget-calculator/">PPC budget calculator</a>.</p>
''',
        faqs=[
            ("How do you calculate CPA?", "Divide your total ad spend by the number of conversions. ₹75,000 spent for 150 conversions gives a CPA of ₹500."),
            ("What is a good CPA?", "A good CPA is one below your maximum affordable CPA, which is the profit you make from one conversion. For leads, multiply the value of a customer by your margin and by the share of leads that become customers."),
            ("Is CPA the same as cost per conversion?", "Yes, in practice. Google Ads labels it Cost / conv. Some people use cost per acquisition only for new customers, so check how your team defines a conversion."),
            ("Does this CPA calculator store my numbers?", "No. Everything is calculated in your browser and nothing is sent or saved."),
        ],
        related=[("Google Ads Target CPA Bidding Change", "google-ads-bidding-change-target-cpa"), ("Conversion Rate Optimization", "conversion-rate-optimization"),
                 ("Enhanced Conversions Explained", "enhanced-conversions-explained-setup-benefits"), ("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026")],
    ))

    # ---------- 4. CPC CALCULATOR ----------
    TOOLS.append(dict(
        slug='cpc-calculator', short='CPC', name='CPC Calculator',
        card='Solve for cost per click, total cost or clicks, and find your maximum CPC bid.',
        title='CPC Calculator: Cost per Click and Max CPC Bid',
        desc='Free CPC calculator. Find cost per click, total ad cost or expected clicks from any two numbers, and work out the max CPC bid your target CPA allows.',
        h1='CPC Calculator',
        lead='Enter any two of cost, clicks and CPC to get the third. Then use your target CPA and conversion rate to find the highest cost per click you can afford.',
        tool='''<section class="tool" aria-label="CPC calculator" id="ccForm">
    <div class="card" style="min-width:0">
      <h2>Your Numbers</h2>
      ''' + R2(F('ccFind', 'What Do You Want to Find?', 'cpc', tag='select', opts=[('cpc', 'Cost per click'), ('cost', 'Total cost'), ('clicks', 'Number of clicks')]), CUR('cc')) + '''
      ''' + F('ccCost', 'Total Ad Cost', '25000') + '''
      ''' + R2(F('ccClicks', 'Clicks', '1250'), F('ccCpc', 'Cost per Click', '20', em='CPC')) + '''
      <p style="font-size:13.5px;color:#666">The green box is the one being calculated.</p>
    </div>
    ''' + RES('cc', 'Result', [('ccRCpc', 'Average CPC'), ('ccRCost', 'Total Cost'), ('ccRClicks', 'Clicks')],
              '<li>Average CPC is usually lower than your max bid</li><li>Better Quality Score can lower what you pay per click</li>') + '''
    ''' + EXTRA('Max CPC Bid Calculator', R2(F('ccTcpa', 'Target CPA', '600', em='cost per conversion'), F('ccCr', 'Conversion Rate', '4', em='%')),
                [('ccMax', 'Max CPC'), ('ccNow', 'CPA at Your Current CPC')], 'ccMaxV') + '''
  </section>''',
        js=CJS + r'''
  function run(){
    var c = v('ccCur'), f = v('ccFind'), cost = n('ccCost'), cl = n('ccClicks'), cpc = n('ccCpc');
    var ids = {cpc:'ccCpc', cost:'ccCost', clicks:'ccClicks'}; solveMode(['ccCost','ccClicks','ccCpc'], ids[f]);
    var err = '';
    if (f === 'cpc'){ if (cost >= 0 && cl > 0) cpc = cost / cl; else { cpc = NaN; err = 'Enter a total cost and a number of clicks above zero.'; } $('ccCpc').value = plain(cpc, 2); }
    else if (f === 'cost'){ if (cl >= 0 && cpc >= 0) cost = cl * cpc; else { cost = NaN; err = 'Enter the number of clicks and the cost per click.'; } $('ccCost').value = plain(cost, 2); }
    else { if (cost >= 0 && cpc > 0) cl = Math.floor(cost / cpc); else { cl = NaN; err = 'Enter a total cost and a cost per click above zero.'; } $('ccClicks').value = plain(cl, 0); }
    set('ccRCpc', money(cpc, c)); set('ccRCost', money(cost, c)); set('ccRClicks', num(cl, 0, c));
    if (err) say('ccVerdict', 'bad', err);
    else if (f === 'cpc') say('ccVerdict', 'ok', 'You paid an average of <strong>' + money(cpc, c) + ' per click</strong> for ' + num(cl, 0, c) + ' clicks.');
    else if (f === 'cost') say('ccVerdict', 'ok', num(cl, 0, c) + ' clicks at ' + money(cpc, c) + ' each will cost about <strong>' + money(cost, c) + '</strong>.');
    else say('ccVerdict', 'ok', 'A budget of ' + money(cost, c) + ' at ' + money(cpc, c) + ' per click buys about <strong>' + num(cl, 0, c) + ' clicks</strong>.');
    var t = n('ccTcpa'), cr = n('ccCr');
    if (!(t > 0) || !(cr > 0 && cr <= 100)){ set('ccMax', '…'); set('ccNow', '…'); say('ccMaxV', 'warn', 'Enter a target CPA and a conversion rate between 0 and 100.'); return; }
    var mx = t * cr / 100, now = cpc > 0 ? cpc / (cr / 100) : NaN;
    set('ccMax', money(mx, c)); set('ccNow', money(now, c));
    if (!isFinite(now)) say('ccMaxV', '', 'To hit a ' + money(t, c) + ' CPA at a ' + pct(cr) + ' conversion rate, pay no more than <strong>' + money(mx, c) + '</strong> per click.');
    else if (cpc <= mx) say('ccMaxV', 'ok', 'Your CPC of ' + money(cpc, c) + ' is under the max of <strong>' + money(mx, c) + '</strong>. At a ' + pct(cr) + ' conversion rate each conversion costs about ' + money(now, c) + ', inside your ' + money(t, c) + ' target.');
    else say('ccMaxV', 'bad', 'Your CPC of ' + money(cpc, c) + ' is above the max of <strong>' + money(mx, c) + '</strong>. At a ' + pct(cr) + ' conversion rate each conversion costs about ' + money(now, c) + ', over your ' + money(t, c) + ' target.');
  }
  wire('cc', run);
''',
        content='''
    <h2>What Is CPC?</h2>
    <p>CPC means cost per click. It is what you pay, on average, each time someone clicks your ad. Google Ads reports it as <a href="''' + GA + '''14074" target="_blank" rel="noopener">average CPC</a>: the total cost of your clicks divided by the number of clicks.</p>
    <p>The basic formula is <strong>CPC = total cost ÷ clicks</strong>. Rearrange it and you can also find your total cost (clicks × CPC) or how many clicks a budget buys (cost ÷ CPC). This CPC calculator does all three.</p>

    <h2>How to Use the CPC Calculator</h2>
    <ol>
      <li><strong>Choose what you want to find</strong>: cost per click, total cost or clicks.</li>
      <li><strong>Fill in the other two boxes.</strong> The green box shows the answer.</li>
      <li><strong>Enter your target CPA and conversion rate</strong> in the second section to get your max CPC bid.</li>
      <li><strong>Compare</strong> your current CPC with the max. If it is higher, your conversions cost more than you can afford.</li>
    </ol>

    <h2>CPC Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('To find', 'Formula', 'Example') + '''
      <tbody>
        <tr><td>Average CPC</td><td>Cost ÷ clicks</td><td>₹25,000 ÷ 1,250 = ₹20</td></tr>
        <tr><td>Total cost</td><td>Clicks × CPC</td><td>1,250 × ₹20 = ₹25,000</td></tr>
        <tr><td>Clicks</td><td>Cost ÷ CPC</td><td>₹25,000 ÷ ₹20 = 1,250</td></tr>
        <tr><td>Max CPC</td><td>Target CPA × conversion rate</td><td>₹600 × 4% = ₹24</td></tr>
      </tbody>
    </table></div>

    <h2>Why Average CPC and Max CPC Differ</h2>
    <p>Your max CPC is the most you are willing to pay for a click. In the Google Ads auction you often pay less, because the price depends on the ad rank of the advertiser below you and on your own Quality Score. That is why average CPC is usually lower than your bid.</p>

    <h2>Tips to Lower Your CPC</h2>
    <ul>
      <li><strong>Raise Quality Score</strong> with tightly themed ad groups, relevant ads and a landing page that matches the search.</li>
      <li><strong>Try long tail keywords.</strong> They have less competition and often convert better.</li>
      <li><strong>Use bid adjustments</strong> to pay less on devices, times or locations that convert poorly.</li>
      <li><strong>Watch your max CPC.</strong> If a keyword needs a CPC above your max to show, it cannot hit your CPA target at its current conversion rate.</li>
    </ul>
    <p>Learn the mechanics in <a href="''' + B + '''how-google-ads-auction-works/">how the Google Ads auction works</a> and <a href="''' + B + '''google-ads-quality-score-explained/">Google Ads Quality Score explained</a>. Buying display or video on impressions instead? Compare prices with the <a href="''' + P + '''cpm-calculator/">CPM calculator</a>.</p>
''',
        faqs=[
            ("How do I calculate CPC?", "Divide your total ad cost by the number of clicks. ₹25,000 spent for 1,250 clicks is an average CPC of ₹20."),
            ("How do I find my maximum CPC bid?", "Multiply your target cost per conversion by your conversion rate. With a ₹600 target CPA and a 4% conversion rate, the most you should pay per click is ₹600 × 0.04 = ₹24."),
            ("Why is my average CPC lower than my bid?", "In the Google Ads auction you usually pay just enough to beat the ad rank of the next advertiser, so the actual cost per click is often below your max bid."),
            ("Is anything I enter saved?", "No. The CPC calculator works only in your browser and does not upload or store anything."),
        ],
        related=[("How the Google Ads Auction Works", "how-google-ads-auction-works"), ("Google Ads Quality Score Explained", "google-ads-quality-score-explained"),
                 ("Google Ads Negative Keywords", "google-ads-negative-keywords"), ("Search Campaign vs Performance Max", "search-campaign-vs-performance-max")],
    ))

    # ---------- 5. CPM CALCULATOR ----------
    TOOLS.append(dict(
        slug='cpm-calculator', short='CPM', name='CPM Calculator',
        card='Solve for CPM, cost or impressions, and convert between CPM and CPC using your CTR.',
        title='CPM Calculator: Cost per Thousand Impressions',
        desc='Free CPM calculator. Work out cost per thousand impressions, total campaign cost or impressions, and convert CPM to an effective CPC using your CTR.',
        h1='CPM Calculator',
        lead='Enter any two of cost, impressions and CPM to get the third. Then see what your CPM means per click, and whether buying on CPM or CPC is cheaper.',
        tool='''<section class="tool" aria-label="CPM calculator" id="cmForm">
    <div class="card" style="min-width:0">
      <h2>Your Numbers</h2>
      ''' + R2(F('cmFind', 'What Do You Want to Find?', 'cpm', tag='select', opts=[('cpm', 'CPM'), ('cost', 'Total cost'), ('imps', 'Impressions')]), CUR('cm')) + '''
      ''' + F('cmCost', 'Total Ad Cost', '12000') + '''
      ''' + R2(F('cmImp', 'Impressions', '400000'), F('cmCpm', 'CPM', '30', em='per 1,000')) + '''
      <p style="font-size:13.5px;color:#666">The green box is the one being calculated.</p>
    </div>
    ''' + RES('cm', 'Result', [('cmRCpm', 'CPM'), ('cmRCost', 'Total Cost'), ('cmRImp', 'Impressions'), ('cmROne', 'Cost per Impression')],
              '<li>The M in CPM is the Roman numeral for 1,000</li><li>Viewable CPM only counts ads that could actually be seen</li>') + '''
    ''' + EXTRA('CPM vs CPC', R2(F('cmCtr', 'Clickthrough Rate', '0.8', em='% CTR'), F('cmBid', 'CPC You Could Pay Instead', '5', em='optional')),
                [('cmEcpc', 'Effective CPC'), ('cmEcpm', 'CPM Equal to That CPC'), ('cmClicks', 'Expected Clicks')], 'cmVsV') + '''
  </section>''',
        js=CJS + r'''
  function run(){
    var c = v('cmCur'), f = v('cmFind'), cost = n('cmCost'), im = n('cmImp'), cpm = n('cmCpm');
    solveMode(['cmCost','cmImp','cmCpm'], {cpm:'cmCpm', cost:'cmCost', imps:'cmImp'}[f]);
    var err = '';
    if (f === 'cpm'){ if (cost >= 0 && im > 0) cpm = cost / im * 1000; else { cpm = NaN; err = 'Enter a total cost and impressions above zero.'; } $('cmCpm').value = plain(cpm, 2); }
    else if (f === 'cost'){ if (im >= 0 && cpm >= 0) cost = im / 1000 * cpm; else { cost = NaN; err = 'Enter impressions and a CPM.'; } $('cmCost').value = plain(cost, 2); }
    else { if (cost >= 0 && cpm > 0) im = Math.floor(cost / cpm * 1000); else { im = NaN; err = 'Enter a total cost and a CPM above zero.'; } $('cmImp').value = plain(im, 0); }
    set('cmRCpm', money(cpm, c)); set('cmRCost', money(cost, c)); set('cmRImp', num(im, 0, c));
    var one = cpm / 1000; set('cmROne', isFinite(one) ? (one < 0.01 ? num(one, 4) + ' ' + c : money(one, c)) : '…');
    if (err) say('cmVerdict', 'bad', err);
    else if (f === 'cpm') say('cmVerdict', 'ok', 'You paid <strong>' + money(cpm, c) + ' per 1,000 impressions</strong> for ' + num(im, 0, c) + ' impressions.');
    else if (f === 'cost') say('cmVerdict', 'ok', num(im, 0, c) + ' impressions at a ' + money(cpm, c) + ' CPM will cost about <strong>' + money(cost, c) + '</strong>.');
    else say('cmVerdict', 'ok', money(cost, c) + ' at a ' + money(cpm, c) + ' CPM buys about <strong>' + num(im, 0, c) + ' impressions</strong>.');
    var ctr = n('cmCtr'), bid = n('cmBid');
    if (!(ctr > 0 && ctr <= 100) || !isFinite(cpm)){ ['cmEcpc','cmEcpm','cmClicks'].forEach(function(i){ set(i, '…'); }); say('cmVsV', 'warn', 'Enter a clickthrough rate between 0 and 100 to convert CPM into cost per click.'); return; }
    var ecpc = cpm / (1000 * ctr / 100), ecpm = bid > 0 ? bid * ctr / 100 * 1000 : NaN, clicks = im * ctr / 100;
    set('cmEcpc', money(ecpc, c)); set('cmEcpm', bid > 0 ? money(ecpm, c) : 'Add a CPC'); set('cmClicks', num(clicks, 0, c));
    var h = 'At a ' + pct(ctr) + ' CTR, a ' + money(cpm, c) + ' CPM works out to <strong>' + money(ecpc, c) + ' per click</strong>, or about ' + num(clicks, 0, c) + ' clicks.';
    if (bid > 0) h += ' A ' + money(bid, c) + ' CPC equals a ' + money(ecpm, c) + ' CPM at this CTR, so <strong>' + (ecpc < bid ? 'buying on CPM is cheaper' : ecpc > bid ? 'buying on CPC is cheaper' : 'both cost the same') + '</strong> here.';
    say('cmVsV', 'ok', h);
  }
  wire('cm', run);
''',
        content='''
    <h2>What Is CPM?</h2>
    <p>CPM means cost per mille, or cost per thousand impressions. It is the price you pay for your ad to be shown 1,000 times. CPM is the standard way to price display, video, social and connected TV ads, and Google describes <a href="''' + GA + '''6310" target="_blank" rel="noopener">CPM bidding</a> as paying per one thousand views on the Display Network.</p>
    <p>The formula is <strong>CPM = total cost ÷ impressions × 1,000</strong>. Spend ₹12,000 for 4,00,000 impressions and your CPM is ₹30.</p>

    <h2>How to Use the CPM Calculator</h2>
    <ol>
      <li><strong>Pick what you want to find</strong>: CPM, total cost or impressions.</li>
      <li><strong>Enter the two numbers you know.</strong> The green box fills in the answer.</li>
      <li><strong>Add your CTR</strong> to see the effective cost per click hidden inside your CPM.</li>
      <li><strong>Add a CPC price</strong> to compare. The tool tells you whether CPM or CPC buying is cheaper at your CTR.</li>
    </ol>

    <h2>CPM Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('To find', 'Formula', 'Example') + '''
      <tbody>
        <tr><td>CPM</td><td>Cost ÷ impressions × 1,000</td><td>₹12,000 ÷ 4,00,000 × 1,000 = ₹30</td></tr>
        <tr><td>Total cost</td><td>Impressions ÷ 1,000 × CPM</td><td>4,00,000 ÷ 1,000 × ₹30 = ₹12,000</td></tr>
        <tr><td>Impressions</td><td>Cost ÷ CPM × 1,000</td><td>₹12,000 ÷ ₹30 × 1,000 = 4,00,000</td></tr>
        <tr><td>Effective CPC</td><td>CPM ÷ (1,000 × CTR)</td><td>₹30 ÷ (1,000 × 0.8%) = ₹3.75</td></tr>
        <tr><td>Effective CPM</td><td>CPC × CTR × 1,000</td><td>₹5 × 0.8% × 1,000 = ₹40</td></tr>
      </tbody>
    </table></div>

    <h2>When CPM Makes Sense</h2>
    <p>CPM buying suits awareness goals, where the aim is to be seen by as many of the right people as possible. If your goal is clicks or sales, the CPM vs CPC section shows the real price of a click. A low CPM with a tiny CTR can cost more per click than a simple CPC bid.</p>
    <ul>
      <li><strong>Compare like with like.</strong> CPMs vary a lot by country, audience, placement and season.</li>
      <li><strong>Watch frequency.</strong> Cheap impressions shown to the same people again and again lose impact.</li>
      <li><strong>Check viewability.</strong> An impression nobody could see is not worth paying for.</li>
      <li><strong>Test creatives.</strong> A better ad raises CTR, which lowers your effective CPC at the same CPM.</li>
    </ul>
    <p>Learn more about <a href="''' + B + '''google-display-network-targeting/">Google Display Network targeting</a>, <a href="''' + B + '''demand-gen-campaigns-explained/">Demand Gen campaigns</a> and <a href="''' + B + '''meta-advantage-plus-campaigns/">Meta Advantage Plus campaigns</a>. To measure how often people click, use the <a href="''' + P + '''ctr-calculator/">CTR calculator</a>.</p>
''',
        faqs=[
            ("How do you calculate CPM?", "Divide your total cost by the number of impressions, then multiply by 1,000. For example, ₹12,000 for 4,00,000 impressions is a CPM of ₹30."),
            ("What does the M in CPM stand for?", "M is the Roman numeral for 1,000, from the Latin word mille. CPM is the cost of 1,000 ad impressions."),
            ("How do I convert CPM to CPC?", "Divide CPM by 1,000 times your CTR. A ₹30 CPM with a 0.8% CTR gives ₹30 ÷ (1,000 × 0.008) = ₹3.75 per click."),
            ("Is my data private?", "Yes. The CPM calculator runs entirely in your browser. Nothing you enter is uploaded."),
        ],
        related=[("Google Display Network Targeting", "google-display-network-targeting"), ("Demand Gen Campaigns Explained", "demand-gen-campaigns-explained"),
                 ("Meta Advantage Plus Campaigns", "meta-advantage-plus-campaigns"), ("LinkedIn Ads Targeting", "linkedin-ads-targeting")],
    ))

    # ---------- 6. CTR CALCULATOR ----------
    TOOLS.append(dict(
        slug='ctr-calculator', short='CTR', name='CTR Calculator',
        card='Calculate clickthrough rate and check if one ad really beats another with a significance test.',
        title='CTR Calculator: Clickthrough Rate and A/B Test',
        desc='Free CTR calculator. Find clickthrough rate, clicks or impressions, then compare two ads to see if the CTR difference is statistically significant.',
        h1='CTR Calculator',
        lead='Work out your clickthrough rate from clicks and impressions, or solve for either one. Then compare two ads and see if the winner is real or just luck.',
        tool='''<section class="tool" aria-label="CTR calculator" id="ctForm">
    <div class="card" style="min-width:0">
      <h2>Your Numbers</h2>
      ''' + F('ctFind', 'What Do You Want to Find?', 'ctr', tag='select', opts=[('ctr', 'Clickthrough rate'), ('clicks', 'Clicks'), ('imps', 'Impressions needed')]) + '''
      ''' + R2(F('ctClicks', 'Clicks', '320'), F('ctImp', 'Impressions', '8000')) + '''
      ''' + F('ctCtr', 'CTR', '4', em='%') + '''
      <p style="font-size:13.5px;color:#666">The green box is the one being calculated.</p>
    </div>
    ''' + RES('ct', 'Result', [('ctRCtr', 'CTR'), ('ctRClicks', 'Clicks'), ('ctRImp', 'Impressions'), ('ctROne', 'Impressions per Click')],
              '<li>CTR is clicks divided by impressions</li><li>Compare CTR within the same network and campaign type</li>') + '''
    <div class="card full" style="min-width:0">
      <h2>Compare Two Ads</h2>
      ''' + R2(F('ctAi', 'Ad A Impressions', '5000'), F('ctAc', 'Ad A Clicks', '180')) + '''
      ''' + R2(F('ctBi', 'Ad B Impressions', '5200'), F('ctBc', 'Ad B Clicks', '240')) + '''
      <div class="stats">''' + S('ctA', 'Ad A CTR') + S('ctB', 'Ad B CTR') + S('ctLift', 'Difference') + S('ctConf', 'Confidence') + '''</div>
      <div class="kw-result" id="ctAbV"></div>
    </div>
  </section>''',
        js=CJS + r'''
  function phi(z){ var t = 1 / (1 + 0.2316419 * Math.abs(z)), d = 0.3989423 * Math.exp(-z * z / 2), p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return z > 0 ? 1 - p : p; }
  function run(){
    var f = v('ctFind'), cl = n('ctClicks'), im = n('ctImp'), ctr = n('ctCtr');
    solveMode(['ctClicks','ctImp','ctCtr'], {ctr:'ctCtr', clicks:'ctClicks', imps:'ctImp'}[f]);
    var err = '';
    if (f === 'ctr'){ if (im > 0 && cl >= 0 && cl <= im) ctr = cl / im * 100; else { ctr = NaN; err = im > 0 && cl > im ? 'Clicks cannot be higher than impressions.' : 'Enter clicks and impressions above zero.'; } $('ctCtr').value = plain(ctr, 2); }
    else if (f === 'clicks'){ if (im >= 0 && ctr >= 0 && ctr <= 100) cl = Math.round(im * ctr / 100); else { cl = NaN; err = 'Enter impressions and a CTR between 0 and 100.'; } $('ctClicks').value = plain(cl, 0); }
    else { if (cl >= 0 && ctr > 0 && ctr <= 100) im = Math.ceil(cl / (ctr / 100)); else { im = NaN; err = 'Enter clicks and a CTR above 0 and up to 100.'; } $('ctImp').value = plain(im, 0); }
    set('ctRCtr', pct(ctr)); set('ctRClicks', num(cl, 0)); set('ctRImp', num(im, 0)); set('ctROne', cl > 0 && isFinite(im) ? num(im / cl, 1) : '…');
    if (err) say('ctVerdict', 'bad', err);
    else if (f === 'ctr') say('ctVerdict', 'ok', num(cl, 0) + ' clicks from ' + num(im, 0) + ' impressions is a <strong>' + pct(ctr) + ' CTR</strong>' + (cl > 0 ? ', about 1 click every ' + num(im / cl, 1) + ' impressions.' : '.'));
    else if (f === 'clicks') say('ctVerdict', 'ok', num(im, 0) + ' impressions at a ' + pct(ctr) + ' CTR should bring about <strong>' + num(cl, 0) + ' clicks</strong>.');
    else say('ctVerdict', 'ok', 'To get ' + num(cl, 0) + ' clicks at a ' + pct(ctr) + ' CTR you need about <strong>' + num(im, 0) + ' impressions</strong>.');
    var ai = n('ctAi'), ac = n('ctAc'), bi = n('ctBi'), bc = n('ctBc');
    if (!(ai > 0 && bi > 0 && ac >= 0 && bc >= 0) || ac > ai || bc > bi){
      ['ctA','ctB','ctLift','ctConf'].forEach(function(i){ set(i, '…'); });
      say('ctAbV', 'warn', 'Enter impressions and clicks for both ads. Clicks cannot be higher than impressions.'); return;
    }
    var pa = ac / ai, pb = bc / bi, pool = (ac + bc) / (ai + bi);
    set('ctA', pct(pa * 100)); set('ctB', pct(pb * 100));
    set('ctLift', pa > 0 ? (pb >= pa ? '+' : '') + num((pb - pa) / pa * 100, 1) + '%' : '…');
    var se = Math.sqrt(pool * (1 - pool) * (1 / ai + 1 / bi));
    if (!(se > 0) || pa === pb){ set('ctConf', '0%'); say('ctAbV', 'warn', 'Both ads have the same CTR so far. Keep the test running.'); return; }
    var z = (pb - pa) / se, conf = (2 * phi(Math.abs(z)) - 1) * 100, win = pb > pa ? 'B' : 'A', lose = win === 'A' ? 'B' : 'A';
    set('ctConf', num(Math.min(conf, 99.9), 1) + '%');
    var pm = (pa + pb) / 2, need = Math.ceil(Math.pow(1.96 * Math.sqrt(2 * pm * (1 - pm)) + 0.8416 * Math.sqrt(pa * (1 - pa) + pb * (1 - pb)), 2) / Math.pow(pa - pb, 2));
    if (conf >= 95) say('ctAbV', 'ok', '<strong>Ad ' + win + ' wins.</strong> Its CTR is higher and we are ' + num(Math.min(conf, 99.9), 1) + '% confident the difference is real, not chance. Pause Ad ' + lose + ' or test a new challenger.');
    else say('ctAbV', 'warn', '<strong>Not significant yet.</strong> Ad ' + win + ' is ahead, but confidence is only ' + num(conf, 1) + '%, below the usual 95%. For a difference this size, plan on about ' + num(need, 0) + ' impressions per ad.');
  }
  wire('ct', run);
''',
        content='''
    <h2>What Is CTR?</h2>
    <p>CTR stands for clickthrough rate. It is the share of people who saw your ad, listing or email and then clicked it. Google Ads defines <a href="''' + GA + '''2615875" target="_blank" rel="noopener">clickthrough rate</a> as clicks divided by impressions, so 5 clicks from 100 impressions is a 5% CTR.</p>
    <p>The formula is <strong>CTR = clicks ÷ impressions × 100</strong>. The same maths works for search ads, display banners, social posts, organic results in Search Console and email links.</p>

    <h2>How to Use the CTR Calculator</h2>
    <ol>
      <li><strong>Choose what to find</strong>: the CTR, the clicks you can expect, or the impressions you need.</li>
      <li><strong>Enter the two numbers you know.</strong> The green box gives the answer.</li>
      <li><strong>Testing two ads?</strong> Enter impressions and clicks for each in the Compare Two Ads section.</li>
      <li><strong>Read the confidence.</strong> At 95% or more you can treat the winner as real. Below that, keep the test running.</li>
    </ol>

    <h2>How the Ad Comparison Works</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Result', 'What it means') + '''
      <tbody>
        <tr><td>Ad A and Ad B CTR</td><td>Clicks ÷ impressions for each ad</td></tr>
        <tr><td>Difference</td><td>How much higher or lower Ad B's CTR is than Ad A's, in percent</td></tr>
        <tr><td>Confidence</td><td>From a two proportion z test. 95% means a gap this big would rarely happen by chance</td></tr>
        <tr><td>Impressions per ad</td><td>Rough sample needed to confirm a gap of this size at 95% confidence and 80% power</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for a Better CTR</h2>
    <ul>
      <li><strong>Match the search.</strong> Put the main keyword in your headline so people see their query reflected back.</li>
      <li><strong>Give a reason to click</strong>: a price, an offer, free delivery or a clear benefit.</li>
      <li><strong>Use assets.</strong> Sitelinks, callouts and images make search ads bigger and more clickable.</li>
      <li><strong>Do not chase CTR alone.</strong> A high CTR with a low conversion rate wastes money. Judge ads on cost per conversion too.</li>
      <li><strong>Compare fairly.</strong> Search CTRs are normally far higher than display CTRs, so benchmark within one channel.</li>
    </ul>
    <p>For a full testing process read <a href="''' + B + '''ppc-ad-copy-testing/">PPC ad copy testing</a>, and see how CTR feeds into <a href="''' + B + '''google-ads-quality-score-explained/">Quality Score</a>. To check organic CTR, use our guide to the <a href="''' + B + '''search-console-performance-report/">Search Console performance report</a>. Turn clicks into a budget with the <a href="''' + P + '''ppc-budget-calculator/">PPC budget calculator</a>.</p>
''',
        faqs=[
            ("How do you calculate CTR?", "Divide clicks by impressions and multiply by 100. 320 clicks from 8,000 impressions is a 4% CTR."),
            ("What is a good CTR?", "It depends on the channel. Search ads usually earn a much higher CTR than display or social ads, and branded searches beat generic ones. Compare against your own past results in the same campaign type."),
            ("How many impressions do I need for an A/B test?", "It depends on how big the difference is. Small gaps need many thousands of impressions per ad. The tool estimates the number needed for 95% confidence based on your current CTRs."),
            ("Does the CTR calculator send my data anywhere?", "No. All the maths, including the significance test, runs in your browser."),
        ],
        related=[("PPC Ad Copy Testing", "ppc-ad-copy-testing"), ("Google Ads Quality Score Explained", "google-ads-quality-score-explained"),
                 ("Search Console Performance Report", "search-console-performance-report"), ("Title Tag Optimization", "title-tag-optimization")],
    ))

    # ---------- 7. PPC BUDGET CALCULATOR ----------
    TOOLS.append(dict(
        slug='ppc-budget-calculator', short='PB', name='PPC Budget Calculator',
        card='Turn a lead, sales or revenue goal into a monthly and daily ad budget, or forecast what a budget buys.',
        title='PPC Budget Calculator: Plan Your Google Ads Budget',
        desc='Free PPC budget calculator. Turn a conversion or revenue goal into a monthly and daily Google Ads budget, or forecast clicks and sales from a set budget.',
        h1='PPC Budget Calculator',
        lead='Tell us your goal, conversion rate and cost per click. Get the monthly and daily budget you need, plus the clicks, impressions, CPA and ROAS to expect.',
        tool='''<section class="tool" aria-label="PPC budget calculator" id="pbForm">
    <div class="card" style="min-width:0">
      <h2>Your Goal</h2>
      ''' + R2(F('pbMode', 'Plan From', 'conv', tag='select', opts=[('conv', 'A conversion goal'), ('rev', 'A revenue goal'), ('budget', 'A monthly budget')]), CUR('pb')) + '''
      ''' + F('pbConv', 'Conversions per Month', '60', em='sales or leads', wid='pbWConv') + '''
      ''' + F('pbRev', 'Revenue Goal per Month', '500000', wid='pbWRev') + '''
      ''' + F('pbBudget', 'Monthly Budget', '100000', wid='pbWBudget') + '''
      ''' + R2(F('pbCr', 'Conversion Rate', '3.5', em='%'), F('pbCpc', 'Average CPC', '25')) + '''
      ''' + R2(F('pbCtr', 'CTR', '5', em='% optional'), F('pbAov', 'Value per Conversion', '4000', em='optional', wid='pbWAov')) + '''
    </div>
    ''' + RES('pb', 'Your Budget Plan', [('pbMonth', 'Monthly Budget'), ('pbDay', 'Daily Budget'), ('pbClicks', 'Clicks'), ('pbConvR', 'Conversions'), ('pbImp', 'Impressions'), ('pbCpa', 'CPA'), ('pbRoas', 'ROAS')],
              '<li>Google Ads may spend up to 2 times your daily budget on busy days</li><li>Your monthly charge is capped at 30.4 times the daily budget</li>') + '''
    <div class="card full" style="min-width:0">
      <h2>What If Your Conversion Rate Changes?</h2>
      <div style="overflow-x:auto"><table class="rtable" id="pbTable"></table></div>
    </div>
  </section>''',
        js=CJS + r'''
  function calc(mode, goalC, goalR, bud, cr, cpc, aov){
    var o = {};
    if (mode === 'budget'){ o.budget = bud; o.clicks = Math.floor(bud / cpc); o.conv = o.clicks * cr; }
    else { o.conv = mode === 'rev' ? Math.ceil(goalR / aov) : goalC; o.clicks = Math.ceil(o.conv / cr); o.budget = o.clicks * cpc; }
    o.cpa = o.conv > 0 ? o.budget / o.conv : NaN; return o;
  }
  function run(){
    var c = v('pbCur'), mode = v('pbMode');
    $('pbWConv').style.display = mode === 'conv' ? '' : 'none';
    $('pbWRev').style.display = mode === 'rev' ? '' : 'none';
    $('pbWBudget').style.display = mode === 'budget' ? '' : 'none';
    $('pbWAov').querySelector('em').textContent = mode === 'rev' ? 'needed' : 'optional';
    var gc = n('pbConv'), gr = n('pbRev'), bud = n('pbBudget'), cr = n('pbCr'), cpc = n('pbCpc'), ctr = n('pbCtr'), aov = n('pbAov');
    var ids = ['pbMonth','pbDay','pbClicks','pbConvR','pbImp','pbCpa','pbRoas'], err = '';
    if (!(cr > 0 && cr <= 100)) err = 'Enter a conversion rate above 0 and up to 100.';
    else if (!(cpc > 0)) err = 'Enter your average cost per click.';
    else if (mode === 'conv' && !(gc > 0)) err = 'Enter how many conversions you want each month.';
    else if (mode === 'rev' && !(gr > 0)) err = 'Enter your monthly revenue goal.';
    else if (mode === 'rev' && !(aov > 0)) err = 'Enter the value per conversion, your average order value, to plan from revenue.';
    else if (mode === 'budget' && !(bud > 0)) err = 'Enter your monthly budget.';
    if (err){ ids.forEach(function(i){ set(i, '…'); }); say('pbVerdict', 'bad', err); $('pbTable').innerHTML = ''; return; }
    var o = calc(mode, gc, gr, bud, cr / 100, cpc, aov), day = o.budget / 30.4;
    var imp = ctr > 0 && ctr <= 100 ? Math.ceil(o.clicks / (ctr / 100)) : NaN, roas = aov > 0 ? o.conv * aov / o.budget : NaN;
    set('pbMonth', money(o.budget, c)); set('pbDay', money(day, c)); set('pbClicks', num(o.clicks, 0, c));
    set('pbConvR', num(o.conv, 1, c)); set('pbImp', ctr > 0 ? num(imp, 0, c) : 'Add CTR'); set('pbCpa', money(o.cpa, c));
    set('pbRoas', aov > 0 ? num(roas, 2) + 'x' : 'Add value');
    var h = mode === 'budget'
      ? 'A ' + money(o.budget, c) + ' monthly budget at ' + money(cpc, c) + ' per click buys about ' + num(o.clicks, 0, c) + ' clicks. At a ' + pct(cr) + ' conversion rate that is about <strong>' + num(o.conv, 1, c) + ' conversions</strong> a month.'
      : 'To get ' + num(o.conv, 0, c) + ' conversions' + (mode === 'rev' ? ' (' + money(gr, c) + ' in revenue)' : '') + ' at a ' + pct(cr) + ' conversion rate you need about ' + num(o.clicks, 0, c) + ' clicks. At ' + money(cpc, c) + ' per click that is <strong>' + money(o.budget, c) + ' a month</strong>.';
    h += ' Set an average daily budget of <strong>' + money(day, c) + '</strong>. Google may spend up to ' + money(day * 2, c) + ' on a busy day, but will not charge more than ' + money(day * 30.4, c) + ' in a month.';
    if (aov > 0 && roas < 1) h += ' Note: at this value per conversion the ads return less than they cost.';
    say('pbVerdict', aov > 0 && roas < 1 ? 'warn' : 'ok', h);
    var rows = [0.75, 1, 1.25].map(function(k){
      var r = calc(mode, gc, gr, bud, cr * k / 100, cpc, aov), lab = k === 1 ? 'Your rate' : (k < 1 ? '25% lower' : '25% higher');
      return '<tr' + (k === 1 ? ' class="hit"' : '') + '><td>' + lab + ' (' + pct(cr * k) + ')</td><td class="num">' + num(r.clicks, 0, c) + '</td><td class="num">' + num(r.conv, 1, c) + '</td><td class="num">' + money(r.budget, c) + '</td><td class="num">' + money(r.cpa, c) + '</td></tr>';
    });
    $('pbTable').innerHTML = '<thead><tr><th>Conversion Rate</th><th class="num">Clicks</th><th class="num">Conversions</th><th class="num">Monthly Budget</th><th class="num">CPA</th></tr></thead><tbody>' + rows.join('') + '</tbody>';
  }
  wire('pb', run);
''',
        content='''
    <h2>What Is a PPC Budget Calculator?</h2>
    <p>A PPC budget calculator works backwards from what you want to achieve. Instead of guessing a number, you start with a goal, such as 60 leads a month, and use your conversion rate and cost per click to find the budget that goal needs.</p>
    <p>The logic is simple: <strong>clicks needed = conversions ÷ conversion rate</strong>, and <strong>budget = clicks × CPC</strong>. You can also flip it and see what a fixed budget will buy.</p>

    <h2>How to Use the PPC Budget Calculator</h2>
    <ol>
      <li><strong>Choose how to plan</strong>: from a conversion goal, a revenue goal or a monthly budget you already have.</li>
      <li><strong>Enter your conversion rate and average CPC.</strong> Use your own account history. If you are new, use the Google Ads Keyword Planner for CPC estimates.</li>
      <li><strong>Add CTR</strong> to see how many impressions you need, and value per conversion to see expected ROAS.</li>
      <li><strong>Copy the daily budget</strong> into your campaign settings.</li>
      <li><strong>Check the table</strong> to see how much a better or worse conversion rate changes the plan.</li>
    </ol>

    <h2>How Google Ads Spends Your Daily Budget</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Rule', 'What it means for you') + '''
      <tbody>
        <tr><td>Average daily budget</td><td>Monthly budget ÷ 30.4, the average number of days in a month</td></tr>
        <tr><td>Daily overdelivery</td><td>On some days spend can reach up to 2 times your daily budget</td></tr>
        <tr><td>Monthly charging limit</td><td>You are not charged more than 30.4 times your average daily budget in a month</td></tr>
        <tr><td>Changing budget mid month</td><td>The limit is worked out again from the new budget for the rest of the month</td></tr>
      </tbody>
    </table></div>
    <p>These rules come from Google's help page on <a href="''' + GA + '''1704424" target="_blank" rel="noopener">managing your spend in Google Ads</a>.</p>

    <h2>Budget Planning Tips</h2>
    <ul>
      <li><strong>Start small and learn.</strong> Your first month tells you your real CPC and conversion rate. Plug those back in and plan again.</li>
      <li><strong>Leave room for learning.</strong> Smart bidding needs enough conversions to work well, so a tiny budget split across many campaigns rarely performs.</li>
      <li><strong>Budget by goal, not by habit.</strong> Give the most money to the campaigns with the lowest CPA or highest ROAS.</li>
      <li><strong>Plan for seasons.</strong> CPCs often rise during festivals and sale periods, so add a buffer.</li>
    </ul>
    <p>Read more about <a href="''' + B + '''google-ads-budget-pacing-update-2026/">Google Ads budget pacing</a>, compare <a href="''' + B + '''search-campaign-vs-performance-max/">Search and Performance Max</a>, and report results with a <a href="''' + B + '''paid-media-reporting-dashboard/">paid media reporting dashboard</a>. To check if the plan is profitable, use the <a href="''' + P + '''break-even-roas-calculator/">break even ROAS calculator</a>.</p>
''',
        faqs=[
            ("How do I calculate my Google Ads budget?", "Divide the conversions you want by your conversion rate to get the clicks you need, then multiply by your average CPC. 60 conversions at a 3.5% conversion rate needs about 1,715 clicks, which at ₹25 per click is about ₹42,875 a month."),
            ("How do I turn a monthly budget into a daily budget?", "Divide the monthly budget by 30.4, the average number of days in a month that Google Ads uses. A ₹1,00,000 monthly budget is a daily budget of about ₹3,289."),
            ("Can Google Ads spend more than my daily budget?", "Yes. On some days Google can spend up to 2 times your average daily budget, but over a month you will not be charged more than 30.4 times that daily budget."),
            ("Is my budget data stored?", "No. The PPC budget calculator runs fully in your browser and nothing you type is uploaded."),
        ],
        related=[("Google Ads Budget Pacing Update", "google-ads-budget-pacing-update-2026"), ("25 Google Ads Optimization Tips", "25-google-ads-optimization-tips"),
                 ("Search Campaign vs Performance Max", "search-campaign-vs-performance-max"), ("Paid Media Reporting Dashboard", "paid-media-reporting-dashboard")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'ppc-calculators'; t['updated'] = '2026-10-30'
