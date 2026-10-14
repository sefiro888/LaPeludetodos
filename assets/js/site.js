/* La Pelu de Tod@s · interacción */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const WA = "34676679807";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- estado abierto/cerrado (hora de Bilbao) ---------- */
  function ahoraMadrid() {
    const p = new Intl.DateTimeFormat("es-ES", { timeZone: "Europe/Madrid", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false })
      .formatToParts(new Date());
    const dias = { lun: 0, mar: 1, "mié": 2, mie: 2, jue: 3, vie: 4, "sáb": 5, sab: 5, dom: 6 };
    const wd = p.find(x => x.type === "weekday").value.replace(".", "").toLowerCase();
    return { d: dias[wd] ?? new Date().getDay() - 1, m: +p.find(x => x.type === "hour").value % 24 * 60 + +p.find(x => x.type === "minute").value };
  }
  const aMin = t => { const [h, m] = t.split(":"); return +h * 60 + +m; };
  const fmt = t => t.replace(/^0/, "");
  const NOMBRES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"];
  function estado() {
    const H = window.HORARIO || {};
    const { d, m } = ahoraMadrid();
    const hoy = H[d] || [];
    for (const [a, c] of hoy) {
      if (m >= aMin(a) && m < aMin(c)) {
        const quedan = aMin(c) - m;
        return { open: true, txt: quedan <= 45 ? `Abierto · cierra pronto (${fmt(c)})` : `Abierto ahora · hasta las ${fmt(c)}${d === 5 ? " (con cita)" : ""}` };
      }
      if (m < aMin(a)) return { open: false, txt: `Cerrado · abrimos hoy a las ${fmt(a)}` };
    }
    for (let i = 1; i <= 7; i++) {
      const nd = (d + i) % 7, f = H[nd] || [];
      if (f.length) return { open: false, txt: `Cerrado · abrimos ${i === 1 ? "mañana" : "el " + NOMBRES[nd]} a las ${fmt(f[0][0])}` };
    }
    return { open: false, txt: "Cerrado" };
  }
  function pintaEstado() {
    const s = estado();
    $$("[data-estado]").forEach(el => {
      el.classList.toggle("is-open", s.open); el.classList.toggle("is-closed", !s.open);
      const t = $(".estado-txt", el); if (t) t.textContent = s.txt;
    });
    const { d } = ahoraMadrid();
    const fila = d === 0 ? 0 : d <= 4 ? 1 : d === 5 ? 2 : 3;
    $$(".horario").forEach(t => $$("tr", t).forEach((tr, i) => tr.classList.toggle("is-today", i === fila)));
  }
  pintaEstado(); setInterval(pintaEstado, 60000);

  /* ---------- cabecera ---------- */
  const header = $("[data-header]");
  let lastY = 0, ticking = false;
  const waFloat = $(".wa-float");
  function onScroll() {
    const y = scrollY;
    header.classList.toggle("is-solid", y > 40);
    header.classList.toggle("is-hidden", y > 600 && y > lastY + 4 && !document.body.classList.contains("menu-open") && !$(".nav-item.is-open"));
    if (y < lastY - 4) header.classList.remove("is-hidden");
    if (waFloat) waFloat.classList.toggle("is-in", y > 500);
    lastY = y; ticking = false;
  }
  addEventListener("scroll", () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* ---------- mega menú y desplegables ---------- */
  const items = $$(".nav-item");
  const cierra = except => items.forEach(it => { if (it !== except) { it.classList.remove("is-open"); $(".nav-btn", it)?.setAttribute("aria-expanded", "false"); } });
  items.forEach(it => {
    const btn = $(".nav-btn", it); let t;
    const abre = () => { clearTimeout(t); cierra(it); it.classList.add("is-open"); btn.setAttribute("aria-expanded", "true");
      const mega = $(".mega", it); if (mega) mega.style.setProperty("--mega-top", header.getBoundingClientRect().bottom + "px"); };
    const sal = () => { t = setTimeout(() => { it.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }, 220); };
    it.addEventListener("mouseenter", () => matchMedia("(hover:hover)").matches && abre());
    it.addEventListener("mouseleave", () => matchMedia("(hover:hover)").matches && sal());
    btn.addEventListener("click", () => it.classList.contains("is-open") ? sal() : abre());
    it.addEventListener("focusout", e => { if (!it.contains(e.relatedTarget)) sal(); });
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") { cierra(); cerrarMenu(); cerrarLB(); } });
  // vista previa del mega menú
  const mImg = $(".mega-img"), mTxt = $(".mega-preview-txt strong"), mTag = $(".mega-preview-txt span");
  $$(".mega-link").forEach(a => a.addEventListener("mouseenter", () => {
    if (!mImg) return;
    mImg.style.opacity = 0;
    setTimeout(() => { mImg.src = a.dataset.img; mImg.style.opacity = 1; }, 140);
    mTxt.textContent = $(".mega-name", a).childNodes[0].textContent.trim();
    mTag.textContent = $(".mega-desc", a).textContent;
  }));

  /* ---------- menú móvil ---------- */
  const mm = $("[data-mmenu]"), burger = $("[data-burger]");
  function abrirMenu() { mm.classList.add("is-open"); mm.setAttribute("aria-hidden", "false"); burger.setAttribute("aria-expanded", "true"); document.body.classList.add("menu-open"); setTimeout(() => $("[data-close]", mm).focus(), 300); }
  function cerrarMenu() { if (!mm?.classList.contains("is-open")) return; mm.classList.remove("is-open"); mm.setAttribute("aria-hidden", "true"); burger.setAttribute("aria-expanded", "false"); document.body.classList.remove("menu-open"); }
  burger?.addEventListener("click", abrirMenu);
  $("[data-close]", mm)?.addEventListener("click", cerrarMenu);
  $$("a", mm).forEach(a => a.addEventListener("click", cerrarMenu));

  /* ---------- aparición al hacer scroll ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach((el, i) => { el.style.transitionDelay = (i % 4) * 70 + "ms"; io.observe(el); });
  } else $$(".reveal").forEach(el => el.classList.add("is-in"));

  /* ---------- índice de la página ---------- */
  const toc = $("[data-toc]");
  if (toc && "IntersectionObserver" in window) {
    const links = $$("a", toc);
    const map = new Map(links.map(a => [a.getAttribute("href").slice(1), a]));
    const io2 = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { links.forEach(l => l.classList.remove("is-on")); const l = map.get(e.target.id); if (l) { l.classList.add("is-on"); const nav = l.parentElement; nav.scrollTo({ left: l.offsetLeft - (nav.clientWidth - l.offsetWidth) / 2, behavior: reduce ? "auto" : "smooth" }); } }
    }), { rootMargin: "-40% 0px -55% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io2.observe(s); });
  }

  /* ---------- carrusel ---------- */
  $$("[data-carousel]").forEach(c => {
    const sec = c.closest("section");
    const paso = () => (c.firstElementChild?.getBoundingClientRect().width || 300) + 20;
    $("[data-car-next]", sec)?.addEventListener("click", () => c.scrollBy({ left: paso(), behavior: "smooth" }));
    $("[data-car-prev]", sec)?.addEventListener("click", () => c.scrollBy({ left: -paso(), behavior: "smooth" }));
  });

  /* ---------- filtros ---------- */
  $$("[data-filter]").forEach(f => {
    const destino = f.dataset.target ? $(f.dataset.target) : $("[data-cards]");
    $$(".filter", f).forEach(b => b.addEventListener("click", () => {
      $$(".filter", f).forEach(x => x.classList.toggle("is-on", x === b));
      $$("[data-cat]", destino).forEach(el => el.classList.toggle("is-hidden", b.dataset.f !== "all" && el.dataset.cat !== b.dataset.f));
    }));
  });

  /* ---------- test «¿qué necesita tu pelo?» ---------- */
  const qbox = $("[data-quizbox]"), qout = $("[data-quiz-out]");
  qbox && $$(".chip", qbox).forEach(b => b.addEventListener("click", () => {
    $$(".chip", qbox).forEach(x => x.classList.toggle("is-on", x === b));
    qout.innerHTML = "";
    JSON.parse(b.dataset.quiz).forEach(slug => { const t = $(`template[data-tpl="${slug}"]`); if (t) qout.appendChild(t.content.cloneNode(true)); });
  }));

  /* ---------- asistente de cita ---------- */
  $$("[data-wizard]").forEach(w => {
    const estadoW = { dias: [], franja: "", primera: "" };
    $$("[data-multi]", w).forEach(g => $$(".chip", g).forEach(c => c.addEventListener("click", () => {
      c.classList.toggle("is-on"); estadoW[g.dataset.multi] = $$(".chip.is-on", g).map(x => x.textContent); render();
    })));
    $$("[data-single]", w).forEach(g => $$(".chip", g).forEach(c => c.addEventListener("click", () => {
      const on = !c.classList.contains("is-on");
      $$(".chip", g).forEach(x => x.classList.remove("is-on"));
      if (on) c.classList.add("is-on");
      estadoW[g.dataset.single] = on ? c.textContent : ""; render();
    })));
    w.addEventListener("input", render); w.addEventListener("change", render);
    w.addEventListener("submit", e => e.preventDefault());
    function render() {
      const f = w.elements;
      const l = ["¡Hola Cova! Me gustaría pedir cita en La Pelu de Tod@s."];
      if (f.nombre.value.trim()) l.push(`Me llamo ${f.nombre.value.trim()}.`);
      l.push(f.servicio.value ? `Servicio: ${f.servicio.value}.` : "Aún no sé qué hacerme, me gustaría que me asesores.");
      if (f.preso.checked) l.push("Me gustaría añadir presoterapia por 5 € con el color.");
      if (estadoW.dias.length) l.push(`Días que me vienen bien: ${estadoW.dias.join(", ").toLowerCase()}.`);
      if (estadoW.franja) l.push(`Franja: ${estadoW.franja.toLowerCase()}.`);
      if (estadoW.primera) l.push(estadoW.primera.startsWith("Sí") ? "Es mi primera vez en la pelu." : "Ya soy cliente/a.");
      if (f.notas.value.trim()) l.push(`Nota: ${f.notas.value.trim()}`);
      const txt = l.join("\n");
      $("[data-preview]", w).textContent = txt;
      $("[data-send]", w).href = `https://wa.me/${WA}?text=${encodeURIComponent(txt)}`;
    }
    render();
  });

  /* ---------- lightbox ---------- */
  const lb = $("[data-lightbox]"); let lbList = [], lbI = 0;
  function abrirLB(list, i) { lbList = list; lbI = i; muestra(); lb.hidden = false; document.body.classList.add("menu-open"); $(".lb-close", lb).focus(); }
  function muestra() { $("img", lb).src = lbList[lbI]; $(".lb-cap", lb).textContent = `${lbI + 1} / ${lbList.length} · Trabajo real de La Pelu de Tod@s`; }
  function cerrarLB() { if (!lb || lb.hidden) return; lb.hidden = true; document.body.classList.remove("menu-open"); }
  $$("[data-gallery]").forEach(g => g.addEventListener("click", e => {
    const b = e.target.closest("[data-lb]"); if (!b) return;
    const visibles = $$("[data-lb]", g).filter(x => !x.closest(".is-hidden"));
    abrirLB(visibles.map(x => x.dataset.lb), visibles.indexOf(b));
  }));
  if (lb) {
    $(".lb-close", lb).onclick = cerrarLB;
    $(".lb-next", lb).onclick = () => { lbI = (lbI + 1) % lbList.length; muestra(); };
    $(".lb-prev", lb).onclick = () => { lbI = (lbI - 1 + lbList.length) % lbList.length; muestra(); };
    lb.addEventListener("click", e => { if (e.target === lb) cerrarLB(); });
    document.addEventListener("keydown", e => { if (lb.hidden) return; if (e.key === "ArrowRight") $(".lb-next", lb).click(); if (e.key === "ArrowLeft") $(".lb-prev", lb).click(); });
  }

  /* ---------- mapa bajo demanda ---------- */
  $$("[data-map-load]").forEach(b => b.addEventListener("click", () => {
    const m = b.closest("[data-map]");
    m.innerHTML = `<iframe src="${m.dataset.src}" title="Mapa de La Pelu de Tod@s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>`;
  }));

  /* ---------- paleta de colores (latón / monocromo) ---------- */
  const root = document.documentElement, meta = $('meta[name="theme-color"]');
  function pintaPaleta() {
    const mono = root.dataset.theme === "mono";
    $$("[data-paleta-nombre]").forEach(el => el.textContent = mono ? "Negro, blanco y gris" : "Paleta latón");
    $$("[data-paleta]").forEach(b => b.setAttribute("aria-pressed", String(mono)));
    if (meta) meta.content = mono ? "#111111" : "#161412";
  }
  $$("[data-paleta]").forEach(b => b.addEventListener("click", () => {
    root.classList.add("theme-anim");
    if (root.dataset.theme === "mono") delete root.dataset.theme; else root.dataset.theme = "mono";
    try { localStorage.setItem("lpdt-paleta", root.dataset.theme === "mono" ? "mono" : "laton"); } catch (_) { }
    pintaPaleta();
    setTimeout(() => root.classList.remove("theme-anim"), 600);
  }));
  pintaPaleta();

  /* ---------- copiar dirección ---------- */
  $$("[data-copy]").forEach(b => b.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); const t = b.textContent; b.textContent = "¡Copiada!"; setTimeout(() => b.textContent = t, 1800); } catch (_) { }
  }));
})();
