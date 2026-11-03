"""Batch 6 (2026-11-03): Social Media Tools category, 7 tools.
Facts checked 2026-11-03 against: X developer docs "Counting characters" (280 weighted, URLs 23, emoji 2, CJK 2, NFC),
WhatsApp Help Center "How to use click to chat" (wa.me/<number>, international format without zeros, brackets or dashes,
?text= URL encoded, wa.me/?text= for message only), YouTube Help 9884579 (chapters: first 00:00, 3+ timestamps, ascending,
each 10s+), YouTube Help 57404 (title 100, description 5,000), Pinterest Help "Review Pin specs" (title 100, description 500),
Meta for Developers "Images in Link Shares" (1200x630 recommended, 600x315 for large display, 200x200 minimum, 1.91:1, 8 MB,
og:image:width/height), ogp.me (required og:title, og:type, og:image, og:url), Buffer character limits (Instagram 2,200,
LinkedIn 3,000, Threads 500, Bluesky 300), Instagram 5 hashtag cap (Social Samosa, Dec 2025), Buffer image size guide 2026."""
import html as _h

SM = 'https://brandella.in/tools/social-media-tools/'
B = 'https://brandella.in/'
TH = '<thead><tr style="background:#2b2b2b !important;">'
def th(*cols):
    return TH + ''.join(f'<th style="background:#2b2b2b !important; color:#ffffff !important;">{c}</th>' for c in cols) + '</tr></thead>'

def F(i, label, val='', em='', tag='input', opts=None, ph='', extra='', mono=False, typ='text'):
    lab = f'<label for="{i}">{label}' + (f' <em>{em}</em>' if em else '') + '</label>'
    cls = ' class="mono"' if mono else ''
    if tag == 'select':
        o = ''
        for x in opts:
            v, t = (x, x) if isinstance(x, str) else x
            o += f'<option value="{v}"' + (' selected' if v == val else '') + f'>{t}</option>'
        ctl = f'<select id="{i}">{o}</select>'
    elif tag == 'textarea':
        ctl = f'<textarea id="{i}"{cls} spellcheck="false" placeholder="{_h.escape(ph)}"{extra}>{_h.escape(val)}</textarea>'
    else:
        ctl = f'<input id="{i}"{cls} type="{typ}" autocomplete="off" spellcheck="false" value="{_h.escape(val)}" placeholder="{_h.escape(ph)}"{extra}>'
    return f'<div class="field">{lab}{ctl}</div>'

def R2(a, b): return f'<div class="row2">{a}{b}</div>'
def S(i, label): return f'<div class="stat-box"><b id="{i}">0</b><span>{label}</span></div>'
def CK(i, label, on=True): return f'<label class="check"><input id="{i}" type="checkbox"' + (' checked' if on else '') + f'> <span>{label}</span></label>'
PRE = 'style="display:block;margin-top:0;max-height:520px;overflow:auto;word-break:normal;overflow-wrap:anywhere"'
EXT = 'target="_blank" rel="noopener"'

BASEJS = r'''
  function v(id){ var e = $(id); return e ? String(e.value).trim() : ''; }
  function say(id, cls, h){ var e = $(id); e.className = 'kw-result' + (cls ? ' ' + cls : ''); e.innerHTML = h; }
  function issues(id, list, okMsg){
    var bad = list.filter(function(i){ return i[0] === 'bad'; }), warn = list.filter(function(i){ return i[0] === 'warn'; });
    var li = function(a){ return '<ul style="margin:6px 0 0 18px">' + a.map(function(i){ return '<li>' + i[1] + '</li>'; }).join('') + '</ul>'; };
    if (bad.length) say(id, 'bad', '<strong>Fix ' + bad.length + ' issue' + (bad.length > 1 ? 's' : '') + '.</strong>' + li(bad.concat(warn)));
    else if (warn.length) say(id, 'warn', '<strong>Works, with ' + warn.length + ' suggestion' + (warn.length > 1 ? 's' : '') + '.</strong>' + li(warn));
    else say(id, 'ok', okMsg);
  }
  function c(s){ return '<code>' + esc(s) + '</code>'; }
  function fmtN(n){ return Number(n).toLocaleString('en-IN'); }
'''

# ---------- shared grapheme and X weighting helpers ----------
COUNTJS = r'''
  var SEG = (window.Intl && Intl.Segmenter) ? new Intl.Segmenter('en', {granularity: 'grapheme'}) : null;
  function graphemes(s){ return SEG ? Array.from(SEG.segment(s), function(x){ return x.segment; }) : Array.from(s); }
  var PICT = /\p{Extended_Pictographic}/u, RIND = /[\u{1F1E6}-\u{1F1FF}]/u;
  function isEmoji(g){ return /️|⃣/.test(g) || RIND.test(g) || (PICT.test(g) && g.codePointAt(0) > 0xFF); }
  function w1(cp){ return cp <= 0x10FF || (cp >= 0x2000 && cp <= 0x200D) || (cp >= 0x2010 && cp <= 0x201F) || (cp >= 0x2032 && cp <= 0x2037); }
  var TLD = 'com|net|org|in|co|io|ai|app|dev|me|info|biz|uk|us|ly|gg|xyz|blog|shop|store|online|site|tech|news|tv|edu|gov|ca|au|de|fr';
  var URLRE = new RegExp('(^|[^@\\w./])((?:https?:\\/\\/(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,24}|(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+(?:' + TLD + ')\\b)(?::\\d+)?(?:\\/[^\\s]*)?)', 'gi');
  function xWeight(t){
    t = String(t).normalize('NFC'); var urls = 0;
    t = t.replace(URLRE, function(m, pre, u){ var tail = (u.match(/[.,!?;:)\]'"]+$/) || [''])[0]; urls++; return pre + tail; });
    var n = urls * 23;
    graphemes(t).forEach(function(g){
      if (isEmoji(g)){ n += 2; return; }
      for (var ch of g) n += w1(ch.codePointAt(0)) ? 1 : 2;
    });
    return {len: n, urls: urls};
  }
'''


