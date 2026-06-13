// ── CURRENCY SYSTEM ──
const MDO_CURRENCIES = {
  USD: { symbol: '$',   locale: 'es-EC', dec: 2 },
  MXN: { symbol: '$',   locale: 'es-MX', dec: 2 },
  COP: { symbol: '$',   locale: 'es-CO', dec: 0 },
  PEN: { symbol: 'S/',  locale: 'es-PE', dec: 2 },
  ARS: { symbol: '$',   locale: 'es-AR', dec: 0 },
  CLP: { symbol: '$',   locale: 'es-CL', dec: 0 },
  BRL: { symbol: 'R$',  locale: 'pt-BR', dec: 2 },
  BOB: { symbol: 'Bs.', locale: 'es-BO', dec: 2 },
};

function getCurr() {
  return MDO_CURRENCIES[localStorage.getItem('mdo_cur') || 'USD'];
}

function fmt(v) {
  const c = getCurr();
  return c.symbol + v.toLocaleString(c.locale, {
    minimumFractionDigits: c.dec,
    maximumFractionDigits: c.dec,
  });
}

function changeCurrency(code) {
  localStorage.setItem('mdo_cur', code);
  const sym = MDO_CURRENCIES[code].symbol;
  document.querySelectorAll('.cur-sym').forEach(el => el.textContent = sym);
  const page = document.querySelector('[data-recalc]');
  if (page) {
    const fn = page.dataset.recalc;
    const shown = document.querySelector('[id^="resultados-data"][style*="block"]');
    if (shown && typeof window[fn] === 'function') window[fn]();
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const saved = localStorage.getItem('mdo_cur') || 'USD';
  const sel = document.getElementById('currency-sel');
  if (sel) sel.value = saved;
  const sym = MDO_CURRENCIES[saved].symbol;
  document.querySelectorAll('.cur-sym').forEach(el => el.textContent = sym);
});

// ── SHARE WHATSAPP ──
function shareWA() {
  var msg = window._shareMsg || '';
  window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
}

// ── CALCULADORA DESCUENTOS ──
function calcularDescuento() {
  const precio = parseFloat(document.getElementById('precio').value);
  const descuento = parseFloat(document.getElementById('descuento').value);

  if (!precio || isNaN(descuento) || descuento < 0 || descuento > 100) {
    alert('Por favor ingresa un precio válido y un descuento entre 0 y 100.');
    return;
  }

  const ahorro = precio * descuento / 100;
  const precioFinal = precio - ahorro;
  const pagado = 100 - descuento;

  document.getElementById('precio-final').textContent = fmt(precioFinal);
  document.getElementById('ahorro-desc').textContent = fmt(ahorro);
  document.getElementById('porcentaje-pagado').textContent = pagado.toFixed(1) + '%';

  document.getElementById('resultados-espera-desc').style.display = 'none';
  document.getElementById('resultados-data-desc').style.display = 'block';
  window._shareMsg = 'Calcule mi descuento en MiDineroObedece:\nPrecio final: ' + fmt(precioFinal) + ' | Ahorro: ' + fmt(ahorro) + ' (' + descuento + '% off)\nCalcula el tuyo gratis: midineroobedece.com/calculadora-descuentos';
  document.getElementById('btn-share-desc').style.display = 'flex';
}

// ── CALCULADORA LIQUIDACION LABORAL ──
function calcularLiquidacion() {
  const sueldo = parseFloat(document.getElementById('sueldo-liq').value);
  const anos = parseInt(document.getElementById('anos-liq').value) || 0;
  const meses = parseInt(document.getElementById('meses-liq').value) || 0;
  const tipo = document.getElementById('tipo-liq').value;

  if (!sueldo || sueldo <= 0) {
    alert('Por favor ingresa un sueldo valido.');
    return;
  }

  const indemnizacion = tipo === 'despido' ? sueldo * anos : 0;
  const vacaciones = (sueldo / 12) * meses;
  const aguinaldo = (sueldo / 12) * meses;
  const total = indemnizacion + vacaciones + aguinaldo;

  document.getElementById('total-liq').textContent = fmt(total);
  document.getElementById('item-indemnizacion').style.display = tipo === 'despido' ? 'block' : 'none';
  document.getElementById('indemnizacion-liq').textContent = fmt(indemnizacion);
  document.getElementById('vacaciones-liq').textContent = fmt(vacaciones);
  document.getElementById('aguinaldo-liq').textContent = fmt(aguinaldo);

  document.getElementById('resultados-espera-liq').style.display = 'none';
  document.getElementById('resultados-data-liq').style.display = 'block';
  window._shareMsg = 'Calcule mi liquidacion laboral en MiDineroObedece:\nTotal a recibir: ' + fmt(total) + '\nCalcula el tuyo gratis: midineroobedece.com/calculadora-liquidacion-laboral';
  document.getElementById('btn-share-liq').style.display = 'flex';
}

