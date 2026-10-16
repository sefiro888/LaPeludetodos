// Prueba de scroll: node scripts/scrolltest.cjs [prefijo-de-página]
// Baja con la rueda paso a paso y avisa si la página retrocede, salta
// o se mueve el contenido mientras cargan las imágenes (CLS).
// Requiere playwright global y el servidor local en 5240.
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require(path.join(process.env.APPDATA, 'npm/node_modules/playwright'));
const only = process.argv[2];
// «eu/» como prefijo revisa la versión en euskera
const sub = only && only.startsWith('eu/') ? 'eu/' : '';
const pref = sub ? only.slice(3) : only;
const pages = fs.readdirSync(path.join(__dirname, '..', sub)).filter(f => f.endsWith('.html') && (!pref || f.startsWith(pref))).map(f => sub + f);
const views = [['escritorio', { width: 1440, height: 900 }, false], ['móvil', { width: 390, height: 844 }, true]];
(async () => {
  const browser = await chromium.launch();
  let fallos = 0;
  for (const file of pages) for (const [name, vp, mobile] of views) {
    const page = await browser.newPage({ viewport: vp, isMobile: mobile, hasTouch: mobile });
    await page.addInitScript(() => { try { sessionStorage.setItem('lpdt-intro', '1'); } catch (e) {} });
    await page.addInitScript(() => {
      window.__cls = 0;
      new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value; }))
        .observe({ type: 'layout-shift', buffered: true });
    });
    await page.goto('http://localhost:5240/' + file, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(400);
    await page.mouse.move(vp.width / 2, vp.height / 2);
    const max = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    const pasos = [];
    let prev = 0, problemas = [];
    for (let i = 0; i < 400; i++) {
      await page.mouse.wheel(0, 240);
      await page.waitForTimeout(90);
      const y = await page.evaluate(() => scrollY);
      if (y < prev - 2) problemas.push(`retrocede ${Math.round(prev)}→${Math.round(y)}`);
      if (y - prev > 700) problemas.push(`salto ${Math.round(prev)}→${Math.round(y)}`);
      pasos.push(y); prev = y;
      if (y >= max - 2) break;
    }
    await page.waitForTimeout(600);
    const cls = await page.evaluate(() => window.__cls);
    const ok = !problemas.length && cls < 0.1;
    if (!ok) fallos++;
    console.log(`${ok ? 'OK  ' : 'MAL '} ${file.padEnd(28)} ${name.padEnd(10)} CLS ${cls.toFixed(3)} ${problemas.slice(0, 4).join(' · ')}`);
    await page.close();
  }
  await browser.close();
  console.log(fallos ? `${fallos} casos con problemas` : 'Scroll limpio en todas las páginas');
})();
