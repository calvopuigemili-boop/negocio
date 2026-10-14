"""Genera las publicaciones de TikTok de «Modo Autónomo» en tiktok/.

Uso: python3 scripts/generar_tiktok.py
Por cada publicación crea una carpeta con:
  - slide-N.png  (1080x1920, para subir como carrusel de fotos)
  - video.mp4    (las mismas diapositivas con transición, sin sonido: el sonido se elige en TikTok)
y escribe todos los textos en tiktok/PUBLICACIONES.md.
"""
import html
import shutil
import subprocess
import tempfile
from pathlib import Path

from generar_disenos import CHROME

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "tiktok"
DISENOS = RAIZ / "tienda-camisetas" / "disenos"
LOGO = RAIZ / "tienda-camisetas" / "marca" / "logo.png"
SEGUNDOS = 2.8
FUNDIDO = 0.4

HASHTAGS_HUMOR = "#autonomos #autonomo #humorautonomos #freelance #emprendedores #españa"
HASHTAGS_TRUCO = "#autonomos #hacienda #iva #irpf #finanzaspersonales #freelance"

CTA_TIENDA = ("cta", "Camisetas y tazas para autónomos", "Link en el perfil 👆")
CTA_KIT = ("cta", "Plantilla que lo calcula sola", "Link en el perfil 👆")

