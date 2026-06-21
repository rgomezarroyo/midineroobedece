from flask import Flask, render_template, Response, jsonify
from datetime import date, datetime, timedelta
import requests, threading

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# ── MOTOR DE TASAS (Bancos Centrales, refresh mensual) ──
_RATES_FALLBACK = {
    'USD': {'lending': 15.79, 'deposit': 5.59,  'inflation':   2.6,  'source': 'BCE Ecuador', 'year': 'abr 2026'},
    'MXN': {'lending': 28.0,  'deposit': 6.54,  'inflation':   4.45, 'source': 'Banxico',     'year': 'mayo 2026'},
    'GTQ': {'lending': 16.0,  'deposit': 5.0,   'inflation':   2.85, 'source': 'Banguat',     'year': 'mayo 2026'},
    'HNL': {'lending': 13.71, 'deposit': 7.32,  'inflation':   5.56, 'source': 'BCH',         'year': 'abr 2026'},
    'SVC': {'lending': 11.0,  'deposit': 3.5,   'inflation':   2.2,  'source': 'BCR El Salvador', 'year': 'abr 2026'},
    'NIO': {'lending': 15.0,  'deposit': 4.0,   'inflation':   3.72, 'source': 'BCN',         'year': 'mayo 2026'},
    'CRC': {'lending': 16.0,  'deposit': 3.65,  'inflation':  -2.7,  'source': 'BCCR',        'year': 'feb 2026'},
    'PAB': {'lending':  9.5,  'deposit': 3.5,   'inflation':  -0.2,  'source': 'SBP Panama',  'year': 'dic 2025'},
    'DOP': {'lending': 13.28, 'deposit': 6.28,  'inflation':   5.11, 'source': 'BCRD',        'year': 'abr 2026'},
    'COP': {'lending': 20.0,  'deposit': 7.5,   'inflation':   5.84, 'source': 'Banrep',      'year': 'mayo 2026'},
    'VES': {'lending': 30.0,  'deposit': 10.0,  'inflation': 130.0,  'source': 'BCV',         'year': 'jun 2025'},
    'CUP': {'lending': 12.0,  'deposit': 3.0,   'inflation':  25.0,  'source': 'BCC Cuba',    'year': 'jun 2025'},
    'PEN': {'lending': 14.0,  'deposit': 4.0,   'inflation':   4.0,  'source': 'BCRP',        'year': 'abr 2026'},
    'BOB': {'lending':  8.0,  'deposit': 2.5,   'inflation':  12.51, 'source': 'BCB Bolivia', 'year': 'mayo 2026'},
    'BRL': {'lending': 44.0,  'deposit': 13.75, 'inflation':   5.5,  'source': 'BCB Brasil',  'year': 'jun 2025'},
    'CLP': {'lending': 13.0,  'deposit': 5.0,   'inflation':   3.9,  'source': 'BCCh',        'year': 'mayo 2026'},
    'ARS': {'lending': 55.0,  'deposit': 29.5,  'inflation':  32.4,  'source': 'BCRA',        'year': 'mayo 2026'},
    'UYU': {'lending': 18.0,  'deposit': 8.0,   'inflation':   3.77, 'source': 'BCU',         'year': 'mayo 2026'},
    'PYG': {'lending': 16.0,  'deposit': 6.0,   'inflation':   4.5,  'source': 'BCP',         'year': 'jun 2025'},
}
# Nota (21 jun 2026): refresco manual con datos reales investigados (sin API gratuita para la mayoria
# de bancos centrales de LATAM). Venezuela, Cuba y Paraguay quedaron SIN tocar a proposito -- la
# investigacion no encontro datos oficiales confiables/recientes para esos 3 (Venezuela y Cuba tienen
# series de tasas/inflacion ampliamente cuestionadas, Paraguay solo tenia una proyeccion, no una medicion).
# Mexico y Colombia tampoco actualizaron su 'lending': lo unico disponible era la tasa de politica
# monetaria, que no equivale a la tasa de credito al consumo que mide este campo. Repetir este proceso
# cada 6-12 meses; no hay forma de automatizarlo salvo para Brasil (ya cubierto por _bcb_get arriba).

