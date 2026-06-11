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

if __name__ == '__main__':
    app.run(debug=True)
