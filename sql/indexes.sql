CREATE INDEX IF NOT EXISTS idx_servidores_ano_mes
  ON servidores (ano_mes);

CREATE INDEX IF NOT EXISTS idx_servidores_masp
  ON servidores (masp);

CREATE INDEX IF NOT EXISTS idx_servidores_sigla_lotacao
  ON servidores (sigla_instituicao_lotacao);