# Cada publicación: (id, texto del pie, hashtags, diapositivas)
# Diapositivas: ("portada", gancho, subtítulo) · ("item", emoji, texto) · ("diseno", archivo, texto)
#               ("lista", título, [líneas]) · ("cta", título, subtítulo)
PUBLICACIONES = [
    ("01-cosas-que-solo-entiende-un-autonomo",
     "¿Cuántas te han pasado? 😅", HASHTAGS_HUMOR, [
         ("portada", "Cosas que solo entiende un autónomo", "Desliza 👉"),
         ("item", "💸", "Cobrar a 90 días… si hay suerte"),
         ("item", "🧾", "Pagar la cuota aunque ese mes factures 0 €"),
         ("item", "🛒", "Preguntar «¿esto desgrava?» hasta en el súper"),
         ("item", "🏖️", "Pedir vacaciones a tu jefe (y que te diga que no)"),
         ("diseno", "02-esto-desgrava", "¿Esto desgrava?"),
         CTA_TIENDA,
     ]),
    ("02-mi-horario-real",
     "Horario de autónomo: de lunes a lunes 🫠", HASHTAGS_HUMOR, [
         ("portada", "Mi horario real como autónomo", "Desliza 👉"),
         ("lista", "Semana tipo", ["Lunes: trabajo", "Martes: trabajo", "Miércoles: trabajo",
                                   "Jueves: trabajo", "Viernes: trabajo", "Sábado: «solo un ratito»",
                                   "Domingo: «solo un email»"]),
         ("diseno", "05-de-lunes-a-lunes", "De lunes a lunes"),
         CTA_TIENDA,
     ]),
    ("03-tipos-de-clientes",
     "¿Cuál es el tuyo? 👀", HASHTAGS_HUMOR, [
         ("portada", "Tipos de clientes que tiene todo autónomo", "Desliza 👉"),
         ("item", "🐌", "El que paga a 90 días"),
         ("item", "✏️", "El que quiere «un cambio pequeñito» (son 40)"),
         ("item", "🤫", "El que pregunta si puede ser sin factura"),
         ("item", "🦄", "El que paga el mismo día (leyenda urbana)"),
         ("diseno", "06-pago-a-90-dias", "Pago a 90 días… y luego ya veremos"),
         CTA_TIENDA,
     ]),
    ("04-vacaciones-de-autonomo",
     "El portátil también necesita playa 🏝️", HASHTAGS_HUMOR, [
         ("portada", "Vacaciones de autónomo", "Expectativa vs realidad 👉"),
         ("item", "🌴", "Expectativa: desconectar 15 días"),
         ("item", "💻", "Realidad: contestar emails desde la toalla"),
         ("diseno", "10-vacaciones-de-autonomo", "Lo mismo, pero con arena"),
         CTA_TIENDA,
     ]),
    ("05-pov-plazo-del-trimestre",
     "Un trimestre más superado 🫡", HASHTAGS_HUMOR, [
         ("portada", "POV: es día 20 y acabas de presentar el IVA", ""),
         ("item", "😮‍💨", "Respiras. Hasta dentro de tres meses."),
         ("diseno", "03-sobrevivi-al-trimestre", "Sobreviví al trimestre"),
         CTA_TIENDA,
     ]),
    ("06-organigrama-de-mi-empresa",
     "Plantilla de la empresa: 1 persona 😂", HASHTAGS_HUMOR, [
         ("portada", "El organigrama de mi empresa", "Desliza 👉"),
         ("lista", "Puestos", ["Director general: yo", "Contable: yo", "Comercial: yo",
                               "Becario: yo", "Limpieza: yo", "Atención al cliente: yo"]),
         ("diseno", "01-autonomo-todo-en-uno", "Jefe, contable, becario y el que limpia"),
         CTA_TIENDA,
     ]),
    ("07-mi-relacion-con-hacienda",
     "Una relación estable 💘", HASHTAGS_HUMOR, [
         ("portada", "Mi relación con Hacienda", "Desliza 👉"),
         ("item", "📅", "Me escribe cada tres meses"),
         ("item", "💌", "Nunca se olvida de mí"),
         ("item", "💶", "Siempre quiere algo"),
         ("diseno", "07-hacienda-me-quiere", "Hacienda me quiere"),
         CTA_TIENDA,
     ]),
    ("08-desgrava-segun-mi-cabeza",
     "Spoiler: el café no 😭 (info orientativa, consulta a tu gestor)", HASHTAGS_HUMOR, [
         ("portada", "¿Desgrava? Mi cabeza vs Hacienda", "Desliza 👉"),
         ("item", "❌", "El café de la mañana en el bar de abajo"),
         ("item", "❌", "Netflix «para inspirarme»"),
         ("item", "✅", "La cuota de autónomos"),
         ("item", "✅", "La gestoría y el software que usas para trabajar"),
         ("diseno", "08-funciono-con-cafe", "Funciono con café al 21 %"),
         CTA_TIENDA,
     ]),
    ("09-calcular-modelo-303",
     "Guárdalo para el próximo trimestre 📌 Info orientativa.", HASHTAGS_TRUCO, [
         ("portada", "Cómo calcular el IVA trimestral (Modelo 303) en 3 pasos", "Guárdalo 📌"),
         ("item", "1️⃣", "Suma el IVA de las facturas que has emitido en el trimestre"),
         ("item", "2️⃣", "Suma el IVA de tus gastos del negocio (con factura a tu nombre)"),
         ("item", "3️⃣", "Resta: lo primero menos lo segundo. Eso es lo que pagas"),
         ("lista", "Ejemplo", ["Facturas: 6.000 € + 1.260 € IVA", "Gastos: 1.000 € + 210 € IVA",
                               "A pagar: 1.260 − 210 = 1.050 €"]),
         CTA_KIT,
     ]),
    ("10-calcular-modelo-130",
     "El error más común: calcular solo el trimestre 👀 Info orientativa.", HASHTAGS_TRUCO, [
         ("portada", "Cómo calcular el Modelo 130 (IRPF) sin gestor", "Guárdalo 📌"),
         ("item", "1️⃣", "Ingresos menos gastos desde el 1 de enero (sin IVA)"),
         ("item", "2️⃣", "Calcula el 20 % de ese resultado"),
         ("item", "3️⃣", "Resta las retenciones que te han hecho en el año"),
         ("item", "4️⃣", "Resta lo que ya pagaste en los 130 anteriores"),
         CTA_KIT,
     ]),
    ("11-cuanto-apartar-cada-mes",
     "La regla que me salvó de los sustos 🙏 Info orientativa.", HASHTAGS_TRUCO, [
         ("portada", "Cuánto apartar cada mes para Hacienda", "Siendo autónomo 👉"),
         ("item", "🧾", "Todo el IVA que cobras: no es tuyo"),
         ("item", "📊", "Un 20 % del beneficio para el IRPF trimestral"),
         ("item", "🛟", "Un 5-10 % extra de colchón para la renta"),
         ("item", "🏦", "Todo en una cuenta aparte que no tocas"),
         CTA_KIT,
     ]),
    ("12-gastos-que-no-sabias-que-desgravan",
     "¿Conocías el 5 %? Info orientativa, consulta a tu gestor.", HASHTAGS_TRUCO, [
         ("portada", "5 gastos que puedes deducir como autónomo", "Y no sabías 👉"),
         ("item", "🩺", "Seguro médico: hasta 500 € al año por persona"),
         ("item", "🏠", "Luz, agua e internet si trabajas en casa (30 % de la parte afecta)"),
         ("item", "🍽️", "Comidas de trabajo fuera: hasta 26,67 € al día en España"),
         ("item", "🏦", "Comisiones del banco de la cuenta del negocio"),
         ("item", "🎁", "Un 5 % del beneficio sin facturas (máx. 2.000 €/año) en estimación directa simplificada"),
         CTA_KIT,
     ]),
    ("13-plazos-2027",
     "Ponlo en el calendario 🗓️", HASHTAGS_TRUCO, [
         ("portada", "Fechas de IVA e IRPF para autónomos en 2027", "Guárdalo 📌"),
         ("lista", "Plazos 303 y 130", ["4T 2026: hasta el 1 de febrero", "1T: del 1 al 20 de abril",
                                        "2T: del 1 al 20 de julio", "3T: del 1 al 20 de octubre",
                                        "4T 2027: hasta el 31 de enero de 2028"]),
         CTA_KIT,
     ]),
    ("14-elige-tu-favorita",
     "¿Con cuál te quedas? 👇", HASHTAGS_HUMOR + " #regalo #regalooriginal", [
         ("portada", "Camisetas para autónomos", "¿Cuál es la tuya? 👉"),
         ("diseno", "02-esto-desgrava", "1. ¿Esto desgrava?"),
         ("diseno", "07-hacienda-me-quiere", "2. Hacienda me quiere"),
         ("diseno", "04-mi-jefe-es-un-explotador", "3. Mi jefe es un explotador"),
         ("diseno", "09-nunca-de-baja", "4. Nunca de baja"),
         CTA_TIENDA,
     ]),
]