_COUNTRY_META = {
    'USD': {'name': 'Ecuador',          'flag': 'ec', 'symbol': '$',    'note': 'Dolarizado'},
    'MXN': {'name': 'Mexico',           'flag': 'mx', 'symbol': '$',    'note': ''},
    'GTQ': {'name': 'Guatemala',        'flag': 'gt', 'symbol': 'Q',    'note': ''},
    'HNL': {'name': 'Honduras',         'flag': 'hn', 'symbol': 'L',    'note': ''},
    'SVC': {'name': 'El Salvador',      'flag': 'sv', 'symbol': '$',    'note': 'Dolarizado'},
    'NIO': {'name': 'Nicaragua',        'flag': 'ni', 'symbol': 'C$',   'note': ''},
    'CRC': {'name': 'Costa Rica',       'flag': 'cr', 'symbol': '₡',    'note': ''},
    'PAB': {'name': 'Panama',           'flag': 'pa', 'symbol': 'B/.', 'note': 'Dolarizado'},
    'DOP': {'name': 'Rep. Dominicana',  'flag': 'do', 'symbol': 'RD$',  'note': ''},
    'CUP': {'name': 'Cuba',             'flag': 'cu', 'symbol': '$',    'note': 'Dato oficial poco confiable'},
    'COP': {'name': 'Colombia',         'flag': 'co', 'symbol': '$',    'note': ''},
    'VES': {'name': 'Venezuela',        'flag': 've', 'symbol': 'Bs.',  'note': 'Alta inflacion'},
    'PEN': {'name': 'Peru',             'flag': 'pe', 'symbol': 'S/',   'note': ''},
    'BOB': {'name': 'Bolivia',          'flag': 'bo', 'symbol': 'Bs.s', 'note': ''},
    'BRL': {'name': 'Brasil',           'flag': 'br', 'symbol': 'R$',   'note': ''},
    'CLP': {'name': 'Chile',            'flag': 'cl', 'symbol': '$',    'note': ''},
    'ARS': {'name': 'Argentina',        'flag': 'ar', 'symbol': '$',    'note': 'Alta inflacion'},
    'UYU': {'name': 'Uruguay',          'flag': 'uy', 'symbol': '$U',   'note': ''},
    'PYG': {'name': 'Paraguay',         'flag': 'py', 'symbol': 'Gs.',  'note': ''},
}

_MONTHS_ES = {'01':'ene','02':'feb','03':'mar','04':'abr','05':'may','06':'jun',
              '07':'jul','08':'ago','09':'sep','10':'oct','11':'nov','12':'dic'}

_rates = None
_rates_ts = None
_refreshing = False

def _bcb_get(series_id):
    """Banco Central do Brasil SGS API — free, no auth."""
    url = ('https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados/ultimos/1'
           '?formato=json').format(series_id)
    resp = requests.get(url, timeout=8)
    data = resp.json()
    if data:
        valor = float(data[0]['valor'].replace(',', '.'))
        parts = data[0]['data'].split('/')  # DD/MM/YYYY
        label = _MONTHS_ES.get(parts[1], parts[1]) + ' ' + parts[2]
        return round(valor, 2), label
    return None, None

def _do_refresh():
    global _rates, _rates_ts, _refreshing
    result = {cur: dict(row) for cur, row in _RATES_FALLBACK.items()}
    # Brasil — BCB SGS: 432=SELIC, 13522=IPCA 12m, 20714=media emprestimos PF
    try:
        selic, yr = _bcb_get(432)
        ipca,  _  = _bcb_get(13522)
        lend,  _  = _bcb_get(20714)
        if selic is not None: result['BRL']['deposit']   = selic
        if ipca  is not None: result['BRL']['inflation'] = ipca
        if lend  is not None: result['BRL']['lending']   = lend
        if yr:                result['BRL']['year']      = yr
    except Exception:
        pass
    _rates = result
    _rates_ts = datetime.utcnow()
    _refreshing = False

def _get_rates():
    global _refreshing
    stale = _rates_ts is None or (datetime.utcnow() - _rates_ts) > timedelta(days=30)
    if stale and not _refreshing:
        _refreshing = True
        threading.Thread(target=_do_refresh, daemon=True).start()
    return _rates or _RATES_FALLBACK

@app.route('/api/tasas')
def api_tasas():
    rates = _get_rates()
    ts = _rates_ts.strftime('%b %Y') if _rates_ts else None
    return jsonify({'rates': rates, 'fetched': ts})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculadora-prestamos')
def calculadora_prestamos():
    return render_template('calculadora_prestamos.html')

@app.route('/calculadora-ahorro')
def calculadora_ahorro():
    return render_template('calculadora_ahorro.html')

@app.route('/calculadora-interes-compuesto')
def calculadora_interes():
    return render_template('calculadora_interes.html')

@app.route('/calculadora-presupuesto')
def calculadora_presupuesto():
    return render_template('calculadora_presupuesto.html')

@app.route('/calculadora-tarjeta-credito')
def calculadora_tarjeta():
    return render_template('calculadora_tarjeta.html')

@app.route('/calculadora-deudas')
def calculadora_deudas():
    return render_template('calculadora_deudas.html')

