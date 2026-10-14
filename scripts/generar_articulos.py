"""Genera los artículos SEO de docs/ (GitHub Pages), el sitemap y robots.txt.

Uso: python3 scripts/generar_articulos.py
Cada artículo responde una búsqueda frecuente de autónomos y enlaza al Kit en Payhip.
"""
from pathlib import Path

BASE = "https://calvopuigemili-boop.github.io/negocio/"
COMPRA = "https://payhip.com/b/OPcw6"
DOCS = Path(__file__).resolve().parent.parent / "docs"

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="canonical" href="{base}{archivo}">
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<nav class="wrap"><a href="index.html">Kit Autónomo</a> · <a href="guias.html">Guías</a></nav>
<article class="wrap">
<h1>{h1}</h1>
{cuerpo}
<aside class="caja">
  <strong>¿Quieres que se calcule solo?</strong>
  <p>El <strong>Kit Autónomo</strong> es una hoja de cálculo donde apuntas facturas y gastos y
  te calcula el Modelo 303 y el Modelo 130 de cada trimestre. Pago único de 9 €.</p>
  <a class="btn" href="{compra}">Ver el Kit Autónomo</a>
</aside>
<p class="nota">Información general y orientativa, actualizada en octubre de 2026. No sustituye
el asesoramiento de un profesional ni la normativa de la Agencia Tributaria.</p>
</article>
<footer class="wrap"><a href="guias.html">Más guías para autónomos</a></footer>
</body>
</html>
"""

ARTICULOS = [
    {
        "archivo": "como-calcular-modelo-130.html",
        "titulo": "Cómo calcular el Modelo 130 paso a paso (con ejemplo)",
        "h1": "Cómo calcular el Modelo 130 paso a paso",
        "descripcion": "Fórmula del Modelo 130 explicada con un ejemplo: 20 % del rendimiento acumulado, retenciones y pagos anteriores. Quién está exento.",
        "cuerpo": """
<p>El Modelo 130 es el <strong>pago a cuenta del IRPF</strong> que hacen cada trimestre los
autónomos en estimación directa. Es un adelanto de lo que pagarás en la declaración de la renta.</p>

<h2>La fórmula</h2>
<ol>
  <li>Suma tus <strong>ingresos</strong> desde el 1 de enero hasta el final del trimestre (sin IVA).</li>
  <li>Resta tus <strong>gastos deducibles</strong> del mismo periodo (sin IVA deducible). El resultado es el <strong>rendimiento neto acumulado</strong>.</li>
  <li>Calcula el <strong>20 %</strong> de ese rendimiento.</li>
  <li>Resta las <strong>retenciones</strong> que te han practicado tus clientes en el año (el 15 % o 7 % de tus facturas).</li>
  <li>Resta lo que ya pagaste en los <strong>130 de trimestres anteriores</strong> del mismo año.</li>
</ol>
<p>Si el resultado es positivo, eso es lo que pagas. Si es negativo, pones 0 (no te devuelven nada hasta la renta).</p>

<h2>Ejemplo</h2>
<table>
<tr><th>Concepto (1 de enero a 30 de junio)</th><th>Importe</th></tr>
<tr><td>Ingresos acumulados</td><td>12.000 €</td></tr>
<tr><td>Gastos deducibles acumulados</td><td>3.000 €</td></tr>
<tr><td>Rendimiento neto</td><td>9.000 €</td></tr>
<tr><td>20 % del rendimiento</td><td>1.800 €</td></tr>
<tr><td>Retenciones de clientes en el año</td><td>−600 €</td></tr>
<tr><td>Pagado en el 130 del primer trimestre</td><td>−500 €</td></tr>
<tr><td><strong>Resultado del segundo trimestre</strong></td><td><strong>700 €</strong></td></tr>
</table>

