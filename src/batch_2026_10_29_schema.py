"""Batch 3 (2026-10-29): Schema Generators category, 7 JSON LD generators.
Properties follow Google Search Central structured data docs (checked 2026-10-29).
FAQ and HowTo generators are deliberately left out: Google no longer shows those rich results."""

G = 'https://developers.google.com/search/docs/appearance/structured-data/'
TH = '<thead><tr style="background:#2b2b2b !important;">'
def th(*cols):
    return TH + ''.join(f'<th style="background:#2b2b2b !important; color:#ffffff !important;">{c}</th>' for c in cols) + '</tr></thead>'

def F(i, label, val='', ph='', em='', tag='input', typ='text', opts=None, extra=''):
    lab = f'<label for="{i}">{label}' + (f' <em>{em}</em>' if em else '') + '</label>'
    if tag == 'select':
        o = ''
        for x in opts:
            v, t = (x, x) if isinstance(x, str) else x
            o += f'<option value="{v}"' + (' selected' if v == val else '') + f'>{t}</option>'
        ctl = f'<select id="{i}">{o}</select>'
    elif tag == 'textarea':
        ctl = f'<textarea id="{i}" placeholder="{ph}"{extra}>{val}</textarea>'
    else:
        ctl = f'<input id="{i}" type="{typ}" value="{val}" placeholder="{ph}"{extra}>'
    return f'<div class="field">{lab}{ctl}</div>'

def R2(a, b): return f'<div class="row2">{a}{b}</div>'

TZ = [('+05:30', '+05:30 India (IST)'), ('+00:00', '+00:00 UTC, London winter'), ('+01:00', '+01:00 London summer, Paris winter'),
      ('+02:00', '+02:00 Paris summer, Johannesburg'), ('+03:00', '+03:00 Riyadh, Nairobi'), ('+04:00', '+04:00 Dubai'),
      ('+05:00', '+05:00 Karachi'), ('+05:45', '+05:45 Kathmandu'), ('+06:00', '+06:00 Dhaka'), ('+07:00', '+07:00 Bangkok, Jakarta'),
      ('+08:00', '+08:00 Singapore, Perth'), ('+09:00', '+09:00 Tokyo'), ('+10:00', '+10:00 Sydney winter'), ('+11:00', '+11:00 Sydney summer'),
      ('+12:00', '+12:00 Auckland winter'), ('-03:00', '-03:00 Sao Paulo'), ('-04:00', '-04:00 New York summer'), ('-05:00', '-05:00 New York winter'),
      ('-06:00', '-06:00 Chicago winter'), ('-07:00', '-07:00 Los Angeles summer'), ('-08:00', '-08:00 Los Angeles winter'), ('', 'No time zone')]
