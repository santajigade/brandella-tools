"""Batch 21 (2026-11-18): Content Writing Tools category, fourth tool (American to British English Converter).
Facts checked 2026-11-18: Oxford spelling (Oxford University Press house style) uses the -ize suffix (organize,
realize) but keeps -yse (analyse, paralyse) and every other British spelling (colour, centre). Standard British
and Indian English mostly use -ise. UK uses practice (noun) and practise (verb), licence (noun) and license (verb),
programme (plan, show) but program (computer), metre (unit) but meter (device), tyre (wheel) but tire (verb),
kerb (road edge) but curb (verb), judgement in general use but judgment in legal rulings.
Google Search Central, localized versions (developers.google.com/search/docs/specialty/international/localized-versions):
use hreflang to tell Google about language and region versions of a page, such as en-gb and en-us.
Search demand: "american to british english converter", "us to uk spelling converter", "british to american
converter" are served by Fun Translations (us2uk, uk2us), rajbhasha.net usa to uk english, elysiatools and others.
This one does both directions, offers -ise or Oxford -ize, flags words that depend on meaning instead of blindly
changing them, lets the writer untick any change (proper nouns such as Pearl Harbor), skips URLs, emails and code,
and reports mixed US and UK spelling in the input. Runs fully in the browser."""
import json
from batch_2026_11_07_developer_tools import F, S, BASEJS, th

T = 'https://brandella.in/tools/content-writing-tools/'
B = 'https://brandella.in/'
EXT = 'target="_blank" rel="noopener"'

# ---------- word data (US form, UK form). Only explicit forms, so nothing unexpected is touched. ----------
P = []  # (us, uk_ise, uk_ize)

def pair(us, uk, ukz=None): P.append((us, uk, ukz or uk))

OUR = {
    'color': ['', 's', 'ed', 'ing', 'ings', 'ful', 'fully', 'less', 'ist', 'ists', 'way', 'ways', 'blind', 'fast'],
    'discolor': ['', 's', 'ed', 'ing', 'ation'], 'multicolor': ['', 'ed'], 'watercolor': ['', 's', 'ist'],
    'honor': ['', 's', 'ed', 'ing', 'able', 'ably'], 'dishonor': ['', 's', 'ed', 'able', 'ably'],
    'favor': ['', 's', 'ed', 'ing', 'able', 'ably', 'ite', 'ites', 'itism'], 'unfavorable': [''], 'unfavorably': [''], 'disfavor': [''],
    'flavor': ['', 's', 'ed', 'ing', 'ings', 'ful', 'less', 'some'],
    'labor': ['', 's', 'ed', 'ing', 'er', 'ers'], 'neighbor': ['', 's', 'ing', 'hood', 'hoods', 'ly', 'liness'],
    'behavior': ['', 's', 'al', 'ally', 'ism', 'ist', 'ists'], 'misbehavior': [''],
    'harbor': ['', 's', 'ed', 'ing'], 'humor': ['', 's', 'ed', 'ing', 'less'], 'rumor': ['', 's', 'ed'],
    'vapor': ['', 's'], 'vigor': [''], 'odor': ['', 's', 'less'], 'savior': ['', 's'],
    'savor': ['', 's', 'ed', 'ing', 'y'], 'savories': [''], 'armor': ['', 'ed', 'y', 'er', 'ers'],
    'endeavor': ['', 's', 'ed', 'ing'], 'parlor': ['', 's'], 'rigor': ['', 's'], 'splendor': ['', 's'],
    'valor': [''], 'clamor': ['', 's', 'ed', 'ing'], 'candor': [''], 'tumor': ['', 's'], 'ardor': [''],
    'fervor': [''], 'demeanor': ['', 's'], 'glamor': [''],
}
for stem, sufs in OUR.items():
    i = stem.rfind('or')
    for s in sufs: pair(stem + s, stem[:i] + 'our' + stem[i + 2:] + s)

