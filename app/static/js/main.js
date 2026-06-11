function fmt(valor) {
    return '$' + valor.toLocaleString('es-EC', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function calcularPrestamo() {
    const monto = parseFloat(document.getElementById('monto').value);
    const tasaAnual = parseFloat(document.getElementById('tasa').value);
    const plazo = parseInt(document.getElementById('plazo').value);

    if (!monto || !tasaAnual || !plazo) {
        alert('Por favor completa todos los campos.');
        return;
    }

    const tasaMensual = tasaAnual / 100 / 12;
    const cuota = monto * (tasaMensual * Math.pow(1 + tasaMensual, plazo)) / (Math.pow(1 + tasaMensual, plazo) - 1);
    const totalPagar = cuota * plazo;
    const totalIntereses = totalPagar - monto;

    document.getElementById('cuota').textContent = fmt(cuota);
    document.getElementById('total').textContent = fmt(totalPagar);
    document.getElementById('intereses').textContent = fmt(totalIntereses);

    document.getElementById('resultados-espera').style.display = 'none';
    document.getElementById('resultados-data').style.display = 'block';
}
