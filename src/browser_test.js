// Loads every built page in Chromium: JS errors, mobile overflow, dashes in visible text.
// Usage: node src/browser_test.js [tools_dir]   (exit 1 on any problem)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(process.argv[2] || 'tools');
const pages = [];
(function walk(d){ for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f === 'index.html') pages.push(p); } })(root);
(async () => {
  const b = await chromium.launch(); let bad = 0;
  for (const file of pages.sort()) {
    const rel = path.relative(root, file);
    const p = await b.newPage({ viewport: { width: 1366, height: 1000 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + file);
    const dashes = await p.evaluate(() => {
      const out = [], w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const n = w.currentNode, el = n.parentElement;
        if (el.closest('.site-header,.site-footer,code,pre,script,style,nav,textarea,select,input,.slug-row,.g-url,.o-row,.rtable,.code-out')) continue;
        (n.textContent.match(/\S*[—–]\S*|\b[A-Za-z]+-[A-Za-z]+\b/g) || []).forEach(x => out.push(x));
      }
      return out;
    });
    const m = await b.newPage({ viewport: { width: 390, height: 800 } });
    await m.goto('file://' + file);
    const sw = await m.evaluate(() => document.documentElement.scrollWidth);
    const problems = [];
    if (errs.length) problems.push('JS errors: ' + errs.join(' / '));
    if (sw > 392) problems.push('mobile horizontal overflow ' + sw + 'px');
    if (dashes.length) problems.push('dashes: ' + [...new Set(dashes)].slice(0, 6).join(', '));
    console.log((problems.length ? 'FIX ' : 'OK  ') + rel + (problems.length ? '\n     ' + problems.join('\n     ') : ''));
    if (problems.length) bad++;
    await p.close(); await m.close();
  }
  await b.close();
  console.log(`\n${pages.length} pages, ${bad} with problems`);
  process.exit(bad ? 1 : 0);
})();
