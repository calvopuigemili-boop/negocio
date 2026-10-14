"""Genera el logo y el banner de la tienda «Modo Autónomo» en tienda-camisetas/marca/.

Uso: python3 scripts/generar_marca.py  (mismos requisitos que generar_disenos.py)
"""
import subprocess
import tempfile
from pathlib import Path

from generar_disenos import CHROME

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "tienda-camisetas" / "marca"

INTERRUPTOR = """<svg viewBox="0 0 120 64" width="{w}" aria-hidden="true">
<rect x="2" y="2" width="116" height="60" rx="30" fill="#e8590c"/>
<circle cx="86" cy="32" r="22" fill="#fff"/></svg>"""

ESTILO = """<style>html,body{margin:0}body{width:%dpx;height:%dpx;display:flex;align-items:center;
justify-content:center;background:#1d2733;color:#fff;font-family:"Anton";overflow:hidden}
.t{line-height:.9;letter-spacing:.01em}.n{color:#ffb000}
.s{font-family:"Bebas Neue";color:#d6d6dc;letter-spacing:.08em}</style>"""

PIEZAS = {
    "logo.png": (1000, 1000, f"""<div style="text-align:center">{INTERRUPTOR.format(w=360)}
<div class="t" style="font-size:190px;margin-top:40px">MODO</div>
<div class="t n" style="font-size:190px;margin-top:48px">AUTÓNOMO</div></div>"""),
    "banner.png": (1920, 480, f"""<div style="display:flex;align-items:center;gap:56px">{INTERRUPTOR.format(w=240)}
<div><div class="t" style="font-size:150px">MODO <span class="n">AUTÓNOMO</span></div>
<div class="s" style="font-size:54px;margin-top:14px">CAMISETAS Y TAZAS PARA LOS QUE SON SU PROPIO JEFE (Y SU PROPIO BECARIO)</div></div></div>"""),
}


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        for nombre, (w, h, cuerpo) in PIEZAS.items():
            pagina = Path(t) / "p.html"
            pagina.write_text(f'<!doctype html><meta charset="utf-8">{ESTILO % (w, h)}<body>{cuerpo}', encoding="utf-8")
            subprocess.run([CHROME, "--headless", "--no-sandbox", "--hide-scrollbars", f"--window-size={w},{h}",
                            "--force-device-scale-factor=2", f"--screenshot={SALIDA / nombre}", pagina.as_uri()],
                           check=True, capture_output=True, timeout=120)
            print(SALIDA / nombre)


if __name__ == "__main__":
    main()
