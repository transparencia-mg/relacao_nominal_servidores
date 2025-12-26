// ============================================
// CONFIGURAÇÃO
// ============================================

// ⚠️ GitHub Pages: docs/ vira a raiz do site
const DATAPACKAGE_URL = '/relacao_nominal_servidores/datapackage.json';

// Proxy para CSVs do CKAN
const CORS_PROXY = 'https://corsproxy.io/?';

let servidoresData = [];
let allData = {};
let RECURSOS_POR_MES = {};

// ============================================
// CARREGAR DATAPACKAGE
// ============================================
async function carregarDatapackage() {
  const resp = await fetch(DATAPACKAGE_URL);

  if (!resp.ok) {
    throw new Error(`Erro ao carregar datapackage.json (${resp.status})`);
  }

  return await resp.json();
}

// ============================================
// INDEXAR RECURSOS POR MÊS
// ============================================
function indexarRecursos(dp) {
  const mapa = {};

  if (!dp.resources || !Array.isArray(dp.resources)) {
    throw new Error('Datapackage inválido: resources não encontrado');
  }

  dp.resources.forEach(r => {
    const match = r.name && r.name.match(/dados_serv_(\d{6})/);
    if (match && r.url) {
      mapa[match[1]] = r.url;
    }
  });

  return mapa;
}

// ============================================
// CARREGAR CSV DE UM MÊS
// ============================================
async function carregarMes(anoMes) {
  const url = RECURSOS_POR_MES[anoMes];
  if (!url) {
    throw new Error(`Mês ${anoMes} não disponível`);
  }

  console.log('📄 Carregando CSV:', url);

  const resp = await fetch(CORS_PROXY + encodeURIComponent(url));
  if (!resp.ok) {
    throw new Error(`Erro ao baixar CSV (${resp.status})`);
  }

  const csv = await resp.text();

  Papa.parse(csv, {
    header: true,
    skipEmptyLines: true,
    complete: results => {
      servidoresData = results.data;
      allData[anoMes] = servidoresData;

      console.log(`✅ ${anoMes}: ${servidoresData.length} registros`);
    },
    error: err => {
      console.error('❌ Erro no parse do CSV:', err);
    }
  });
}

// ============================================
// INICIALIZAÇÃO
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
  try {
    console.log('=== INICIANDO DASHBOARD SERVIDORES ===');

    const dp = await carregarDatapackage();
    console.log('📦 Datapackage carregado');

    RECURSOS_POR_MES = indexarRecursos(dp);

    const meses = Object.keys(RECURSOS_POR_MES).sort();
    if (meses.length === 0) {
      throw new Error('Nenhum mês disponível no datapackage');
    }

    const mesMaisRecente = meses[meses.length - 1];
    console.log('📅 Mês mais recente:', mesMaisRecente);

    await carregarMes(mesMaisRecente);

  } catch (e) {
    console.error('❌ Erro ao inicializar:', e);
  }
});

