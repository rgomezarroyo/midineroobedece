from flask import Flask, render_template, Response, jsonify
from datetime import date, datetime, timedelta
import requests, threading

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# ── MOTOR DE TASAS (Banco Mundial API, refresh mensual) ──
_RATES_FALLBACK = {
    'USD': {'lending': 16.0, 'deposit': 4.0, 'inflation':  2.0, 'year': '2024'},
    'MXN': {'lending': 18.0, 'deposit': 4.0, 'inflation':  5.5, 'year': '2024'},
    'COP': {'lending': 22.0, 'deposit': 5.5, 'inflation':  7.0, 'year': '2024'},
    'PEN': {'lending': 17.0, 'deposit': 3.5, 'inflation':  4.5, 'year': '2024'},
    'ARS': {'lending': 80.0, 'deposit':60.0, 'inflation':120.0, 'year': '2024'},
    'CLP': {'lending': 14.0, 'deposit': 3.0, 'inflation':  5.0, 'year': '2024'},
    'BRL': {'lending': 35.0, 'deposit':11.0, 'inflation':  5.5, 'year': '2024'},
    'BOB': {'lending': 10.0, 'deposit': 2.5, 'inflation':  4.5, 'year': '2024'},
}
_WB_CTRY = {'USD':'ECU','MXN':'MEX','COP':'COL','PEN':'PER','ARS':'ARG','CLP':'CHL','BRL':'BRA','BOB':'BOL'}
_WB_IND  = {'lending':'FR.INR.LEND','deposit':'FR.INR.DPST','inflation':'FP.CPI.TOTL.ZG'}

_rates = None
_rates_ts = None
_refreshing = False

def _wb_get(wb_code, indicator):
    url = ('https://api.worldbank.org/v2/country/{}/indicator/{}'
           '?format=json&mrv=3&per_page=3').format(wb_code, indicator)
    resp = requests.get(url, timeout=8)
    rows = resp.json()
    if len(rows) > 1 and rows[1]:
        for row in rows[1]:
            if row.get('value') is not None:
                return round(float(row['value']), 1), row['date']
    return None, None

def _do_refresh():
    global _rates, _rates_ts, _refreshing
    result = {}
    for cur, wb in _WB_CTRY.items():
        row = dict(_RATES_FALLBACK.get(cur, {}))
        for key, ind in _WB_IND.items():
            try:
                val, yr = _wb_get(wb, ind)
                if val is not None:
                    row[key] = val
                    row['year'] = yr
            except Exception:
                pass
        result[cur] = row
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
