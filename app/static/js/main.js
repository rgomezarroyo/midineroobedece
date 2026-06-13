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

// ── RATE HINTS ──
var HINT_DATE = '· <em class="hint-date">Ref. jun 2026</em>';
var RATE_HINTS = {
  prestamos: {
    USD: '<strong>Ecuador (USD):</strong> credito personal 16-24% anual · tasa maxima BCE',
    MXN: '<strong>Mexico (MXN):</strong> credito personal 18-36% anual · segun banco y perfil',
    COP: '<strong>Colombia (COP):</strong> credito consumo 20-32% anual · DTF + spread bancario',
    PEN: '<strong>Peru (PEN):</strong> credito personal 15-28% anual · segun entidad',
    ARS: '<strong>Argentina (ARS):</strong> credito personal 70-100%+ anual · tasa muy variable',
    CLP: '<strong>Chile (CLP):</strong> credito consumo 12-20% anual · CAE referencial CMF',
    BRL: '<strong>Brasil (BRL):</strong> credito pessoal 25-55% anual · juros variam por banco',
    BOB: '<strong>Bolivia (BOB):</strong> credito personal 8-18% anual · sistema regulado BCB',
  },
  tarjeta: {
    USD: '<strong>Ecuador (USD):</strong> max 17% anual · tasa maxima regulada por BCE',
    MXN: '<strong>Mexico (MXN):</strong> 24-60% anual · TEA segun banco emisor',
    COP: '<strong>Colombia (COP):</strong> 22-36% anual · tasa maxima legal establecida',
    PEN: '<strong>Peru (PEN):</strong> 20-45% anual · TEA segun entidad financiera',
    ARS: '<strong>Argentina (ARS):</strong> 50-80% anual · regulada por BCRA',
    CLP: '<strong>Chile (CLP):</strong> 20-35% anual · tasa maxima convencional CMF',
    BRL: '<strong>Brasil (BRL):</strong> 80-200%+ anual · rotativo muy caro, paga el total mensual',
    BOB: '<strong>Bolivia (BOB):</strong> 15-25% anual · credito revolvente regulado BCB',
  },
  ahorro: {
    USD: '<strong>Ecuador (USD):</strong> 3-5% anual · bancos y cooperativas reguladas',
    MXN: '<strong>Mexico (MXN):</strong> 3-5% cuenta ahorro · hasta 10-12% en CETES',
    COP: '<strong>Colombia (COP):</strong> 4-7% anual · cuenta de ahorros bancaria',
    PEN: '<strong>Peru (PEN):</strong> 2-5% anual · cuenta de ahorros',
    ARS: '<strong>Argentina (ARS):</strong> 50-80% anual nominal · busca tasa mayor a la inflacion',
    CLP: '<strong>Chile (CLP):</strong> 2-4% anual · cuenta de ahorro vista',
    BRL: '<strong>Brasil (BRL):</strong> poupanca ~6% · CDB ~12-13% · rendimiento variable',
    BOB: '<strong>Bolivia (BOB):</strong> 2-4% anual · caja de ahorros regulada',
  },
  interes: {
    USD: '<strong>Ecuador (USD):</strong> plazo fijo 3-7% · fondos indexados ~10% hist.',
    MXN: '<strong>Mexico (MXN):</strong> CETES 9-12% · fondos de inversion 8-13%',
    COP: '<strong>Colombia (COP):</strong> CDT 9-13% · fondos mixtos 8-15%',
    PEN: '<strong>Peru (PEN):</strong> depositos a plazo 4-8% · fondos mutuos 7-12%',
    ARS: '<strong>Argentina (ARS):</strong> FCI 60-80%+ nominal · prioriza cobertura de inflacion',
    CLP: '<strong>Chile (CLP):</strong> depositos a plazo 4-7% · fondos mutuos 6-11%',
    BRL: '<strong>Brasil (BRL):</strong> CDI ~13% · fundos renda fixa 10-16%',
    BOB: '<strong>Bolivia (BOB):</strong> depositos 3-6% · fondos de inversion 5-10%',
  },
  plazofijo: {
    USD: '<strong>Ecuador (USD):</strong> 3-7% anual · tasa BCE regulada segun plazo',
    MXN: '<strong>Mexico (MXN):</strong> 9-11% (CETES) · bancos y pagares 8-12%',
    COP: '<strong>Colombia (COP):</strong> 9-13% anual · CDT bancario',
    PEN: '<strong>Peru (PEN):</strong> 4-8% anual · deposito a plazo',
    ARS: '<strong>Argentina (ARS):</strong> 70-100%+ nominal · plazo fijo UVA cubre inflacion',
    CLP: '<strong>Chile (CLP):</strong> 4-7% anual · deposito a plazo',
    BRL: '<strong>Brasil (BRL):</strong> 10-14% anual · CDB/LCI referenciado al CDI',
    BOB: '<strong>Bolivia (BOB):</strong> 3-6% anual · DPF en sistema bancario',
  },
  inflacion: {
    USD: '<strong>Ecuador (USD):</strong> 1-3% anual · economia dolarizada, inflacion baja',
    MXN: '<strong>Mexico (MXN):</strong> 4-7% anual · meta Banxico 3%',
    COP: '<strong>Colombia (COP):</strong> 6-9% anual · meta Banrep 3%',
    PEN: '<strong>Peru (PEN):</strong> 3-6% anual · meta BCRP 2%',
    ARS: '<strong>Argentina (ARS):</strong> 50%+ anual · inflacion muy alta, revisa dato actual',
    CLP: '<strong>Chile (CLP):</strong> 4-6% anual · meta BCCh 3%',
    BRL: '<strong>Brasil (BRL):</strong> 4-7% anual · meta Bacen 3%',
    BOB: '<strong>Bolivia (BOB):</strong> 3-6% anual · meta BCB 3%',
  },
  jubilacion: {
    USD: '<strong>Ecuador:</strong> conservador 4-6% · moderado 6-9% · agresivo 8-12%',
    MXN: '<strong>Mexico (AFORE):</strong> conservador 5-8% · moderado 7-11% · agresivo 9-14%',
    COP: '<strong>Colombia (AFP):</strong> conservador 5-8% · moderado 7-11% · agresivo 9-14%',
    PEN: '<strong>Peru (AFP):</strong> conservador 4-7% · moderado 6-10% · agresivo 8-13%',
    ARS: '<strong>Argentina:</strong> fondos ARS ajustar por inflacion · evalua cobertura en USD',
    CLP: '<strong>Chile (AFP):</strong> fondo E 3-5% · fondo C 5-8% · fondo A 7-12%',
    BRL: '<strong>Brasil (PGBL/VGBL):</strong> conservador 8-10% · moderado 10-14% · agresivo 12-18%',
    BOB: '<strong>Bolivia:</strong> conservador 4-6% · moderado 5-8% · instrumentos limitados',
  },
};