CUR = ['INR', 'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'AED', 'SGD', 'NZD', 'ZAR', 'JPY']

def OUT(P, tips):
    return f'''<div class="card">
      <h2>Your JSON LD Code</h2>
      <div class="kw-result" id="{P}Check"></div>
      <pre class="code-out" id="{P}Code" style="display:block;margin-top:0;max-height:620px;overflow:auto;word-break:normal;overflow-wrap:anywhere"></pre>
      <label class="check" style="margin-top:12px"><input id="{P}Wrap" type="checkbox" checked> Wrap in a <code>&lt;script&gt;</code> tag</label>
      <div class="actions">
        <button class="btn dark" id="{P}Copy">Copy Code</button>
        <a class="btn" style="text-decoration:none" href="https://search.google.com/test/rich-results" target="_blank" rel="noopener">Open Rich Results Test</a>
        <span class="toast" id="toast">Copied!</span>
      </div>
      <div class="tips"><strong>Before you publish</strong><ul>{tips}</ul></div>
    </div>'''

SJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function lines(id){ return v(id).split(/\n/).map(function(s){ return s.trim(); }).filter(Boolean); }
  function isUrl(s){ return /^https?:\/\/[^\s\/.]+\.[^\s]+$/i.test(s); }
  function clean(o){
    if (Array.isArray(o)){ var a = o.map(clean).filter(function(x){ return x !== undefined; }); return a.length ? a : undefined; }
    if (o && typeof o === 'object'){
      var r = {}, n = 0;
      for (var k in o){ var c = clean(o[k]); if (c !== undefined){ r[k] = c; if (k !== '@type') n++; } }
      return n ? r : undefined;
    }
    if (o === '' || o === null || o === undefined || (typeof o === 'number' && isNaN(o))) return undefined;
    return o;
  }
  function num(s){ s = String(s).replace(/,/g,'').trim(); if (!/^\d+(\.\d+)?$/.test(s)) return undefined; return parseFloat(s); }
  function dt(d, t, z){ d = v(d); if (!d) return ''; t = v(t); return t ? d + 'T' + (t.length === 5 ? t + ':00' : t) + v(z) : d; }
  function pairs(id){ return lines(id).map(function(l){ var p = l.split('|'); return { name: p[0].trim(), url: (p[1] || '').trim() }; }); }
  function addr(P){ return { '@type':'PostalAddress', streetAddress: v(P+'Street'), addressLocality: v(P+'City'), addressRegion: v(P+'Region'), postalCode: v(P+'Zip'), addressCountry: v(P+'Country').toUpperCase() }; }
  function phoneCheck(p, label, issues){ if (p && !/^\+\d/.test(p)) issues.push(['warn', label + ' should start with + and the country code, for example +91 or +1.']); }
  function urlCheck(u, label, issues, lvl){ if (u && !isUrl(u)) issues.push([lvl || 'bad', label + ' must be a full URL starting with https://']); }
  function render(P, obj, issues){
    var data = clean(obj) || {};
    var json = JSON.stringify(data, null, 2).replace(/<\//g, '<\\/');
    var code = $(P+'Wrap').checked ? '<script type="application/ld+json">\n' + json + '\n<\/script>' : json;
    $(P+'Code').textContent = code;
    var bad = issues.filter(function(i){ return i[0] === 'bad'; }), warn = issues.filter(function(i){ return i[0] === 'warn'; });
    var box = $(P+'Check'), li = function(a){ return '<ul style="margin:6px 0 0 18px">' + a.map(function(i){ return '<li>' + esc(i[1]) + '</li>'; }).join('') + '</ul>'; };
    if (bad.length){ box.className = 'kw-result bad'; box.innerHTML = '<strong>Fix ' + bad.length + ' issue' + (bad.length > 1 ? 's' : '') + ' before publishing.</strong>' + li(bad.concat(warn)); }
    else if (warn.length){ box.className = 'kw-result warn'; box.innerHTML = '<strong>Required properties are in place.</strong> Suggestions:' + li(warn); }
    else { box.className = 'kw-result ok'; box.innerHTML = '<strong>Looks good.</strong> All required and recommended properties are filled in.'; }
  }
  function wire(P, run){
    $(P+'Form').addEventListener('input', run); $(P+'Form').addEventListener('change', run);
    $(P+'Copy').onclick = function(){ copyText($(P+'Code').textContent, 'toast'); };
    run();
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. LOCAL BUSINESS SCHEMA GENERATOR ----------
    lb_types = ['LocalBusiness', 'Restaurant', 'CafeOrCoffeeShop', 'Bakery', 'BarOrPub', 'Store', 'ClothingStore', 'ElectronicsStore',
                'GroceryStore', 'FurnitureStore', 'Dentist', 'MedicalClinic', 'Physician', 'Pharmacy', 'Optician', 'LegalService', 'Attorney',
                'AccountingService', 'FinancialService', 'InsuranceAgency', 'RealEstateAgent', 'HairSalon', 'BeautySalon', 'DaySpa',
                'HealthClub', 'AutoRepair', 'AutoDealer', 'Plumber', 'Electrician', 'HVACBusiness', 'RoofingContractor', 'Locksmith',
                'MovingCompany', 'Hotel', 'TravelAgency', 'ChildCare', 'ProfessionalService']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hrs = ''
    for i, d in enumerate(days):
        o, c, s = ('08:00', '22:00', 'open') if i < 5 else (('09:00', '23:00', 'open') if i == 5 else ('', '', 'closed'))
        hrs += (f'<tr><td>{d}</td><td><input id="lbO{i}" type="time" value="{o}" aria-label="{d} opens" style="width:100%;min-width:92px;padding:6px"></td>'
                f'<td><input id="lbC{i}" type="time" value="{c}" aria-label="{d} closes" style="width:100%;min-width:92px;padding:6px"></td>'
                f'<td><select id="lbS{i}" aria-label="{d} status" style="padding:6px;border:1px solid #cfcfcf;border-radius:6px">'
                + ''.join(f'<option value="{k}"' + (' selected' if k == s else '') + f'>{t}</option>' for k, t in (('open', 'Open'), ('24', '24 hours'), ('closed', 'Closed')))
                + '</select></td></tr>')
    TOOLS.append(dict(
        slug='local-business-schema-generator', short='LB', name='Local Business Schema Generator',
        card='Create LocalBusiness JSON LD with address, map coordinates, phone, price range and opening hours.',
        title='Local Business Schema Generator: Free JSON LD Tool',
        desc='Free local business schema generator. Create LocalBusiness JSON LD with address, geo coordinates, opening hours and phone, checked against Google rules.',
        h1='Local Business Schema Generator',
        lead='Fill in your business details and get valid LocalBusiness JSON LD with opening hours, map coordinates and contact details, checked against Google\'s rules as you type.',
        tool='''<section class="tool" aria-label="Local business schema generator" id="lbForm">
    <div class="card">
      <h2>Business Details</h2>
      ''' + F('lbType', 'Business Type', 'CafeOrCoffeeShop', tag='select', opts=lb_types, em='pick the most specific') + '''
      ''' + F('lbName', 'Business Name', 'Green Leaf Cafe') + '''
      ''' + F('lbDesc', 'Short Description', 'Neighbourhood cafe serving filter coffee, fresh bakes and all day breakfast in Koregaon Park.', tag='textarea', em='optional') + '''
      ''' + R2(F('lbUrl', 'Page URL for This Location', 'https://www.example.com/pune/'), F('lbPhone', 'Phone', '+91 20 2550 1234', em='with country code')) + '''
      ''' + R2(F('lbImg', 'Photo URL', 'https://www.example.com/images/green-leaf-cafe.jpg'), F('lbPrice', 'Price Range', '₹₹', em='e.g. $$ or ₹200 to ₹600')) + '''
      ''' + F('lbStreet', 'Street Address', 'Lane 6, North Main Road, Koregaon Park') + '''
      ''' + R2(F('lbCity', 'City', 'Pune'), F('lbRegion', 'State or Region', 'Maharashtra')) + '''
      ''' + R2(F('lbZip', 'Postal Code', '411001'), F('lbCountry', 'Country Code', 'IN', em='2 letters')) + '''
      ''' + R2(F('lbLat', 'Latitude', '18.53621', em='5+ decimals'), F('lbLng', 'Longitude', '73.89412', em='5+ decimals')) + '''
      <div class="field"><label>Opening Hours <em>24 hour clock</em></label>
        <div style="overflow-x:auto"><table class="rtable"><thead><tr><th>Day</th><th>Opens</th><th>Closes</th><th>Status</th></tr></thead><tbody>''' + hrs + '''</tbody></table></div>
      </div>
      ''' + R2(F('lbMenu', 'Menu URL', 'https://www.example.com/pune/menu/', em='food places'), F('lbCuisine', 'Cuisine', 'Cafe, Indian', em='comma separated')) + '''
      ''' + F('lbSame', 'Profile Links', 'https://www.instagram.com/example\nhttps://www.facebook.com/example', tag='textarea', em='one URL per line') + '''
    </div>
    ''' + OUT('lb', '<li>Paste the code into the page for this location only</li><li>Make sure the name, address and phone match your Google Business Profile</li><li>Run the Rich Results Test and fix any errors</li>') + '''
  </section>''',
        js=SJS + r'''
  var DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
  function dec(s){ var m = String(s).split('.')[1]; return m ? m.length : 0; }
  function run(){
    var I = [], P = 'lb';
    var groups = [], key = {};
    DAYS.forEach(function(d, i){
      var st = v('lbS'+i), o = v('lbO'+i), c = v('lbC'+i);
      $('lbO'+i).disabled = $('lbC'+i).disabled = (st !== 'open');
      if (st === '24'){ o = '00:00'; c = '23:59'; }
      else if (st === 'closed'){ o = '00:00'; c = '00:00'; }
      else if (!o || !c){ I.push(['warn', d + ' is marked open but is missing an opening or closing time.']); return; }
      var k = o + '|' + c;
      if (!(k in key)){ key[k] = groups.length; groups.push({ '@type':'OpeningHoursSpecification', dayOfWeek: [], opens: o, closes: c }); }
      groups[key[k]].dayOfWeek.push(d);
    });
    var lat = v('lbLat'), lng = v('lbLng'), geo;
    if (lat || lng){
      if (isNaN(+lat) || isNaN(+lng) || Math.abs(+lat) > 90 || Math.abs(+lng) > 180) I.push(['bad', 'Latitude must be between 90 and minus 90, longitude between 180 and minus 180.']);
      else { geo = { '@type':'GeoCoordinates', latitude: +lat, longitude: +lng }; if (dec(lat) < 5 || dec(lng) < 5) I.push(['warn', 'Google asks for at least 5 decimal places in latitude and longitude.']); }
    } else I.push(['warn', 'Add latitude and longitude so Google can place you exactly on the map.']);
    var url = v('lbUrl'), phone = v('lbPhone'), pr = v('lbPrice');
    if (!v('lbName')) I.push(['bad', 'Business name is required.']);
    if (!v('lbStreet') && !v('lbCity')) I.push(['bad', 'Address is required. Add at least the street and city.']);
    else if (!v('lbStreet')) I.push(['warn', 'Add the street address. Google asks for as many address fields as possible.']);
    if (!v('lbCountry')) I.push(['warn', 'Add the 2 letter country code, for example IN, US or GB.']);
    else if (!/^[A-Za-z]{2}$/.test(v('lbCountry'))) I.push(['warn', 'Use a 2 letter ISO country code such as IN, US or GB.']);
    urlCheck(url, 'Page URL', I); if (!url) I.push(['warn', 'Add the URL of the page for this location.']);
    if (!phone) I.push(['warn', 'Add a phone number with the country code.']); phoneCheck(phone, 'Phone', I);
    if (pr.length >= 100) I.push(['bad', 'Price range must be under 100 characters or Google will not show it.']);
    urlCheck(v('lbImg'), 'Photo URL', I); urlCheck(v('lbMenu'), 'Menu URL', I);
    var same = lines('lbSame'); same.forEach(function(s){ urlCheck(s, 'Profile link "' + s + '"', I); });
    var cuisine = v('lbCuisine').split(',').map(function(s){ return s.trim(); }).filter(Boolean);
    var o = { '@context':'https://schema.org', '@type': v('lbType'), name: v('lbName'), description: v('lbDesc'), image: v('lbImg'),
      '@id': url ? url.replace(/#.*$/,'') + '#business' : '', url: url, telephone: phone, priceRange: pr, address: addr(P), geo: geo,
      openingHoursSpecification: groups, menu: v('lbMenu'), servesCuisine: cuisine, sameAs: same };
    render(P, o, I);
  }
  wire('lb', run);
''',
        content=r'''
    <h2>What Is Local Business Schema?</h2>
    <p>Local business schema is structured data that tells Google the facts about a physical business: its name, address, phone number, opening hours and exact location on the map.</p>
    <p>It uses the <code>LocalBusiness</code> type from schema.org, or a more specific subtype such as <code>Restaurant</code>, <code>Dentist</code> or <code>Plumber</code>. Google can use it to show your details in the knowledge panel and in local results.</p>

    <h2>How to Use This Generator</h2>
    <ol>
      <li><strong>Pick the most specific business type.</strong> A bakery should use <code>Bakery</code>, not just <code>LocalBusiness</code>.</li>
      <li><strong>Enter your name, address and phone</strong> exactly as they appear on your Google Business Profile.</li>
      <li><strong>Add coordinates.</strong> In Google Maps, right click your pin and copy the numbers shown.</li>
      <li><strong>Set your opening hours.</strong> Days with the same hours are grouped automatically.</li>
      <li><strong>Copy the code</strong> and paste it into the page for that location, then test it.</li>
    </ol>

    <h2>Properties Google Uses</h2>
    <table class="lim">
      ''' + th('Property', 'Status', 'What to enter') + '''
      <tbody>
        <tr><td><code>name</code></td><td>Required</td><td>Your business name, as customers know it</td></tr>
        <tr><td><code>address</code></td><td>Required</td><td>As many address fields as you can fill</td></tr>
        <tr><td><code>geo</code></td><td>Recommended</td><td>Latitude and longitude with at least 5 decimal places</td></tr>
        <tr><td><code>openingHoursSpecification</code></td><td>Recommended</td><td>Days with opening and closing times in 24 hour format</td></tr>
        <tr><td><code>telephone</code></td><td>Recommended</td><td>Main number with country and area code</td></tr>
        <tr><td><code>priceRange</code></td><td>Recommended</td><td>Symbols like $$ or a range, under 100 characters</td></tr>
        <tr><td><code>url</code></td><td>Recommended</td><td>The page for this exact location</td></tr>
        <tr><td><code>menu</code>, <code>servesCuisine</code></td><td>Recommended</td><td>For restaurants and cafes</td></tr>
      </tbody>
    </table>
    <p>The full list is in <a href="''' + G + '''local-business" target="_blank" rel="noopener">Google's local business documentation</a>.</p>

    <h2>Opening Hours Rules</h2>
    <ul>
      <li><strong>Open 24 hours:</strong> the tool writes opens <code>00:00</code> and closes <code>23:59</code>.</li>
      <li><strong>Closed all day:</strong> the tool writes <code>00:00</code> for both, which is how Google asks for it.</li>
      <li><strong>Open past midnight:</strong> just enter a closing time like 02:00. That is allowed.</li>
    </ul>

    <h2>Tips for Better Local Results</h2>
    <ul>
      <li>Have several branches? Give each one its own page and its own schema block.</li>
      <li>Do not add star ratings for your own business. Google treats reviews a business controls about itself as self serving and will not show stars for them.</li>
      <li>Keep your name, address and phone identical everywhere online.</li>
    </ul>
    <p>Learn more in our guides to <a href="https://brandella.in/localbusiness-schema-markup/">LocalBusiness schema markup</a>, <a href="https://brandella.in/nap-consistency-hidden-local-seo-ranking-factor/">NAP consistency</a> and <a href="https://brandella.in/how-to-rank-higher-on-google-maps-2026/">ranking higher on Google Maps</a>. For your head office or brand, use the <a href="https://brandella.in/tools/schema-generators/organization-schema-generator/">Organization schema generator</a>.</p>
''',
        faqs=[
            ("Where should I put local business schema?", "Put it on the page that describes that location, usually your home page for a single shop or a dedicated location page for each branch. It can go in the head or the body of the page."),
            ("Does local business schema help my Google Maps ranking?", "It does not directly boost Maps rankings. It helps Google understand and confirm your business details. Your Google Business Profile, reviews and proximity matter far more for Maps."),
            ("Can I add review stars to my local business schema?", "Not for reviews about your own business. Google says pages using LocalBusiness or Organization markup are not eligible for review stars when the business controls those reviews, even through a widget."),
            ("Is my business information sent anywhere?", "No. This local business schema generator runs entirely in your browser. Nothing you type is uploaded or stored."),
        ],
        related=[("LocalBusiness Schema Markup", "localbusiness-schema-markup"), ("Google Business Profile Guide", "google-my-business-profile-complete-guide-beginners"),
                 ("Local Citations Explained", "local-citations-explained-seo"), ("How to Get More Google Reviews", "how-to-get-more-google-reviews")],
    ))

    # ---------- 2. PRODUCT SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='product-schema-generator', short='PS', name='Product Schema Generator',
        card='Build Product JSON LD with price, availability, brand, GTIN, ratings and a review.',
        title='Product Schema Generator: Free Product JSON LD',
        desc='Free product schema generator. Create Product JSON LD with price, currency, availability, brand, GTIN, ratings and reviews for Google product snippets.',
        h1='Product Schema Generator',
        lead='Create Product JSON LD with price, stock status, brand and ratings, so Google can show your price and stars right in the search results.',
        tool='''<section class="tool" aria-label="Product schema generator" id="prForm">
    <div class="card">
      <h2>Product Details</h2>
      ''' + F('prName', 'Product Name', 'Leafline Organic Cotton Tote Bag') + '''
      ''' + F('prDesc', 'Description', 'Reusable tote bag made from 100% organic cotton with reinforced handles. Holds up to 15 kg.', tag='textarea') + '''
      ''' + F('prImg', 'Image URLs', 'https://www.example.com/images/tote-front.jpg\nhttps://www.example.com/images/tote-side.jpg', tag='textarea', em='one per line') + '''
      ''' + R2(F('prBrand', 'Brand', 'Leafline'), F('prSku', 'SKU', 'LL-TOTE-01', em='optional')) + '''
      ''' + R2(F('prGtin', 'GTIN or Barcode', '8901234567893', em='8, 12, 13 or 14 digits'), F('prUrl', 'Product Page URL', 'https://www.example.com/tote-bag/')) + '''
      <h2 style="margin-top:8px">Price and Stock</h2>
      ''' + R2(F('prPrice', 'Price', '499', em='numbers only'), F('prCur', 'Currency', 'INR', tag='select', opts=CUR)) + '''
      ''' + R2(F('prAvail', 'Availability', 'InStock', tag='select', opts=[('InStock', 'In stock'), ('OutOfStock', 'Out of stock'), ('PreOrder', 'Pre order'), ('BackOrder', 'Back order'), ('LimitedAvailability', 'Limited availability'), ('OnlineOnly', 'Online only'), ('InStoreOnly', 'In store only'), ('SoldOut', 'Sold out'), ('Discontinued', 'Discontinued')]),
                 F('prCond', 'Condition', 'NewCondition', tag='select', opts=[('NewCondition', 'New'), ('RefurbishedCondition', 'Refurbished'), ('UsedCondition', 'Used'), ('DamagedCondition', 'Damaged'), ('', 'Not set')])) + '''
      ''' + F('prValid', 'Price Valid Until', '2027-03-31', typ='date', em='optional') + '''
      <h2 style="margin-top:8px">Ratings <em style="font-size:13px;font-weight:600;color:#777">optional</em></h2>
      ''' + R2(F('prRating', 'Average Rating', '4.6'), F('prCount', 'Number of Ratings', '128')) + '''
      ''' + R2(F('prAuthor', 'Review Author', 'Priya Sharma'), F('prRev', 'Review Rating', '5', em='out of 5')) + '''
      ''' + F('prBody', 'Review Text', 'Strong, roomy and still looks new after six months of grocery runs.', tag='textarea') + '''
    </div>
    ''' + OUT('pr', '<li>Only mark up ratings and reviews that are visible on the page</li><li>Keep the price in the code the same as the price shown to shoppers</li><li>Update availability when stock changes</li>') + '''
  </section>''',
        js=SJS + r'''
  function run(){
    var I = [], P = 'pr';
    var price = v('prPrice'), pn = num(price), rv = v('prRating'), rc = v('prCount'), ra = v('prAuthor'), rr = v('prRev');
    if (!v('prName')) I.push(['bad', 'Product name is required.']);
    if (price && pn === undefined) I.push(['bad', 'Price must be a plain number like 499 or 19.99, with no currency symbol.']);
    var offers;
    if (price && pn !== undefined){
      offers = { '@type':'Offer', url: v('prUrl'), priceCurrency: v('prCur'), price: pn, availability: 'https://schema.org/' + v('prAvail'),
        itemCondition: v('prCond') ? 'https://schema.org/' + v('prCond') : '', priceValidUntil: v('prValid') };
      if (v('prValid') && v('prValid') < new Date().toISOString().slice(0,10)) I.push(['warn', 'Price valid until is in the past. Google may not show the snippet.']);
    }
    var agg;
    if (rv || rc){
      var rvn = num(rv), rcn = num(rc);
      if (rvn === undefined || rvn < 1 || rvn > 5) I.push(['bad', 'Average rating must be a number from 1 to 5.']);
      else if (!rcn || rcn < 1) I.push(['bad', 'Add the number of ratings. Google requires a rating count or review count.']);
      else agg = { '@type':'AggregateRating', ratingValue: rvn, bestRating: 5, ratingCount: Math.round(rcn) };
    }
    var rev;
    if (ra || rr || v('prBody')){
      var rrn = num(rr);
      if (!ra) I.push(['bad', 'A review needs the name of a real person or organization as the author.']);
      else if (ra.length >= 100) I.push(['bad', 'Review author name must be under 100 characters.']);
      else if (rrn === undefined || rrn < 1 || rrn > 5) I.push(['bad', 'Review rating must be a number from 1 to 5.']);
      else rev = { '@type':'Review', author: { '@type':'Person', name: ra }, reviewRating: { '@type':'Rating', ratingValue: rrn, bestRating: 5 }, reviewBody: v('prBody') };
    }
    if (!offers && !agg && !rev) I.push(['bad', 'Google needs at least one of: a price, a rating, or a review.']);
    else if (!agg && !rev) I.push(['warn', 'The Rich Results Test may warn when there is a price but no rating or review. That is fine if you have none.']);
    var imgs = lines('prImg'); if (!imgs.length) I.push(['warn', 'Add at least one product image URL.']);
    imgs.forEach(function(u){ urlCheck(u, 'Image "' + u + '"', I); });
    urlCheck(v('prUrl'), 'Product page URL', I);
    var g = v('prGtin').replace(/\s/g,''); if (g && !/^(\d{8}|\d{12,14})$/.test(g)) I.push(['warn', 'A GTIN is usually 8, 12, 13 or 14 digits.']);
    if (!v('prBrand')) I.push(['warn', 'Add the brand name.']);
    var o = { '@context':'https://schema.org', '@type':'Product', name: v('prName'), description: v('prDesc'), image: imgs, sku: v('prSku'), gtin: g,
      brand: { '@type':'Brand', name: v('prBrand') }, offers: offers, aggregateRating: agg, review: rev };
    render(P, o, I);
  }
  wire('pr', run);
''',
        content=r'''
    <h2>What Is Product Schema?</h2>
    <p>Product schema is structured data that describes an item you sell: its name, price, currency, stock status and reviews. Google can use it to show a product snippet with the price, availability and star rating under your result.</p>
    <p>This product schema generator writes the <code>Product</code> type with a nested <code>Offer</code>, <code>AggregateRating</code> and <code>Review</code>, following the <a href="''' + G + '''product-snippet" target="_blank" rel="noopener">Google product snippet guidelines</a>.</p>

    <h2>How to Use the Product Schema Generator</h2>
    <ol>
      <li><strong>Enter the product name, description and images.</strong> Use the same text shoppers see on the page.</li>
      <li><strong>Add brand, SKU and GTIN</strong> if you have them. A GTIN is the number under the barcode.</li>
      <li><strong>Set the price and currency.</strong> Type numbers only, such as 499 or 19.99.</li>
      <li><strong>Add ratings and a review</strong> only if they are real and shown on the page.</li>
      <li><strong>Copy the code</strong>, paste it into the product page and run the Rich Results Test.</li>
    </ol>

    <h2>What Google Requires</h2>
    <table class="lim">
      ''' + th('Property', 'Rule') + '''
      <tbody>
        <tr><td><code>name</code></td><td>Required</td></tr>
        <tr><td><code>offers</code>, <code>aggregateRating</code> or <code>review</code></td><td>At least one is required</td></tr>
        <tr><td><code>offers.price</code></td><td>Required inside an offer. Use 0 for free items</td></tr>
        <tr><td><code>offers.priceCurrency</code></td><td>Recommended, a 3 letter code such as INR or USD</td></tr>
        <tr><td><code>offers.availability</code></td><td>Recommended, for example InStock or OutOfStock</td></tr>
        <tr><td><code>aggregateRating</code></td><td>Needs a rating value plus a rating count or review count</td></tr>
        <tr><td><code>review.author</code></td><td>A real person or organization name, under 100 characters</td></tr>
      </tbody>
    </table>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Match the page.</strong> If the code says 499 but the page says 549, Google may ignore your markup.</li>
      <li><strong>Avoid a past price valid until date.</strong> Google notes the snippet may not show if that date has passed.</li>
      <li><strong>Selling in a store?</strong> Online shops that want free Shopping listings should also look at Google's merchant listing markup, which asks for shipping and return details.</li>
      <li><strong>Reviewer names must be real.</strong> A promo line like "50% off today" is not a valid author.</li>
    </ul>
    <p>To track sales from these pages, read our guide to <a href="https://brandella.in/ga4-ecommerce-events-examples/">GA4 ecommerce events</a>, and learn the basics in <a href="https://brandella.in/what-is-schema-markup/">what is schema markup</a>. Want your result to look sharp too? Check it in the <a href="https://brandella.in/tools/seo-tools/serp-snippet-preview/">SERP snippet preview</a>.</p>
''',
        faqs=[
            ("Why are my product stars not showing in Google?", "Valid markup makes a page eligible, but Google decides whether to show stars. Make sure the ratings are real, visible on the page, and that your code passes the Rich Results Test."),
            ("Do I need ratings for product schema to work?", "No. Google needs at least one of a price, a rating or a review. A product with only a price and stock status is valid, though the test tool may suggest adding a rating."),
            ("Should I include the currency symbol in the price?", "No. Put only the number in the price field and the 3 letter currency code, such as INR or USD, in its own field. The generator does this for you."),
            ("Is my product data stored?", "No. The product schema generator runs only in your browser, so nothing you enter is uploaded or saved."),
        ],
        related=[("What Is Schema Markup", "what-is-schema-markup"), ("How to Add Schema Markup With JSON LD", "how-to-add-schema-markup-json-ld"),
                 ("GA4 Ecommerce Events Examples", "ga4-ecommerce-events-examples"), ("Conversion Rate Optimization", "conversion-rate-optimization")],
    ))

    # ---------- 3. ARTICLE SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='article-schema-generator', short='AS', name='Article Schema Generator',
        card='Generate Article, BlogPosting or NewsArticle JSON LD with authors, dates, images and publisher.',
        title='Article Schema Generator: BlogPosting and NewsArticle',
        desc='Free article schema generator. Create Article, BlogPosting or NewsArticle JSON LD with headline, images, authors, publish dates and publisher logo.',
        h1='Article Schema Generator',
        lead='Create Article, BlogPosting or NewsArticle JSON LD with the right authors, dates and images, so Google picks the correct headline, byline and date for your post.',
        tool='''<section class="tool" aria-label="Article schema generator" id="arForm">
    <div class="card">
      <h2>Article Details</h2>
      ''' + F('arType', 'Article Type', 'BlogPosting', tag='select', opts=[('BlogPosting', 'BlogPosting (blog post)'), ('Article', 'Article (general)'), ('NewsArticle', 'NewsArticle (news)')]) + '''
      ''' + F('arHead', 'Headline', 'How to Plan a Content Calendar That Your Team Will Actually Use', em='0 chars') + '''
      ''' + F('arUrl', 'Article URL', 'https://www.example.com/blog/content-calendar/') + '''
      ''' + F('arDesc', 'Description', 'A simple, repeatable way to plan a month of content in one afternoon, with a free template.', tag='textarea', em='optional') + '''
      ''' + F('arImg', 'Image URLs', 'https://www.example.com/images/calendar-16x9.jpg\nhttps://www.example.com/images/calendar-4x3.jpg\nhttps://www.example.com/images/calendar-1x1.jpg', tag='textarea', em='one per line') + '''
      ''' + R2(F('arPubD', 'Date Published', '2026-10-20', typ='date'), F('arPubT', 'Time Published', '09:00', typ='time')) + '''
      ''' + R2(F('arModD', 'Date Modified', '2026-10-27', typ='date'), F('arModT', 'Time Modified', '14:30', typ='time')) + '''
      ''' + F('arTz', 'Time Zone', '+05:30', tag='select', opts=TZ) + '''
      ''' + F('arAuth', 'Authors', 'Santaji Gade | https://www.example.com/author/santaji/', tag='textarea', em='Name | profile URL, one per line') + '''
      ''' + F('arAType', 'Author Type', 'Person', tag='select', opts=[('Person', 'Person'), ('Organization', 'Organization')]) + '''
      ''' + R2(F('arPub', 'Publisher Name', 'Example Media'), F('arLogo', 'Publisher Logo URL', 'https://www.example.com/logo.png')) + '''
    </div>
    ''' + OUT('ar', '<li>Use dates that match the dates shown on the page</li><li>List every author in their own line</li><li>Use large images in 16x9, 4x3 and 1x1 shapes</li>') + '''
  </section>''',
        js=SJS + r'''
  function run(){
    var I = [], P = 'ar', h = v('arHead');
    $('arForm').querySelector('label[for=arHead] em').textContent = h.length + ' chars';
    if (!h) I.push(['warn', 'Add a headline. It should match the title of the article.']);
    else if (h.length > 110) I.push(['warn', 'Long headlines may be cut off on some devices. Keep it concise.']);
    var pub = dt('arPubD','arPubT','arTz'), mod = dt('arModD','arModT','arTz');
    if (!pub) I.push(['warn', 'Add the date published.']);
    if (pub && mod && v('arModD') + v('arModT') < v('arPubD') + v('arPubT')) I.push(['bad', 'Date modified cannot be before date published.']);
    if (pub && v('arPubT') && !v('arTz')) I.push(['warn', 'Pick a time zone. Without one Google assumes the time zone of Googlebot.']);
    var at = v('arAType'), authors = pairs('arAuth').map(function(a){
      if (/^by\s/i.test(a.name)) I.push(['warn', 'Put only the name in the author field, without "By".']);
      if (/,|\band\b|&/.test(a.name) && at === 'Person') I.push(['warn', '"' + a.name + '" looks like several people. Put each author on their own line.']);
      if (!a.url) I.push(['warn', 'Add a profile URL for ' + a.name + '.']); else urlCheck(a.url, 'Author URL for ' + a.name, I);
      return { '@type': at, name: a.name, url: a.url };
    });
    if (!authors.length) I.push(['warn', 'Add at least one author.']);
    var imgs = lines('arImg'); if (!imgs.length) I.push(['warn', 'Add at least one image. Google recommends 16x9, 4x3 and 1x1 versions.']);
    imgs.forEach(function(u){ urlCheck(u, 'Image "' + u + '"', I); });
    urlCheck(v('arUrl'), 'Article URL', I); urlCheck(v('arLogo'), 'Publisher logo URL', I);
    var o = { '@context':'https://schema.org', '@type': v('arType'), headline: h, description: v('arDesc'), image: imgs,
      datePublished: pub, dateModified: mod, author: authors.length === 1 ? authors[0] : authors,
      publisher: { '@type':'Organization', name: v('arPub'), logo: { '@type':'ImageObject', url: v('arLogo') } },
      mainEntityOfPage: v('arUrl') ? { '@type':'WebPage', '@id': v('arUrl') } : '' };
    render(P, o, I);
  }
  wire('ar', run);
''',
        content=r'''
    <h2>What Is Article Schema?</h2>
    <p>Article schema is structured data for news stories, blog posts and other written content. It tells Google the headline, the authors, when the piece was published and updated, and which images represent it.</p>
    <p>Google supports three types: <code>Article</code>, <code>BlogPosting</code> and <code>NewsArticle</code>. There are no required properties, but every recommended one you add helps Google show the right title, date and byline.</p>

    <h2>How to Use the Article Schema Generator</h2>
    <ol>
      <li><strong>Choose the type.</strong> BlogPosting for blog posts, NewsArticle for news, Article for anything else.</li>
      <li><strong>Enter the headline and URL</strong> exactly as they appear on the page.</li>
      <li><strong>Add images.</strong> Paste one URL per line, ideally in wide, standard and square shapes.</li>
      <li><strong>Set dates, times and your time zone.</strong> The tool builds ISO 8601 dates such as <code>2026-10-20T09:00:00+05:30</code>.</li>
      <li><strong>List authors</strong> as <code>Name | profile URL</code>, one per line, then copy the code.</li>
    </ol>

    <h2>Recommended Properties</h2>
    <table class="lim">
      ''' + th('Property', 'Google guidance') + '''
      <tbody>
        <tr><td><code>headline</code></td><td>The article title. Keep it concise</td></tr>
        <tr><td><code>image</code></td><td>At least 50,000 pixels (width times height), in 16x9, 4x3 and 1x1 ratios</td></tr>
        <tr><td><code>datePublished</code></td><td>ISO 8601 with time zone</td></tr>
        <tr><td><code>dateModified</code></td><td>The last time the content changed</td></tr>
        <tr><td><code>author</code></td><td>Person or Organization, with name and url</td></tr>
      </tbody>
    </table>
    <p>See <a href="''' + G + '''article" target="_blank" rel="noopener">Google's article structured data guide</a> for the full details.</p>

    <h2>Author Best Practices</h2>
    <ul>
      <li>Give each author their own entry. Do not join two names in one field.</li>
      <li>Put only the name in the name field. No "By", job titles or the site name.</li>
      <li>Link each author to a real profile page or social profile.</li>
      <li>Only change <code>dateModified</code> when you make a real update, not a typo fix.</li>
    </ul>
    <p>Strong author signals support trust, which we cover in <a href="https://brandella.in/eeat-experience-expertise-authority-trust/">E E A T explained</a> and <a href="https://brandella.in/how-to-refresh-old-content-without-losing-rankings/">refreshing old content</a>. Pair this with the <a href="https://brandella.in/tools/schema-generators/breadcrumb-schema-generator/">breadcrumb schema generator</a> for complete blog markup.</p>
''',
        faqs=[
            ("Should I use Article or BlogPosting schema?", "Use BlogPosting for blog posts, NewsArticle for news reporting, and Article for other written content. Google supports all three the same way, so pick the one that describes your page best."),
            ("Do I need article schema if I use Yoast or Rank Math?", "Usually not. Those plugins already output article schema. Use this generator for sites without a plugin, custom pages, or to check what good markup looks like."),
            ("Why should I include a time zone in dates?", "Without a time zone, Google assumes the time zone of Googlebot, which can make your date look a day off. Adding the offset, such as +05:30 for India, avoids that."),
            ("Does this article schema generator save my content?", "No. Everything runs in your browser and nothing is uploaded."),
        ],
        related=[("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("E E A T Explained", "eeat-experience-expertise-authority-trust"),
                 ("What Is Entity SEO", "what-is-entity-seo-who-vs-what-2026"), ("How to Add Schema Markup With JSON LD", "how-to-add-schema-markup-json-ld")],
    ))

    # ---------- 4. ORGANIZATION SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='organization-schema-generator', short='OS', name='Organization Schema Generator',
        card='Create Organization JSON LD with logo, social profiles, contact point, address and business IDs.',
        title='Organization Schema Generator: Logo and sameAs JSON LD',
        desc='Free organization schema generator. Create Organization JSON LD with logo, sameAs social profiles, contact details, address, founding date and IDs.',
        h1='Organization Schema Generator',
        lead='Tell Google who you are. Create Organization JSON LD with your logo, social profiles, contact details and business identifiers for your home page or About page.',
        tool='''<section class="tool" aria-label="Organization schema generator" id="orForm">
    <div class="card">
      <h2>Organization Details</h2>
      ''' + F('orType', 'Organization Type', 'Organization', tag='select', opts=['Organization', 'Corporation', 'OnlineStore', 'NewsMediaOrganization', 'EducationalOrganization', 'NGO', 'MedicalOrganization', 'SportsOrganization']) + '''
      ''' + R2(F('orName', 'Name', 'Brightpath Digital'), F('orAlt', 'Other Name', 'Brightpath', em='optional')) + '''
      ''' + R2(F('orLegal', 'Legal Name', 'Brightpath Digital Private Limited', em='if different'), F('orUrl', 'Website URL', 'https://www.example.com/')) + '''
      ''' + F('orLogo', 'Logo URL', 'https://www.example.com/images/logo-512.png', em='112 x 112 px or larger') + '''
      ''' + F('orDesc', 'Description', 'Brightpath Digital is a performance marketing agency helping D2C brands grow through search and social.', tag='textarea', em='optional') + '''
      ''' + R2(F('orEmail', 'Email', 'hello@example.com'), F('orPhone', 'Phone', '+91 22 4000 1234')) + '''
      ''' + F('orStreet', 'Street Address', '4th Floor, Sunrise Towers, Andheri East') + '''
      ''' + R2(F('orCity', 'City', 'Mumbai'), F('orRegion', 'State or Region', 'Maharashtra')) + '''
      ''' + R2(F('orZip', 'Postal Code', '400069'), F('orCountry', 'Country Code', 'IN', em='2 letters')) + '''
      ''' + R2(F('orFound', 'Founding Date', '2018-04-01', typ='date'), F('orStaff', 'Number of Employees', '45', em='optional')) + '''
      ''' + F('orSame', 'Social and Profile Links (sameAs)', 'https://www.linkedin.com/company/example\nhttps://www.instagram.com/example\nhttps://www.youtube.com/@example', tag='textarea', em='one URL per line') + '''
      <h2 style="margin-top:8px">Customer Contact <em style="font-size:13px;font-weight:600;color:#777">optional</em></h2>
      ''' + R2(F('orCpType', 'Contact Type', 'customer support', tag='select', opts=['customer support', 'customer service', 'sales', 'technical support', 'billing support']), F('orCpPhone', 'Contact Phone', '+91 22 4000 1200')) + '''
      ''' + R2(F('orCpEmail', 'Contact Email', 'support@example.com'), F('orCpLang', 'Languages', 'English, Hindi', em='comma separated')) + '''
      ''' + R2(F('orVat', 'VAT or GST ID', '', em='optional'), F('orTax', 'Tax ID', '', em='optional')) + '''
    </div>
    ''' + OUT('or', '<li>Add it to your home page or About page only</li><li>Check that your logo looks good on a white background</li><li>Use full profile URLs in sameAs, not handles</li>') + '''
  </section>''',
        js=SJS + r'''
  function run(){
    var I = [], P = 'or', url = v('orUrl');
    if (!v('orName')) I.push(['warn', 'Add your organization name.']);
    if (!url) I.push(['warn', 'Add your website URL.']); urlCheck(url, 'Website URL', I);
    if (!v('orLogo')) I.push(['warn', 'Add a logo URL so Google can show your logo. It must be at least 112 x 112 pixels.']); urlCheck(v('orLogo'), 'Logo URL', I);
    if (/\.svg(\?|$)/i.test(v('orLogo'))) I.push(['warn', 'Use a PNG, JPG or WebP logo. Check that the format is supported by Google Images.']);
    phoneCheck(v('orPhone'), 'Phone', I); phoneCheck(v('orCpPhone'), 'Contact phone', I);
    var em = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (v('orEmail') && !em.test(v('orEmail'))) I.push(['bad', 'Email does not look valid.']);
    if (v('orCpEmail') && !em.test(v('orCpEmail'))) I.push(['bad', 'Contact email does not look valid.']);
    var same = lines('orSame'); same.forEach(function(s){ urlCheck(s, 'Profile link "' + s + '"', I); });
    if (!same.length) I.push(['warn', 'Add links to your social and review profiles in sameAs.']);
    if (v('orLegal') && v('orLegal') === v('orName')) I.push(['warn', 'Legal name is only needed when it differs from the name.']);
    if (v('orCountry') && !/^[A-Za-z]{2}$/.test(v('orCountry'))) I.push(['warn', 'Use a 2 letter ISO country code such as IN, US or GB.']);
    var staff = num(v('orStaff')); if (v('orStaff') && staff === undefined) I.push(['bad', 'Number of employees must be a number.']);
    var cp = (v('orCpPhone') || v('orCpEmail')) ? { '@type':'ContactPoint', contactType: v('orCpType'), telephone: v('orCpPhone'), email: v('orCpEmail'),
      availableLanguage: v('orCpLang').split(',').map(function(s){ return s.trim(); }).filter(Boolean) } : '';
    var o = { '@context':'https://schema.org', '@type': v('orType'), '@id': url ? url.replace(/\/?$/, '/') + '#organization' : '', name: v('orName'),
      alternateName: v('orAlt'), legalName: v('orLegal') !== v('orName') ? v('orLegal') : '', url: url, logo: v('orLogo'), description: v('orDesc'),
      email: v('orEmail'), telephone: v('orPhone'), address: addr(P), foundingDate: v('orFound'),
      numberOfEmployees: staff !== undefined ? { '@type':'QuantitativeValue', value: Math.round(staff) } : '',
      sameAs: same, contactPoint: cp, vatID: v('orVat'), taxID: v('orTax') };
    render(P, o, I);
  }
  wire('or', run);
''',
        content=r'''
    <h2>What Is Organization Schema?</h2>
    <p>Organization schema is structured data that describes your company or brand: its official name, logo, website, contact details and the profiles that belong to it. Google can use it in knowledge panels and to pick the logo shown for your site.</p>
    <p>It also helps search engines and AI assistants connect your brand to your social profiles, which supports entity understanding.</p>

    <h2>How to Use This Tool</h2>
    <ol>
      <li><strong>Choose the most specific type.</strong> An online shop can use <code>OnlineStore</code>. A shop with a physical address should use the <a href="https://brandella.in/tools/schema-generators/local-business-schema-generator/">local business schema generator</a> instead.</li>
      <li><strong>Enter your name, website and logo.</strong> The logo should be square or close to it and at least 112 x 112 pixels.</li>
      <li><strong>Add your social profiles</strong> in sameAs, one full URL per line.</li>
      <li><strong>Add contact details and IDs</strong> if you want, then copy the code into your home page.</li>
    </ol>

    <h2>Useful Organization Properties</h2>
    <table class="lim">
      ''' + th('Property', 'What it does') + '''
      <tbody>
        <tr><td><code>name</code>, <code>alternateName</code></td><td>Your main name and a common short name</td></tr>
        <tr><td><code>legalName</code></td><td>Registered company name, if different</td></tr>
        <tr><td><code>logo</code></td><td>Logo image, at least 112 x 112 px, crawlable</td></tr>
        <tr><td><code>sameAs</code></td><td>Links to your profiles on other sites</td></tr>
        <tr><td><code>contactPoint</code></td><td>Support or sales phone and email</td></tr>
        <tr><td><code>address</code></td><td>Your registered or main office address</td></tr>
        <tr><td><code>vatID</code>, <code>taxID</code></td><td>Business identifiers that match your country</td></tr>
      </tbody>
    </table>
    <p>Google lists every supported field in its <a href="''' + G + '''organization" target="_blank" rel="noopener">organization structured data documentation</a>. None are strictly required, so add what applies.</p>

    <h2>Tips</h2>
    <ul>
      <li>One page is enough. Google says you do not need this markup on every page.</li>
      <li>Use full URLs in sameAs, such as your LinkedIn company page, not just a handle.</li>
      <li>The <code>@id</code> the tool adds lets other schema on your site refer to the same organization.</li>
      <li>Keep details identical to your website footer and profiles.</li>
    </ul>
    <p>Want to go deeper on brand signals? Read <a href="https://brandella.in/what-is-entity-seo-who-vs-what-2026/">what is entity SEO</a> and <a href="https://brandella.in/brand-authority-vs-domain-authority/">brand authority vs domain authority</a>.</p>
''',
        faqs=[
            ("Which page should have organization schema?", "Your home page or a single page about your company, such as the About page. Google says it does not need to be on every page of your site."),
            ("What is sameAs in organization schema?", "sameAs is a list of URLs for your profiles on other websites, such as LinkedIn, Instagram, YouTube or Wikipedia. It helps search engines confirm those profiles belong to you."),
            ("What size should my logo be?", "At least 112 x 112 pixels, in a format Google Images supports such as PNG, JPG or WebP. Check that it still looks good on a plain white background."),
            ("Is my company data sent to a server?", "No. This organization schema generator works fully in your browser. Nothing you type is uploaded."),
        ],
        related=[("What Is Entity SEO", "what-is-entity-seo-who-vs-what-2026"), ("Brand Authority vs Domain Authority", "brand-authority-vs-domain-authority"),
                 ("What Is Schema Markup", "what-is-schema-markup"), ("How Google AI Mode Decides to Cite Websites", "how-google-ai-mode-decides-cite-websites")],
    ))

    # ---------- 5. BREADCRUMB SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='breadcrumb-schema-generator', short='BS', name='Breadcrumb Schema Generator',
        card='Turn a page URL or a list of links into valid BreadcrumbList JSON LD in one click.',
        title='Breadcrumb Schema Generator: BreadcrumbList JSON LD',
        desc='Free breadcrumb schema generator. Build BreadcrumbList JSON LD from a page URL or your own list of names and links, with instant checks for Google.',
        h1='Breadcrumb Schema Generator',
        lead='Paste a page URL to build the trail automatically, or type your own names and links. You get valid BreadcrumbList JSON LD with a live preview of the trail.',
        tool='''<section class="tool" aria-label="Breadcrumb schema generator" id="bcForm">
    <div class="card">
      <h2>Build Your Breadcrumb Trail</h2>
      ''' + F('bcFrom', 'Page URL', 'https://www.example.com/blog/seo/schema-markup-guide/', em='optional shortcut') + '''
      <div class="actions" style="margin:0 0 16px"><button class="btn" id="bcBuild">Build Trail From URL</button></div>
      ''' + F('bcList', 'Breadcrumb Items', 'Home | https://www.example.com/\nBlog | https://www.example.com/blog/\nSEO | https://www.example.com/blog/seo/\nSchema Markup Guide | https://www.example.com/blog/seo/schema-markup-guide/', tag='textarea', em='Name | URL, one per line, in order', extra=' class="mono" style="min-height:150px"') + '''
      <label class="check"><input id="bcLast" type="checkbox"> Leave out the URL of the last item (the current page)</label>
      <div class="field" style="margin-top:14px"><label>Trail Preview</label><div class="chips" id="bcPrev" style="align-items:center"></div></div>
    </div>
    ''' + OUT('bc', '<li>The trail should match the breadcrumb people see on the page</li><li>Use full URLs, not paths like /blog/</li><li>You need at least two items</li>') + '''
  </section>''',
        js=SJS + r'''
  function nice(s){ s = decodeURIComponent(s).replace(/\.(html?|php|aspx?)$/i,'').replace(/[-_+]+/g,' ').trim(); return s.replace(/\b\w/g, function(c){ return c.toUpperCase(); }); }
  $('bcBuild').onclick = function(){
    var u; try { u = new URL(v('bcFrom')); } catch(e){ $('bcCheck').className='kw-result bad'; $('bcCheck').innerHTML = '<strong>Enter a full URL starting with https:// to build a trail.</strong>'; return; }
    var parts = u.pathname.split('/').filter(Boolean), out = ['Home | ' + u.origin + '/'], path = u.origin, slash = /\/$/.test(u.pathname);
    parts.forEach(function(p, i){ path += '/' + p; out.push(nice(p) + ' | ' + path + (i < parts.length - 1 || slash ? '/' : '')); });
    $('bcList').value = out.join('\n'); run();
  };
  function run(){
    var I = [], P = 'bc', items = pairs('bcList'), skipLast = $('bcLast').checked, host = {};
    if (items.length < 2) I.push(['bad', 'A breadcrumb trail needs at least two items.']);
    var list = items.map(function(it, i){
      var last = i === items.length - 1;
      if (!it.name) I.push(['bad', 'Item ' + (i+1) + ' is missing a name.']);
      if (!it.url && !(last && skipLast)) I.push(['bad', 'Item ' + (i+1) + ' (' + (it.name || 'no name') + ') needs a URL.']);
      else if (it.url && !(last && skipLast)){ urlCheck(it.url, 'URL for ' + (it.name || 'item ' + (i+1)), I); try { host[new URL(it.url).host] = 1; } catch(e){} }
      return { '@type':'ListItem', position: i + 1, name: it.name, item: (last && skipLast) ? '' : it.url };
    });
    if (Object.keys(host).length > 1) I.push(['warn', 'Your URLs use more than one domain. Breadcrumbs should stay on the same site.']);
    $('bcPrev').innerHTML = items.map(function(it){ return '<span class="chip">' + esc(it.name || '?') + '</span>'; }).join('<span style="color:#999">&rsaquo;</span>');
    render(P, { '@context':'https://schema.org', '@type':'BreadcrumbList', itemListElement: list }, I);
  }
  wire('bc', run);
''',
        content=r'''
    <h2>What Is Breadcrumb Schema?</h2>
    <p>Breadcrumb schema is structured data that shows where a page sits in your site. It uses the <code>BreadcrumbList</code> type with one <code>ListItem</code> per level, such as Home, then Blog, then the post.</p>
    <p>Google can use it to show a clean trail of categories in your search result instead of a long URL, which helps people understand your page before they click.</p>

    <h2>How to Use the Breadcrumb Schema Generator</h2>
    <ol>
      <li><strong>Fastest way:</strong> paste the page URL and click Build Trail From URL. Each folder in the path becomes a step.</li>
      <li><strong>Edit the names</strong> so they match the labels on your site, for example "SEO Guides" instead of "Seo".</li>
      <li><strong>Or type your own list</strong> as <code>Name | URL</code>, one per line, from the top level down.</li>
      <li><strong>Copy the code</strong> and add it to the page, then test it in the Rich Results Test.</li>
    </ol>

    <h2>Google's Breadcrumb Rules</h2>
    <table class="lim">
      ''' + th('Rule', 'Details') + '''
      <tbody>
        <tr><td>At least two items</td><td>A single item trail is not valid</td></tr>
        <tr><td><code>position</code></td><td>Starts at 1 for the top level and counts up</td></tr>
        <tr><td><code>name</code></td><td>The label shown for each step</td></tr>
        <tr><td><code>item</code></td><td>The URL of each step. Optional for the last item, where Google uses the page URL</td></tr>
        <tr><td>Multiple trails</td><td>Allowed if a page sits in more than one category</td></tr>
      </tbody>
    </table>
    <p>Read the official <a href="''' + G + '''breadcrumb" target="_blank" rel="noopener">Google breadcrumb documentation</a> for examples.</p>

    <h2>Tips for Better Breadcrumbs</h2>
    <ul>
      <li>Show a visible breadcrumb on the page too. Markup should describe what users see.</li>
      <li>Base the trail on how people browse your site, not only on your URL folders.</li>
      <li>Keep names short. One to three words per step reads best.</li>
      <li>Breadcrumbs also pass internal links up to category pages, which helps them rank.</li>
    </ul>
    <p>For more on site structure, read our guides to <a href="https://brandella.in/internal-linking-best-practices-seo-rankings/">internal linking best practices</a> and <a href="https://brandella.in/url-structure-for-ai-seo/">URL structure for SEO</a>. To create clean URLs in the first place, try the <a href="https://brandella.in/tools/seo-tools/seo-slug-generator/">SEO slug generator</a>.</p>
''',
        faqs=[
            ("Do breadcrumbs still show in Google results?", "Google still supports breadcrumb structured data and lists it in its search gallery. How the trail appears can vary by device and query, but valid markup keeps your page eligible."),
            ("Should the last breadcrumb have a URL?", "It is optional. If you leave out the item URL for the last step, Google uses the URL of the page the markup is on. Tick the option above to do this."),
            ("Can a page have more than one breadcrumb trail?", "Yes. If a product or post belongs to two categories, you can add two BreadcrumbList blocks. Google allows multiple trails for one page."),
            ("Is anything I enter uploaded?", "No. The breadcrumb schema generator runs in your browser. URLs you paste are only read on your device."),
        ],
        related=[("Internal Linking Best Practices", "internal-linking-best-practices-seo-rankings"), ("URL Structure for AI SEO", "url-structure-for-ai-seo"),
                 ("Pagination SEO Explained", "pagination-seo-explained-best-practices"), ("How Google Crawls Websites", "how-google-crawls-websites")],
    ))

    # ---------- 6. EVENT SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='event-schema-generator', short='ES', name='Event Schema Generator',
        card='Create Event JSON LD with dates, venue, tickets, organizer, performers and event status.',
        title='Event Schema Generator: Free Event JSON LD Markup',
        desc='Free event schema generator. Create Event JSON LD with start and end dates, venue address, tickets, organizer, performers and cancelled or postponed status.',
        h1='Event Schema Generator',
        lead='Get your concert, workshop or meetup into Google\'s event listings. Fill in the date, venue and tickets and copy valid Event JSON LD.',
        tool='''<section class="tool" aria-label="Event schema generator" id="evForm">
    <div class="card">
      <h2>Event Details</h2>
      ''' + F('evName', 'Event Name', 'Growth Marketing Summit 2027') + '''
      ''' + F('evDesc', 'Description', 'A one day conference on search, social and AI marketing with 20 speakers and hands on workshops.', tag='textarea') + '''
      ''' + R2(F('evSD', 'Start Date', '2027-01-16', typ='date'), F('evST', 'Start Time', '09:30', typ='time', em='optional')) + '''
      ''' + R2(F('evED', 'End Date', '2027-01-16', typ='date'), F('evET', 'End Time', '18:00', typ='time', em='optional')) + '''
      ''' + R2(F('evTz', 'Time Zone', '+05:30', tag='select', opts=TZ), F('evStatus', 'Event Status', 'EventScheduled', tag='select', opts=[('EventScheduled', 'Scheduled'), ('EventRescheduled', 'Rescheduled'), ('EventPostponed', 'Postponed'), ('EventCancelled', 'Cancelled')])) + '''
      <div id="evPrevBox" style="display:none">''' + F('evPrev', 'Original Start Date', '', typ='date', em='for rescheduled events') + '''</div>
      ''' + F('evImg', 'Image URLs', 'https://www.example.com/images/summit-16x9.jpg', tag='textarea', em='one per line') + '''
      <h2 style="margin-top:8px">Venue</h2>
      ''' + F('evVenue', 'Venue Name', 'Jio World Convention Centre') + '''
      ''' + F('evStreet', 'Street Address', 'G Block, Bandra Kurla Complex') + '''
      ''' + R2(F('evCity', 'City', 'Mumbai'), F('evRegion', 'State or Region', 'Maharashtra')) + '''
      ''' + R2(F('evZip', 'Postal Code', '400098'), F('evCountry', 'Country Code', 'IN', em='2 letters')) + '''
      <h2 style="margin-top:8px">Tickets and People</h2>
      ''' + F('evTUrl', 'Ticket Page URL', 'https://www.example.com/summit/tickets/') + '''
      ''' + R2(F('evPrice', 'Lowest Ticket Price', '2999', em='0 if free'), F('evCur', 'Currency', 'INR', tag='select', opts=CUR)) + '''
      ''' + R2(F('evAvail', 'Ticket Availability', 'InStock', tag='select', opts=[('InStock', 'On sale'), ('PreOrder', 'Pre order'), ('SoldOut', 'Sold out'), ('', 'Not on sale yet')]), F('evFrom', 'Tickets On Sale From', '2026-11-01', typ='date', em='optional')) + '''
      ''' + R2(F('evOrg', 'Organizer Name', 'Example Events'), F('evOrgUrl', 'Organizer URL', 'https://www.example.com/')) + '''
      ''' + F('evPerf', 'Performers or Speakers', 'Ananya Rao\nRahul Mehta', tag='textarea', em='one per line') + '''
      ''' + F('evPType', 'Performer Type', 'Person', tag='select', opts=[('Person', 'Person'), ('PerformingGroup', 'Band or group')]) + '''
    </div>
    ''' + OUT('ev', '<li>Add one Event block per date if the event repeats</li><li>Never change the start date of a cancelled event, just set the status</li><li>The ticket link should go to a page where anyone can buy</li>') + '''
  </section>''',
        js=SJS + r'''
  function run(){
    var I = [], P = 'ev', st = v('evStatus');
    $('evPrevBox').style.display = st === 'EventRescheduled' ? 'block' : 'none';
    var start = dt('evSD','evST','evTz'), end = dt('evED','evET','evTz');
    if (!v('evName')) I.push(['bad', 'Event name is required.']);
    if (!start) I.push(['bad', 'Start date is required.']);
    if (start && end && v('evED') + v('evET') < v('evSD') + v('evST')) I.push(['bad', 'The end date is before the start date.']);
    if (!v('evStreet') && !v('evCity')) I.push(['bad', 'Venue address is required. Google only supports events at a physical location.']);
    if (!v('evVenue')) I.push(['warn', 'Add the venue name.']);
    if (v('evSD') && v('evSD') < new Date().toISOString().slice(0,10)) I.push(['warn', 'This start date is in the past. Past events are not shown in event results.']);
    if (st === 'EventRescheduled' && !v('evPrev')) I.push(['warn', 'Add the original start date for a rescheduled event.']);
    if (!end) I.push(['warn', 'Add an end date.']);
    if (!lines('evImg').length) I.push(['warn', 'Add an image. Google recommends 16x9, 4x3 and 1x1 versions.']);
    lines('evImg').forEach(function(u){ urlCheck(u, 'Image "' + u + '"', I); });
    urlCheck(v('evTUrl'), 'Ticket page URL', I); urlCheck(v('evOrgUrl'), 'Organizer URL', I);
    var pn = num(v('evPrice')), offers = '';
    if (v('evPrice') && pn === undefined) I.push(['bad', 'Ticket price must be a plain number, such as 2999 or 0.']);
    if (v('evTUrl') || pn !== undefined){
      offers = { '@type':'Offer', url: v('evTUrl'), price: pn, priceCurrency: pn !== undefined ? v('evCur') : '',
        availability: v('evAvail') ? 'https://schema.org/' + v('evAvail') : '', validFrom: v('evFrom') ? v('evFrom') + 'T00:00:00' + v('evTz') : '' };
      if (!v('evAvail') && !v('evFrom')) I.push(['warn', 'If tickets are not on sale yet, add the date they go on sale.']);
    } else I.push(['warn', 'Add ticket details: a ticket URL and the lowest price.']);
    if (!v('evOrg')) I.push(['warn', 'Add the organizer name and URL.']);
    var pt = v('evPType'), perf = lines('evPerf').map(function(n){ return { '@type': pt, name: n }; });
    var o = { '@context':'https://schema.org', '@type':'Event', name: v('evName'), description: v('evDesc'), image: lines('evImg'),
      startDate: start, endDate: end, eventStatus: 'https://schema.org/' + st,
      previousStartDate: st === 'EventRescheduled' ? v('evPrev') : '', eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
      location: { '@type':'Place', name: v('evVenue'), address: addr(P) },
      offers: offers, organizer: { '@type':'Organization', name: v('evOrg'), url: v('evOrgUrl') },
      performer: perf.length === 1 ? perf[0] : perf };
    render(P, o, I);
  }
  wire('ev', run);
''',
        content=r'''
    <h2>What Is Event Schema?</h2>
    <p>Event schema is structured data that describes an event people can attend: what it is, when it starts, where it happens and how to get tickets. Google can use it to list your event in its event search experience, with dates and venue shown at a glance.</p>
    <p>This event schema generator writes the <code>Event</code> type with a nested <code>Place</code>, <code>Offer</code>, organizer and performers.</p>

    <h2>How to Use the Event Schema Generator</h2>
    <ol>
      <li><strong>Enter the event name and description.</strong></li>
      <li><strong>Set the start and end dates.</strong> Add times and a time zone if you know them. For all day events, leave the time empty.</li>
      <li><strong>Fill in the venue</strong> with the full address.</li>
      <li><strong>Add tickets.</strong> Use the lowest price including fees, or 0 for a free event.</li>
      <li><strong>Copy the code</strong> into your event page and test it.</li>
    </ol>

    <h2>Event Properties Explained</h2>
    <table class="lim">
      ''' + th('Property', 'Status', 'Notes') + '''
      <tbody>
        <tr><td><code>name</code></td><td>Required</td><td>The event title</td></tr>
        <tr><td><code>startDate</code></td><td>Required</td><td>ISO 8601 with a time zone offset, or a date only for all day events</td></tr>
        <tr><td><code>location</code></td><td>Required</td><td>A Place with a full address</td></tr>
        <tr><td><code>eventStatus</code></td><td>Recommended</td><td>Scheduled, Rescheduled, Postponed or Cancelled</td></tr>
        <tr><td><code>offers</code></td><td>Recommended</td><td>Ticket URL, price, currency and availability</td></tr>
        <tr><td><code>organizer</code>, <code>performer</code></td><td>Recommended</td><td>Who runs and who appears at the event</td></tr>
        <tr><td><code>previousStartDate</code></td><td>Recommended</td><td>Only for rescheduled events</td></tr>
      </tbody>
    </table>
    <p>See the full list in <a href="''' + G + '''event" target="_blank" rel="noopener">Google's event structured data guide</a>.</p>

    <h2>Handling Changes to Your Event</h2>
    <ul>
      <li><strong>Cancelled:</strong> set the status to Cancelled and keep the original date.</li>
      <li><strong>Postponed with no new date:</strong> set Postponed and keep the original date.</li>
      <li><strong>Rescheduled:</strong> set the new start date, choose Rescheduled and add the original date.</li>
      <li><strong>Online only:</strong> Google's event results only support events at a physical place, so purely virtual events will not appear.</li>
    </ul>
    <p>Promoting your event? Plan the posts with our <a href="https://brandella.in/content-calendar-planning/">content calendar guide</a> and track sign ups with <a href="https://brandella.in/utm-parameters-explained/">UTM parameters</a>. For the venue itself, use the <a href="https://brandella.in/tools/schema-generators/local-business-schema-generator/">local business schema generator</a>.</p>
''',
        faqs=[
            ("Can I use event schema for webinars or online events?", "Google's event rich results only support events that happen at a physical location. You can still describe an online event with schema.org, but it will not appear in Google's event listings."),
            ("How do I mark up an event that repeats every week?", "Add a separate Event block for each date, each with its own start date. Do not put several dates in one Event."),
            ("What price should I use if there are several ticket types?", "Google asks for the lowest available price, including any fees. Use 0 for free events."),
            ("Is my event data stored?", "No. The event schema generator runs entirely in your browser and nothing is uploaded."),
        ],
        related=[("Content Calendar Planning", "content-calendar-planning"), ("UTM Parameters Explained", "utm-parameters-explained"),
                 ("How to Add Schema Markup With JSON LD", "how-to-add-schema-markup-json-ld"), ("Social Media KPIs to Track", "social-media-kpis-every-marketer-should-track")],
    ))

    # ---------- 7. VIDEO SCHEMA GENERATOR ----------
    TOOLS.append(dict(
        slug='video-schema-generator', short='VS', name='Video Schema Generator',
        card='Create VideoObject JSON LD with thumbnail, duration, embed URL and key moments, with a YouTube helper.',
        title='Video Schema Generator: VideoObject and Key Moments',
        desc='Free video schema generator. Create VideoObject JSON LD with thumbnail, upload date, duration, embed URL and key moments. Paste a YouTube link to start.',
        h1='Video Schema Generator',
        lead='Create VideoObject JSON LD for any video on your page. Paste a YouTube link to fill the embed and thumbnail, add chapters, and get key moments markup too.',
        tool='''<section class="tool" aria-label="Video schema generator" id="vdForm">
    <div class="card">
      <h2>Video Details</h2>
      ''' + F('vdYt', 'YouTube Link', '', ph='https://www.youtube.com/watch?v=...', em='optional shortcut') + '''
      ''' + F('vdName', 'Video Title', 'How to Add Schema Markup to WordPress in 5 Minutes') + '''
      ''' + F('vdDesc', 'Description', 'A quick walkthrough of adding JSON LD schema markup to a WordPress page and testing it in the Rich Results Test.', tag='textarea') + '''
      ''' + F('vdThumb', 'Thumbnail URLs', 'https://www.example.com/videos/schema-wordpress-thumb.jpg', tag='textarea', em='one per line') + '''
      ''' + R2(F('vdUD', 'Upload Date', '2026-10-15', typ='date'), F('vdUT', 'Upload Time', '10:00', typ='time')) + '''
      ''' + R2(F('vdTz', 'Time Zone', '+05:30', tag='select', opts=TZ), F('vdDur', 'Duration', '5:42', em='h:mm:ss or m:ss')) + '''
      ''' + F('vdContent', 'Video File URL (contentUrl)', 'https://www.example.com/videos/schema-wordpress.mp4', em='optional') + '''
      ''' + F('vdEmbed', 'Player URL (embedUrl)', 'https://www.example.com/embed/schema-wordpress', em='optional') + '''
      ''' + R2(F('vdViews', 'View Count', '', em='optional'), F('vdExp', 'Expires On', '', typ='date', em='optional')) + '''
      <h2 style="margin-top:8px">Key Moments <em style="font-size:13px;font-weight:600;color:#777">optional</em></h2>
      ''' + F('vdWatch', 'Watch Page URL', 'https://www.example.com/videos/schema-wordpress/', em='where the video plays') + '''
      ''' + R2(F('vdParam', 'Time Parameter', 't', em='e.g. t'), F('vdCreator', 'Creator Name', 'Example Media', em='optional')) + '''
      ''' + F('vdClips', 'Chapters', '0:00 Introduction\n0:35 Choosing a schema type\n2:10 Adding the code in WordPress\n4:05 Testing in Google', tag='textarea', em='start time then label, one per line', extra=' class="mono" style="min-height:130px"') + '''
    </div>
    ''' + OUT('vd', '<li>Each video needs its own unique title</li><li>Use a thumbnail that actually shows the video</li><li>Key moments need a video of at least 30 seconds that can start at any time</li>') + '''
  </section>''',
        js=SJS + r'''
  function secs(s){ s = String(s).trim(); if (!s) return NaN; if (/^\d+$/.test(s)) return +s;
    if (!/^\d+(:\d{1,2}){1,2}$/.test(s)) return NaN; return s.split(':').reduce(function(a, x){ return a * 60 + (+x); }, 0); }
  function iso(t){ var h = Math.floor(t/3600), m = Math.floor(t%3600/60), s = t%60; return 'PT' + (h ? h + 'H' : '') + (m ? m + 'M' : '') + (s || (!h && !m) ? s + 'S' : ''); }
  $('vdYt').addEventListener('input', function(){
    var m = v('vdYt').match(/(?:youtu\.be\/|[?&]v=|\/embed\/|\/shorts\/|\/live\/)([\w-]{11})/);
    if (!m) return;
    $('vdEmbed').value = 'https://www.youtube.com/embed/' + m[1];
    $('vdThumb').value = 'https://i.ytimg.com/vi/' + m[1] + '/hqdefault.jpg';
    $('vdWatch').value = 'https://www.youtube.com/watch?v=' + m[1];
    $('vdContent').value = ''; $('vdParam').value = 't';
  });
  function run(){
    var I = [], P = 'vd';
    if (!v('vdName')) I.push(['bad', 'Video title is required.']);
    var th = lines('vdThumb'); if (!th.length) I.push(['bad', 'A thumbnail URL is required.']);
    th.forEach(function(u){ urlCheck(u, 'Thumbnail "' + u + '"', I); });
    var up = dt('vdUD','vdUT','vdTz'); if (!up) I.push(['bad', 'Upload date is required.']);
    else if (!v('vdUT') || !v('vdTz')) I.push(['warn', 'Add a time and time zone to the upload date. Otherwise Google assumes the time zone of Googlebot.']);
    if (!v('vdDesc')) I.push(['warn', 'Add a description of the video.']);
    var d = secs(v('vdDur')); if (v('vdDur') && isNaN(d)) I.push(['bad', 'Duration should look like 5:42 or 1:05:30.']);
    if (!v('vdDur')) I.push(['warn', 'Add the duration.']);
    if (!v('vdContent') && !v('vdEmbed')) I.push(['warn', 'Add a video file URL or a player URL so Google can fetch the video.']);
    urlCheck(v('vdContent'), 'Video file URL', I); urlCheck(v('vdEmbed'), 'Player URL', I);
    var views = num(v('vdViews')); if (v('vdViews') && views === undefined) I.push(['bad', 'View count must be a whole number.']);
    var raw = lines('vdClips'), clips = [], seen = {};
    raw.forEach(function(l){
      var m = l.match(/^(\d+(?::\d{1,2}){0,2})\s*[|.)]?\s*(.+)$/);
      if (!m){ I.push(['bad', 'Could not read chapter line "' + l + '". Use a start time then a label, like 1:30 Setup.']); return; }
      var s = secs(m[1]); if (seen[s]){ I.push(['bad', 'Two chapters start at ' + m[1] + '. Each start time must be unique.']); return; }
      seen[s] = 1; clips.push({ s: s, name: m[2].trim() });
    });
    clips.sort(function(a, b){ return a.s - b.s; });
    var parts = '';
    if (clips.length){
      var w = v('vdWatch'), par = v('vdParam') || 't';
      if (!isUrl(w)) I.push(['bad', 'Key moments need a watch page URL starting with https://']);
      if (!isNaN(d) && d < 30) I.push(['bad', 'Key moments need a video of at least 30 seconds.']);
      if (!isNaN(d) && clips[clips.length-1].s >= d) I.push(['bad', 'A chapter starts after the video ends. Check the duration.']);
      parts = clips.map(function(c, i){
        var end = i < clips.length - 1 ? clips[i+1].s : (isNaN(d) ? undefined : d);
        return { '@type':'Clip', name: c.name, startOffset: c.s, endOffset: end, url: w + (w.indexOf('?') > -1 ? '&' : '?') + par + '=' + c.s };
      });
    }
    var o = { '@context':'https://schema.org', '@type':'VideoObject', name: v('vdName'), description: v('vdDesc'), thumbnailUrl: th,
      uploadDate: up, duration: isNaN(d) ? '' : iso(d), contentUrl: v('vdContent'), embedUrl: v('vdEmbed'),
      expires: v('vdExp') ? v('vdExp') + 'T00:00:00' + v('vdTz') : '',
      creator: v('vdCreator') ? { '@type':'Organization', name: v('vdCreator') } : '',
      interactionStatistic: views !== undefined ? { '@type':'InteractionCounter', interactionType: { '@type':'WatchAction' }, userInteractionCount: Math.round(views) } : '',
      hasPart: parts };
    render(P, o, I);
  }
  wire('vd', run);
''',
        content=r'''
    <h2>What Is Video Schema?</h2>
    <p>Video schema is structured data that describes a video on your page using the <code>VideoObject</code> type. It gives Google the title, thumbnail, upload date, length and where to find the video file or player.</p>
    <p>With it, your page can appear in video results and the Videos tab, and with chapters added, Google can show key moments that let people jump straight to a section.</p>

    <h2>How to Use the Video Schema Generator</h2>
    <ol>
      <li><strong>Got a YouTube video?</strong> Paste the link at the top. The tool fills the player URL, a thumbnail and the watch page for you.</li>
      <li><strong>Add the title, description and upload date</strong> with time and time zone.</li>
      <li><strong>Enter the duration</strong> as minutes and seconds, such as 5:42. The tool converts it to ISO 8601, like <code>PT5M42S</code>.</li>
      <li><strong>Add chapters</strong> as a start time then a label, one per line, to create key moments.</li>
      <li><strong>Copy the code</strong> into the page where the video is embedded.</li>
    </ol>

    <h2>VideoObject Properties</h2>
    <table class="lim">
      ''' + th('Property', 'Status', 'Notes') + '''
      <tbody>
        <tr><td><code>name</code></td><td>Required</td><td>A unique title for each video</td></tr>
        <tr><td><code>thumbnailUrl</code></td><td>Required</td><td>A unique thumbnail image for the video</td></tr>
        <tr><td><code>uploadDate</code></td><td>Required</td><td>ISO 8601 with a time zone</td></tr>
        <tr><td><code>contentUrl</code></td><td>Recommended</td><td>The actual video file, the best way for Google to fetch it</td></tr>
        <tr><td><code>embedUrl</code></td><td>Recommended</td><td>The player URL, used when there is no file URL</td></tr>
        <tr><td><code>duration</code></td><td>Recommended</td><td>ISO 8601 duration, such as PT1H2M30S</td></tr>
        <tr><td><code>hasPart</code></td><td>Recommended</td><td>Clip items with start and end seconds for key moments</td></tr>
      </tbody>
    </table>
    <p>Full details are in <a href="''' + G + '''video" target="_blank" rel="noopener">Google's video structured data guide</a>.</p>

    <h2>Key Moments Tips</h2>
    <ul>
      <li>The video must be at least 30 seconds long and support starting at a set time through the URL.</li>
      <li>Each chapter needs a unique start time. The tool works out end times for you.</li>
      <li>On YouTube, adding timestamps in the video description also creates chapters on YouTube itself.</li>
      <li>Put the markup on the page where the video plays, not on a page that only links to it.</li>
    </ul>
    <p>Get more from video with our <a href="https://brandella.in/7-creative-video-marketing-ideas/">creative video marketing ideas</a> and <a href="https://brandella.in/optimize-images-for-seo-without-losing-quality/">image optimization guide</a> for better thumbnails. Writing the post around the video? Add the <a href="https://brandella.in/tools/schema-generators/article-schema-generator/">article schema generator</a> output too.</p>
''',
        faqs=[
            ("Do I need video schema for embedded YouTube videos?", "It is not strictly needed, since Google can often detect embeds, but markup makes the title, thumbnail, date and chapters explicit and can help your own page appear for the video."),
            ("What is the difference between contentUrl and embedUrl?", "contentUrl points to the video file itself, such as an MP4. embedUrl points to the player, usually the src of an iframe. Google prefers contentUrl when you can provide it."),
            ("How do I write video duration in ISO 8601?", "Use PT, then hours with H, minutes with M and seconds with S. For example, 5 minutes 42 seconds is PT5M42S. This tool converts it for you."),
            ("Is my video information uploaded?", "No. The video schema generator works only in your browser. Even the YouTube helper just reads the video ID from the link you paste, without contacting YouTube."),
        ],
        related=[("7 Creative Video Marketing Ideas", "7-creative-video-marketing-ideas"), ("YouTube Monetization Guide", "youtube-monetization-2025"),
                 ("What Is Schema Markup", "what-is-schema-markup"), ("Optimize Images for SEO", "optimize-images-for-seo-without-losing-quality")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'schema-generators'; t['updated'] = '2026-10-29'
        t['content'] = t['content'].replace('<table class="lim">', '<div style="overflow-x:auto"><table class="lim">').replace('</table>', '</table></div>')
        t['tool'] = t['tool'].replace('<div class="card">', '<div class="card" style="min-width:0">')