@app.route('/calculadora-inflacion')
def calculadora_inflacion():
    return render_template('calculadora_inflacion.html')

@app.route('/calculadora-jubilacion')
def calculadora_jubilacion():
    return render_template('calculadora_jubilacion.html')

@app.route('/calculadora-plazo-fijo')
def calculadora_plazo_fijo():
    return render_template('calculadora_plazo_fijo.html')

@app.route('/calculadora-fondo-emergencia')
def calculadora_fondo_emergencia():
    return render_template('calculadora_fondo_emergencia.html')

@app.route('/calculadora-descuentos')
def calculadora_descuentos():
    return render_template('calculadora_descuentos.html')

@app.route('/calculadora-liquidacion-laboral')
def calculadora_liquidacion():
    return render_template('calculadora_liquidacion.html')

@app.route('/calculadora-roi')
def calculadora_roi():
    return render_template('calculadora_roi.html')

@app.route('/calculadora-tipo-cambio')
def calculadora_tipo_cambio():
    return render_template('calculadora_tipo_cambio.html')

@app.route('/calculadora-tir-van')
def calculadora_tir_van():
    return render_template('calculadora_tir_van.html')

@app.route('/calculadora-seguro-vida')
def calculadora_seguro_vida():
    return render_template('calculadora_seguro_vida.html')

@app.route('/calculadora-portafolio')
def calculadora_portafolio():
    return render_template('calculadora_portafolio.html')

@app.route('/tasas-de-interes-latam')
def tasas_latam():
    rates = _get_rates()
    rows = []
    for code, meta in _COUNTRY_META.items():
        r = rates.get(code, _RATES_FALLBACK.get(code, {}))
        rows.append({
            'code':      code,
            'name':      meta['name'],
            'flag':      meta['flag'],
            'symbol':    meta['symbol'],
            'note':      meta['note'],
            'lending':   r.get('lending'),
            'deposit':   r.get('deposit'),
            'inflation': r.get('inflation'),
            'source':    r.get('source', ''),
            'year':      r.get('year', ''),
        })
    return render_template('tasas_latam.html', rows=rows)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

BLOG_ARTICLES = {
    'como-calcular-cuota-prestamo-personal': 'blog_prestamos.html',
    'cuanto-debo-ahorrar-al-mes':            'blog_ahorro.html',
    'que-es-el-interes-compuesto':           'blog_interes.html',
    'como-salir-deuda-tarjeta-credito':      'blog_tarjeta.html',
    'como-hacer-presupuesto-personal':       'blog_presupuesto.html',
    'como-proteger-dinero-de-la-inflacion':  'blog_inflacion.html',
    'cuanto-necesito-para-jubilarme':        'blog_jubilacion.html',
    'que-es-un-plazo-fijo':                 'blog_plazo_fijo.html',
    'como-calcular-roi-inversion':           'blog_roi.html',
    'como-calcular-fondo-emergencia':        'blog_fondo_emergencia.html',
    'calcular-descuento-porcentaje':         'blog_descuentos.html',
    'como-calcular-liquidacion-laboral':     'blog_liquidacion.html',
    'que-es-el-tipo-de-cambio':              'blog_tipo_cambio.html',
    'como-pagar-varias-deudas-bola-de-nieve-avalancha': 'blog_deudas.html',
    'que-es-la-tir-y-el-van':                'blog_tir_van.html',
    'cuanto-seguro-de-vida-necesito':        'blog_seguro_vida.html',
    'como-armar-un-portafolio-de-inversion': 'blog_portafolio.html',
}

@app.route('/blog')
def blog_index():
    return render_template('blog_index.html')

@app.route('/blog/<slug>')
def blog_article(slug):
    template = BLOG_ARTICLES.get(slug)
    if not template:
        from flask import abort
        abort(404)
    return render_template(template)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/sitemap.xml')
