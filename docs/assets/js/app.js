// ============================================
// DASHBOARD – DADOS LOCAIS (GitHub Pages)
// ============================================

async function fetchJSON(path) {
  const resp = await fetch(path);
  if (!resp.ok) {
    throw new Error(`Erro ao carregar ${path}`);
  }
  return resp.json();
}

// ============================================
// VISÃO GERAL
// ============================================

async function carregarVisaoGeral() {
  const tbody = document.querySelector('#tabela-visao-geral tbody');
  if (!tbody) {
    console.warn('Tabela visão geral não encontrada');
    return;
  }

  tbody.innerHTML = '';

  const dados = await fetchJSON('data/visao_geral.json');

  dados.forEach(item => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${item.sigla}</td>
      <td>${item.nome}</td>
      <td>${item.total}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================
// DETALHADO
// ============================================

async function carregarDetalhado() {
  const tbody = document.querySelector('#tabela-detalhada tbody');
  if (!tbody) {
    console.warn('Tabela detalhada não encontrada');
    return;
  }

  tbody.innerHTML = '';

  const dados = await fetchJSON('data/detalhado.json');

  dados.forEach(r => {
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

// ============================================
// INICIALIZAÇÃO
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
  try {
    console.log('🚀 Iniciando dashboard (dados locais)');
    await carregarVisaoGeral();
    await carregarDetalhado();
    console.log('✅ Dashboard carregado com sucesso');
  } catch (e) {
    console.error(e);
    alert('Erro ao carregar os dados do dashboard');
  }
});

