from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