IZE = ('organ reorgan disorgan real recogn apolog priorit optim custom minim maxim summar emphas critic final util standard '
       'categor memor special author character civil modern monet personal visual normal sanit synchron central capital '
       'familiar general global harmon hospital ideal immun initial legal local mobil neutral popular public rational '
       'revolution scrutin stabil steril symbol sympath terror theor vapor verbal privat democrat energ jeopard legitim '
       'marginal material mesmer metabol ostrac patron penal plagiar polar pressur random social subsid vandal victim '
       'digit incentiv operational contextual conceptual hypothes agon antagon dramat fertil homogen human item '
       'commercial colon crystal decentral demoral desensit destabil formal industrial internal accessor equal fantas '
       'galvan glamor imperial institutional italic journal liberal lion mechan miniatur moral motor oxid pasteur philosoph '
       'proselyt radical regular satir scandal secular sensit serial solemn spiritual tantal tempor trivial tyrann urban '
       'vocal natural western woman computer container alphabet emotional dehuman deodor desalin evangel exorc memorial caramel').split()
seen = set()
for st in IZE:
    if st in seen: continue
    seen.add(st)
    for a, b in [('ize', 'ise'), ('izes', 'ises'), ('ized', 'ised'), ('izing', 'ising'), ('izer', 'iser'), ('izers', 'isers'),
                 ('ization', 'isation'), ('izations', 'isations'), ('izational', 'isational')]:
        pair(st + a, st + b, st + a)
for st in ['anal', 'paral', 'catal', 'electrol', 'dial', 'hydrol']:
    for a, b in [('yze', 'yse'), ('yzes', 'yses'), ('yzed', 'ysed'), ('yzing', 'ysing'), ('yzer', 'yser'), ('yzers', 'ysers')]:
        pair(st + a, st + b)

RE_ = {'center': ['', 's', 'piece', 'pieces', 'fold'], 'epicenter': ['', 's'], 'theater': ['', 's', 'goer', 'goers'],
       'fiber': ['', 's', 'glass', 'board'], 'liter': ['', 's'], 'kilometer': ['', 's'], 'centimeter': ['', 's'],
       'millimeter': ['', 's'], 'milliliter': ['', 's'], 'caliber': ['', 's'], 'saber': ['', 's'], 'somber': ['', 'ly'],
       'specter': ['', 's'], 'luster': ['', 'less'], 'meager': ['', 'ly'], 'sepulcher': [''], 'lackluster': ['']}
for stem, sufs in RE_.items():
    for s in sufs: pair(stem + s, stem[:-2] + 're' + s)
for us, uk in [('centered', 'centred'), ('centering', 'centring'), ('maneuver', 'manoeuvre'), ('maneuvers', 'manoeuvres'),
               ('maneuvered', 'manoeuvred'), ('maneuvering', 'manoeuvring'), ('maneuverable', 'manoeuvrable'),
               ('maneuverability', 'manoeuvrability'), ('defense', 'defence'), ('defenses', 'defences'), ('defenseless', 'defenceless'),
               ('offense', 'offence'), ('offenses', 'offences'), ('pretense', 'pretence'), ('pretenses', 'pretences')]:
    pair(us, uk)

LL = {'travel': ['ed', 'ing', 'er', 'ers'], 'cancel': ['ed', 'ing'], 'label': ['ed', 'ing'], 'model': ['ed', 'ing', 'er', 'ers'],
      'fuel': ['ed', 'ing'], 'level': ['ed', 'ing'], 'signal': ['ed', 'ing'], 'total': ['ed', 'ing'], 'counsel': ['ed', 'ing', 'or', 'ors'],
      'dial': ['ed', 'ing'], 'quarrel': ['ed', 'ing'], 'equal': ['ed', 'ing'], 'rival': ['ed', 'ing'], 'tunnel': ['ed', 'ing'],
      'channel': ['ed', 'ing'], 'marvel': ['ed', 'ing', 'ous', 'ously'], 'jewel': ['er', 'ers'], 'wool': ['en', 'ens'],
      'panel': ['ed', 'ing', 'ist', 'ists'], 'pummel': ['ed', 'ing'], 'snorkel': ['ed', 'ing'], 'shovel': ['ed', 'ing'],
      'libel': ['ed', 'ing', 'ous'], 'council': ['or', 'ors'], 'duel': ['ed', 'ing'], 'grovel': ['ed', 'ing'], 'revel': ['ed', 'ing', 'er', 'ers'],
      'tranquil': ['ity'], 'initial': ['ed', 'ing'], 'yodel': ['ed', 'ing'], 'squirrel': ['ed', 'ing'], 'spiral': ['ed', 'ing'],
      'swivel': ['ed', 'ing'], 'unravel': ['ed', 'ing'], 'cudgel': ['ed', 'ing'], 'enamel': ['ed', 'ing'], 'gruel': ['ing']}