def sitemap():
    pages = [
        ('/', '1.0', 'weekly'),
        ('/calculadora-prestamos', '0.9', 'monthly'),
        ('/calculadora-ahorro', '0.9', 'monthly'),
        ('/calculadora-interes-compuesto', '0.9', 'monthly'),
        ('/calculadora-presupuesto', '0.9', 'monthly'),
        ('/calculadora-tarjeta-credito', '0.9', 'monthly'),
        ('/calculadora-deudas', '0.9', 'monthly'),
        ('/calculadora-inflacion', '0.9', 'monthly'),
        ('/calculadora-jubilacion', '0.9', 'monthly'),
        ('/calculadora-plazo-fijo', '0.9', 'monthly'),
        ('/calculadora-fondo-emergencia', '0.9', 'monthly'),
        ('/calculadora-descuentos', '0.9', 'monthly'),
        ('/calculadora-liquidacion-laboral', '0.9', 'monthly'),
        ('/calculadora-roi', '0.9', 'monthly'),
        ('/calculadora-tipo-cambio', '0.9', 'monthly'),
        ('/blog', '0.8', 'weekly'),
        ('/blog/como-calcular-cuota-prestamo-personal', '0.8', 'monthly'),
        ('/blog/cuanto-debo-ahorrar-al-mes', '0.8', 'monthly'),
        ('/blog/que-es-el-interes-compuesto', '0.8', 'monthly'),
        ('/blog/como-salir-deuda-tarjeta-credito', '0.8', 'monthly'),
        ('/blog/como-hacer-presupuesto-personal', '0.8', 'monthly'),
        ('/blog/como-proteger-dinero-de-la-inflacion', '0.8', 'monthly'),
        ('/blog/cuanto-necesito-para-jubilarme', '0.8', 'monthly'),
        ('/blog/que-es-un-plazo-fijo', '0.8', 'monthly'),
        ('/blog/como-calcular-roi-inversion', '0.8', 'monthly'),
        ('/blog/como-calcular-fondo-emergencia', '0.8', 'monthly'),
        ('/blog/calcular-descuento-porcentaje', '0.8', 'monthly'),
        ('/blog/como-calcular-liquidacion-laboral', '0.8', 'monthly'),
        ('/blog/que-es-el-tipo-de-cambio', '0.8', 'monthly'),
        ('/blog/como-pagar-varias-deudas-bola-de-nieve-avalancha', '0.8', 'monthly'),
        ('/blog/que-es-la-tir-y-el-van', '0.8', 'monthly'),
        ('/blog/cuanto-seguro-de-vida-necesito', '0.8', 'monthly'),
        ('/blog/como-armar-un-portafolio-de-inversion', '0.8', 'monthly'),
        ('/calculadora-tir-van', '0.9', 'monthly'),
        ('/calculadora-seguro-vida', '0.9', 'monthly'),
        ('/calculadora-portafolio', '0.9', 'monthly'),
        ('/tasas-de-interes-latam', '0.85', 'monthly'),
        ('/contacto', '0.4', 'yearly'),
        ('/acerca', '0.4', 'yearly'),
        ('/privacidad', '0.3', 'yearly'),
        ('/terminos', '0.3', 'yearly'),
    ]
    base = 'https://midineroobedece.com'
    hoy = date.today().isoformat()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path, priority, freq in pages:
        xml += f'  <url>\n    <loc>{base}{path}</loc>\n    <lastmod>{hoy}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')

@app.route('/manifest.json')
def manifest():
    data = '''{
  "name": "MiDineroObedece",
  "short_name": "MiDinero",
  "description": "Calculadoras financieras gratuitas para America Latina",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#08091a",
  "theme_color": "#5b4fff",
  "lang": "es",
  "categories": ["finance", "utilities"],
  "icons": [
    {"src": "/static/images/logo.jpg", "sizes": "192x192", "type": "image/jpeg", "purpose": "any maskable"},
    {"src": "/static/images/logo.jpg", "sizes": "512x512", "type": "image/jpeg", "purpose": "any maskable"}
  ],
  "shortcuts": [
    {"name": "Calculadora de Prestamos", "url": "/calculadora-prestamos", "description": "Calcula tu cuota mensual"},
    {"name": "Tipo de Cambio",           "url": "/calculadora-tipo-cambio", "description": "Conversor de monedas"},
    {"name": "Pago de Deudas",           "url": "/calculadora-deudas",     "description": "Bola de nieve vs avalancha"}
  ]
}'''
    return Response(data, mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    sw = """var CACHE = 'mdo-v2';
var SHELL = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js'
];

self.addEventListener('install', function(e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function(c) { return c.addAll(SHELL); }));
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE; }).map(function(k) { return caches.delete(k); }));
    })
  );
  return self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  var url = e.request.url;
  if (url.includes('/api/') || url.includes('er-api.com') || url.includes('list-manage.com') || e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      var net = fetch(e.request).then(function(res) {
        if (res && res.status === 200 && res.type === 'basic') {
          caches.open(CACHE).then(function(c) { c.put(e.request, res.clone()); });
        }
        return res;
      });
      return cached || net;
    })
  );
});
"""
    return Response(sw, mimetype='application/javascript')

@app.route('/robots.txt')
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: https://midineroobedece.com/sitemap.xml\n"
    return Response(content, mimetype='text/plain')

@app.route('/ads.txt')
def ads_txt():
    content = "google.com, pub-2445512602031923, DIRECT, f08c47fec0942fa0\n"
    return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
