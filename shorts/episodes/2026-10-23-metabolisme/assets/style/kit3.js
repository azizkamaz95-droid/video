/* v3 motion helpers. Every tween is a fromTo placed on the scene's paused timeline (seek-safe, deterministic). */
window.K3 = (function () {
  // local scene time from a global time
  const T = (t0) => (t) => +Math.max(0, t - t0).toFixed(3);

  // auto-fit [data-fit] texts to their max width (uses the text's own font)
  function fit(root) {
    root.querySelectorAll("[data-fit]").forEach((el) => {
      const cs = getComputedStyle(el);
      const base = parseFloat(cs.fontSize);
      const fam = cs.fontFamily.split(",")[0].trim();
      el.style.fontSize = window.__hyperframes.fitTextFontSize(el.textContent, { maxWidth: +el.dataset.fit, fontFamily: fam, fontWeight: +cs.fontWeight || 900, baseFontSize: base, minFontSize: 36, step: 2 }).fontSize + "px";
    });
  }

  // wrap every word of an element in <span class="w"> (once, DOM based). Each span carries its own trailing space
  // (white-space: pre), so no bare whitespace text node is left between animated words.
  function split(el) {
    if (!el.dataset.split) {
      Array.from(el.childNodes).forEach((n) => {
        if (n.nodeType !== 3) return;
        const frag = document.createDocumentFragment();
        const toks = n.textContent.match(/\s+|[^\s]+/g) || [];
        let last = null;
        toks.forEach((p) => {
          if (/^\s+$/.test(p)) {
            if (last) { last.textContent += " "; }
            else { const sp = document.createElement("span"); sp.className = "w"; sp.textContent = " "; frag.appendChild(sp); }
            return;
          }
          const sp = document.createElement("span");
          sp.className = "w";
          sp.textContent = p;
          frag.appendChild(sp);
          last = sp;
        });
        el.replaceChild(frag, n);
      });
      el.dataset.split = "1";
    }
    return Array.from(el.children).filter((c) => c.tagName !== "BR" && c.textContent.trim() !== "");
  }

  // words pop in at the given times (one time per word; missing times reuse the last)
  function words(tl, at, el, times, opt = {}) {
    const ws = split(el);
    ws.forEach((w, i) => {
      const t = times[Math.min(i, times.length - 1)];
      tl.fromTo(w, { y: opt.y ?? 46, opacity: 0, scale: opt.s ?? 0.7, rotation: opt.r ?? -5 }, { y: 0, opacity: 1, scale: 1, rotation: 0, duration: 0.26, ease: "back.out(2.4)" }, at(t));
    });
    return ws;
  }

  function pop(tl, at, sel, t, o = {}) {
    tl.fromTo(sel, { scale: o.from ?? 0.4, opacity: 0, rotation: o.r0 ?? -8, y: o.y ?? 0 }, { scale: 1, opacity: 1, rotation: o.r ?? 0, y: 0, duration: o.d ?? 0.34, ease: o.ease ?? "back.out(2.2)" }, at(t));
  }

  function slam(tl, at, sel, t, o = {}) {
    tl.fromTo(sel, { scale: o.from ?? 2.4, opacity: 0, rotation: o.r0 ?? 0 }, { scale: 1, opacity: 1, rotation: o.r ?? 0, duration: o.d ?? 0.2, ease: "power4.in" }, at(t));
  }

  function slide(tl, at, sel, t, o = {}) {
    tl.fromTo(sel, { x: o.dx ?? 900, y: o.dy ?? 0, opacity: 0, rotation: o.r0 ?? 0 }, { x: 0, y: 0, opacity: 1, rotation: o.r ?? 0, duration: o.d ?? 0.34, ease: o.ease ?? "power3.out" }, at(t));
  }

  // marker highlight: the box behind .mk sweeps in from the left
  function marker(tl, at, mkEl, t, d = 0.22) {
    const el = typeof mkEl === "string" ? document.querySelector(mkEl) : mkEl;
    tl.fromTo(el.querySelector(":scope > i"), { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power2.out" }, at(t));
  }

  // draw an SVG path / line (stroke reveal)
  function draw(tl, at, path, t, d = 0.45, ease = "power1.inOut") {
    const els = typeof path === "string" ? Array.from(document.querySelectorAll(path)) : [path];
    els.forEach((p) => {
      const L = Math.ceil((p.getTotalLength ? p.getTotalLength() : 1000) + 2);
      tl.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease }, at(t));
    });
  }

  // handwriting feel: left-to-right wipe
  function write(tl, at, sel, t, d = 0.45) {
    tl.fromTo(sel, { clipPath: "inset(-30% 104% -30% -4%)" }, { clipPath: "inset(-30% -4% -30% -4%)", duration: d, ease: "power1.inOut" }, at(t));
  }

  // thin-space thousands: 5004 -> "5 004"
  const fmtInt = (v) => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, " ");

  function count(tl, at, el, from, to, t, d, fmt) {
    const o = { v: from };
    const f = fmt || fmtInt;
    el.textContent = f(from);
    tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", onUpdate: () => { el.textContent = f(o.v); } }, at(t));
  }

  // card dropped onto the table
  function drop(tl, at, sel, t, r = 0, o = {}) {
    tl.fromTo(sel, { y: o.y ?? -220, rotation: r - 12, opacity: 0, scale: 1.12 }, { y: 0, rotation: r, opacity: 1, scale: 1, duration: o.d ?? 0.42, ease: "back.out(1.5)" }, at(t));
  }

  // scene entrance / exit pushes (camera-like, with motion blur)
  function enter(tl, at, sel, t, dir = 1) {
    tl.fromTo(sel, { x: 1100 * dir, filter: "blur(14px)" }, { x: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }, at(t));
  }
  function exit(tl, at, sel, t, dir = -1) {
    tl.fromTo(sel, { x: 0, filter: "blur(0px)" }, { x: 1100 * dir, filter: "blur(14px)", duration: 0.22, ease: "power3.in", immediateRender: false }, at(t));
  }

  function wobble(tl, at, sel, t, amp = 3, n = 5) {
    tl.fromTo(sel, { rotation: 0 }, { rotation: amp, duration: 0.06, ease: "sine.inOut", yoyo: true, repeat: n, immediateRender: false }, at(t));
  }

  return { T, fit, split, words, pop, slam, slide, marker, draw, write, fmtInt, count, drop, enter, exit, wobble };
})();
