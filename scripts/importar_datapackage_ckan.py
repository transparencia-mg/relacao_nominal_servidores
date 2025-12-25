import json
import os
import requests
import psycopg2
from io import StringIO
import re

# =====================================
# CONFIGURAÇÕES
# =====================================
DATAPACKAGE_PATH = "datapackage/datapackage.json"

# =====================================
# CONEXÃO POSTGRES
# =====================================
conn = psycopg2.connect(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PASSWORD"],
    port=os.environ.get("PG_PORT", 5432)
)

cur = conn.cursor()

# =====================================
# FUNÇÕES AUXILIARES
# =====================================
def mes_ja_importado(ano_mes):
    cur.execute(
        "SELECT 1 FROM servidores WHERE ano_mes = %s LIMIT 1",
        (ano_mes,)
    )
    return cur.fetchone() is not None


def importar_csv(url, ano_mes):
    print(f"📥 Baixando {url}")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    buffer = StringIO(resp.text)

    print(f"📤 Importando dados do mês {ano_mes}")

    cur.copy_expert("""
        COPY servidores (
            ano_mes,
            masp,
            adm,
            nome,
            siglaefetivo,
            nmefetivo,
            cdcomi,
            desccomi,
            cd_funcao_gratif_gte,
            desc_funcao_gratif_gte,
            carga_horaria,
            cd_instituicao_dotacao,
            sigla_instituicao_dotacao,
            desc_instituicao_dotacao,
            cd_instituicao_lotacao,
            sigla_instituicao_lotacao,
            desc_instituicao_lotacao,
            descsitserv,
            data_inicio,
            data_aposentadoria,
            data_desligamento
        )
        FROM STDIN
        WITH CSV
        HEADER
        DELIMITER ';'
        ENCODING 'UTF8'
    """, buffer)

    conn.commit()
    print(f"✅ Mês {ano_mes} importado")


# =====================================
# EXECUÇÃO
# =====================================
print("📦 Lendo datapackage.json")

with open(DATAPACKAGE_PATH, encoding="utf-8") as f:
    datapackage

