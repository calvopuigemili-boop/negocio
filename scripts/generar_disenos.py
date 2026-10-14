"""Genera los diseños de camisetas de «Modo Autónomo» (PNG transparentes para Spreadshop).

Uso: python3 scripts/generar_disenos.py
Requiere Chromium (Playwright lo trae en /opt/pw-browsers), ImageMagick y las fuentes
Anton, Archivo Black, Permanent Marker, DM Serif Display y Bebas Neue (Google Fonts, licencia OFL).

Cada diseño sale en dos versiones:
  -oscuro.png → tinta oscura, para prendas claras (blanco, gris claro, arena)
  -claro.png  → tinta clara, para prendas oscuras (negro, azul marino, gris oscuro)
"""
import glob
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "tienda-camisetas" / "disenos"
CHROME = sorted(glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome"))[-1]
LADO_FINAL = 4000  # px del lado largo (requisito Spreadshop: ≥ 4000 px lado largo, PNG < 10 MB)

TINTAS = {
    "oscuro": {"tinta": "#1b1b1f", "acento": "#e8590c", "suave": "#55555c"},
    "claro": {"tinta": "#ffffff", "acento": "#ffb000", "suave": "#d6d6dc"},
}

# Cada diseño: líneas de texto. Clases: fit (ajusta al ancho), y estilos por fuente.
DISENOS = {
    "01-autonomo-todo-en-uno": """
<div class="fit anton" data-w="900">AUTÓNOMO</div>
<div class="fit bebas acento" data-w="900">JEFE · CONTABLE · BECARIO</div>
<div class="fit marker" data-w="620">y el que limpia</div>
""",
    "02-esto-desgrava": """
<div class="fit archivo" data-w="900">¿ESTO</div>
<div class="fit archivo acento" data-w="900">DESGRAVA?</div>
<div class="fit bebas suave" data-w="760">— TODO AUTÓNOMO, SIEMPRE</div>
""",
    "03-sobrevivi-al-trimestre": """
<div class="fit anton" data-w="900">SOBREVIVÍ</div>
<div class="fit anton" data-w="900">AL TRIMESTRE</div>
<div class="checks">
  <span><b>✔</b>1T</span><span><b>✔</b>2T</span><span><b>✔</b>3T</span><span><b>✔</b>4T</span>
</div>
""",
    "04-mi-jefe-es-un-explotador": """
<div class="fit archivo" data-w="900">MI JEFE ES UN</div>
<div class="fit archivo acento" data-w="900">EXPLOTADOR</div>
<div class="fit marker" data-w="620">(soy autónomo)</div>
""",
    "05-de-lunes-a-lunes": """
<div class="fit bebas suave" data-w="700">HORARIO DE AUTÓNOMO</div>
<div class="fit anton" data-w="900">DE LUNES</div>
<div class="fit anton acento" data-w="900">A LUNES</div>
""",
    "06-pago-a-90-dias": """
<div class="sello">
  <div class="fit anton" data-w="620">PAGO A</div>
  <div class="fit anton" data-w="620">90 DÍAS</div>
  <div class="fit bebas" data-w="520">Y LUEGO YA VEREMOS</div>
</div>
""",
    "07-hacienda-me-quiere": """
<div class="fit dm" data-w="900">Hacienda</div>
<div class="fit dm acento" data-w="900">me quiere</div>
<div class="fit marker" data-w="900">me lo demuestra cada tres meses</div>
""",
    "08-funciono-con-cafe": """
<svg class="icono" viewBox="0 0 100 80" width="300" height="240" aria-hidden="true">
  <path d="M28 6c-4 6 4 9 0 15M46 6c-4 6 4 9 0 15M64 6c-4 6 4 9 0 15" fill="none" stroke="var(--suave)" stroke-width="4" stroke-linecap="round"/>
  <path d="M12 28h64v22a24 24 0 0 1-24 24H36a24 24 0 0 1-24-24z" fill="var(--tinta)"/>
  <path d="M76 34h6a10 10 0 0 1 0 20h-7" fill="none" stroke="var(--tinta)" stroke-width="6"/>
</svg>
<div class="fit bebas" data-w="900">FUNCIONO CON CAFÉ</div>
<div class="fit anton acento" data-w="560">AL 21 %</div>
""",
    "09-nunca-de-baja": """
<div class="fit anton" data-w="900">NUNCA DE BAJA</div>
<div class="fit anton acento" data-w="900">SIEMPRE DE ALTA</div>
<div class="fit bebas suave" data-w="420">AUTÓNOMO</div>
""",
    "10-vacaciones-de-autonomo": """
<svg class="icono" viewBox="0 0 120 80" width="390" height="260" aria-hidden="true">
  <circle cx="92" cy="20" r="12" fill="var(--acento)"/>
  <rect x="22" y="22" width="56" height="36" rx="4" fill="none" stroke="var(--tinta)" stroke-width="6"/>
  <path d="M10 62h80l-6 8H16z" fill="var(--tinta)"/>
  <path d="M0 76c15-6 30-6 45 0s30 6 45 0 22-5 30-2" fill="none" stroke="var(--suave)" stroke-width="4"/>
</svg>
<div class="fit archivo" data-w="900">VACACIONES</div>
<div class="fit archivo" data-w="900">DE AUTÓNOMO</div>
<div class="fit marker acento" data-w="900">lo mismo, pero con arena</div>
""",
}

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
:root {{ --tinta:{tinta}; --acento:{acento}; --suave:{suave}; }}
html,body {{ margin:0; background:transparent; }}
body {{ width:1000px; height:1000px; display:flex; flex-direction:column; align-items:center;
       justify-content:center; gap:8px; color:var(--tinta); }}
.fit {{ white-space:nowrap; line-height:.95; }}
.anton {{ font-family:"Anton"; }}
.archivo {{ font-family:"Archivo Black"; letter-spacing:-.01em; }}
.bebas {{ font-family:"Bebas Neue"; letter-spacing:.04em; }}
.marker {{ font-family:"Permanent Marker"; line-height:1.2; }}
.dm {{ font-family:"DM Serif Display"; line-height:1.05; }}
.acento {{ color:var(--acento); }}
.suave {{ color:var(--suave); }}
.checks {{ display:flex; gap:38px; font-family:"Bebas Neue"; font-size:96px; margin-top:16px; }}
.checks b {{ color:var(--acento); margin-right:10px; }}
.sello {{ border:22px solid var(--acento); border-radius:40px; padding:40px 60px; transform:rotate(-8deg);
         display:flex; flex-direction:column; align-items:center; gap:6px; color:var(--acento); }}
.icono {{ margin-bottom:24px; }}
</style></head><body>{cuerpo}
<script>
for (const el of document.querySelectorAll('.fit')) {{
  el.style.fontSize = '100px';
  const w = el.getBoundingClientRect().width;
  el.style.fontSize = (100 * Number(el.dataset.w) / w) + 'px';
}}
</script></body></html>"""


def renderizar(html: str, destino: Path, tmp: Path):
    pagina = tmp / "d.html"
    pagina.write_text(html, encoding="utf-8")
    bruto = tmp / "bruto.png"
    subprocess.run(
        [CHROME, "--headless", "--no-sandbox", "--hide-scrollbars",
         "--default-background-color=00000000", "--window-size=1000,1000",
         "--force-device-scale-factor=5", f"--screenshot={bruto}", pagina.as_uri()],
        check=True, capture_output=True, timeout=120,
    )
    subprocess.run(
        ["convert", str(bruto), "-trim", "+repage",
         "-resize", f"{LADO_FINAL}x{LADO_FINAL}", "-strip", str(destino)],
        check=True,
    )


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for nombre, cuerpo in DISENOS.items():
            for variante, colores in TINTAS.items():
                destino = SALIDA / f"{nombre}-{variante}.png"
                renderizar(HTML.format(cuerpo=cuerpo, **colores), destino, tmp)
                print(destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