<h2>¿Quién no tiene que presentarlo?</h2>
<p>Si en el año anterior <strong>al menos el 70 % de tus ingresos</strong> llevaron retención
(trabajas sobre todo para empresas que te retienen), no estás obligado a presentar el 130.
Tampoco lo presentan quienes tributan por módulos (que usan el Modelo 131).</p>

<h2>Errores frecuentes</h2>
<ul>
  <li><strong>Calcular solo el trimestre.</strong> El 130 es acumulativo: siempre desde el 1 de enero.</li>
  <li><strong>Incluir el IVA</strong> en ingresos o gastos. El IVA va en el Modelo 303, no aquí.</li>
  <li><strong>Olvidar restar los pagos anteriores</strong>, con lo que pagarías dos veces.</li>
</ul>
<p>Los plazos son del 1 al 20 de abril, julio y octubre, y del 1 al 30 de enero.
Mira el <a href="plazos-modelo-303-130.html">calendario completo</a>.</p>
""",
    },
    {
        "archivo": "como-calcular-modelo-303.html",
        "titulo": "Cómo calcular el Modelo 303 de IVA trimestral (con ejemplo)",
        "h1": "Cómo calcular el Modelo 303 (IVA trimestral)",
        "descripcion": "Cómo se calcula el Modelo 303: IVA repercutido menos IVA soportado, con ejemplo, qué pasa si sale negativo y qué gastos permiten deducir IVA.",
        "cuerpo": """
<p>El Modelo 303 es la <strong>declaración trimestral del IVA</strong>. El IVA que cobras en tus
facturas no es tuyo: lo recaudas para Hacienda y cada trimestre lo ingresas, restando el IVA que
tú has pagado en los gastos de tu actividad.</p>

<h2>La fórmula</h2>
<p><strong>Resultado = IVA repercutido − IVA soportado deducible</strong></p>
<ul>
  <li><strong>IVA repercutido:</strong> el IVA de las facturas que has emitido en el trimestre.</li>
  <li><strong>IVA soportado deducible:</strong> el IVA de las facturas de gastos de tu actividad en el trimestre (con factura a tu nombre y NIF).</li>
</ul>
<p>A diferencia del 130, el 303 <strong>no es acumulativo</strong>: cada trimestre va por separado.</p>

<h2>Ejemplo</h2>
<table>
<tr><th>Concepto (un trimestre)</th><th>Base</th><th>IVA 21 %</th></tr>
<tr><td>Facturas emitidas</td><td>6.000 €</td><td>1.260 €</td></tr>
<tr><td>Gastos con IVA</td><td>1.000 €</td><td>210 €</td></tr>
<tr><td colspan="2"><strong>A pagar en el 303</strong></td><td><strong>1.050 €</strong></td></tr>
</table>

<h2>¿Y si sale negativo?</h2>
<p>Si has pagado más IVA del que has cobrado, el resultado es "a compensar": lo restas en los
trimestres siguientes. En el <strong>cuarto trimestre</strong> puedes elegir pedir la devolución.</p>

<h2>Gastos cuyo IVA no puedes deducir (o solo en parte)</h2>
<ul>
  <li>Gastos personales o sin factura completa (un ticket simplificado sin tus datos no vale).</li>
  <li>Vehículo: Hacienda presume un uso afecto del 50 %, así que normalmente deduces la mitad del IVA.</li>
  <li>Comidas, regalos y atenciones a clientes: su IVA, en general, no es deducible.</li>
</ul>

<h2>Casos especiales</h2>
<p>Si facturas a clientes de otros países de la UE, haces operaciones con inversión del sujeto
pasivo o tu actividad está exenta de IVA (por ejemplo, algunas sanitarias o de formación), el
cálculo cambia. Consulta con un asesor.</p>
<p>Plazos: <a href="plazos-modelo-303-130.html">calendario del 303 y el 130</a>.</p>
""",
    },
    {
        "archivo": "plazos-modelo-303-130.html",
        "titulo": "Plazos del Modelo 303 y 130 en 2027: calendario del autónomo",
        "h1": "Plazos del Modelo 303 y 130: calendario 2027",
        "descripcion": "Fechas para presentar el Modelo 303 (IVA) y el Modelo 130 (IRPF) en 2027, trimestre a trimestre, y qué pasa si te retrasas.",
        "cuerpo": """
