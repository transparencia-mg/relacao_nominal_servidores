CREATE OR REPLACE VIEW servidores_visao_geral AS
SELECT
  desc_instituicao_lotacao AS instituicao,
  sigla_instituicao_lotacao AS sigla,
  COUNT(*) AS quantidade_servidores
FROM servidores
GROUP BY
  desc_instituicao_lotacao,
  sigla_instituicao_lotacao
ORDER BY quantidade_servidores DESC;


CREATE OR REPLACE VIEW servidores_detalhado AS
SELECT
  masp,
  nome,
  desc_instituicao_lotacao AS instituicao,
  nmefetivo AS cargo_efetivo,
  carga_horaria,
  descsitserv
FROM servidores;
