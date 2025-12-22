#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gera datapackage.json para o dataset
'Relação Nominal de Servidores', usando:

- Recursos já publicados no dados.mg.gov.br (CKAN)
- Hash SHA-256 previamente calculado
- Schema EMBUTIDO em cada resource (frictionless)
- Nenhum CSV armazenado no GitHub
"""

import json
import requests
from pathlib import Path

# ===============================
# CONFIGURAÇÕES
# ===============================

CKAN_HOST = "https://dados.mg.gov.br"
DATASET_ID = "relacao_nominal_servidores"

HASHES_FILE = Path("datapackage/hashes.json")
OUTPUT_FILE = Path("datapackage/datapackage.json")

# ===============================
# SCHEMA EMBUTIDO (dados_serv_YYYYMM.csv)
# ===============================

SCHEMA_DADOS_SERV = {
    "fields": [
        {"name": "ano_mes", "type": "string"},
        {"name": "masp", "type": "string"},
        {"name": "adm", "type": "string"},
        {"name": "nome", "type": "string"},
        {"name": "siglaefetivo", "type": "string"},
        {"name": "nmefetivo", "type": "string"},
        {"name": "cdcomi", "type": "string"},
        {"name": "desccomi", "type": "string"},
        {"name": "cd_funcao_gratif_gte", "type": "string"},
        {"name": "desc_funcao_gratif_gte", "type": "string"},
        {"name": "carga_horaria", "type": "string"},
        {"name": "descsitserv", "type": "string"}
    ],
    "missingValues": [""]
}

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def carregar_hashes():
    if not HASHES_FILE.exists():
        raise RuntimeError("Arquivo datapackage/hashes.json não encontrado")

    return json.loads(HASHES_FILE.read_text(encoding="utf-8"))


def buscar_resources_ckan():
    url = f"{CKAN_HOST}/api/3/action/package_show?id={DATASET_ID}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()["result"]["resources"]


# ===============================
# MAIN
# ===============================

def main():
    print("📦 Gerando datapackage.json")

    hashes = carregar_hashes()
    resources_ckan = buscar_resources_ckan()

    resources = []

    for r in resources_ckan:
        name = r.get("name")
        download_url = r.get("url")

        if not name or not download_url:
            continue

        # Ignora arquivos que não são CSV de servidores
        if not name.startswith("dados_serv_") or not name.endswith(".csv"):
            print(f"⏭️ Ignorado: {name}")
            continue

        hash_value = hashes.get(name)

        if not hash_value:
            print(f"⚠️ Hash não encontrado para {name}")
            continue

        resource = {
            "name": name.replace(".csv", ""),
            "title": f"Relação Nominal de Servidores – {name[-10:-4]}",
            "format": "csv",
            "mediatype": "text/csv",
            "path": download_url,
            "hash": hash_value,
            "schema": SCHEMA_DADOS_SERV
        }

        resources.append(resource)
        print(f"✅ Adicionado: {name}")

    datapackage = {
        "name": "relacao-nominal-servidores",
        "title": "Relação Nominal de Servidores do Estado de Minas Gerais",
        "profile": "data-package",
        "resources": resources
    }

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(datapackage, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"🎉 datapackage.json gerado em {OUTPUT_FILE}")
    print(f"📊 Total de recursos: {len(resources)}")


if __name__ == "__main__":
    main()