CSS = """
html,body{margin:0}
body{width:1080px;height:1920px;background:#1d2733;color:#fff;font-family:"Archivo Black";
     position:relative;overflow:hidden}
.marca{position:absolute;top:120px;left:0;right:0;text-align:center;font-family:"Bebas Neue";
       font-size:46px;letter-spacing:.12em;color:#ffb000}
.zona{position:absolute;top:240px;left:90px;right:150px;bottom:480px;display:flex;
      flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:48px}
.gancho{font-family:"Anton";font-size:132px;line-height:1.18;text-transform:uppercase}
.sub{font-family:"Bebas Neue";font-size:72px;letter-spacing:.06em;color:#ffb000}
.emoji{font-size:220px;line-height:1}
.texto{font-size:78px;line-height:1.2}
.titulo{font-family:"Anton";font-size:110px;color:#ffb000;text-transform:uppercase}
ul{list-style:none;margin:0;padding:0;text-align:left;font-size:60px;line-height:1.55}
.camiseta{position:relative;width:760px;height:836px}
.camiseta img{position:absolute;left:50%;top:250px;transform:translateX(-50%);max-width:300px;max-height:330px}
.logo{width:420px;border-radius:40px}
"""

CAMISETA = """<svg viewBox="0 0 400 440" width="760" height="836" aria-hidden="true">
<path d="M135 22 Q200 62 265 22 L372 74 L338 168 L302 152 L302 426 L98 426 L98 152 L62 168 L28 74 Z"
 fill="#f2f0eb"/><path d="M135 22 Q200 62 265 22" fill="none" stroke="#d8d4cb" stroke-width="6"/></svg>"""


def cuerpo_diapositiva(d):
    tipo = d[0]
    e = html.escape
    if tipo == "portada":
        sub = f'<div class="sub">{e(d[2])}</div>' if d[2] else ""
        return f'<div class="gancho">{e(d[1])}</div>{sub}'
    if tipo == "item":
        return f'<div class="emoji">{d[1]}</div><div class="texto">{e(d[2])}</div>'
    if tipo == "lista":
        items = "".join(f"<li>{e(x)}</li>" for x in d[2])
        return f'<div class="titulo">{e(d[1])}</div><ul>{items}</ul>'
    if tipo == "diseno":
        png = (DISENOS / f"{d[1]}-oscuro.png").as_uri()
        return f'<div class="camiseta">{CAMISETA}<img src="{png}"></div><div class="texto">{e(d[2])}</div>'
    if tipo == "cta":
        return (f'<img class="logo" src="{LOGO.as_uri()}"><div class="gancho" style="font-size:100px">'
                f'{e(d[1])}</div><div class="sub">{e(d[2])}</div>')
    raise ValueError(tipo)


def renderizar(diapositiva, destino: Path, tmp: Path):
    pagina = tmp / "s.html"
    pagina.write_text(
        f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>'
        f'<div class="marca">@MODOAUTONOMO</div><div class="zona">{cuerpo_diapositiva(diapositiva)}</div>',
        encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--window-size=1080,1920", f"--screenshot={destino}", pagina.as_uri()],
                   check=True, capture_output=True, timeout=120)


def video(slides, destino: Path):
    entradas, filtros = [], []
    for s in slides:
        entradas += ["-loop", "1", "-t", str(SEGUNDOS), "-i", str(s)]
    for i in range(len(slides)):
        filtros.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v{i}]")
    previo, desfase = "v0", 0.0
    for i in range(1, len(slides)):
        desfase += SEGUNDOS - FUNDIDO
        filtros.append(f"[{previo}][v{i}]xfade=transition=slideleft:duration={FUNDIDO}:offset={desfase:.2f}[x{i}]")
        previo = f"x{i}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", ";".join(filtros),
                    "-map", f"[{previo}]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(destino)], check=True)


def main():
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir()
    textos = ["# Publicaciones de TikTok (copiar y pegar)\n",
              "Cada carpeta tiene las imágenes (carrusel) y `video.mp4`. Sube **una de las dos cosas**.",
              "Elige el sonido dentro de TikTok (uno que esté en tendencia).\n"]
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for ident, pie, hashtags, diapositivas in PUBLICACIONES:
            carpeta = SALIDA / ident
            carpeta.mkdir()
            slides = []
            for n, d in enumerate(diapositivas, 1):
                destino = carpeta / f"slide-{n}.png"
                renderizar(d, destino, tmp)
                slides.append(destino)
            video(slides, carpeta / "video.mp4")
            textos.append(f"## {ident}\n\n```\n{pie}\n\n{hashtags}\n```\n")
            print(ident)
    (SALIDA / "PUBLICACIONES.md").write_text("\n".join(textos), encoding="utf-8")


if __name__ == "__main__":
    main()