for stem, sufs in LL.items():
    for s in sufs: pair(stem + s, stem + 'l' + s)
for us, uk in [('jewelry', 'jewellery'), ('enroll', 'enrol'), ('enrolls', 'enrols'), ('enrollment', 'enrolment'), ('enrollments', 'enrolments'),
               ('fulfill', 'fulfil'), ('fulfills', 'fulfils'), ('fulfillment', 'fulfilment'), ('skillful', 'skilful'), ('skillfully', 'skilfully'),
               ('willful', 'wilful'), ('willfully', 'wilfully'), ('installment', 'instalment'), ('installments', 'instalments'),
               ('instill', 'instil'), ('instills', 'instils'), ('distill', 'distil'), ('distills', 'distils'), ('appall', 'appal'), ('appalls', 'appals'),
               ('gray', 'grey'), ('grays', 'greys'), ('grayish', 'greyish'), ('grayscale', 'greyscale'), ('grayed', 'greyed'), ('graying', 'greying'),
               ('aluminum', 'aluminium'), ('airplane', 'aeroplane'), ('airplanes', 'aeroplanes'),
               ('mold', 'mould'), ('molds', 'moulds'), ('molded', 'moulded'), ('molding', 'moulding'), ('moldy', 'mouldy'),
               ('smolder', 'smoulder'), ('smolders', 'smoulders'), ('smoldered', 'smouldered'), ('smoldering', 'smouldering'),
               ('molt', 'moult'), ('molting', 'moulting'), ('plow', 'plough'), ('plows', 'ploughs'), ('plowed', 'ploughed'), ('plowing', 'ploughing'),
               ('catalog', 'catalogue'), ('catalogs', 'catalogues'), ('cataloged', 'catalogued'), ('cataloging', 'cataloguing'),
               ('analog', 'analogue'), ('analogs', 'analogues'), ('prolog', 'prologue'), ('epilog', 'epilogue'), ('monolog', 'monologue'),
               ('pajamas', 'pyjamas'), ('cozy', 'cosy'), ('cozier', 'cosier'), ('coziest', 'cosiest'), ('coziness', 'cosiness'),
               ('mustache', 'moustache'), ('mustaches', 'moustaches'), ('skeptic', 'sceptic'), ('skeptics', 'sceptics'), ('skeptical', 'sceptical'),
               ('skeptically', 'sceptically'), ('skepticism', 'scepticism'), ('artifact', 'artefact'), ('artifacts', 'artefacts'),
               ('acknowledgment', 'acknowledgement'), ('acknowledgments', 'acknowledgements'), ('aging', 'ageing'),
               ('donut', 'doughnut'), ('donuts', 'doughnuts'), ('sulfur', 'sulphur'), ('sulfate', 'sulphate'), ('sulfates', 'sulphates'),
               ('yogurt', 'yoghurt'), ('omelet', 'omelette'), ('omelets', 'omelettes'), ('mollusk', 'mollusc'), ('mollusks', 'molluscs'),
               ('licorice', 'liquorice'), ('carburetor', 'carburettor'), ('pediatric', 'paediatric'), ('pediatrics', 'paediatrics'),
               ('pediatrician', 'paediatrician'), ('pediatricians', 'paediatricians'), ('anemia', 'anaemia'), ('anemic', 'anaemic'),
               ('anesthesia', 'anaesthesia'), ('anesthetic', 'anaesthetic'), ('anesthetics', 'anaesthetics'), ('anesthetist', 'anaesthetist'),
               ('fetus', 'foetus'), ('fetuses', 'foetuses'), ('hemoglobin', 'haemoglobin'), ('leukemia', 'leukaemia'), ('diarrhea', 'diarrhoea'),
               ('esophagus', 'oesophagus'), ('estrogen', 'oestrogen'), ('orthopedic', 'orthopaedic'), ('orthopedics', 'orthopaedics'),
               ('hemorrhage', 'haemorrhage'), ('gynecology', 'gynaecology'), ('furor', 'furore'), ('behoove', 'behove'), ('behooves', 'behoves'),
               ('practiced', 'practised'), ('practicing', 'practising'), ('ax', 'axe'), ('plowshare', 'ploughshare'), ('cigaret', 'cigarette'),
               ('sulfuric', 'sulphuric')]:
    pair(us, uk)

