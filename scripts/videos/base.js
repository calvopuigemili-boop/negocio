// Utilidades compartidas por todos los vídeos.
// Cada vídeo define DURATION (segundos) y render(t). SOUNDS = [{t, tipo}] se mezcla en el audio.
window.SOUNDS = [];
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, t0, d) => clamp((t - t0) / d);
const easeOut = x => 1 - Math.pow(1 - x, 3);
const easeInOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const easeBack = x => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const $ = s => document.querySelector(s);
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const sonido = (t, tipo) => window.SOUNDS.push({ t: +t.toFixed(3), tipo });
const euros = n => n.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: 'always' }) + ' €';

// Tiempo de escritura "humano": ritmo variable y determinista.
// Trabaja con caracteres completos (Array.from) para no partir emojis.
function tiemposEscritura(texto, t0, cps = 13) {
  const cs = Array.from(texto), ts = []; let t = t0;
  for (let i = 0; i < cs.length; i++) {
    const r = Math.abs(Math.sin(i * 12.9898 + cs.length) * 43758.5453) % 1;
    t += (1 / cps) * (0.6 + r * 0.9) + (cs[i] === ' ' ? 0.03 : 0);
    ts.push(t);
  }
  return ts;
}
// Igual, pero programado para terminar justo en tFin.
function escrituraHasta(texto, tFin, cps = 13) {
  const ts = tiemposEscritura(texto, 0, cps), d = tFin - ts[ts.length - 1];
  return ts.map(x => x + d);
}
const escritoHasta = (texto, ts, t) => { let n = 0; while (n < ts.length && ts[n] <= t) n++; return Array.from(texto).slice(0, n).join(''); };

// Barra de estado iOS
function barraEstado(color = '#000', hora = '9:41') {
  return `<div class="estado" style="color:${color}"><span>${hora}</span><span class="iconos">
    <span class="barras"><i style="height:4px"></i><i style="height:6px"></i><i style="height:8.5px"></i><i style="height:11px"></i></span>
    <svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 11.5 5.2 8.6a4 4 0 0 1 5.6 0zM2.6 6a7.6 7.6 0 0 1 10.8 0l-1.4 1.4a5.6 5.6 0 0 0-8 0zM0 3.4a11.3 11.3 0 0 1 16 0L14.6 4.8a9.3 9.3 0 0 0-13.2 0z" fill="currentColor"/></svg>
    <span class="bat"></span></span></div>`;
}

// Teclado iOS en español con pulsaciones visibles
const FILAS = ['qwertyuiop', 'asdfghjklñ', 'zxcvbnm'];
function crearTeclado(padre) {
  const t = el('div', 'teclado');
  const teclas = {};
  FILAS.forEach((f, i) => {
    const fila = el('div', 'fila');
    if (i === 2) fila.appendChild(el('div', 'k esp', '⇧'));
    for (const c of f) { const k = el('div', 'k', c); teclas[c] = k; fila.appendChild(k); }
    if (i === 2) fila.appendChild(el('div', 'k esp', '⌫'));
    t.appendChild(fila);
  });
  const ult = el('div', 'fila');
  ult.appendChild(el('div', 'k esp', '123'));
  ult.appendChild(el('div', 'k esp', '☺'));
  const esp = el('div', 'k barra-esp', 'espacio'); teclas[' '] = esp; ult.appendChild(esp);
  ult.appendChild(el('div', 'k esp', 'intro'));
  t.appendChild(ult);
  padre.appendChild(t);
  return {
    nodo: t,
    pulsar(caracter) {
      for (const k of Object.values(teclas)) { k.classList.remove('on'); const g = k.querySelector('.globo'); if (g) g.remove(); }
      if (caracter == null) return;
      const base = caracter.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
      const k = teclas[caracter === 'ñ' ? 'ñ' : base];
      if (!k) return;
      if (caracter === ' ') k.classList.add('on'); else k.appendChild(el('div', 'globo', caracter.toLowerCase()));
    },
  };
}
// Qué tecla se está pulsando en el instante t (se ilumina 70 ms)
function teclaActiva(texto, ts, t) {
  const cs = Array.from(texto);
  for (let i = 0; i < ts.length; i++) if (t >= ts[i] - 0.07 && t < ts[i]) return cs[i];
  return null;
}
function sonidosTeclas(ts) { ts.forEach(x => sonido(x - 0.07, 'tecla')); }

// Rótulo estilo TikTok
function rotulo(texto, top, negro = false) {
  const r = el('div', 'rotulo' + (negro ? ' negro' : ''), `<span>${texto}</span>`);
  r.style.top = top + 'px';
  document.body.appendChild(r);
  return r;
}
function animarRotulo(r, t, t0, t1 = 1e9) {
  const p = easeBack(prog(t, t0, 0.35)), q = prog(t, t1, 0.25);
  r.style.opacity = Math.min(prog(t, t0, 0.15), 1 - q);
  r.style.transform = `scale(${0.85 + 0.15 * p})`;
}

