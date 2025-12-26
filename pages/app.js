// ============================================
// CONFIGURAÇÃO
// ============================================

// ⚠️ Troque pelo resource_id do mês que você quiser
// (ex: mês mais recente)
const RESOURCE_ID = '74e9fe88-a476-4061-95d0-5091ec131b3f';

const DATASTORE_URL =
  'https://dados.mg.gov.br/api/3/action/datastore_search';

const LIMITE_PADRAO = 500;

// ============================================
// FUNÇÃO GENÉRICA PARA CONSULTAR DATASTORE
// ============================================
async function consultarDataStore(params = {}) {
  const url = new URL(DATASTORE_URL);

  url.searchParams.set('resource_id', RESOURCE_ID);
  url.searchParams.set('limit', params.limit || LIMITE_PADRAO);
  url.searchParams.set('offset', params.offset || 0);

  if (params.filters) {
    url.searchParams.set('filters', JSON.stringify(params.filters));
  }

  const resp = await fetch(url.toString());
  if (!resp.ok) {
    throw new Error('Erro ao consultar DataStore');
  }

  const json = await resp.json();
  if (!json.success) {
    throw new Error('Resposta inválida do CKAN');
  }

  return json.result.records;
}

// ============================================
// VISÃO GERAL
// ============================================
async function carregarVisaoGeral() {
  const tbody = document.querySelector('#tabela-visao-geral tbody');
  tbody.innerHTML = '';

  // Exemplo: filtrar apenas servidores ativos
  const registros = await consultarDataStore({
    limit: 500
  });

  const agrupado = {};

  registros.forEach(r => {
    const sigla = r.sigla_instituicao_lotacao || 'N/I';
    const nome = r.desc_instituicao_lotacao || 'Não informado';

    if (!agrupado[sigla]) {
      agrupado[sigla] = { nome, total: 0 };
    }
    agrupado[sigla].total++;
  });

  Object.entries(agrupado).forEach(([sigla, info]) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${sigla}</td>
      <td>${info.nome}</td>
      <td>${info.total}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================
// DASHBOARD DETALHADO
// ============================================
async function carregarDetalhado() {
  const tbody = document.querySelector('#tabela-detalhada tbody');
  tbody.innerHTML = '';

  const registros = await consultarDataStore({
    limit: 1000
  });

  registros.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.masp || ''}</td>
      <td>${r.nome || ''}</td>
      <td>${r.sigla_instituicao_lotacao || ''}</td>
      <td>${r.nmefetivo || ''}</td>
      <td>${r.carga_horaria || ''}</td>
      <td>${r.descsitserv || ''}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================
// INICIALIZAÇÃO
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    console.log('🚀 Iniciando dashboard (DataStore)');
    await carregarVisaoGeral();
    await carregarDetalhado();
  } catch (e) {
    console.error(e);
    alert('Erro ao carregar dados do DataStore');
  }
});
