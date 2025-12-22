const urlCKAN =
  "https://dados.mg.gov.br/dataset/relacao_nominal_servidores/resource/dc57c390-dda8-4360-8bfb-0474231108cd/download/dados_serv_202501.csv";

const urlComProxy = "https://corsproxy.io/?" + encodeURIComponent(urlCKAN);

fetch(urlComProxy)
  .then(r => r.text())
  .then(csv => {
    console.log("CSV carregado com sucesso");
  });