def add(TOOLS, STOP_JS):
    _n = len(TOOLS)

    # ---------- 1. SOCIAL MEDIA IMAGE RESIZER ----------
    presets = [
        ('Instagram', [('ig_portrait', 'Portrait post 4:5', 1080, 1350), ('ig_grid', 'Tall post for the 3:4 grid', 1080, 1440),
                       ('ig_square', 'Square post 1:1', 1080, 1080), ('ig_land', 'Landscape post 1.91:1', 1080, 566),
                       ('ig_story', 'Story or Reel cover 9:16', 1080, 1920), ('ig_profile', 'Profile photo', 320, 320)]),
        ('Facebook', [('fb_square', 'Feed post square', 1080, 1080), ('fb_portrait', 'Feed post portrait 4:5', 1080, 1350),
                      ('fb_link', 'Link share image 1.91:1', 1200, 630), ('fb_cover', 'Page or profile cover', 851, 315),
                      ('fb_group', 'Group cover', 1640, 856), ('fb_event', 'Event cover', 1920, 1005), ('fb_story', 'Story 9:16', 1080, 1920)]),
        ('LinkedIn', [('li_square', 'Post square', 1080, 1080), ('li_portrait', 'Post portrait 4:5', 1080, 1350),
                      ('li_link', 'Link share image', 1200, 627), ('li_banner', 'Personal profile banner', 1584, 396),
                      ('li_company', 'Company page cover', 1128, 191)]),
        ('X (Twitter)', [('x_land', 'Post image 16:9', 1600, 900), ('x_square', 'Post image square', 1080, 1080),
                         ('x_header', 'Profile header 3:1', 1500, 500)]),
        ('YouTube', [('yt_thumb', 'Video thumbnail 16:9', 1280, 720), ('yt_banner', 'Channel banner', 2560, 1440)]),
        ('Pinterest and TikTok', [('pin', 'Pinterest pin 2:3', 1000, 1500), ('tt_cover', 'TikTok video cover 9:16', 1080, 1920)]),
    ]
    popt, pjs = '', []
    for grp, items in presets:
        popt += f'<optgroup label="{grp}">' + ''.join(
            f'<option value="{k}"' + (' selected' if k == 'ig_portrait' else '') + f'>{t} ({w} x {h})</option>' for k, t, w, h in items) + '</optgroup>'
        pjs += [f"{k}:['{grp.split(' ')[0]} {t}',{w},{h}]" for k, t, w, h in items]
    popt += '<option value="custom">Custom size</option>'
    TOOLS.append(dict(
        slug='social-media-image-resizer', short='IR', name='Social Media Image Resizer',
        card='Resize and crop any photo to the exact size for Instagram, Facebook, LinkedIn, X, YouTube and Pinterest.',
        title='Social Media Image Resizer: Free Crop and Resize Tool',
        desc='Free social media image resizer. Crop and resize photos to exact sizes for Instagram, Facebook, LinkedIn, X, YouTube and Pinterest. Runs in your browser.',
        h1='Social Media Image Resizer',
        lead='Pick a platform size, drop in your photo and download a perfectly sized image. Choose what to keep in the crop, or fit the whole picture on a blurred or plain background. Your image never leaves your device.',
        tool='''<section class="tool" aria-label="Social media image resizer" id="irForm">
    <div class="card" style="min-width:0" id="irDrop">
      <h2>Your Image and Size</h2>
      <div class="field"><label for="irFile">Upload Image <em>JPG, PNG or WebP</em></label><input id="irFile" type="file" accept="image/*"></div>
      <p style="font-size:13.5px;color:#666;margin:-6px 0 12px">You can also drag a photo onto this box. A sample image is loaded so you can try it first.</p>
      <div class="field"><label for="irPreset">Size</label><select id="irPreset">''' + popt + '''</select></div>
      <div class="row2" id="irCustom" style="display:none">''' + F('irW', 'Width', '1200', em='px', typ='number') + F('irH', 'Height', '630', em='px', typ='number') + '''</div>
      ''' + F('irFit', 'Fit', 'cover', tag='select', opts=[('cover', 'Fill the frame and crop the edges'), ('blur', 'Fit whole image on a blurred background'), ('color', 'Fit whole image on a solid colour')]) + '''
      <div id="irFocus">
        <div class="field"><label for="irFx">Keep in Crop, Left to Right <em id="irFxv">50%</em></label><input id="irFx" type="range" min="0" max="100" value="50" style="width:100%"></div>
        <div class="field"><label for="irFy">Keep in Crop, Top to Bottom <em id="irFyv">50%</em></label><input id="irFy" type="range" min="0" max="100" value="50" style="width:100%"></div>
      </div>
      <div class="row2">''' + F('irFmt', 'Format', 'image/jpeg', tag='select', opts=[('image/jpeg', 'JPG'), ('image/png', 'PNG'), ('image/webp', 'WebP')]) + '''<div class="field"><label for="irBg">Background Colour</label><input id="irBg" type="color" value="#ffffff" style="width:100%;height:42px;border:1px solid #cfcfcf;border-radius:8px"></div></div>
      <div class="field" id="irQRow"><label for="irQ">Quality <em id="irQv">90</em></label><input id="irQ" type="range" min="50" max="100" value="90" style="width:100%"></div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Resized Image</h2>
      <div style="background:repeating-conic-gradient(#eee 0 25%,#fff 0 50%) 0 0/20px 20px;border:1px solid #ddd;border-radius:10px;padding:10px;text-align:center"><canvas id="irCanvas" style="display:block;margin:0 auto;max-width:100%;max-height:430px;width:auto;height:auto"></canvas></div>
      <div class="actions"><button class="btn dark" id="irDl">Download Image</button><span class="toast" id="toast">Saved!</span></div>
      <div class="stats" style="margin-top:16px">''' + S('irDim', 'Output Size') + S('irRatio', 'Aspect Ratio') + S('irKb', 'File Size') + '''</div>
      <div class="kw-result" id="irCheck"></div>
      <div class="tips"><strong>Good to know</strong><ul><li>Faces and text should sit near the middle, as apps crop previews differently</li><li>JPG at 80 to 90 quality keeps photos sharp and small</li><li>Use PNG for logos, screenshots and graphics with text</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var P = {''' + ','.join(pjs) + r'''};
  var cv = $('irCanvas'), ctx = cv.getContext('2d'), src = null, srcName = 'sample', blob = null, timer = null;
  function sample(){
    var s = document.createElement('canvas'); s.width = 2400; s.height = 1600; var x = s.getContext('2d'); x.scale(1.5, 1.5);
    var g = x.createLinearGradient(0, 0, 1600, 1067); g.addColorStop(0, '#1f5f0a'); g.addColorStop(1, '#b7e36b'); x.fillStyle = g; x.fillRect(0, 0, 1600, 1067);
    x.fillStyle = 'rgba(255,255,255,.18)'; [[300,250,180],[1250,820,260],[980,260,120]].forEach(function(p){ x.beginPath(); x.arc(p[0], p[1], p[2], 0, 7); x.fill(); });
    x.fillStyle = '#fff'; x.textAlign = 'center'; x.font = 'bold 120px sans-serif'; x.fillText('Sample Photo', 800, 560);
    x.font = '46px sans-serif'; x.fillText('Upload your own image to resize it', 800, 650); return s;
  }
  function clampPx(n){ n = Math.round(+n) || 0; return Math.max(16, Math.min(8000, n)); }
  function gcd(a, b){ return b ? gcd(b, a % b) : a; }
  function ratio(w, h){ var g = gcd(w, h), a = w / g, b = h / g; return (a <= 32 && b <= 32) ? a + ':' + b : (w / h).toFixed(2) + ':1'; }
  function size(){ var k = $('irPreset').value; return k === 'custom' ? [clampPx($('irW').value), clampPx($('irH').value), 'custom ' + clampPx($('irW').value) + 'x' + clampPx($('irH').value)] : [P[k][1], P[k][2], P[k][0]]; }
  function slug(s){ return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function draw(){
    if (!src) return;
    var s = size(), W = s[0], H = s[1], sw = src.width, sh = src.height, mode = $('irFit').value, fmt = $('irFmt').value, iss = [];
    cv.width = W; cv.height = H; ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    ctx.clearRect(0, 0, W, H);
    if (fmt === 'image/jpeg' || mode === 'color'){ ctx.fillStyle = $('irBg').value; ctx.fillRect(0, 0, W, H); }
    var cover = Math.max(W / sw, H / sh), fit = Math.min(W / sw, H / sh), scale;
    if (mode === 'cover'){
      var dw = sw * cover, dh = sh * cover;
      ctx.drawImage(src, (W - dw) * (+$('irFx').value / 100), (H - dh) * (+$('irFy').value / 100), dw, dh);
      scale = cover;
      var lost = Math.round((1 - (W * H) / (dw * dh)) * 100);
      if (lost >= 30) iss.push(['warn', 'About ' + lost + '% of your photo is cropped away. Move the sliders to keep the important part, or choose a fit option.']);
    } else {
      if (mode === 'blur'){
        ctx.save(); ctx.filter = 'blur(' + Math.round(Math.max(W, H) / 40) + 'px) brightness(0.85)';
        ctx.drawImage(src, (W - sw * cover) / 2 - 20, (H - sh * cover) / 2 - 20, sw * cover + 40, sh * cover + 40); ctx.restore();
      }
      ctx.drawImage(src, (W - sw * fit) / 2, (H - sh * fit) / 2, sw * fit, sh * fit);
      scale = fit;
    }
    if (scale > 1.05) iss.push(['warn', 'Your image is ' + sw + ' x ' + sh + ' px, smaller than this size, so it was enlarged ' + scale.toFixed(1) + ' times and may look soft. Start from a bigger photo if you can.']);
    if (src.width && srcName === 'sample') iss.push(['warn', 'This is the sample image. Upload your own photo above.']);
    $('irDim').textContent = W + ' x ' + H; $('irRatio').textContent = ratio(W, H);
    $('irFocus').style.display = mode === 'cover' ? '' : 'none';
    $('irQRow').style.display = fmt === 'image/png' ? 'none' : '';
    $('irFxv').textContent = $('irFx').value + '%'; $('irFyv').textContent = $('irFy').value + '%'; $('irQv').textContent = $('irQ').value;
    issues('irCheck', iss, '<strong>Ready to download.</strong> Your image is exactly ' + W + ' x ' + H + ' px for ' + esc(s[2]) + '.');
    clearTimeout(timer); $('irKb').textContent = '…';
    timer = setTimeout(function(){
      cv.toBlob(function(b){ blob = b; if (!b){ $('irKb').textContent = 'n/a'; return; }
        $('irKb').textContent = b.size > 1048576 ? (b.size / 1048576).toFixed(1) + ' MB' : Math.round(b.size / 1024) + ' KB';
        if (b.type !== fmt) say('irCheck', 'warn', 'This browser cannot save ' + esc(fmt.split('/')[1].toUpperCase()) + ' files, so the image will download as ' + esc(b.type.split('/')[1].toUpperCase()) + '.');
      }, fmt, +$('irQ').value / 100);
    }, 150);
  }
  function load(file){
    if (!file) return;
    if (!/^image\//.test(file.type)){ say('irCheck', 'bad', 'That file is not an image. Choose a JPG, PNG or WebP file.'); return; }
    var img = new Image(), url = URL.createObjectURL(file);
    img.onload = function(){ src = img; srcName = file.name.replace(/\.[^.]+$/, '') || 'image'; draw(); };
    img.onerror = function(){ say('irCheck', 'bad', 'Your browser could not open this image. HEIC photos from iPhones often fail, so export as JPG first and try again.'); };
    img.src = url;
  }
  $('irFile').addEventListener('change', function(){ load(this.files[0]); });
  var dz = $('irDrop');
  dz.addEventListener('dragover', function(e){ e.preventDefault(); dz.style.borderColor = '#4fa61d'; });
  dz.addEventListener('dragleave', function(){ dz.style.borderColor = ''; });
  dz.addEventListener('drop', function(e){ e.preventDefault(); dz.style.borderColor = ''; if (e.dataTransfer.files[0]) load(e.dataTransfer.files[0]); });
  $('irPreset').addEventListener('change', function(){ $('irCustom').style.display = this.value === 'custom' ? '' : 'none'; });
  $('irForm').addEventListener('input', function(e){ if (e.target.id !== 'irFile') draw(); });
  $('irForm').addEventListener('change', function(e){ if (e.target.id !== 'irFile') draw(); });
  $('irDl').onclick = function(){
    if (!blob) return;
    var s = size(), ext = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}[blob.type] || 'png';
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
    a.download = slug(srcName) + '-' + slug(s[2]) + '-' + s[0] + 'x' + s[1] + '.' + ext;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 4000);
    var t = $('toast'); t.classList.add('show'); setTimeout(function(){ t.classList.remove('show'); }, 1600);
  };
  src = sample(); draw();
''',
        content='''
    <h2>What Is a Social Media Image Resizer?</h2>
    <p>Every network shows images at its own shape and size. A photo that looks great as an Instagram portrait gets its head cut off as a LinkedIn banner, and a small image turns blurry when an app stretches it. This resizer turns any photo into the exact pixel size each platform expects, so you control the crop instead of the app.</p>
    <p>Everything happens inside your browser using the built in canvas feature. Your photo is not uploaded to any server, which makes it safe for client work and unreleased product shots.</p>

    <h2>How to Use the Image Resizer</h2>
    <ol>
      <li><strong>Upload or drag in a photo.</strong> JPG, PNG and WebP all work.</li>
      <li><strong>Choose a size</strong> from the list, grouped by platform, or pick Custom size for any width and height.</li>
      <li><strong>Pick how it should fit.</strong> Fill crops the edges for a full bleed look. The two fit options keep the whole picture and fill the gaps with a blurred copy or a solid colour.</li>
      <li><strong>Move the sliders</strong> to keep faces, products or text inside the crop.</li>
      <li><strong>Download</strong> as JPG, PNG or WebP.</li>
    </ol>

    <h2>Popular Social Media Image Sizes</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Placement', 'Size in pixels', 'Shape') + '''
      <tbody>
        <tr><td>Instagram portrait post</td><td>1080 x 1350</td><td>4:5</td></tr>
        <tr><td>Instagram tall post for the grid</td><td>1080 x 1440</td><td>3:4</td></tr>
        <tr><td>Instagram, Facebook and TikTok stories or reels</td><td>1080 x 1920</td><td>9:16</td></tr>
        <tr><td>Facebook link share image</td><td>1200 x 630</td><td>1.91:1</td></tr>
        <tr><td>LinkedIn personal banner</td><td>1584 x 396</td><td>4:1</td></tr>
        <tr><td>X profile header</td><td>1500 x 500</td><td>3:1</td></tr>
        <tr><td>YouTube thumbnail</td><td>1280 x 720</td><td>16:9</td></tr>
        <tr><td>Pinterest pin</td><td>1000 x 1500</td><td>2:3</td></tr>
      </tbody>
    </table></div>
    <p>For link previews, Meta recommends at least 1200 x 630 pixels in its guide to <a href="https://developers.facebook.com/docs/sharing/webmasters/images" ''' + EXT + '''>images in link shares</a>. Pinterest lists its accepted formats and ratios on its <a href="https://help.pinterest.com/en/article/review-pin-specs" ''' + EXT + '''>Pin specs page</a>.</p>

    <h2>Tips for Sharp, Well Cropped Images</h2>
    <ul>
      <li><strong>Start big.</strong> Shrinking a photo keeps it sharp, while enlarging one always softens it. The tool warns you when it has to enlarge.</li>
      <li><strong>Keep key details central.</strong> Profile photos show as circles and banners are covered by profile pictures on some screens.</li>
      <li><strong>Choose 4:5 for feed posts.</strong> Taller images take up more of the screen on phones than squares do.</li>
      <li><strong>Mind the file size.</strong> A JPG between 80 and 90 quality is usually a few hundred KB and looks the same as 100.</li>
    </ul>

    <h2>Make Your Visuals Work Harder</h2>
    <p>Plan what to post with our <a href="''' + B + '''instagram-marketing-guide-businesses/">Instagram marketing guide for businesses</a>, get more from each picture by learning to <a href="''' + B + '''repurpose-blog-content-maximum-reach/">repurpose content for more reach</a>, and keep website images light with <a href="''' + B + '''optimize-images-for-seo-without-losing-quality/">image optimization for SEO</a>. Sharing a link instead of a photo? Check how it will look with the <a href="''' + SM + '''open-graph-preview/">Open Graph preview</a>.</p>
''',
        faqs=[
            ("What is the best image size for Instagram posts?", "1080 x 1350 pixels in a 4:5 shape works best for feed posts because it fills more of the screen. The profile grid now shows posts in a taller 3:4 shape, so 1080 x 1440 keeps your grid neat too."),
            ("Will resizing make my photo blurry?", "Not when you make it smaller. If your photo is smaller than the size you choose, it has to be enlarged and can look soft. The tool tells you when that happens so you can use a larger original."),
            ("Can I resize without cropping my photo?", "Yes. Choose one of the fit options. The whole photo is kept and the empty space is filled with a blurred copy of the image or a solid colour you pick."),
            ("Are my images uploaded anywhere?", "No. The resizing happens inside your browser and the file is saved straight to your device. Nothing is sent to a server."),
        ],
        related=[("Instagram Marketing Guide for Businesses", "instagram-marketing-guide-businesses"), ("Optimize Images for SEO", "optimize-images-for-seo-without-losing-quality"),
                 ("WebP vs AVIF Image Format", "webp-vs-avif-image-format-seo"), ("Facebook Marketing in 2026", "facebook-marketing-2026-whats-working")],
    ))

    # ---------- 2. OPEN GRAPH PREVIEW ----------
    OG_SAMPLE = '''<title>Free Social Media Tools for Marketers | Example</title>
<meta name="description" content="Resize images, count characters and preview links before you post.">
<link rel="canonical" href="https://www.example.com/social-media-tools/">
<meta property="og:type" content="website">
<meta property="og:title" content="Free Social Media Tools for Marketers">
<meta property="og:description" content="Resize images, count characters and preview your links before you post. Free, fast and private.">
<meta property="og:url" content="https://www.example.com/social-media-tools/">
<meta property="og:site_name" content="Example">
<meta property="og:image" content="https://www.example.com/images/social-tools-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''
    TOOLS.append(dict(
        slug='open-graph-preview', short='OG', name='Open Graph Preview',
        card='Paste your page head and see how the link will look on Facebook, LinkedIn, X and WhatsApp, with a tag check.',
        title='Open Graph Preview: Check Link Previews and OG Tags',
        desc='Free Open Graph preview and checker. Paste your HTML to see link cards for Facebook, LinkedIn, X and WhatsApp, and fix missing or weak og tags.',
        h1='Open Graph Preview',
        lead='Paste the head of your page to see how its link will look when shared on Facebook, LinkedIn, X and WhatsApp. The checker flags missing tags, weak images and titles that will be cut off.',
        tool='''<style>
.ogp{border:1px solid #dadde1;border-radius:10px;overflow:hidden;background:#fff;margin-bottom:18px;font-family:Helvetica,Arial,sans-serif}
.ogp h3{font-size:13px;margin:0;padding:7px 10px;background:#f4f4f4;color:#555;border-bottom:1px solid #e5e5e5;font-family:inherit}
.ogp .im{width:100%;aspect-ratio:1.91/1;background:#e9ecef center/cover no-repeat;display:block;object-fit:cover}
.ogp .ph{width:100%;aspect-ratio:1.91/1;display:grid;place-items:center;background:linear-gradient(135deg,#1f5f0a,#b7e36b);color:#fff;font-weight:700;font-size:15px;text-align:center;padding:8px}
.ogp .tx{padding:10px 12px}
.ogp .dm{font-size:12px;color:#65676b;text-transform:uppercase;word-break:break-all}
.ogp .tt{font-size:16px;font-weight:700;color:#1c1e21;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:3px 0}
.ogp .ds{font-size:14px;color:#606770;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
.ogp.li .tt{font-size:14px}.ogp.li .dm{text-transform:none}
.ogp.x .wrapx{position:relative}.ogp.x .im,.ogp.x .ph{aspect-ratio:2/1}
.ogp.x .lab{position:absolute;left:10px;bottom:10px;background:rgba(0,0,0,.75);color:#fff;font-size:13px;padding:2px 8px;border-radius:4px;max-width:85%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ogp .row{display:flex;gap:10px;padding:10px;align-items:center;background:#e7fce3}
.ogp .row .im,.ogp .row .ph{width:84px;min-width:84px;aspect-ratio:1/1;border-radius:6px;font-size:11px}
.ogp .row .tx{padding:0;min-width:0}
</style>
<section class="tool" aria-label="Open Graph preview" id="ogForm">
    <div class="card" style="min-width:0">
      <h2>Your Page Tags</h2>
      ''' + F('ogHtml', 'Paste HTML', OG_SAMPLE, em='the head of your page, or the whole page', tag='textarea', mono=True, extra=' style="min-height:330px"') + '''
      <div class="field"><label for="ogImg">Preview Image <em>optional, from your device</em></label><input id="ogImg" type="file" accept="image/*"></div>
      ''' + CK('ogLoad', 'Load the og:image from its web address', on=False) + '''
      <p style="font-size:13px;color:#666;margin:8px 0 0">Tip: to get the code, open your page, view the page source and copy everything between the head tags.</p>
    </div>
    <div class="card" style="min-width:0">
      <h2>Link Previews</h2>
      <div class="kw-result" id="ogCheck"></div>
      <div id="ogPrev"></div>
      <p style="font-size:12.5px;color:#777;margin:-6px 0 14px">Previews are close approximations. Each app changes its design from time to time.</p>
      <div style="overflow-x:auto"><table class="rtable" id="ogTable" style="font-size:13.5px"></table></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var localImg = '', localDim = null;
  function host(u){ try { return new URL(u).hostname; } catch(e){ return ''; } }
  function absUrl(u){ return /^https?:\/\//i.test(u); }
  function run(){
    var raw = $('ogHtml').value, doc = new DOMParser().parseFromString(raw, 'text/html'), m = {}, nameOg = [], iss = [];
    doc.querySelectorAll('meta').forEach(function(t){
      var k = (t.getAttribute('property') || t.getAttribute('name') || '').trim().toLowerCase(), val = (t.getAttribute('content') || '').trim();
      if (!k) return;
      if (/^og:/.test(k) && !t.getAttribute('property')) nameOg.push(k);
      if (!(k in m)) m[k] = val;
    });
    var tEl = doc.querySelector('title'), canon = doc.querySelector('link[rel="canonical"]');
    var pageTitle = tEl ? tEl.textContent.trim() : '', canonical = canon ? (canon.getAttribute('href') || '') : '';
    var title = m['og:title'] || m['twitter:title'] || pageTitle, desc = m['og:description'] || m['twitter:description'] || m['description'] || '';
    var img = m['og:image'] || m['og:image:url'] || m['og:image:secure_url'] || m['twitter:image'] || '', url = m['og:url'] || canonical;
    var xt = m['twitter:title'] || title, xi = m['twitter:image'] || img, card = m['twitter:card'] || '';
    var dom = host(url) || host(img) || 'example.com';
    var iw = +m['og:image:width'] || 0, ih = +m['og:image:height'] || 0;
    if (!raw.trim()){ say('ogCheck', 'bad', 'Paste the HTML of your page to see the previews.'); $('ogPrev').innerHTML = ''; $('ogTable').innerHTML = ''; return; }
    if (!m['og:title']) iss.push([pageTitle ? 'warn' : 'bad', 'No ' + c('og:title') + '.' + (pageTitle ? ' Apps will fall back to your title tag, which often carries a brand suffix you may not want.' : ' Add one so shares have a headline.')]);
    else if (m['og:title'].length > 70) iss.push(['warn', 'Your ' + c('og:title') + ' is ' + m['og:title'].length + ' characters. Long titles are cut after about two lines, so put the key words first.']);
    if (!m['og:description']) iss.push(['warn', 'No ' + c('og:description') + '. Facebook and WhatsApp show a line of description under the title.']);
    else if (m['og:description'].length > 200) iss.push(['warn', 'Your description is ' + m['og:description'].length + ' characters. Most apps show only the first line or two.']);
    if (!img) iss.push(['bad', 'No ' + c('og:image') + '. Without it, links show as a small text card or with a random image from the page.']);
    else if (!absUrl(img)) iss.push(['bad', c('og:image') + ' must be a full address starting with ' + c('https://') + ', not a relative path.']);
    else if (/^http:/i.test(img)) iss.push(['warn', 'Serve your ' + c('og:image') + ' over https so every app can load it.']);
    if (img && (!iw || !ih)) iss.push(['warn', 'Add ' + c('og:image:width') + ' and ' + c('og:image:height') + '. Meta says this lets the image show on the very first share.']);
    var dw = localDim ? localDim[0] : iw, dh = localDim ? localDim[1] : ih, src = localDim ? 'Your uploaded image' : 'The declared image';
    if (dw && dh){
      if (dw < 200 || dh < 200) iss.push(['bad', src + ' is ' + dw + ' x ' + dh + ' px. Facebook needs at least 200 x 200.']);
      else if (dw < 600 || dh < 315) iss.push(['warn', src + ' is ' + dw + ' x ' + dh + ' px, so it shows as a small thumbnail. Use at least 1200 x 630 for a large card.']);
      var r = dw / dh; if (r < 1.7 || r > 2.1) iss.push(['warn', src + ' has a ' + r.toFixed(2) + ':1 shape. Cards are about 1.91:1, so the edges will be cropped.']);
    }
    if (!m['og:image:alt'] && img) iss.push(['warn', 'Add ' + c('og:image:alt') + ' to describe the image for screen reader users.']);
    if (!m['og:url']) iss.push(['warn', 'No ' + c('og:url') + '. Set it to the canonical address so likes and shares count on one URL.']);
    else if (!absUrl(m['og:url'])) iss.push(['bad', c('og:url') + ' must be a full address starting with ' + c('https://') + '.']);
    if (!m['og:type']) iss.push(['warn', 'No ' + c('og:type') + '. The Open Graph protocol lists it as required. Use ' + c('website') + ' or ' + c('article') + '.']);
    if (!card) iss.push(['warn', 'No ' + c('twitter:card') + '. Add ' + c('summary_large_image') + ' to get the large image card on X.']);
    if (nameOg.length) iss.push(['warn', c(nameOg[0]) + ' uses ' + c('name=') + '. The protocol uses ' + c('property=') + ', which every app reads.']);
    issues('ogCheck', iss, '<strong>Looks great.</strong> All the key Open Graph and X card tags are in place.');

    var useUrl = $('ogLoad').checked && absUrl(img);
    function pic(u, label){
      var s = localImg || (useUrl ? u : '');
      if (s) return '<img class="im" alt="Link preview image" src="' + esc(s) + '" onerror="this.outerHTML=\'<div class=ph>Image could not load</div>\'">';
      return '<div class="ph">' + (u ? 'og:image ' + (iw && ih ? iw + ' x ' + ih : '') : 'No image set') + '</div>';
    }
    var T = esc(title || dom), D = esc(desc), DM = esc(dom);
    var xCard = card === 'summary'
      ? '<div class="row" style="background:#fff">' + pic(xi) + '<div class="tx"><div class="dm" style="text-transform:none">' + DM + '</div><div class="tt">' + esc(xt || dom) + '</div><div class="ds">' + D + '</div></div></div>'
      : '<div class="wrapx">' + pic(xi) + '<span class="lab">' + esc(xt || dom) + '</span></div><div class="tx"><div class="dm" style="text-transform:none">From ' + DM + '</div></div>';
    $('ogPrev').innerHTML =
      '<div class="ogp fb"><h3>Facebook</h3>' + pic(img) + '<div class="tx" style="background:#f0f2f5"><div class="dm">' + DM + '</div><div class="tt">' + T + '</div><div class="ds">' + D + '</div></div></div>' +
      '<div class="ogp li"><h3>LinkedIn</h3>' + pic(img) + '<div class="tx"><div class="tt">' + T + '</div><div class="dm">' + DM + '</div></div></div>' +
      '<div class="ogp x"><h3>X (Twitter)</h3>' + xCard + '</div>' +
      '<div class="ogp wa"><h3>WhatsApp</h3><div class="row">' + pic(img) + '<div class="tx"><div class="tt" style="font-size:14px">' + T + '</div><div class="ds" style="font-size:13px">' + D + '</div><div class="dm" style="text-transform:none">' + DM + '</div></div></div></div>';
    var keys = Object.keys(m).filter(function(k){ return /^(og|twitter|article):/.test(k); });
    $('ogTable').innerHTML = '<thead><tr><th>Tag found</th><th>Value</th></tr></thead><tbody>' +
      (pageTitle ? '<tr><td><code>title</code></td><td>' + esc(pageTitle) + '</td></tr>' : '') +
      (keys.length ? keys.map(function(k){ return '<tr><td><code>' + esc(k) + '</code></td><td style="word-break:break-all">' + esc(m[k]) + '</td></tr>'; }).join('') : '<tr><td colspan="2">No Open Graph or X tags found.</td></tr>') + '</tbody>';
  }
  $('ogImg').addEventListener('change', function(){
    var f = this.files[0]; if (!f || !/^image\//.test(f.type)) return;
    var r = new FileReader();
    r.onload = function(){ var im = new Image(); im.onload = function(){ localImg = r.result; localDim = [im.naturalWidth, im.naturalHeight]; run(); }; im.src = r.result; };
    r.readAsDataURL(f);
  });
  $('ogHtml').addEventListener('input', run); $('ogLoad').addEventListener('change', run);
  run();
''',
        content='''
    <h2>What Is an Open Graph Preview?</h2>
    <p>When someone shares your page on Facebook, LinkedIn, WhatsApp or X, the app reads a few meta tags in your HTML to build the link card: a title, a short description and an image. These are Open Graph tags, defined by the <a href="https://ogp.me/" ''' + EXT + '''>Open Graph protocol</a>. If they are missing or wrong, your link shows up with a random picture, a cut off title or no image at all.</p>
    <p>This tool reads the tags straight from the HTML you paste, shows how each app is likely to display the link, and lists exactly what to fix. Nothing is fetched from your site, so it also works for pages that are not live yet.</p>

    <h2>How to Use the Open Graph Preview</h2>
    <ol>
      <li><strong>Copy your page source.</strong> Open the page, view its source and copy the head section, or paste the whole page.</li>
      <li><strong>Paste it into the box.</strong> The previews and the tag check update as you type.</li>
      <li><strong>Add the share image</strong> from your device to see it in each card and check its size and shape.</li>
      <li><strong>Work through the list</strong> of issues, update your tags, and paste again to confirm.</li>
    </ol>

    <h2>The Tags That Matter Most</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Tag', 'What it does', 'Advice') + '''
      <tbody>
        <tr><td><code>og:title</code></td><td>The headline on the card</td><td>Keep the key words in the first 60 characters</td></tr>
        <tr><td><code>og:description</code></td><td>One or two lines under the title</td><td>Write a clear benefit in about 100 to 150 characters</td></tr>
        <tr><td><code>og:image</code></td><td>The picture on the card</td><td>1200 x 630 px, full https address</td></tr>
        <tr><td><code>og:image:width</code> and <code>og:image:height</code></td><td>Tell apps the image size up front</td><td>Lets the image show on the first share</td></tr>
        <tr><td><code>og:url</code></td><td>The main address of the page</td><td>Match your canonical URL</td></tr>
        <tr><td><code>og:type</code></td><td>The kind of page</td><td><code>website</code> or <code>article</code></td></tr>
        <tr><td><code>twitter:card</code></td><td>Picks the card layout on X</td><td><code>summary_large_image</code> for a big picture</td></tr>
      </tbody>
    </table></div>
    <p>Meta explains its image rules, including the 1200 x 630 recommendation and the 8 MB limit, in its guide to <a href="https://developers.facebook.com/docs/sharing/webmasters/images" ''' + EXT + '''>images in link shares</a>.</p>

    <h2>Tips for Better Link Previews</h2>
    <ul>
      <li><strong>Design a share image for each key page.</strong> A clear headline on the image gets more clicks than a generic logo.</li>
      <li><strong>Keep text away from the edges.</strong> Some apps crop the card to 2:1 or show a square thumbnail.</li>
      <li><strong>Refresh the cache after changes.</strong> Apps store previews, so use the Facebook Sharing Debugger or LinkedIn Post Inspector to fetch the new version.</li>
      <li><strong>Use one image URL per version.</strong> If you change the picture, change its file name too, so old copies are not reused.</li>
    </ul>

    <h2>Get More From Every Share</h2>
    <p>Learn how tags fit together in <a href="''' + B + '''dynamic-meta-tags-php/">dynamic meta tags in PHP</a> and <a href="''' + B + '''what-is-canonical-tag/">what a canonical tag is</a>, then plan your posts with our <a href="''' + B + '''linkedin-marketing-strategy/">LinkedIn marketing strategy</a>. Need to write the tags from scratch? Use the <a href="https://brandella.in/tools/seo-tools/meta-tag-generator/">meta tag generator</a>, and size your share image with the <a href="''' + SM + '''social-media-image-resizer/">social media image resizer</a>.</p>
''',
        faqs=[
            ("What size should an Open Graph image be?", "Use 1200 x 630 pixels, a 1.91:1 shape. Meta recommends at least that size for sharp cards, needs at least 600 x 315 for the large layout, and rejects images smaller than 200 x 200 pixels."),
            ("Why is my old image still showing after I changed it?", "Facebook, LinkedIn and other apps cache link previews. Run the page through the Facebook Sharing Debugger or LinkedIn Post Inspector to fetch it again, and give the new image a new file name."),
            ("Does X use Open Graph tags?", "Yes. X reads its own twitter tags first and falls back to Open Graph for the title, description and image. You still need twitter:card set to summary_large_image for the big image layout."),
            ("Does this tool visit my website?", "No. It only reads the HTML you paste. The share image is loaded from its web address only if you tick that option, and an image you pick from your device stays on your device."),
        ],
        related=[("Dynamic Meta Tags in PHP", "dynamic-meta-tags-php"), ("What Is a Canonical Tag", "what-is-canonical-tag"),
                 ("LinkedIn Marketing Strategy", "linkedin-marketing-strategy"), ("Facebook Marketing in 2026", "facebook-marketing-2026-whats-working")],
    ))

    # ---------- 3. SOCIAL MEDIA CHARACTER COUNTER ----------
    CC_SAMPLE = ('Our free social media tools are live! \U0001F680\n\n'
                 'Resize images, preview links and count characters for every network, right in your browser.\n\n'
                 'Try them here: brandella.in/tools/social-media-tools/\n\n'
                 '#SocialMedia #MarketingTips #FreeTools #ContentCreator #SmallBusiness #DigitalMarketing')
    TOOLS.append(dict(
        slug='social-media-character-counter', short='CH', name='Social Media Character Counter',
        card='Count characters for X, Instagram, LinkedIn, Threads, TikTok, YouTube and more, the way each app counts.',
        title='Social Media Character Counter for X, Instagram and More',
        desc='Free social media character counter. Check posts against limits for X, Instagram, LinkedIn, Threads, Bluesky, TikTok, YouTube and Pinterest as you type.',
        h1='Social Media Character Counter',
        lead='Write or paste your post to see how many characters you have left on every major network. X posts are counted the way X counts them, with links as 23 and emoji as 2, and hashtags are checked against the new Instagram limit.',
        tool='''<section class="tool" aria-label="Social media character counter" id="ccForm">
    <div class="card" style="min-width:0">
      <h2>Your Post</h2>
      ''' + F('ccText', 'Post Text', CC_SAMPLE, tag='textarea', extra=' style="min-height:260px"') + '''
      <div class="stats">''' + S('ccChars', 'Characters') + S('ccWords', 'Words') + S('ccX', 'X Count') + S('ccTags', 'Hashtags') + S('ccEmo', 'Emoji') + S('ccLines', 'Lines') + '''</div>
      <div class="actions" style="margin-top:0"><button class="btn dark" id="ccCopy">Copy Text</button><button class="btn" id="ccClear">Clear</button><span class="toast" id="toast">Copied!</span></div>
      <h2 style="margin-top:22px">Instagram Feed Preview</h2>
      <div id="ccIg" style="border:1px solid #e5e5e5;border-radius:10px;padding:12px 14px;font:14px/1.5 Helvetica,Arial,sans-serif;white-space:pre-wrap;word-break:break-word;color:#111"></div>
      <p style="font-size:12.5px;color:#777;margin:6px 0 0">Instagram shows roughly the first 125 characters before the more link. Put your hook there.</p>
    </div>
    <div class="card" style="min-width:0">
      <h2>Limits by Platform</h2>
      <div class="kw-result" id="ccCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="ccTable"></table></div>
      <div class="chips" id="ccChips" style="margin-top:14px"></div>
    </div>
  </section>''',
        js=BASEJS + COUNTJS + r'''
  var L = [
    ['X post (free account)', 280, 'x'], ['Bluesky post', 300], ['Threads post', 500], ['Pinterest pin title', 100], ['Pinterest pin description', 500],
    ['YouTube video title', 100], ['Instagram caption', 2200], ['LinkedIn post', 3000], ['TikTok caption', 4000], ['YouTube description', 5000]
  ];
  function run(){
    var t = $('ccText').value, g = graphemes(t), n = g.length, iss = [];
    var words = (t.match(/[\p{L}\p{N}][\p{L}\p{N}'’_]*/gu) || []).length;
    var tags = t.match(/(^|[^\p{L}\p{N}_&])#([\p{L}\p{N}_]*\p{L}[\p{L}\p{N}_]*)/gu) || [];
    tags = tags.map(function(s){ return s.replace(/^[^#]*/, ''); });
    var ments = (t.match(/(^|[^\w@])@\w{1,30}/g) || []).length;
    var emo = g.filter(isEmoji).length, xw = xWeight(t);
    $('ccChars').textContent = fmtN(n); $('ccWords').textContent = fmtN(words); $('ccX').textContent = fmtN(xw.len);
    $('ccTags').textContent = tags.length; $('ccEmo').textContent = emo; $('ccLines').textContent = t ? t.split('\n').length : 0;
    $('ccTable').innerHTML = '<thead><tr><th>Platform</th><th class="num">Limit</th><th class="num">Used</th><th>Status</th></tr></thead><tbody>' + L.map(function(p){
      var used = p[2] === 'x' ? xw.len : n, left = p[1] - used;
      return '<tr' + (left < 0 ? ' style="background:#fdecea"' : '') + '><td>' + p[0] + '</td><td class="num">' + fmtN(p[1]) + '</td><td class="num">' + fmtN(used) + '</td><td>' + (left < 0 ? '<strong style="color:#c0392b">Over by ' + fmtN(-left) + '</strong>' : fmtN(left) + ' left') + '</td></tr>';
    }).join('') + '</tbody>';
    var low = {}, dup = [];
    tags.forEach(function(h){ var k = h.toLowerCase(); if (low[k]) dup.push(h); low[k] = (low[k] || 0) + 1; });
    $('ccChips').innerHTML = tags.length ? Object.keys(low).map(function(k){ return '<span class="chip">' + esc(k) + (low[k] > 1 ? ' x' + low[k] : '') + '</span>'; }).join('') : '';
    if (!t.trim()){ say('ccCheck', '', 'Start typing to see your counts.'); $('ccIg').textContent = ''; return; }
    if (xw.len > 280) iss.push(['warn', 'Too long for a standard X post by ' + (xw.len - 280) + '. Premium accounts can post longer, but only about the first 280 show before Show more.']);
    if (n > 500) iss.push(['warn', 'Too long for Threads, which allows 500 characters per post. Split it into a thread.']);
    if (tags.length > 5) iss.push(['warn', 'You have ' + tags.length + ' hashtags. Instagram now allows up to 5 per post or reel, so pick your 5 most relevant.']);
    if (dup.length) iss.push(['warn', 'Repeated hashtag: ' + c(dup[0]) + '.']);
    if (xw.urls) iss.push(['ok', '']);
    issues('ccCheck', iss.filter(function(i){ return i[0] !== 'ok'; }), '<strong>Fits everywhere you see a green status.</strong> ' + (xw.urls ? 'Links count as 23 characters on X, however long they are.' : 'Emoji count as 2 characters on X.'));
    var cut = '', k = 0;
    for (var i = 0; i < g.length && k < 125; i++){ cut += g[i]; k++; }
    $('ccIg').innerHTML = '<strong>yourbrand</strong> ' + esc(cut.replace(/\n{2,}/g, '\n')) + (g.length > 125 ? '<span style="color:#8e8e8e">… more</span>' : '');
  }
  $('ccText').addEventListener('input', run);
  $('ccCopy').onclick = function(){ copyText($('ccText').value, 'toast'); };
  $('ccClear').onclick = function(){ $('ccText').value = ''; run(); $('ccText').focus(); };
  run();
''',
        content='''
    <h2>What Is a Social Media Character Counter?</h2>
    <p>Each network caps how long a post can be, and the caps are very different: 280 on X, 500 on Threads, 2,200 on Instagram and 3,000 on LinkedIn. A post that fits one app gets cut off or rejected on another. This counter checks your text against all the major limits at once, so you can write one post and adapt it with confidence.</p>
    <p>X does not count every character the same way. Its <a href="https://docs.x.com/fundamentals/counting-characters" ''' + EXT + '''>counting rules</a> treat any link as 23 characters and every emoji as 2, and count Chinese, Japanese and Korean characters as 2. The X Count box applies those rules, which is why it can differ from the plain character count.</p>

    <h2>How to Use the Character Counter</h2>
    <ol>
      <li><strong>Type or paste your post</strong> into the box. Counts update as you type.</li>
      <li><strong>Check the table</strong> for every platform you plan to post on. Rows turn red when you go over.</li>
      <li><strong>Read the suggestions</strong> for hashtags, repeated tags and X length.</li>
      <li><strong>Look at the Instagram preview</strong> to see what people read before they tap more.</li>
      <li><strong>Copy your text</strong> and post it.</li>
    </ol>

    <h2>Character Limits by Platform</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Platform', 'Limit', 'Notes') + '''
      <tbody>
        <tr><td>X post</td><td>280</td><td>Weighted count. Premium accounts can post more.</td></tr>
        <tr><td>Bluesky post</td><td>300</td><td>Links are shortened in the post</td></tr>
        <tr><td>Threads post</td><td>500</td><td>Longer ideas can run as a thread</td></tr>
        <tr><td>Instagram caption</td><td>2,200</td><td>Up to 5 hashtags. About 125 characters show before more.</td></tr>
        <tr><td>LinkedIn post</td><td>3,000</td><td>Only the first lines show before see more</td></tr>
        <tr><td>TikTok caption</td><td>4,000</td><td>Some scheduling tools allow less</td></tr>
        <tr><td>YouTube title and description</td><td>100 and 5,000</td><td>From <a href="https://support.google.com/youtube/answer/57404" ''' + EXT + '''>YouTube Help</a></td></tr>
        <tr><td>Pinterest pin title and description</td><td>100 and 500</td><td>Descriptions are not shown in the home feed</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Posts That Fit and Perform</h2>
    <ul>
      <li><strong>Lead with the hook.</strong> On Instagram and LinkedIn, most readers only see the first line or two before deciding to expand.</li>
      <li><strong>Use fewer, sharper hashtags.</strong> Instagram now caps posts at 5 hashtags, so choose specific ones over generic tags like #reels.</li>
      <li><strong>Count links on X.</strong> A short link and a long one both cost 23 characters, so there is no need to shorten links just to save space.</li>
      <li><strong>Leave room for replies and quotes.</strong> A post a little under the limit is easier for others to quote with their own comment.</li>
    </ul>

    <h2>Write Better Social Posts</h2>
    <p>Plan what to say with our <a href="''' + B + '''content-calendar-planning/">content calendar planning guide</a>, learn what to measure in <a href="''' + B + '''social-media-kpis-every-marketer-should-track/">social media KPIs every marketer should track</a>, and grow on short video with our <a href="''' + B + '''tiktok-marketing-strategy/">TikTok marketing strategy</a>. Want a few words to stand out? Style them with the <a href="''' + SM + '''bold-text-generator/">bold text generator</a>.</p>
''',
        faqs=[
            ("How are characters counted on X?", "X uses a weighted count with a limit of 280. Most letters, numbers and punctuation count as 1, emoji and Chinese, Japanese or Korean characters count as 2, and every link counts as 23 no matter how long it is."),
            ("How many hashtags can I use on Instagram?", "Instagram now allows up to 5 hashtags in a post or reel caption, down from the old limit of 30. The change rolled out gradually from late 2025 to cut down on spammy generic tags."),
            ("Why does my count differ from another tool?", "Emoji are the usual reason. Some tools count the hidden parts of an emoji separately. This counter treats each emoji you see as one character, and applies X's own rules for the X count."),
            ("Is my text saved anywhere?", "No. The counter runs entirely in your browser and nothing you type is uploaded or stored."),
        ],
        related=[("Social Media KPIs to Track", "social-media-kpis-every-marketer-should-track"), ("Content Calendar Planning", "content-calendar-planning"),
                 ("TikTok Marketing Strategy", "tiktok-marketing-strategy"), ("Instagram Marketing Guide", "instagram-marketing-guide-businesses")],
    ))

    # ---------- 4. BOLD TEXT GENERATOR ----------
    BT_SAMPLE = ('**3 lessons from 10 years in marketing**\n\n'
                 '1. *Consistency beats intensity.*\n'
                 '2. Your audience cares about **their** problems.\n'
                 '3. Measure what matters, then repeat it.\n\n'
                 'Which one do you agree with most?')
    TOOLS.append(dict(
        slug='bold-text-generator', short='BT', name='Bold Text Generator',
        card='Make bold, italic and other styled text you can paste into LinkedIn, Instagram, X and Facebook posts.',
        title='Bold Text Generator for LinkedIn, Instagram and X',
        desc='Free bold text generator. Turn plain words into bold, italic, script and monospace text you can copy into LinkedIn, Instagram, X and Facebook posts.',
        h1='Bold Text Generator',
        lead='Social apps do not have a bold button, but you can still make words stand out. Wrap words in double stars for bold and single stars for italic, then copy the formatted post, or copy any style from the list below.',
        tool='''<section class="tool" aria-label="Bold text generator" id="btForm">
    <div class="card" style="min-width:0">
      <h2>Your Text</h2>
      ''' + F('btText', 'Text', BT_SAMPLE, em='use **bold** and *italic*', tag='textarea', extra=' style="min-height:220px"') + '''
      ''' + F('btFont', 'Font for Bold and Italic', 'sans', tag='select', opts=[('sans', 'Sans serif (matches LinkedIn and Instagram)'), ('serif', 'Serif (classic look)')]) + '''
      <div class="actions" style="margin-top:0"><button class="btn" id="btPlain">Remove All Styling</button></div>
      <div class="stats" style="margin-top:16px">''' + S('btN', 'Styled Letters') + S('btX', 'X Count') + S('btLen', 'Characters') + '''</div>
    </div>
    <div class="card" style="min-width:0">
      <h2>Formatted Post</h2>
      <div id="btOut" style="border:1px solid #e5e5e5;border-radius:10px;padding:12px 14px;white-space:pre-wrap;word-break:break-word;font-size:15px;line-height:1.55;min-height:80px"></div>
      <div class="actions"><button class="btn dark" id="btCopy">Copy Formatted Post</button><span class="toast" id="toast">Copied!</span></div>
      <div class="kw-result" id="btCheck" style="margin-top:16px"></div>
      <h2 style="margin-top:6px">Every Style</h2>
      <div id="btList"></div>
    </div>
  </section>''',
        js=BASEJS + COUNTJS + r'''
  var ST = [
    ['Bold', 0x1D400, 0x1D41A, 0x1D7CE, {}], ['Italic', 0x1D434, 0x1D44E, 0, {h: 0x210E}], ['Bold Italic', 0x1D468, 0x1D482, 0, {}],
    ['Sans Bold', 0x1D5D4, 0x1D5EE, 0x1D7EC, {}], ['Sans Italic', 0x1D608, 0x1D622, 0, {}], ['Sans Bold Italic', 0x1D63C, 0x1D656, 0, {}],
    ['Script Bold', 0x1D4D0, 0x1D4EA, 0, {}], ['Gothic Bold', 0x1D56C, 0x1D586, 0, {}],
    ['Double Struck', 0x1D538, 0x1D552, 0x1D7D8, {C: 0x2102, H: 0x210D, N: 0x2115, P: 0x2119, Q: 0x211A, R: 0x211D, Z: 0x2124}],
    ['Monospace', 0x1D670, 0x1D68A, 0x1D7F6, {}]
  ];
  var BY = {}; ST.forEach(function(s){ BY[s[0]] = s; });
  function sty(t, s){
    var o = '';
    for (var ch of t){
      var cp = ch.codePointAt(0);
      if (s[4][ch]) o += String.fromCodePoint(s[4][ch]);
      else if (cp >= 65 && cp <= 90) o += String.fromCodePoint(s[1] + cp - 65);
      else if (cp >= 97 && cp <= 122) o += String.fromCodePoint(s[2] + cp - 97);
      else if (cp >= 48 && cp <= 57 && s[3]) o += String.fromCodePoint(s[3] + cp - 48);
      else o += ch;
    }
    return o;
  }
  function comb(t, mk){ var o = ''; for (var ch of t){ o += ch; if (!/\s/.test(ch)) o += mk; } return o; }
  function plain(t){ return String(t).normalize('NFKC').replace(/[̶̲]/g, ''); }
  function styled(t){ var n = 0; for (var ch of t){ var cp = ch.codePointAt(0); if ((cp >= 0x1D400 && cp <= 0x1D7FF) || [0x210E,0x2102,0x210D,0x2115,0x2119,0x211A,0x211D,0x2124].indexOf(cp) > -1) n++; } return n; }
  function format(t){
    var sans = $('btFont').value === 'sans';
    var b = BY[sans ? 'Sans Bold' : 'Bold'], i = BY[sans ? 'Sans Italic' : 'Italic'], bi = BY[sans ? 'Sans Bold Italic' : 'Bold Italic'];
    t = t.replace(/\*\*\*([^*\n]+?)\*\*\*/g, function(m, x){ return sty(x, bi); });
    t = t.replace(/\*\*([^\n]+?)\*\*/g, function(m, x){ return sty(x.replace(/\*([^*\n]+?)\*/g, function(m2, y){ return sty(y, bi); }), b); });
    t = t.replace(/(^|[^*\w])\*([^*\n]+?)\*(?!\w)/g, function(m, p, x){ return p + sty(x, i); });
    return t;
  }
  var out = '', items = [];
  function run(){
    var t = $('btText').value, iss = [];
    out = format(t);
    var base = t.replace(/\*+/g, '');
    $('btOut').textContent = out || 'Your formatted post appears here.';
    var n = styled(out), xw = xWeight(out).len;
    $('btN').textContent = n; $('btX').textContent = fmtN(xw); $('btLen').textContent = fmtN(graphemes(out).length);
    var short = Array.from(base.split('\n').filter(function(l){ return l.trim(); })[0] || 'Your text').slice(0, 60).join('');
    items = ST.map(function(s){ return [s[0], sty(short, s)]; }).concat([['Underline', comb(short, '̲')], ['Strikethrough', comb(short, '̶')]]);
    $('btList').innerHTML = items.map(function(it, k){
      return '<div class="slug-row"><div style="min-width:0"><small style="margin:0 0 2px">' + it[0] + '</small><div style="font-size:16px;word-break:break-word">' + esc(it[1]) + '</div></div><button class="btn btn-sm" data-k="' + k + '">Copy</button></div>';
    }).join('');
    if (/[À-ÿĀ-ž]/.test(base)) iss.push(['warn', 'Accented letters such as é have no styled version, so they stay plain.']);
    if (n > 60) iss.push(['warn', n + ' letters are styled. Screen readers can read styled letters one by one or skip them, so keep styling to a few key words.']);
    if (xw > 280) iss.push(['warn', 'This post counts as ' + xw + ' on X, over the 280 limit. Styled letters count as 2 each there.']);
    issues('btCheck', iss, '<strong>Ready to paste.</strong> Styled letters are special Unicode characters, so they work anywhere you can type text.');
  }
  $('btList').addEventListener('click', function(e){ var b = e.target.closest('button'); if (b) copyText(items[+b.getAttribute('data-k')][1], 'toast'); });
  $('btText').addEventListener('input', run); $('btFont').addEventListener('change', run);
  $('btCopy').onclick = function(){ if (out) copyText(out, 'toast'); };
  $('btPlain').onclick = function(){ $('btText').value = plain($('btText').value).replace(/\*+/g, ''); run(); };
  run();
''',
        content='''
    <h2>What Is a Bold Text Generator?</h2>
    <p>LinkedIn, Instagram, X and Facebook posts are plain text, with no bold or italic button. A bold text generator gets around this by swapping normal letters for look alike characters from the Unicode <em>Mathematical Alphanumeric Symbols</em> block. They look bold or italic, and because they are real characters, they stay styled wherever you paste them.</p>
    <p>This tool works like a mini editor. Write your post as usual, wrap words in double stars for bold or single stars for italic, and copy the finished post in one click.</p>

    <h2>How to Use the Bold Text Generator</h2>
    <ol>
      <li><strong>Type or paste your post.</strong> Line breaks are kept.</li>
      <li><strong>Mark words to style.</strong> Use <code>**words**</code> for bold, <code>*words*</code> for italic and <code>***words***</code> for bold italic.</li>
      <li><strong>Pick a font.</strong> Sans serif blends in with most apps. Serif looks more formal.</li>
      <li><strong>Copy the formatted post</strong>, or copy a single style from the list for a headline or bio.</li>
      <li><strong>Changed your mind?</strong> Paste styled text and press Remove All Styling to get plain letters back.</li>
    </ol>

    <h2>Text Styles You Can Use</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Style', 'Works for', 'Best use') + '''
      <tbody>
        <tr><td>Bold and Sans Bold</td><td>Letters and numbers</td><td>Headlines, key phrases, hooks</td></tr>
        <tr><td>Italic and Sans Italic</td><td>Letters only</td><td>Quotes, emphasis, titles</td></tr>
        <tr><td>Bold Italic</td><td>Letters only</td><td>Strong emphasis</td></tr>
        <tr><td>Script Bold and Gothic Bold</td><td>Letters only</td><td>Bios and decorative names</td></tr>
        <tr><td>Double Struck and Monospace</td><td>Letters and numbers</td><td>Stats, codes, playful accents</td></tr>
        <tr><td>Underline and Strikethrough</td><td>Any character</td><td>Price drops, corrections</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Using Styled Text Well</h2>
    <ul>
      <li><strong>Style a few words, not whole posts.</strong> Screen readers may read styled letters one at a time or skip them, which shuts out some of your audience.</li>
      <li><strong>Never style hashtags or names you want found.</strong> Search treats styled letters as different characters, so a styled hashtag will not match.</li>
      <li><strong>Watch your X count.</strong> X counts each styled letter as 2 characters under its <a href="https://docs.x.com/fundamentals/counting-characters" ''' + EXT + '''>counting rules</a>.</li>
      <li><strong>Keep accents plain.</strong> Letters like é have no styled version, so mixed words can look uneven.</li>
    </ul>

    <h2>Write Posts People Stop For</h2>
    <p>Put your formatting to work with our <a href="''' + B + '''linkedin-marketing-strategy/">LinkedIn marketing strategy</a>, learn how to <a href="''' + B + '''grow-your-linkedin-company-page/">grow your LinkedIn company page</a>, and avoid common slips in <a href="''' + B + '''25-content-writing-mistakes/">25 content writing mistakes</a>. Before you post, check the length with the <a href="''' + SM + '''social-media-character-counter/">social media character counter</a>.</p>
''',
        faqs=[
            ("How do I write in bold on LinkedIn?", "LinkedIn posts have no bold button. Write your post here, put double stars around the words you want in bold, copy the formatted post and paste it into LinkedIn. The bold letters are Unicode characters, so they stay bold."),
            ("Does bold text work on Instagram, X and Facebook?", "Yes. The styled letters are standard Unicode characters that work in captions, bios, comments and posts on all major apps. A few very old phones may show empty boxes instead."),
            ("Is styled text bad for accessibility?", "It can be. Screen readers may spell out styled letters one by one or skip them entirely. Use styling for a few words of emphasis rather than whole sentences, and never for hashtags."),
            ("Is my text saved?", "No. Everything happens in your browser and nothing you type is uploaded or stored."),
        ],
        related=[("LinkedIn Marketing Strategy", "linkedin-marketing-strategy"), ("Grow Your LinkedIn Company Page", "grow-your-linkedin-company-page"),
                 ("25 Content Writing Mistakes", "25-content-writing-mistakes"), ("Instagram Marketing Guide", "instagram-marketing-guide-businesses")],
    ))

    # ---------- 5. WHATSAPP LINK GENERATOR ----------
    cc = [('91', 'India +91'), ('1', 'USA and Canada +1'), ('44', 'United Kingdom +44'), ('971', 'UAE +971'), ('966', 'Saudi Arabia +966'),
          ('974', 'Qatar +974'), ('965', 'Kuwait +965'), ('968', 'Oman +968'), ('973', 'Bahrain +973'), ('65', 'Singapore +65'),
          ('60', 'Malaysia +60'), ('61', 'Australia +61'), ('64', 'New Zealand +64'), ('977', 'Nepal +977'), ('880', 'Bangladesh +880'),
          ('94', 'Sri Lanka +94'), ('92', 'Pakistan +92'), ('62', 'Indonesia +62'), ('63', 'Philippines +63'), ('27', 'South Africa +27'),
          ('234', 'Nigeria +234'), ('254', 'Kenya +254'), ('49', 'Germany +49'), ('33', 'France +33'), ('39', 'Italy +39'), ('34', 'Spain +34'),
          ('31', 'Netherlands +31'), ('55', 'Brazil +55'), ('52', 'Mexico +52'), ('', 'Other: type the full number with +')]
    TOOLS.append(dict(
        slug='whatsapp-link-generator', short='WA', name='WhatsApp Link Generator',
        card='Create a wa.me click to chat link with a ready typed message for your website, bio, ads or QR codes.',
        title='WhatsApp Link Generator: Free wa.me Click to Chat Link',
        desc='Free WhatsApp link generator. Create a wa.me click to chat link with a pre filled message for your website, Instagram bio, ads and emails in seconds.',
        h1='WhatsApp Link Generator',
        lead='Turn your WhatsApp number into a link that opens a chat with you, with your message already typed. Use it on your website, Instagram bio, Google Business Profile, ads and emails.',
        tool='''<section class="tool" aria-label="WhatsApp link generator" id="waForm">
    <div class="card" style="min-width:0">
      <h2>Your Details</h2>
      <div class="tabs" id="waMode" style="margin-bottom:14px"><button type="button" class="btn btn-sm dark" data-m="chat">Chat with my number</button> <button type="button" class="btn btn-sm" data-m="share">Share a message only</button></div>
      <div id="waNumRow">
        ''' + R2(F('waCc', 'Country Code', '91', tag='select', opts=cc), F('waNum', 'WhatsApp Number', '98765 43210', ph='98765 43210', typ='tel')) + '''
      </div>
      ''' + F('waMsg', 'Pre Filled Message', 'Hi! I found you on your website and would like to know more about your services.', em='optional', tag='textarea', extra=' style="min-height:120px"') + '''
      ''' + F('waLabel', 'Button Text', 'Chat with us on WhatsApp', em='for the HTML button') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your WhatsApp Link</h2>
      <pre class="code-out" id="waOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="waCopy">Copy Link</button><a class="btn" id="waOpen" href="#" target="_blank" rel="noopener">Test Link</a><span class="toast" id="toast">Copied!</span></div>
      <div class="stats" style="margin-top:16px">''' + S('waDigits', 'Number Digits') + S('waChars', 'Message Length') + S('waLen', 'Link Length') + '''</div>
      <div class="kw-result" id="waCheck"></div>
      <h2>HTML Button Code</h2>
      <pre class="code-out" id="waHtml" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn" id="waCopyHtml">Copy HTML</button></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  var mode = 'chat', link = '', htmlCode = '';
  function run(){
    var iss = [], raw = v('waNum'), msg = $('waMsg').value.replace(/^\s+|\s+$/g, ''), cc = $('waCc').value, full = '';
    $('waNumRow').style.display = mode === 'chat' ? '' : 'none';
    if (mode === 'chat'){
      var intl = /^\s*(\+|00)/.test(raw), d = raw.replace(/\D/g, '');
      if (intl) full = d.replace(/^00/, '');
      else if (!cc){ iss.push(['bad', 'Choose a country code, or type the full number starting with ' + c('+') + '.']); }
      else {
        d = d.replace(/^0+/, '');
        if (d.indexOf(cc) === 0 && d.length > 10 && cc !== '1') iss.push(['warn', 'Your number seems to start with the country code already. If so, remove it from the number box.']);
        full = cc + d;
      }
      if (!raw) iss.push(['bad', 'Enter your WhatsApp number.']);
      else if (full && (full.length < 8 || full.length > 15)) iss.push(['bad', 'A full international number has 8 to 15 digits. Yours has ' + full.length + '. Check for missing or extra digits.']);
      if (cc === '91' && !intl && d && !/^[6-9]\d{9}$/.test(d)) iss.push(['warn', 'Indian mobile numbers have 10 digits and start with 6, 7, 8 or 9. Check your number.']);
      if (/^0/.test(raw.replace(/\D/g, '')) && !intl) iss.push(['warn', 'The leading 0 was removed, as WhatsApp links use the international format.']);
      $('waDigits').textContent = full.length;
    } else $('waDigits').textContent = 'n/a';
    if (mode === 'share' && !msg) iss.push(['bad', 'Type the message you want people to share.']);
    var bad = iss.some(function(i){ return i[0] === 'bad'; });
    link = bad ? '' : 'https://wa.me/' + (mode === 'chat' ? full : '') + (msg ? '?text=' + encodeURIComponent(msg) : '');
    $('waOut').textContent = link || 'Fix the details to build your link.';
    $('waOpen').href = link || '#';
    $('waChars').textContent = msg.length; $('waLen').textContent = link ? link.length : '…';
    if (link.length > 2000) iss.push(['warn', 'This link is very long. Some apps and QR code makers struggle with links over 2,000 characters, so shorten the message.']);
    issues('waCheck', iss, '<strong>Ready to use.</strong> ' + (mode === 'chat' ? 'Anyone who taps this link gets a chat with +' + esc(full) + (msg ? ' and your message typed in.' : '.') : 'Tapping the link lets people pick a contact to send your message to.'));
    var lab = esc(v('waLabel') || 'Chat on WhatsApp');
    htmlCode = link ? '<a href="' + esc(link) + '" target="_blank" rel="noopener"\n   style="display:inline-block;background:#25D366;color:#fff;padding:12px 20px;border-radius:8px;font-weight:700;text-decoration:none">' + lab + '</a>' : '';
    $('waHtml').textContent = htmlCode || 'Your button code appears here.';
  }
  $('waMode').addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return; mode = b.getAttribute('data-m');
    $('waMode').querySelectorAll('button').forEach(function(x){ x.classList.toggle('dark', x === b); }); run();
  });
  $('waForm').addEventListener('input', run); $('waForm').addEventListener('change', run);
  $('waCopy').onclick = function(){ if (link) copyText(link, 'toast'); };
  $('waCopyHtml').onclick = function(){ if (htmlCode) copyText(htmlCode, 'toast'); };
  $('waOpen').addEventListener('click', function(e){ if (!link) e.preventDefault(); });
  run();
''',
        content='''
    <h2>What Is a WhatsApp Link Generator?</h2>
    <p>WhatsApp's click to chat feature lets anyone start a chat with you without saving your number first. You share a short <code>wa.me</code> link, and when someone taps it, WhatsApp opens a chat with you on their phone or computer, often with a message already typed. It is one of the simplest ways for a shop, clinic, coach or service business to turn website visitors and followers into conversations.</p>
    <p>This generator builds the link exactly as described in WhatsApp's own <a href="https://whatsapp.com/faq/en/general/26000030" ''' + EXT + '''>click to chat guide</a>: the full number in international format, without zeros, brackets or dashes, and the message encoded so spaces, emoji and line breaks work.</p>

    <h2>How to Use the WhatsApp Link Generator</h2>
    <ol>
      <li><strong>Choose your country code</strong> and type your WhatsApp number. Spaces and a leading 0 are cleaned up for you.</li>
      <li><strong>Write a pre filled message</strong>, such as the product or page the person came from.</li>
      <li><strong>Copy the link</strong> and test it on your phone.</li>
      <li><strong>Copy the HTML button</strong> if you want a green chat button on your website.</li>
      <li><strong>Sharing a promo instead?</strong> Switch to Share a message only to let people forward your message to their own contacts.</li>
    </ol>

    <h2>WhatsApp Link Formats</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Link type', 'Format', 'Use it for') + '''
      <tbody>
        <tr><td>Chat with a number</td><td><code>https://wa.me/919876543210</code></td><td>Contact buttons, bios, business cards</td></tr>
        <tr><td>Chat with a message</td><td><code>https://wa.me/919876543210?text=Hi</code></td><td>Product pages, ads, enquiry forms</td></tr>
        <tr><td>Message only</td><td><code>https://wa.me/?text=Hi</code></td><td>Referral and share buttons</td></tr>
      </tbody>
    </table></div>

    <h2>Where to Use Your WhatsApp Link</h2>
    <ul>
      <li><strong>Instagram and Facebook bios.</strong> Put the link in your bio or link in bio page so followers can message you in one tap.</li>
      <li><strong>Google Business Profile.</strong> Add it as your chat or website link to get leads straight from Maps.</li>
      <li><strong>Product and pricing pages.</strong> Use a different message on each page so you know what the person was looking at.</li>
      <li><strong>Print and packaging.</strong> Turn the link into a QR code for flyers, menus and shop counters.</li>
      <li><strong>Track your clicks.</strong> The wa.me link itself cannot carry UTM tags, so track clicks on the button with an analytics event instead.</li>
    </ul>

    <h2>Turn Chats Into Customers</h2>
    <p>Bring more people to your chat with our guide on <a href="''' + B + '''how-to-generate-high-quality-leads-2026/">how to generate high quality leads</a>, set up your listing with the <a href="''' + B + '''google-my-business-profile-complete-guide-beginners/">Google Business Profile guide</a>, and measure clicks on your button with <a href="''' + B + '''track-button-clicks-ga4/">button click tracking in GA4</a>. Writing the message for an Instagram caption too? Check its length with the <a href="''' + SM + '''social-media-character-counter/">social media character counter</a>.</p>
''',
        faqs=[
            ("How do I create a WhatsApp link with my number?", "Use https://wa.me/ followed by your full number in international format, with no plus sign, spaces, brackets, dashes or leading zero. For an Indian number 98765 43210 the link is https://wa.me/919876543210. This tool builds it for you."),
            ("Can I add a message to a WhatsApp link?", "Yes. Add ?text= followed by your message, encoded for web addresses. The message appears in the chat box when the link opens, and the person can edit it before sending."),
            ("Does the link work for WhatsApp Business numbers?", "Yes. wa.me links work the same way for personal and WhatsApp Business numbers, on phones and on WhatsApp for desktop and web."),
            ("Is my phone number stored?", "No. The link is built entirely in your browser. Your number and message are never uploaded or saved."),
        ],
        related=[("How to Generate High Quality Leads", "how-to-generate-high-quality-leads-2026"), ("Google Business Profile Guide", "google-my-business-profile-complete-guide-beginners"),
                 ("Track Button Clicks in GA4", "track-button-clicks-ga4"), ("Instagram Marketing Guide", "instagram-marketing-guide-businesses")],
    ))

    # ---------- 6. ENGAGEMENT RATE CALCULATOR ----------
    TOOLS.append(dict(
        slug='engagement-rate-calculator', short='ER', name='Engagement Rate Calculator',
        card='Work out engagement rate by followers, reach and impressions for Instagram, LinkedIn, TikTok, Facebook and X.',
        title='Engagement Rate Calculator: Instagram, LinkedIn, TikTok',
        desc='Free engagement rate calculator. Get engagement rate by followers, reach and views for Instagram, LinkedIn, TikTok, Facebook, X and YouTube in seconds.',
        h1='Engagement Rate Calculator',
        lead='Enter likes, comments, shares and saves with your followers, reach or views. Get engagement rate by every common formula, see which one to report, and find how many interactions you need to hit a goal.',
        tool='''<section class="tool" aria-label="Engagement rate calculator" id="erForm">
    <div class="card" style="min-width:0">
      <h2>Your Numbers</h2>
      ''' + R2(F('erPlat', 'Platform', 'Instagram', tag='select', opts=['Instagram', 'LinkedIn', 'TikTok', 'Facebook', 'X (Twitter)', 'YouTube', 'Threads']), F('erPosts', 'Number of Posts', '1', em='totals below cover these', typ='number', extra=' min="1"')) + '''
      ''' + R2(F('erLikes', 'Likes or Reactions', '420', typ='number', extra=' min="0"'), F('erComments', 'Comments', '36', typ='number', extra=' min="0"')) + '''
      ''' + R2(F('erShares', 'Shares or Reposts', '28', typ='number', extra=' min="0"'), F('erSaves', 'Saves', '64', typ='number', extra=' min="0"')) + '''
      ''' + F('erClicks', 'Other Interactions', '0', em='optional, such as link clicks', typ='number', extra=' min="0"') + '''
      ''' + F('erFollowers', 'Followers', '12500', typ='number', extra=' min="0"') + '''
      ''' + R2(F('erReach', 'Reach', '8200', em='unique accounts', typ='number', extra=' min="0"'), F('erImpr', 'Impressions or Views', '11400', typ='number', extra=' min="0"')) + '''
      ''' + F('erGoal', 'Target Engagement Rate', '5', em='% by followers', typ='number', extra=' min="0" step="0.1"') + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Your Engagement Rate</h2>
      <div class="stats">''' + S('erF', 'By Followers') + S('erR', 'By Reach') + S('erI', 'By Views') + '''</div>
      <div class="stats">''' + S('erTot', 'Engagements') + S('erPer', 'Per Post') + S('erRR', 'Reach Rate') + '''</div>
      <div class="kw-result" id="erCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="erTable"></table></div>
      <div class="tips"><strong>Which rate should I report?</strong><ul><li>By followers is best for comparing accounts</li><li>By reach is best for judging your content</li><li>By views suits video and paid posts</li></ul></div>
    </div>
  </section>''',
        js=BASEJS + r'''
  function n(id){ var x = parseFloat($(id).value); return isFinite(x) && x > 0 ? x : 0; }
  function pct(a, b){ return b ? (a / b * 100) : NaN; }
  function p2(x){ return isFinite(x) ? x.toFixed(2) + '%' : '…'; }
  function run(){
    var posts = Math.max(1, Math.round(n('erPosts')) || 1), likes = n('erLikes'), com = n('erComments'), sh = n('erShares'), sv = n('erSaves'), oth = n('erClicks');
    var fol = n('erFollowers'), reach = n('erReach'), imp = n('erImpr'), goal = n('erGoal'), iss = [];
    var tot = likes + com + sh + sv + oth, per = tot / posts;
    var byF = pct(per, fol), byR = pct(tot, reach), byI = pct(tot, imp), rr = pct(reach / posts, fol);
    $('erF').textContent = p2(byF); $('erR').textContent = p2(byR); $('erI').textContent = p2(byI);
    $('erTot').textContent = fmtN(Math.round(tot)); $('erPer').textContent = fmtN(Math.round(per)); $('erRR').textContent = p2(rr);
    if (!tot) iss.push(['bad', 'Enter at least one type of interaction, such as likes or comments.']);
    if (!fol && !reach && !imp) iss.push(['bad', 'Enter followers, reach or views to work out a rate.']);
    if (reach && imp && reach > imp) iss.push(['warn', 'Reach is higher than views. Reach counts unique accounts, so it is normally the smaller number. Check you have not swapped them.']);
    if (reach && tot > reach) iss.push(['warn', 'You have more engagements than reach. That can happen when people interact more than once, but double check the numbers.']);
    if (posts > 1 && reach) iss.push(['warn', 'Reach is added up across ' + posts + ' posts, so the same person may be counted more than once.']);
    var need = goal && fol ? Math.ceil(goal / 100 * fol) : 0;
    var plat = $('erPlat').value, msg = '';
    if (isFinite(byF)) msg = '<strong>' + esc(plat) + ' engagement rate: ' + p2(byF) + ' by followers.</strong> ' + (isFinite(byR) ? 'Of the people who saw ' + (posts > 1 ? 'these posts' : 'this post') + ', ' + p2(byR) + ' interacted. ' : '');
    else if (isFinite(byR)) msg = '<strong>' + p2(byR) + ' of people reached interacted.</strong> ';
    else msg = '<strong>Engagement rate by views: ' + p2(byI) + '.</strong> ';
    if (need) msg += per >= need ? 'You beat your ' + goal + '% target.' : 'To hit ' + goal + '%, each post needs about ' + fmtN(need) + ' interactions, ' + fmtN(Math.ceil(need - per)) + ' more than now.';
    issues('erCheck', iss, msg);
    $('erTable').innerHTML = '<thead><tr><th>Formula</th><th>Calculation</th><th class="num">Result</th></tr></thead><tbody>' +
      '<tr><td>By followers</td><td>' + fmtN(Math.round(per)) + ' per post ÷ ' + fmtN(fol) + ' × 100</td><td class="num">' + p2(byF) + '</td></tr>' +
      '<tr><td>By reach</td><td>' + fmtN(tot) + ' ÷ ' + fmtN(reach) + ' × 100</td><td class="num">' + p2(byR) + '</td></tr>' +
      '<tr><td>By views</td><td>' + fmtN(tot) + ' ÷ ' + fmtN(imp) + ' × 100</td><td class="num">' + p2(byI) + '</td></tr>' +
      '<tr><td>Comments share</td><td>' + fmtN(com) + ' ÷ ' + fmtN(tot) + ' × 100</td><td class="num">' + p2(pct(com, tot)) + '</td></tr>' +
      '<tr><td>Saves and shares share</td><td>' + fmtN(sv + sh) + ' ÷ ' + fmtN(tot) + ' × 100</td><td class="num">' + p2(pct(sv + sh, tot)) + '</td></tr></tbody>';
  }
  $('erForm').addEventListener('input', run); $('erForm').addEventListener('change', run);
  run();
''',
        content='''
    <h2>What Is Engagement Rate?</h2>
    <p>Engagement rate shows how many people interact with your content compared with how many could have. It turns raw likes and comments into a percentage, so a small account and a big one can be compared fairly, and so you can tell whether this month's posts did better than last month's.</p>
    <p>There is no single official formula. Brands, agencies and the apps themselves use different versions, so this calculator shows the three most common side by side and explains when to use each.</p>

    <h2>How to Use the Engagement Rate Calculator</h2>
    <ol>
      <li><strong>Open your insights</strong> in the app or in Meta Business Suite, LinkedIn analytics, TikTok Studio or YouTube Studio.</li>
      <li><strong>Enter the interactions</strong> for one post, or the totals for several posts and how many posts they cover.</li>
      <li><strong>Add followers, reach and views</strong> from the same period.</li>
      <li><strong>Read the three rates</strong> and the breakdown table.</li>
      <li><strong>Set a target</strong> to see how many interactions each post needs to hit it.</li>
    </ol>

    <h2>Engagement Rate Formulas</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Formula', 'Calculation', 'Best for') + '''
      <tbody>
        <tr><td>By followers</td><td>Engagements per post ÷ followers × 100</td><td>Comparing your account with competitors, since follower counts are public</td></tr>
        <tr><td>By reach</td><td>Engagements ÷ reach × 100</td><td>Judging how good a post was with the people who actually saw it</td></tr>
        <tr><td>By views or impressions</td><td>Engagements ÷ views × 100</td><td>Video, reels, shorts and paid posts shown to non followers</td></tr>
      </tbody>
    </table></div>
    <p>Engagements are the sum of likes or reactions, comments, shares or reposts, saves and any other actions you choose to count, such as link clicks. Whatever you include, keep it the same every month so your trend is honest.</p>

    <h2>Tips to Read and Raise Engagement</h2>
    <ul>
      <li><strong>Weigh comments, saves and shares higher.</strong> They take more effort than a like and are strong signals that content is useful.</li>
      <li><strong>Expect lower rates as you grow.</strong> Larger accounts almost always have lower rates by followers, so compare with accounts of a similar size.</li>
      <li><strong>Compare formats separately.</strong> Carousels, reels and text posts behave differently, so track each one on its own.</li>
      <li><strong>Watch reach rate.</strong> If reach rate falls while engagement by reach holds steady, the content is fine and distribution is the problem.</li>
    </ul>

    <h2>Measure What Matters</h2>
    <p>See where engagement fits among other metrics in <a href="''' + B + '''social-media-kpis-every-marketer-should-track/">social media KPIs every marketer should track</a>, learn what your audience says about you through <a href="''' + B + '''social-media-listening/">social media listening</a>, and pick partners wisely with <a href="''' + B + '''influencer-marketing-best-practices-b2b/">influencer marketing best practices</a>. Planning next week's posts? Check their length with the <a href="''' + SM + '''social-media-character-counter/">social media character counter</a>.</p>
''',
        faqs=[
            ("How do you calculate engagement rate?", "Add up likes, comments, shares and saves, divide by followers, reach or views, and multiply by 100. For example 548 engagements on a post from an account with 12,500 followers is a 4.38% engagement rate by followers."),
            ("Should I use followers or reach?", "Use followers when comparing accounts, because anyone can see follower counts. Use reach when judging your own content, because it only counts people who actually saw the post."),
            ("What is a good engagement rate?", "It depends on the platform, your industry and your account size, and published benchmarks vary widely. The most useful comparison is your own trend over time and accounts of a similar size in your niche."),
            ("Is my data stored?", "No. The calculator runs entirely in your browser and the numbers you enter are never uploaded or saved."),
        ],
        related=[("Social Media KPIs to Track", "social-media-kpis-every-marketer-should-track"), ("Social Media Listening", "social-media-listening"),
                 ("Influencer Marketing Best Practices", "influencer-marketing-best-practices-b2b"), ("Instagram Marketing Guide", "instagram-marketing-guide-businesses")],
    ))

    # ---------- 7. YOUTUBE CHAPTERS GENERATOR ----------
    YC_SAMPLE = ('0:45 Why chapters matter\n'
                 '2:10 Writing good chapter titles\n'
                 'Adding timestamps in YouTube Studio 4:05\n'
                 '[6:30] Common mistakes\n'
                 '7:20 Checking chapters on mobile\n'
                 '9:12 Final tips')
    TOOLS.append(dict(
        slug='youtube-chapters-generator', short='YC', name='YouTube Chapters Generator',
        card='Turn rough notes into valid YouTube chapter timestamps, check every rule, and make timestamp links.',
        title='YouTube Chapters Generator: Timestamps for Descriptions',
        desc='Free YouTube chapters generator. Turn rough notes into valid timestamps for your description, check every YouTube chapter rule and build timestamp links.',
        h1='YouTube Chapters Generator',
        lead='Paste your timestamps and titles in any rough format. The generator sorts them, adds the 0:00 start, checks every rule YouTube sets for chapters, and gives you a clean list to paste into your video description.',
        tool='''<section class="tool" aria-label="YouTube chapters generator" id="ycForm">
    <div class="card" style="min-width:0">
      <h2>Your Timestamps</h2>
      ''' + F('ycIn', 'Timestamps and Titles', YC_SAMPLE, em='one per line, any order', tag='textarea', extra=' style="min-height:220px"') + '''
      ''' + R2(F('ycLen', 'Video Length', '10:24', em='optional, like 12:30', ph='12:30'), F('ycSep', 'Format', 'space', tag='select', opts=[('space', '0:00 Title'), ('dash', '0:00 - Title'), ('pipe', '0:00 | Title')])) + '''
      ''' + CK('ycIntro', 'Add a 0:00 chapter if missing') + '''
      ''' + F('ycIntroT', 'Title for the 0:00 Chapter', 'Intro') + '''
      ''' + F('ycUrl', 'Video URL', '', em='optional, for timestamp links', ph='https://youtu.be/VIDEO_ID', mono=True) + '''
    </div>
    <div class="card" style="min-width:0">
      <h2>Chapters for Your Description</h2>
      <pre class="code-out" id="ycOut" ''' + PRE + '''></pre>
      <div class="actions"><button class="btn dark" id="ycCopy">Copy Chapters</button><button class="btn" id="ycCopyL">Copy Timestamp Links</button><span class="toast" id="toast">Copied!</span></div>
      <div class="stats" style="margin-top:16px">''' + S('ycN', 'Chapters') + S('ycShort', 'Shortest') + S('ycAvg', 'Average Length') + '''</div>
      <div class="kw-result" id="ycCheck"></div>
      <div style="overflow-x:auto"><table class="rtable" id="ycTable"></table></div>
      <pre class="code-out" id="ycLinks" ''' + PRE.replace('margin-top:0', 'margin-top:14px') + '''></pre>
    </div>
  </section>''',
        js=BASEJS + r'''
  var TRE = /(^|[\s\[(])((?:\d{1,2}:)?\d{1,3}:\d{2})(?=$|[\s\])|:.,\-–—])/;
  function secs(t){ var p = t.split(':').map(Number); return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1]; }
  function okT(t){ var p = t.split(':').map(Number); return p[p.length - 1] < 60 && (p.length < 3 || p[1] < 60); }
  function pad(x){ return (x < 10 ? '0' : '') + x; }
  function fmt(s){ var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return h ? h + ':' + pad(m) + ':' + pad(x) : m + ':' + pad(x); }
  function dur(s){ return s >= 60 ? Math.floor(s / 60) + 'm ' + pad(s % 60) + 's' : s + 's'; }
  function vid(u){ var m = String(u).match(/(?:youtu\.be\/|[?&]v=|\/shorts\/|\/embed\/|\/live\/)([\w-]{11})/); return m ? m[1] : (/^[\w-]{11}$/.test(u) ? u : ''); }
  var outText = '', linkText = '';
  function run(){
    var iss = [], ch = [], skipped = [], badT = [];
    $('ycIn').value.split('\n').forEach(function(line){
      var l = line.trim(); if (!l) return;
      var m = l.match(TRE);
      if (!m){ skipped.push(l); return; }
      if (!okT(m[2])){ badT.push(m[2]); return; }
      var title = (l.slice(0, m.index) + m[1] + ' ' + l.slice(m.index + m[0].length)).replace(/[\[\]()]/g, ' ').replace(/^[\s\-–—|:.]+|[\s\-–—|:.]+$/g, '').replace(/\s{2,}/g, ' ');
      ch.push({s: secs(m[2]), t: title});
    });
    ch.sort(function(a, b){ return a.s - b.s; });
    var seen = {}, dupes = [];
    ch = ch.filter(function(x){ if (seen[x.s]){ dupes.push(fmt(x.s)); return false; } seen[x.s] = 1; return true; });
    if (ch.length && ch[0].s !== 0){
      if ($('ycIntro').checked){ ch.unshift({s: 0, t: v('ycIntroT') || 'Intro', added: true}); }
      else iss.push(['bad', 'The first chapter must start at ' + c('0:00') + '. Tick the box to add one.']);
    }
    var lenRaw = v('ycLen'), len = /^(\d{1,2}:)?\d{1,3}:\d{2}$/.test(lenRaw) && okT(lenRaw) ? secs(lenRaw) : 0;
    if (lenRaw && !len) iss.push(['warn', 'Write the video length as minutes and seconds, like ' + c('12:30') + ', or hours too, like ' + c('1:05:00') + '.']);
    var sep = {space: ' ', dash: ' - ', pipe: ' | '}[$('ycSep').value];
    var shortest = Infinity, total = 0;
    var rows = ch.map(function(x, i){
      var end = i + 1 < ch.length ? ch[i + 1].s : len, d = end ? end - x.s : 0, st = 'OK';
      if (end && d < 10){ st = 'Too short'; iss.push(['bad', 'Chapter ' + c(fmt(x.s) + ' ' + (x.t || '')) + ' is only ' + d + ' seconds. Each chapter must be at least 10 seconds.']); }
      if (len && x.s >= len){ st = 'After video end'; iss.push(['bad', 'Chapter at ' + c(fmt(x.s)) + ' starts after the video ends at ' + c(fmt(len)) + '.']); }
      if (!x.t){ st = st === 'OK' ? 'No title' : st; iss.push(['warn', 'The chapter at ' + c(fmt(x.s)) + ' has no title.']); }
      if (end && d > 0){ shortest = Math.min(shortest, d); total += d; }
      return '<tr' + (st !== 'OK' ? ' style="background:#fdecea"' : '') + '><td class="num">' + (i + 1) + '</td><td><code>' + fmt(x.s) + '</code></td><td>' + (end ? dur(Math.max(0, d)) : 'to the end') + '</td><td>' + esc(x.t || '(no title)') + (x.added ? ' <em>(added)</em>' : '') + '</td><td>' + st + '</td></tr>';
    });
    if (ch.length && ch.length < 3) iss.push(['bad', 'YouTube needs at least 3 chapters. You have ' + ch.length + '.']);
    if (!ch.length) iss.push(['bad', 'No timestamps found. Start each line with a time like ' + c('1:30') + ' followed by the chapter title.']);
    if (skipped.length) iss.push(['warn', skipped.length + ' line' + (skipped.length > 1 ? 's have' : ' has') + ' no timestamp and ' + (skipped.length > 1 ? 'were' : 'was') + ' skipped: ' + c(skipped[0].slice(0, 40)) + '.']);
    if (badT.length) iss.push(['warn', c(badT[0]) + ' is not a valid time, as seconds and minutes must be under 60.']);
    if (dupes.length) iss.push(['warn', 'Two lines share the time ' + c(dupes[0]) + '. Only the first was kept.']);
    if (!len && ch.length) iss.push(['warn', 'Add the video length to check that the last chapter is at least 10 seconds long.']);
    outText = ch.map(function(x){ return fmt(x.s) + sep + (x.t || ''); }).join('\n');
    $('ycOut').textContent = outText || 'Your chapters appear here.';
    $('ycN').textContent = ch.length; $('ycShort').textContent = isFinite(shortest) ? dur(shortest) : '…';
    var counted = rows.length ? ch.filter(function(x, i){ return i + 1 < ch.length || len; }).length : 0;
    $('ycAvg').textContent = counted && total ? dur(Math.round(total / counted)) : '…';
    issues('ycCheck', iss, '<strong>All YouTube chapter rules pass.</strong> Paste the list into your video description and save.');
    $('ycTable').innerHTML = ch.length ? '<thead><tr><th class="num">#</th><th>Start</th><th>Length</th><th>Title</th><th>Status</th></tr></thead><tbody>' + rows.join('') + '</tbody>' : '';
    var id = vid(v('ycUrl'));
    if (v('ycUrl') && !id) iss.push(['warn', 'Could not find a video ID in that URL.']);
    linkText = id ? ch.map(function(x){ return fmt(x.s) + ' ' + (x.t || '') + '\nhttps://youtu.be/' + id + (x.s ? '?t=' + x.s : ''); }).join('\n\n') : '';
    $('ycLinks').textContent = linkText || 'Add your video URL above to get a direct link to each chapter.';
    if (v('ycUrl') && !id) issues('ycCheck', iss, '');
  }
  $('ycForm').addEventListener('input', run); $('ycForm').addEventListener('change', run);
  $('ycCopy').onclick = function(){ if (outText) copyText(outText, 'toast'); };
  $('ycCopyL').onclick = function(){ if (linkText) copyText(linkText, 'toast'); };
  run();
''',
        content='''
    <h2>What Is a YouTube Chapters Generator?</h2>
    <p>YouTube chapters split a video into named sections. Viewers see them as segments on the progress bar and as a list under the video, so they can jump straight to the part they want. Chapters also give Google clear labels for each part of your video, which can help it show key moments in search.</p>
    <p>To add chapters manually, you type a list of timestamps and titles into the video description. The list has to follow strict rules, and a single mistake means YouTube ignores all of it. This generator cleans up rough notes and checks every rule from <a href="https://support.google.com/youtube/answer/9884579" ''' + EXT + '''>YouTube's chapters help page</a> before you paste.</p>

    <h2>How to Use the YouTube Chapters Generator</h2>
    <ol>
      <li><strong>Paste your notes.</strong> Each line needs a time and a title, in any order: <code>1:30 Setup</code>, <code>Setup 1:30</code> or <code>[1:30] Setup</code> all work.</li>
      <li><strong>Add the video length</strong> so the last chapter can be checked too.</li>
      <li><strong>Keep the 0:00 box ticked</strong> to add a starting chapter if your list does not have one.</li>
      <li><strong>Fix anything in red</strong>, such as chapters shorter than 10 seconds.</li>
      <li><strong>Copy the chapters</strong> into your description in YouTube Studio and save.</li>
    </ol>

    <h2>YouTube Chapter Rules</h2>
    <div style="overflow-x:auto"><table class="lim">
      ''' + th('Rule', 'What it means', 'Checked here') + '''
      <tbody>
        <tr><td>Start at 0:00</td><td>The first timestamp must be 0:00</td><td>Yes, and added for you</td></tr>
        <tr><td>At least 3 chapters</td><td>Fewer than three timestamps are ignored</td><td>Yes</td></tr>
        <tr><td>Ascending order</td><td>Times must go from earliest to latest</td><td>Yes, sorted for you</td></tr>
        <tr><td>10 seconds minimum</td><td>Every chapter must last at least 10 seconds</td><td>Yes, including the last one if you add the length</td></tr>
        <tr><td>Account in good standing</td><td>Channels with active strikes cannot use chapters</td><td>No, check YouTube Studio</td></tr>
      </tbody>
    </table></div>

    <h2>Tips for Chapters Viewers Use</h2>
    <ul>
      <li><strong>Write titles people search for.</strong> "Adding timestamps in YouTube Studio" helps more than "Part 3".</li>
      <li><strong>Keep titles short.</strong> On phones only a few words show on the progress bar.</li>
      <li><strong>Do not overdo it.</strong> Five to ten chapters suit most videos. Very short chapters make the bar hard to use.</li>
      <li><strong>Saving your own list overrides automatic chapters.</strong> If YouTube already added chapters you like, you can leave them.</li>
      <li><strong>Share a moment.</strong> Use the timestamp links to point people to a section from social posts or comments.</li>
    </ul>

    <h2>Grow Your Channel</h2>
    <p>Learn what it takes to earn from your videos in <a href="''' + B + '''youtube-monetization-2025/">YouTube monetization</a> and the latest <a href="''' + B + '''youtube-partner-program-2027-updates/">YouTube Partner Program updates</a>, and find fresh formats in <a href="''' + B + '''7-creative-video-marketing-ideas/">7 creative video marketing ideas</a>. Need a thumbnail at the right size? Use the <a href="''' + SM + '''social-media-image-resizer/">social media image resizer</a>.</p>
''',
        faqs=[
            ("Why are my YouTube chapters not showing?", "Usually one rule is broken: the first timestamp is not 0:00, there are fewer than three timestamps, they are out of order, or a chapter is shorter than 10 seconds. Channels with active strikes also cannot use chapters. Paste your list here to find the problem."),
            ("How do I add chapters to a YouTube video?", "Open the video in YouTube Studio, go to Details, and paste a list of timestamps and titles into the description, starting with 0:00. Save the video and the chapters appear within a few minutes."),
            ("Do I need hours in timestamps for long videos?", "Only for times past one hour. Use minutes and seconds like 12:30 below an hour and hours, minutes and seconds like 1:05:00 after it. The generator formats each time for you."),
            ("Is my data sent anywhere?", "No. The generator runs entirely in your browser. Your notes and video link are never uploaded or stored."),
        ],
        related=[("YouTube Monetization Guide", "youtube-monetization-2025"), ("YouTube Partner Program Updates", "youtube-partner-program-2027-updates"),
                 ("7 Creative Video Marketing Ideas", "7-creative-video-marketing-ideas"), ("Content Calendar Planning", "content-calendar-planning")],
    ))

    for t in TOOLS[_n:]:
        t['cat'] = 'social-media-tools'; t['updated'] = '2026-11-03'
