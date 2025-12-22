// ============================================
// CONFIGURAÇÃO
// ============================================
const DATAPACKAGE_URL = './datapackage.json';
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
    throw new Error('Erro ao carregar datapackage.json');
  }
  return await resp.json();
}

// ============================================
// INDEXAR RECURSOS POR MÊS
// ============================================
function indexarRecursos(dp) {
  const mapa = {};

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
async function carregarMes(key) {
  const url = RECURSOS_POR_MES[key];
  if (!url) throw new Error(`Mês ${key} não disponível`);

  console.log('📄 Carregando CSV:', url);

  const resp = await fetch(CORS_PROXY + encodeURIComponent(url));
  if (!resp.ok) throw new Error('Erro ao baixar CSV');

  const csv = await resp.text();

  Papa.parse(csv, {
    header: true,
    skipEmptyLines: true,
    complete: results => {
      servidoresData = results.data;
      allData[key] = servidoresData;

      console.log(`✅ ${key}: ${servidoresData.length} registros`);
    },
    error: err => {
      console.error('Erro no parse CSV:', err);
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
    RECURSOS_POR_MES = indexarRecursos(dp);

    const mesMaisRecente = Object.keys(RECURSOS_POR_MES).sort().pop();
    console.log('📅 Mês mais recente:', mesMaisRecente);

    await carregarMes(mesMaisRecente);

  } catch (e) {
    console.error('Erro ao inicializar:', e);
  }
});