// Mockups (camiseta con sombreado y taza)
function camiseta(diseno, ancho = 760, color = '#f4f2ee') {
  const m = el('div', 'mock');
  m.style.width = ancho + 'px'; m.style.height = ancho * 1.1 + 'px';
  m.innerHTML = `<svg viewBox="0 0 400 440" width="${ancho}" height="${ancho * 1.1}">
    <defs><radialGradient id="luz" cx="45%" cy="35%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#000" stop-opacity=".07"/></radialGradient>
    <filter id="som" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-opacity=".22"/></filter></defs>
    <g filter="url(#som)"><path id="tela" d="M138 24 Q200 58 262 24 L368 72 Q372 74 371 79 L343 165 Q341 170 336 168 L304 156 L306 420 Q306 428 298 428 L102 428 Q94 428 94 420 L96 156 L64 168 Q59 170 57 165 L29 79 Q28 74 32 72 Z" fill="${color}"/></g>
    <path d="M138 24 Q200 58 262 24 L368 72 L343 165 L304 156 L306 428 L94 428 L96 156 L57 165 L29 79 Z" fill="url(#luz)"/>
    <path d="M138 24 Q200 64 262 24" fill="none" stroke="rgba(0,0,0,.12)" stroke-width="7"/>
    <path d="M110 200 Q130 300 116 410 M290 210 Q276 300 288 400 M150 395 Q200 405 250 392" fill="none" stroke="rgba(0,0,0,.05)" stroke-width="6" stroke-linecap="round"/>
    <path d="M96 156 Q98 120 92 96 M304 156 Q302 120 308 96" fill="none" stroke="rgba(0,0,0,.08)" stroke-width="3"/></svg>
    <img class="estampado" src="../../tienda-camisetas/disenos/${diseno}-oscuro.png">`;
  const img = m.querySelector('img');
  img.style.left = '50%'; img.style.top = (ancho * 0.30) + 'px';
  img.style.maxWidth = (ancho * 0.40) + 'px'; img.style.maxHeight = (ancho * 0.42) + 'px';
  img.style.transform = 'translateX(-50%)';
  return m;
}
function taza(diseno, ancho = 520) {
  const m = el('div', 'mock');
  m.style.width = ancho * 1.25 + 'px'; m.style.height = ancho * 1.05 + 'px';
  m.innerHTML = `<svg viewBox="0 0 250 210" width="${ancho * 1.25}" height="${ancho * 1.05}">
    <defs><linearGradient id="cil" x1="0" x2="1"><stop offset="0" stop-color="#cfcac2"/><stop offset=".25" stop-color="#fff"/><stop offset=".7" stop-color="#f1eee9"/><stop offset="1" stop-color="#bdb8b0"/></linearGradient>
    <filter id="s2"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-opacity=".22"/></filter></defs>
    <g filter="url(#s2)"><path d="M190 60 C240 60 240 150 190 150" fill="none" stroke="#e9e5df" stroke-width="18"/>
    <path d="M10 22 L10 182 Q10 205 100 205 Q190 205 190 182 L190 22 Z" fill="url(#cil)"/></g>
    <ellipse cx="100" cy="22" rx="90" ry="14" fill="#f7f5f1" stroke="#dcd7cf"/><ellipse cx="100" cy="24" rx="80" ry="10" fill="#4a3426"/></svg>
    <img class="estampado" src="../../tienda-camisetas/disenos/${diseno}-oscuro.png">`;
  const img = m.querySelector('img');
  img.style.left = (ancho * 0.40) + 'px'; img.style.top = (ancho * 0.38) + 'px';
  img.style.maxWidth = (ancho * 0.56) + 'px'; img.style.maxHeight = (ancho * 0.5) + 'px';
  img.style.transform = 'translateX(-50%)';
  return m;
}

// Cierre: producto + llamada a la acción
function crearCierre(tipo, diseno, titulo, t0) {
  sonido(t0, 'swoosh');
  const c = el('div'); c.id = 'cierre';
  let visual;
  if (tipo === 'kit') {
    visual = el('div', 'kit', `<div style="width:820px;background:#fff;border-radius:28px;box-shadow:0 20px 50px rgba(0,0,0,.15);overflow:hidden;font-family:UI">
      <div style="background:#1f6f43;color:#fff;font-weight:700;font-size:40px;padding:26px 34px">Kit Autónomo · Trimestres</div>
      <div style="padding:20px 34px;font-size:36px;line-height:2.1">
      <div style="display:flex;justify-content:space-between"><span>IVA a pagar (303)</span><b>1.050,00 €</b></div>
      <div style="display:flex;justify-content:space-between"><span>IRPF a pagar (130)</span><b>700,00 €</b></div>
      <div style="display:flex;justify-content:space-between;color:#e8590c"><span>Total trimestre</span><b>1.750,00 €</b></div></div></div>`);
  } else visual = tipo === 'taza' ? taza(diseno) : camiseta(diseno, 700);
  c.appendChild(visual);
  c.appendChild(el('div', 't1', titulo));
  c.appendChild(el('div', 't2', 'Link en el perfil'));
  document.body.appendChild(c);
  return { nodo: c, visual };
}
function animarCierre(cierre, t, t0) {
  const p = prog(t, t0, 0.5);
  cierre.nodo.style.opacity = p;
  cierre.visual.style.transform = `translateY(${(1 - easeOut(p)) * 120}px) scale(${1 + 0.04 * prog(t, t0, 4)})`;
}