<p>El Modelo 303 (IVA) y el Modelo 130 (IRPF) se presentan <strong>en las mismas fechas</strong>,
cuatro veces al año.</p>

<table>
<tr><th>Trimestre</th><th>Periodo que declaras</th><th>Plazo</th></tr>
<tr><td>4T 2026</td><td>octubre-diciembre 2026</td><td>del 1 de enero al <strong>1 de febrero de 2027</strong> (el 30 de enero cae en sábado)</td></tr>
<tr><td>1T 2027</td><td>enero-marzo</td><td>del 1 al <strong>20 de abril de 2027</strong></td></tr>
<tr><td>2T 2027</td><td>abril-junio</td><td>del 1 al <strong>20 de julio de 2027</strong></td></tr>
<tr><td>3T 2027</td><td>julio-septiembre</td><td>del 1 al <strong>20 de octubre de 2027</strong></td></tr>
<tr><td>4T 2027</td><td>octubre-diciembre</td><td>del 1 al <strong>31 de enero de 2028</strong> (el 30 cae en domingo)</td></tr>
</table>
<p>Si el último día cae en sábado, domingo o festivo nacional, el plazo pasa al siguiente día
hábil. Si pagas por <strong>domiciliación bancaria</strong>, el plazo termina unos días antes;
comprueba la fecha exacta en la sede de la Agencia Tributaria.</p>

<h2>¿Qué pasa si presento tarde?</h2>
<p>Si lo presentas fuera de plazo por tu cuenta (sin requerimiento de Hacienda), pagas un
<strong>recargo</strong> que crece con el retraso: 1 % más un 1 % adicional por cada mes completo
durante el primer año. Si Hacienda te lo reclama antes, la sanción es mayor. Presentar a tiempo,
aunque sea con resultado 0, siempre sale más barato.</p>

<h2>Cómo llegar al plazo sin sustos</h2>
<ul>
  <li>Apunta cada factura y cada gasto el mismo día.</li>
  <li>Aparta cada mes el IVA cobrado y alrededor de un 20 % del beneficio en otra cuenta. Lo explicamos en <a href="cuanto-apartar-impuestos-autonomo.html">cuánto apartar para impuestos</a>.</li>
  <li>Calcula una estimación antes del día 1 de cada plazo: <a href="como-calcular-modelo-303.html">303</a> y <a href="como-calcular-modelo-130.html">130</a>.</li>
</ul>
""",
    },
    {
        "archivo": "gastos-deducibles-autonomos.html",
        "titulo": "Gastos deducibles del autónomo: lista completa y límites",
        "h1": "Gastos deducibles para autónomos: lista y límites",
        "descripcion": "Qué gastos puede deducir un autónomo en estimación directa: cuota, suministros de casa, dietas, seguro médico, vehículo y más, con sus límites.",
        "cuerpo": """
<p>Un gasto es deducible si está <strong>relacionado con tu actividad</strong>, tiene
<strong>factura a tu nombre</strong> y está <strong>registrado</strong> en tu libro de gastos.
Estos son los más habituales en estimación directa.</p>

<h2>Deducibles al 100 %</h2>
<ul>
  <li>Cuota de autónomos de la Seguridad Social.</li>
  <li>Gestoría o asesoría.</li>
  <li>Software, suscripciones y herramientas de trabajo.</li>
  <li>Publicidad, dominio y web.</li>
  <li>Alquiler de un local u oficina dedicado a la actividad.</li>
  <li>Formación relacionada con tu actividad.</li>
  <li>Seguro de responsabilidad civil profesional.</li>
  <li>Comisiones bancarias de la cuenta que usas para el negocio.</li>
</ul>

