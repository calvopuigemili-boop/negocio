# Kit Autónomo — negocio de producto digital con inversión 0 €

> 👉 **Empieza por [EMPIEZA-AQUI.md](EMPIEZA-AQUI.md)**: plan adaptado (Payhip + PayPal, 10 min/día).

Plantilla de hoja de cálculo para autónomos españoles (facturas, gastos, Modelo 303 y Modelo 130)
que se vende en Gumroad a 9 €. Análisis completo en [ANALISIS.md](ANALISIS.md).

## Contenido

| Ruta | Qué es |
|---|---|
| `producto/Kit-Autonomo-2027.xlsx` | **El producto que se vende** |
| `scripts/generar_kit.py` | Regenera el producto (`python3 scripts/generar_kit.py`, requiere `openpyxl`) |
| `docs/index.html` | Web de venta, lista para GitHub Pages |
| `marketing/ficha-gumroad.md` | Texto de la ficha del producto en Gumroad |
| `marketing/publicaciones.md` | Posts para LinkedIn, X, TikTok, Reddit y grupos |

## Para empezar a vender (≈ 30 minutos)

1. Crea una cuenta gratuita en [gumroad.com](https://gumroad.com) y conecta tu cuenta bancaria.
2. Nuevo producto → «Digital product» → sube `producto/Kit-Autonomo-2027.xlsx`,
   pega el texto de `marketing/ficha-gumroad.md` y pon el precio en 9 €.
3. Sustituye `https://TU-USUARIO.gumroad.com/l/kit-autonomo` en `docs/index.html` por tu enlace real.
4. En GitHub: Settings → Pages → Branch: tu rama, carpeta `/docs` → Save.
5. Publica los posts de `marketing/publicaciones.md` (1-2 al día) hasta el 20 de octubre.

---

# Negocio 2 (descartado por ahora): tienda Shopify «Huella & Co.»

> No encaja con el objetivo de bajo mantenimiento (pedidos, devoluciones, vídeos diarios). Se conserva como referencia.

Todo en [`tienda-mascotas/`](tienda-mascotas/):

| Archivo | Qué es |
|---|---|
| `1-ESTUDIO-NICHOS.md` | Comparativa de 6 nichos y por qué gana mascotas |
| `2-PROVEEDOR-Y-PRODUCTOS.md` | CJdropshipping (gratis), los 12 productos, precios y números |
| `3-PLAN-MARKETING.md` | Plan 100 % orgánico: 30 días de vídeos, mensajes para influencers y protectoras, SEO y email |
| `4-CHECKLIST-TIENDA.md` | Qué está hecho en Shopify y qué te falta (≈1 hora) |
| `5-POLITICAS-LEGALES.md` | Textos legales para pegar en Shopify |
| `logo-huella.png` / `.svg` | Logo |

---

# Negocio 3: «Modo Autónomo» — camisetas y tazas bajo demanda (Spreadshop, 0 €)

Todo en [`tienda-camisetas/`](tienda-camisetas/). Empieza por
[`tienda-camisetas/EMPIEZA-AQUI.md`](tienda-camisetas/EMPIEZA-AQUI.md).
Diseños regenerables con `python3 scripts/generar_disenos.py` y `python3 scripts/generar_marca.py`.
