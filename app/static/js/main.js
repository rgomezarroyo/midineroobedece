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
}
