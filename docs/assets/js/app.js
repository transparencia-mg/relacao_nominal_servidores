// =====================================================
// CONFIGURAÇÃO DA API (HOMOLOGAÇÃO)
// =====================================================
const API_BASE = 'http://localhost:8000';

// =====================================================
// FUNÇÕES AUXILIARES
// =====================================================
async function fetchJSON(url) {
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(`Erro ao acessar ${url}`);
  }
  return resp.json();
}

function formatarPeriodo(periodo) {
  // aceita "2025-11" ou "202511"
  const p = periodo.includes('-')
    ? periodo.replace('-', '')
    : periodo;

  const ano = p.slice(0, 4);
  const mes = p.slice(4, 6);

  const meses = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Março",
    "04": "Abril", "05": "Maio", "06": "Junho",
    "07": "Julho", "08": "Agosto", "09": "Setembro",
    "10": "Outubro", "11": "Novembro", "12": "Dezembro"
  };

  return `${meses[mes]} de ${ano}`;
}

// =====================================================
// PERÍODOS
// =====================================================
async function carregarPeriodos() {
  const periodos = await fetchJSON(`${API_BASE}/periodos`);
  periodos.sort(); // ordem crescente
  return periodos;
}

function preencherSelectPeriodos(periodos, periodoAtual) {
  const select = document.getElementById('periodo');
  select.innerHTML = '';

  periodos.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p;
    opt.text = formatarPeriodo(p);
    if (p === periodoAtual) opt.selected = true;
    select.appendChild(opt);
  });

  select.addEventListener('change', e => {
    carregarDashboard(e.target.value);
  });
}

// =====================================================
// VISÃO GERAL
// =====================================================
async function carregarVisaoGeral(periodo) {
  const tbody = document.querySelector('#tabela-visao-geral tbody');
  if (!tbody) return;

  tbody.innerHTML = '';

  const resp = await fetchJSON(
    `${API_BASE}/servidores/visao-geral?periodo=${periodo}`
  );

  resp.dados.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${item.sigla}</td>
      <td>${item.nome}</td>
      <td>${item.total}</td>
    `;
    tbody.appendChild(tr);
  });
}

// =====================================================
// DETALHADO
// =====================================================
async function carregarDetalhado(periodo) {
  const tbody = document.querySelector('#tabela-detalhada tbody');
  if (!tbody) return;

  tbody.innerHTML = '';

  const resp = await fetchJSON(
    `${API_BASE}/servidores/detalhado?periodo=${periodo}&limit=1000`
  );

  resp.dados.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.masp || ''}</td>
      <td>${r.nome || ''}</td>
      <td>${r.orgao || ''}</td>
      <td>${r.cargo || ''}</td>
      <td>${r.carga_horaria || ''}</td>
      <td>${r.situacao || ''}</td>
    `;
    tbody.appendChild(tr);
  });
}

// =====================================================
// DASHBOARD
// =====================================================
async function carregarDashboard(periodo) {
  try {
    document.getElementById('periodo-atual').innerText =
      formatarPeriodo(periodo);

    await carregarVisaoGeral(periodo);
    await carregarDetalhado(periodo);

    console.log(`✅ Dashboard carregado para ${periodo}`);
  } catch (e) {
    console.error(e);
    alert('Erro ao carregar dados do período selecionado');
  }
}

// =====================================================
// INICIALIZAÇÃO
// =====================================================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    console.log('🚀 Iniciando dashboard (API homologação)');

    const periodos = await carregarPeriodos();
    const periodoAtual = periodos[periodos.length - 1];

    preencherSelectPeriodos(periodos, periodoAtual);
    carregarDashboard(periodoAtual);

  } catch (e) {
    console.error(e);
    alert('Erro ao inicializar o dashboard');
  }
});