<h2>Deducibles con límites</h2>
<table>
<tr><th>Gasto</th><th>Regla</th></tr>
<tr><td>Suministros si trabajas en casa (luz, agua, gas, internet)</td><td>30 % de la parte proporcional a los metros que dedicas a la actividad (y debes haberlo declarado a Hacienda).</td></tr>
<tr><td>Seguro de salud</td><td>Hasta 500 € al año por ti, tu cónyuge e hijos menores de 25 que convivan contigo (1.500 € con discapacidad).</td></tr>
<tr><td>Dietas de manutención</td><td>En España, hasta 26,67 € al día (53,34 € si pernoctas); en el extranjero, 48,08 € (91,35 €). Pago con tarjeta en restaurante, en un municipio distinto al de tu residencia y del de tu lugar de trabajo.</td></tr>
<tr><td>Teléfono móvil</td><td>La parte que corresponda al uso profesional.</td></tr>
<tr><td>Vehículo</td><td>En IRPF solo si el uso es exclusivo para la actividad (salvo comerciales, transportistas y similares). Del IVA se suele deducir el 50 %.</td></tr>
<tr><td>Ordenadores y equipos caros</td><td>Por norma general se amortizan en varios años.</td></tr>
</table>

<h2>El 5 % de gastos de difícil justificación</h2>
<p>En estimación directa simplificada puedes deducir además un <strong>5 % de tu rendimiento
neto</strong>, con un máximo de <strong>2.000 € al año</strong>, sin necesidad de facturas.</p>

<h2>No deducibles</h2>
<ul>
  <li>Multas y sanciones.</li>
  <li>El propio IRPF.</li>
  <li>Gastos personales o familiares, aunque los pagues con la tarjeta del negocio.</li>
  <li>Gastos sin factura completa.</li>
</ul>
<p>Cómo influyen en lo que pagas: <a href="como-calcular-modelo-130.html">Modelo 130</a> y
<a href="como-calcular-modelo-303.html">Modelo 303</a>.</p>
""",
    },
    {
        "archivo": "cuanto-apartar-impuestos-autonomo.html",
        "titulo": "¿Cuánto debe apartar un autónomo para impuestos cada mes?",
        "h1": "¿Cuánto dinero apartar cada mes para impuestos?",
        "descripcion": "Regla sencilla para que el autónomo no se quede sin dinero al pagar el 303 y el 130: qué porcentaje apartar de cada factura, con ejemplo.",
        "cuerpo": """
<p>El error más común del autónomo que empieza es <strong>gastarse el dinero de Hacienda</strong>
y llegar al trimestre sin saldo. La solución es una cuenta separada y una regla fija.</p>

<h2>La regla</h2>
<p>Cada vez que cobres una factura, pasa a una cuenta aparte:</p>
<ol>
  <li><strong>Todo el IVA</strong> de la factura (el 21 % de la base). No es tuyo.</li>
  <li><strong>Un 20 % del beneficio</strong> (base menos gastos) para el Modelo 130, menos lo que ya te haya retenido el cliente.</li>
  <li><strong>Un colchón del 5-10 %</strong> extra para la declaración de la renta, porque el 20 % del 130 suele quedarse corto si ganas más de unos 20.000-25.000 € al año.</li>
</ol>

<h2>Ejemplo</h2>
<p>Facturas 2.000 € + IVA a un particular (sin retención) y ese mes tienes 400 € de gastos:</p>
<table>
<tr><th>Concepto</th><th>Apartar</th></tr>
<tr><td>IVA cobrado (21 % de 2.000 €)</td><td>420 €</td></tr>
<tr><td>IRPF: 20 % de (2.000 − 400)</td><td>320 €</td></tr>
<tr><td>Colchón renta (≈ 5 % del beneficio)</td><td>80 €</td></tr>
<tr><td><strong>Total a apartar</strong></td><td><strong>820 €</strong></td></tr>
</table>
<p>Del IVA que apartas, recuperas el IVA de tus gastos al presentar el 303, así que lo que sobre
al final del trimestre vuelve a ser tuyo.</p>