# words whose UK spelling depends on meaning: flagged, not changed unless the writer ticks them
FLAG = {
    'practice': ('practise', 'UK uses practice for the noun and practise for the verb.'),
    'practices': ('practises', 'UK uses practices for the noun and practises for the verb.'),
    'license': ('licence', 'UK uses licence for the noun and license for the verb.'),
    'licenses': ('licences', 'UK uses licences for the noun and licenses for the verb.'),
    'program': ('programme', 'UK uses programme for a plan, course or TV show, but program for computer software.'),
    'programs': ('programmes', 'UK uses programmes for plans, courses and TV shows, but programs for software.'),
    'meter': ('metre', 'UK uses metre for the unit of length, but meter for a device such as a gas meter.'),
    'meters': ('metres', 'UK uses metres for the unit of length, but meters for devices.'),
    'tire': ('tyre', 'UK uses tyre for the wheel, but tire for the verb, as in to tire quickly.'),
    'tires': ('tyres', 'UK uses tyres for wheels, but tires for the verb.'),
    'curb': ('kerb', 'UK uses kerb for the edge of a road, but curb for the verb, as in to curb spending.'),
    'curbs': ('kerbs', 'UK uses kerbs for road edges, but curbs for the verb.'),
    'judgment': ('judgement', 'UK writes judgement in general use, but judgment for a court ruling.'),
    'judgments': ('judgements', 'UK writes judgements in general use, but judgments for court rulings.'),
    'dialog': ('dialogue', 'UK writes dialogue for conversation, but dialog box is common for a window on screen.'),
    'check': ('cheque', 'UK uses cheque only for the bank payment. Every other check stays check.'),
    'checks': ('cheques', 'UK uses cheques only for bank payments.'),
    'draft': ('draught', 'UK uses draught for cold air or beer from a tap, but draft for a first version of writing.'),
    'story': ('storey', 'UK uses storey for a floor of a building, but story for a tale.'),
    'stories': ('storeys', 'UK uses storeys for floors of a building, but stories for tales.'),
}
# UK forms that map back to US without doubt
UK_ONLY = [('practise', 'practice'), ('practises', 'practices'), ('licence', 'license'), ('licences', 'licenses'),
           ('programme', 'program'), ('programmes', 'programs'), ('metre', 'meter'), ('metres', 'meters'), ('tyre', 'tire'),
           ('tyres', 'tires'), ('kerb', 'curb'), ('kerbs', 'curbs'), ('judgement', 'judgment'), ('judgements', 'judgments'),
           ('cheque', 'check'), ('cheques', 'checks'), ('storey', 'story'), ('storeys', 'stories'),
           ('draught', 'draft'), ('draughty', 'drafty'), ('chequebook', 'checkbook')]

# sanity: no duplicate US keys, no identical pairs
_d = {}
for us, uk, ukz in P:
    assert us != uk or us != ukz, us
    _d.setdefault(us, (uk, ukz))
_IZ = [('ize', 'ise'), ('izes', 'ises'), ('ized', 'ised'), ('izing', 'ising'), ('izer', 'iser'), ('izers', 'isers'),
       ('ization', 'isation'), ('izations', 'isations'), ('izational', 'isational')]
_gen = {st + a for st in seen for a, _ in _IZ}
DATA = json.dumps({'z': sorted(seen), 'p': [[u, a] for u, (a, b) in _d.items() if u not in _gen],
                   'f': {k: list(v) for k, v in FLAG.items()}, 'r': UK_ONLY}, separators=(',', ':'))

