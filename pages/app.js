async function carregarCSV(url) {
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`Erro ao carregar ${url}`);
  const texto = await resp.text();
  return texto.split('\n').slice(1).map(l => l.split(';'));
}

async function carregarVisaoGeral() {
  const linhas = await carregarCSV('../data/servidores_visao_geral.csv');
  const tbody = document.querySelector('#tabela-visao-geral tbody');

  linhas.forEach(l => {
    if (l.length < 3) return;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${l[0]}</td>
      <td>${l[1]}</td>
      <td>${l[2]}</td>
    `;
    tbody.appendChild(tr);
  });
}

async function carregarDetalhado() {
  const linhas = await carregarCSV('../data/servidores_detalhado.csv');
  const tbody = document.querySelector('#tabela-detalhada tbody');

  linhas.slice(0, 1000).forEach(l => {
    if (l.length < 6) return;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${l[0]}</td>
      <td>${l[1]}</td>
      <td>${l[2]}</td>
      <td>${l[3]}</td>
      <td>${l[4]}</td>
      <td>${l[5]}</td>
    `;
    tbody.appendChild(tr);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    await carregarVisaoGeral();
    await carregarDetalhado();
  } catch (e) {
    console.error(e);
    alert('Erro ao carregar dados');
  }
});

