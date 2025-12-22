const URL_SERVIDORES =
  "https://dados.mg.gov.br/dataset/relacao_nominal_servidores/resource/UUID/download/dados_serv_202510.csv";

fetch(URL_SERVIDORES)
  .then(r => r.text())
  .then(csv => {
    console.log("CSV carregado do dados.mg");
  });
