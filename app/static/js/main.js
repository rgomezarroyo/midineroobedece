function formatearMoneda(valor) {
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

    document.getElementById('cuota').textContent = formatearMoneda(cuota);
    document.getElementById('total').textContent = formatearMoneda(totalPagar);
    document.getElementById('intereses').textContent = formatearMoneda(totalIntereses);
    document.getElementById('resultados').style.display = 'block';
}

function calcularAhorro() {
    const meta = parseFloat(document.getElementById('meta').value);
    const meses = parseInt(document.getElementById('meses').value);
    const tasaAnual = parseFloat(document.getElementById('tasa_ahorro').value) || 0;

    if (!meta || !meses) {
        alert('Por favor completa todos los campos.');
        return;
    }

    const tasaMensual = tasaAnual / 100 / 12;
    let ahorroMensual;

    if (tasaMensual === 0) {
        ahorroMensual = meta / meses;
    } else {
        ahorroMensual = meta * tasaMensual / (Math.pow(1 + tasaMensual, meses) - 1);
    }

    document.getElementById('ahorro_mensual').textContent = formatearMoneda(ahorroMensual);
    document.getElementById('total_aportado').textContent = formatearMoneda(ahorroMensual * meses);
    document.getElementById('ganancia_intereses').textContent = formatearMoneda(meta - (ahorroMensual * meses));
    document.getElementById('resultados_ahorro').style.display = 'block';
}

function calcularInteres() {
    const capital = parseFloat(document.getElementById('capital').value);
    const tasaAnual = parseFloat(document.getElementById('tasa_interes').value);
    const anos = parseInt(document.getElementById('anos').value);
    const frecuencia = parseInt(document.getElementById('frecuencia').value);

    if (!capital || !tasaAnual || !anos) {
        alert('Por favor completa todos los campos.');
        return;
    }

    const montoFinal = capital * Math.pow(1 + (tasaAnual / 100 / frecuencia), frecuencia * anos);
    const ganancia = montoFinal - capital;

    document.getElementById('monto_final').textContent = formatearMoneda(montoFinal);
    document.getElementById('ganancia_total').textContent = formatearMoneda(ganancia);
    document.getElementById('multiplicador').textContent = (montoFinal / capital).toFixed(2) + 'x';
    document.getElementById('resultados_interes').style.display = 'block';
}
