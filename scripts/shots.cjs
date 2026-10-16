// Capturas de revisión: node scripts/shots.cjs <carpeta> [prefijo-de-página] [d|m]
// Requiere playwright global y el servidor local: python -m http.server 5240
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require(path.join(process.env.APPDATA, 'npm/node_modules/playwright'));
const out = process.argv[2] || '.';
const only = process.argv[3];
const which = process.argv[4];
fs.mkdirSync(out, { recursive: true });
// «eu/» como prefijo revisa la versión en euskera
const sub = only && only.startsWith('eu/') ? 'eu/' : '';
const pref = sub ? only.slice(3) : only;
const pages = fs.readdirSync(path.join(__dirname, '..', sub)).filter(f => f.endsWith('.html') && (!pref || f.startsWith(pref))).map(f => sub + f);
const views = [['d', { width: 1440, height: 900 }, false], ['m', { width: 390, height: 844 }, true]].filter(v => !which || v[0] === which);
(async () => {
  const browser = await chromium.launch();
  for (const file of pages) for (const [name, vp, mobile] of views) {
    const page = await browser.newPage({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1 });
    await page.addInitScript(() => { try { sessionStorage.setItem('lpdt-intro', '1'); } catch (e) {} });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => m.type() === 'error' && !/maps|google|ERR_|favicon/i.test(m.text()) && errors.push(m.text()));
    page.on('requestfailed', r => !/google|gstatic/.test(r.url()) && errors.push('FALLA ' + r.url()));
    await page.goto('http://localhost:5240/' + file, { waitUntil: 'networkidle' });
    await page.evaluate(async () => {
      document.documentElement.style.scrollBehavior = 'auto';
      document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
      for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
      await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
      window.scrollTo(0, 0);
      document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in'));
      document.querySelectorAll('.hero-in>*').forEach(e => { e.style.animation = 'none'; e.style.opacity = 1; e.style.transform = 'none'; });
    });
    await page.waitForTimeout(1200);
    const ow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    await page.screenshot({ path: path.join(out, `${file.replace('.html', '').replace('/', '_')}-${name}.png`), fullPage: true });
    console.log(file, name, ow > 0 ? `DESBORDE ${ow}px` : 'ok', errors.length ? errors.join(' | ') : '');
    await page.close();
  }
  await browser.close();
})();