SAMPLE = ('Our new color guide will help you organize your brand. We analyzed the behavior of 500 shoppers at a mall in the city center, '
          'and the results were fascinating: bright colors and familiar flavors were their favorite.\n\n'
          'If you are traveling to the theater next week, check the program first. Every licensed vendor must show a valid license, '
          'and our team practiced the catalog launch for months. The defense of a strong brand starts with consistent labeling, '
          'so customize each label and prioritize clarity over humor.\n\n'
          'Read the full report at https://example.com/color-report or email team@example.com for the gray and aluminum samples.')


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    TOOLS.append(dict(
        slug='american-to-british-english-converter', short='UK', name='American to British English Converter',
        card='Convert US spelling to UK spelling and back, with Oxford ize option, flagged tricky words and a mixed spelling check.',
        title='American to British English Converter: US to UK Spelling',
        desc='Free American to British English converter. Change US spelling to UK or UK to US, with ise or Oxford ize, tricky words flagged and links kept safe.',
        h1='American to British English Converter',
        lead='Paste any text to switch it from American to British spelling, or back again. Every change is highlighted, words that depend on meaning are flagged for you to decide, and links, emails and code stay untouched.',
        tool='''<section class="tool" aria-label="American to British English converter">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('ukIn', 'Text to convert', SAMPLE, em='a blog post, AI draft, email or page copy', tag='textarea', extra=' style="min-height:280px"') + '''
      <div class="row2">
        ''' + F('ukDir', 'Convert', 'us2uk', tag='select', opts=[('us2uk', 'American to British'), ('uk2us', 'British to American')]) + '''
        ''' + F('ukSty', 'British style', 'ise', tag='select', opts=[('ise', 'ise endings (UK, India)'), ('ize', 'Oxford ize endings')]) + '''
      </div>
      ''' + F('ukKeep', 'Words to leave alone', 'Pearl Harbor, Labor Day', em='names and brands, separated by commas') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Converted Text</h2>
      <div class="stats">''' + S('ukChg', 'Spellings changed') + S('ukRev', 'Words to review') + S('ukUS', 'American in input') + S('ukGB', 'British in input') + '''</div>
      <div class="kw-result" id="ukVerdict"></div>
      <pre class="code-out" id="ukOut" style="display:block;margin-top:0;max-height:360px;overflow:auto;white-space:pre-wrap;word-break:normal;overflow-wrap:break-word;font-family:inherit;font-size:15px;line-height:1.7;background:#fff;color:#222;border:1px solid #ddd"></pre>
      <div class="actions"><button class="btn dark" id="ukCopy">Copy Converted Text</button><button class="btn" id="ukUse">Use as New Input</button><span class="toast" id="toast">Copied!</span></div>
      <p style="font-size:13px;color:#666;margin:8px 0 0"><mark style="background:#d9f2c4">Green</mark> is changed. <mark style="background:#ffe08a">Yellow</mark> needs your call, see the list below.</p>
    </div>
    <div class="card full" style="min-width:0">
      <h2>Every Change and Flag</h2>
      <p style="font-size:13px;color:#666;margin:0 0 8px">Untick a row to keep the original spelling, or tick a yellow row to change it everywhere.</p>
      <div style="overflow-x:auto;max-height:440px;overflow-y:auto"><table class="rtable" id="ukList"></table></div>
    </div>
  </section>''',
        js=STOP_JS + BASEJS + r'''
  var D = ''' + DATA + r''';
  var U2B = {}, U2Z = {}, B2U = {}, FL = D.f, RV = {}, choice = {}, last = '';
  var IZ = [['ize','ise'],['izes','ises'],['ized','ised'],['izing','ising'],['izer','iser'],['izers','isers'],['ization','isation'],['izations','isations'],['izational','isational']];
  D.z.forEach(function(st){ IZ.forEach(function(e){ D.p.push([st + e[0], st + e[1], st + e[0]]); }); });
  D.p.forEach(function(x){ U2B[x[0]] = x[1]; U2Z[x[0]] = x[2] || x[1]; B2U[x[1]] = x[0]; if (x[2]) B2U[x[2]] = B2U[x[2]] || x[0]; });
  D.r.forEach(function(x){ RV[x[0]] = x[1]; B2U[x[0]] = x[1]; });
  var TOK = /(https?:\/\/[^\s<>"]+|www\.[^\s<>"]+|[\w.+-]+@[\w-]+(?:\.[\w-]+)+|`[^`\n]*`)|([A-Za-z]+(?:['’][A-Za-z]+)?)/g;
  function shape(src, w){
    if (src.length > 1 && src === src.toUpperCase()) return w.toUpperCase();
    if (src[0] === src[0].toUpperCase()) return w[0].toUpperCase() + w.slice(1);
    return w;
  }
  function look(lw, dir, ize){
    if (dir === 'us2uk'){
      if (U2B.hasOwnProperty(lw)){ var t = ize ? U2Z[lw] : U2B[lw]; return t === lw ? null : {to: t}; }
      if (FL.hasOwnProperty(lw)) return {to: FL[lw][0], flag: FL[lw][1]};
      return null;
    }
    if (B2U.hasOwnProperty(lw) && B2U[lw] !== lw) return {to: B2U[lw]};
    return null;
  }
  function run(){
    var text = $('ukIn').value, dir = $('ukDir').value, ize = $('ukSty').value === 'ize';
    $('ukSty').disabled = dir !== 'us2uk';
    var keep = new Set($('ukKeep').value.split(/[,\n]/).map(function(s){ return s.trim().toLowerCase(); }).filter(Boolean));
    var keepRe = null, kp = Array.from(keep).filter(function(k){ return /\s/.test(k); });
    if (kp.length) keepRe = new RegExp('\\b(' + kp.map(function(k){ return k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\s+/g, '\\s+'); }).join('|') + ')\\b', 'gi');
    var protect = [];
    if (keepRe){ var km; keepRe.lastIndex = 0; while ((km = keepRe.exec(text))) protect.push([km.index, km.index + km[0].length]); }
    function isProt(i){ for (var k = 0; k < protect.length; k++) if (i >= protect[k][0] && i < protect[k][1]) return true; return false; }
    var html = '', plain = '', pos = 0, m, rows = {}, nUS = 0, nGB = 0, chg = 0, rev = 0;
    TOK.lastIndex = 0;
    while ((m = TOK.exec(text))){
      var seg = text.slice(pos, m.index); html += esc(seg); plain += seg; pos = m.index + m[0].length;
      if (m[1]){ html += esc(m[0]); plain += m[0]; continue; }
      var w = m[2], lw = w.toLowerCase().replace(/’/g, "'");
      var skip = keep.has(lw) || isProt(m.index);
      if (!skip && U2B.hasOwnProperty(lw) && !(ize && U2Z[lw] === lw)) nUS++;
      if (!skip && ((B2U.hasOwnProperty(lw) && !U2B.hasOwnProperty(lw)) || RV.hasOwnProperty(lw))) nGB++;
      var r = skip ? null : look(lw, dir, ize);
      if (!r){ html += esc(w); plain += w; continue; }
      var key = lw, row = rows[key] || (rows[key] = {from: lw, to: r.to, flag: r.flag, n: 0});
      row.n++;
      var on = choice.hasOwnProperty(dir + key) ? choice[dir + key] : !r.flag;
      var out = on ? shape(w, r.to) : w;
      if (on) chg++; else if (r.flag) rev++;
      var bg = r.flag && !on ? '#ffe08a' : on ? '#d9f2c4' : '#eee';
      html += '<mark title="' + esc(w + ' → ' + shape(w, r.to)) + '" style="background:' + bg + ';padding:0 1px;border-radius:3px">' + esc(out) + '</mark>';
      plain += out;
    }
    var tail = text.slice(pos); html += esc(tail); plain += tail; last = plain;
    $('ukOut').innerHTML = html || '<span style="color:#888">Your converted text will appear here.</span>';
    $('ukChg').textContent = fmtN(chg); $('ukRev').textContent = fmtN(rev); $('ukUS').textContent = fmtN(nUS); $('ukGB').textContent = fmtN(nGB);
    var target = dir === 'us2uk' ? 'British' : 'American';
    if (!text.trim()) say('ukVerdict', '', 'Paste some text to convert it.');
    else if (nUS && nGB) say('ukVerdict', 'warn', '<strong>Mixed spelling.</strong> Your text uses ' + nUS + ' American and ' + nGB + ' British spellings. The output below is now all ' + target + (rev ? ', apart from the yellow words you still need to check.' : '.'));
    else if (!chg && !rev) say('ukVerdict', 'ok', '<strong>Nothing to change.</strong> No spellings were found that differ in ' + target + ' English.');
    else say('ukVerdict', 'ok', '<strong>Done.</strong> ' + chg + ' spelling' + (chg === 1 ? '' : 's') + ' changed to ' + target + ' English' + (rev ? ', and ' + rev + ' word' + (rev === 1 ? '' : 's') + ' flagged for you to check.' : '.'));
    var list = Object.keys(rows).map(function(k){ return rows[k]; }).sort(function(a, b){ return (b.flag ? 1 : 0) - (a.flag ? 1 : 0) || b.n - a.n || (a.from < b.from ? -1 : 1); });
    $('ukList').innerHTML = list.length ? '<thead><tr><th>Change</th><th>From</th><th>To</th><th class="num">Times</th><th>Note</th></tr></thead><tbody>' + list.map(function(r){
      var on = choice.hasOwnProperty(dir + r.from) ? choice[dir + r.from] : !r.flag;
      return '<tr' + (r.flag ? ' style="background:#fff8e1"' : '') + '><td><input type="checkbox" data-k="' + esc(r.from) + '"' + (on ? ' checked' : '') + ' aria-label="Change ' + esc(r.from) + '"></td><td>' + esc(r.from) + '</td><td><strong>' + esc(r.to) + '</strong></td><td class="num">' + r.n + '</td><td>' + esc(r.flag || 'Spelling only') + '</td></tr>';
    }).join('') + '</tbody>' : '<tbody><tr><td>No spellings to change.</td></tr></tbody>';
  }
  $('ukList').addEventListener('change', function(ev){ var k = ev.target.getAttribute('data-k'); if (k){ choice[$('ukDir').value + k] = ev.target.checked; run(); } });
  ['ukIn', 'ukKeep'].forEach(function(i){ $(i).addEventListener('input', run); });
  ['ukDir', 'ukSty'].forEach(function(i){ $(i).addEventListener('change', run); });
  $('ukCopy').onclick = function(){ copyText(last, 'toast'); };
  $('ukUse').onclick = function(){ $('ukIn').value = last; choice = {}; run(); };
  run();
''',
        content=f'''
    <h2>What Is an American to British English Converter?</h2>
    <p>An American to British English converter changes US spellings in your text into UK spellings, such as color to colour, organize to organise and center to centre. This one also works the other way, from British to American.</p>
    <p>It is handy when you write for readers in the UK, India, Australia or other places that mostly follow British spelling. It also fixes a common problem with AI drafts: tools like ChatGPT often write in American spelling unless you ask otherwise, so a post for an Indian or UK audience ends up with a mix of both.</p>
    <p>Unlike a simple find and replace, the tool knows which words change only with meaning. Practice and practise, licence and license, program and programme are flagged for you to decide, instead of being changed blindly.</p>

    <h2>How to Use the Converter</h2>
    <ol>
      <li><strong>Paste your text</strong> into the first box. A sample is already there so you can see how it works.</li>
      <li><strong>Pick the direction:</strong> American to British, or British to American.</li>
      <li><strong>Pick a British style.</strong> Choose <code>ise</code> endings for standard UK and Indian English, or Oxford <code>ize</code> endings if you follow Oxford or many academic publishers.</li>
      <li><strong>Add names to leave alone,</strong> such as Pearl Harbor, World Trade Center or a brand name.</li>
      <li><strong>Review the list.</strong> Untick any change you do not want, and tick a yellow word if it should change in your text. Then copy the result.</li>
    </ol>

    <h2>Main Spelling Differences</h2>
    <div style="overflow-x:auto"><table class="lim">
      {th('Pattern', 'American', 'British')}
      <tbody>
        <tr><td>or and our</td><td>color, favorite, behavior</td><td>colour, favourite, behaviour</td></tr>
        <tr><td>ize and ise</td><td>organize, realize, optimization</td><td>organise, realise, optimisation (Oxford keeps <code>ize</code>)</td></tr>
        <tr><td>yze and yse</td><td>analyze, paralyze</td><td>analyse, paralyse (Oxford too)</td></tr>
        <tr><td>er and re</td><td>center, theater, fiber</td><td>centre, theatre, fibre</td></tr>
        <tr><td>se and ce</td><td>defense, offense</td><td>defence, offence</td></tr>
        <tr><td>Single and double L</td><td>traveled, canceled, jewelry, fulfill</td><td>travelled, cancelled, jewellery, fulfil</td></tr>
        <tr><td>Other words</td><td>gray, catalog, aging, skeptical</td><td>grey, catalogue, ageing, sceptical</td></tr>
        <tr><td>Depends on meaning</td><td>practice, license, program, tire, curb</td><td>practise (verb), licence (noun), programme (not software), tyre (wheel), kerb (road)</td></tr>
      </tbody>
    </table></div>
    <p>Words that end in <code>ise</code> in both, such as advertise, advise, exercise and surprise, are never touched. Links, email addresses and text inside backticks are skipped too.</p>

    <h2>Practical Tips</h2>
    <ul>
      <li><strong>Pick one style per site.</strong> The mixed spelling check tells you when a page uses both, which looks careless to readers.</li>
      <li><strong>Tell the AI first.</strong> Ask for British English in your prompt, then run the draft through this tool to catch what slipped through.</li>
      <li><strong>Keep keywords natural.</strong> People in India and the UK often search with British spelling, so match how your readers type.</li>
      <li><strong>Running separate US and UK pages?</strong> Use <a href="https://developers.google.com/search/docs/specialty/international/localized-versions" {EXT}>hreflang tags as Google explains</a> so each reader gets the right version.</li>
    </ul>

    <h2>Write for Your Readers</h2>
    <p>Spelling is one part of writing that fits your audience. Learn the rest in <a href="{B}how-to-write-seo-friendly-blog/">how to write an SEO friendly blog</a> and <a href="{B}10-easy-tips-for-effective-content-writing/">10 easy tips for effective content writing</a>, and set up regional pages with <a href="{B}hreflang-tags-explained/">hreflang tags explained</a>. Then remove the ChatGPT tone from your draft with the <a href="{T}ai-words-checker/">AI words checker</a>.</p>
''',
        faqs=[
            ("How do I convert American English to British English?", "Paste your text into the converter and keep the direction on American to British. It changes spellings such as color, organize and center to colour, organise and centre, highlights every change, and flags words like practice and license that depend on meaning, so you can copy a clean British version."),
            ("Should I use ise or ize in British English?", "Both are correct. Most UK and Indian writers use ise, as in organise. Oxford spelling, used by Oxford University Press and many academic journals, keeps ize but still writes analyse and colour. Pick one and use it across your whole site."),
            ("Does Indian English use British or American spelling?", "Indian English mostly follows British spelling, such as colour, centre and programme, and schools and newspapers usually teach and use it. American spelling is common online and in AI tools, which is why Indian content often mixes both."),
            ("Does the tool change words like practice or program?", "Not by default. Their British spelling depends on meaning, so they are marked in yellow with a note. Tick the row if your text uses the meaning that changes, such as practise as a verb or programme for a TV show."),
        ],
        related=[("How to Write an SEO Friendly Blog", "how-to-write-seo-friendly-blog"), ("Hreflang Tags Explained", "hreflang-tags-explained"),
                 ("10 Easy Tips for Effective Content Writing", "10-easy-tips-for-effective-content-writing"), ("25 Content Writing Mistakes", "25-content-writing-mistakes")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'content-writing-tools'; t['updated'] = '2026-11-18'