function updateRateHints(code) {
  document.querySelectorAll('.tasa-hint[data-hint]').forEach(function(el) {
    var type = el.dataset.hint;
    var hints = RATE_HINTS[type];
    if (hints && hints[code]) el.innerHTML = hints[code] + ' ' + HINT_DATE;
  });
}

function changeCurrency(code) {
  localStorage.setItem('mdo_cur', code);
  const sym = MDO_CURRENCIES[code].symbol;
  document.querySelectorAll('.cur-sym').forEach(el => el.textContent = sym);
  updateRateHints(code);
  const page = document.querySelector('[data-recalc]');
  if (page) {
    const fn = page.dataset.recalc;
    const shown = document.querySelector('[id^="resultados-data"][style*="block"]');
    if (shown && typeof window[fn] === 'function') window[fn]();
  }
}

// ── CURRENCY PICKER ──
var CP_FLAGS = {
  USD: ['🇪🇨', 'Ecuador'],
  MXN: ['🇲🇽', 'Mexico'],
  COP: ['🇨🇴', 'Colombia'],
  PEN: ['🇵🇪', 'Peru'],
  ARS: ['🇦🇷', 'Argentina'],
  CLP: ['🇨🇱', 'Chile'],
  BRL: ['🇧🇷', 'Brasil'],
  BOB: ['🇧🇴', 'Bolivia'],
};

function toggleCurrencyPicker(e) {
  e.stopPropagation();
  var dd = document.getElementById('cp-dropdown');
  var btn = document.getElementById('currency-trigger');
  var isOpen = dd.classList.contains('open');
  dd.classList.toggle('open', !isOpen);
  btn.classList.toggle('open', !isOpen);
}

function selectCurrency(code) {
  var data = CP_FLAGS[code];
  if (!data) return;
  var flagEl = document.getElementById('cp-flag-sel');
  var codeEl = document.getElementById('cp-code-sel');
  if (flagEl) { flagEl.textContent = data[0]; flagEl.classList.remove('flag-pick'); void flagEl.offsetWidth; flagEl.classList.add('flag-pick'); }
  if (codeEl) codeEl.textContent = code;
  document.querySelectorAll('.cp-option').forEach(function(el) {
    el.classList.toggle('active', el.dataset.code === code);
  });
  var dd = document.getElementById('cp-dropdown');
  var btn = document.getElementById('currency-trigger');
  if (dd) dd.classList.remove('open');
  if (btn) btn.classList.remove('open');
  changeCurrency(code);
}

document.addEventListener('click', function() {
  var dd = document.getElementById('cp-dropdown');
  var btn = document.getElementById('currency-trigger');
  if (dd) dd.classList.remove('open');
  if (btn) btn.classList.remove('open');
});

document.addEventListener('DOMContentLoaded', function () {
  var saved = localStorage.getItem('mdo_cur') || 'USD';
  var data = CP_FLAGS[saved];
  if (data) {
    var flagEl = document.getElementById('cp-flag-sel');
    var codeEl = document.getElementById('cp-code-sel');
    if (flagEl) flagEl.textContent = data[0];
    if (codeEl) codeEl.textContent = saved;
    document.querySelectorAll('.cp-option').forEach(function(el) {
      el.classList.toggle('active', el.dataset.code === saved);
    });
  }
  var sym = MDO_CURRENCIES[saved].symbol;
  document.querySelectorAll('.cur-sym').forEach(function(el) { el.textContent = sym; });
  updateRateHints(saved);
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
