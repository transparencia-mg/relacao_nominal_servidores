import json
import os
import re
import time
import requests
import psycopg2
from io import StringIO

# ==================================================
# CONFIGURAÇÕES
# ==================================================
DATAPACKAGE_PATH = "datapackage/datapackage.json"

HEADERS = {
    "User-Agent": "relacao-nominal-servidores/1.0 (contato: dados@mg.gov.br)",
    "Accept": "text/csv"
}

TENTATIVAS_MAX = 3
ESPERA_ENTRE_TENTATIVAS = 15  # segundos

# ==================================================
# CONEXÃO POSTGRES
# ==================================================
conn = psycopg2.connect(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PASSWORD"],
    port=os.environ.get("PG_PORT", 5432)
)

cur = conn.cursor()

# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================
def mes_ja_importado(ano_mes):
    cur.execute(
        "SELECT 1 FROM servidores WHERE ano_mes = %s LIMIT 1",
        (ano_mes,)
    )
    return cur.fetchone() is not None


def importar_csv(url, ano_mes):
    for tentativa in range(1, TENTATIVAS_MAX + 1):
        try:
            print(f"\n📥 Baixando ({tentativa}/{TENTATIVAS_MAX}) {url}")

            resp = requests.get(url, headers=HEADERS, timeout=180)
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
            print(f"✅ Mês {ano_mes} importado com sucesso")
            return

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro ao baixar/importar {ano_mes}: {e}")

            if tentativa == TENTATIVAS_MAX:
                print(f"❌ Falha definitiva no mês {ano_mes}. Pulando.")
                return

            print(f"⏳ Aguardando {ESPERA_ENTRE_TENTATIVAS}s para nova tentativa…")
            time.sleep(ESPERA_ENTRE_TENTATIVAS)


# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================
print("📦 Lendo datapackage.json")

with open(DATAPACKAGE_PATH, encoding="utf-8") as f:
    datapackage = json.load(f)

resources = datapackage.get("resources", [])
print(f"🔎 {len(resources)} recursos encontrados no datapackage")

for r in resources:
    nome = r.get("name", "")
    url = r.get("url")

    if not nome.startswith("dados_serv_") or not nome.endswith(".csv"):
        continue

    match = re.search(r"dados_serv_(\d{6})\.csv", nome)
    if not match:
        continue

    ano_mes = match.group(1)

    if mes_ja_importado(ano_mes):
        print(f"⏭️ Mês {ano_mes} já existe no banco, pulando")
        continue

    importar_csv(url, ano_mes)

cur.close()
conn.close()

print("\n🎉 Importação finalizada")


