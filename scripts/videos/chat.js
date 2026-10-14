// Motor de conversación tipo app de mensajería (genérica, sin marcas).
// Uso: montarChat({contacto, iniciales, colorAvatar, rotulo:{texto,t0,t1}, mensajes:[...], cierre:{tipo,diseno,titulo,t}, duracion})
// Mensajes: {de:'yo'|'el', texto, t, pdf?:'nombre.pdf', cps?} · {fecha:'13 de noviembre', t}
function montarChat(cfg) {
  const css = `
  #pantalla{background:#efeae2}
  #pantalla .estado{background:#f6f5f3}
  .cab{position:absolute;top:44px;left:0;right:0;height:58px;background:#f6f5f3;display:flex;align-items:center;gap:9px;padding:0 12px;border-bottom:.5px solid #d8d6d2;z-index:4}
  .cab .atras{font-size:30px;color:#0a7c66;margin-top:-4px;width:14px}
  .cab .av{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600;font-size:15px}
  .cab .nom{font-weight:600;font-size:16.5px;color:#111}
  .cab .sub{font-size:12.5px;color:#667781;margin-top:1px}
  .cab .sub.esc{color:#0a7c66}
  .cab .ic{margin-left:auto;display:flex;gap:22px;color:#0a7c66}
  .fondo{position:absolute;inset:0;background-image:radial-gradient(rgba(0,0,0,.035) 1.2px,transparent 1.3px);background-size:18px 18px}
  .msgs{position:absolute;top:102px;left:0;right:0;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;padding:0 9px;box-sizing:border-box}
  .w{overflow:hidden;flex:none}
  .w .in{padding-top:3px;padding-bottom:3px;display:flex}
  .w.yo .in{justify-content:flex-end}
  .b{max-width:76%;padding:6px 9px 7px 10px;border-radius:9px;font-size:16px;line-height:1.3;color:#111;box-shadow:0 .6px .5px rgba(0,0,0,.13);position:relative}
  .yo .b{background:#d9fdd3;border-top-right-radius:2px}
  .el .b{background:#fff;border-top-left-radius:2px}
  .b .h{float:right;font-size:11px;color:#667781;margin:7px 0 -4px 9px;display:flex;align-items:center;gap:3px}
  .b .h .ck{color:#53bdeb;font-size:12px;letter-spacing:-4px;margin-right:3px}
  .pdf{display:flex;gap:9px;align-items:center;background:rgba(0,0,0,.05);border-radius:7px;padding:9px;margin-bottom:3px;min-width:220px}
  .pdf .ico{width:30px;height:36px;background:#e2463d;color:#fff;font-size:9px;font-weight:700;border-radius:3px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:4px;box-sizing:border-box}
  .pdf .meta{font-size:12px;color:#667781}
  .fecha .in{justify-content:center;padding:8px 0}
  .fecha .p{background:#fff;color:#54656f;font-size:12.5px;padding:5px 11px;border-radius:7px;box-shadow:0 .6px .5px rgba(0,0,0,.1)}
  .esc-b .b{padding:12px 14px;display:flex;gap:4px}
  .esc-b i{width:7px;height:7px;border-radius:50%;background:#8696a0;display:block}
  .entrada{position:absolute;left:0;right:0;height:54px;background:#f6f5f3;display:flex;align-items:center;gap:10px;padding:0 10px;box-sizing:border-box;z-index:5}
  .entrada .mas{font-size:28px;color:#0a7c66;font-weight:300}
  .entrada .campo{flex:1;min-height:34px;background:#fff;border-radius:18px;border:.5px solid #d1d1d1;padding:7px 13px;box-sizing:border-box;font-size:16px;color:#111;white-space:nowrap;overflow:hidden;display:flex;justify-content:flex-end}
  .entrada .campo .tx{white-space:nowrap}
  .entrada .cur{display:inline-block;width:2px;height:19px;background:#0a7c66;vertical-align:-4px;margin-left:1px}
  .entrada .env{width:34px;height:34px;border-radius:50%;background:#0a7c66;display:flex;align-items:center;justify-content:center}
  `;
  document.head.appendChild(el('style', null, css));
  const pant = $('#pantalla');
  pant.appendChild(el('div', 'fondo'));
  pant.insertAdjacentHTML('beforeend', barraEstado());
  pant.insertAdjacentHTML('beforeend', `<div class="cab"><span class="atras">‹</span>
    <div class="av" style="background:${cfg.colorAvatar}">${cfg.iniciales}</div>
    <div><div class="nom">${cfg.contacto}</div><div class="sub">en línea</div></div>
    <div class="ic"><svg width="22" height="16" viewBox="0 0 22 16"><rect x="1" y="2" width="14" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15 6.5 21 3v10l-6-3.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>
    <svg width="18" height="18" viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></div></div>`);
  const msgs = el('div', 'msgs'); pant.appendChild(msgs);
  const entrada = el('div', 'entrada', `<span class="mas">+</span><div class="campo"><span class="tx"></span></div>
    <div class="env"><svg width="16" height="16" viewBox="0 0 24 24"><path d="M3 20.5 21 12 3 3.5 3 10l12 2-12 2z" fill="#fff"/></svg></div>`);
  pant.appendChild(entrada);
  const tec = crearTeclado(pant);
  const sub = $('.cab .sub'), campo = $('.entrada .tx'), env = $('.entrada .env');

  // Construcción de mensajes + indicador de escritura
  const items = [];
  const hora = i => `10:${String(12 + i * 3).padStart(2, '0')}`;
  cfg.mensajes.forEach((m, i) => {
    let w;
    if (m.fecha) {
      w = el('div', 'w fecha', `<div class="in"><span class="p">${m.fecha}</span></div>`);
    } else {
      const pdf = m.pdf ? `<div class="pdf"><div class="ico">PDF</div><div><div>${m.pdf}</div><div class="meta">1 página · PDF · 84 kB</div></div></div>` : '';
      const ck = m.de === 'yo' ? '<span class="ck">✓✓</span>' : '';
      w = el('div', `w ${m.de}`, `<div class="in"><div class="b">${pdf}${m.texto || ''}<span class="h">${hora(i)}${ck}</span></div></div>`);
      if (m.de === 'yo' && m.texto && !m.pdf) {
        m.ts = escrituraHasta(m.texto, m.t - 0.25, m.cps || 14);
        sonidosTeclas(m.ts);
      }
      sonido(m.t, m.de === 'yo' ? 'enviar' : 'pop');
    }
    msgs.appendChild(w);
    items.push({ m, w });
    if (m.de === 'el') {
      const e = el('div', 'w el esc-b', '<div class="in"><div class="b"><i></i><i></i><i></i></div></div>');
      msgs.insertBefore(e, w);
      items.push({ esc: true, m, w: e });
    }
  });
  items.forEach(it => { it.h = it.w.scrollHeight; });

  // Teclado visible mientras escribo
  const intervalos = cfg.mensajes.filter(m => m.ts).map(m => [m.ts[0] - 0.45, m.t + 0.35]);
  const kbVis = t => {
    let v = 0;
    for (const [a, b] of intervalos) v = Math.max(v, Math.min(easeOut(prog(t, a, 0.3)), 1 - easeOut(prog(t, b, 0.3))));
    return v;
  };

  const rot = cfg.rotulo ? rotulo(cfg.rotulo.texto, 320) : null;
  const cierre = crearCierre(cfg.cierre.tipo, cfg.cierre.diseno, cfg.cierre.titulo, cfg.cierre.t);
  window.DURATION = cfg.duracion;

  window.render = t => {
    const kv = kbVis(t);
    tec.nodo.style.transform = `translateY(${(1 - kv) * 262}px)`;
    const baseEntrada = 693.33 - 262 * kv - 54;
    entrada.style.top = baseEntrada + 'px';
    msgs.style.height = (baseEntrada - 102) + 'px';

    let escribiendo = false, texto = '', tecla = null;
    for (const it of items) {
      const { m } = it;
      if (it.esc) {
        const a = m.t - (m.pensar || 1.1);
        const vis = t >= a && t < m.t;
        if (vis) escribiendo = true;
        const p = vis ? easeOut(prog(t, a, 0.2)) : 0;
        it.w.style.height = it.h * p + 'px';
        it.w.querySelectorAll('i').forEach((d, k) => { d.style.opacity = 0.35 + 0.65 * Math.max(0, Math.sin((t * 6) - k * 0.9)); });
        continue;
      }
      const p = easeOut(prog(t, m.t, 0.22));
      it.w.style.height = it.h * p + 'px';
      const b = it.w.querySelector('.b, .p');
      b.style.opacity = prog(t, m.t, 0.12);
      b.style.transform = `scale(${0.92 + 0.08 * easeBack(prog(t, m.t, 0.3))})`;
      b.style.transformOrigin = m.de === 'yo' ? '100% 100%' : '0 100%';
      if (m.ts && t >= m.ts[0] - 0.1 && t < m.t) { texto = escritoHasta(m.texto, m.ts, t); tecla = teclaActiva(m.texto, m.ts, t); }
    }
    sub.textContent = escribiendo ? 'escribiendo…' : 'en línea';
    sub.className = 'sub' + (escribiendo ? ' esc' : '');
    campo.innerHTML = texto ? `${texto}<span class="cur"></span>` : (kv > 0.5 ? '<span class="cur"></span>' : '');
    env.style.opacity = texto ? 1 : 0.35;
    tec.pulsar(tecla);
    if (rot) animarRotulo(rot, t, cfg.rotulo.t0, cfg.rotulo.t1);
    animarCierre(cierre, t, cfg.cierre.t);
  };
  render(0);
}
