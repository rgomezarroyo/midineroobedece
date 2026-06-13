from flask import Flask, render_template, Response
from datetime import date

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

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