// ── CALCULADORA ROI ──
function calcularROI() {
  const inversion = parseFloat(document.getElementById('inversion-roi').value);
  const valorFinal = parseFloat(document.getElementById('valor-final-roi').value);
  const periodo = parseInt(document.getElementById('periodo-roi').value);

  if (!inversion || inversion <= 0 || !valorFinal || valorFinal < 0) {
    alert('Por favor ingresa una inversion inicial y un valor final validos.');
    return;
  }

  const ganancia = valorFinal - inversion;
  const roiTotal = (ganancia / inversion) * 100;
  const multiplicador = valorFinal / inversion;
  const item = document.getElementById('ganancia-item-roi');
  item.classList.remove('positivo', 'negativo');
  item.classList.add(ganancia >= 0 ? 'positivo' : 'negativo');
  document.getElementById('roi-total').textContent = roiTotal.toFixed(2) + '%';
  document.getElementById('ganancia-roi').textContent = (ganancia >= 0 ? '+' : '') + fmt(ganancia);
  document.getElementById('multiplicador-roi').textContent = multiplicador.toFixed(2) + 'x';

  if (periodo && periodo > 0) {
    const roiAnual = (Math.pow(valorFinal / inversion, 12 / periodo) - 1) * 100;
    document.getElementById('roi-anual').textContent = roiAnual.toFixed(2) + '% / año';
  } else {
    document.getElementById('roi-anual').textContent = '— (sin periodo)';
  }

  document.getElementById('resultados-espera-roi').style.display = 'none';
  document.getElementById('resultados-data-roi').style.display = 'block';
  window._shareMsg = 'Calcule el ROI de mi inversion en MiDineroObedece:\nROI total: ' + roiTotal.toFixed(2) + '% | Ganancia: ' + fmt(ganancia) + '\nROI anualizado: ' + document.getElementById('roi-anual').textContent + '\nCalcula el tuyo gratis: midineroobedece.com/calculadora-roi';
  document.getElementById('btn-share-roi').style.display = 'flex';
}

// ── CALCULADORA TIPO DE CAMBIO ──
async function calcularTipoCambio() {
  const monto = parseFloat(document.getElementById('monto-tc').value);
  const fromCur = document.getElementById('moneda-from').value;
  const toCur = document.getElementById('moneda-to').value;

  if (!monto || monto <= 0) {
    alert('Por favor ingresa un monto valido.');
    return;
  }

  const btn = document.getElementById('btn-tc');
  btn.textContent = 'Obteniendo tasa...';
  btn.disabled = true;

  try {
    const res = await fetch('https://open.er-api.com/v6/latest/' + fromCur);
    const data = await res.json();
    if (data.result !== 'success') throw new Error('API error');

    const tasa = data.rates[toCur];
    const resultado = monto * tasa;
    const fecha = data.time_last_update_utc ? data.time_last_update_utc.split(' 00:')[0] : 'hoy';

    document.getElementById('resultado-tc').textContent = toCur + ' ' + resultado.toLocaleString('es-EC', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('tasa-tc').textContent = '1 ' + fromCur + ' = ' + tasa.toLocaleString('es-EC', { minimumFractionDigits: 4, maximumFractionDigits: 4 }) + ' ' + toCur;
    document.getElementById('fecha-tc').textContent = fecha;

    document.getElementById('resultados-espera-tc').style.display = 'none';
    document.getElementById('resultados-data-tc').style.display = 'block';
    window._shareMsg = 'Calcule el tipo de cambio en MiDineroObedece:\n' + document.getElementById('resultado-tc').textContent + '\nTasa: ' + document.getElementById('tasa-tc').textContent + '\nCalcula el tuyo gratis: midineroobedece.com/calculadora-tipo-cambio';
    document.getElementById('btn-share-tc').style.display = 'flex';
  } catch (err) {
    alert('No se pudo obtener la tasa de cambio. Verifica tu conexion a internet.');
  } finally {
    btn.textContent = 'Convertir →';
    btn.disabled = false;
  }
}

// ── CALCULADORA PRÉSTAMOS ──
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
  window._shareMsg = 'Calcule mi cuota de prestamo en MiDineroObedece:\nCuota mensual: ' + fmt(cuota) + '\nTotal a pagar: ' + fmt(totalPagar) + ' (' + fmt(totalIntereses) + ' en intereses)\nCalcula el tuyo gratis: midineroobedece.com/calculadora-prestamos';
  document.getElementById('btn-share-pres').style.display = 'flex';
}