<h2>¿Y si facturo a empresas con retención?</h2>
<p>Si tu cliente te retiene un 15 % (o un 7 % los primeros años), Hacienda ya ha cobrado parte
de tu IRPF. En ese caso suele bastar con apartar el IVA y el colchón. Haz el cálculo exacto con la
<a href="como-calcular-modelo-130.html">fórmula del 130</a>.</p>
""",
    },
    {
        "archivo": "plantilla-excel-autonomos.html",
        "titulo": "Plantilla Excel para autónomos: facturas, gastos, IVA e IRPF",
        "h1": "Plantilla Excel para autónomos: qué debe incluir",
        "descripcion": "Qué debe tener una buena plantilla de Excel para autónomos: libro de ingresos y gastos, cálculo del 303 y 130 y generador de facturas.",
        "cuerpo": """
<p>Si emites pocas facturas al mes, un programa de facturación de 10-30 € al mes es demasiado.
Una hoja de cálculo bien hecha cubre lo mismo. Esto es lo mínimo que debe tener.</p>

<h2>1. Libro de ingresos</h2>
<p>Fecha, número de factura, cliente y NIF, base imponible, IVA, retención de IRPF y total. La
numeración debe ser <strong>correlativa</strong> (sin saltos), como exige la normativa.</p>

<h2>2. Libro de gastos</h2>
<p>Fecha, proveedor, base, IVA y, muy importante, el <strong>porcentaje deducible</strong> de cada
gasto (no todo se deduce al 100 %; mira la <a href="gastos-deducibles-autonomos.html">lista de gastos deducibles</a>).</p>

<h2>3. Cálculo trimestral automático</h2>
<p>Que te diga, sin hacer cuentas, cuánto sale el <a href="como-calcular-modelo-303.html">Modelo 303</a>
y el <a href="como-calcular-modelo-130.html">Modelo 130</a> de cada trimestre. Ahí es donde fallan
la mayoría de plantillas gratuitas: solo registran, no calculan.</p>

<h2>4. Generador de facturas</h2>
<p>Una hoja que, a partir del número de factura, rellene los datos y quede lista para exportar
a PDF con todos los datos obligatorios.</p>

<h2>5. Resumen</h2>
<p>Ingresos, gastos y beneficio por mes, y qué facturas tienes pendientes de cobro.</p>

<h2>La nuestra</h2>
<p>El <strong>Kit Autónomo</strong> incluye todo lo anterior, funciona en Excel, Google Sheets y
LibreOffice, y cuesta 9 € una sola vez. Ojo: no cubre módulos, recargo de equivalencia ni
operaciones intracomunitarias.</p>
""",
    },
]


def main():
    for a in ARTICULOS:
        html = PLANTILLA.format(base=BASE, compra=COMPRA, **a)
        (DOCS / a["archivo"]).write_text(html, encoding="utf-8")

    enlaces = "\n".join(
        f'  <li><a href="{a["archivo"]}">{a["h1"]}</a><br><span>{a["descripcion"]}</span></li>'
        for a in ARTICULOS
    )
    indice = PLANTILLA.format(
        base=BASE, compra=COMPRA, archivo="guias.html",
        titulo="Guías para autónomos: IVA, IRPF y gastos",
        h1="Guías para autónomos",
        descripcion="Guías claras para autónomos en España: Modelo 303, Modelo 130, plazos, gastos deducibles y cuánto apartar para impuestos.",
        cuerpo=f'<ul class="lista">\n{enlaces}\n</ul>',
    )
    (DOCS / "guias.html").write_text(indice, encoding="utf-8")

    urls = ["", "guias.html"] + [a["archivo"] for a in ARTICULOS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls)
    sitemap += "</urlset>\n"
    (DOCS / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    print(f"{len(ARTICULOS)} artículos + guias.html + sitemap.xml + robots.txt en {DOCS}")


if __name__ == "__main__":
    main()
